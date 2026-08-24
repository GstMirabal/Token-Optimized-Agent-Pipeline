"""Tests for scripts/ci_gate.py — Sprint 023 `C10`.

What these pin is not the script's syntax but the single inversion it exists to
make. `gh pr checks [N] --watch` enumerated the checks GitHub had already
registered and waited for those; a required check with no run yet was not
waited for at all. Measured on pull request `#45`: `--watch` returned at roughly
`16:13` having seen only `audit`, while `Analyze (python)` completed at
`16:16:21`. The gate returned green over two checks that had not reported.

So the load-bearing test here is `test_a_required_check_with_no_run_is_pending`.
Every other test in this file guards a way that inversion could be undone: by
reading the required set from one source, by treating an unreadable source as an
empty one, or by letting an unprotected branch read as a verified one.

No test in this file reaches the network. `gh` is replaced at the seam
(`gh_json`), because a test whose verdict depends on GitHub being up tests
GitHub.
"""
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import ci_gate  # noqa: E402

REQUIRED = {"audit", "Analyze (python)", "CodeQL"}
SLUG = "owner/name"

# No verdict in this file needs more than a handful of `gh` calls. See `fake_gh`
# for why the ceiling exists at all.
CALL_CAP = 20

# The three `gh` calls `main()` makes before it can judge anything. Tests that
# drive `main()` start from these and override the one fragment they are about,
# so a test reads as its own deviation from a healthy repository.
HEALTHY = {
    "repo view": ({"nameWithOwner": SLUG}, ""),
    "baseRefName": ({"baseRefName": "main"}, ""),
    "protection": ({"contexts": sorted(REQUIRED),
                    "checks": [{"context": c} for c in sorted(REQUIRED)]}, ""),
    "rules/branches": ([], ""),
}

# The exact stderr `gh` emits, copied from a live run against this repository
# rather than recalled. Both are HTTP 404 and only the message separates them.
NOT_PROTECTED = "gh: Branch not protected (HTTP 404)"
NO_SUCH_BRANCH = "gh: Branch not found (HTTP 404)"


def fake_gh(responses: dict[str, tuple[object, str]]) -> Callable[[list[str]], tuple[object, str]]:
    """Build a `gh_json` replacement that answers by substring of the endpoint.

    Args:
        responses: fragment of the `gh` argument list mapped to the
            `(payload, error)` pair `gh_json` would return for it.

    Returns:
        Callable: a stand-in with `gh_json`'s signature, which raises on any
            call the test did not anticipate rather than returning a default —
            an unplanned call is a change in behaviour, not a detail.

    **Also bounded at `CALL_CAP` invocations**, which is not tidiness. Two
    mutations that remove `poll`'s exit conditions — dropping the deadline
    check, or ignoring `--no-wait` — turn the gate into an unbounded loop, and
    without this cap the suite detects them by *hanging*. A hang reads as
    infrastructure trouble in CI and gets retried; a failed assertion reads as
    the defect it is. Both mutants were detected either way, so this changes the
    quality of the signal rather than its presence.
    """
    calls = 0

    def _call(args: list[str]) -> tuple[object, str]:
        nonlocal calls
        calls += 1
        if calls > CALL_CAP:
            raise AssertionError(
                f"`gh` was called {calls} times for one verdict — the gate is "
                f"looping without an exit condition"
            )
        joined = " ".join(args)
        for fragment, answer in responses.items():
            if fragment in joined:
                return answer
        raise AssertionError(f"unexpected gh call: {joined}")
    return _call


def protection(contexts: list[str]) -> tuple[object, str]:
    """The shape the classic protection endpoint returns, as measured."""
    return {"contexts": contexts,
            "checks": [{"context": c, "app_id": 1} for c in contexts]}, ""


def check_run(name: str, conclusion: str,
              started_at: str = "2026-08-17T16:00:00Z") -> dict[str, Any]:
    """One completed `CheckRun` entry of a `statusCheckRollup`."""
    return {"__typename": "CheckRun", "name": name, "status": "COMPLETED",
            "conclusion": conclusion, "startedAt": started_at}


def rollup(*entries: dict[str, Any]) -> tuple[object, str]:
    """The `gh pr view --json statusCheckRollup` payload holding `entries`."""
    return {"statusCheckRollup": list(entries)}, ""


def _completed(returncode: int, stdout: str, stderr: str) -> subprocess.CompletedProcess:
    """What `subprocess.run` hands back, for tests that exercise `gh_json`."""
    return subprocess.CompletedProcess(args=["gh"], returncode=returncode,
                                       stdout=stdout, stderr=stderr)


def _gh_failing(stderr: str) -> Callable[..., subprocess.CompletedProcess]:
    """A `subprocess.run` that always fails with `stderr`.

    Args:
        stderr: the exact text `gh` writes, copied from a live run.

    Returns:
        Callable: a stand-in accepting `subprocess.run`'s call shape.
    """
    return lambda *args, **kwargs: _completed(1, "", stderr)


