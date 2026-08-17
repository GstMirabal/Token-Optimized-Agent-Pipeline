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
import _mode  # noqa: E402
import session_cost as sc  # noqa: E402
import branch_sovereignty as bs  # noqa: E402
import detect_drift as dd  # noqa: E402
import session_state as ss  # noqa: E402
import submodule_purity as sp  # noqa: E402


# --- jurisdiction: host work never lands inside the submodule -----------

def _tiny_repo(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    run = lambda *a: subprocess.run(["git", *a], cwd=path, check=True,
                                    capture_output=True, text=True)
    run("init", "-q", "-b", "main")
    run("config", "user.email", "t@example.com")
    run("config", "user.name", "T")
    (path / "agents.md").write_text("# constitution\n")
    run("add", "-A")
    run("commit", "-qm", "base")


def test_a_git_directory_is_the_nucleus(tmp_path, monkeypatch):
    monkeypatch.setattr(_mode, "agents_dir", lambda: tmp_path)
    (tmp_path / ".git").mkdir()
    assert _mode.is_nucleus() is True


def test_a_git_pointer_file_is_a_submodule_checkout(tmp_path, monkeypatch):
    """git's own layout is the discriminator; nothing has to be configured."""
    monkeypatch.setattr(_mode, "agents_dir", lambda: tmp_path)
    (tmp_path / ".git").write_text("gitdir: ../.git/modules/.agents\n")
    assert _mode.is_nucleus() is False


def test_nucleus_mode_never_blocks_even_on_a_dirty_tree(tmp_path, monkeypatch):
    """The mirror of Sprint 024's D7: a guard must not fire inside its own jurisdiction.

    The branch-sovereignty gate refused the very branch it was sealing. A
    jurisdiction guard that refused the framework's own sprint would be that
    defect rebuilt, and it would block every nucleus close.
    """
    _tiny_repo(tmp_path)
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "loose.md").write_text("uncommitted work\n")
    monkeypatch.setattr(sp, "is_nucleus", lambda: True)
    monkeypatch.setattr(sp, "agents_dir", lambda: tmp_path)
    assert sp.main() == 0


def test_a_clean_submodule_passes(tmp_path, monkeypatch):
    _tiny_repo(tmp_path)
    monkeypatch.setattr(sp, "is_nucleus", lambda: False)
    monkeypatch.setattr(sp, "agents_dir", lambda: tmp_path)
    assert sp.main() == 0


def test_host_sprint_records_written_into_the_submodule_are_refused(
    tmp_path, monkeypatch, capsys
):
    """The contamination case, and the one .gitignore used to hide entirely."""
    _tiny_repo(tmp_path)
    sprint = tmp_path / "docs" / "sprints" / "085-backend-api"
    sprint.mkdir(parents=True)
    (sprint / "task_scope.md").write_text("a host's sprint scope\n")
    monkeypatch.setattr(sp, "is_nucleus", lambda: False)
    monkeypatch.setattr(sp, "agents_dir", lambda: tmp_path)

    assert sp.main() == 2
    err = capsys.readouterr().err
    assert "085-backend-api" in err
    # The remedy must name the HOST root, or the reader moves it sideways.
    assert "HOST root" in err


def test_editing_the_framework_in_place_is_classified_separately(
    tmp_path, monkeypatch, capsys
):
    """A modified tracked file is the strict_rule violation proper, not misplaced records."""
    _tiny_repo(tmp_path)
    (tmp_path / "agents.md").write_text("# constitution, patched by a host\n")
    monkeypatch.setattr(sp, "is_nucleus", lambda: False)
    monkeypatch.setattr(sp, "agents_dir", lambda: tmp_path)

    assert sp.main() == 2
    err = capsys.readouterr().err
    assert "tracked framework file" in err
    assert "feedback_upstream" in err


def test_an_ignored_only_dirty_state_is_not_contamination(tmp_path, monkeypatch):
    """venv_skillopt/, memory/ and the anchor are transient by design."""
    _tiny_repo(tmp_path)
    (tmp_path / ".gitignore").write_text("venv_skillopt/\n")
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-qm", "ignore"], cwd=tmp_path, check=True,
                   capture_output=True)
    (tmp_path / "venv_skillopt").mkdir()
    (tmp_path / "venv_skillopt" / "pyvenv.cfg").write_text("home = /usr\n")
    monkeypatch.setattr(sp, "is_nucleus", lambda: False)
    monkeypatch.setattr(sp, "agents_dir", lambda: tmp_path)
    assert sp.main() == 0


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


def test_the_branch_being_sealed_does_not_refuse_its_own_seal(repo):
    """close_workflow.md 5.5 runs on the sprint branch; Phase 6 leaves it unmerged.

    Auditing the checked-out branch made every close refuse itself. Verified on
    ai-sprint/024: audit passed until the first commit, then exited 2 naming that
    branch and advising the very integration Phase 6 defers to deployment.
    """
    subprocess.run(["git", "checkout", "-qb", "ai-sprint/999"], check=True)
    (repo / "f.txt").write_text("sprint work\n")
    subprocess.run(["git", "commit", "-aqm", "sprint work"], check=True)
    assert bs.audit("main") == 0


