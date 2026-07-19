import json
import shutil
from pathlib import Path

ACTIVE_STATE = Path("docs/active_state.json")
MIRROR_STATE = Path(".agent_state/mirror.json")

def mirror_active_state():
    """State redundancy (agents.md §5 state_anchor, Sprint #031): shadow copy of the active state to prevent data loss."""
    if ACTIVE_STATE.exists():
        MIRROR_STATE.parent.mkdir(parents=True, exist_ok=True)
        # Verify valid JSON before mirroring
        try:
            with open(ACTIVE_STATE, "r") as f:
                json.load(f)
            shutil.copy2(ACTIVE_STATE, MIRROR_STATE)
        except json.JSONDecodeError:
            pass # Keep it silent to not interrupt workflows unnecessarily unless debugging
    else:
        pass


if __name__ == "__main__":
    # Invoked directly as a Claude Code Stop hook (see claude/settings.hooks.json).
    mirror_active_state()
