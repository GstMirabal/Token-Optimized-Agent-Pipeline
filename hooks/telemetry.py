"""Record hook errors as raw material for heuristic distillation.

**Host-scoped**: the root is the project being worked. `memory/` belongs to the
host and is purged at its sprint close, so this path MUST NOT be anchored to
`scripts/_root.py` — doing so would write a host's error log into the framework
submodule, which `agents.md §3 strict_rule` forbids outright (Sprint 023 `C0.3`).

invoked_by: hooks/on_commit.py, hooks/on_init.py.
"""
import json
from datetime import datetime
from pathlib import Path

# Note: As these hooks are triggered from the root, we use relative paths from the root.
TELEMETRY_PATH = Path("memory/telemetry/raw_errors.json")

def log_error(hook_name: str, error_type: str, details: str):
    """Logs errors for heuristic distillation (Sprint #028 / #031)."""
    if not TELEMETRY_PATH.exists():
        TELEMETRY_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(TELEMETRY_PATH, "w") as f:
            json.dump([], f)
    
    try:
        with open(TELEMETRY_PATH, "r") as f:
            data = json.load(f)
        
        data.append({
            "timestamp": datetime.now().isoformat(),
            "hook": hook_name,
            "type": error_type,
            "details": details
        })
        
        with open(TELEMETRY_PATH, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"⚠️ [TELEMETRY] Failed to log error: {e}")
