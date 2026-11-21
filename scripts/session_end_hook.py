"""SessionEnd wrapper: end the session without sealing the sprint.

Calls ``scripts/session_state.py suspend`` (never ``release``), forwarding the
SessionEnd payload's ``session_id`` so only the lock holder's end suspends. Wiring
``release`` here would write a false ``last_close_commit`` and blind
``detect_drift.py`` (Sprint 027 Design §D4 / roadmap SessionEnd note).

invoked_by: claude/settings.hooks.json SessionEnd.

Usage:
    python3 scripts/session_end_hook.py   # SessionEnd JSON payload on stdin

Exit codes:
    Propagates ``session_state.py suspend`` (0 success, 2 lock conflict).
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "session_state.py"


def payload_session_id() -> str:
    """The `session_id` of the SessionEnd payload on stdin.

    Returns:
        str: the id, or "" when stdin is unreadable, is not a JSON object, or
            holds no non-empty string `session_id`. "" makes `suspend` leave
            the anchor untouched: an absent id cannot show the ending session
            is the lock holder (KI-057-2).
    """
    try:
        payload = json.loads(sys.stdin.read(65536))
    except (OSError, ValueError):
        return ""
    value = payload.get("session_id") if isinstance(payload, dict) else None
    return value if isinstance(value, str) else ""


def main() -> int:
    """Run suspend in a subprocess for the ending session; refuse to call release."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "suspend", f"--hook-session-id={payload_session_id()}"],
        check=False,
    )
    return int(result.returncode)


if __name__ == "__main__":
    sys.exit(main())
