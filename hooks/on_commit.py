import subprocess
import sys
import json
from datetime import datetime
from pathlib import Path

# Configuration
TELEMETRY_PATH = Path("core/memory/telemetry/raw_errors.json")

def log_error(error_type: str, details: str):
    """Logs errors for heuristic distillation (Sprint #028)."""
    if not TELEMETRY_PATH.exists():
        TELEMETRY_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(TELEMETRY_PATH, "w") as f:
            json.dump([], f)
    
    try:
        with open(TELEMETRY_PATH, "r") as f:
            data = json.load(f)
        
        data.append({
            "timestamp": datetime.now().isoformat(),
            "hook": "on_commit",
            "type": error_type,
            "details": details
        })
        
        with open(TELEMETRY_PATH, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"⚠️ [TELEMETRY] Failed to log error: {e}")

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
            # skills/layer/skill-name/... -> skill-name is at index 2
            parts = path.parts
            if len(parts) >= 3 and parts[0] == "skills":
                skill_root = Path(*parts[:3])
                modified_skills.add(skill_root)

    violations = []
    for skill_path in modified_skills:
        print(f"🔍 [DEVOPS SENTINEL] Auditing {skill_path}...")
        
        # Trinity requirements
        readme = skill_path / "README.md"
        skill_md = skill_path / "SKILL.md"
        scripts = skill_path / "scripts"

        if not readme.exists():
            violations.append(f"{skill_path}: Missing README.md")
        if not skill_md.exists():
            violations.append(f"{skill_path}: Missing SKILL.md")
        if not scripts.is_dir():
            violations.append(f"{skill_path}: Missing scripts/ directory")

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

def main():
    print("🛡️ [DEVOPS SENTINEL] Pre-Commit Integrity Handshake...")
    
    trinity_ok = audit_trinity_standard()
    if not trinity_ok:
        log_error("TRINITY_VIOLATION", "Rule 60 compliance check failed")

    secrets_ok = audit_secret_shielding()
    if not secrets_ok:
        log_error("SECRET_VIOLATION", "Rule 66 scrutiny detected vulnerabilities")
    
    if trinity_ok and secrets_ok:
        print("✅ [DEVOPS SENTINEL] PR_COMMIT_UNLOCKED: PASSED.")
        sys.exit(0)
    else:
        print("❌ [DEVOPS SENTINEL] CRITICAL VIOLATION DETECTED. Commit blocked.")
        sys.exit(1)

if __name__ == "__main__":
    main()
