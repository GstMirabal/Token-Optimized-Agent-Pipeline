"""Refuse to seal a session while a branch still holds unintegrated work.

`close_workflow.md` pushes `ai-sprint/[ID]` and leaves it unmerged, because
`RA-12` reserves merging for `deployment_workflow.md`. When deployment is not
run, the branch survives — by design, and invisibly. Nothing ever checked.

**Why `git branch --merged` is the wrong instrument here.** `deployment` merges
with `gh pr merge --squash`. A squash merge creates one new commit whose SHA is
not a descendant of the branch, so the branch never appears in
`git branch --merged`, however completely its work landed. Verified on this
repository: `git log --all --merges` after v4.3.0 shows zero merge commits, yet
five pull requests were integrated.

`git cherry` is better but not sufficient either: it compares per-commit
patch-ids, so it recognises a fast-forward, a rebase or a cherry-pick, and
still misses a multi-commit branch collapsed into one. The authoritative signal
for a squash workflow is the pull request state, so that is consulted first and
`git cherry` is the offline fallback. Anything neither can prove is reported,
not assumed — and a false positive is answered with a recorded waiver rather
than by weakening the check.

**That promise used to be broken by this file's own code.** The pull-request
lookup returned a plain bool and mapped any non-zero exit to `False`, so
"I could not find out" became "no merged PR exists". Measured against the live
API: **2 of 12 calls returned `rc=1`, `HTTP 503`**. Since `content_is_integrated`
already returns `False` for every squash-merged branch, one 503 was enough to
flip an *integrated* branch to unintegrated. Two triple-runs of `audit` on an
unchanged tree exited `0,2,0` and `0,0,2`, **accusing a different branch each
time** — the signature of a per-call failure rather than a property of any
branch. The verdict was therefore assumed, not reported, and the operator was
steered toward a permanent waiver for a healthy branch: exactly the "weakening
the check" this docstring warns against, produced by the check itself.

So the lookup is now **three-valued** — `YES` / `NO` / `UNKNOWN` — and `UNKNOWN`
is carried through to the report as its own category. **It still blocks**, and
that is deliberate: a real outage that passed the gate would be a false green,
which is the same defect inverted. What changes is that the report names the
cause. A retry with backoff makes the state rare; the third value makes it
honest.

invoked_by: close_workflow.md#branch_audit (audit), close_workflow.md#local_prune
(prune), deployment_workflow.md#local_prune (prune after merge). Close runs
prune *before* the branch is integrated, so it cannot delete the branch just
published; deployment re-invokes prune after `gh pr merge --squash`.

Usage:
    python3 scripts/branch_sovereignty.py audit
    python3 scripts/branch_sovereignty.py prune

Exit codes:
    0 — nothing unintegrated (audit), or pruning finished
    2 — unintegrated branches remain, or integration could not be determined:
        the session must not be sealed either way (RA-11)
"""

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _root import agents_root  # noqa: E402

# **Mixed scope, deliberately**: every git command below runs against the HOST
# repository in the cwd, while the waiver list is FRAMEWORK data. As a bare
# relative path this was read from wherever the caller stood, so running the
# gate from any other directory found no waivers and said nothing about it —
# a declared exception silently ignored reads exactly like no exception.
WAIVERS = agents_root() / "config" / "abandoned_branches.json"

# Three answers, because two cannot express doubt. The whole finding behind this
# file's second docstring paragraph is that `NO` and `UNKNOWN` were the same value.
YES, NO, UNKNOWN = "yes", "no", "unknown"

# A transient API failure is common enough to be worth retrying and rare enough
# that three attempts collapse it: 2-in-12 per call becomes roughly 1-in-200.
ATTEMPTS = 3
BACKOFF_SECONDS = 1.5

# `gh` exiting non-zero does not always mean the lookup failed — sometimes it
# means there is nothing to look up, and the two must not share a verdict.
# Where no GitHub repository is reachable at all, no merged pull request can
# exist, so the honest answer is NO rather than UNKNOWN. Getting this wrong
# would trade an intermittently-wrong gate for a permanently-closed one: every
# local-only repository, and every test running in a bare temporary repo, would
# refuse its own seal forever.
#
# These strings are empirical — each was produced by running the exact query
# against a repository in that state, not recalled. Deliberately absent:
# `Could not resolve to a Repository`, which means either the repository does
# not exist or the token cannot see it. That is genuinely undetermined, and a
# misconfigured remote should surface rather than read as clean.
NO_GITHUB_SIDE = (
    "no git remotes found",
    "not a git repository",
    "none of the git remotes",
)


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], capture_output=True, text=True)


def base_branch() -> str:
    """The integration branch, `main` unless the repository says otherwise."""
    result = git("symbolic-ref", "--quiet", "--short", "refs/remotes/origin/HEAD")
    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.strip().split("/", 1)[-1]
    return "main"


def current_branch() -> str | None:
    """The checked-out branch, or None on a detached HEAD."""
    result = git("symbolic-ref", "--quiet", "--short", "HEAD")
    return result.stdout.strip() if result.returncode == 0 else None


