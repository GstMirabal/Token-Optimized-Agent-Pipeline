"""Tests for skills/token-saver-auditor/scripts/audit_plan.py.

Every case asserts the auditor FAILS where it must. A gate proven only on a
healthy tree proves nothing.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
AUDIT = REPO / "skills" / "token-saver-auditor" / "scripts" / "audit_plan.py"


def _run(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(AUDIT), str(path)],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )


def _plan(tmp_path: Path, body: str) -> Path:
    path = tmp_path / "IMPLEMENTATION_PLAN.md"
    path.write_text(body, encoding="utf-8")
    return path


MECHANISMS = """
## Mechanisms

| Mechanism | Deterministic or agent judgment | Invoker (`RA-16`) |
| :--- | :--- | :--- |
| example | script | Makefile verify |
"""

COST = """
## Cost

| Field | Value |
| :--- | :--- |
| Work units | 1 |
"""


def test_audit_plan_script_exists() -> None:
    """The auditor must be a real script, not an empty scripts/ stub."""
    assert AUDIT.is_file()


def test_029_plan_fails_without_cost_section() -> None:
    """Sprint 029 plans predate the Cost section — that is the defect."""
    target = REPO / "docs" / "sprints" / "029-core-pipeline" / "IMPLEMENTATION_PLAN.md"
    result = _run(target)
    assert result.returncode == 2
    assert "Cost" in result.stderr


def test_clean_plan_passes(tmp_path: Path) -> None:
    body = "# Plan\n" + MECHANISMS + COST
    result = _run(_plan(tmp_path, body))
    assert result.returncode == 0, result.stderr


def test_review_the_whole_system_is_rejected(tmp_path: Path) -> None:
    body = "# Plan\nreview the whole system\n" + MECHANISMS + COST
    result = _run(_plan(tmp_path, body))
    assert result.returncode == 2
    assert "whole system" in result.stderr.lower()


def test_raw_json_dump_is_rejected(tmp_path: Path) -> None:
    body = "# Plan\nraw JSON dump into the chat\n" + MECHANISMS + COST
    result = _run(_plan(tmp_path, body))
    assert result.returncode == 2
    assert "JSON" in result.stderr or "CSV" in result.stderr


def test_loop_without_guard_is_rejected(tmp_path: Path) -> None:
    body = "# Plan\nWrap phases in `/loop`.\n" + MECHANISMS + COST
    result = _run(_plan(tmp_path, body))
    assert result.returncode == 2
    assert "loop_guard" in result.stderr


def test_mechanisms_without_invoker_column_is_rejected(tmp_path: Path) -> None:
    body = "# Plan\n## Mechanisms\n\n| Mechanism | Kind |\n| :--- | :--- |\n| x | script |\n" + COST
    result = _run(_plan(tmp_path, body))
    assert result.returncode == 2
    assert "Invoker" in result.stderr


def test_missing_mechanisms_section_is_rejected(tmp_path: Path) -> None:
    result = _run(_plan(tmp_path, "# Plan\n" + COST))
    assert result.returncode == 2
    assert "Mechanisms" in result.stderr


def test_current_sprint_skips_when_anchor_absent(tmp_path: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(AUDIT), "--current-sprint"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
