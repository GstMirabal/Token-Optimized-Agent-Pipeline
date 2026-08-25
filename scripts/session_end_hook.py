"""SessionEnd wrapper: end the session without sealing the sprint.

Calls ``scripts/session_state.py suspend`` (never ``release``). Wiring
``release`` here would write a false ``last_close_commit`` and blind
``detect_drift.py`` (Sprint 027 Design §D4 / roadmap SessionEnd note).

invoked_by: claude/settings.hooks.json SessionEnd.

Usage:
    python3 scripts/session_end_hook.py

Exit codes:
    Propagates ``session_state.py suspend`` (0 success, 2 lock conflict).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "session_state.py"


def main() -> int:
    """Run suspend in a subprocess; refuse to call release."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "suspend"],
        check=False,
    )
    return int(result.returncode)


if __name__ == "__main__":
    sys.exit(main())
