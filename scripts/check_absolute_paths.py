"""Reject real developer-machine absolute paths in tracked, staged and untracked files (RA-15).

A real home path reaching a public commit leaks the machine's user name and,
usually, a real project name alongside it. This is not hypothetical: a real
host project folder leaked into `skills/skillopt/data/scenarios.json` and was
caught only during the pre-publication audit (agents.md §7, RA-15).

Generic placeholders are allowed; the allow-list below is deliberately small,
and it has already rejected a contribution from this framework's own author — a
home path in a PR #28 test fixture whose user segment was not on the list. That
literal is paraphrased rather than quoted here: quoting it would trip this very
scanner, as an earlier draft of this docstring did.

invoked_by: Makefile `verify` target (and therefore .github/workflows/ci.yml,
which invokes `make verify`). Extracted from a CI-inline heredoc so the same
check can run locally, where the decision to push is made (RA-16).

Usage:
    python3 scripts/check_absolute_paths.py

Exit codes:
    0 — no real-looking developer paths
    1 — violations found, listed on stdout
    2 — git failed; the scan is not trusted (fail-closed)
"""

import re
import subprocess
import sys
from pathlib import Path

ALLOWED_USERS = {"developer", "user", "username", "yourname", "example"}
HOME_PATH = re.compile(r"/(?:Users|home)/([A-Za-z0-9_.-]+)/")
GIT_GREP_PATTERN = r"/Users/[A-Za-z0-9_.-]\+/\|/home/[A-Za-z0-9_.-]\+/"


class GitError(RuntimeError):
    """`git` failed in a way that is not "no match"; the scan cannot be trusted."""


def _grep_listing(*flags: str) -> list[str]:
    """Run `git grep -lIz` with `flags` and return the matching paths.

    Args:
        *flags: extra `git grep` flags selecting the tree to search.

    Returns:
        list[str]: paths containing a home-path-looking string, minus `venv_skillopt/`.

    Raises:
        GitError: git exited with anything other than 0 (match) or 1 (no match).
    """
    result = subprocess.run(
        ["git", "grep", "-lIz", *flags, "-e", GIT_GREP_PATTERN],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode not in (0, 1):
        raise GitError(f"git grep {' '.join(flags)} exited {result.returncode}: {result.stderr.strip()}")
    return [f for f in result.stdout.split("\0") if f and not f.startswith("venv_skillopt/")]


def _index_text(path: str) -> str:
    """Return the staged content of `path`.

    Args:
        path: repository-relative path of an index entry.

    Returns:
        str: the staged blob decoded as UTF-8, undecodable bytes dropped.

    Raises:
        GitError: `git show` could not read the index entry.
    """
    result = subprocess.run(["git", "show", f":{path}"], capture_output=True, check=False)
    if result.returncode != 0:
        raise GitError(f"git show :{path} exited {result.returncode}")
    return result.stdout.decode("utf-8", errors="ignore")


def collect_texts() -> list[tuple[str, str]]:
    """Gather `(label, text)` pairs for every file the check covers.

    Covers the working copy of tracked and untracked non-ignored files, plus
    the staged content of the index (which can differ from the working copy).
    `.gitignore`d files are out of scope.

    Returns:
        list[tuple[str, str]]: label and content per candidate.

    Raises:
        GitError: a git invocation failed.
    """
    texts = []
    for path in _grep_listing("--untracked", "--exclude-standard"):
        try:
            texts.append((path, Path(path).read_text(encoding="utf-8", errors="ignore")))
        except OSError as exc:
            print(f"⚠️  Could not read {path}: {exc}")
    for path in _grep_listing("--cached"):
        texts.append((path, _index_text(path)))
    return texts


def _violations_in_text(path: str, text: str) -> list[str]:
    """Home-path matches in `text` whose user segment is not allow-listed.

    Args:
        path: source file path, used to build each violation message.
        text: file content to scan for `HOME_PATH` matches.

    Returns:
        list[str]: one `"{path}: {match}"` entry per non-allow-listed match.
    """
    found = []
    for match in HOME_PATH.finditer(text):
        if match.group(1).lower() not in ALLOWED_USERS:
            found.append(f"{path}: {match.group(0)}")
    return found


def main() -> int:
    """Scan tracked, staged and untracked files; return the process exit code."""
    try:
        texts = collect_texts()
    except GitError as exc:
        print(f"❌ Scan aborted, git failed: {exc}", file=sys.stderr)
        return 2
    violations = []
    for path, text in texts:
        violations.extend(_violations_in_text(path, text))

    if violations:
        print("❌ Real-looking local developer paths found (use a generic placeholder):")
        for violation in sorted(set(violations)):
            print(f"  {violation}")
        return 1

    print("✅ No local developer-machine absolute paths found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
