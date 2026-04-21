import os
import subprocess
import json
from datetime import datetime
from pathlib import Path

import sys
# Add parent directory to path so 'hooks' module can be found if run directly
sys.path.append(str(Path(__file__).parent.parent))
from hooks.telemetry import log_error

# Configuration
CONFIG_PATH = Path(".env")
SYNC_SCRIPT = Path("skills/core/slash-commander/scripts/generate_commands.py")

def check_environment() -> bool:
    """Verifies that the .env file exists for secret sovereignty."""
    if not CONFIG_PATH.exists():
        print(f"❌ [ON_INIT] Fatal: {CONFIG_PATH} not found. Security Rule 66 violated.")
        return False
    return True

def sync_commands() -> bool:
    """Invokes slash-commander to synchronize workflows with Claude Code."""
    if not SYNC_SCRIPT.exists():
        print(f"⚠️ [ON_INIT] Warning: {SYNC_SCRIPT} not found. Skipping command sync.")
        return True
    
    try:
        subprocess.run(["python3", str(SYNC_SCRIPT)], check=True)
        return True
    except subprocess.CalledProcessError:
        print("❌ [ON_INIT] Failed to synchronize slash commands.")
        return False

def main():
    print("🛡️ [DEVOPS SENTINEL] Initializing Matrix Session Protocol...")
    
    env_ok = check_environment()
    if not env_ok:
        log_error("on_init", "ENVIRONMENT_VIOLATION", ".env file missing")

    sync_ok = sync_commands()
    if not sync_ok:
        log_error("on_init", "SYNC_VIOLATION", "Slash Command sync failed")
    
    if env_ok and sync_ok:
        print("✅ [DEVOPS SENTINEL] DEPLOYMENT_READY: PASSED. Matrix integrity certified.")
    else:
        print("⚠️ [DEVOPS SENTINEL] DEPLOYMENT_READY: SEMI-PASSED. Review alerts above.")

if __name__ == "__main__":
    main()
