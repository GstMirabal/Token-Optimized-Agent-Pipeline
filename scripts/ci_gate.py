"""Prove every required CI check reported and passed, before a merge is issued.

`deployment_workflow.md` Phase 1 names this the `RA-13` gate. Its verdict is
observed as a separate invocation and only then is `gh pr merge` issued, so this
script merges nothing and holds no credentials for merging. Chaining a wait and
a merge in one command is what let a red CI reach `main` in Sprint `#081`.

**What it replaces, and why that had to go.** The step used to name
`gh pr checks [N] --watch`. That command waits for the checks it can *see*, and
a check GitHub has not registered yet is not one of them. Measured on pull
request `#45` of this repository: created at `16:12:37`; `--watch` terminated at
roughly `16:13` having observed only `audit`; `Analyze (python)` completed at
`16:16:21` and `CodeQL` at `16:15:49`, three and a half minutes later. Two of
the three required checks had not reported when the gate returned. What actually
blocked that merge was GitHub branch protection — **not the framework's gate** —
and `/agents:harden` is optional and runs once, so on a host without it the
merge would have gone through unverified.

**`mergeStateStatus` is not the fix either.** It returns `CLEAN` also when no
check is required, so an unprotected repository reads green from its first
second. That is precisely the host case this gate exists for.

So the question is inverted. Instead of *"have the checks I can see finished?"*
this asks *"what does the base branch require, and did each of those report and
pass?"* A required check with no run registered is `PENDING` — a state
`--watch` had no way to represent, because it enumerates what exists.

**No required check declared is a failure, not a pass.** An unprotected
repository is not a verified one. Reporting it green is the same defect this
sprint's `C9` repaired in the other direction: `C9` answered red when it did not
know, this one answered green. Neither corrupts data; both make a gate lie.

## The two sources are not interchangeable — measured, not assumed

GitHub can express a required check as classic branch protection or as a
ruleset, and the endpoints do not mirror each other. On this repository, with
three checks required:

| Query | Answer |
| :--- | :--- |
| `repos/{slug}/branches/main/protection/required_status_checks` | `audit`, `Analyze (python)`, `CodeQL` |
| `repos/{slug}/rules/branches/main` | `[]` |

So the rules endpoint does **not** surface classic protection, and either source
read alone is wrong in an opposite direction: the rules endpoint would report
this protected repository as declaring nothing, and the protection endpoint
needs admin, which most host tokens lack. Both are queried and unioned, and the
gate reports doubt only when neither answered.

`Branch not protected` and `Branch not found` both arrive as **HTTP 404** and
only the message separates them. The first is an answer — classic protection
requires nothing here. The second is not: the branch does not exist, and
treating it as "requires nothing" would pass a gate against a typo.

invoked_by: deployment_workflow.md#pr_flow.

The branch whose requirements apply is read from the pull request itself, never
defaulted. `--base` exists to override that, not to supply it.

Usage:
    python3 scripts/ci_gate.py 47
    python3 scripts/ci_gate.py 47 --timeout 600
    python3 scripts/ci_gate.py 47 --no-wait
    python3 scripts/ci_gate.py 47 --base release/2.0

Exit codes:
    0 — every required check reported and passed; the merge may be issued
    2 — a required check failed, is still pending, none is declared, or the
        state could not be determined. The merge must not be issued in any of
        those cases (RA-11)
"""

import argparse
import json
import shutil
import subprocess
import sys
import time
from typing import Any

# Host-scoped, by the classification `scripts/_root.py` declares: every query
# below addresses the repository in the current working directory and none reads
# framework data. Adopting `agents_root()` would make this gate the framework's
# own CI while a host was being deployed — the larger defect that module warns
# against.

# A required check is in exactly one of these. `PENDING` is not a softer
# `FAILED`: it has a different remedy (wait) and a different meaning (the check
# will report), and collapsing the two is what made `--watch` unusable here.
PASSED, FAILED, PENDING = "passed", "failed", "pending"

