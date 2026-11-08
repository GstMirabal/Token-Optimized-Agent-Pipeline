"""Tests for scripts/check_task_scope.py.

A gate proven only on a healthy tree proves nothing — fixtures must fail.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
CHECK = REPO / "scripts" / "check_task_scope.py"

# The F-051-R2 tests call `current_sprint_dir` directly: the resolver's bug was
# invisible through the CLI, which exits 0 either way — skipping and passing are
# the same exit code, which is precisely why it went unnoticed.
sys.path.insert(0, str(REPO / "scripts"))


def _run(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECK), *args],
        cwd=cwd or REPO,
        capture_output=True,
        text=True,
        check=False,
    )


def _scope(tmp_path: Path, body: str) -> Path:
    sprint = tmp_path / "docs" / "sprints" / "030-core-pipeline"
    sprint.mkdir(parents=True)
    path = sprint / "task_scope.md"
    path.write_text(body, encoding="utf-8")
    return sprint


SHAPE = "# | File | Operation | Risk | Assignee | Model | Effort | Status"

OLD = """# Task Scope

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| X | `a.py` | modify | high | `devops_agent` | ⏳ |
"""

CURSOR_NO_MODEL = f"""# Task Scope

**Mode.** Cursor `delegation_mode: sequential`.

| {SHAPE} |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| X | `a.py` | modify | high | `devops_agent` | | | ⏳ |
"""

# Header claims Model/Effort but the table omits them.
MISSING_COLUMNS = """# Task Scope

**Table shape (Work units).** `# | File | Operation | Risk | Assignee | Model | Effort | Status`

**Mode.** Cursor `delegation_mode: sequential`.

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| X | `a.py` | modify | high | `devops_agent` | ⏳ |
"""

# `run`, not `modify`: devops_agent declares no Write/Edit tool, so a mutating
# operation would now trip the capability check and stop testing escalation.
MECHANICAL_HIGH = f"""# Task Scope

**Mode.** Cursor.

| {SHAPE} |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| X | `a.py` | run | high | `devops_agent` | `composer-2.5` | N/A | ⏳ |
"""

ESCALATED = f"""# Task Scope

**Mode.** Cursor.

| {SHAPE} |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| X | `a.py` | run | high | `devops_agent` — escalated | `grok-4.6` | `high` | ⏳ |
"""

INCAPABLE = f"""# Task Scope

**Mode.** Cursor.

| {SHAPE} |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| X | `a.py` | modify | low | `devops_agent` | `composer-2.5` | N/A | ⏳ |
"""

CAPABLE = f"""# Task Scope

**Mode.** Cursor.

| {SHAPE} |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| X | `a.py` | modify | low | `implementer_agent` | `grok-4.5` | `high` | ⏳ |
"""

NO_SUCH_PROFILE = f"""# Task Scope

**Mode.** Cursor.

