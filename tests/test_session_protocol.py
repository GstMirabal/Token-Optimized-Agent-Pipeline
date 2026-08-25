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
import session_probe as spr  # noqa: E402
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
    monkeypatch.setattr(_mode, "agents_root", lambda: tmp_path)
    (tmp_path / ".git").mkdir()
    assert _mode.is_nucleus() is True


def test_a_git_pointer_file_is_a_submodule_checkout(tmp_path, monkeypatch):
    """git's own layout is the discriminator; nothing has to be configured."""
    monkeypatch.setattr(_mode, "agents_root", lambda: tmp_path)
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
    monkeypatch.setattr(sp, "agents_root", lambda: tmp_path)
    assert sp.main() == 0


def test_a_clean_submodule_passes(tmp_path, monkeypatch):
    _tiny_repo(tmp_path)
    monkeypatch.setattr(sp, "is_nucleus", lambda: False)
    monkeypatch.setattr(sp, "agents_root", lambda: tmp_path)
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
    monkeypatch.setattr(sp, "agents_root", lambda: tmp_path)

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
    monkeypatch.setattr(sp, "agents_root", lambda: tmp_path)

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
    monkeypatch.setattr(sp, "agents_root", lambda: tmp_path)
    assert sp.main() == 0


# --- session lock ------------------------------------------------------

@pytest.fixture
def anchor(tmp_path, monkeypatch):
    (tmp_path / "docs").mkdir()
    monkeypatch.chdir(tmp_path)
    return tmp_path / "docs" / "active_state.json"


def test_claim_writes_the_state_start_never_wrote(anchor):
    assert ss.claim("session-a", takeover=False, tool="terminal") == 0
    state = json.loads(anchor.read_text())
    assert state["status"] == "IN_PROGRESS"
    assert state["session_id"] == "session-a"
    assert state["start_time"]


def test_second_session_is_blocked_with_exit_2(anchor):
    ss.claim("session-a", takeover=False, tool="terminal")
    assert ss.claim("session-b", takeover=False, tool="terminal") == 2
    # The first session keeps the lock: a refused claim must not half-write.
    assert json.loads(anchor.read_text())["session_id"] == "session-a"


def test_takeover_is_explicit_and_works(anchor):
    ss.claim("session-a", takeover=False, tool="terminal")
    assert ss.claim("session-b", takeover=True, tool="terminal") == 0
    assert json.loads(anchor.read_text())["session_id"] == "session-b"


def test_reclaim_by_same_session_is_not_a_collision(anchor):
    ss.claim("session-a", takeover=False, tool="terminal")
    assert ss.claim("session-a", takeover=False, tool="terminal") == 0


def test_release_marks_closed(anchor):
    ss.claim("session-a", takeover=False, tool="terminal")
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


# --- anchor vs. the branch being worked --------------------------------
#
# Opening a sprint updates no field of the anchor — `claim` takes only a
# session id — so a cold session reads a sprint number nobody wrote. Found on
# the resume of Sprint 023, where the anchor said 22.

def _checkout(repo: Path, branch: str) -> None:
    subprocess.run(["git", "checkout", "-q", "-b", branch], cwd=repo, check=True,
                   capture_output=True)


def test_an_anchor_behind_the_branch_is_reported(repo):
    _checkout(repo, "ai-sprint/023")
    finding = spr.probe_anchor_sprint({"current_sprint": {"id": 22}})
    assert finding is not None
    assert "22" in finding and "ai-sprint/023" in finding


def test_an_anchor_that_agrees_is_silent(repo):
    _checkout(repo, "ai-sprint/023")
    assert spr.probe_anchor_sprint({"current_sprint": {"id": 23}}) is None


def test_a_branch_outside_the_convention_is_no_evidence_either_way(repo):
    """`main`, a hotfix branch or a detached HEAD say nothing about which
    sprint is active. Reporting a mismatch from them would be inventing one."""
    assert spr.probe_anchor_sprint({"current_sprint": {"id": 23}}) is None


def test_a_newer_sprint_directory_is_not_a_mismatch(repo, tmp_path):
    """The comparison deliberately ignores `docs/sprints/`.

    That looks like the equivalent signal and is not: measured on this
    repository, `024` and `025` exist as directories while `023` is
    legitimately in flight, so a directory-based check fires on a correct
    state. The branch is the sprint being worked (`RA-12`).
    """
    _checkout(repo, "ai-sprint/023")
    (tmp_path / "docs" / "sprints" / "025-core-pipeline").mkdir(parents=True)
    assert spr.probe_anchor_sprint({"current_sprint": {"id": 23}}) is None


def test_an_anchor_with_no_sprint_recorded_is_not_accused(repo):
    """A first run has no `current_sprint` yet. Absent is not wrong."""
    _checkout(repo, "ai-sprint/023")
    assert spr.probe_anchor_sprint({}) is None


# --- the platform probe answers in more than two values ----------------
#
# Sprint 023 C2. `security.get(control, {}).get("status") != "enabled"` made a
# field that was never returned indistinguishable from a control that is off,
# in a SECURITY report. `security_and_analysis` is omitted wholesale for a
# caller without administrative access, so the whole object going missing told
# a hardened repository that all three controls were disabled.

def test_a_control_that_is_on_reads_enabled():
    assert spr.analysis_state({"secret_scanning": {"status": "enabled"}},
                              "secret_scanning") == spr.ENABLED


def test_a_control_that_is_off_reads_disabled():
    assert spr.analysis_state({"secret_scanning": {"status": "disabled"}},
                              "secret_scanning") == spr.DISABLED


