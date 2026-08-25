"""Reject force-push and non-fast-forward updates to existing refs.

The Claude Code ``permissions.deny`` list blocks ``git push --force`` only
inside Claude Code. Under Cursor there is no equivalent guard; this native
``pre-push`` hook covers every tool path into the repository.

``rm -rf /`` is intentionally out of scope — that guard remains Claude Code
exclusive (roadmap line 984).

invoked_by: .git/hooks/pre-push, installed by scripts/install.py.

Exit codes:
    0 — push allowed
    1 — push rejected (any non-zero exit blocks ``git push``)
"""
from __future__ import annotations

import subprocess
import sys

ZERO_SHA = "0" * 40


def ref_update_allowed(local_sha: str, remote_sha: str) -> bool:
    """Return True when updating ``remote_ref`` is a fast-forward."""
    if remote_sha == ZERO_SHA:
        return True
    if local_sha == ZERO_SHA:
        return True
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", remote_sha, local_sha],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0


def main() -> int:
    for line in sys.stdin:
        stripped = line.strip()
        if not stripped:
            continue
        parts = stripped.split()
        if len(parts) != 4:
            continue
        _local_ref, local_sha, remote_ref, remote_sha = parts
        if ref_update_allowed(local_sha, remote_sha):
            continue
        print(
            f"❌ [ON_PUSH] Rejected non-fast-forward update to {remote_ref}. "
            "Force-push and history rewrite are blocked.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