def drive(monkeypatch, capsys, responses: dict[str, tuple[object, str]],
          argv: list[str] | None = None) -> tuple[int, str, str]:
    """Run the real `main()` end to end with `gh` replaced at the seam.

    Args:
        monkeypatch: pytest fixture, used to replace `gh_json` and `sys.argv`.
        capsys: pytest fixture, used to read what the operator would see.
        responses: as `fake_gh`.
        argv: arguments after the program name; defaults to gating PR 45.

    Returns:
        tuple: `(exit_code, stdout, stderr)`.

    The Tester gate rejected round 1 of this unit because every test stopped at
    a pure function while **`main()` was never executed by anything**. Mutating
    the one line that issues the verdict — `if buckets[FAILED] or
    buckets[PENDING]` — to drop `PENDING` left all 25 tests green while the gate
    reprinted the exact false green PR `#45` produced. A gate is not its helpers;
    it is the exit code, so these tests assert the exit code.
    """
    monkeypatch.setattr(ci_gate, "gh_json", fake_gh(responses))
    monkeypatch.setattr(ci_gate.shutil, "which", lambda _: "/usr/bin/gh")
    monkeypatch.setattr(ci_gate.time, "sleep", lambda _: None)
    monkeypatch.setattr(sys, "argv", ["ci_gate.py", *(argv or ["45", "--no-wait"])])
    code = ci_gate.main()
    captured = capsys.readouterr()
    return code, captured.out, captured.err


# --- The defect ------------------------------------------------------------

def test_a_required_check_with_no_run_is_pending():
    """The PR `#45` case, and the whole reason this script replaced `--watch`.

    `audit` has reported and passed; the other two required checks have no run
    registered at all. The old gate saw one check, saw it green, and returned.
    """
    buckets = ci_gate.evaluate(REQUIRED, {"audit": ci_gate.PASSED})
    assert buckets[ci_gate.PENDING] == ["Analyze (python)", "CodeQL"]
    assert buckets[ci_gate.PASSED] == ["audit"]
    assert buckets[ci_gate.FAILED] == []


def test_an_unrelated_check_passing_does_not_satisfy_a_required_one():
    """`Analyze (actions)` ran green on PR `#45` and is not required. A gate
    keyed on "did the checks pass" rather than "did the required checks pass"
    counts it, which is how an unprotected repository reads clean."""
    observed = {"Analyze (actions)": ci_gate.PASSED, "audit": ci_gate.PASSED}
    buckets = ci_gate.evaluate(REQUIRED, observed)
    assert set(buckets[ci_gate.PENDING]) == {"Analyze (python)", "CodeQL"}


# --- The required set ------------------------------------------------------

def test_the_two_sources_are_unioned_not_first_wins(monkeypatch):
    """A repository can carry classic protection and a ruleset at once. Taking
    whichever answered first would silently drop the other half."""
    ruleset = [{"type": "required_status_checks",
                "parameters": {"required_status_checks": [{"context": "lint"}]}}]
    monkeypatch.setattr(ci_gate, "gh_json", fake_gh({
        "protection": protection(["audit"]),
        "rules/branches": (ruleset, ""),
    }))
    names, error = ci_gate.required_checks(SLUG, "main")
    assert error == ""
    assert names == {"audit", "lint"}


def test_rulesets_alone_do_not_prove_a_branch_requires_nothing(monkeypatch):
    """Measured on this repository: `rules/branches/main` returns `[]` while
    classic protection requires three checks. A gate reading only the rules
    endpoint would report a protected repository as declaring nothing."""
    monkeypatch.setattr(ci_gate, "gh_json", fake_gh({
        "protection": protection(sorted(REQUIRED)),
        "rules/branches": ([], ""),
    }))
    names, _ = ci_gate.required_checks(SLUG, "main")
    assert names == REQUIRED


def test_a_repository_with_no_rulesets_at_all_is_an_answer(monkeypatch):
    """A 404 from the rules endpoint means no ruleset governs the branch, which
    is a finding about the repository. Conflating it with an unreadable endpoint
    would push every repository without rulesets into `D3`'s doubt path."""
    monkeypatch.setattr(ci_gate, "gh_json", fake_gh({"rules": (None, ci_gate.NOT_FOUND)}))
    names, error = ci_gate.required_from_rulesets(SLUG, "main")
    assert names == set() and error == ""


def test_rulesets_that_are_not_about_status_checks_are_ignored(monkeypatch):
    """A ruleset list mixes rule types — deletion, linear history, required
    checks. Reading a `pull_request` rule as a check name would invent a
    requirement nothing can ever satisfy."""
    rules = [{"type": "deletion"},
             {"type": "non_fast_forward"},
             {"type": "required_status_checks",
              "parameters": {"required_status_checks": [{"context": "audit"}]}}]
    monkeypatch.setattr(ci_gate, "gh_json", fake_gh({"rules": (rules, "")}))
    names, error = ci_gate.required_from_rulesets(SLUG, "main")
    assert names == {"audit"} and error == ""


