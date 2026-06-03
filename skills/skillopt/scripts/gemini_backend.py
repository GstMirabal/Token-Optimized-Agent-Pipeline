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


def _init_client() -> None:
    """Configures the google.generativeai client using env keys."""
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        logging.warning("No GEMINI_API_KEY or GOOGLE_API_KEY found in environment.")
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
    model = genai.GenerativeModel(
        model_name=model_name or "gemini-2.5-flash",
        system_instruction=system_instruction
    )
    contents = _format_messages(messages)
    
    response = model.generate_content(
        contents=contents,
        generation_config={"temperature": 0.0}
    )
    
    # Extract token usage
    usage = response.usage_metadata
    prompt_tokens = usage.prompt_token_count if usage else 0
    completion_tokens = usage.candidates_token_count if usage else 0
    
    meta = {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": prompt_tokens + completion_tokens
    }
    return response.text or "", meta


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