@pytest.mark.parametrize("payload", [
    {},                                          # key absent
    {"secret_scanning": {}},                     # present, no status
    {"secret_scanning": {"status": None}},       # present, null status
    {"secret_scanning": {"status": "not_set"}},  # a value this code does not know
    {"secret_scanning": None},                   # not an object at all
    None,                                        # the call did not answer
])
def test_only_an_explicit_disabled_is_reported_as_disabled(payload):
    """The defect, and the second version of it the Tester gate found.

    Absence became `disabled` at first. The repair then collapsed *everything
    that is not the string "enabled"* into `disabled`, which moved the same
    two-value collapse one level in rather than removing it. Safe to report all
    of these as doubt because a genuinely-off control is stated explicitly:
    this repository's live payload returns `secret_scanning_validity_checks:
    disabled` in full.
    """
    assert spr.analysis_state(payload, "secret_scanning") == spr.UNDETERMINED


def test_an_explicitly_disabled_control_is_still_an_accusation():
    """Doubt must not swallow the real finding — the inverse failure."""
    assert spr.analysis_state({"secret_scanning": {"status": "disabled"}},
                              "secret_scanning") == spr.DISABLED


def test_a_404_is_only_off_for_a_caller_who_could_have_seen_it():
    """Reproduced live by the Tester gate, and the reason this unit was rejected.

    GitHub answers `404` on an admin-only endpoint to any caller without
    administrative access, whether the feature is on or off. `cli/cli` and
    `torvalds/linux` — both demonstrably hardened — returned 404 on all three
    probed endpoints for a non-admin token, so mapping 404 to `disabled` told
    them they were exposed and offered to patch repositories the caller cannot
    administer. The first version of this test asserted the defect.
    """
    assert spr.state_from_exit(1, "gh: Not Found (HTTP 404)", True) == spr.DISABLED
    assert spr.state_from_exit(1, "gh: Not Found (HTTP 404)", False) == spr.UNDETERMINED
    assert spr.state_from_exit(1, "gh: Not Found (HTTP 404)", None) == spr.UNDETERMINED


def test_the_status_comes_from_the_status_not_from_a_substring():
    """Also reproduced with the real binary: a dead proxy on a repository whose
    NAME contains 404 emitted a transport error carrying the URL, and a 503 body
    read `upstream cache miss for /404/handler`. Both were classified as off."""
    proxy_failure = ('Get "https://api.github.com/repos/acme/tools404/vulnerability-alerts": '
                     'proxyconnect tcp: dial tcp 127.0.0.1:1: connect: connection refused')
    assert spr.state_from_exit(1, proxy_failure, True) == spr.UNDETERMINED
    assert spr.state_from_exit(
        1, "gh: upstream cache miss for /404/handler (HTTP 503)", True) == spr.UNDETERMINED
    assert spr.state_from_exit(0, "", False) == spr.ENABLED
    assert spr.http_status("gh: Not Found (HTTP 404)") == 404
    assert spr.http_status("dial tcp: no such host") is None


@pytest.mark.parametrize("payload,expected", [
    ('{"enabled": true, "paused": false}', "enabled"),
    ('{"enabled": true, "paused": true}', "paused"),
    ('{"enabled": false, "paused": false}', "disabled"),
    ('{"paused": false}', "undetermined"),        # no `enabled` at all
    ('{}', "undetermined"),
    ('{"enabled": null}', "undetermined"),
    ('{"enabled": "false"}', "undetermined"),     # truthiness would say ENABLED
    ('["not", "an", "object"]', "undetermined"),
    ("not json at all", "undetermined"),
])
def test_dependabot_updates_come_from_the_endpoint_that_answers_them(
    payload, expected, monkeypatch
):
    """`{"enabled": true, "paused": false}` is the live shape, verified against
    the API. `paused` is its own finding: enabled-but-paused applies nothing.

    The last six rows are the Tester gate's `D2` and `D3`. A missing `enabled`
    read as `disabled` while `analysis_state` read a missing key as doubt — two
    opposite rules for absence inside one unit, and the branch that failed was
    the security one. `{"enabled": "false"}` reported the control ON, the only
    false green in the unit.
    """
    assert spr.dependabot_updates_state(0, payload, "", True) == expected


def test_a_transient_failure_does_not_report_dependabot_as_off():
    assert spr.dependabot_updates_state(
        1, "", "gh: Server Error (HTTP 503)", True) == spr.UNDETERMINED


def test_branch_protection_reads_the_field_a_non_admin_can_see():
    """`branches/{b}/protection` is admin-only and 404s to everyone else, so it
    cannot tell an unprotected branch from an unprivileged caller. The public
    `protected` boolean can — measured on `cli/cli`, true while the admin
    endpoint returned 404."""
    assert spr.branch_protection_state(0, '{"protected": true}', "", False) == spr.ENABLED
    assert spr.branch_protection_state(0, '{"protected": false}', "", False) == spr.DISABLED
    assert spr.branch_protection_state(0, '{}', "", False) == spr.UNDETERMINED
    # `D6` on this function specifically. Its twin `dependabot_updates_state`
    # had the non-dict row and this one did not, so dropping the isinstance
    # guard here survived a green suite while raising AttributeError out of a
    # `main()` that has no try/except — every probe dies, not just this one.
    assert spr.branch_protection_state(0, '[]', "", True) == spr.UNDETERMINED
    assert spr.branch_protection_state(0, 'null', "", True) == spr.UNDETERMINED