def local_branches(base: str) -> list[str]:
    """Every local branch except the base and the one currently checked out.

    Deliberately not filtered to `ai-sprint/*`: this repository has never used
    that prefix (`git log --all` records no such reference), and a check scoped
    to a naming convention the repository does not follow reports clean on a
    dirty tree — the failure `revdoc` Phase 4 documents.

    **The checked-out branch is excluded, and that is not a weakening.**
    `close_workflow.md` Phase 5.5 runs this while the sprint branch holds the
    sprint's own commits, and Phase 6 of the same workflow states that branch
    stays unmerged until `deployment_workflow.md` integrates it. Auditing it
    here refused every seal for the branch being sealed — verified on
    `ai-sprint/024`, where `audit` passed until the first commit and then exited
    `2` naming that same branch, advising `/agents:deployment` to integrate what
    Phase 6 says must not be integrated yet. What this check exists to catch is
    stated in its own docstring: branches left behind by *earlier* sprints. The
    branch whose close is executing is the subject of the close, not a leftover.
    """
    result = git("for-each-ref", "--format=%(refname:short)", "refs/heads/")
    skip = {base, current_branch()}
    return [b for b in result.stdout.split() if b not in skip]


def load_waivers() -> dict[str, str]:
    """Branches the human has declared abandoned, with a reason."""
    if not WAIVERS.exists():
        return {}
    data = json.loads(WAIVERS.read_text(encoding="utf-8"))
    return {entry["branch"]: entry["reason"] for entry in data.get("abandoned", [])}


def merged_pr_exists(branch: str) -> str:
    """Whether a merged pull request exists for `branch` — or that it is unknown.

    Authoritative for a squash workflow, and the only signal that recognises one.
    Returns a **three-valued** answer rather than a bool, because the two things
    this used to conflate are not the same fact: "no merged PR exists" is a
    finding about the repository, while "the lookup failed" is a finding about
    the network. Reporting the second as the first is what made this gate
    intermittently accuse healthy branches.

    Args:
        branch: local branch name, used as the pull request's head ref.

    Returns:
        str: `YES`, `NO`, or `UNKNOWN`. `NO` also covers every state in which no
            GitHub repository can be reached at all (see `NO_GITHUB_SIDE`), since
            no pull request can exist there. `UNKNOWN` covers `gh` being absent,
            a request that kept failing, and unparseable output — each logged
            with its cause rather than silently folded into a verdict
            (`agents.md §1 exception_handling`).
    """
    if not shutil.which("gh"):
        print(f"   ℹ️  {branch}: `gh` is not installed, so pull request state "
              f"cannot be read here.", file=sys.stderr)
        return UNKNOWN

    last_error = ""
    for attempt in range(1, ATTEMPTS + 1):
        result = subprocess.run(
            ["gh", "pr", "list", "--state", "merged", "--head", branch, "--json", "number"],
            capture_output=True, text=True,
        )
        if result.returncode == 0:
            try:
                return YES if json.loads(result.stdout or "[]") else NO
            except json.JSONDecodeError:
                last_error = f"unparseable output: {result.stdout.strip()[:120]}"
                break

        stderr = result.stderr.strip()
        # Retrying will not conjure a remote. This is an answer, not a failure.
        if any(marker in stderr for marker in NO_GITHUB_SIDE):
            return NO

        last_error = stderr.splitlines()[0][:120] if stderr else f"exit {result.returncode}"
        if attempt < ATTEMPTS:
            time.sleep(BACKOFF_SECONDS * attempt)

    print(f"   ⚠️  {branch}: pull request state undetermined after {ATTEMPTS} "
          f"attempt(s) — {last_error}", file=sys.stderr)
    return UNKNOWN


def content_is_integrated(branch: str, base: str) -> bool:
    """True when every commit on `branch` has an equivalent in `base`.

    Recognises fast-forward, rebase and cherry-pick. Does NOT recognise a
    multi-commit branch squashed into one — see the module docstring.
    """
    result = git("cherry", base, branch)
    if result.returncode != 0:
        return False
    return not any(line.startswith("+") for line in result.stdout.splitlines())


def classify(base: str) -> tuple[list[str], list[str], list[str], dict[str, str]]:
    """Split local branches into integrated, unintegrated, indeterminate and waived.

    The two signals are asked in cost order: `git cherry` is local and free, so a
    branch it can already prove never reaches the network. Only what it cannot
    prove — every squash-merged branch — costs a pull request lookup.

    **The condition is spelled out rather than chained**, because the previous
    `content_is_integrated(...) or merged_pr_exists(...)` cannot survive a
    three-valued answer: `NO` and `UNKNOWN` are non-empty strings, so both are
    truthy and *every* branch would be reported integrated. A silent inversion of
    this gate is worse than the flakiness it replaces.

    Returns:
        tuple: (integrated, unintegrated, indeterminate, waivers).
    """
    waivers = load_waivers()
    integrated, unintegrated, indeterminate = [], [], []
    for branch in local_branches(base):
        if branch in waivers:
            continue
        if content_is_integrated(branch, base):
            integrated.append(branch)
            continue
        state = merged_pr_exists(branch)
        if state == YES:
            integrated.append(branch)
        elif state == NO:
            unintegrated.append(branch)
        else:
            indeterminate.append(branch)
    return integrated, unintegrated, indeterminate, waivers


