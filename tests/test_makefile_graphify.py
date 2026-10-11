"""Regression test for the Makefile graphify forms (Sprint 055 U08, D9)."""

from __future__ import annotations

import re
from pathlib import Path

MAKEFILE = Path(__file__).resolve().parent.parent / "Makefile"
CONSOLE_SCRIPT = re.compile(r"venv_skillopt/bin/graphify\b")


def _active_lines() -> list[str]:
    """Return the Makefile lines that are not comments.

    Returns:
        list[str]: Non-comment lines.
    """
    lines = MAKEFILE.read_text(encoding="utf-8").splitlines()
    return [ln for ln in lines if not ln.lstrip().startswith("#")]


def test_no_console_script_invocation() -> None:
    offenders = [ln for ln in _active_lines() if CONSOLE_SCRIPT.search(ln)]
    assert offenders == []


def test_graphify_deep_runs_through_with_env() -> None:
    lines = _active_lines()
    index = next((i for i, ln in enumerate(lines) if ln.startswith("graphify-deep:")), None)
    assert index is not None, "graphify-deep target is missing"
    recipe = []
    for ln in lines[index + 1:]:
        if not ln.startswith("\t"):
            break
        recipe.append(ln)
    joined = "\n".join(recipe)
    assert "python3 -I $(AGENTS_DIR)/scripts/with_env.py graphify-extract-deep" in joined


def test_every_module_invocation_is_isolated() -> None:
    """A `graphify/` folder in the cwd must not shadow the venv package (R2-4)."""
    invocations = [ln for ln in _active_lines() if "-m graphify" in ln]
    assert invocations, "no `-m graphify` invocation found"
    offenders = [ln for ln in invocations if not re.search(r"\s-I\s+-m graphify\b", ln)]
    assert offenders == []