| {SHAPE} |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| X | `a.py` | modify | low | `invented_agent` | `grok-4.5` | `high` | ⏳ |
"""


def test_historical_024_is_skipped() -> None:
    """Sprints before Model/Effort columns must not fail the close."""
    result = _run("--sprint-dir", "docs/sprints/024-core-pipeline")
    assert result.returncode == 0, result.stderr


def test_cursor_scope_without_model_columns_fails(tmp_path: Path) -> None:
    sprint = _scope(tmp_path, MISSING_COLUMNS)
    result = _run("--sprint-dir", str(sprint))
    assert result.returncode == 2
    assert "Model" in result.stderr or "Effort" in result.stderr


def test_mechanical_high_without_keep_or_escalation_fails(tmp_path: Path) -> None:
    sprint = _scope(tmp_path, MECHANICAL_HIGH)
    result = _run("--sprint-dir", str(sprint))
    assert result.returncode == 2
    assert "mechanical" in result.stderr.lower() or "escalat" in result.stderr.lower()


def test_escalated_mechanical_high_passes(tmp_path: Path) -> None:
    sprint = _scope(tmp_path, ESCALATED)
    result = _run("--sprint-dir", str(sprint))
    assert result.returncode == 0, result.stderr


# --- Sprint 034 I4/K3: assignments that cannot execute, and absence. ---


def test_assignee_without_write_tool_fails(tmp_path: Path) -> None:
    """Sprints 028-032 recorded 32 rows like this one as executed successfully."""
    sprint = _scope(tmp_path, INCAPABLE)
    result = _run("--sprint-dir", str(sprint))
    assert result.returncode == 2
    assert "Write/Edit" in result.stderr


def test_assignee_with_write_tool_passes(tmp_path: Path) -> None:
    sprint = _scope(tmp_path, CAPABLE)
    result = _run("--sprint-dir", str(sprint))
    assert result.returncode == 0, result.stderr


def test_assignee_with_no_profile_file_fails(tmp_path: Path) -> None:
    sprint = _scope(tmp_path, NO_SUCH_PROFILE)
    result = _run("--sprint-dir", str(sprint))
    assert result.returncode == 2
    assert "no profile file" in result.stderr


def test_absent_task_scope_fails_in_a_sprint_directory(tmp_path: Path) -> None:
    """Absence used to exit 0, which disabled jurisdictional_lock silently."""
    sprint = tmp_path / "docs" / "sprints" / "030-core-pipeline"
    sprint.mkdir(parents=True)
    result = _run("--sprint-dir", str(sprint))
    assert result.returncode == 2
    assert "Phase 4.3" in result.stderr


def test_absent_task_scope_skips_outside_a_sprint_directory(tmp_path: Path) -> None:
    plain = tmp_path / "not-a-sprint"
    plain.mkdir()
    result = _run("--sprint-dir", str(plain))
    assert result.returncode == 0, result.stderr


def test_current_sprint_skips_when_anchor_absent(tmp_path: Path) -> None:
    result = _run("--current-sprint", cwd=tmp_path)
    assert result.returncode == 0


# --- F-051-R2: the resolver required an int and real anchors carry a string ---


def _anchor(root: Path, sprint_id: object) -> Path:
    """An anchor naming `sprint_id`, plus the matching sprint directory."""
    (root / "docs" / "sprints" / "051-core-pipeline").mkdir(parents=True)
    (root / "docs" / "active_state.json").write_text(
        json.dumps({"current_sprint": {"id": sprint_id}}), encoding="utf-8"
    )
    return root / "docs" / "sprints" / "051-core-pipeline"


def test_a_zero_padded_string_id_resolves_like_an_int(tmp_path: Path) -> None:
    """Real anchors carry `"051"`, because that is the directory-name form.

    The resolver required `int` and returned None otherwise, and both callers
    read None as "no current sprint, skip" — so two steps of `make verify`
    printed `[OK] … (skip)` and exited 0 in every repository using the string
    form. A gate that fails open reports success for work it never looked at.
    """
    import check_task_scope as cts

    expected = _anchor(tmp_path, "051")
    assert cts.current_sprint_dir(tmp_path) == expected


def test_an_integer_id_still_resolves(tmp_path: Path) -> None:
    """The pre-051 form must not regress."""
    import check_task_scope as cts

    expected = _anchor(tmp_path, 51)
    assert cts.current_sprint_dir(tmp_path) == expected


def test_a_non_numeric_id_raises(tmp_path: Path) -> None:
    """An unusable id is an error, never a skip (plan D37 M-02)."""
    import check_task_scope as cts

    _anchor(tmp_path, "not-a-sprint")
    with pytest.raises(cts.CurrentSprintError):
        cts.current_sprint_dir(tmp_path)
    _anchor2 = tmp_path / "docs" / "active_state.json"
    _anchor2.write_text(json.dumps({"current_sprint": {"id": True}}), encoding="utf-8")
    with pytest.raises(cts.CurrentSprintError):
        cts.current_sprint_dir(tmp_path)


# --- Plan D37 M-02: no silent skip from a subdirectory or on a missing directory ---


def _git_repo_with_anchor(root: Path, anchor_text: str) -> Path:
    """A fixture repository: `.git`, an anchor, and no sprint directory."""
    (root / ".git").mkdir()
    (root / "docs" / "sprints").mkdir(parents=True)
    (root / "docs" / "active_state.json").write_text(anchor_text, encoding="utf-8")
    return root


def test_current_sprint_from_a_subdirectory_exits_2_on_a_missing_directory(
    tmp_path: Path,
) -> None:
    root = _git_repo_with_anchor(tmp_path, json.dumps({"current_sprint": {"id": "059"}}))
    result = _run("--current-sprint", cwd=root / "docs")
    assert result.returncode == 2, result.stdout


def test_current_sprint_exits_2_on_a_truncated_anchor(tmp_path: Path) -> None:
    root = _git_repo_with_anchor(tmp_path, '{"current_sprint": {"id": 59')
    result = _run("--current-sprint", cwd=root)
    assert result.returncode == 2, result.stdout


# --- B-3: a Markdown-escaped pipe inside a cell is not a column separator. ---

ESCAPED_PIPE = f"""# Task Scope

