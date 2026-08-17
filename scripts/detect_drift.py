"""Detect work that happened outside the protocol, before trusting the anchor.

The case: commits were made without `start`, without `close`, or without
either. The recorded state and the repository then disagree, and every workflow
that follows reasons from a false premise.

This is not hypothetical. Five pull requests (#26-#30) were merged after tag
`v4.3.0` with no `CHANGELOG.md` entry, no roadmap phase record, and
`docs/active_state.json` frozen at sprint 017 dated 2026-07-27 while the work
continued to 2026-08-02. Nothing noticed, because nothing could: the anchor
recorded no commit to compare against.

`last_close_commit` — written by `session_state.py release` — is that missing
comparison point.

**A non-empty range is not drift by itself.** `deployment_workflow.md` Phase 4
seals `[Unreleased]` into a released section and tags it, without touching
`last_close_commit`, so commits recorded in the ledger keep landing after the
last close. Reporting those as "outside the protocol" made this check exit `2`
on a healthy repository after every deployment, and a gate with no answer gets
disabled rather than satisfied. The range is therefore split against **sealing
tags** — tags whose version owns a `## [X.Y.Z]` section — and the exit code
follows the action required, not the severity observed. See
`docs/decisions/ADR-0002-drift-verdict-exit-codes.md`.

**Reachability is not per-commit coverage.** That a commit is an ancestor of a
sealing tag proves the range is covered by a published section, never that the
commit has its own ledger entry: PRs #26-#30 ended up ancestors of a tag and
were still unrecorded. The `S` report says so rather than let it be read as
"every commit documented".

**Ordering matters.** This runs BEFORE `state_claim`, never after: claiming the
lock sets `status: IN_PROGRESS`, and a check keyed on the previous status would
read its own side effect. The check is deliberately status-agnostic for the
same reason — it compares commits, not state labels.

invoked_by: start_workflow.md#drift_check.

Usage:
    python3 scripts/detect_drift.py

Exit codes:
    0 — no drift, or every commit in range is covered by a released section
    2 — unrecorded or unprovable work: run /agents:reconcile before Planning
"""

import json
import re
import subprocess
import sys
from pathlib import Path

ACTIVE_STATE = Path("docs/active_state.json")
CHANGELOG = Path("CHANGELOG.md")

SECTION = re.compile(r"^## \[(\d[^\]]*)\]", re.MULTILINE)


