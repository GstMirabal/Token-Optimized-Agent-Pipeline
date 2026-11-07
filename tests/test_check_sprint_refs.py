"""Tests for scripts/check_sprint_refs.py: each finding class must fail on a fixture."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
CHECK = REPO / "scripts" / "check_sprint_refs.py"

PLAN = """# Plan

## Design

| ID | Decision | Rejected |
| :--- | :--- | :--- |
| D0 | Order. **Check**: `true` → exit 0 | none |

## Work

| # | File | Operation | Risk | Assignee |
| :--- | :--- | :--- | :--- | :--- |
| A-01 | `a.py` | modify — D0 | low | `implementer_agent` |

## Dependencies
"""
SCOPE = "## Work\n\n| # | File |\n| :--- | :--- |\n| A-01 | `a.py` |\n\n## Jurisdiction\n"
ASSIGN = "## Staffing\n\n| # | Target |\n| :--- | :--- |\n| A-01 | `a.py` |\n\n## Disagreements\n"
LOG = """## KI

| Friction Point | Resolution | KI ID |
| :--- | :--- | :--- |
| x | y | KI-060-1 |

## Quality Gate

| Gate | Round | Verdict | Class | Severity | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| QA Agent (Gate 1) | 1 | REJECTED | charter | S2 | R1-1 open. KI-060-1. |

### Gate findings

| Round | ID | Severity | File:line | Check |
| :--- | :--- | :--- | :--- | :--- |
| 1 | R1-1 | S2 | `a.py:1` | `true` → exit 0 |

### Remediation notes
"""


def _sprint(tmp_path: Path, name: str = "060-core-x", **overrides: str) -> Path:
    sprint = tmp_path / name
    sprint.mkdir()
    texts = {
        "IMPLEMENTATION_PLAN.md": PLAN,
        "task_scope.md": SCOPE,
        "agent_assignment.md": ASSIGN,
        "SPRINT_LOG.md": LOG,
    }
    texts.update({key.replace("_md", ".md"): value for key, value in overrides.items()})
    for file_name, body in texts.items():
        (sprint / file_name).write_text(body, encoding="utf-8")
    return sprint


def _run(*args: str, cwd: Path = REPO) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECK), *args], cwd=cwd, capture_output=True, text=True, check=False
    )


def test_a_consistent_sprint_passes(tmp_path: Path) -> None:
    result = _run("--sprint-dir", str(_sprint(tmp_path)))
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize(
    ("file_key", "body", "message"),
    [
        ("task_scope_md", SCOPE.replace("A-01", "A-02"), "unit A-01 of the plan is missing"),
        ("agent_assignment_md", ASSIGN.replace("| A-01 |", "| A-01 |\n| A-09 |"), "unit A-09 is not in the plan"),
        ("SPRINT_LOG_md", LOG + "\nSee D7.\n", "decision D7 is cited"),
        ("SPRINT_LOG_md", LOG + "\nSee KI-060-2.\n", "KI-060-2 is cited"),
        ("SPRINT_LOG_md", LOG + "\nSee R1-2.\n", "R1-2 is cited"),
        ("IMPLEMENTATION_PLAN_md", PLAN.replace(" **Check**: `true` → exit 0", ""), "Design row D0 has no **Check**:"),
        ("SPRINT_LOG_md", LOG.replace("R1-1 open. KI-060-1.", "R1-1. " + "x" * 400), "Notes holds"),
    ],
)
def test_each_finding_class_exits_2(tmp_path: Path, file_key: str, body: str, message: str) -> None:
    result = _run("--sprint-dir", str(_sprint(tmp_path, **{file_key: body})))
    assert result.returncode == 2
    assert message in result.stderr


def test_sprint_059_exempts_what_predates_d37(tmp_path: Path) -> None:
    """D0 without **Check**: and a round 12 note over the limit predate D37 in 059."""
    plan = PLAN.replace(" **Check**: `true` → exit 0", "")
    log = LOG.replace("KI-060-1", "KI-059-1").replace("| 1 | R", "| 12 | R").replace(
        "| QA Agent (Gate 1) | 1 |", "| QA Agent (Gate 1) | 12 |"
    ).replace("R1-1 open.", "R1-1 open. " + "x" * 400)
    sprint = _sprint(tmp_path, "059-core-x", IMPLEMENTATION_PLAN_md=plan, SPRINT_LOG_md=log)
    assert _run("--sprint-dir", str(sprint)).returncode == 0


def test_a_sprint_before_059_is_skipped(tmp_path: Path) -> None:
    sprint = _sprint(tmp_path, "058-core-x", SPRINT_LOG_md=LOG + "\nSee D7.\n")
    assert _run("--sprint-dir", str(sprint)).returncode == 0


def test_a_sprint_without_a_plan_yet_is_skipped(tmp_path: Path) -> None:
    sprint = _sprint(tmp_path)
    (sprint / "IMPLEMENTATION_PLAN.md").unlink()
    assert _run("--sprint-dir", str(sprint)).returncode == 0


def test_a_plan_without_a_design_table_exits_2(tmp_path: Path) -> None:
    sprint = _sprint(tmp_path, IMPLEMENTATION_PLAN_md="# empty plan\n")
    assert _run("--sprint-dir", str(sprint)).returncode == 2


def test_a_missing_sprint_dir_exits_2(tmp_path: Path) -> None:
    assert _run("--sprint-dir", str(tmp_path / "060-typo")).returncode == 2



def test_a_check_column_counts_as_the_check(tmp_path: Path) -> None:
    """The plan template writes the check in its own Design column (plan D37 M-08)."""
    plan = PLAN.replace("| ID | Decision | Rejected |\n| :--- | :--- | :--- |", "| ID | Decision | Rejected | Check |\n| :--- | :--- | :--- | :--- |")
    filled = plan.replace("| D0 | Order. **Check**: `true` → exit 0 | none |", "| D0 | Order. | none | `true` → exit 0 |")
    empty = plan.replace("| D0 | Order. **Check**: `true` → exit 0 | none |", "| D0 | Order. | none |  |")
    assert _run("--sprint-dir", str(_sprint(tmp_path, IMPLEMENTATION_PLAN_md=filled))).returncode == 0
    other = tmp_path / "second"
    other.mkdir()
    assert _run("--sprint-dir", str(_sprint(other, IMPLEMENTATION_PLAN_md=empty))).returncode == 2
