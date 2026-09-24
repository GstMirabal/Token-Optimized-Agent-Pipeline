"""Tests for scripts/loop_guard.py — the stop set of an unattended loop.

The guard is fail-closed by design, so most of these assert it STOPS. A loop
guard proven only on the happy path is the PR #28 defect with a counter
attached: a verdict computed on every run and consulted on none.
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import loop_guard as lg  # noqa: E402


@pytest.fixture
def repo(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    run = lambda *a: subprocess.run(["git", *a], capture_output=True, text=True, check=True)
    run("init", "-q", "-b", "main")
    run("config", "user.email", "t@example.com")
    run("config", "user.name", "T")
    (tmp_path / "f.txt").write_text("base\n")
    run("add", "-A")
    run("commit", "-qm", "base")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "active_state.json").write_text("{}")
    return tmp_path


def loop_block(repo) -> dict:
    return json.loads((repo / "docs" / "active_state.json").read_text())["loop"]


# --- fail closed -------------------------------------------------------

def test_check_without_an_armed_loop_stops(repo):
    assert lg.check() == 2


def test_check_with_an_incomplete_loop_block_stops(repo):
    (repo / "docs" / "active_state.json").write_text(json.dumps({"loop": {"iteration": 0}}))
    assert lg.check() == 2


def test_arming_without_a_success_condition_is_refused(repo):
    assert lg.start(5, "") == 2


# --- the binding stops -------------------------------------------------

def test_iteration_cap_stops_the_loop(repo):
    lg.start(2, "tests pass")
    assert lg.check() == 0
    assert lg.check() == 0
    assert lg.check() == 2


def test_progress_resets_the_stagnation_counter(repo):
    lg.start(10, "tests pass")
    lg.check()
    (repo / "f.txt").write_text("changed\n")
    subprocess.run(["git", "commit", "-aqm", "work"], check=True)
    assert lg.check() == 0
    assert loop_block(repo)["stagnant_iterations"] == 0


def test_first_iteration_is_never_counted_as_stagnant(repo):
    """`check` runs at the start of an iteration, so the first comparison is
    against a baseline written before any work could happen. Counting it would
    stop the loop after one unproductive iteration, not the two the rule states."""
    lg.start(10, "tests pass")
    assert lg.check() == 0
    assert loop_block(repo)["stagnant_iterations"] == 0


def test_two_stagnant_iterations_stop_the_loop(repo):
    lg.start(10, "tests pass")
    assert lg.check() == 0   # iteration 1: exempt by the rule above
    assert lg.check() == 0   # iteration 2: stagnant #1
    assert lg.check() == 2   # iteration 3: stagnant #2 — stop


def test_task_scope_status_change_counts_as_progress(repo):
    """Progress is measured from artifacts that already exist, so a subtask
    moving to DONE counts even when no commit was made."""
    (repo / "task_scope.md").write_text("| a | f.py | qa | PENDING |\n")
    lg.start(10, "tests pass")
    lg.check()
    (repo / "task_scope.md").write_text("| a | f.py | qa | DONE |\n")
    assert lg.check() == 0
    assert loop_block(repo)["stagnant_iterations"] == 0


# --- Sprint 051: the canonical task_scope.md is inside the sprint directory ---


def _nested_sprint(repo: Path, rows: str) -> Path:
    """A host's real layout: task_scope.md inside `docs/sprints/[ID]-...`."""
    sprint = repo / "docs" / "sprints" / "051-core-pipeline"
    sprint.mkdir(parents=True)
    (sprint / "task_scope.md").write_text(rows, encoding="utf-8")
    (repo / "docs" / "active_state.json").write_text(
        json.dumps({"current_sprint": {"id": "051", "path": str(
            sprint.relative_to(repo))}}),
        encoding="utf-8",
    )
    return sprint


def test_a_nested_task_scope_is_found_through_the_anchor(repo):
    """`agents.md §5` puts the file in the sprint directory, and the anchor
    names that directory. A bare relative path resolved to the repository root
    instead — where no host keeps it."""
    sprint = _nested_sprint(repo, "| a | f.py | qa | PENDING |\n")
    # Relative by design: `agents.md §1 path_type` forbids absolute paths, and
    # the anchor stores the sprint directory relative to the repository root.
    assert lg.task_scope_path() == sprint.relative_to(repo) / "task_scope.md"
    assert lg.status_hash() != ""


def test_a_nested_status_change_counts_as_progress(repo):
    """The defect this closes was silent: `status_hash` returns "" for a missing
    file, so the Status-column half of the progress signal never fired in any
    host with a nested sprint directory. A guard that cannot see movement
    cannot see its absence either."""
    sprint = _nested_sprint(repo, "| a | f.py | qa | PENDING |\n")
    lg.start(10, "tests pass")
    lg.check()
    (sprint / "task_scope.md").write_text("| a | f.py | qa | DONE |\n")
    assert lg.check() == 0
    assert loop_block(repo)["stagnant_iterations"] == 0


def test_sprint_dir_flag_overrides_the_anchor(repo):
    """Same flag as the sibling checks, and it wins over the anchor."""
    _nested_sprint(repo, "| a | f.py | qa | PENDING |\n")
    other = repo / "elsewhere"
    other.mkdir()
    (other / "task_scope.md").write_text("| b | g.py | qa | DONE |\n", encoding="utf-8")
    assert lg.task_scope_path(str(other)) == other / "task_scope.md"
    assert lg.status_hash(str(other)) != lg.status_hash()


def test_the_repository_root_path_still_works_without_an_anchor_sprint(repo):
    """Backward compatibility: a repository that really keeps it at the root
    must not regress just because the anchor names no sprint."""
    (repo / "task_scope.md").write_text("| a | f.py | qa | PENDING |\n")
    assert lg.task_scope_path() == Path("task_scope.md")
    assert lg.status_hash() != ""


def _cli(repo: Path, *args: str) -> int:
    """Run the script as a process, which is how every caller reaches it."""
    return subprocess.run(
        [sys.executable, str(Path(lg.__file__).resolve()), *args],
        cwd=repo, capture_output=True, text=True,
    ).returncode


def test_current_sprint_fails_closed_when_the_anchor_names_no_sprint(repo):
    """Gate 1's `F-5`: the flag the done-criterion demanded was never shipped.

    It is not an alias for the default. The default falls back to the repository
    root; this refuses to, because a loop measuring progress from a file that is
    not there reads every iteration as stagnant — and fail-closed is the whole
    design of this script."""
    (repo / "task_scope.md").write_text("| a | f.py | qa | PENDING |\n")
    assert _cli(repo, "check", "--current-sprint") == 2


def test_current_sprint_resolves_the_nested_directory_the_anchor_names(repo):
    """With a sprint declared, the flag targets it rather than the root."""
    _nested_sprint(repo, "| a | f.py | qa | PENDING |\n")
    assert _cli(repo, "start", "--max-iterations", "3", "--success", "tests pass",
                "--current-sprint") == 0
    assert loop_block(repo)["last_status_hash"] != ""


def test_the_two_scope_flags_together_are_refused(repo):
    """Two ways to name one thing is a caller error, not a precedence puzzle."""
    _nested_sprint(repo, "| a | f.py | qa | PENDING |\n")
    assert _cli(repo, "check", "--current-sprint", "--sprint-dir", "x") == 2