def test_branch_not_protected_is_an_answer(monkeypatch):
    """`Branch not protected` means classic protection requires nothing — a
    finding about the repository, which the gate then rejects as unverified."""
    monkeypatch.setattr(ci_gate, "gh_json", fake_gh({
        "protection": (None, ci_gate.NOT_FOUND),
        "rules/branches": ([], ""),
    }))
    names, error = ci_gate.required_checks(SLUG, "topic")
    assert names == set() and error == ""


def test_neither_source_readable_is_doubt_and_never_a_pass(monkeypatch):
    """The `C9` doctrine in the other direction. An unreadable required set is
    not an empty one: `None` reaches `main`, which exits 2 naming the cause."""
    monkeypatch.setattr(ci_gate, "gh_json", fake_gh({
        "protection": (None, ci_gate.FORBIDDEN),
        "rules/branches": (None, "HTTP 503"),
    }))
    names, error = ci_gate.required_checks(SLUG, "main")
    assert names is None
    assert ci_gate.FORBIDDEN in error and "503" in error


def test_one_unreadable_source_still_verifies_what_the_other_declares(monkeypatch, capsys):
    """Most host tokens lack the admin the protection endpoint needs. Blocking
    every non-admin operator produces a gate nobody can pass, which is a gate
    that gets deleted — so the readable half is verified and the gap printed."""
    ruleset = [{"type": "required_status_checks",
                "parameters": {"required_status_checks": [{"context": "audit"}]}}]
    monkeypatch.setattr(ci_gate, "gh_json", fake_gh({
        "protection": (None, ci_gate.FORBIDDEN),
        "rules/branches": (ruleset, ""),
    }))
    names, error = ci_gate.required_checks(SLUG, "main")
    assert names == {"audit"} and error == ""
    assert "may be incomplete" in capsys.readouterr().err


# --- Reducing one rollup entry --------------------------------------------

@pytest.mark.parametrize("conclusion", ["SUCCESS", "NEUTRAL", "SKIPPED"])
def test_reported_and_passed_conclusions(conclusion):
    """A required check that skips has reported. Failing it would block every
    conditionally-run workflow."""
    _, state, _ = ci_gate._state_of(check_run("audit", conclusion))
    assert state == ci_gate.PASSED


@pytest.mark.parametrize("conclusion", ["FAILURE", "CANCELLED", "TIMED_OUT",
                                        "ACTION_REQUIRED", "STALE"])
def test_conclusions_that_are_not_a_pass(conclusion):
    """Each of these means the check did not pass. Admitting any is the false
    green this file exists to remove."""
    _, state, _ = ci_gate._state_of(check_run("audit", conclusion))
    assert state == ci_gate.FAILED


def test_a_running_check_is_pending_not_failed():
    """Pending and failed have different remedies — wait versus fix — so a gate
    that conflates them sends the operator after the wrong one."""
    entry = {"__typename": "CheckRun", "name": "audit", "status": "IN_PROGRESS",
             "conclusion": None, "startedAt": "2026-08-17T16:12:03Z"}
    _, state, _ = ci_gate._state_of(entry)
    assert state == ci_gate.PENDING


def test_the_older_status_context_shape_is_understood():
    """Third-party integrations still publish a single `state` and no
    conclusion. Reading `conclusion` off these yields `FAILED` for a green one."""
    passing = {"__typename": "StatusContext", "context": "ci/external",
               "state": "SUCCESS", "createdAt": "2026-08-17T16:12:03Z"}
    assert ci_gate._state_of(passing)[1] == ci_gate.PASSED
    assert ci_gate._state_of({**passing, "state": "PENDING"})[1] == ci_gate.PENDING
    assert ci_gate._state_of({**passing, "state": "ERROR"})[1] == ci_gate.FAILED


def test_an_expected_status_is_pending_not_failed():
    """`EXPECTED` is a required status GitHub knows about and has not received.
    It is the commit-status spelling of the defect this gate exists for, so
    reading it as failed would be right for the wrong reason and would send the
    operator to fix a check that has simply not run."""
    entry = {"__typename": "StatusContext", "context": "ci/external",
             "state": "EXPECTED", "createdAt": "2026-08-17T16:12:03Z"}
    assert ci_gate._state_of(entry)[1] == ci_gate.PENDING


def test_a_status_context_carrying_a_null_conclusion_is_not_read_as_a_check_run():
    """The abort criterion of this unit, pinned.

    `gh` emits the union of both rollup shapes, so a `StatusContext` can arrive
    with `"conclusion": null` next to its real `state`. Dispatching on *which
    keys exist* rather than on `__typename` sends this entry down the `CheckRun`
    branch, where it finds no `status` and reports `PENDING` — a green
    third-party status that could never clear, and a merge path permanently
    closed. The first version of `_state_of` had exactly that bug.
    """
    entry = {"__typename": "StatusContext", "context": "ci/external",
             "state": "SUCCESS", "conclusion": None, "status": None,
             "createdAt": "2026-08-17T16:12:03Z"}
    assert ci_gate._state_of(entry)[1] == ci_gate.PASSED