def test_each_gated_endpoint_is_asked_exactly_once(monkeypatch):
    """The QA gate's `G-1`, round 2: `collect_security_controls` fetched an
    endpoint to derive the doubt line and the state function fetched the same
    endpoint again, so the cause explained a response that had not produced the
    state it annotated. Measured before the fix: 5 calls for 3 endpoints,
    `automated-security-fixes` and `branches/main` twice each.

    Counting calls rather than asserting a rendered string, because the defect
    was invisible in the output — both responses were identical under a healthy
    network, and only a failure between them diverged.

    The identity assertion is the Tester gate's `T-1`. Counting alone let `D2`
    be reverted in full while the suite stayed green: swapping
    `branches/{branch}` back to the admin-only `branches/{branch}/protection`
    keeps the count at three. That URL used to live inside
    `branch_protection_state`, where its own test could see it; moving the
    fetch to the caller moved it out of every test's reach, so the assertion
    belongs here now.
    """
    calls: list[str] = []

    def counting_gh_call(*args: str) -> tuple[int, str, str]:
        calls.append(" ".join(args))
        return 1, "", "gh: Not Found (HTTP 404)"

    monkeypatch.setattr(spr, "gh_call", counting_gh_call)
    spr.collect_security_controls("o/r", {}, True, "main")

    assert calls == [
        "api repos/o/r/automated-security-fixes",
        "api repos/o/r/vulnerability-alerts",
        "api repos/o/r/branches/main",
    ], calls


def test_a_doubt_line_states_the_cause_it_measured(monkeypatch):
    """Every doubt line used to read "field not returned" whatever had actually
    happened — the unit's own thesis violated one level down."""
    assert "HTTP 503" in spr.undetermined_cause(1, "gh: Server Error (HTTP 503)", True)
    assert "does not administer" in spr.undetermined_cause(
        1, "gh: Not Found (HTTP 404)", False)
    assert "no HTTP response" in spr.undetermined_cause(1, "dial tcp: no such host", True)


def test_a_non_dict_control_does_not_take_down_the_whole_probe():
    """`security[control].get("status")` raised AttributeError on a null value,
    and `probe_platform` has no try/except, so the graph, docs, anchor and cost
    findings would never print."""
    assert spr.analysis_state({"secret_scanning": None}, "secret_scanning") == spr.UNDETERMINED


def test_doubt_is_reported_apart_from_accusation_and_never_as_disabled(monkeypatch):
    """The two belong under different headings because they have different
    remedies: a disabled control needs `/agents:harden`, an unanswered question
    needs a token that can see the answer."""
    monkeypatch.setattr(spr.shutil, "which", lambda _: "/usr/bin/gh")
    monkeypatch.setattr(spr, "gh_json", lambda *a: (
        {"nameWithOwner": "o/r", "description": "d", "homepageUrl": "h",
         "defaultBranchRef": {"name": "main"}}
        if a[:2] == ("repo", "view") else None
    ))
    monkeypatch.setattr(spr, "gh_call", lambda *a: (1, "", "gh: Server Error (HTTP 503)"))
    monkeypatch.setattr(spr.Path, "exists", lambda self: True)
    monkeypatch.setattr(spr.Path, "is_dir", lambda self: True)

    report = spr.probe_platform({}, force=True)

    assert report is not None
    assert "cannot determine" in report
    assert "an unanswered question" in report
    # The accusation block must be absent entirely — asserted on its heading
    # rather than on the word "disabled", which legitimately appears in the
    # remedy sentence telling the reader not to treat doubt as a disabled control.
    assert "not in the state" not in report
    assert "/agents:harden" not in report
    assert "Re-run before treating any of these as disabled" in report


@pytest.mark.parametrize("admin,accuses", [(True, True), (False, False), (None, False)])
def test_the_admin_discriminator_is_read_from_the_repository_payload(
    admin, accuses, monkeypatch
):
    """The Tester gate's `T-2`. `permissions.admin` is what separates a 404
    meaning "off" from a 404 meaning "you cannot see this", so it is the whole
    of `D1`. Nothing pinned its extraction: replacing the lookup with a literal
    `None` passed the entire suite while turning the probe into the permanently
    closed gate the Implementation Plan names as an abort criterion.

    The pre-existing integration test cannot catch it — it stubs `gh_json` to
    return None for `api repos/{slug}`, so `is_admin` is already None inside it
    and a broken extraction is indistinguishable from a working one.

    Every endpoint answers 404 here, so the verdict is decided by `admin` alone:
    an administrator is told the controls are off, everyone else is told the
    probe could not see them.

    The two `security_and_analysis` controls are supplied as enabled so they
    contribute neither bucket. Left absent they land in doubt on their own —
    correctly, since the payload genuinely did not answer — and an admin would
    then produce both buckets at once, which measures the payload rather than
    the discriminator this test exists to pin.
    """
    monkeypatch.setattr(spr.shutil, "which", lambda _: "/usr/bin/gh")
    monkeypatch.setattr(spr, "gh_json", lambda *a: (
        {"nameWithOwner": "o/r", "description": "d", "homepageUrl": "h",
         "defaultBranchRef": {"name": "main"}}
        if a[:2] == ("repo", "view")
        else {"permissions": {"admin": admin},
              "security_and_analysis": {
                  "secret_scanning": {"status": "enabled"},
                  "secret_scanning_push_protection": {"status": "enabled"}}}
    ))
    monkeypatch.setattr(spr, "gh_call", lambda *a: (1, "", "gh: Not Found (HTTP 404)"))
    monkeypatch.setattr(spr.Path, "exists", lambda self: True)
    monkeypatch.setattr(spr.Path, "is_dir", lambda self: True)

    report = spr.probe_platform({}, force=True)

    assert report is not None
    assert ("Propose: `/agents:harden`" in report) is accuses, report
    assert ("an unanswered question" in report) is not accuses, report


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


