"""Report chains of `fix(` commits that correct each other inside a range (A-1).

A `fix(` commit (subject starting `fix(` or `fix:`) is a link when a line it
removes or modifies was introduced by another `fix(` commit of the same range.
Links form chains: fix A <- fix B <- fix C is one chain. Attribution is
`git blame --porcelain` on the commit's first parent over the removed line
ranges of `git diff -U0 --no-renames`; a hunk with no removed lines (a pure
addition) has nothing to blame and is skipped, as are root commits. Only
commits inside the range count: a correction of a line from a `fix(` outside it
is not a link. A deleted or renamed file is blamed at its old path in the
parent, so neither crashes the scan.

The count of chains is the signal, not the commit count: one chain is a normal
remediation, a second chain means remediation is not converging
(`rules/qa_and_testing.md §4`).

invoked_by: hooks/on_commit.py (warning on each `fix(` commit, exit 0) and QA
Gate 1 second check (workflows/pipeline_workflow.md Phase 7, agents/qa_agent.md).

Usage:
    python3 scripts/check_remediation_chain.py --range <base>..HEAD

Exit codes:
    0 - zero or one chain
    2 - two or more chains (the A-1 stop), or any git/range failure
        (fail closed on error)
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys

FIX_RE = re.compile(r"^fix(\([^)]*\))?!?:|^fix\(")
HUNK_RE = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+")
BLAME_RE = re.compile(r"^([0-9a-f]{40}) \d+ \d+")
OLD_PATH_RE = re.compile(r"^--- a/(.+)$")


def _git(*args: str) -> str:
    """Run git and return stdout.

    Args:
        *args: Arguments after `git`.

    Returns:
        Standard output text.

    Raises:
        RuntimeError: When git exits non-zero.
    """
    proc = subprocess.run(
        ["git", *args], capture_output=True, text=True, check=False
    )
    if proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {proc.stderr.strip()}")
    return proc.stdout


def range_commits(rng: str) -> list[tuple[str, str, str]]:
    """List the range's single-parent-or-merge commits, oldest first.

    Args:
        rng: A revision range such as `base..HEAD`.

    Returns:
        Tuples of (sha, first parent or empty string, subject).
    """
    out = _git("rev-list", "--reverse", "--parents", "--format=%s", rng)
    commits: list[tuple[str, str, str]] = []
    lines = out.splitlines()
    for i in range(0, len(lines) - 1, 2):
        ids = lines[i].split()[1:]
        sha = ids[0]
        parent = ids[1] if len(ids) > 1 else ""
        commits.append((sha, parent, lines[i + 1]))
    return commits


def removed_ranges(parent: str, sha: str) -> list[tuple[str, int, int]]:
    """Return the old-side line ranges a commit removes or modifies.

    Args:
        parent: Parent commit id.
        sha: The commit id.

    Returns:
        Tuples of (old path, first line, last line), pure additions excluded.
    """
    diff = _git("diff", "-U0", "--no-renames", parent, sha)
    found: list[tuple[str, int, int]] = []
    path = ""
    for line in diff.splitlines():
        old = OLD_PATH_RE.match(line)
        if old:
            path = old.group(1)
            continue
        if line.startswith("--- /dev/null"):
            path = ""
            continue
        span = _removed_span(line)
        if span and path:
            found.append((path, *span))
    return found


def _removed_span(line: str) -> tuple[int, int] | None:
    """Parse a hunk header into its removed old-side span.

    Args:
        line: One diff line.

    Returns:
        (first, last) old-side lines, or None when not a hunk or a pure addition.
    """
    hunk = HUNK_RE.match(line)
    if not hunk:
        return None
    start = int(hunk.group(1))
    count = 1 if hunk.group(2) is None else int(hunk.group(2))
    return (start, start + count - 1) if count > 0 else None


def blamed_commits(parent: str, path: str, first: int, last: int) -> set[str]:
    """Return the commits that introduced the given lines in `parent`.

    Args:
        parent: Commit whose tree is blamed.
        path: Old-side path.
        first: First line, 1-based.
        last: Last line, inclusive.

    Returns:
        Full commit ids.
    """
    out = _git(
        "blame", "--porcelain", "-L", f"{first},{last}", parent, "--", path
    )
    return {m.group(1) for m in map(BLAME_RE.match, out.splitlines()) if m}


def find_links(commits: list[tuple[str, str, str]]) -> list[tuple[str, str]]:
    """Find (earlier fix, later fix) pairs within the range.

    Args:
        commits: Output of `range_commits`.

    Returns:
        Pairs where the later `fix(` corrected lines of the earlier one.
    """
    fixes = {sha for sha, _, subj in commits if FIX_RE.match(subj)}
    links: list[tuple[str, str]] = []
    for sha, parent, _ in commits:
        if sha not in fixes or not parent:
            continue
        sources: set[str] = set()
        for path, first, last in removed_ranges(parent, sha):
            sources |= blamed_commits(parent, path, first, last)
        links.extend((src, sha) for src in sorted(sources & fixes) if src != sha)
    return links


def build_chains(links: list[tuple[str, str]]) -> list[list[str]]:
    """Group linked commits into connected chains.

    Args:
        links: Pairs from `find_links`.

    Returns:
        Each chain as its commit ids, in first-seen order.
    """
    groups: list[list[str]] = []
    for a, b in links:
        hit = [g for g in groups if a in g or b in g]
        merged = [x for g in hit for x in g]
        for g in hit:
            groups.remove(g)
        merged += [x for x in (a, b) if x not in merged]
        groups.append(merged)
    return groups


def main(argv: list[str] | None = None) -> int:
    """Run the check.

    Args:
        argv: Optional argument list.

    Returns:
        Process exit code.
    """
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--range", required=True, dest="rng")
    args = ap.parse_args(argv)
    try:
        commits = range_commits(args.rng)
        chains = build_chains(find_links(commits))
    except RuntimeError as exc:
        print(f"check_remediation_chain: error: {exc}", file=sys.stderr)
        return 2
    subjects = {sha: subj for sha, _, subj in commits}
    order = {sha: i for i, (sha, _, _) in enumerate(commits)}
    for n, chain in enumerate(chains, 1):
        print(f"chain {n}:")
        for sha in sorted(chain, key=order.__getitem__):
            print(f"  {sha[:7]} {subjects[sha]}")
    print(f"chains: {len(chains)}")
    if len(chains) >= 2:
        print("A-1 stop: second remediation chain in the range", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