def test_the_same_branch_still_blocks_once_it_is_no_longer_checked_out(repo):
    """The exclusion is positional, not permanent — regression guard.

    A branch left behind by an earlier sprint is exactly what this gate exists
    to catch, and it must still catch it the moment it stops being HEAD.
    """
    subprocess.run(["git", "checkout", "-qb", "ai-sprint/999"], check=True)
    (repo / "f.txt").write_text("sprint work\n")
    subprocess.run(["git", "commit", "-aqm", "sprint work"], check=True)
    subprocess.run(["git", "checkout", "-q", "main"], check=True)
    assert bs.audit("main") == 2


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


# --- the nucleus can record its own pipeline state ---------------------

REPO_ROOT = Path(__file__).parent.parent


@pytest.mark.parametrize("path", [
    "docs/sprints/024-core-pipeline/task_scope.md",
    "docs/sprints/024-core-pipeline/graph_stats.json",
    "docs/sprints/024-core-pipeline/IMPLEMENTATION_PLAN.md",
])
def test_the_pipeline_record_is_not_hidden_from_git(path):
    """`git status --porcelain` does not list ignored files, and that is the point.

    `close_workflow.md` submodule_purity guards the submodule with exactly that
    command, so excluding these paths hid host contamination from the only check
    built to catch it — verified: a file created under docs/sprints/ left the
    command completely empty. It also made rules/documentation_standard.md:94
    impossible to satisfy, since that rule mandates a *git-tracked*
    graph_stats.json inside this very directory.

    Scoped to sprint CONTENT. docs/active_state.json stays ignored on purpose:
    it mixes durable record with live session state, and tracking it would ship
    the nucleus's session into every host checkout.
    """
    result = subprocess.run(
        ["git", "check-ignore", "-q", path],
        cwd=REPO_ROOT, capture_output=True,
    )
    assert result.returncode != 0, f"{path} is gitignored; submodule_purity cannot see it"


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


# --- cost instrumentation: the unit is the context cycle ----------------

def _turn(cache_read: int, model: str = "claude-opus-5", out: int = 100) -> str:
    return json.dumps({"message": {"model": model, "usage": {
        "input_tokens": 0, "output_tokens": out,
        "cache_read_input_tokens": cache_read, "cache_creation_input_tokens": 0}}})


def _transcript(tmp_path, lines: list[str], name: str = "s.jsonl"):
    p = tmp_path / name
    p.write_text("\n".join(lines) + "\n")
    return p


def test_two_resets_produce_three_cycles(tmp_path):
    """The defect the quartile view hid: a session is a sawtooth, not a ramp.

    Measuring against the session's first turn would stop the bound firing after
    the first reset, because the ratio collapses with the window.
    """
    lines = ([_turn(20_000), _turn(400_000), _turn(800_000)]
             + [_turn(20_000), _turn(500_000)]
             + [_turn(22_000), _turn(300_000)])
    result = sc.measure(_transcript(tmp_path, lines))
    assert len(result["cycles"]) == 3
    assert [c["messages"] for c in result["cycles"]] == [3, 2, 2]
    assert result["cycles"][0]["ratio"] == 40.0   # 800k / 20k
    assert result["cycles"][1]["ratio"] == 25.0   # 500k / 20k


def test_a_small_dip_is_not_a_reset(tmp_path):
    """Ordinary variation must not register as compaction — regression guard."""
    lines = [_turn(200_000), _turn(150_000), _turn(400_000)]
    assert len(sc.measure(_transcript(tmp_path, lines))["cycles"]) == 1


def test_a_drop_below_the_floor_is_not_a_reset(tmp_path):
    """Early small turns collapse in ratio without the window being rebuilt."""
    lines = [_turn(50_000), _turn(1_000), _turn(80_000)]
    assert len(sc.measure(_transcript(tmp_path, lines))["cycles"]) == 1


def test_synthetic_turns_are_discarded(tmp_path):
    """They are not API calls; counting them inflates every total."""
    lines = [_turn(10_000), _turn(999_999, model="<synthetic>"), _turn(20_000)]
    result = sc.measure(_transcript(tmp_path, lines))
    assert result["synthetic_skipped"] == 1
    assert result["totals"]["cache_read_input_tokens"] == 30_000
    assert "<synthetic>" not in result["by_model"]


def test_a_transcript_without_usage_says_so_instead_of_returning_zero(tmp_path):
    """A silent zero reads as 'this session was free' — the defect in
    docs_freshness_check.py that this program keeps finding in other shapes."""
    lines = [json.dumps({"message": {"model": "claude-opus-5"}}), "not json at all"]
    result = sc.measure(_transcript(tmp_path, lines))
    assert result["measurable"] is False
    assert "no usage" in result["reason"]


def test_totals_are_split_per_model(tmp_path):
    """Tier decisions are compared per model, so the meter must separate them."""
    lines = [_turn(10_000, model="claude-opus-5", out=500),
             _turn(20_000, model="claude-haiku-4-5", out=300)]
    models = sc.measure(_transcript(tmp_path, lines))["by_model"]
    assert models["claude-opus-5"]["output_tokens"] == 500
    assert models["claude-haiku-4-5"]["cache_read_input_tokens"] == 20_000


def test_the_meter_reports_no_currency(tmp_path):
    """Prices belong to config/model_tiers.json (Sprint 022). A price copied here
    would be stale the day it was written."""
    result = sc.measure(_transcript(tmp_path, [_turn(10_000)]))
    assert not any(k in json.dumps(result).lower() for k in ("usd", "$", "price", "cost_per"))
