"""Gemini API model backend adapter for SkillOpt.

This module maps standard chat target and optimizer calls onto the official
Google GenAI SDK.
"""

from __future__ import annotations

import logging
import os
from typing import Any

import google.generativeai as genai
from skillopt.model.common import CompatAssistantMessage, tracker

logger = logging.getLogger(__name__)


def _init_client() -> None:
    """Configures the google.generativeai client using env keys."""
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        logger.warning("No GEMINI_API_KEY or GOOGLE_API_KEY found in environment.")
    genai.configure(api_key=api_key)


_init_client()


def _format_messages(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Translates standard role/content messages to Gemini contents format.

    Args:
        messages: List of message dictionaries containing role and content.

    Returns:
        Formatted contents matching the Google GenAI SDK requirements.
    """
    contents = []
    for msg in messages:
        role = msg.get("role", "user")
        # Map assistant -> model
        if role == "assistant":
            role = "model"
        contents.append({
            "role": role,
            "parts": [msg.get("content", "")]
        })
    return contents


def _is_retryable_gemini_error(err_str: str) -> bool:
    """True if `err_str` indicates a Gemini rate-limit/quota error.

    Args:
        err_str: String representation of the raised exception.

    Returns:
        True when the error looks like a transient rate-limit condition.
    """
    return (
        "429" in err_str
        or "Quota exceeded" in err_str
        or "limit" in err_str
        or "ResourceExhausted" in err_str
    )


def _handle_gemini_retry_error(error: Exception, attempt: int, max_retries: int) -> None:
    """Sleeps on a retryable Gemini error, or re-raises the original error.

    Module-level (not inlined in `_call_gemini`) so this if/raise does not
    stack a third nesting level on top of the caller's for/try.

    Args:
        error: The exception raised by the Gemini API call.
        attempt: Zero-based index of the current retry attempt.
        max_retries: Total number of retries configured for the caller.

    Raises:
        Exception: the original `error`, re-raised unchanged, when it is
            not a retryable rate limit.
    """
    import time

    err_str = str(error)
    if not _is_retryable_gemini_error(err_str):
        raise error
    sleep_time = 62
    logger.warning(
        "Gemini API rate limit (429) hit. Retrying in %d seconds... (Attempt %d/%d). Error: %s",
        sleep_time,
        attempt + 1,
        max_retries,
        err_str
    )
    time.sleep(sleep_time)


def _call_gemini(
    messages: list[dict[str, Any]],
    model_name: str,
    system_instruction: str | None = None
) -> tuple[str, dict[str, int]]:
    """Helper method to invoke the model generation and record tokens.

    Args:
        messages: Input message history.
        model_name: The target model name.
        system_instruction: Optional system instructions.

    Returns:
        A tuple of the response text and the token usage dict.
    """
    contents = _format_messages(messages)
    max_retries = 5
    response = None

    for attempt in range(max_retries):
        try:
            model = genai.GenerativeModel(
                model_name=model_name or "gemini-2.5-flash",
                system_instruction=system_instruction
            )
            response = model.generate_content(
                contents=contents,
                generation_config={"temperature": 0.0}
            )
            break
        except Exception as e:
            logger.debug("Gemini call attempt %d failed", attempt + 1, exc_info=True)
            _handle_gemini_retry_error(e, attempt, max_retries)
    else:
        raise RuntimeError("Max retries exceeded for Gemini API call due to rate limits.")

    # Extract token usage
    usage = response.usage_metadata if response else None
    prompt_tokens = usage.prompt_token_count if usage else 0
    completion_tokens = usage.candidates_token_count if usage else 0
    
    meta = {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": prompt_tokens + completion_tokens
    }
    return (response.text if response else "") or "", meta


def chat_optimizer(
    system: str,
    user: str,
    max_completion_tokens: int = 16384,
    retries: int = 5,
    stage: str = "optimizer",
    reasoning_effort: str | None = None,
    timeout: int | None = None
) -> tuple[str, dict[str, int]]:
    """Redirects optimizer generation to Gemini."""
    del max_completion_tokens, retries, reasoning_effort, timeout
    messages = [{"role": "user", "content": user}]
    model_name = os.environ.get("OPTIMIZER_DEPLOYMENT") or os.environ.get("OPTIMIZER_MODEL") or "gemini-2.5-flash"
    
    text, meta = _call_gemini(messages, model_name, system_instruction=system)
    tracker.record(stage, meta["prompt_tokens"], meta["completion_tokens"])
    return text, meta


def chat_target(
    system: str,
    user: str,
    max_completion_tokens: int = 16384,
    retries: int = 5,
    stage: str = "target",
    reasoning_effort: str | None = None,
    timeout: int | None = None
) -> tuple[str, dict[str, int]]:
    """Redirects target generation to Gemini."""
    del max_completion_tokens, retries, reasoning_effort, timeout
    messages = [{"role": "user", "content": user}]
    model_name = os.environ.get("TARGET_DEPLOYMENT") or os.environ.get("TARGET_MODEL") or "gemini-2.5-flash"
    
    text, meta = _call_gemini(messages, model_name, system_instruction=system)
    tracker.record(stage, meta["prompt_tokens"], meta["completion_tokens"])
    return text, meta


def chat_optimizer_messages(
    messages: list[dict[str, Any]],
    max_completion_tokens: int = 16384,
    retries: int = 5,
    stage: str = "optimizer",
    reasoning_effort: str | None = None,
    *,
    tools: list[dict[str, Any]] | None = None,
    tool_choice: str | dict[str, Any] | None = None,
    return_message: bool = False,
    timeout: int | None = None
) -> tuple[Any, dict[str, int]]:
    """Redirects list messages optimizer calls to Gemini."""
    del max_completion_tokens, retries, reasoning_effort, tools, tool_choice, timeout
    model_name = os.environ.get("OPTIMIZER_MODEL", "gemini-1.5-flash")
    
    text, meta = _call_gemini(messages, model_name)
    tracker.record(stage, meta["prompt_tokens"], meta["completion_tokens"])
    
    if return_message:
        return CompatAssistantMessage(content=text), meta
    return text, meta


def chat_target_messages(
    messages: list[dict[str, Any]],
    max_completion_tokens: int = 16384,
    retries: int = 5,
    stage: str = "target",
    reasoning_effort: str | None = None,
    *,
    tools: list[dict[str, Any]] | None = None,
    tool_choice: str | dict[str, Any] | None = None,
    return_message: bool = False,
    timeout: int | None = None
) -> tuple[Any, dict[str, int]]:
    """Redirects list messages target calls to Gemini."""
    del max_completion_tokens, retries, reasoning_effort, tools, tool_choice, timeout
    model_name = os.environ.get("TARGET_MODEL", "gemini-1.5-flash")
    
    text, meta = _call_gemini(messages, model_name)
    tracker.record(stage, meta["prompt_tokens"], meta["completion_tokens"])
    
    if return_message:
        return CompatAssistantMessage(content=text), meta
    return text, meta


def chat_with_deployment(
    deployment: str,
    system: str,
    user: str,
    max_completion_tokens: int = 16384,
    retries: int = 5,
    stage: str = "custom",
    reasoning_effort: str | None = None,
    timeout: int | None = None
) -> tuple[str, dict[str, int]]:
    """Redirects chat with deployment calls to Gemini."""
    del deployment, max_completion_tokens, retries, reasoning_effort, timeout
    messages = [{"role": "user", "content": user}]
    model_name = os.environ.get("TARGET_DEPLOYMENT") or os.environ.get("TARGET_MODEL") or "gemini-2.5-flash"
    
    text, meta = _call_gemini(messages, model_name, system_instruction=system)
    tracker.record(stage, meta["prompt_tokens"], meta["completion_tokens"])
    return text, meta


def chat_messages_with_deployment(
    deployment: str,
    messages: list[dict[str, Any]],
    max_completion_tokens: int = 16384,
    retries: int = 5,
    stage: str = "custom",
    reasoning_effort: str | None = None,
    *,
    tools: list[dict[str, Any]] | None = None,
    tool_choice: str | dict[str, Any] | None = None,
    return_message: bool = False,
    timeout: int | None = None
) -> tuple[Any, dict[str, int]]:
    """Redirects chat messages with deployment calls to Gemini."""
    del deployment, max_completion_tokens, retries, reasoning_effort, tools, tool_choice, timeout
    model_name = os.environ.get("TARGET_DEPLOYMENT") or os.environ.get("TARGET_MODEL") or "gemini-2.5-flash"
    
    text, meta = _call_gemini(messages, model_name)
    tracker.record(stage, meta["prompt_tokens"], meta["completion_tokens"])
    
    if return_message:
        return CompatAssistantMessage(content=text), meta
    return text, meta

