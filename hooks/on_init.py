"""Session-start bridge sync for Claude Code **hosts**.

Host-scoped: the process cwd is the host project. Framework paths resolve
through ``scripts._root.agents_root()``; host paths (``.env``, bridge anchors
under ``.claude/``) stay relative to cwd. ``SessionStart`` does not run in the
nucleus — portable counterpart is ``workflows/start_workflow.md`` Phase 1.5
``bridge_check`` (`F-026-A3`).

invoked_by: claude/settings.hooks.json SessionStart, merged by scripts/install.py.

Usage:
    python3 hooks/on_init.py

Exit codes:
    0 — session may proceed (warnings are non-blocking)
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

# Package import for telemetry; scripts/ for agents_root.
_REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO))
sys.path.insert(0, str(_REPO / "scripts"))

from _root import agents_root  # noqa: E402
from hooks.telemetry import log_error  # noqa: E402

# Host-scoped (cwd = host project).
CONFIG_PATH = Path(".env")
ENV_TEMPLATE = Path(".env.template")
BRIDGE_ANCHORS = [
    Path(".claude/commands/agents/start.md"),
    Path(".claude/agents/principal_agent.md"),
]


def bridge_lock_path() -> Path:
    """Framework lock file inside the agents checkout."""
    return agents_root() / ".bridge_claude.lock"


def install_script_path() -> Path:
    """Framework installer entrypoint."""
    return agents_root() / "scripts" / "install.py"


def check_environment() -> bool:
    """Warn when a secrets template exists but ``.env`` does not.

    Secret sovereignty governs *not reading* ``.env`` into context — it does
    not require every host to have one.
    """
    if ENV_TEMPLATE.exists() and not CONFIG_PATH.exists():
        print(
            f"⚠️ [ON_INIT] {ENV_TEMPLATE} exists but {CONFIG_PATH} is missing — "
            "copy the template and export your secrets before running workflows "
            "that need them."
        )
        return False
    return True


def current_submodule_commit() -> str:
    """HEAD of the agents checkout, or \"unknown\" outside a git context."""
    root = agents_root()
    try:
        return subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except (subprocess.CalledProcessError, OSError):
        return "unknown"


def bridge_intact() -> bool:
    """Confirm linked host artifacts survive on disk, independent of the lock."""
    return all(path.exists() for path in BRIDGE_ANCHORS)


def sync_commands() -> bool:
    """Install or refresh the Claude Code bridge when the lock or artifacts drift."""
    lock = bridge_lock_path()
    installer = install_script_path()

    if lock.exists():
        if not bridge_intact():
            print(
                "🔄 [ON_INIT] Bridge lock present but linked artifacts are missing "
                "(likely wiped by `git clean` or a manual deletion). Re-linking bridge..."
            )
        else:
            recorded = lock.read_text().strip()
            current = current_submodule_commit()
            if current == "unknown" or recorded == current:
                return True
            print(
                f"🔄 [ON_INIT] .agents updated ({recorded[:12]} -> {current[:12]}). "
                "Re-linking bridge..."
            )

    if not installer.is_file():
        print(f"⚠️ [ON_INIT] Warning: {installer} not found. Skipping bridge install.")
        return True

    try:
        subprocess.run([sys.executable, str(installer)], check=True)
        return True
    except subprocess.CalledProcessError:
        print("❌ [ON_INIT] Failed to install the Claude Code bridge.")
        return False


def main() -> None:
    """Run environment and bridge checks for a host SessionStart."""
    print("🛡️ [DEVOPS AGENT] Initializing Pipeline Session Protocol...")

    env_ok = check_environment()
    if not env_ok:
        log_error("on_init", "ENVIRONMENT_VIOLATION", ".env file missing")

    sync_ok = sync_commands()
    if not sync_ok:
        log_error("on_init", "SYNC_VIOLATION", "Slash Command sync failed")

    if env_ok and sync_ok:
        print("✅ [DEVOPS AGENT] DEPLOYMENT_READY: PASSED. Pipeline integrity certified.")
    else:
        print("⚠️ [DEVOPS AGENT] DEPLOYMENT_READY: SEMI-PASSED. Review alerts above.")


if __name__ == "__main__":
    main()