# Same retry doctrine as `branch_sovereignty.py`, and for the same measured
# reason: 2 of 12 live API calls returned `HTTP 503` there. Three attempts turn
# a 2-in-12 per-call failure into roughly 1-in-200.
ATTEMPTS = 3
BACKOFF_SECONDS = 1.5

# PR `#45` registered its last required check 3m44s after creation. A deadline
# near that reproduces the defect this gate replaces, so the default sits an
# order of magnitude above the measurement rather than just above it.
DEFAULT_TIMEOUT_SECONDS = 1800
POLL_SECONDS = 15

# A check run reports `status`, then `conclusion`. `NEUTRAL` and `SKIPPED` count
# as reported-and-passed deliberately: a required check that skips has answered,
# and failing it would block every conditionally-run workflow. `CANCELLED`,
# `TIMED_OUT`, `ACTION_REQUIRED`, `STALE` and `FAILURE` are absent on purpose —
# each means the check did not pass, and admitting any of them is the false
# green this file exists to remove.
PASSING_CONCLUSIONS = {"SUCCESS", "NEUTRAL", "SKIPPED"}

# The older commit-status shape, which reports a single `state` and no
# conclusion. Third-party integrations still publish these.
PASSING_STATES = {"SUCCESS"}

# `EXPECTED` is a required status GitHub knows about and has not received — the
# same situation as an unregistered check run, and the state this whole gate was
# built to stop reading as satisfied. `ERROR` and `FAILURE` are not here.
PENDING_STATES = {"PENDING", "EXPECTED"}

# What a run reports for `startedAt` before it has started. Neither form can be
# compared against a real timestamp — both sort below every genuine one — so
# `_reduce_runs` normalises them to one value rather than ordering them.
#
# **Both forms are schema-permitted; neither is observed here.** `startedAt` is
# nullable on `CheckRun`, and the zero date is GitHub's rendering of the same
# state. Measured across 12 pull requests of this repository: 0 of 51 rollup
# entries carry an unorderable `startedAt`, and 0 are `StatusContext`. Stated
# this way because the previous comment claimed both "arrive in practice",
# which was an unmeasured claim written as a measured one.
UNORDERABLE = {"", "0001-01-01T00:00:00Z"}

# Sentinels distinguishing "the API answered" from "the API did not".
NOT_FOUND = "not-found"
FORBIDDEN = "forbidden"

# Both are HTTP 404; only this message means "protected by nothing", which is an
# answer. Any other 404 from that endpoint is not.
NO_CLASSIC_PROTECTION = "Branch not protected"


def gh_json(args: list[str]) -> tuple[Any, str]:
    """Run a `gh` command expected to emit JSON, retrying transient failures.

    Args:
        args: `gh` arguments, without the leading executable name.

    Returns:
        tuple: `(payload, "")` when the call answered. `(None, reason)` when it
            did not, where `reason` is `NOT_FOUND`, `FORBIDDEN`, or a one-line
            message. The reason is never discarded — `agents.md §1
            exception_handling` forbids swallowing it, and a verdict with no
            stated cause is the defect this whole sprint exists to remove.
    """
    last_error = ""
    for attempt in range(1, ATTEMPTS + 1):
        result = subprocess.run(["gh", *args], capture_output=True, text=True, check=False)
        if result.returncode == 0:
            try:
                return json.loads(result.stdout or "null"), ""
            except json.JSONDecodeError:
                return None, f"unparseable output: {result.stdout.strip()[:120]}"

        stderr = result.stderr.strip()
        if "HTTP 404" in stderr:
            return None, NOT_FOUND if NO_CLASSIC_PROTECTION in stderr else stderr[:160]
        if "HTTP 403" in stderr:
            return None, FORBIDDEN

        last_error = stderr.splitlines()[0][:160] if stderr else f"exit {result.returncode}"
        if attempt < ATTEMPTS:
            time.sleep(BACKOFF_SECONDS * attempt)
    return None, last_error


def repo_slug() -> tuple[str, str]:
    """The `owner/name` of the repository in the current working directory.

    Returns:
        tuple: `(slug, "")`, or `("", reason)` when it could not be read.
    """
    payload, error = gh_json(["repo", "view", "--json", "nameWithOwner"])
    if error:
        return "", error
    slug = (payload or {}).get("nameWithOwner", "")
    return (slug, "") if slug else ("", "`gh repo view` returned no repository name")


