"""Persist session continuity artifacts before context loss (PreCompact).

Reads ``docs/active_state.json``, refreshes the mirror, and prints the sprint
``task_scope.md`` path derived from ``current_sprint`` when present. Does **not**
call ``session_state.py release`` (that seals the sprint).

invoked_by: claude/settings.hooks.json PreCompact; manual under Cursor after
compaction (docs/guides/AUTONOMY_POSTURE_GUIDE.md).

Usage:
    python3 scripts/persist_session_context.py

Exit codes:
    0 — mirror refreshed (or no anchor yet)
    2 — anchor exists but is invalid JSON
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from hooks.state_mirror import mirror_active_state

ACTIVE_STATE = Path("docs/active_state.json")


def task_scope_path(state: dict) -> Path | None:
    """Return the sprint task_scope path from the anchor, if derivable."""
    sprint = state.get("current_sprint") or {}
    sprint_id = sprint.get("id")
    layer = sprint.get("layer") or "core"
    app = sprint.get("app") or "pipeline"
    if sprint_id is None:
        return None
    return Path(f"docs/sprints/{int(sprint_id):03d}-{layer}-{app}/task_scope.md")


def main() -> int:
    """Refresh the mirror and report the task_scope pointer."""
    if not ACTIVE_STATE.is_file():
        print("⚠️ [PERSIST] No docs/active_state.json — nothing to persist.")
        return 0
    try:
        state = json.loads(ACTIVE_STATE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"❌ [PERSIST] Invalid active_state.json: {exc}", file=sys.stderr)
        return 2

    mirror_active_state()
    scope = task_scope_path(state)
    session_id = state.get("session_id", "?")
    status = state.get("status", "?")
    print(f"✅ [PERSIST] Mirrored anchor session={session_id} status={status}")
    if scope is not None:
        exists = "present" if scope.is_file() else "MISSING"
        print(f"   task_scope: {scope} ({exists})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