# --- Duplicate runs --------------------------------------------------------

def test_the_most_recent_run_of_a_name_wins(monkeypatch):
    """PR `#45` carries two `audit` entries from two pushes. Judging a branch by
    a superseded run is the same class of error as judging it by no run."""
    monkeypatch.setattr(ci_gate, "gh_json", fake_gh({"pr view": rollup(
        check_run("audit", "FAILURE", "2026-08-17T16:12:03Z"),
        check_run("audit", "SUCCESS", "2026-08-17T16:12:43Z"))}))
    observed, error = ci_gate.observed_checks("45")
    assert error == "" and observed == {"audit": ci_gate.PASSED}


def test_a_superseded_pass_does_not_mask_a_later_failure(monkeypatch):
    """The same rule in the direction that matters for safety."""
    monkeypatch.setattr(ci_gate, "gh_json", fake_gh({"pr view": rollup(
        check_run("audit", "SUCCESS", "2026-08-17T16:12:03Z"),
        check_run("audit", "FAILURE", "2026-08-17T16:12:43Z"))}))
    observed, _ = ci_gate.observed_checks("45")
    assert observed == {"audit": ci_gate.FAILED}


def test_a_queued_rerun_is_not_discarded_for_the_pass_it_replaces(monkeypatch):
    """`D4`, and the fixture failure that hid it.

    `CheckRun.startedAt` is null until the run actually starts, so a queued
    re-run reduces to `""` — which sorts BELOW every real timestamp under a
    newest-wins rule and is thrown away in favour of the superseded pass it
    replaces. Push a fix commit, gate the pull request in the window before the
    new run starts, and the old green verdict is reported as current.

    Round 1's `test_a_superseded_pass_does_not_mask_a_later_failure` was written
    against exactly this risk and gave both runs real ordered timestamps, so it
    passed over the one input that breaks it. That is the same fixture failure
    `C4` shipped earlier in this sprint, caught here by the Tester gate rather
    than by this file's author.
    """
    queued = {"__typename": "CheckRun", "name": "audit", "status": "QUEUED",
              "conclusion": None, "startedAt": None}
    monkeypatch.setattr(ci_gate, "gh_json", fake_gh({"pr view": rollup(
        check_run("audit", "SUCCESS", "2026-08-17T16:12:03Z"), queued)}))
    observed, _ = ci_gate.observed_checks("45")
    assert observed == {"audit": ci_gate.PENDING}


def test_githubs_zero_timestamp_form_of_a_queued_run_is_also_pending(monkeypatch):
    """GitHub also spells an unstarted run `0001-01-01T00:00:00Z` rather than
    null, which sorts below real timestamps just the same."""
    queued = {"__typename": "CheckRun", "name": "audit", "status": "QUEUED",
              "conclusion": None, "startedAt": "0001-01-01T00:00:00Z"}
    monkeypatch.setattr(ci_gate, "gh_json", fake_gh({"pr view": rollup(
        check_run("audit", "SUCCESS", "2026-08-17T16:12:03Z"), queued)}))
    observed, _ = ci_gate.observed_checks("45")
    assert observed == {"audit": ci_gate.PENDING}


def test_a_run_with_an_older_real_timestamp_is_superseded(monkeypatch):
    """What the newest-group rule actually pins — stated after a test that
    claimed more than it proved.

    This test was originally named for the Tester gate's `P1`: a stale `QUEUED`
    entry no longer pinning a check whose later run completed. **It passed only
    because its fixture gave the `QUEUED` run a real `startedAt`**, which
    contradicts the premise stated in `_reduce_runs`'s own docstring — a queued
    run has no start time — and departs from the shape its two neighbouring
    `QUEUED` fixtures use. Given `startedAt: None`, the input it named still
    reduces to `PENDING`.

    That is `C4` fixture avoidance for the third time in this sprint, and it is
    the exact lesson `_reduce_runs` cites in the paragraph above the code it
    tests. `P1` is recorded as OPEN and unfixable from rollup data; this test
    now pins only the property the rule does have.
    """
    superseded = {"__typename": "CheckRun", "name": "audit", "status": "QUEUED",
                  "conclusion": None, "startedAt": "2026-08-17T16:00:00Z"}
    monkeypatch.setattr(ci_gate, "gh_json", fake_gh({"pr view": rollup(
        superseded, check_run("audit", "SUCCESS", "2026-08-17T16:12:03Z"))}))
    observed, _ = ci_gate.observed_checks("45")
    assert observed == {"audit": ci_gate.PASSED}