def test_waived_branch_does_not_block(repo, monkeypatch):
    """The waiver list is patched, not written where the constant points.

    It used to be a bare relative path, so writing it landed inside the test's
    own `tmp_path`. Sprint 023 `C0.3` anchored it to the framework root — which
    is correct, and made this test overwrite the repository's real
    `config/abandoned_branches.json` with fixture data, destroying the three
    explanatory keys it ships with. Caught by reading a commit's diff rather
    than by any assertion, so the fixture is pinned here instead.
    """
    subprocess.run(["git", "checkout", "-qb", "abandoned"], check=True)
    (repo / "f.txt").write_text("changed\n")
    subprocess.run(["git", "commit", "-aqm", "work"], check=True)
    subprocess.run(["git", "checkout", "-q", "main"], check=True)
    (repo / "config").mkdir()
    waivers = repo / "config" / "abandoned_branches.json"
    waivers.write_text(json.dumps(
        {"abandoned": [{"branch": "abandoned", "reason": "superseded experiment"}]}
    ))
    monkeypatch.setattr(bs, "WAIVERS", waivers)
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


# --- branch sovereignty: "could not determine" is not a verdict --------
#
# The pull request lookup used to return a bool and map every non-zero exit to
# False, so a transient API failure read as "no merged PR exists". Measured
# against the live API: 2 of 12 calls returned rc=1, HTTP 503. Because
# content_is_integrated already returns False for every squash-merged branch,
# one 503 was enough to flip an integrated branch to unintegrated — reproduced
# as two triple-runs on an unchanged tree exiting 0,2,0 and 0,0,2, accusing a
# different branch each time.

REAL_RUN = subprocess.run


def _gh_returning(returncode, stderr="", stdout=""):
    """A stand-in for `gh` that leaves real `git` calls alone."""
    def run(cmd, **kwargs):
        if cmd and cmd[0] == "gh":
            return subprocess.CompletedProcess(cmd, returncode, stdout, stderr)
        return REAL_RUN(cmd, **kwargs)
    return run


@pytest.fixture
def gh_installed(monkeypatch):
    """Pretend `gh` is on PATH and remove the retry sleep."""
    monkeypatch.setattr(bs, "BACKOFF_SECONDS", 0)
    monkeypatch.setattr(bs.shutil, "which", lambda _: "/usr/bin/gh")


def test_a_transient_failure_is_undetermined_not_a_verdict(repo, gh_installed, monkeypatch):
    """HTTP 503 says nothing about whether a pull request was merged."""
    monkeypatch.setattr(bs.subprocess, "run",
                        _gh_returning(1, "HTTP 503: No server is currently available"))
    assert bs.merged_pr_exists("feature") == bs.UNKNOWN


def test_a_transient_failure_is_retried_before_giving_up(repo, gh_installed, monkeypatch):
    """The retry is what makes UNKNOWN rare enough to be worth blocking on."""
    calls = []

    def run(cmd, **kwargs):
        if cmd and cmd[0] == "gh":
            calls.append(1)
            if len(calls) < bs.ATTEMPTS:
                return subprocess.CompletedProcess(cmd, 1, "", "HTTP 503: unavailable")
            return subprocess.CompletedProcess(cmd, 0, '[{"number": 41}]', "")
        return REAL_RUN(cmd, **kwargs)

    monkeypatch.setattr(bs.subprocess, "run", run)
    assert bs.merged_pr_exists("feature") == bs.YES
    assert len(calls) == bs.ATTEMPTS


def test_no_github_side_is_a_definitive_no(repo, gh_installed, monkeypatch):
    """A repository with no remote can hold no pull requests, and that is an answer.

    Reporting it as UNKNOWN would refuse the seal forever in every local-only
    repository — trading an intermittently wrong gate for a permanently closed
    one, which is strictly worse. Retrying cannot conjure a remote either.
    """
    monkeypatch.setattr(bs.subprocess, "run", _gh_returning(1, "no git remotes found"))
    assert bs.merged_pr_exists("feature") == bs.NO


def test_missing_gh_is_declared_rather_than_assumed(repo, monkeypatch):
    monkeypatch.setattr(bs.shutil, "which", lambda _: None)
    assert bs.merged_pr_exists("feature") == bs.UNKNOWN


def test_a_negative_lookup_does_not_read_as_integrated(repo, monkeypatch):
    """Regression guard for the truthiness trap the three-valued answer introduces.

    The condition used to be `content_is_integrated(...) or merged_pr_exists(...)`.
    With strings, `NO` is non-empty and therefore truthy, so that chain would have
    reported *every* branch integrated — silently inverting the gate, which is far
    worse than the flakiness this change removes.
    """
    subprocess.run(["git", "checkout", "-qb", "feature"], check=True)
    (repo / "f.txt").write_text("changed\n")
    subprocess.run(["git", "commit", "-aqm", "work"], check=True)
    subprocess.run(["git", "checkout", "-q", "main"], check=True)
    monkeypatch.setattr(bs, "merged_pr_exists", lambda _: bs.NO)
    integrated, unintegrated, indeterminate, _ = bs.classify("main")
    assert unintegrated == ["feature"]
    assert integrated == [] and indeterminate == []


