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
import detect_drift as dd  # noqa: E402
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


# --- drift detection ---------------------------------------------------

def test_no_baseline_is_reported_not_silently_passed(anchor, capsys):
    """Silence about an unmeasurable state is what let the v4.3.0 drift last."""
    anchor.write_text(json.dumps({"status": "CLOSED_SUCCESSFULLY"}))
    assert dd.main() == 0
    assert "baseline" in capsys.readouterr().out


def test_commits_after_the_sealed_close_are_drift(repo):
    (repo / "docs").mkdir()
    baseline = subprocess.run(["git", "rev-parse", "HEAD"],
                              capture_output=True, text=True).stdout.strip()
    (repo / "f.txt").write_text("out of protocol\n")
    subprocess.run(["git", "commit", "-aqm", "outside"], check=True)
    (repo / "docs" / "active_state.json").write_text(
        json.dumps({"status": "CLOSED_SUCCESSFULLY", "last_close_commit": baseline})
    )
    assert dd.main() == 2


def test_head_matching_the_sealed_close_is_clean(repo):
    (repo / "docs").mkdir()
    head = subprocess.run(["git", "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()
    (repo / "docs" / "active_state.json").write_text(
        json.dumps({"status": "CLOSED_SUCCESSFULLY", "last_close_commit": head})
    )
    assert dd.main() == 0


def test_unknown_baseline_does_not_crash(repo):
    """A rewritten history or a different clone must degrade, not explode."""
    (repo / "docs").mkdir()
    (repo / "docs" / "active_state.json").write_text(
        json.dumps({"last_close_commit": "0" * 40})
    )
    assert dd.main() == 0


# --- drift verdicts (ADR-0002) -----------------------------------------

def _head() -> str:
    return subprocess.run(["git", "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()


def _commit(repo, text: str, message: str) -> str:
    """Commit distinct content. The `repo` fixture already committed 'base'."""
    (repo / "f.txt").write_text(text)
    subprocess.run(["git", "commit", "-aqm", message], check=True)
    return _head()


def _ledger(repo, released: list[str], unreleased: str = "") -> None:
    body = f"# Changelog\n\n## [Unreleased]\n{unreleased}\n"
    for version in released:
        body += f"\n## [{version}] - 2026-01-01\n- an entry\n"
    (repo / "CHANGELOG.md").write_text(body)


def _baseline(repo, sha: str) -> None:
    (repo / "docs").mkdir(exist_ok=True)
    (repo / "docs" / "active_state.json").write_text(
        json.dumps({"last_close_commit": sha})
    )


def test_sealed_range_is_not_drift(repo, capsys):
    """The live defect: deployment seals and tags, and the check cried wolf."""
    base = _head()
    _commit(repo, "work\n", "work")
    subprocess.run(["git", "tag", "v1.1.0"], check=True)
    _ledger(repo, ["1.1.0"])
    _baseline(repo, base)

    assert dd.main() == 0
    out = capsys.readouterr().out
    assert "v1.1.0" in out
    # The limit must be stated, or `S` reads as "every commit documented".
    assert "RANGE" in out


def test_unrecorded_range_is_still_drift(repo):
    """Anti-whitewash calibration — the Phase 018 scenario.

    If this ever returns 0 the fix has certified genuine drift as sealed, which
    is worse than crying wolf: a false clean verdict reads as evidence. The
    abort criterion in the Sprint 024 plan is keyed on this test.
    """
    base = _head()
    subprocess.run(["git", "tag", "v1.0.0"], check=True)
    _commit(repo, "unrecorded\n", "outside the protocol")
    _ledger(repo, ["1.0.0"])          # nothing covers the commit after the tag
    _baseline(repo, base)

    assert dd.main() == 2


def test_mixed_range_reports_only_the_unsealed(repo, capsys):
    """A partially sealed range must name the uncovered commits, not all of them."""
    base = _head()
    _commit(repo, "sealed\n", "already released")
    subprocess.run(["git", "tag", "v1.1.0"], check=True)
    _commit(repo, "loose\n", "landed after the tag")
    _ledger(repo, ["1.1.0"])
    _baseline(repo, base)

    assert dd.main() == 2
    err = capsys.readouterr().err
    assert "landed after the tag" in err
    # Messages must not overlap as substrings, or this assertion cannot fail.
    assert "already released" not in err


def test_nonempty_unreleased_is_indeterminate_not_clean(repo, capsys):
    """Entries may cover the commits, but reachability cannot prove it per commit."""
    base = _head()
    _commit(repo, "work\n", "work")
    _ledger(repo, ["1.0.0"], unreleased="- something was recorded here\n")
    subprocess.run(["git", "tag", "v1.0.0", base], check=True)
    _baseline(repo, base)

    assert dd.main() == 2
    assert "per commit" in capsys.readouterr().err


def test_no_sealing_tag_cannot_clear_the_range(repo, capsys):
    """Unproven coverage is not coverage — the case a pre-existing test caught.

    An earlier design returned 0 here ("nothing measurable"), which whitewashed
    the Phase 018 scenario in its early form: commits after the baseline in a
    repository that has never released anything.
    """
    base = _head()
    _commit(repo, "work\n", "work")
    _ledger(repo, [])
    _baseline(repo, base)

    assert dd.main() == 2
    assert "nothing proves any of" in capsys.readouterr().err


def test_tag_without_a_ledger_section_does_not_seal(repo):
    """This repository carries v3.4.0 and v3.5.2 with no section; they seal nothing."""
    base = _head()
    _commit(repo, "work\n", "work")
    subprocess.run(["git", "tag", "v9.9.9"], check=True)
    _ledger(repo, ["1.0.0"])          # v9.9.9 owns no section
    _baseline(repo, base)

    assert dd.main() == 2
    assert dd.sealing_tags() == []


def test_orphaned_baseline_falls_back_to_merge_base(repo, capsys):
    """A squash-merged sprint branch leaves the recorded baseline off-branch.

    `git cat-file -e` cannot catch it — the object still exists — so without
    the merge-base fallback the range lists the whole history since the fork.
    """
    fork = _head()
    subprocess.run(["git", "checkout", "-qb", "sprint"], check=True)
    orphan = _commit(repo, "on the branch\n", "branch work")
    subprocess.run(["git", "checkout", "-q", "main"], check=True)
    _commit(repo, "squashed\n", "squashed onto main")
    subprocess.run(["git", "tag", "v1.1.0"], check=True)
    _ledger(repo, ["1.1.0"])
    _baseline(repo, orphan)

    assert dd.main() == 0
    assert "merge-base" in capsys.readouterr().err
    assert dd.resolve_baseline(orphan)[0] == fork


def test_baseline_on_the_branch_is_not_substituted(repo):
    """The fallback must fire only when it has to — regression guard."""
    base = _head()
    _commit(repo, "work\n", "work")
    assert dd.resolve_baseline(base) == (base, None)
