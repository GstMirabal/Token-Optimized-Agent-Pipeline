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
