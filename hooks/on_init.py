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
ENV_TEMPLATE = Path(".env.template")
BRIDGE_LOCK = Path(".agents/.claude_bridge.lock")
INSTALL_SCRIPT = Path(".agents/scripts/install_claude.py")

def check_environment() -> bool:
    """Secret sovereignty (agents.md §3 secret_sovereignty) governs *not reading* .env into context —
    it does not require every host to have one. Only warn when the project
    declares it needs secrets (an .env.template exists) but .env is missing."""
    if ENV_TEMPLATE.exists() and not CONFIG_PATH.exists():
        print(f"⚠️ [ON_INIT] {ENV_TEMPLATE} exists but {CONFIG_PATH} is missing — "
              "copy the template and export your secrets before running workflows that need them.")
        return False
    return True

def current_submodule_commit() -> str:
    """HEAD of the .agents submodule, or "unknown" outside a git context."""
    try:
        return subprocess.run(
            ["git", "-C", ".agents", "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except (subprocess.CalledProcessError, OSError):
        return "unknown"


def sync_commands() -> bool:
    """Ensures the Claude Code bridge (.claude/agents, commands, skills, hooks,
    MCP) is installed AND current. Re-runs the (idempotent) installer when the
    lock is missing or the submodule commit changed since the last install —
    a deliberate `.agents` update ships new assets that need linking."""
    if BRIDGE_LOCK.exists():
        recorded = BRIDGE_LOCK.read_text().strip()
        current = current_submodule_commit()
        if current == "unknown" or recorded == current:
            return True
        print(f"🔄 [ON_INIT] .agents updated ({recorded[:12]} -> {current[:12]}). Re-linking bridge...")

    if not INSTALL_SCRIPT.exists():
        print(f"⚠️ [ON_INIT] Warning: {INSTALL_SCRIPT} not found. Skipping bridge install.")
        return True

    try:
        subprocess.run([sys.executable, str(INSTALL_SCRIPT)], check=True)
        return True
    except subprocess.CalledProcessError:
        print("❌ [ON_INIT] Failed to install the Claude Code bridge.")
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
