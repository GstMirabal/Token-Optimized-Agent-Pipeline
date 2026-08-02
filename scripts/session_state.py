"""Claim and release the session lock in docs/active_state.json.

Until Phase 019, `start_workflow.md` was the only workflow that wrote nothing:
all nine of its steps read or verified. `close_workflow.md` had `state_sync`;
`start` had no counterpart, so `session_id` in the anchor was always the *last
closed* session's, never the running one.

The consequence was not cosmetic. `start_workflow.md` Phase 1 promised to
"abort if IN_PROGRESS exists with a different session UID (crash forensics)",
but nothing anywhere ever wrote that state — `grep -rn IN_PROGRESS` over the
Python and workflow corpus returned zero writes. The collision guard could
never fire, and an abandoned session was indistinguishable from a clean one.

Claiming the lock and recording the session are the same act, so they are one
command rather than two steps that both rewrite the same file.

invoked_by: start_workflow.md#state_claim (claim), close_workflow.md#state_sync
(release).

Usage:
    python3 scripts/session_state.py claim --session-id <uid> [--takeover]
    python3 scripts/session_state.py release

Exit codes:
    0 — lock claimed or released
    2 — a different session holds the lock (RA-11: only 2 blocks a tool call)
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from hooks.state_mirror import mirror_active_state  # noqa: E402

ACTIVE_STATE = Path("docs/active_state.json")
IN_PROGRESS = "IN_PROGRESS"
CLOSED = "CLOSED_SUCCESSFULLY"


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def head_sha() -> str | None:
    """Current commit, or None outside a repository."""
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], capture_output=True, text=True
    )
    return result.stdout.strip() if result.returncode == 0 else None


def load_state() -> dict:
    if not ACTIVE_STATE.exists():
        return {}
    return json.loads(ACTIVE_STATE.read_text(encoding="utf-8"))


def save_state(state: dict) -> None:
    ACTIVE_STATE.parent.mkdir(parents=True, exist_ok=True)
    ACTIVE_STATE.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    mirror_active_state()


def claim(session_id: str, takeover: bool) -> int:
    """Record this session as the holder of the lock.

    Args:
        session_id: UID of the session claiming the lock.
        takeover: Seize a lock held by another session (crash recovery).

    Returns:
        int: 0 when claimed, 2 when another live session holds the lock.
    """
    state = load_state()
    holder = state.get("session_id")

    if state.get("status") == IN_PROGRESS and holder and holder != session_id and not takeover:
        # Deliberately not auto-seized: a second agent running concurrently and
        # a session that died mid-flight look identical from here, and only one
        # of them is safe to overwrite. The human decides which this is.
        print(
            f"❌ Session lock held by {holder}, still IN_PROGRESS.\n"
            f"   If that session crashed, re-run with --takeover.\n"
            f"   If it is still running, do not: two sessions writing one anchor "
            f"is the collision this guard exists to prevent.",
            file=sys.stderr,
        )
        return 2

    state.update({
        "session_id": session_id,
        "status": IN_PROGRESS,
        "start_time": now(),
        "last_updated": now(),
    })
    state.pop("end_time", None)
    save_state(state)
    print(f"✅ Session lock claimed by {session_id}.")
    return 0


def release() -> int:
    """Release the lock and record the commit the close sealed at."""
    state = load_state()
    state.update({
        "status": CLOSED,
        "end_time": now(),
        "last_updated": now(),
    })
    sha = head_sha()
    if sha:
        # Anything committed after this SHA happened outside the protocol.
        # Without it, drift is undetectable — which is how five merged pull
        # requests reached main with no ledger entry (Phase 018).
        state["last_close_commit"] = sha
    save_state(state)
    print(f"✅ Session lock released{f' at {sha[:7]}' if sha else ''}.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)

    claim_parser = sub.add_parser("claim", help="Record this session as lock holder.")
    claim_parser.add_argument("--session-id", required=True)
    claim_parser.add_argument(
        "--takeover", action="store_true",
        help="Seize a lock left behind by a crashed session.",
    )
    sub.add_parser("release", help="Release the lock at session close.")

    args = parser.parse_args()
    if args.command == "claim":
        return claim(args.session_id, args.takeover)
    return release()


if __name__ == "__main__":
    sys.exit(main())