def pr_base(pr: str) -> tuple[str, str]:
    """The branch `pr` actually targets.

    Args:
        pr: pull request number, as a string.

    Returns:
        tuple: `(branch, "")`, or `("", reason)` when it could not be read.

    **Read rather than assumed, and `--base` is only an override.** This
    defaulted to `main` while `deployment_workflow.md` invokes the gate with no
    `--base` at all, so a pull request targeting any other branch was gated
    against `main`'s requirements: green while its own base had a failing
    required check, or permanently closed on every host whose default branch is
    `master`. The base is a property of the pull request, and guessing it is
    the same error as guessing the checks.
    """
    payload, error = gh_json(["pr", "view", pr, "--json", "baseRefName"])
    if error:
        return "", error
    branch = (payload or {}).get("baseRefName", "")
    return (branch, "") if branch else ("", f"#{pr} reports no base branch")


def required_from_protection(slug: str, base: str) -> tuple[set[str] | None, str]:
    """Required check names declared by classic branch protection.

    Args:
        slug: `owner/name` of the repository.
        base: the branch a merge would target.

    Returns:
        tuple: `(names, "")` when the endpoint answered — an empty set means
            classic protection requires nothing, which is a finding. `(None,
            reason)` when it did not, which is a different finding: `FORBIDDEN`
            is the common case, since this endpoint needs admin.
    """
    payload, error = gh_json(
        ["api", f"repos/{slug}/branches/{base}/protection/required_status_checks"]
    )
    if error == NOT_FOUND:
        return set(), ""
    if error:
        return None, error

    payload = payload or {}
    from_checks = {c["context"] for c in payload.get("checks", []) if c.get("context")}
    return from_checks | set(payload.get("contexts", [])), ""


def required_from_rulesets(slug: str, base: str) -> tuple[set[str] | None, str]:
    """Required check names declared by repository rulesets.

    Queried in addition to classic protection, never instead of it: measured on
    this repository, this endpoint returns `[]` while three checks are required
    through classic protection. It is read because it is the only source a
    non-admin token can see, and because a ruleset is the form GitHub now steers
    repositories toward.

    Args:
        slug: `owner/name` of the repository.
        base: the branch a merge would target.

    Returns:
        tuple: `(names, "")` when the endpoint answered, `(None, reason)`
            otherwise.
    """
    payload, error = gh_json(["api", f"repos/{slug}/rules/branches/{base}"])
    if error == NOT_FOUND:
        return set(), ""
    if error:
        return None, error

    names: set[str] = set()
    for rule in payload or []:
        if rule.get("type") != "required_status_checks":
            continue
        declared = (rule.get("parameters") or {}).get("required_status_checks", [])
        names |= {c["context"] for c in declared if c.get("context")}
    return names, ""


def required_checks(slug: str, base: str) -> tuple[set[str] | None, str]:
    """Every check `base` requires, from both places GitHub can express one.

    The union, not the first source that answers. A repository may carry classic
    protection and a ruleset at once, and a check required by only one of them is
    still required; taking whichever replied first would silently drop the other
    half.

    Args:
        slug: `owner/name` of the repository.
        base: the branch a merge would target.

    Returns:
        tuple: `(names, "")` when the answer is trustworthy. `(None, reason)`
            when it is not — the states where this gate must say it does not
            know instead of guessing. A non-empty set is returned even if one
            source was unreadable; an EMPTY one never is unless both sources
            answered.
    """
    protection, protection_error = required_from_protection(slug, base)
    rulesets, ruleset_error = required_from_rulesets(slug, base)

    if protection is None and rulesets is None:
        return None, f"branch protection: {protection_error}; rulesets: {ruleset_error}"

    known = (protection or set()) | (rulesets or set())
    if protection is not None and rulesets is not None:
        return known, ""

    unreadable = "branch protection" if protection is None else "rulesets"
    return _from_one_source(known, unreadable, protection_error or ruleset_error)


