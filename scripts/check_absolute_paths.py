"""Reject real developer-machine absolute paths in the tracked tree (RA-15).

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
"""

import re
import subprocess
import sys

ALLOWED_USERS = {"developer", "user", "username", "yourname", "example"}
HOME_PATH = re.compile(r"/(?:Users|home)/([A-Za-z0-9_.-]+)/")
GIT_GREP_PATTERN = r"/Users/[A-Za-z0-9_.-]\+/\|/home/[A-Za-z0-9_.-]\+/"


def candidate_files() -> list[str]:
    """Tracked files containing anything that looks like a home path."""
    result = subprocess.run(
        ["git", "grep", "-lIn", GIT_GREP_PATTERN],
        capture_output=True,
        text=True,
    )
    return [f for f in result.stdout.splitlines() if f and not f.startswith("venv_skillopt/")]


def main() -> int:
    violations = []
    for path in candidate_files():
        try:
            text = open(path, encoding="utf-8", errors="ignore").read()
        except OSError as exc:
            print(f"⚠️  Could not read {path}: {exc}")
            continue
        for match in HOME_PATH.finditer(text):
            if match.group(1).lower() not in ALLOWED_USERS:
                violations.append(f"{path}: {match.group(0)}")

    if violations:
        print("❌ Real-looking local developer paths found (use a generic placeholder):")
        for violation in sorted(set(violations)):
            print(f"  {violation}")
        return 1

    print("✅ No local developer-machine absolute paths found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