def test_undetermined_is_reported_as_such_and_offered_no_waiver(repo, capsys, monkeypatch):
    """It still blocks — but as doubt, not as an accusation.

    The waiver is permanent. Offering it here would invite silencing a branch
    whose work may be perfectly integrated, which is how a gate gets disabled
    instead of answered.
    """
    subprocess.run(["git", "checkout", "-qb", "feature"], check=True)
    (repo / "f.txt").write_text("changed\n")
    subprocess.run(["git", "commit", "-aqm", "work"], check=True)
    subprocess.run(["git", "checkout", "-q", "main"], check=True)
    monkeypatch.setattr(bs, "merged_pr_exists", lambda _: bs.UNKNOWN)

    assert bs.audit("main") == 2
    err = capsys.readouterr().err
    assert "could NOT be determined" in err
    assert "unintegrated work" not in err
    assert str(bs.WAIVERS) not in err


def test_prune_never_deletes_an_undetermined_branch(repo, monkeypatch):
    """Deletion is irreversible; a lookup that did not answer must not authorise it."""
    subprocess.run(["git", "checkout", "-qb", "maybe-merged"], check=True)
    (repo / "f.txt").write_text("changed\n")
    subprocess.run(["git", "commit", "-aqm", "work"], check=True)
    subprocess.run(["git", "checkout", "-q", "main"], check=True)
    monkeypatch.setattr(bs, "merged_pr_exists", lambda _: bs.UNKNOWN)

    bs.prune("main")
    branches = REAL_RUN(
        ["git", "for-each-ref", "--format=%(refname:short)", "refs/heads/"],
        capture_output=True, text=True,
    ).stdout.split()
    assert "maybe-merged" in branches


def _heads() -> list[str]:
    return REAL_RUN(
        ["git", "for-each-ref", "--format=%(refname:short)", "refs/heads/"],
        capture_output=True, text=True,
    ).stdout.split()


def _squash_feature_onto_main(repo: Path, branch: str) -> None:
    """Two commits on `branch`, collapsed onto main as one new SHA.

    Reproduces `gh pr merge --squash`: the branch tip is not an ancestor of
    main and `git branch --merged main` does not list it.
    """
    subprocess.run(["git", "checkout", "-qb", branch], check=True)
    (repo / "f.txt").write_text("one\n")
    subprocess.run(["git", "commit", "-aqm", "one"], check=True)
    (repo / "f.txt").write_text("two\n")
    subprocess.run(["git", "commit", "-aqm", "two"], check=True)
    subprocess.run(["git", "checkout", "-q", "main"], check=True)
    subprocess.run(["git", "merge", "-q", "--squash", branch], check=True)
    subprocess.run(["git", "commit", "-aqm", "squash"], check=True)


def test_git_branch_merged_misses_a_squash_merge(repo):
    """The instrument that would have left hotfix/H-002 and release/4.9.1 forever.

    Measured on this repository after PRs #51/#52:
    `git merge-base --is-ancestor hotfix/H-002 main` exits 1, and
    `git branch --merged main` lists neither leftover. A squash commit is a
    new SHA, not a descendant of the branch.
    """
    _squash_feature_onto_main(repo, "feature")
    ancestor = REAL_RUN(["git", "merge-base", "--is-ancestor", "feature", "main"])
    assert ancestor.returncode == 1
    merged = REAL_RUN(
        ["git", "branch", "--merged", "main"], capture_output=True, text=True,
    ).stdout
    assert "feature" not in merged
    assert bs.content_is_integrated("feature", "main") is False


def test_prune_deletes_a_squash_merged_branch_when_a_merged_pr_exists(
        repo, monkeypatch):
    """merged-PR state, not `git branch --merged`, authorises the delete."""
    _squash_feature_onto_main(repo, "feature")
    monkeypatch.setattr(bs, "merged_pr_exists", lambda _: bs.YES)
    bs.prune("main")
    assert "feature" not in _heads()


def _bare_origin(repo: Path, tmp_path: Path) -> Path:
    origin = tmp_path / "origin.git"
    REAL_RUN(["git", "init", "-q", "--bare", str(origin)], check=True)
    REAL_RUN(["git", "remote", "add", "origin", str(origin)], check=True)
    REAL_RUN(["git", "push", "-q", "origin", "main"], check=True)
    return origin


def test_prune_deletes_origin_head_of_a_proven_integrated_branch(repo, tmp_path):
    """`git remote prune origin` cannot delete a live origin head.

    GitHub `delete_branch_on_merge` is false on this nucleus
    (`gh api repos/:owner/:repo --jq .delete_branch_on_merge`). After a
    squash-merge the origin ref survives unless prune deletes it.
    """
    _bare_origin(repo, tmp_path)
    subprocess.run(["git", "checkout", "-qb", "feature"], check=True)
    (repo / "f.txt").write_text("changed\n")
    subprocess.run(["git", "commit", "-aqm", "work"], check=True)
    subprocess.run(["git", "push", "-q", "origin", "feature"], check=True)
    subprocess.run(["git", "checkout", "-q", "main"], check=True)
    subprocess.run(["git", "merge", "-q", "feature"], check=True)

    bs.prune("main")

    assert "feature" not in _heads()
    remote = REAL_RUN(
        ["git", "ls-remote", "--heads", "origin", "feature"],
        capture_output=True, text=True,
    )
    assert remote.stdout.strip() == ""


