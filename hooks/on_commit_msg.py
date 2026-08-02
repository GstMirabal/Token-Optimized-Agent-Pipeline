"""Message-dependent commit gates, for every path into the repository.

`on_commit.py` runs at pre-commit time, where the commit message does not yet
exist: git has not finalised `COMMIT_EDITMSG`, so reading it there would test
the *previous* commit's message — worse than not checking. The agent path gets
around this because the Bash command carries `-m`, but a commit typed in a
terminal or made from an IDE had no message gate at all.

`commit-msg` is the hook that does have the message. This closes the coverage
hole rather than leaving it declared, and it is the same lesson PR #30 recorded
for the secret scanner: a guard that only sees the agent's commits misses most
of the commits in a repository with a human in it.

invoked_by: .git/hooks/commit-msg, installed by scripts/install_claude.py.

Usage:
    python3 hooks/on_commit_msg.py <path-to-commit-message-file>

Exit codes:
    0 — message passes every gate
    1 — rejected (git aborts the commit; `commit-msg` has no special code)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from hooks.on_commit import (  # noqa: E402
    audit_dependency_justification,
    audit_regression_test,
    get_staged_files,
    is_valid_commit_message,
)
from hooks.telemetry import log_error  # noqa: E402


def strip_comments(raw: str) -> str:
    """Drop git's own commentary, which is not part of the message."""
    return "\n".join(line for line in raw.splitlines() if not line.startswith("#")).strip()


def main() -> int:
    if len(sys.argv) < 2:
        print("⚠️  [DEVOPS AGENT] commit-msg hook called without a message file.",
              file=sys.stderr)
        return 0

    message_file = Path(sys.argv[1])
    if not message_file.exists():
        return 0

    message = strip_comments(message_file.read_text(encoding="utf-8", errors="replace"))
    if not message:
        return 0  # An empty message aborts the commit on git's own terms.

    staged = get_staged_files()

    failures = []
    if not is_valid_commit_message(message):
        failures.append(
            "Commit message must follow Conventional Commits and end with the "
            "#[Sprint_ID] suffix, e.g. \"feat(auth): add login flow #078\" (agents.md §5)."
        )
    for check in (audit_regression_test, audit_dependency_justification):
        if reason := check(message, staged):
            failures.append(reason)

    if failures:
        for reason in failures:
            print(f"❌ [DEVOPS AGENT] {reason}", file=sys.stderr)
        log_error("on_commit_msg", "MESSAGE_GATE_VIOLATION", message.splitlines()[0][:80])
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
