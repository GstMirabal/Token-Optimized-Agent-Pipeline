"""Environment adapter for Agents rules optimization.

Runs rollouts of target rules on mock scenarios, scores model output,
writes trajectories, and handles the reflection process.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any

from skillopt.datasets.base import BatchSpec
from skillopt.envs.base import EnvAdapter
from skillopt.model.router import chat_target


class AgentsOptEnv(EnvAdapter):
    """Adapter for testing and evaluating agents governance rules."""

    def __init__(
        self,
        split_dir: str = "",
        data_path: str = "",
        split_mode: str = "ratio",
        split_ratio: str = "2:1:7",
        split_seed: int = 42,
        split_output_dir: str = "",
        workers: int = 4,
        analyst_workers: int = 4,
        failure_only: bool = False,
        minibatch_size: int = 8,
        edit_budget: int = 4,
        seed: int = 42,
        limit: int = 0,
        max_completion_tokens: int = 4096,
        **kwargs: Any,
    ) -> None:
        """Initializes the environment adapter and the custom dataloader.

        Args:
            split_dir: Directory containing pre-split data.
            data_path: Path to the raw JSON scenarios file.
            split_mode: Mode to split the dataset (ratio or split_dir).
            split_ratio: Train:val:test ratio.
            split_seed: Seed for the split.
            split_output_dir: Output directory for split files.
            workers: Number of rollout workers.
            analyst_workers: Number of reflection workers.
            failure_only: If True, reflect only on failure trajectories.
            minibatch_size: Size of minibatches for reflection.
            edit_budget: Maximum edits per update step.
            seed: Random seed.
            limit: Limit the number of loaded items.
            max_completion_tokens: Max target model output tokens.
            kwargs: Extra keyword arguments.
        """
        self.workers = workers
        self.analyst_workers = analyst_workers
        self.failure_only = failure_only
        self.minibatch_size = minibatch_size
        self.edit_budget = edit_budget
        self.max_completion_tokens = int(max_completion_tokens)

        from skills.skillopt.scripts.dataloader import AgentsOptDataLoader

        self.dataloader = AgentsOptDataLoader(
            split_dir=split_dir,
            data_path=data_path,
            split_mode=split_mode,
            split_ratio=split_ratio,
            split_seed=split_seed,
            split_output_dir=split_output_dir,
            seed=seed,
            limit=limit,
        )

    def setup(self, cfg: dict[str, Any]) -> None:
        """Sets up the environment configuration.

        Args:
            cfg: Dictionary containing training parameters.
        """
        super().setup(cfg)
        self.dataloader.setup(cfg)

    def get_dataloader(self) -> AgentsOptDataLoader:
        """Returns the active dataloader.

        Returns:
            The dataloader instance.
        """
        return self.dataloader

    def build_env_from_batch(
        self, batch: BatchSpec, **kwargs: Any
    ) -> list[dict[str, Any]]:
        """Extracts items from the BatchSpec.

        Args:
            batch: The batch specifications.
            kwargs: Extra parameters.

        Returns:
            A list of scenario dictionaries.
        """
        return list(batch.payload or [])

    def build_train_env(
        self, batch_size: int, seed: int, **kwargs: Any
    ) -> list[dict[str, Any]]:
        """Constructs the training split payload.

        Args:
            batch_size: Number of training items.
            seed: Random seed.
            kwargs: Extra parameters.

        Returns:
            A list of training scenario dictionaries.
        """
        batch = self.dataloader.build_train_batch(
            batch_size=batch_size, seed=seed, **kwargs
        )
        return self.build_env_from_batch(batch, **kwargs)

    def build_eval_env(
        self, env_num: int, split: str, seed: int, **kwargs: Any
    ) -> list[dict[str, Any]]:
        """Constructs the evaluation split payload.

        Args:
            env_num: Number of evaluation items.
            split: Dataset split identifier.
            seed: Random seed.
            kwargs: Extra parameters.

        Returns:
            A list of evaluation scenario dictionaries.
        """
        batch = self.dataloader.build_eval_batch(
            env_num=env_num, split=split, seed=seed, **kwargs
        )
        return self.build_env_from_batch(batch, **kwargs)

    def _call_target_safe(self, system: str, user: str) -> str:
        """Invokes chat_target catching any exception.

        Args:
            system: System instructions.
            user: User input.

        Returns:
            The response string.
        """
        try:
            pred_answer, _ = chat_target(
                system=system,
                user=user,
                max_completion_tokens=self.max_completion_tokens,
                stage="target_rollout",
            )
            return pred_answer
        except Exception as e:
            logging.error("Target model execution failed: %s", e)
            return ""

    def _grade_prediction(self, question: str, gold: str, pred: str) -> tuple[int, float, str]:
        """Grades the prediction against the ground truth.

        Args:
            question: Scenario description.
            gold: Expected ground truth.
            pred: Actual prediction.

        Returns:
            A tuple of hard score (0/1), soft score (0.0-1.0), and reason.
        """
        eval_system = (
            "You are an automated evaluation judge.\n"
            "Compare the Model Prediction with the expected Ground Truth for "
            "a rule validation scenario.\n"
            "The Ground Truth specifies why a code change or proposal is "
            "non-compliant with the rules.\n"
            "Determine if the Model Prediction correctly identified that the "
            "proposal is non-compliant and gave a reason matching the Ground Truth.\n"
            "Respond with exactly:\n"
            "- hard: 1 (if correct) or 0 (if incorrect)\n"
            "- soft: 1.0 (if correct) or 0.0 (if incorrect)\n"
            "- reasoning: a brief explanation of why.\n"
            "Format your output as a JSON block:\n"
            "```json\n"
            "{\n"
            "  \"hard\": 1,\n"
            "  \"soft\": 1.0,\n"
            "  \"reasoning\": \"...\"\n"
            "}\n"
            "```"
        )
        eval_user = (
            f"## Question\n{question}\n\n"
            f"## Expected Ground Truth\n{gold}\n\n"
            f"## Model Prediction\n{pred}"
        )
        try:
            eval_response, _ = chat_target(
                system=eval_system,
                user=eval_user,
                max_completion_tokens=1024,
                stage="eval_judge",
            )
            from skillopt.gradient.reflect import extract_json

            eval_json = extract_json(eval_response)
            if eval_json:
                hard = int(eval_json.get("hard", 0))
                soft = float(eval_json.get("soft", 0.0))
                reason = eval_json.get("reasoning", "")
                return hard, soft, reason
        except Exception as e:
            logging.error("Grading prediction failed: %s", e)
        return 0, 0.0, "Grading process encountered an error."

    def rollout(
        self,
        env_manager: Any,
        skill_content: str,
        out_dir: str,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """Evaluates the scenarios and records the conversation histories.

        Args:
            env_manager: List of scenarios to run.
            skill_content: The rules under test.
            out_dir: Output directory.
            kwargs: Extra parameters.

        Returns:
            A list of rollout results.
        """
        items: list[dict[str, Any]] = env_manager
        results: list[dict[str, Any]] = []
        pred_dir = os.path.join(out_dir, "predictions")

        for item in items:
            question = item.get("question", "")
            gold = item.get("ground_truth", "")
            item_id = item.get("id", "")

            pred = self._call_target_safe(skill_content, question)
            hard, soft, reason = self._grade_prediction(question, gold, pred)

            os.makedirs(os.path.join(pred_dir, str(item_id)), exist_ok=True)
            conv_path = os.path.join(pred_dir, str(item_id), "conversation.json")
            conv = [
                {"role": "user", "content": question},
                {"role": "assistant", "content": pred},
            ]
            try:
                with open(conv_path, "w", encoding="utf-8") as f:
                    json.dump(conv, f, indent=2)
            except Exception as e:
                logging.error("Failed to save conversation: %s", e)

            results.append({
                "id": str(item_id),
                "hard": hard,
                "soft": soft,
                "predicted_answer": pred,
                "question": question,
                "fail_reason": reason,
                "task_description": question,
                "task_type": item.get("task_type", "general_rule"),
                "reference_text": gold,
                "target_system_prompt": skill_content,
            })
        return results

    def reflect(
        self,
        results: list[dict[str, Any]],
        skill_content: str,
        out_dir: str,
        **kwargs: Any,
    ) -> list[dict[str, Any] | None]:
        """Analyzes rollout results and generates patch suggestions.

        Args:
            results: Rollout evaluation outputs.
            skill_content: The current rules text.
            out_dir: Output directory.
            kwargs: Extra parameters.

        Returns:
            A list of patch dictionaries.
        """
        from skillopt.gradient.reflect import run_minibatch_reflect

        err_prompt = self.get_error_minibatch_prompt()
        succ_prompt = self.get_success_minibatch_prompt()
        pred_dir = kwargs.get("prediction_dir", os.path.join(out_dir, "predictions"))
        pat_dir = kwargs.get("patches_dir", os.path.join(out_dir, "patches"))

        return run_minibatch_reflect(
            results=results,
            skill_content=skill_content,
            prediction_dir=pred_dir,
            patches_dir=pat_dir,
            workers=self.analyst_workers,
            failure_only=self.failure_only,
            minibatch_size=self.minibatch_size,
            edit_budget=self.edit_budget,
            random_seed=kwargs.get("random_seed"),
            error_system=err_prompt,
            success_system=succ_prompt,
            step_buffer_context=kwargs.get("step_buffer_context", ""),
            update_mode=getattr(self, "_cfg", {}).get("skill_update_mode", "patch"),
        )

    def get_task_types(self) -> list[str]:
        """Returns the task types inside the dataset.

        Returns:
            List of task type strings.
        """
        seen: list[str] = []
        all_items = (
            self.dataloader.train_items
            + self.dataloader.val_items
            + self.dataloader.test_items
        )
        for item in all_items:
            tt = str(item.get("task_type") or "general_rule")
            if tt not in seen:
                seen.append(tt)
        return seen or ["general_rule"]

    def get_error_minibatch_prompt(self) -> str:
        """Returns the hardcoded error analyst prompt.

        Returns:
            Prompt text.
        """
        return (
            "You are a Governance Rules Analyst.\n"
            "Your task is to analyze failures in rule evaluation scenarios and "
            "propose changes to the system rules or skills (written in Markdown).\n\n"
            "Analyze the discrepancies. Identify where the rules were ambiguous, "
            "incomplete, or confusing. Suggest concrete improvements to the rules.\n"
            "Your output must be a JSON object containing a \"patch\" key with "
            "a list of \"edits\", where each edit has \"target\" (exact string "
            "in the skill to replace) and \"content\" (new string to insert).\n"
            "Ensure the target is unique in the original text.\n\n"
            "Example:\n"
            "```json\n"
            "{\n"
            "  \"patch\": {\n"
            "    \"edits\": [\n"
            "      {\n"
            "        \"target\": \"old rule text\",\n"
            "        \"content\": \"new rule text\"\n"
            "      }\n"
            "    ]\n"
            "  }\n"
            "}\n"
            "```"
        )

    def get_success_minibatch_prompt(self) -> str:
        """Returns the hardcoded success analyst prompt.

        Returns:
            Prompt text.
        """
        return (
            "You are a Governance Rules Analyst.\n"
            "Review the successful trajectories and reinforce the current rules.\n"
            "Propose edits in JSON format to clarify the rules further if needed.\n"
            "Your output must be a JSON object containing a \"patch\" key with "
            "a list of \"edits\", as described in the failure prompt."
        )