def test_prune_does_not_delete_origin_head_of_unproven_work(repo, tmp_path):
    _bare_origin(repo, tmp_path)
    subprocess.run(["git", "checkout", "-qb", "unmerged"], check=True)
    (repo / "f.txt").write_text("changed\n")
    subprocess.run(["git", "commit", "-aqm", "work"], check=True)
    subprocess.run(["git", "push", "-q", "origin", "unmerged"], check=True)
    subprocess.run(["git", "checkout", "-q", "main"], check=True)

    bs.prune("main")

    assert "unmerged" in _heads()
    remote = REAL_RUN(
        ["git", "ls-remote", "--heads", "origin", "unmerged"],
        capture_output=True, text=True,
    )
    assert "unmerged" in remote.stdout


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


# --- SUSPENDED: a session can end without sealing its sprint ------------

def test_suspend_does_not_write_the_close_baseline(anchor):
    """The whole point. last_close_commit means "where the last CLOSE sealed";
    writing it at session end would set a false baseline and blind detect_drift."""
    ss.claim("session-a", takeover=False, tool="terminal")
    anchor.write_text(json.dumps({**json.loads(anchor.read_text()),
                                  "last_close_commit": "baseline-sha"}))
    assert ss.suspend() == 0
    state = json.loads(anchor.read_text())
    assert state["status"] == "SUSPENDED"
    assert state["last_close_commit"] == "baseline-sha"
    assert state["end_time"]


def test_release_still_seals_the_sprint(repo):
    """The asymmetry's other half — regression to protect."""
    (repo / "docs").mkdir()
    ss.claim("session-a", takeover=False, tool="terminal")
    assert ss.release() == 0
    state = json.loads((repo / "docs" / "active_state.json").read_text())
    assert state["status"] == "CLOSED_SUCCESSFULLY"
    assert state["last_close_commit"]


def test_resuming_a_suspended_sprint_is_not_a_collision(anchor, capsys):
    """A planned handoff and a crash were indistinguishable before this state."""
    ss.claim("session-a", takeover=False, tool="terminal")
    ss.suspend()
    assert ss.claim("session-b", takeover=False, tool="terminal") == 0
    assert "Resuming" in capsys.readouterr().out


def test_a_live_session_still_blocks_a_second_one(anchor):
    """The collision guard must stay armed on IN_PROGRESS — regression guard."""
    ss.claim("session-a", takeover=False, tool="terminal")
    assert ss.claim("session-b", takeover=False, tool="terminal") == 2


def test_sessions_are_counted_across_a_suspended_sprint(anchor):
    """session_cost.py needs to know a sprint took three sessions, not three sprints."""
    ss.claim("session-a", takeover=False, tool="terminal")
    ss.suspend()
    ss.claim("session-b", takeover=False, tool="terminal")
    ss.suspend()
    ss.claim("session-c", takeover=False, tool="terminal")
    assert json.loads(anchor.read_text())["session_count"] == 3


# --- require-released: deployment preflight (close → deploy, never suspend) ---

def test_require_released_refuses_suspended(repo, capsys):
    """A suspended session must never chain into /agents:deployment."""
    (repo / "docs").mkdir()
    ss.claim("session-a", takeover=False, tool="terminal")
    ss.release()
    ss.claim("session-b", takeover=False, tool="terminal")
    ss.suspend()
    assert ss.require_released() == 2
    assert "SUSPENDED" in capsys.readouterr().out


def test_require_released_passes_after_release_on_sealed_tip(repo, capsys):
    """Close seals HEAD; deploy merges that tip — tip must equal last_close_commit."""
    (repo / "docs").mkdir()
    ss.claim("session-a", takeover=False, tool="terminal")
    assert ss.release() == 0
    assert ss.require_released() == 0
    assert "Deploy preflight passed" in capsys.readouterr().out


def test_require_released_refuses_unsealed_tip(repo, capsys):
    """IN_PROGRESS commits after the last seal are not deployable as HEAD."""
    (repo / "docs").mkdir()
    ss.claim("session-a", takeover=False, tool="terminal")
    ss.release()
    sealed = json.loads((repo / "docs" / "active_state.json").read_text())[
        "last_close_commit"
    ]
    (repo / "extra.txt").write_text("after close\n")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-qm", "after close"],
        cwd=repo,
        check=True,
        capture_output=True,
    )
    ss.claim("session-b", takeover=False, tool="terminal")
    assert ss.require_released() == 2
    out = capsys.readouterr().out
    assert sealed[:7] in out
    assert "not the sealed close" in out


def test_require_released_accepts_explicit_sealed_branch(repo, capsys):
    """Later claim may move HEAD; --branch still deploys the sealed tip."""
    (repo / "docs").mkdir()
    ss.claim("session-a", takeover=False, tool="terminal")
    ss.release()
    sealed = json.loads((repo / "docs" / "active_state.json").read_text())[
        "last_close_commit"
    ]
    subprocess.run(
        ["git", "branch", "ai-sprint/029", sealed],
        cwd=repo,
        check=True,
        capture_output=True,
    )
    (repo / "extra.txt").write_text("next sprint\n")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-qm", "next"],
        cwd=repo,
        check=True,
        capture_output=True,
    )
    ss.claim("session-b", takeover=False, tool="terminal")
    assert ss.require_released("ai-sprint/029") == 0
    assert "Deploy preflight passed" in capsys.readouterr().out