def audit(base: str) -> int:
    """Report each branch's integration state; refuse the seal unless all are proven.

    Both failure categories exit `2` (`RA-11`), and they are reported separately
    on purpose. An unintegrated branch is a finding about the repository and has
    a remedy the operator can act on. An indeterminate one is a finding about the
    network and has a different remedy — retry — so offering the waiver there
    would invite disabling the check for a branch that was never at fault.
    """
    integrated, unintegrated, indeterminate, waivers = classify(base)

    for branch, reason in waivers.items():
        print(f"⚪ {branch} — waived: {reason}")
    for branch in integrated:
        print(f"✅ {branch} — work is in {base}")

    if unintegrated:
        print(
            f"\n❌ {len(unintegrated)} branch(es) still hold unintegrated work; "
            f"the session must not be sealed:",
            file=sys.stderr,
        )
        for branch in unintegrated:
            print(f"   • {branch}", file=sys.stderr)
        print(
            f"\n   Run `/agents:deployment` to integrate them — merging is that "
            f"protocol's job, not this one's (RA-12), and it holds the Tester "
            f"signature and the observed-green CI gate (RA-13).\n"
            f"   If a branch is genuinely abandoned, record it in {WAIVERS} "
            f"with a reason; an undeclared exception is how this check gets "
            f"disabled instead of answered.",
            file=sys.stderr,
        )

    if indeterminate:
        print(
            f"\n⚠️  {len(indeterminate)} branch(es) could NOT be determined; "
            f"the seal is refused because unproven is not the same as clean:",
            file=sys.stderr,
        )
        for branch in indeterminate:
            print(f"   • {branch}", file=sys.stderr)
        print(
            f"\n   This is not an accusation. `git cherry` cannot see a squash "
            f"merge, and the pull request lookup did not answer — so nothing "
            f"here says the work is missing, only that it is unproven.\n"
            f"   Re-run this check: the cause is usually transient. Do NOT record "
            f"a waiver for these — a waiver is permanent and would silence a "
            f"branch that may be perfectly integrated.",
            file=sys.stderr,
        )

    if unintegrated or indeterminate:
        return 2

    print("\n✅ No unintegrated branches. Safe to seal.")
    return 0


def origin_has_head(branch: str) -> bool:
    """True when `origin` still holds a head named `branch`.

    `git remote prune origin` only drops stale tracking refs after the remote
    head is already gone. GitHub `delete_branch_on_merge` is an independent
    remote-side setting and is `false` on this nucleus (measured 2026-08-25
    with `gh api repos/:owner/:repo --jq .delete_branch_on_merge`), so a
    squash-merged origin head survives unless something deletes it.
    """
    remotes = git("remote")
    if remotes.returncode != 0 or "origin" not in remotes.stdout.split():
        return False
    result = git("ls-remote", "--heads", "origin", branch)
    if result.returncode != 0:
        cause = (result.stderr.strip() or f"exit {result.returncode}")[:120]
        print(f"   ℹ️  {branch}: origin lookup failed — {cause}", file=sys.stderr)
        return False
    return bool(result.stdout.strip())


def delete_origin_head(branch: str) -> None:
    """Delete `origin/<branch>` when that head still exists."""
    if not origin_has_head(branch):
        return
    result = git("push", "origin", "--delete", branch)
    if result.returncode == 0:
        print(f"🧹 deleted origin/{branch}")
        return
    cause = (result.stderr.strip() or f"exit {result.returncode}")[:120]
    print(f"⚠️  origin/{branch}: {cause}", file=sys.stderr)


def prune(base: str) -> int:
    """Delete only branches whose integration was proven.

    Deletion is irreversible, so `integrated` is the only category acted on.
    Indeterminate branches are left alone and named — the third value costs one
    extra run here, and buys never deleting a branch on the strength of a lookup
    that did not answer.

    Proven-integrated origin heads are deleted first (`git push origin --delete`).
    `git remote prune origin` then drops leftover tracking refs; it cannot
    delete a live origin head, which is why origin survived PRs #51 and #52.
    """
    integrated, unintegrated, indeterminate, _ = classify(base)
    for branch in integrated:
        delete_origin_head(branch)
        result = git("branch", "-D", branch)
        print(f"🧹 deleted {branch}" if result.returncode == 0 else f"⚠️  {branch}: {result.stderr.strip()}")
    git("remote", "prune", "origin")
    if unintegrated:
        print(f"⚠️  Left untouched (not integrated): {', '.join(unintegrated)}")
    if indeterminate:
        print(f"⚠️  Left untouched (integration undetermined, re-run to resolve): "
              f"{', '.join(indeterminate)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("command", choices=["audit", "prune"])
    args = parser.parse_args()
    base = base_branch()
    return audit(base) if args.command == "audit" else prune(base)


if __name__ == "__main__":
    sys.exit(main())
