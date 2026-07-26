import os
import re
import sys
import json
from pathlib import Path

# 🛡️ Hybrid Structural Auditor (Repo & Project Mode)
# Version: 3.0.0 — flat-topology aware, project app list externalized.

APP_MANIFEST = Path("docs/architecture/APPS_MANIFEST.json")


def detect_context():
    if os.path.exists("backend") or os.path.exists("manage.py"):
        return "PROJECT"
    return "REPO"


def audit_project_apps():
    """Validates backend/apps/ against the host's own sanctioned app list.

    The list lives in the HOST project (docs/architecture/APPS_MANIFEST.json,
    format: {"apps": ["core", "users", ...]}), never hardcoded here — a
    universal framework cannot know a host's domain apps.
    """
    apps_dir = Path("backend/apps")
    print("🔍 [STRUCTURAL AUDITOR] ANALYZING PROJECT BACKEND...")
    if not apps_dir.exists():
        print(f"🚨 Error: Apps directory {apps_dir} not found.")
        return 1
    if not APP_MANIFEST.exists():
        print(f"⚠️ {APP_MANIFEST} not found — skipping sanctioned-app audit. "
              "Create it with {\"apps\": [...]} to enable shadow-app detection.")
        return 0

    sanctioned = set(json.loads(APP_MANIFEST.read_text()).get("apps", []))
    existing = {p.name for p in apps_dir.iterdir()
                if p.is_dir() and p.name not in ("__pycache__", ".DS_Store")}

    errors = 0
    for app in sorted(existing - sanctioned):
        print(f"❌ [SHADOW APP DETECTED]: '{app}' is NOT sanctioned.")
        errors += 1
    for app in sorted(sanctioned - existing):
        print(f"⚠️ Warning: Missing App '{app}'.")
        errors += 1
    return errors


def audit_repo_nodes():
    """Validates the .agents core: agent frontmatter + flat skill topology."""
    print("🔍 [STRUCTURAL AUDITOR] ANALYZING PIPELINE CORE NODES...")
    errors = 0

    # 1. Agent profiles: every agents/*.md needs name/description frontmatter.
    for profile in sorted(Path("agents").glob("*.md")):
        head = profile.read_text(encoding="utf-8")[:500]
        if not head.startswith("---") or "name:" not in head or "description:" not in head:
            print(f"❌ [PROFILE ERROR]: {profile} missing name/description frontmatter.")
            errors += 1

    # 2. Skills: flat topology (agents.md §3) + Three-File Skill Standard.
    skills_root = Path("skills")
    forbidden_layers = {"core", "local", "3rd", "frontend", "backend"}
    for item in sorted(skills_root.iterdir()):
        if not item.is_dir():
            continue
        if item.name in forbidden_layers:
            print(f"❌ [TOPOLOGY ERROR]: Nested layer '{item.name}/' is PROHIBITED (flat topology).")
            errors += 1
            continue
        skill_md = item / "SKILL.md"
        if not skill_md.exists():
            print(f"❌ [STRUCTURE ERROR]: {item} missing SKILL.md.")
            errors += 1
            continue
        head = skill_md.read_text(encoding="utf-8")[:500]
        if not head.startswith("---") or "name:" not in head or "description:" not in head:
            print(f"❌ [STRUCTURE ERROR]: {skill_md} missing name/description frontmatter.")
            errors += 1
        scripts = item / "scripts"
        if scripts.is_dir():
            if not (item / "README.md").exists():
                print(f"❌ [STRUCTURE ERROR]: executable skill {item} missing README.md.")
                errors += 1
            if not (scripts / "__init__.py").exists():
                print(f"❌ [STRUCTURE ERROR]: {scripts} missing __init__.py.")
                errors += 1

    return errors


def main():
    context = detect_context()
    if context == "PROJECT":
        errors = audit_project_apps()
    else:
        errors = audit_repo_nodes()

    if errors > 0:
        print(f"🚨 [AUDIT FAILED]: {errors} structural conflicts detected.")
        sys.exit(1)

    print("✨ [AUDIT PASSED]: Pipeline Structure is Valid.")
    sys.exit(0)


if __name__ == "__main__":
    main()