# --- P8.1: UID generation and tool recording for portability --------
#
# When `--session-id` is omitted (as in Cursor, which exposes no session UID
# to the caller), `claim()` generates a UID. These tests verify the mechanism
# that enables tool migration: P8 makes it possible for a Cursor session to
# claim the lock after Claude Code suspends, because the collision guard is
# no longer bound to the harness's own session identifier.


def test_claim_without_session_id_generates_uid(anchor):
    """When session_id is None, claim() generates a UID with form `<timestamp>-<PID>`.

    The form is chosen for forensics legibility, not uniqueness — a collision
    guard that compares UIDs as opaque strings is satisfied by any unique
    string. The timestamp + PID combination is legible in a crash report
    without tooling.
    """
    assert ss.claim(None, takeover=False, tool="terminal") == 0
    state = json.loads(anchor.read_text())
    session_id = state["session_id"]

    # Must be non-empty and have the form <YYYYMMDDTHHMMSSZ>-<PID>
    assert session_id
    assert "-" in session_id
    parts = session_id.split("-")
    assert len(parts) >= 2
    # Timestamp part should contain T and Z
    assert "T" in parts[0]
    assert parts[0].endswith("Z")
    # PID part should be numeric
    assert parts[-1].isdigit()


def test_claim_records_session_tool(anchor):
    """The session_tool field is recorded in the state.

    Forensics must distinguish which tool left a session open, because the
    unlock path differs between Claude Code (running as subagent) and Cursor
    (keyboard command). The tool is written alongside the session_id.
    """
    assert ss.claim("session-a", takeover=False, tool="cursor") == 0
    state = json.loads(anchor.read_text())
    assert state["session_tool"] == "cursor"

    # Verify the default tool is "terminal" when not specified
    ss.claim("session-b", takeover=True, tool="terminal")
    state = json.loads(anchor.read_text())
    assert state["session_tool"] == "terminal"


def test_collision_guard_holds_for_generated_uids(anchor):
    """The collision guard is armed against generated UIDs.

    Two sessions claiming without providing UIDs must still result in the
    second blocking unless takeover is set. The guard does not care whether
    the UID was supplied by the caller or generated by the claim function.
    """
    # First session generates a UID
    assert ss.claim(None, takeover=False, tool="terminal") == 0
    first_id = json.loads(anchor.read_text())["session_id"]

    # Second session tries to claim with a different generated UID
    # (we supply a distinct explicit ID, but the mechanism is the same)
    assert ss.claim("session-b", takeover=False, tool="terminal") == 2

    # The first session's lock remains intact
    state = json.loads(anchor.read_text())
    assert state["session_id"] == first_id

    # Takeover succeeds
    assert ss.claim("session-b", takeover=True, tool="terminal") == 0
    state = json.loads(anchor.read_text())
    assert state["session_id"] == "session-b"


def test_claim_over_suspended_state_resumes(anchor, capsys):
    """Claiming over a SUSPENDED state resumes without triggering the collision guard.

    This is the critical mechanism of tool migration (Design §D0b): the
    sequence is suspend, install target tool, claim from target tool. If the
    collision guard fired on a SUSPENDED state, the migration would fail.

    The test verifies that a new session with a different UID can claim
    over SUSPENDED, that it prints a resume message, and that session_count
    increments to track multi-session sprints.
    """
    # First session claims and suspends
    assert ss.claim("session-a", takeover=False, tool="claude-code") == 0
    state = json.loads(anchor.read_text())
    assert state["session_id"] == "session-a"
    assert state["session_tool"] == "claude-code"

    assert ss.suspend() == 0
    state = json.loads(anchor.read_text())
    assert state["status"] == "SUSPENDED"
    assert state["session_count"] == 1

    # Second session (Cursor) claims with a generated UID over SUSPENDED
    assert ss.claim(None, takeover=False, tool="cursor") == 0
    state = json.loads(anchor.read_text())

    # The new session is recorded
    new_session_id = state["session_id"]
    assert new_session_id  # Generated, not empty
    assert new_session_id != "session-a"  # Different from first session
    assert state["session_tool"] == "cursor"

    # Status is back to IN_PROGRESS for the new session
    assert state["status"] == "IN_PROGRESS"

    # Session count incremented
    assert state["session_count"] == 2

    # Resume message was printed
    out = capsys.readouterr().out
    assert "Resuming" in out
    assert "session #2" in out


def test_suspend_records_where_to_resume(repo):
    """Degraded and declared: the registry-derived form arrives with C0.2."""
    (repo / "docs").mkdir()
    ss.claim("session-a", takeover=False, tool="terminal")
    ss.suspend()
    pointer = json.loads((repo / "docs" / "active_state.json").read_text())["resume_pointer"]
    assert pointer["branch"] == "main"
    assert pointer["at"]
    assert "registry pending" in pointer["derived_from"]


def test_suspend_does_not_launder_unrecorded_work(repo):
    """The abort criterion. If suspending cleared the drift, the new state would
    have broken the detector Sprint 024 repaired."""
    (repo / "docs").mkdir()
    baseline = subprocess.run(["git", "rev-parse", "HEAD"],
                              capture_output=True, text=True).stdout.strip()
    (repo / "docs" / "active_state.json").write_text(
        json.dumps({"status": "CLOSED_SUCCESSFULLY", "last_close_commit": baseline}))
    ss.claim("session-a", takeover=False, tool="terminal")
    (repo / "f.txt").write_text("work done in a suspended sprint\n")
    subprocess.run(["git", "commit", "-aqm", "mid-sprint work"], check=True)
    ss.suspend()
    assert dd.main() == 2