def _from_one_source(known: set[str], unreadable: str,
                     reason: str) -> tuple[set[str] | None, str]:
    """Decide what a half-readable answer is worth.

    Args:
        known: check names the readable source declared, possibly empty.
        unreadable: which source did not answer, named for the operator.
        reason: why it did not answer.

    Returns:
        tuple: `(names, "")` when the readable half is worth verifying, or
            `(None, reason)` when it proves nothing.

    **An unreadable source plus an empty readable one proves nothing**, and
    returning `set()` here was this unit's own instance of the defect it was
    written to remove: doubt collapsed into a verdict. Measured on this
    repository with a non-admin token — classic protection answers `FORBIDDEN`
    and `rules/branches/main` returns `[]` while three checks are genuinely
    required. The empty union was then reported as "this branch declares no
    required status check", which is false, permanently closes the merge path,
    and routes the operator to `/agents:harden` on an already-hardened
    repository. Found by the Tester gate, not by this file's author.

    A non-empty readable source is a different matter: those checks are known to
    be required and can be verified, even though the set may be incomplete.
    Blocking there too would make this a gate no non-admin operator can pass,
    and a gate nobody can pass is a gate that gets removed.
    """
    if not known:
        return None, (f"{unreadable} could not be read ({reason}) and the other "
                      f"source declares nothing, so what this branch requires is "
                      f"unproven rather than empty")

    print(f"⚠️  {unreadable} could not be read ({reason}); the {len(known)} "
          f"required check(s) below are verified, but the set may be incomplete.",
          file=sys.stderr)
    return known, ""


def _state_of(entry: dict[str, Any]) -> tuple[str, str, str]:
    """Reduce one rollup entry to a name, a state and the moment it started.

    Two shapes arrive here. A `CheckRun` carries `name`, `status` and — once
    complete — `conclusion`. A `StatusContext` carries `context` and a single
    `state`, with no separate notion of "running".

    **Dispatched on `__typename`, not on which keys are present.** The obvious
    shape test — *"does it have a `conclusion`?"* — is wrong in a way that would
    have closed this gate permanently: `gh` emits the union of both shapes, so a
    `StatusContext` can arrive carrying `"conclusion": null` alongside its real
    `state`. Read by shape, that entry takes the `CheckRun` branch, finds no
    `status`, and reports `PENDING` forever — a passing third-party status that
    can never clear. That is this unit's declared abort criterion, reached by
    reasoning rather than by an outage, so the dispatch is keyed on the field
    GitHub provides for exactly this purpose. The shape test survives only as a
    fallback for data that carries no `__typename`.

    Args:
        entry: one element of `statusCheckRollup`.

    Returns:
        tuple: `(name, state, started_at)`. `state` is `PASSED`, `FAILED` or
            `PENDING`; `started_at` is `""` when the shape does not report one.
    """
    name = entry.get("name") or entry.get("context") or ""
    started_at = entry.get("startedAt") or entry.get("createdAt") or ""
    typename = entry.get("__typename", "")

    if typename == "CheckRun" or (not typename and "state" not in entry):
        if (entry.get("status") or "").upper() != "COMPLETED":
            return name, PENDING, started_at
        conclusion = (entry.get("conclusion") or "").upper()
        return name, PASSED if conclusion in PASSING_CONCLUSIONS else FAILED, started_at

    state = (entry.get("state") or "").upper()
    if state in PASSING_STATES:
        return name, PASSED, started_at
    return name, PENDING if state in PENDING_STATES else FAILED, started_at


def observed_checks(pr: str) -> tuple[dict[str, str] | None, str]:
    """The state of every check GitHub has registered against `pr`.

    Args:
        pr: pull request number, as a string.

    Returns:
        tuple: `(states, "")` mapping check name to `PASSED`/`FAILED`/`PENDING`,
            or `(None, reason)` when the lookup did not answer.

    A name can appear more than once — PR `#45` carries two `audit` entries from
    two pushes — so every run of a name is collected and reduced by
    `_reduce_runs`. Keeping only the first would judge a branch by a superseded
    run.
    """
    payload, error = gh_json(["pr", "view", pr, "--json", "statusCheckRollup"])
    if error:
        return None, error

    runs: dict[str, list[tuple[str, str]]] = {}
    for entry in (payload or {}).get("statusCheckRollup") or []:
        name, state, started_at = _state_of(entry)
        if name:
            runs.setdefault(name, []).append((started_at, state))
    return {name: _reduce_runs(states) for name, states in runs.items()}, ""


