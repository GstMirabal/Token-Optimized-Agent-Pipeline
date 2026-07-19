import subprocess
import sys
import json
import re
from datetime import datetime
from pathlib import Path

import sys
# Add parent directory to path so 'hooks' module can be found if run directly
sys.path.append(str(Path(__file__).parent.parent))
from hooks.telemetry import log_error

def get_staged_files() -> list[str]:
    """Retrieves the list of files staged for the current commit."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        print(f"⚠️ [DEVOPS SENTINEL] Git error: {e}")
        return []

def audit_trinity_standard() -> bool:
    """Certifies Rule 60 (Trinity Standard) for modified skills."""
    staged_files = get_staged_files()
    if not staged_files:
        return True

    # Identify skills that have modified files
    modified_skills = set()
    for file_path in staged_files:
        path = Path(file_path)
        if "skills/" in file_path:
            # skills/skill-name/... -> skill-name is at index 1 (flat topology)
            parts = path.parts
            if len(parts) >= 2 and parts[0] == "skills":
                skill_root = Path(*parts[:2])
                modified_skills.add(skill_root)

    violations = []
    for skill_path in modified_skills:
        print(f"🔍 [DEVOPS SENTINEL] Auditing {skill_path}...")

        skill_md = skill_path / "SKILL.md"
        scripts = skill_path / "scripts"

        # Every skill needs a SKILL.md with name/description frontmatter.
        if not skill_md.exists():
            violations.append(f"{skill_path}: Missing SKILL.md")
        else:
            head = skill_md.read_text(encoding="utf-8")[:500]
            if not head.startswith("---") or "name:" not in head or "description:" not in head:
                violations.append(f"{skill_path}: SKILL.md missing name/description frontmatter")

        # Full Trinity only applies to executable skills (agents.md §3 trinity_standard):
        # a skill that ships scripts/ must also ship README.md and scripts/__init__.py.
        # Knowledge skills (no scripts/) are complete with just SKILL.md.
        if scripts.is_dir():
            if not (skill_path / "README.md").exists():
                violations.append(f"{skill_path}: Executable skill missing README.md")
            if not (scripts / "__init__.py").exists():
                violations.append(f"{skill_path}: scripts/ missing __init__.py")

    if violations:
        for v in violations:
            print(f"❌ [ON_COMMIT] Trinity Violation: {v}")
        return False
    
    return True

def audit_secret_shielding() -> bool:
    """Certifies Rule 66 (Secret Shielding)."""
    staged_files = get_staged_files()
    
    forbidden_extensions = [".env", ".pem", ".key"]
    forbidden_names = ["secrets.json", "credentials.json"]
    
    violations = []
    for file_path in staged_files:
        path = Path(file_path)
        
        # Check by filename/extension
        if path.suffix in forbidden_extensions or path.name in forbidden_names:
            violations.append(f"Forbidden file staged: {file_path}")
            continue

        # Basic content scanning for API keys or secrets
        try:
            content = subprocess.run(
                ["git", "show", f":{file_path}"],
                capture_output=True,
                text=True,
                check=True
            ).stdout
            
            # Pattern matching (Case insensitive)
            secret_patterns = ["API_KEY =", "SECRET =", "PASSWORD =", "PRIVATE_KEY"]
            for pattern in secret_patterns:
                if pattern in content.upper():
                    violations.append(f"Suspicious string '{pattern}' detected in {file_path}")
                    break
        except Exception:
            # Skip binary files or git errors
            continue

    if violations:
        for v in violations:
            print(f"❌ [ON_COMMIT] Secret Violation: {v}")
        return False

    return True

DEPLOY_UNLOCK = Path(".agents/.deploy_unlock")

# Conventional Commit type + optional scope + description ending in #[Sprint_ID]
# (agents.md §5 historical_log). Example: "feat(auth): add login flow #078".
COMMIT_MSG_REGEX = re.compile(
    r"^(feat|fix|docs|chore|refactor|test|style|perf|ci|build|revert)"
    r"(\([\w\-./]+\))?!?: .+#\w+"
)


def read_hook_command() -> str:
    """Reads the PreToolUse payload from stdin and returns the Bash command.

    Claude Code invokes PreToolUse hooks on every matching tool call (here: every
    Bash call), passing {"tool_name": ..., "tool_input": {"command": ...}} on stdin.
    Returns "" when there is no payload (e.g. run manually for testing).
    """
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return ""
    return payload.get("tool_input", {}).get("command", "")


def is_blocked_push(command: str) -> bool:
    """J-12 mechanical enforcement: pushes to main/master are blocked unless the
    deployment workflow has explicitly created the .agents/.deploy_unlock marker."""
    if "git push" not in command:
        return False
    if not re.search(r"git push\s+(?:-[^\s]+\s+)*\S+\s+(main|master)(?=\s|$|:)", command):
        return False
    return not DEPLOY_UNLOCK.exists()


def extract_commit_message(command: str) -> str | None:
    """Pulls the -m message out of a git commit command, if present."""
    m = re.search(r"-m\s+(?:\"([^\"]*)\"|'([^']*)')", command)
    if not m:
        return None
    return m.group(1) if m.group(1) is not None else m.group(2)


def is_valid_commit_message(message: str) -> bool:
    """Conventional Commit + mandatory #[Sprint_ID] suffix (agents.md §5)."""
    first_line = message.splitlines()[0] if message else ""
    return bool(COMMIT_MSG_REGEX.match(first_line))