# --- model tiering: the map, the detector, the guards --------------------

import check_model_tiers as cmt  # noqa: E402
import detect_new_models as dnm  # noqa: E402

CATALOGUE_FIXTURE = """\
# Claude Model Catalog

| Friendly Name   | Alias (use this)  | Full ID  | Context | Max Output | Status |
|-----------------|-------------------|----------|---------|------------|--------|
| Claude Opus 5   | `claude-opus-5`   | —        | 1M      | 128K       | Active |
| Claude Sonnet 5 | `claude-sonnet-5` | —        | 1M      | 128K       | Active |
| Claude Opus 4.1 | `claude-opus-4-1` | `claude-opus-4-1-20250805` | Deprecated (retires 2026-08-05 — migrate to `claude-opus-5`) |
| Claude Haiku 3  | `claude-haiku-3`  | `claude-3-haiku-20240307`  | Retired |

## What users mean

| Phrase        | Model |
|---------------|-------|
| "sonnet 3.7"  | Retired — suggest `claude-sonnet-5` |
| "haiku 3"     | Deprecated — suggest `claude-opus-5` |
"""


def test_the_phrasing_table_does_not_overwrite_the_catalogue(tmp_path):
    """The bug that would have failed the build over a healthy tier.

    A first parser scanned each row for any alias and any status word, so
    `| "sonnet 3.7" | Retired — suggest \\`claude-sonnet-5\\` |` recorded Sonnet 5
    as Retired. Wired to the severity ladder, that fails `make verify` on a tier
    that is perfectly current. This fixture reproduces the real file's shape --
    without the phrasing table, the broken parser passes this test.
    """
    path = tmp_path / "models.md"
    path.write_text(CATALOGUE_FIXTURE)
    catalogue = dnm.parse_catalogue(path)
    assert catalogue["claude-sonnet-5"]["status"] == "Active"
    assert catalogue["claude-opus-5"]["status"] == "Active"


def test_status_is_read_from_rows_of_differing_width(tmp_path):
    """The catalogue's tables do not share a column count, so index-based reads fail."""
    path = tmp_path / "models.md"
    path.write_text(CATALOGUE_FIXTURE)
    catalogue = dnm.parse_catalogue(path)
    assert catalogue["claude-opus-4-1"]["status"] == "Deprecated"
    assert catalogue["claude-haiku-3"]["status"] == "Retired"


def test_a_retirement_date_is_captured_when_present(tmp_path):
    """It rides inside the status prose, which is what lets Deprecated carry a clock."""
    path = tmp_path / "models.md"
    path.write_text(CATALOGUE_FIXTURE)
    assert dnm.parse_catalogue(path)["claude-opus-4-1"]["retires"] == "2026-08-05"


def _tiers(gate="opus", snapshot=None) -> dict:
    return {
        "tiers": {"gate": {"claude_code": {"model": gate, "effort": "high"},
                           "profiles": ["qa_agent"]}},
        "catalog_snapshot": {"aliases": snapshot or {"claude-opus-5": "Active"}},
    }


def test_the_gate_reads_the_committed_snapshot_not_the_bundled_file():
    """The bundled catalogue is absent in CI, so a gate reading it would never fire
    exactly where nobody is watching -- a mechanism wired where it cannot run."""
    retired, _ = dnm.tier_status(
        _tiers(snapshot={"claude-opus-5": "Retired"}),
        dnm.snapshot_catalogue(_tiers(snapshot={"claude-opus-5": "Retired"})),
    )
    assert retired and "RETIRED" in retired[0]


def test_a_current_snapshot_clears_the_gate():
    retired, deprecated = dnm.tier_status(_tiers(), dnm.snapshot_catalogue(_tiers()))
    assert not retired and not deprecated


def test_a_new_alias_is_proposed_and_never_blocks(tmp_path):
    """A model is not adopted for existing; that is the evidence protocol's job."""
    path = tmp_path / "models.md"
    path.write_text(CATALOGUE_FIXTURE)
    fresh, _ = dnm.refresh_findings(_tiers(), dnm.parse_catalogue(path))
    assert "claude-sonnet-5" in fresh


def test_a_family_alias_resolves_to_the_newest_release(tmp_path):
    """Profiles declare `opus`, never a pinned ID -- the alias absorbs bumps."""
    path = tmp_path / "models.md"
    path.write_text(CATALOGUE_FIXTURE)
    alias, entry = dnm.resolve("opus", dnm.parse_catalogue(path))
    assert alias == "claude-opus-5"
    assert entry["status"] == "Active"


def test_a_profile_whose_tier_disagrees_with_the_map_is_a_failure():
    """Not a typo: the harness reads `model:` and ignores `tier:`, so the file
    would claim one thing and the subagent do another."""
    problems = cmt.check_agreement(
        _tiers(), {"qa_agent": {"tier": "mechanical", "model": "opus"}}
    )
    assert any("declares tier" in p for p in problems)


def test_a_profile_agreeing_with_the_map_passes():
    assert not cmt.check_agreement(_tiers(), {"qa_agent": {"tier": "gate", "model": "opus"}})


def test_a_dated_model_id_is_rejected_by_the_pattern():
    """`claude-opus-4-1` is a legitimate alias; `...-20250805` pins one release."""
    assert cmt.DATED_ID.search("claude-opus-4-1-20250805")
    assert not cmt.DATED_ID.search("claude-opus-4-1")
    assert not cmt.DATED_ID.search("claude-haiku-4-5")