def _reduce_runs(runs: list[tuple[str, str]]) -> str:
    """Collapse every run of one check name into the state that governs it.

    Args:
        runs: `(started_at, state)` for each run GitHub reports under that name.

    Returns:
        str: `PASSED`, `FAILED` or `PENDING`.

    **An unorderable pending run pins the check; otherwise the newest group
    decides.** `CheckRun.startedAt` is null until a run starts, and GitHub also
    spells that `0001-01-01T00:00:00Z`; both sort below every real timestamp, so
    a plain newest-wins rule discards a queued re-run in favour of the
    superseded pass it replaces. Push a fix commit, gate the pull request before
    the new run starts, and the old green verdict is reported as current.

    **Declared limit: this rule cannot distinguish a queued re-run from a stale
    queued entry, and does not try.** Both present the same rollup data — an
    unorderable pending run beside a newer completed pass — so a check whose
    earlier `QUEUED` entry lingers after a later run has passed stays pending
    here even though GitHub's own protection is satisfied. That is a real
    false red and it is **open**, not solved: separating the two cases needs a
    signal `statusCheckRollup` does not carry. It is recorded rather than
    hidden because the alternative rules are worse — newest-wins is the false
    green above, and the version of this function that claimed to fix both was
    shipped with a test whose fixture gave a `QUEUED` run a real `startedAt`,
    contradicting the premise stated in this very paragraph. The Tester gate
    found that, having also written the recommendation it disproved.

    Unorderable timestamps are normalised to one value before comparison rather
    than filtered out. Filtering was redundant with the guard that followed it —
    `""` already sorts below every real timestamp — and no test could tell the
    filter's contribution from the guard's, so a mutant deleting it survived.
    Normalising also fixes the case both forms of "not started" appear at once,
    where filtering ranked `0001-01-01T00:00:00Z` above `""` and dropped runs it
    should have weighed.

    On equal timestamps `FAILED` wins over `PASSED`: ties resolve toward
    blocking, because the cost of the two errors is not symmetric.
    """
    if any(started_at in UNORDERABLE and state == PENDING for started_at, state in runs):
        return PENDING
    ordered = [("" if at in UNORDERABLE else at, state) for at, state in runs]
    newest = max(at for at, _ in ordered)
    states = {state for at, state in ordered if at == newest}
    if PENDING in states:
        return PENDING
    return FAILED if FAILED in states else PASSED


def evaluate(required: set[str], observed: dict[str, str]) -> dict[str, list[str]]:
    """Sort the required checks into passed, failed and pending.

    Args:
        required: check names the base branch requires.
        observed: check name to state, from `observed_checks`.

    Returns:
        dict: keys `PASSED`, `FAILED`, `PENDING`, each a sorted list of names.

    A required check absent from `observed` is `PENDING`, never satisfied. That
    single line is the defect: `--watch` enumerated what existed, so a check not
    yet registered was not waited for at all.
    """
    buckets: dict[str, list[str]] = {PASSED: [], FAILED: [], PENDING: []}
    for name in sorted(required):
        buckets[observed.get(name, PENDING)].append(name)
    return buckets


def report(buckets: dict[str, list[str]], pr: str) -> None:
    """Print the verdict for each required check, passing ones included.

    Args:
        buckets: the output of `evaluate`.
        pr: pull request number, for the failure message.
    """
    for name in buckets[PASSED]:
        print(f"✅ {name} — reported and passed")

    if buckets[FAILED]:
        print(f"\n❌ {len(buckets[FAILED])} required check(s) did not pass; "
              f"the merge must not be issued:", file=sys.stderr)
        for name in buckets[FAILED]:
            print(f"   • {name}", file=sys.stderr)

    if buckets[PENDING]:
        print(f"\n⏳ {len(buckets[PENDING])} required check(s) have not reported; "
              f"unproven is not the same as passed:", file=sys.stderr)
        for name in buckets[PENDING]:
            print(f"   • {name}", file=sys.stderr)
        print(f"\n   A required check with no run registered is normal for the "
              f"first minutes of a pull request — on PR #45 the last one "
              f"appeared 3m44s after creation. Re-run this gate, or raise "
              f"`--timeout`.\n   Inspect them at: gh pr checks {pr}",
              file=sys.stderr)


