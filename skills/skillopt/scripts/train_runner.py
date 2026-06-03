"""Runner script for local Agents rules optimization.

Monkeypatches SkillOpt model backends to redirect calls to Gemini and
registers the custom `agents_opt` benchmark environment.
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Any

# Ensure parent and package paths are accessible
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_SKILLOPT_DIR = os.path.dirname(_SCRIPT_DIR)
_SKILLS_DIR = os.path.dirname(_SKILLOPT_DIR)
_AGENTS_DIR = os.path.dirname(_SKILLS_DIR)

if _AGENTS_DIR not in sys.path:
    sys.path.insert(0, _AGENTS_DIR)


def custom_load_prompt(name: str, env: str | None = None) -> str:
    """Provides memory-based fallbacks for required prompts.

    Bypasses local file reads to prevent FileNotFoundError since prompt md
    files are not packaged in the PyPI distribution.

    Args:
        name: Name of the prompt file requested.
        env: Environment name context.

    Returns:
        The prompt string.
    """
    del env
    prompts = {
        "analyst_error": (
            "You are an expert rules analyst. Review the failed trajectories "
            "and identify why the rules failed to produce the correct behavior. "
            "Propose edits in JSON format.\n"
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
        ),
        "analyst_success": (
            "You are an expert rules analyst. Review the successful trajectories "
            "and reinforce the current rules.\n"
            "Propose edits in JSON format to clarify the rules further if needed.\n"
            "Your output must be a JSON object containing a \"patch\" key with "
            "a list of \"edits\", as described in the failure prompt."
        ),
        "merge_failure": (
            "You are a rules merger. Merge the following proposed edits for "
            "failures into a single cohesive patch.\n"
            "Your output must be a JSON object containing a \"patch\" key with "
            "a list of \"edits\"."
        ),
        "merge_success": (
            "You are a rules merger. Merge the following proposed edits for "
            "successes into a single cohesive patch.\n"
            "Your output must be a JSON object containing a \"patch\" key with "
            "a list of \"edits\"."
        ),
        "merge_final": (
            "You are a rules merger. Merge the failure and success patches "
            "into a final consolidated patch.\n"
            "Your output must be a JSON object containing a \"patch\" key with "
            "a list of \"edits\"."
        ),
        "rewrite_skill": (
            "You are an instruction writer. Rewrite the instruction/rules "
            "document to incorporate the following suggestions.\n"
            "Your output must be the complete updated markdown text."
        ),
        "lr_autonomous": (
            "Determine the best learning rate (edit budget) based on "
            "training progress. Return a single number between 1 and 8."
        ),
        "slow_update": (
            "Decide if the proposed rule update should be accepted based "
            "on the evaluation scores. Return JSON with 'accept': true or false."
        ),
        "meta_skill": (
            "Analyze the history of rule optimizations and summarize "
            "key insights to guide future steps."
        ),
    }

    base_name = name
    for suffix in ["_rewrite", "_full_rewrite"]:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    if base_name in prompts:
        return prompts[base_name]

    return (
        f"You are a helpful assistant executing the '{name}' task. "
        "Please output the appropriate JSON format with 'patch' or "
        "text replacement."
    )


def apply_monkeypatches(cfg: dict[str, Any]) -> None:
    """Applies necessary runtime monkeypatches to SkillOpt modules.

    Args:
        cfg: The parsed configurations.
    """
    # 1. Intercept prompt loading
    import skillopt.prompts
    import skillopt.gradient.reflect
    import skillopt.envs.base

    skillopt.prompts.load_prompt = custom_load_prompt
    skillopt.gradient.reflect.load_prompt = custom_load_prompt
    skillopt.envs.base.load_prompt = custom_load_prompt

    # 2. Redirect models to Gemini unless Claude is requested
    optimizer_backend = cfg.get("model_backend") or cfg.get("optimizer_backend") or ""
    is_claude = "claude" in str(optimizer_backend).lower()

    if not is_claude:
        # Set env variables for our gemini backend
        os.environ["OPTIMIZER_MODEL"] = str(cfg.get("optimizer_model") or "gemini-1.5-flash")
        os.environ["TARGET_MODEL"] = str(cfg.get("target_model") or "gemini-1.5-flash")

        import skillopt.model.azure_openai as ao
        from skills.skillopt.scripts import gemini_backend

        ao.chat_optimizer = gemini_backend.chat_optimizer
        ao.chat_target = gemini_backend.chat_target
        ao.chat_optimizer_messages = gemini_backend.chat_optimizer_messages
        ao.chat_target_messages = gemini_backend.chat_target_messages
        ao.chat_with_deployment = gemini_backend.chat_with_deployment
        ao.chat_messages_with_deployment = gemini_backend.chat_messages_with_deployment


def main() -> None:
    """Main entrypoint wrapper for the SkillOpt training process."""
    from skills.skillopt.scripts.env import AgentsOptEnv

    # Check if we are running in evaluation-only mode
    is_eval = "--skill" in sys.argv

    if is_eval:
        import scripts.eval_only
        scripts.eval_only._ENV_REGISTRY["agents_opt"] = AgentsOptEnv
        # Locate the config file from sys.argv
        cfg_path = ""
        for i, arg in enumerate(sys.argv):
            if arg == "--config" and i + 1 < len(sys.argv):
                cfg_path = sys.argv[i + 1]
                break
        from skillopt.config import load_config
        cfg = load_config(cfg_path) if cfg_path else {}
    else:
        import scripts.train
        scripts.train._ENV_REGISTRY["agents_opt"] = AgentsOptEnv
        args = scripts.train.parse_args()
        cfg = scripts.train.load_config(args)

    # Apply all runtime patches
    apply_monkeypatches(cfg)

    # Run the correct main loop
    if is_eval:
        print("Launching SkillOpt in Evaluation-Only mode...")
        import scripts.eval_only
        scripts.eval_only.main()
    else:
        print("Launching SkillOpt with custom monkeypatched backend...")
        import scripts.train
        scripts.train.main()


if __name__ == "__main__":
    main()
