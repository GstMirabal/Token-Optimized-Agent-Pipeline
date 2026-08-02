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