def block(reason: str) -> None:
    # Claude Code only feeds stderr back to the model on a blocking hook, and
    # only exit code 2 actually blocks (J-11 HOOK_BLOCKING_SEMANTICS).
    print(f"❌ [DEVOPS SENTINEL] {reason}", file=sys.stderr)
    sys.exit(2)


def main():
    command = read_hook_command()

    # Guard 1 (J-12): no direct pushes to main/master outside deployment.
    if command and is_blocked_push(command):
        log_error("on_commit", "BRANCH_VIOLATION", "Direct push to main/master blocked (J-12)")
        block("Push to main/master is PROHIBITED (J-12 Branch Discipline). "
              "Merge through the deployment workflow (/agents:deployment), which creates "
              ".agents/.deploy_unlock for its sanctioned fallback push.")

    # Everything below only applies to git commit invocations.
    if command and "git commit" not in command:
        sys.exit(0)

    # Guard 2 (agents.md §5): Conventional Commit + #[Sprint_ID] suffix.
    if command:
        message = extract_commit_message(command)
        if message is not None and not is_valid_commit_message(message):
            log_error("on_commit", "COMMIT_MSG_VIOLATION", f"Non-conforming message: {message[:80]}")
            block("Commit message must follow Conventional Commits and end with the "
                  "#[Sprint_ID] suffix, e.g. \"feat(auth): add login flow #078\" (agents.md §5).")

    print("🛡️ [DEVOPS SENTINEL] Pre-Commit Integrity Handshake...")

    trinity_ok = audit_trinity_standard()
    if not trinity_ok:
        log_error("on_commit", "TRINITY_VIOLATION", "Rule 60 compliance check failed")

    secrets_ok = audit_secret_shielding()
    if not secrets_ok:
        log_error("on_commit", "SECRET_VIOLATION", "Rule 66 scrutiny detected vulnerabilities")

    if trinity_ok and secrets_ok:
        try:
            from hooks.state_mirror import mirror_active_state
            mirror_active_state()
        except ImportError:
            pass
        print("✅ [DEVOPS SENTINEL] PR_COMMIT_UNLOCKED: PASSED.")
        sys.exit(0)
    else:
        block("CRITICAL VIOLATION DETECTED. Commit blocked.")

if __name__ == "__main__":
    main()
