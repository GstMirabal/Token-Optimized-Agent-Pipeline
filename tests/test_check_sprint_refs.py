"""Tests for scripts/check_sprint_refs.py: each finding class must fail on a fixture."""

from __future__ import annotations

import os
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


def test_an_unreadable_artifact_exits_2(tmp_path: Path) -> None:
    """Bytes that are not UTF-8 in task_scope.md make the script exit 2 with a read error."""
    sprint = _sprint(tmp_path)
    with (sprint / "task_scope.md").open("ab") as handle:
        handle.write(b"\xff\xfe")
    result = _run("--sprint-dir", str(sprint))
    assert result.returncode == 2
    assert "cannot read an artifact" in result.stderr


@pytest.mark.skipif(os.geteuid() == 0, reason="root ignores the file mode")
def test_a_permission_denied_artifact_exits_2(tmp_path: Path) -> None:
    """A task_scope.md with mode 0o000 raises OSError and makes the script exit 2 with a read error."""
    sprint = _sprint(tmp_path)
    scope = sprint / "task_scope.md"
    scope.chmod(0o000)
    try:
        result = _run("--sprint-dir", str(sprint))
    finally:
        scope.chmod(0o644)
    assert result.returncode == 2
    assert "cannot read an artifact" in result.stderr


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


SCOPE_DONE = (
    "## Work\n\n| # | File | Status |\n| :--- | :--- | :--- |\n"
    "| A-01 | `a.py` | ✅ `5c5e0a3`, `ad7cd48` |\n| A-01b | `b.py` | ⏳ |\n\n## Jurisdiction\n"
)


def _ki_sprint(tmp_path: Path, ki_text: str, scope: str = SCOPE_DONE) -> Path:
    log = LOG.replace("| x | y | KI-060-1 |", f"| x | {ki_text} | KI-060-1 |")
    plan = PLAN.replace("| A-01 | `a.py` | modify — D0 | low | `implementer_agent` |", "| A-01 | `a.py` | modify — D0 | low | `implementer_agent` |\n| A-01b | `b.py` | modify — D0 | low | `implementer_agent` |")
    assign = ASSIGN.replace("| A-01 | `a.py` |", "| A-01 | `a.py` |\n| A-01b | `b.py` |")
    return _sprint(tmp_path, task_scope_md=scope, SPRINT_LOG_md=log, IMPLEMENTATION_PLAN_md=plan, agent_assignment_md=assign)


def test_a_ki_row_naming_a_done_unit_without_its_sha_exits_2(tmp_path: Path) -> None:
    result = _run("--sprint-dir", str(_ki_sprint(tmp_path, "measured in A-01")))
    assert result.returncode == 2
    assert "KI-060-1 names unit A-01" in result.stderr
    assert "5c5e0a3" in result.stderr


def test_a_ki_row_citing_the_sha_passes(tmp_path: Path) -> None:
    assert _run("--sprint-dir", str(_ki_sprint(tmp_path, "measured in A-01 at `ad7cd48`"))).returncode == 0


def test_a_unit_id_matches_as_a_whole_token(tmp_path: Path) -> None:
    """A-01b is not done, so naming it must not trip the check for A-01."""
    result = _run("--sprint-dir", str(_ki_sprint(tmp_path, "see A-01b")))
    assert result.returncode == 0, result.stderr


def test_a_not_done_unit_named_without_sha_passes(tmp_path: Path) -> None:
    scope = SCOPE_DONE.replace("✅ `5c5e0a3`, `ad7cd48`", "⏳")
    assert _run("--sprint-dir", str(_ki_sprint(tmp_path, "pending A-01", scope))).returncode == 0


@pytest.mark.parametrize("missing", ["task_scope.md", "SPRINT_LOG.md"])
def test_a_missing_ki_input_skips_the_ki_check_and_exits_0(tmp_path: Path, missing: str) -> None:
    sprint = _ki_sprint(tmp_path, "x")
    (sprint / missing).unlink()
    result = _run("--sprint-dir", str(sprint))
    assert result.returncode == 0, result.stderr
    assert f"no {missing} under" in result.stdout
    assert "(skip)" in result.stdout