def test_p1_remains_open_an_unorderable_pending_run_still_pins(monkeypatch):
    """`P1` pinned as a KNOWN limitation, so it cannot be silently "fixed" by a
    change that only moves the false red somewhere else.

    A queued re-run and a stale queued entry present identical rollup data — an
    unorderable pending run beside a newer completed pass — so no timestamp rule
    can separate them. Erring toward `PENDING` is the deliberate choice: the
    alternative is `D4`'s false green. If a future change makes this return
    `PASSED`, `D4` is back, and this test is what says so.
    """
    for unstarted in (None, "0001-01-01T00:00:00Z"):
        queued = {"__typename": "CheckRun", "name": "audit", "status": "QUEUED",
                  "conclusion": None, "startedAt": unstarted}
        monkeypatch.setattr(ci_gate, "gh_json", fake_gh({"pr view": rollup(
            queued, check_run("audit", "SUCCESS", "2026-08-17T16:12:03Z"))}))
        observed, _ = ci_gate.observed_checks("45")
        assert observed == {"audit": ci_gate.PENDING}, (
            f"startedAt={unstarted!r} no longer pins the check — D4 is reopened"
        )


def test_both_unstarted_forms_rank_equally(monkeypatch):
    """The mutant that survived three rounds because nothing distinguished the
    filter from the guard that followed it.

    When both spellings of "not started" appear at once, treating them as
    ordered ranks `0001-01-01T00:00:00Z` above `""` and silently drops the `""`
    run from the newest group. Normalising them to one value weighs both, which
    is why this input reduces to `FAILED` and not `PASSED`.
    """
    def unstarted(at: str | None, state: str) -> dict[str, Any]:
        return {"__typename": "CheckRun", "name": "audit", "status": "COMPLETED",
                "conclusion": state, "startedAt": at}

    monkeypatch.setattr(ci_gate, "gh_json", fake_gh({"pr view": rollup(
        unstarted("0001-01-01T00:00:00Z", "SUCCESS"), unstarted(None, "FAILURE"))}))
    observed, _ = ci_gate.observed_checks("45")
    assert observed == {"audit": ci_gate.FAILED}


def test_a_pending_run_in_the_newest_group_still_pins_the_check(monkeypatch):
    """The boundary on the other side: a pending run that is NOT superseded must
    still block, or the fix above would reopen the false green it sits next to."""
    pending = {"__typename": "CheckRun", "name": "audit", "status": "IN_PROGRESS",
               "conclusion": None, "startedAt": "2026-08-17T16:12:03Z"}
    monkeypatch.setattr(ci_gate, "gh_json", fake_gh({"pr view": rollup(
        check_run("audit", "SUCCESS", "2026-08-17T16:00:00Z"), pending)}))
    observed, _ = ci_gate.observed_checks("45")
    assert observed == {"audit": ci_gate.PENDING}


def test_runs_that_are_all_unorderable_still_yield_a_verdict(monkeypatch):
    """A `StatusContext` reports no `startedAt` and may report no `createdAt`
    either, so every run of a name can be unorderable at once. With no newest
    group to compute, the reduction still has to answer — and `FAILED` wins,
    because a check that failed somewhere and cannot be ordered is not one to
    merge over."""
    def status(state: str) -> dict[str, Any]:
        return {"__typename": "StatusContext", "context": "ci/external", "state": state}

    monkeypatch.setattr(ci_gate, "gh_json", fake_gh({"pr view": rollup(
        status("SUCCESS"), status("FAILURE"))}))
    observed, _ = ci_gate.observed_checks("45")
    assert observed == {"ci/external": ci_gate.FAILED}

    monkeypatch.setattr(ci_gate, "gh_json", fake_gh({"pr view": rollup(
        status("SUCCESS"), status("SUCCESS"))}))
    observed, _ = ci_gate.observed_checks("45")
    assert observed == {"ci/external": ci_gate.PASSED}


def test_a_rollup_entry_with_no_name_is_skipped(monkeypatch):
    """The one branch edge the Tester's branch-coverage pass found untaken:
    `if name:` in `observed_checks` never saw its false side, so removing the
    guard changed nothing any test could see."""
    nameless = {"__typename": "CheckRun", "name": "", "status": "COMPLETED",
                "conclusion": "FAILURE", "startedAt": "2026-08-17T16:12:03Z"}
    monkeypatch.setattr(ci_gate, "gh_json", fake_gh({"pr view": rollup(
        nameless, check_run("audit", "SUCCESS"))}))
    observed, _ = ci_gate.observed_checks("45")
    assert observed == {"audit": ci_gate.PASSED}, (
        "an unnamed entry leaked into the observed set under a key no required "
        "check can match"
    )


def test_simultaneous_runs_resolve_toward_blocking(monkeypatch):
    """Equal timestamps are a tie, and the two errors do not cost the same."""
    monkeypatch.setattr(ci_gate, "gh_json", fake_gh({"pr view": rollup(
        check_run("audit", "SUCCESS", "2026-08-17T16:12:03Z"),
        check_run("audit", "FAILURE", "2026-08-17T16:12:03Z"))}))
    observed, _ = ci_gate.observed_checks("45")
    assert observed == {"audit": ci_gate.FAILED}


# --- The regression to protect --------------------------------------------