def git(*args: str) -> str | None:
    """Run a git command, returning stdout or None when it fails."""
    result = subprocess.run(["git", *args], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else None


def unreleased_is_empty() -> bool:
    """True when the Master Ledger has no entries under [Unreleased].

    Kept from the original check: it remains the correct signal separating
    unrecorded work from work that may be recorded but unprovable. What was
    false was the conclusion drawn from it, not the measurement.
    """
    if not CHANGELOG.exists():
        return False
    text = CHANGELOG.read_text(encoding="utf-8")
    if "## [Unreleased]" not in text:
        return False
    section = text.split("## [Unreleased]", 1)[1].split("\n## ", 1)[0]
    return not any(line.lstrip().startswith(("-", "*")) for line in section.splitlines())


def sealing_tags() -> list[str]:
    """Tags whose version owns a released section in the Master Ledger.

    A tag with no section seals nothing: this repository carries `v3.4.0` and
    `v3.5.2` with no matching entry, and counting them would certify work no
    ledger describes.

    Returns:
        list[str]: tag names, in git's own ordering.
    """
    if not CHANGELOG.exists():
        return []
    versions = set(SECTION.findall(CHANGELOG.read_text(encoding="utf-8")))
    return [t for t in (git("tag") or "").split() if t.lstrip("v") in versions]


def resolve_baseline(recorded: str) -> tuple[str | None, str | None]:
    """Map the recorded baseline onto a commit reachable from HEAD.

    `close_workflow.md` Phase 4 records HEAD while Phase 5 has pushed
    `ai-sprint/[ID]` and never `main`; `deployment_workflow.md` then squash-
    merges, so the recorded commit stops being an ancestor of the base branch.
    `git cat-file -e` cannot see this — the orphaned object still exists — and
    `recorded..HEAD` would then list the entire history since the fork point.

    Args:
        recorded: the SHA stored in `last_close_commit`.

    Returns:
        tuple: (usable baseline or None, substitution note or None).
    """
    if git("cat-file", "-e", f"{recorded}^{{commit}}") is None:
        return None, None
    if git("merge-base", "--is-ancestor", recorded, "HEAD") is not None:
        return recorded, None
    substitute = git("merge-base", recorded, "HEAD")
    if not substitute:
        return None, None
    return substitute, (
        f"Recorded baseline {recorded[:7]} is not an ancestor of HEAD — the "
        f"branch it named was squash-merged or rewritten. Comparing from their "
        f"merge-base {substitute[:7]} instead."
    )


def commits_since(baseline: str, *exclude: str) -> list[str]:
    """One-line log entries reachable from HEAD but not from the exclusions."""
    log = git("log", "--oneline", "HEAD", f"^{baseline}", *exclude) or ""
    return [line for line in log.splitlines() if line]


def classify(baseline: str) -> tuple[str, list[str], list[str], list[str]]:
    """Decide the verdict for the range `baseline..HEAD`.

    Args:
        baseline: a commit reachable from HEAD.

    Returns:
        tuple: (verdict, every commit in range, unsealed commits, sealing tags).
    """
    every = commits_since(baseline)
    if not every:
        return "CLEAN", [], [], []

    tags = sealing_tags()
    if not tags:
        return "R", every, every, []

    unsealed = commits_since(baseline, *(f"^{tag}" for tag in tags))
    if not unsealed:
        return "S", every, [], tags
    if not unreleased_is_empty():
        return "A", every, unsealed, tags
    return ("U" if len(unsealed) == len(every) else "M"), every, unsealed, tags


def enumerate_commits(commits: list[str], stream) -> None:
    """Print at most 20 commits, then say how many were withheld."""
    for line in commits[:20]:
        print(f"   • {line}", file=stream)
    if len(commits) > 20:
        print(f"   … and {len(commits) - 20} more", file=stream)


def report_sealed(every: list[str], tags: list[str]) -> int:
    """Verdict S: the range is covered by a released section. Propose, never block."""
    print(f"✅ {len(every)} commit(s) after the last sealed close, all covered by "
          f"a released ledger section ({', '.join(tags[:3])}).")
    enumerate_commits(every, sys.stdout)
    print("\n   Reachability proves the RANGE is covered, not that each commit has "
          "its own entry — PRs #26-#30 were ancestors of a tag and still unrecorded.")
    print("   The recorded baseline is stale; the next close refreshes it. "
          "Nothing to reconcile.")
    return 0


def report_unverifiable(every: list[str]) -> int:
    """Verdict R: no tag owns a ledger section, so nothing proves the range sealed.

    Exits `2`, not `0`. An earlier design passed here on the grounds that
    nothing could be measured — `test_commits_after_the_sealed_close_are_drift`
    refuted it: a repository with commits after the baseline and no releases at
    all is the Phase 018 scenario in its early form, and passing it would
    whitewash the exact drift this check exists to catch. Unproven coverage is
    not coverage, which is why `A` blocks for the same reason.
    """
    print(f"\n❌ {len(every)} commit(s) landed after the last sealed close, and no "
          f"tag owns a released section in {CHANGELOG} — nothing proves any of "
          f"them recorded:", file=sys.stderr)
    enumerate_commits(every, sys.stderr)
    print("\n   Run `/agents:reconcile` before handing off to Planning. New work "
          "on top of a state that misreports the repository multiplies the "
          "inconsistency instead of resolving it.", file=sys.stderr)
    return 2


def report_drift(verdict: str, every: list[str], unsealed: list[str]) -> int:
    """Verdicts M, U and A: work that is unrecorded or cannot be proven recorded."""
    headline = {
        "U": f"❌ {len(unsealed)} commit(s) landed outside the protocol and no "
             f"released section covers them:",
        "M": f"❌ {len(unsealed)} of {len(every)} commit(s) since the last sealed "
             f"close are covered by no released section:",
        "A": f"❌ {len(unsealed)} of {len(every)} commit(s) are covered by no "
             f"released section, and [Unreleased] is not empty:",
    }[verdict]
    print(f"\n{headline}", file=sys.stderr)
    enumerate_commits(unsealed, sys.stderr)
    if verdict == "A":
        print("\n   They may be recorded there, but reachability cannot prove it "
              "per commit. A human must read the section before this is cleared.",
              file=sys.stderr)
    print("\n   Run `/agents:reconcile` before handing off to Planning. New work "
          "on top of a state that misreports the repository multiplies the "
          "inconsistency instead of resolving it.", file=sys.stderr)
    return 2


def read_baseline() -> str | None:
    """The recorded `last_close_commit`, or None with the reason printed."""
    if not ACTIVE_STATE.exists():
        print("ℹ️  No state anchor yet — first session in this repository.")
        return None
    try:
        state = json.loads(ACTIVE_STATE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print("⚠️  State anchor is not valid JSON; the mirror is authoritative "
              "for crash recovery (start_workflow.md read_anchor).", file=sys.stderr)
        return None
    baseline = state.get("last_close_commit")
    if not baseline:
        # Not an error: the field is written by the first close that runs with
        # it. Saying so is the point — silence here is what let the drift last.
        print("ℹ️  No `last_close_commit` baseline recorded yet. Drift cannot be "
              "measured until the next close writes one.")
    return baseline


def main() -> int:
    """Report a drift verdict for `last_close_commit..HEAD`.

    Returns:
        int: 0 when nothing is required, 2 when reconciliation is.
    """
    recorded = read_baseline()
    if not recorded:
        return 0

    baseline, note = resolve_baseline(recorded)
    if baseline is None:
        print(f"⚠️  Recorded baseline {recorded[:7]} is not in this repository "
              f"(history rewritten, or a different clone). Drift not measured.",
              file=sys.stderr)
        return 0
    if note:
        print(f"⚠️  {note}", file=sys.stderr)

    verdict, every, unsealed, tags = classify(baseline)
    if verdict == "CLEAN":
        print(f"✅ No drift — HEAD matches the last sealed close ({baseline[:7]}).")
        return 0
    if verdict == "S":
        return report_sealed(every, tags)
    if verdict == "R":
        return report_unverifiable(every)
    return report_drift(verdict, every, unsealed)


if __name__ == "__main__":
    sys.exit(main())
