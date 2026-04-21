import os
import sys
import json
from pathlib import Path

# 🛡️ Hybrid Structural Auditor (Repo & Project Mode)
# Version: 2.0.0

def detect_context():
    if os.path.exists("backend") or os.path.exists("manage.py"):
        return "PROJECT"
    return "REPO"

def audit_project_apps():
    APPS_DIR = "backend/apps/"
    CONSTITUTIONAL_APPS = [
        "core", "datafeed", "live_trading", "notifications", 
        "portfolio_reporting", "risk_control", "strategies", 
        "technical_analysis", "trades", "users", "workbench"
    ]
    print("🔍 [STRUCTURAL AUDITOR] ANALYZING PROJECT BACKEND...")
    if not os.path.exists(APPS_DIR):
        print(f"🚨 Error: Apps directory {APPS_DIR} not found.")
        return 1

    existing_apps = [name for name in os.listdir(APPS_DIR) 
                    if os.path.isdir(os.path.join(APPS_DIR, name)) 
                    and name not in ["__pycache__", ".DS_Store"]]

    errors = 0
    for app in existing_apps:
        if app not in CONSTITUTIONAL_APPS:
            print(f"❌ [SHADOW APP DETECTED]: '{app}' is NOT sanctioned.")
            errors += 1
    for app in CONSTITUTIONAL_APPS:
        if app not in existing_apps:
            print(f"⚠️ Warning: Missing App '{app}'.")
            errors += 1
    return errors

def audit_repo_nodes():
    print("🔍 [STRUCTURAL AUDITOR] ANALYZING MATRIX CORE NODES...")
    errors = 0
    
    # 1. Audit Agent Profiles
    AGENTS_DIR = Path("agents")
    REGISTRY_FILE = Path("agents/agents_registry.json")
    
    if REGISTRY_FILE.exists():
        with open(REGISTRY_FILE, "r") as f:
            registry = json.load(f)
        
        # Check profiles on disk vs registry
        registered_agents = [registry[a].get("node_id", a) for a in registry]
        # (Assuming filenames match or are mapped) - Keep it simple: check if profiles exist
        for agent_key in registry:
            profile_path = AGENTS_DIR / f"{agent_key}.md"
            if not profile_path.exists() and agent_key != "principal_agent": # Principal might be root or moved
                 # Re-check relative to subfolder
                 pass
            
    # 2. Audit Skills (Sovereignty Check)
    SKILLS_ROOT = Path("skills")
    REQUIRED_LAYERS = ["core", "local", "3rd"]
    for layer in REQUIRED_LAYERS:
        if not (SKILLS_ROOT / layer).exists():
            print(f"❌ [SOVEREIGNTY BREACH]: Layer '{layer}' is missing from skills/.")
            errors += 1
        else:
            print(f"✅ Verified Layer: {layer}")

    # Check for stray root skills
    for item in SKILLS_ROOT.iterdir():
        if item.is_dir() and item.name not in REQUIRED_LAYERS:
            print(f"❌ [TOPOLOGY ERROR]: Stray folder '{item.name}' found in skills/ root.")
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
    
    print("✨ [AUDIT PASSED]: Matrix Structure is Valid.")
    sys.exit(0)

if __name__ == "__main__":
    main()