def test_all_required_reported_and_passed_is_the_only_green():
    """PR `#45` did eventually pass all three. A gate that cannot say yes is as
    useless as one that cannot say no."""
    observed = dict.fromkeys(REQUIRED, ci_gate.PASSED)
    buckets = ci_gate.evaluate(REQUIRED, observed)
    assert not buckets[ci_gate.FAILED] and not buckets[ci_gate.PENDING]
    assert len(buckets[ci_gate.PASSED]) == 3


# --- The verdict itself, driven through main() -----------------------------
#
# Everything above this line tests a helper. The Tester gate rejected round 1
# because `main()` — the only thing that issues an exit code — was executed by
# no test at all, so the verdict line could be mutated back to the PR `#45`
# defect with the whole suite still green. These tests assert exit codes.

def test_a_pending_required_check_blocks_the_merge(monkeypatch, capsys):
    """`D1`. The literal PR `#45` state: `audit` green, the other two required
    checks never registered. Mutating `main`'s verdict line to
    `if buckets[FAILED]:` makes this test fail, which is the property round 1
    did not have."""
    code, out, err = drive(monkeypatch, capsys, {
        **HEALTHY, "statusCheckRollup": rollup(check_run("audit", "SUCCESS"))})
    assert code == 2
    assert "have not reported" in err
    assert "may now be issued" not in out


def test_a_failed_required_check_blocks_the_merge(monkeypatch, capsys):
    """The other half of the same verdict line, so neither disjunct can be
    dropped without a test going red."""
    code, out, err = drive(monkeypatch, capsys, {
        **HEALTHY, "statusCheckRollup": rollup(
            *[check_run(n, "SUCCESS") for n in ["audit", "CodeQL"]],
            check_run("Analyze (python)", "FAILURE"))})
    assert code == 2
    assert "did not pass" in err and "Analyze (python)" in err
    assert "may now be issued" not in out


def test_all_required_passing_is_the_only_exit_zero(monkeypatch, capsys):
    """The regression to protect. A gate that cannot say yes is as useless as
    one that cannot say no."""
    code, out, _ = drive(monkeypatch, capsys, {
        **HEALTHY, "statusCheckRollup": rollup(
            *[check_run(n, "SUCCESS") for n in sorted(REQUIRED)])})
    assert code == 0
    assert "All 3 required check(s) reported and passed" in out


def test_a_branch_declaring_no_required_check_blocks_the_merge(monkeypatch, capsys):
    """`D2`. The unit's second headline claim, which the docstring argued for
    three paragraphs and no test asserted. Both sources answer; neither requires
    anything; an unprotected branch is not a verified one."""
    code, out, err = drive(monkeypatch, capsys, {
        **HEALTHY, "protection": (None, ci_gate.NOT_FOUND)})
    assert code == 2
    assert "declares no required status check" in err
    assert "may now be issued" not in out


def test_an_unreadable_source_over_an_empty_one_is_doubt_not_an_empty_set(monkeypatch, capsys):
    """`D3`, and this unit's declared abort criterion.

    The measured configuration of this repository seen by a write-but-not-admin
    token: classic protection answers `FORBIDDEN`, `rules/branches/main` returns
    `[]`, and three checks are genuinely required. Round 1 returned the empty
    union as a verdict and told the operator the branch declared nothing — false,
    permanently closing the merge path, and routing them to `/agents:harden` on
    an already-hardened repository. The gate must block here, but say why.
    """
    code, _, err = drive(monkeypatch, capsys, {
        **HEALTHY, "protection": (None, ci_gate.FORBIDDEN)})
    assert code == 2
    assert "unproven rather than empty" in err
    assert "declares no required status check" not in err, (
        "the gate is again reporting doubt as a finding about the repository"
    )


def test_a_readable_source_with_checks_survives_an_unreadable_one(monkeypatch, capsys):
    """The boundary of `D3`'s fix, in the direction that must NOT block: a
    non-admin token whose ruleset does declare checks can still pass the gate.
    Blocking here would make this a gate no host operator can clear."""
    ruleset = [{"type": "required_status_checks",
                "parameters": {"required_status_checks": [{"context": "audit"}]}}]
    code, out, err = drive(monkeypatch, capsys, {
        **HEALTHY,
        "protection": (None, ci_gate.FORBIDDEN),
        "rules/branches": (ruleset, ""),
        "statusCheckRollup": rollup(check_run("audit", "SUCCESS"))})
    assert code == 0
    assert "may be incomplete" in err
    assert "may now be issued" in out


def test_the_base_is_read_from_the_pull_request_not_defaulted(monkeypatch, capsys):
    """`D5`. `deployment_workflow.md` invokes the gate with no `--base`, so a
    default of `main` gated every pull request against `main`'s requirements —
    green while its own base had a failing check, or permanently closed on any
    host whose default branch is not `main`."""
    calls: list[str] = []

    def recording(args: list[str]) -> tuple[object, str]:
        calls.append(" ".join(args))
        return fake_gh({**HEALTHY,
                        "baseRefName": ({"baseRefName": "develop"}, ""),
                        "statusCheckRollup": rollup(
                            *[check_run(n, "SUCCESS") for n in sorted(REQUIRED)])})(args)

    monkeypatch.setattr(ci_gate, "gh_json", recording)
    monkeypatch.setattr(ci_gate.shutil, "which", lambda _: "/usr/bin/gh")
    monkeypatch.setattr(sys, "argv", ["ci_gate.py", "45", "--no-wait"])
    assert ci_gate.main() == 0
    assert any("branches/develop/protection" in c for c in calls), (
        f"the gate asked about a branch the pull request does not target: {calls}"
    )