def poll(pr: str, required: set[str], deadline: float) -> dict[str, list[str]] | None:
    """Re-read the checks until none is pending or `deadline` passes.

    Args:
        pr: pull request number, as a string.
        required: check names the base branch requires.
        deadline: monotonic clock value after which to stop waiting.

    Returns:
        dict: the final buckets, or None when the lookup stopped answering —
            which is reported as doubt rather than resolved into a verdict.
    """
    while True:
        observed, error = observed_checks(pr)
        if observed is None:
            print(f"⚠️  Check state for #{pr} could not be read: {error}", file=sys.stderr)
            return None

        buckets = evaluate(required, observed)
        if not buckets[PENDING] or time.monotonic() >= deadline:
            return buckets

        waiting = ", ".join(buckets[PENDING])
        remaining = int(deadline - time.monotonic())
        print(f"⏳ waiting on {waiting} ({remaining}s left)", flush=True)
        time.sleep(POLL_SECONDS)


def resolve_inputs(args: argparse.Namespace) -> set[str] | int:
    """Read the repository, the branch the pull request targets, and its checks.

    Args:
        args: parsed command line, supplying `pr` and an optional `base`.

    Returns:
        set: the required check names, or an exit code when any of the three
            lookups did not answer. Every failure path here returns `2`: an
            input this gate could not read is not an input it may pass.
    """
    slug, error = repo_slug()
    if error:
        print(f"❌ The repository could not be identified: {error}", file=sys.stderr)
        return 2

    base = args.base
    if not base:
        base, error = pr_base(args.pr)
        if error:
            print(f"❌ The branch #{args.pr} targets could not be read: {error}. "
                  f"Pass `--base` to state it.", file=sys.stderr)
            return 2

    required, error = required_checks(slug, base)
    if required is None:
        print(f"❌ What `{base}` requires could not be determined, so nothing "
              f"here proves the checks passed — {error}\n"
              f"   This is not an accusation about the pull request. Re-run the "
              f"gate, or use a token that can read branch protection.",
              file=sys.stderr)
        return 2

    if not required:
        print(f"❌ `{base}` declares no required status check, in branch "
              f"protection or in a ruleset. An unprotected branch is not a "
              f"verified one, and reporting it green is the false pass this "
              f"gate exists to prevent.\n"
              f"   Run `/agents:harden` to declare them "
              f"(repository_hardening_workflow.md Phase 8).", file=sys.stderr)
        return 2

    print(f"🔒 {base} requires {len(required)}: {', '.join(sorted(required))}")
    return required


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("pr", help="pull request number to gate")
    parser.add_argument("--base", default="",
                        help="override the branch the pull request targets; "
                             "read from the pull request itself when omitted")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS,
                        help="seconds to wait for required checks to report")
    parser.add_argument("--no-wait", action="store_true",
                        help="report the current state without waiting")
    args = parser.parse_args()

    if not shutil.which("gh"):
        print("❌ `gh` is not installed, so no check state can be read. This gate "
              "reports that rather than passing: an unreadable CI is not a green "
              "one.", file=sys.stderr)
        return 2

    required = resolve_inputs(args)
    if isinstance(required, int):
        return required

    deadline = time.monotonic() + (0 if args.no_wait else args.timeout)
    buckets = poll(args.pr, required, deadline)
    if buckets is None:
        return 2

    report(buckets, args.pr)
    if buckets[FAILED] or buckets[PENDING]:
        return 2

    print(f"\n✅ All {len(required)} required check(s) reported and passed. "
          f"The merge may now be issued as a separate command (RA-13).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
