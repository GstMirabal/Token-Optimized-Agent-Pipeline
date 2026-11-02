"""Paired tests for scripts/check_plan_closure.py (R-9 and R-10)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "check_plan_closure.py"

PLAN = """# Plan

## Tests

| Check | Fails? |
| :--- | :--- |
| `test -f a` | yes |
| `test -f b` | yes |

## Verification

| Command | Expected |
| :--- | :--- |
| `make verify` | exit `0` |

## Abort criterion

1. First criterion.
2. Second criterion.

## Approval
"""

ABORT = """## Abort criteria

| Criterion | Command | Exit | Observation |
| :--- | :--- | :--- | :--- |
| 1 | `rg -c x .` | 1 | none |
| 2 | `make verify` | 0 | green |
"""

RESULTS = """## Plan results

| Section | Row | Check | Result |
| :--- | :--- | :--- | :--- |
| Tests | 1 | `test -f a` | exit 0 |
| Tests | 2 | `test -f b` | exit 0 |
| Verification | 1 | `make verify` | exit 0 |
"""


def run(tmp_path: Path, log: str, plan: str = PLAN) -> subprocess.CompletedProcess[str]:
    (tmp_path / "IMPLEMENTATION_PLAN.md").write_text(plan, encoding="utf-8")
    (tmp_path / "SPRINT_LOG.md").write_text(log, encoding="utf-8")
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--sprint-dir", str(tmp_path)],
        capture_output=True,
        text=True,
        check=False,
    )


def test_clean_pair_passes(tmp_path: Path) -> None:
    assert run(tmp_path, ABORT + RESULTS).returncode == 0


def test_criterion_without_row_fails(tmp_path: Path) -> None:
    log = ABORT.replace("| 2 | `make verify` | 0 | green |\n", "") + RESULTS
    result = run(tmp_path, log)
    assert result.returncode == 2
    assert "criterion 2" in result.stderr


def test_row_without_exit_fails(tmp_path: Path) -> None:
    log = ABORT.replace("| 1 | `rg -c x .` | 1 |", "| 1 | `rg -c x .` |  |") + RESULTS
    assert run(tmp_path, log).returncode == 2


def test_row_without_command_fails(tmp_path: Path) -> None:
    log = ABORT.replace("`rg -c x .`", "by arithmetic") + RESULTS
    assert run(tmp_path, log).returncode == 2


def test_results_short_by_one_fails(tmp_path: Path) -> None:
    log = ABORT + RESULTS.replace("| Verification | 1 | `make verify` | exit 0 |\n", "")
    result = run(tmp_path, log)
    assert result.returncode == 2
    assert "no row for Verification row 1" in result.stderr


def test_empty_result_fails(tmp_path: Path) -> None:
    log = ABORT + RESULTS.replace("| exit 0 |\n| Tests | 2", "|  |\n| Tests | 2")
    assert run(tmp_path, log).returncode == 2


def test_missing_table_fails(tmp_path: Path) -> None:
    result = run(tmp_path, ABORT)
    assert result.returncode == 2
    assert "Section | Row | Check | Result" in result.stderr


def test_missing_file_fails(tmp_path: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--sprint-dir", str(tmp_path)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 2


def test_escaped_pipe_in_cell_parsed(tmp_path: Path) -> None:
    log = ABORT.replace("`rg -c x .`", "`rg -c 'a\\|b' .`") + RESULTS.replace(
        "`test -f a`", "`rg 'a\\|b'`"
    )
    assert run(tmp_path, log).returncode == 0