def test_base_override_wins_over_the_pull_request(monkeypatch, capsys):
    """`--base` is an override, so it must still work — and must skip the
    lookup entirely, which `fake_gh` proves by raising on an unplanned call."""
    responses = {k: v for k, v in HEALTHY.items() if k != "baseRefName"}
    code, _, _ = drive(monkeypatch, capsys, {
        **responses, "statusCheckRollup": rollup(
            *[check_run(n, "SUCCESS") for n in sorted(REQUIRED)])},
        argv=["45", "--no-wait", "--base", "main"])
    assert code == 0


def test_an_unreadable_check_state_blocks_rather_than_passes(monkeypatch, capsys):
    """`poll` returning None must reach the exit code. A lookup that did not
    answer is not a lookup that answered green.

    **The stderr assertions are what make this test mean its name.** The Tester
    gate showed that mutating `poll` to swallow an unreadable read as `{}` left
    this test passing, because every required check then read as pending and the
    exit code was `2` either way — so the test proved only that something
    blocked, not that the cause was reported. Two states with the same exit code
    and different remedies must be distinguished by the message, or the operator
    is sent to wait for checks that were never read.
    """
    code, out, err = drive(monkeypatch, capsys, {
        **HEALTHY, "statusCheckRollup": (None, "HTTP 503")})
    assert code == 2
    assert "could not be read" in err and "503" in err
    assert "have not reported" not in err, (
        "an unreadable lookup is being reported as checks that have not run"
    )
    assert "may now be issued" not in out


def test_an_unidentifiable_repository_blocks(monkeypatch, capsys):
    """`repo_slug` failing must block. Round 1 never executed this path."""
    code, _, err = drive(monkeypatch, capsys, {
        **HEALTHY, "repo view": (None, "HTTP 403")})
    assert code == 2
    assert "repository could not be identified" in err


def test_an_unreadable_base_blocks_and_names_the_override(monkeypatch, capsys):
    """A pull request whose base cannot be read is not one to merge, and the
    operator is told the flag that resolves it rather than left to find it."""
    code, _, err = drive(monkeypatch, capsys, {
        **HEALTHY, "baseRefName": (None, "HTTP 503")})
    assert code == 2
    assert "could not be read" in err and "--base" in err


def test_gh_absent_blocks(monkeypatch, capsys):
    """An unreadable CI is not a green one."""
    monkeypatch.setattr(ci_gate, "gh_json", fake_gh(HEALTHY))
    monkeypatch.setattr(ci_gate.shutil, "which", lambda _: None)
    monkeypatch.setattr(sys, "argv", ["ci_gate.py", "45", "--no-wait"])
    assert ci_gate.main() == 2
    assert "not installed" in capsys.readouterr().err


# --- gh_json, and the 404 distinction the module docstring rests on ---------

def test_the_two_404s_are_not_the_same_answer(monkeypatch):
    """`D7`. Round 1 declared `NOT_PROTECTED` and `NO_SUCH_BRANCH` as fixtures,
    wrote a comment saying only the message separates them, and then referenced
    neither — so collapsing both to `NOT_FOUND` kept the suite green. Both
    strings are copied from live runs against this repository."""
    monkeypatch.setattr(ci_gate.subprocess, "run", _gh_failing(NOT_PROTECTED))
    assert ci_gate.gh_json(["api", "x"]) == (None, ci_gate.NOT_FOUND)

    monkeypatch.setattr(ci_gate.subprocess, "run", _gh_failing(NO_SUCH_BRANCH))
    payload, error = ci_gate.gh_json(["api", "x"])
    assert payload is None and error != ci_gate.NOT_FOUND
    assert "Branch not found" in error


def test_a_missing_branch_is_not_read_as_requiring_nothing(monkeypatch):
    """The consequence of the distinction above, at the level that matters: a
    typo in `--base` must not pass the gate as an unprotected branch would."""
    monkeypatch.setattr(ci_gate.subprocess, "run", _gh_failing(NO_SUCH_BRANCH))
    names, error = ci_gate.required_from_protection(SLUG, "no-such-branch")
    assert names is None and "Branch not found" in error


def test_a_403_is_never_confused_with_an_answer(monkeypatch):
    """`FORBIDDEN` is the sentinel `D3`'s fix keys on, so it must survive the
    retry loop rather than degrade into a generic message."""
    monkeypatch.setattr(ci_gate.subprocess, "run", _gh_failing("gh: Forbidden (HTTP 403)"))
    assert ci_gate.gh_json(["api", "x"]) == (None, ci_gate.FORBIDDEN)


