"""Detect work that happened outside the protocol, before trusting the anchor.

**Host-scoped**: the root is the project being worked. The git history, the
anchor and the Master Ledger it compares all belong to the host, so this script
MUST NOT adopt `scripts/_root.py` — anchored to the framework it would report
drift in the wrong repository (Sprint 023 `C0.3`).

There is no root computation in this module at all: `ACTIVE_STATE` and
`CHANGELOG` are cwd-relative and `git()` runs with no `cwd=`, so it inherits the
process working directory. The scope is therefore whatever the caller's cwd is —
the invoker is responsible for setting it to the framework root in nucleus mode
and to the host root in submodule mode, the same `F-BOOT-2` scoping that
`session_start.py` `_anchor_cwd` applies to the anchor-writing sub-scripts. The
roadmap line "checks the framework's git history rather than the host's"
(`021-030-program-queue.md`) describes a caller passing the wrong cwd, not this
module: adopting `agents_root()` here is the defect, not the fix.

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

A routine `docs(state)` anchor write — a commit whose subject starts
`docs(state)` and whose only changed path is `docs/active_state.json` — is
dropped from the range before it is judged (`F-BOOT-4`). `close_workflow.md`
Phase 4 and `deployment_workflow.md` each append one after `last_close_commit`,
and with `[Unreleased]` empty they otherwise read as verdict `U`/`A` and force a
no-op `/agents:reconcile` on every session until the next deployment tags over
them. Both conditions are required: a commit that also touches another file is
still counted whatever its subject says.

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
from typing import TextIO

ACTIVE_STATE = Path("docs/active_state.json")
CHANGELOG = Path("CHANGELOG.md")

SECTION = re.compile(r"^## \[(\d[^\]]*)\]", re.MULTILINE)


def git(*args: str) -> str | None:
    """Run a git command, returning stdout or None when it fails."""
    result = subprocess.run(["git", *args], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else None


def unreleased_section() -> str:
    """The text under ``## [Unreleased]``, or empty when there is none.

    One reader for the section, because two would drift: `unreleased_is_empty`
    asks whether it holds anything and `_cited_in_unreleased` asks what it
    names, and both must agree on where the section ends.
    """
    if not CHANGELOG.exists():
        return ""
    text = CHANGELOG.read_text(encoding="utf-8")
    if "## [Unreleased]" not in text:
        return ""
    return text.split("## [Unreleased]", 1)[1].split("\n## ", 1)[0]


def unreleased_is_empty() -> bool:
    """True when the Master Ledger has no entries under [Unreleased].

    Kept from the original check: it remains the correct signal separating
    unrecorded work from work that may be recorded but unprovable. What was
    false was the conclusion drawn from it, not the measurement.
    """
    if not CHANGELOG.exists() or "## [Unreleased]" not in (
        CHANGELOG.read_text(encoding="utf-8")
    ):
        return False
    section = unreleased_section()
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


_STATE_SUBJECT = re.compile(r"^docs\((?:state|changelog)\)")
_LEDGER_PATHS = frozenset({"docs/active_state.json", "CHANGELOG.md"})


def _routine_state_shas(commits: list[str]) -> set[str]:
    """SHAs in ``commits`` that only maintain the anchor or the ledger.

    ``close_workflow.md`` Phase 4 and ``deployment_workflow.md`` both append a
    commit touching only ``docs/active_state.json`` after ``last_close_commit``.
    With ``[Unreleased]`` empty these read as drift (verdict ``U``/``A``) and
    force a no-op ``/agents:reconcile`` on every session between that close and
    the next deployment's tag (``F-BOOT-4``). They are outside the drift range
    by construction, not by severity — the same principle as
    ``ADR-0002-drift-verdict-exit-codes``.

    Sprint 051 widens this from the anchor alone to the anchor **and** the
    ledger, for a reason that is structural rather than lenient: **a commit
    that writes the ledger cannot appear in the ledger it writes.**
    ``reconciliation_workflow.md`` Phase 3 produces exactly such a commit —
    it adds the missing ``[Unreleased]`` entries — and the reporting host then
    had that commit flagged as uncovered on every subsequent session, by the
    very entry it had just authored.

    Both conditions are still required: a substantive commit mis-subjected
    ``docs(state)`` or ``docs(changelog)`` touches other files and is counted.

    Args:
        commits: ``git log --oneline`` lines for the range under judgement.

    Returns:
        set[str]: the leading short SHA of each line that is a ledger- or
        anchor-maintenance commit.
    """
    routine: set[str] = set()
    for line in commits:
        parts = line.split()
        if not parts:
            continue
        sha = parts[0]
        subject = git("log", "-1", "--format=%s", sha) or ""
        if not _STATE_SUBJECT.match(subject):
            continue
        files = git("diff-tree", "--no-commit-id", "--name-only", "-r", sha) or ""
        changed = {f for f in files.splitlines() if f.strip()}
        if changed and changed <= _LEDGER_PATHS:
            routine.add(sha)
    return routine


def _cited_in_unreleased(commits: list[str]) -> set[str]:
    """SHAs that an entry under ``[Unreleased]`` names outright.

    ``report_drift`` tells the reader that reachability cannot prove coverage
    per commit, and that is true of reachability. It is not true of a ledger
    entry that **cites the commit**: the citation is direct, per-commit
    evidence, and it is the one signal verdict ``A`` was missing.

    Without this, every host sits on verdict ``A`` for every session between
    the moment work lands on the integration branch and the next deployment's
    tag, re-asking a human to read a section they already read. That is the
    desensitisation this check cannot afford, because a reader who has cleared
    the same warning five times clears the sixth without reading.

    The convention it depends on — an ``[Unreleased]`` entry names the commit
    it describes — is stated in ``agents.md §0 Master Ledger``.

    Args:
        commits: ``git log --oneline`` lines still unaccounted for.

    Returns:
        set[str]: the short SHA of each commit its own entry names.
    """
    # Only entry lines count. Scanning the whole section let prose, a URL, a
    # filename or a fenced command clear a commit — worst of all a
    # ``git revert <sha>`` in a code block, where the ledger says the work was
    # undone and the gate read it as recorded (Gate 2). It also disagreed with
    # `unreleased_is_empty`, which has always required a ``-``/``*`` line: two
    # readers of one section differing on what an entry is, which
    # `unreleased_section`'s own docstring exists to prevent.
    entries = "\n".join(
        raw.lstrip()
        for raw in unreleased_section().splitlines()
        if raw.lstrip().startswith(("-", "*"))
    )
    if not entries:
        return set()
    cited: set[str] = set()
    for line in commits:
        if not line.strip():
            continue
        sha = line.split()[0]
        if len(sha) < 7:
            continue
        # The lookbehind refuses a match starting mid-hex — `abc1234` inside
        # `9abc1234` is a different commit (Gate 1, `F-2`) — while the trailing
        # class still accepts the same commit cited at 8, 12 or 40 characters.
        # Case-insensitive because both guards already accept either case, so
        # rejecting `ABC1234` was an asymmetry rather than a decision (Gate 2).
        if re.search(rf"(?<![0-9a-fA-F]){re.escape(sha)}[0-9a-fA-F]*\b",
                     entries, re.IGNORECASE):
            cited.add(sha)
    return cited


def _resolves(ref: str) -> bool:
    """True when ``ref`` names a commit in this repository."""
    return git("rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}") is not None


def integration_refs() -> list[str]:
    """**Every** resolvable ref a sprint might merge into, local and remote.

    Returns a list, not the first match, and the distinction is the whole
    correctness argument. Gate 1 of Sprint 051 rejected the single-ref form as
    `charter`-class: it tried the local branch before ``origin/``, so in a clone
    whose local ``main`` is behind ``origin/main`` — the normal state of a clone
    that has not pulled — a commit that had landed on ``origin/main`` was absent
    from the ref being consulted, got classified **in flight**, and was
    suppressed from the half that blocks. That is the `PRs #26-#30` failure this
    whole script exists to catch, reintroduced by the fix meant to sharpen it.

    Callers therefore treat a commit as in flight only when it is absent from
    **all** of these. Being wrong in that direction over-reports; being wrong in
    the other direction hides drift, and only one of those is recoverable by a
    reader.

    Candidate names: the anchor's own, then ``main``, then ``master``. Not
    hardcoded to ``main``, or a repository naming it otherwise would silently get
    the pre-Sprint-051 behaviour back.

    Returns:
        list[str]: resolvable refs, empty when none resolve or when HEAD is
        itself an integration branch — both meaning every commit in range has
        landed, so there is no in-flight half to separate.
    """
    candidates: list[str] = []
    if ACTIVE_STATE.exists():
        try:
            state = json.loads(ACTIVE_STATE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            state = {}
        named = state.get("integration_branch") or state.get("base_branch")
        if named:
            candidates.append(str(named))
    candidates.extend(["main", "master"])

    head = git("rev-parse", "--abbrev-ref", "HEAD")
    # Every configured remote, not a hardcoded `origin`. Gate 2 found the
    # `charter` hole reopening under a different remote name: the fork workflow
    # `agents.md §4 feedback_upstream` *mandates* leaves the integration branch on
    # `upstream/`, and consulting only `origin/` put work already landed there back
    # into the in-flight half.
    remotes = (git("remote") or "").split()
    refs: list[str] = []
    for name in candidates:
        if name == head:
            return []
        forms = (name, *(f"{remote}/{name}" for remote in remotes))
        refs.extend(form for form in forms if _resolves(form))
    return refs


def _in_flight_shas(commits: list[str]) -> set[str]:
    """SHAs in ``commits`` that have not reached the integration branch.

    ``RA-12`` puts every sprint on ``ai-sprint/[ID]``, so its commits are
    absent from every release tag by construction. ``agents.md §0`` and
    ``RA-05`` place the sprint's ledger entry at **Sprint Closeout**, which
    means a sprint stopped earlier is *correctly* unrecorded — and the
    reconciliation this check would force must then reconstruct nothing, which
    ``reconciliation_workflow.md`` Phase 3 prohibits.

    Separating them keeps the failure this check exists for: ``PRs #26-#30``
    were unrecorded work **on the integration branch**, which stays in the
    blocking half.
    """
    refs = integration_refs()
    if not refs:
        return set()
    # `merge-base --is-ancestor` exits 0 when the sha has landed, and `git()`
    # returns None only on a non-zero exit — the idiom `covering_tags` uses.
    # `all()` is load-bearing: a commit counts as in flight only when **every**
    # integration ref lacks it. Consulting one ref let a stale local branch hide
    # work that had already landed on its remote (Gate 1, `charter`).
    return {
        sha
        for sha in (line.split()[0] for line in commits if line.strip())
        if all(git("merge-base", "--is-ancestor", sha, ref) is None for ref in refs)
    }


def classify(baseline: str) -> tuple[str, list[str], list[str], list[str], list[str]]:
    """Decide the verdict for the range `baseline..HEAD`.

    The verdict is computed over the **landed** half of the range only. The
    in-flight half is returned so the caller can list it, never counted as
    drift (Sprint 051).

    Args:
        baseline: a commit reachable from HEAD.

    Returns:
        tuple: (verdict, landed commits, unsealed commits, sealing tags,
        in-flight commits).
    """
    every = commits_since(baseline)
    routine = _routine_state_shas(every)
    if routine:
        every = [c for c in every if c.split()[0] not in routine]

    in_flight = _in_flight_shas(every)
    in_flight_lines = [c for c in every if c.split()[0] in in_flight]
    if in_flight:
        every = [c for c in every if c.split()[0] not in in_flight]

    if not every:
        return "CLEAN", [], [], [], in_flight_lines

    tags = sealing_tags()
    if not tags:
        return "R", every, every, [], in_flight_lines

    unsealed = [
        c
        for c in commits_since(baseline, *(f"^{tag}" for tag in tags))
        if c.split()[0] not in routine and c.split()[0] not in in_flight
    ]
    cited = _cited_in_unreleased(unsealed)
    if cited:
        unsealed = [c for c in unsealed if c.split()[0] not in cited]
    if not unsealed:
        return ("C" if cited else "S"), every, [], tags, in_flight_lines
    if not unreleased_is_empty():
        return "A", every, unsealed, tags, in_flight_lines
    verdict = "U" if len(unsealed) == len(every) else "M"
    return verdict, every, unsealed, tags, in_flight_lines


def enumerate_commits(commits: list[str], stream: TextIO) -> None:
    """Print at most 20 commits, then say how many were withheld."""
    for line in commits[:20]:
        print(f"   • {line}", file=stream)
    if len(commits) > 20:
        print(f"   … and {len(commits) - 20} more", file=stream)


def covering_tags(every: list[str], tags: list[str]) -> list[str]:
    """Sealing tags that contain at least one commit from the drift range.

    ``sealing_tags()`` returns the full ledger-backed catalogue; listing
    ``tags[:3]`` after a long release history names ancient ``v3.x`` tags that
    do not cover the range (Sprint 039). Prefer tags that actually ancestor
    a commit in ``every``.

    Args:
        every: ``git log --oneline`` lines for ``baseline..HEAD``.
        tags: Candidate sealing tags from ``sealing_tags()``.

    Returns:
        list[str]: Covering tags in catalogue order; empty if none match.
    """
    shas = [line.split()[0] for line in every if line.strip()]
    covering: list[str] = []
    for tag in tags:
        for sha in shas:
            # merge-base --is-ancestor exits 0 when sha is ancestor of tag.
            if git("merge-base", "--is-ancestor", sha, tag) is not None:
                covering.append(tag)
                break
    return covering


def report_sealed(every: list[str], tags: list[str]) -> int:
    """Verdict S: the range is covered by a released section. Propose, never block."""
    named = covering_tags(every, tags) or tags[:3]
    print(f"✅ {len(every)} commit(s) after the last sealed close, all covered by "
          f"a released ledger section ({', '.join(named[:5])}).")
    enumerate_commits(every, sys.stdout)
    print("\n   Reachability proves the RANGE is covered, not that each commit has "
          "its own entry — PRs #26-#30 were ancestors of a tag and still unrecorded.")
    print("   The recorded baseline is stale; refresh at deploy "
          "(`session_state.py refresh-baseline`), not at close. "
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


def report_cited(every: list[str]) -> int:
    """Verdict C: nothing is left unaccounted, and a citation closed the gap.

    Distinct from ``S`` on purpose. ``S`` means a release tag reaches the work;
    ``C`` means the ledger names it by commit while it is still unreleased.
    Reporting both as ``S`` would claim a seal that has not happened.
    """
    print(f"✅ {len(every)} landed commit(s) since the last sealed close are "
          f"accounted for: by a released section, or by an entry under "
          f"[Unreleased] that names the commit.")
    enumerate_commits(every, sys.stdout)
    print("\n   A citing entry is per-commit evidence, which reachability alone "
          "cannot give. The next deployment seals these into a released section.")
    return 0


def report_in_flight(commits: list[str]) -> None:
    """List sprint work that has not merged. Informational — never blocks.

    Printed for every verdict, including ``CLEAN``, so the half that is
    deliberately not counted stays visible. A branch that never merges must
    not become a blind spot just because it stopped blocking.
    """
    print(f"ℹ️  {len(commits)} commit(s) on this branch have not reached the "
          f"integration branch. Their ledger entry is due at Sprint Closeout "
          f"(RA-05), so they are listed here and not counted as drift:")
    enumerate_commits(commits, sys.stdout)


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

    verdict, every, unsealed, tags, in_flight = classify(baseline)
    if in_flight:
        report_in_flight(in_flight)
    if verdict == "CLEAN":
        print(f"✅ No drift — HEAD matches the last sealed close ({baseline[:7]}).")
        return 0
    if verdict == "C":
        return report_cited(every)
    if verdict == "S":
        return report_sealed(every, tags)
    if verdict == "R":
        return report_unverifiable(every)
    return report_drift(verdict, every, unsealed)


if __name__ == "__main__":
    sys.exit(main())
