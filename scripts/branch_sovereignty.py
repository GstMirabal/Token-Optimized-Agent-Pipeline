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

invoked_by: close_workflow.md#branch_audit (audit), close_workflow.md#local_prune
(prune).

Usage:
    python3 scripts/branch_sovereignty.py audit
    python3 scripts/branch_sovereignty.py prune

Exit codes:
    0 — nothing unintegrated (audit), or pruning finished
    2 — unintegrated branches remain: the session must not be sealed
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

WAIVERS = Path("config/abandoned_branches.json")


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], capture_output=True, text=True)


def base_branch() -> str:
    """The integration branch, `main` unless the repository says otherwise."""
    result = git("symbolic-ref", "--quiet", "--short", "refs/remotes/origin/HEAD")
    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.strip().split("/", 1)[-1]
    return "main"


def local_branches(base: str) -> list[str]:
    """Every local branch except the base itself.

    Deliberately not filtered to `ai-sprint/*`: this repository has never used
    that prefix (`git log --all` records no such reference), and a check scoped
    to a naming convention the repository does not follow reports clean on a
    dirty tree — the failure `revdoc` Phase 4 documents.
    """
    result = git("for-each-ref", "--format=%(refname:short)", "refs/heads/")
    return [b for b in result.stdout.split() if b != base]


def load_waivers() -> dict[str, str]:
    """Branches the human has declared abandoned, with a reason."""
    if not WAIVERS.exists():
        return {}
    data = json.loads(WAIVERS.read_text(encoding="utf-8"))
    return {entry["branch"]: entry["reason"] for entry in data.get("abandoned", [])}


def merged_pr_exists(branch: str) -> bool:
    """Authoritative for a squash workflow; unavailable offline."""
    if not shutil.which("gh"):
        return False
    result = subprocess.run(
        ["gh", "pr", "list", "--state", "merged", "--head", branch, "--json", "number"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return False
    try:
        return bool(json.loads(result.stdout or "[]"))
    except json.JSONDecodeError:
        return False


def content_is_integrated(branch: str, base: str) -> bool:
    """True when every commit on `branch` has an equivalent in `base`.

    Recognises fast-forward, rebase and cherry-pick. Does NOT recognise a
    multi-commit branch squashed into one — see the module docstring.
    """
    result = git("cherry", base, branch)
    if result.returncode != 0:
        return False
    return not any(line.startswith("+") for line in result.stdout.splitlines())


def classify(base: str) -> tuple[list[str], list[str], dict[str, str]]:
    """Split local branches into integrated, unintegrated and waived."""
    waivers = load_waivers()
    integrated, unintegrated = [], []
    for branch in local_branches(base):
        if branch in waivers:
            continue
        if content_is_integrated(branch, base) or merged_pr_exists(branch):
            integrated.append(branch)
        else:
            unintegrated.append(branch)
    return integrated, unintegrated, waivers


def audit(base: str) -> int:
    integrated, unintegrated, waivers = classify(base)

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
        return 2

    print(f"\n✅ No unintegrated branches. Safe to seal.")
    return 0


def prune(base: str) -> int:
    """Delete only branches whose integration was proven."""
    integrated, unintegrated, _ = classify(base)
    for branch in integrated:
        result = git("branch", "-D", branch)
        print(f"🧹 deleted {branch}" if result.returncode == 0 else f"⚠️  {branch}: {result.stderr.strip()}")
    git("remote", "prune", "origin")
    if unintegrated:
        print(f"⚠️  Left untouched (not proven integrated): {', '.join(unintegrated)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("command", choices=["audit", "prune"])
    args = parser.parse_args()
    base = base_branch()
    return audit(base) if args.command == "audit" else prune(base)


if __name__ == "__main__":
    sys.exit(main())