**Mode.** Cursor.

| {SHAPE} |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| X | `a\\|b.py` | modify | low | `devops_agent` | `composer-2.5` | N/A | ⏳ |
"""


def test_escaped_pipe_does_not_split_a_cell() -> None:
    from check_task_scope import _cells

    cells = _cells("| X | `a\\|b` | modify |")
    assert cells == ["X", "a|b", "modify"]


def test_escaped_pipe_in_a_cell_does_not_shift_columns(tmp_path: Path) -> None:
    """A shifted row reads Operation as `b.py` and skips the capability check."""
    sprint = _scope(tmp_path, ESCAPED_PIPE)
    result = _run("--sprint-dir", str(sprint))
    assert result.returncode == 2
    assert "Write/Edit" in result.stderr


def test_sprint_id_from_dir_accepts_a_prefix_of_three_or_more_digits() -> None:
    """A four-digit id returned None, so `check` skipped a real sprint and exited 0."""
    from check_task_scope import sprint_id_from_dir

    assert sprint_id_from_dir(Path("1059-core-x")) == 1059
    assert sprint_id_from_dir(Path("059-core-x")) == 59
    assert sprint_id_from_dir(Path("12-core-x")) is None
    assert sprint_id_from_dir(Path("core-x")) is None


# --- G-01: the optional `Depends on` column and the parallel batches (D11). ---

DEP_HEAD = (
    "| # | File | Operation | Risk | Assignee | Model | Effort | Depends on | Status |\n"
    "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
)
PLAIN_HEAD = (
    "| # | File | Operation | Risk | Assignee | Model | Effort | Status |\n"
    "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
)


def _dep_scope(tmp_path: Path, rows: list[tuple[str, str, str, str]]) -> Path:
    """Sprint with one Work table; rows are (id, file, depends on, status)."""
    body = "# Task Scope\n\n" + DEP_HEAD + "".join(
        f"| {uid} | `{file}` | run | low | `implementer_agent` | sonnet | medium "
        f"| {deps} | {status} |\n"
        for uid, file, deps, status in rows
    )
    return _scope(tmp_path, body)


def _batches(sprint: Path) -> subprocess.CompletedProcess[str]:
    return _run("--sprint-dir", str(sprint), "--batches")


def test_table_without_depends_on_stays_valid_and_keeps_table_order(
    tmp_path: Path,
) -> None:
    body = "# Task Scope\n\n" + PLAIN_HEAD + (
        "| A | `a.py` | run | low | `implementer_agent` | sonnet | medium | ⏳ |\n"
        "| B | `b.py` | run | low | `implementer_agent` | sonnet | medium | ⏳ |\n"
    )
    sprint = _scope(tmp_path, body)
    assert _run("--sprint-dir", str(sprint)).returncode == 0
    result = _batches(sprint)
    assert result.returncode == 0
    assert result.stdout == "batch 1: A B\n"


def test_unknown_dependency_id_exits_2(tmp_path: Path) -> None:
    sprint = _dep_scope(tmp_path, [("A", "a.py", "Z", "⏳")])
    for args in ((), ("--batches",)):
        result = _run("--sprint-dir", str(sprint), *args)
        assert result.returncode == 2
        assert "'Z'" in result.stderr


def test_self_dependency_exits_2(tmp_path: Path) -> None:
    sprint = _dep_scope(tmp_path, [("A", "a.py", "A", "⏳")])
    result = _run("--sprint-dir", str(sprint))
    assert result.returncode == 2
    assert "depends on itself" in result.stderr


def test_dependency_cycle_exits_2(tmp_path: Path) -> None:
    sprint = _dep_scope(
        tmp_path,
        [("A", "a.py", "B", "⏳"), ("B", "b.py", "A", "⏳"), ("C", "c.py", "-", "⏳")],
    )
    for args in ((), ("--batches",)):
        result = _run("--sprint-dir", str(sprint), *args)
        assert result.returncode == 2
        assert "cycle" in result.stderr
        assert "A, B" in result.stderr
        assert "C" not in result.stderr.split("cycle", 1)[1]


def test_same_file_units_are_split_across_batches(tmp_path: Path) -> None:
    sprint = _dep_scope(
        tmp_path,
        [("A", "x.py", "-", "⏳"), ("B", "x.py", "", "⏳"), ("C", "y.py", "-", "⏳")],
    )
    assert _batches(sprint).stdout == "batch 1: A C\nbatch 2: B\n"


def test_a_batch_holds_at_most_four_units(tmp_path: Path) -> None:
    rows = [(f"U{n}", f"f{n}.py", "-", "⏳") for n in range(1, 7)]
    sprint = _dep_scope(tmp_path, rows)
    assert _batches(sprint).stdout == "batch 1: U1 U2 U3 U4\nbatch 2: U5 U6\n"


def test_committed_dependency_releases_a_unit(tmp_path: Path) -> None:
    sprint = _dep_scope(
        tmp_path, [("A", "a.py", "-", "✅ abc1234"), ("B", "b.py", "A", "⏳")]
    )
    assert _batches(sprint).stdout == "batch 1: B\n"


def test_pending_dependency_holds_a_unit_to_a_later_batch(tmp_path: Path) -> None:
    sprint = _dep_scope(
        tmp_path,
        [("A", "a.py", "B", "⏳"), ("B", "b.py", "-", "⏳"), ("C", "c.py", "A, B", "⏳")],
    )
    assert _batches(sprint).stdout == "batch 1: B\nbatch 2: A\nbatch 3: C\n"


def test_batches_are_deterministic(tmp_path: Path) -> None:
    rows = [(f"U{n}", f"f{n % 3}.py", "-" if n < 4 else f"U{n - 3}", "⏳") for n in range(1, 9)]
    sprint = _dep_scope(tmp_path, rows)
    first = _batches(sprint)
    assert first.returncode == 0
    assert all(_batches(sprint).stdout == first.stdout for _ in range(3))


def test_everything_committed_prints_no_pending_units(tmp_path: Path) -> None:
    sprint = _dep_scope(tmp_path, [("A", "a.py", "-", "✅ abc1234")])
    result = _batches(sprint)
    assert (result.returncode, result.stdout) == (0, "no pending units\n")


def test_batches_without_task_scope_exits_2(tmp_path: Path) -> None:
    sprint = tmp_path / "docs" / "sprints" / "030-core-pipeline"
    sprint.mkdir(parents=True)
    assert _batches(sprint).returncode == 2


def test_batches_never_mix_units_of_different_tables(tmp_path: Path) -> None:
    """Each Work table is a wave barrier: the Phase 7 gate runs between waves."""
    row = "| {} | `{}` | run | low | `implementer_agent` | sonnet | medium | - | ⏳ |\n"
    body = (
        "# Task Scope\n\n### Wave 1\n\n" + DEP_HEAD + row.format("A", "a.py")
        + row.format("B", "b.py") + "\n### Wave 2\n\n" + DEP_HEAD
        + row.format("C", "c.py") + row.format("D", "d.py")
    )
    result = _batches(_scope(tmp_path, body))
    assert result.returncode == 0
    assert result.stdout == "batch 1: A B\nbatch 2: C D\n"


def test_dependency_on_a_later_table_is_unschedulable(tmp_path: Path) -> None:
    row = "| {} | `{}` | run | low | `implementer_agent` | sonnet | medium | {} | ⏳ |\n"
    body = (
        "# Task Scope\n\n" + DEP_HEAD + row.format("A", "a.py", "C") + "\n"
        + DEP_HEAD + row.format("C", "c.py", "-")
    )
    result = _batches(_scope(tmp_path, body))
    assert result.returncode == 2
    assert "cannot be scheduled" in result.stderr


def test_a_replaced_unit_is_never_scheduled(tmp_path: Path) -> None:
    """Only the pending mark schedules a unit; replaced and RECORD rows stay out."""
    sprint = _dep_scope(
        tmp_path,
        [
            ("A", "a.py", "-", "replaced by B (D37)"),
            ("B", "b.py", "-", "RECORD"),
            ("C", "c.py", "-", "⏳"),
        ],
    )
    result = _batches(sprint)
    assert (result.returncode, result.stdout) == (0, "batch 1: C\n")


def test_only_non_pending_units_print_no_pending_units(tmp_path: Path) -> None:
    sprint = _dep_scope(tmp_path, [("A", "a.py", "-", "replaced by B (D37)")])
    result = _batches(sprint)
    assert (result.returncode, result.stdout) == (0, "no pending units\n")


def test_a_pending_unit_depending_on_a_finished_unit_is_scheduled(
    tmp_path: Path,
) -> None:
    sprint = _dep_scope(
        tmp_path,
        [
            ("A", "a.py", "-", "✅ abc1234"),
            ("R", "r.py", "-", "replaced by A (D37)"),
            ("B", "b.py", "A, R", "⏳"),
        ],
    )
    result = _batches(sprint)
    assert (result.returncode, result.stdout) == (0, "batch 1: B\n")


def test_batches_refuse_a_unit_with_no_status_column(tmp_path: Path) -> None:
    head = "| # | File | Operation | Risk | Assignee | Model | Effort |\n" + "| :--- " * 7 + "|\n"
    body = "# Task Scope\n\n" + head + (
        "| A | `a.py` | run | low | `implementer_agent` | sonnet | medium |\n"
    )
    sprint = _scope(tmp_path, body)
    assert _run("--sprint-dir", str(sprint)).returncode == 0
    result = _batches(sprint)
    assert result.returncode == 2
    assert result.stdout == ""
    assert "A" in result.stderr and "Status" in result.stderr


def test_batches_refuse_a_unit_with_an_empty_status_cell(tmp_path: Path) -> None:
    sprint = _dep_scope(tmp_path, [("A", "a.py", "-", ""), ("B", "b.py", "-", "⏳")])
    assert _run("--sprint-dir", str(sprint)).returncode == 0
    result = _batches(sprint)
    assert result.returncode == 2
    assert result.stdout == ""
    assert "Unit A: Status is missing" in result.stderr


def test_an_unrecognised_status_fails_the_audit_and_batches(tmp_path: Path) -> None:
    sprint = _dep_scope(
        tmp_path, [("A", "a.py", "-", "in progress"), ("B", "b.py", "A", "⏳")]
    )
    for args in ((), ("--batches",)):
        result = _run("--sprint-dir", str(sprint), *args)
        assert result.returncode == 2
        assert result.stdout == ""
        assert "Unit A" in result.stderr and "in progress" in result.stderr


def test_recognised_status_forms_pass_the_audit_and_batches(tmp_path: Path) -> None:
    sprint = _dep_scope(
        tmp_path,
        [
            ("A", "a.py", "-", "✅ `0cbf261`"),
            ("C", "c.py", "-", "replaced by D (D37)"),
            ("D", "d.py", "-", "RECORD"),
            ("B", "b.py", "A", "⏳"),
        ],
    )
    assert _run("--sprint-dir", str(sprint)).returncode == 0
    result = _batches(sprint)
    assert (result.returncode, result.stdout) == (0, "batch 1: B\n")