def test_a_transient_failure_is_retried_and_then_reported(monkeypatch):
    """The retry exists because 2 of 12 live calls returned `HTTP 503` when
    `branch_sovereignty.py` measured it. `ATTEMPTS = 1` must not pass silently."""
    attempts = []

    def failing(argv, **kwargs):
        attempts.append(argv)
        return _completed(1, "", "gh: something went wrong (HTTP 503)")

    monkeypatch.setattr(ci_gate, "BACKOFF_SECONDS", 0)
    monkeypatch.setattr(ci_gate.subprocess, "run", failing)
    payload, error = ci_gate.gh_json(["api", "x"])
    assert payload is None and "503" in error
    assert len(attempts) == ci_gate.ATTEMPTS == 3


def test_a_retry_that_succeeds_returns_the_payload(monkeypatch):
    """The retry must also be able to win, or it is just a slower failure."""
    outcomes = [_completed(1, "", "gh: (HTTP 503)"), _completed(0, '{"ok": true}', "")]
    monkeypatch.setattr(ci_gate, "BACKOFF_SECONDS", 0)
    monkeypatch.setattr(ci_gate.subprocess, "run", lambda *a, **k: outcomes.pop(0))
    assert ci_gate.gh_json(["api", "x"]) == ({"ok": True}, "")


def test_unparseable_output_is_reported_with_its_cause(monkeypatch):
    """`agents.md §1 exception_handling`: the cause is logged, never swallowed."""
    monkeypatch.setattr(ci_gate.subprocess, "run",
                        lambda *a, **k: _completed(0, "not json at all", ""))
    payload, error = ci_gate.gh_json(["api", "x"])
    assert payload is None and "unparseable output" in error


# --- poll ------------------------------------------------------------------

def test_poll_returns_once_the_deadline_passes(monkeypatch):
    """A gate that waits forever is a gate that gets killed and skipped.

    `time.sleep` is neutralised so that removing the deadline check fails on
    `fake_gh`'s call cap in milliseconds instead of stalling the suite for the
    real `POLL_SECONDS` per iteration — the difference between a red test and a
    CI timeout somebody retries.
    """
    monkeypatch.setattr(ci_gate.time, "sleep", lambda _: None)
    monkeypatch.setattr(ci_gate, "gh_json",
                        fake_gh({"statusCheckRollup": rollup(check_run("audit", "SUCCESS"))}))
    buckets = ci_gate.poll("45", REQUIRED, deadline=ci_gate.time.monotonic() - 1)
    assert buckets[ci_gate.PENDING] == ["Analyze (python)", "CodeQL"]


def test_poll_waits_while_a_check_is_still_pending(monkeypatch):
    """And must actually loop, or `--no-wait` is the only behaviour there is."""
    states = [rollup(check_run("audit", "SUCCESS")),
              rollup(check_run("audit", "SUCCESS"), check_run("lint", "SUCCESS"))]
    monkeypatch.setattr(ci_gate, "gh_json", lambda args: states.pop(0))
    monkeypatch.setattr(ci_gate.time, "sleep", lambda _: None)
    buckets = ci_gate.poll("45", {"audit", "lint"}, deadline=ci_gate.time.monotonic() + 60)
    assert not buckets[ci_gate.PENDING] and len(buckets[ci_gate.PASSED]) == 2
    assert states == [], "poll returned without re-reading the check state"


# --- RA-16 -----------------------------------------------------------------

def test_the_gate_declares_its_invoker():
    """`RA-16`: a mechanism nothing calls is a regression. `verify_references.py`
    check (d) enforces this, and this test states the requirement at the source
    so it is visible to whoever edits the docstring."""
    assert "invoked_by: deployment_workflow.md#pr_flow" in ci_gate.__doc__


def test_the_workflow_phase_that_declares_it_actually_names_the_script():
    """The other half of `RA-16`, and the half a docstring cannot assert alone.
    `/agents:harden` shipped in PR `#29` and was never invoked by anything."""
    workflow = (ROOT / "workflows" / "deployment_workflow.md").read_text(encoding="utf-8")
    assert "ci_gate.py" in workflow
    assert "run `gh pr checks [N] --watch`" not in workflow, (
        "deployment_workflow.md still instructs `gh pr checks [N] --watch`, the "
        "gate C10 replaced because it cannot wait for an unregistered check."
    )


def test_the_replaced_command_is_still_named_as_history():
    """Asserting `--watch` is absent from the file would be the wrong test, and
    the first version of this one made that mistake.

    The step deliberately still quotes the command it replaced, because a
    correction that erases what it corrected leaves the next reader free to
    reintroduce it — `reverse_documentation_workflow.md` Phase 5 says to correct
    in place *"saying what it said before"*. So the instruction must be gone and
    the history must remain, which are two different assertions about the same
    string. Pinned because the crude version of this test would pass by deleting
    the paragraph that explains why the gate exists.
    """
    workflow = (ROOT / "workflows" / "deployment_workflow.md").read_text(encoding="utf-8")
    assert "--watch" in workflow and "PR `#45`" in workflow
