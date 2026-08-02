"""Tests for the session-protocol mechanisms added in Phase 019.

Every case asserts the mechanism FAILS where it must. A gate proven only on a
healthy tree proves nothing — the lesson PR #28 left behind.
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))
import branch_sovereignty as bs  # noqa: E402
import session_state as ss  # noqa: E402


# --- session lock ------------------------------------------------------

@pytest.fixture
def anchor(tmp_path, monkeypatch):
    (tmp_path / "docs").mkdir()
    monkeypatch.chdir(tmp_path)
    return tmp_path / "docs" / "active_state.json"


def test_claim_writes_the_state_start_never_wrote(anchor):
    assert ss.claim("session-a", takeover=False) == 0
    state = json.loads(anchor.read_text())
    assert state["status"] == "IN_PROGRESS"
    assert state["session_id"] == "session-a"
    assert state["start_time"]


def test_second_session_is_blocked_with_exit_2(anchor):
    ss.claim("session-a", takeover=False)
    assert ss.claim("session-b", takeover=False) == 2
    # The first session keeps the lock: a refused claim must not half-write.
    assert json.loads(anchor.read_text())["session_id"] == "session-a"


def test_takeover_is_explicit_and_works(anchor):
    ss.claim("session-a", takeover=False)
    assert ss.claim("session-b", takeover=True) == 0
    assert json.loads(anchor.read_text())["session_id"] == "session-b"


def test_reclaim_by_same_session_is_not_a_collision(anchor):
    ss.claim("session-a", takeover=False)
    assert ss.claim("session-a", takeover=False) == 0


def test_release_marks_closed(anchor):
    ss.claim("session-a", takeover=False)
    assert ss.release() == 0
    state = json.loads(anchor.read_text())
    assert state["status"] == "CLOSED_SUCCESSFULLY"
    assert state["end_time"]


# --- branch sovereignty ------------------------------------------------

@pytest.fixture
def repo(tmp_path, monkeypatch):
    """A real repository, because these checks are about git semantics."""
    monkeypatch.chdir(tmp_path)
    run = lambda *a: subprocess.run(["git", *a], capture_output=True, text=True, check=True)
    run("init", "-q", "-b", "main")
    run("config", "user.email", "t@example.com")
    run("config", "user.name", "T")
    (tmp_path / "f.txt").write_text("base\n")
    run("add", "-A")
    run("commit", "-qm", "base")
    return tmp_path


def test_branch_with_unique_work_is_reported(repo):
    subprocess.run(["git", "checkout", "-qb", "feature"], check=True)
    (repo / "f.txt").write_text("changed\n")
    subprocess.run(["git", "commit", "-aqm", "work"], check=True)
    subprocess.run(["git", "checkout", "-q", "main"], check=True)
    assert bs.audit("main") == 2


def test_branch_whose_commits_are_in_main_passes(repo):
    subprocess.run(["git", "checkout", "-qb", "merged-branch"], check=True)
    (repo / "f.txt").write_text("changed\n")
    subprocess.run(["git", "commit", "-aqm", "work"], check=True)
    subprocess.run(["git", "checkout", "-q", "main"], check=True)
    subprocess.run(["git", "merge", "-q", "merged-branch"], check=True)
    assert bs.audit("main") == 0


def test_waived_branch_does_not_block(repo):
    subprocess.run(["git", "checkout", "-qb", "abandoned"], check=True)
    (repo / "f.txt").write_text("changed\n")
    subprocess.run(["git", "commit", "-aqm", "work"], check=True)
    subprocess.run(["git", "checkout", "-q", "main"], check=True)
    (repo / "config").mkdir()
    bs.WAIVERS.write_text(json.dumps(
        {"abandoned": [{"branch": "abandoned", "reason": "superseded experiment"}]}
    ))
    assert bs.audit("main") == 0


def test_prune_never_deletes_unproven_work(repo):
    subprocess.run(["git", "checkout", "-qb", "unmerged"], check=True)
    (repo / "f.txt").write_text("changed\n")
    subprocess.run(["git", "commit", "-aqm", "work"], check=True)
    subprocess.run(["git", "checkout", "-q", "main"], check=True)
    bs.prune("main")
    branches = subprocess.run(
        ["git", "for-each-ref", "--format=%(refname:short)", "refs/heads/"],
        capture_output=True, text=True,
    ).stdout.split()
    assert "unmerged" in branches
