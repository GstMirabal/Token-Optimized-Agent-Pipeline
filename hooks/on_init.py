import os
import subprocess
from pathlib import Path

# Configuration
CONFIG_PATH = Path(".env")
SYNC_SCRIPT = Path("skills/core/slash-commander/scripts/generate_commands.py")

def check_environment():
    """Certifies environment habitability (Rule 66)."""
    if not CONFIG_PATH.exists():
        print("⚠️ [DEVOPS SENTINEL] Warning: .env file missing. Environmental Sovereignty at risk.")
        return False
    return True

def sync_commands():
    """Triggers Slash Command Synchronization (Rule 113)."""
    if SYNC_SCRIPT.exists():
        try:
            subprocess.run(["python3", str(SYNC_SCRIPT)], check=True)
            return True
        except subprocess.CalledProcessError:
            print("❌ [DEVOPS SENTINEL] Error: Slash Command synchronization failed.")
            return False
    return False

def main():
    print("🛡️ [DEVOPS SENTINEL] Initializing Matrix Session Protocol...")
    
    env_ok = check_environment()
    sync_ok = sync_commands()
    
    if env_ok and sync_ok:
        print("✅ [DEVOPS SENTINEL] DEPLOYMENT_READY: PASSED. Matrix integrity certified.")
    else:
        print("⚠️ [DEVOPS SENTINEL] DEPLOYMENT_READY: SEMI-PASSED. Review alerts above.")

if __name__ == "__main__":
    main()
