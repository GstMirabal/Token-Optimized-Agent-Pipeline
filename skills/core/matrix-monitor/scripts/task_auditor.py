import os
import re
import sys
from pathlib import Path

# 🛡️ Hybrid Task Auditor (Repo & Project Mode)
# Version: 2.0.0

def detect_context():
    """Detects if we are in a Submodule Repo context or a Parent Project context."""
    if os.path.exists("backend") or os.path.exists("manage.py"):
        return "PROJECT"
    return "REPO"

def find_task_file(context):
    """Finds the authoritative task file based on context."""
    if context == "PROJECT":
        paths = [".agents/task/task.md", ".agents/task.md", "task.md"]
    else:
        paths = ["task.md", "agents.md"]
        
    for p in paths:
        if os.path.exists(p):
            return p
    return None

def find_clusters(context):
    """Finds the clusters (roadmaps, sprints, etc) based on context."""
    if context == "PROJECT":
        base = Path(".agents/task")
    else:
        base = Path(".")
        
    clusters = ["roadmaps", "sprints", "history", "topology"]
    found = []
    for c in clusters:
        p = base / c
        if p.exists() and p.is_dir():
            found.append(p)
    return found

def audit():
    context = detect_context()
    print(f"🔍 [TASK AUDITOR] IDENTIFIED CONTEXT: {context}")
    
    task_file = find_task_file(context)
    if not task_file:
        print("🚨 Error: No master task index (task.md or agents.md) found.")
        sys.exit(1)
        
    print(f"📖 Using Index: {task_file}")
    with open(task_file, "r") as f:
        content = f.read()

    clusters = find_clusters(context)
    if not clusters:
        print("⚠️ No clusters (roadmaps/sprints/etc) found. Checking index integrity only...")
    
    errors = 0
    for cluster in clusters:
        print(f"📁 Auditing Cluster: {cluster}")
        found_files = list(cluster.glob("*.md"))
        for file_path in found_files:
            file_name = file_path.name
            # Check if filename or its ID is in index
            identifier = file_name.replace(".md", "")
            if identifier not in content:
                print(f"❌ [SOVEREIGNTY BREACH]: '{file_name}' is NOT in {task_file}")
                errors += 1
            else:
                print(f"✅ Verified: {file_name}")

    if errors > 0:
        print(f"🚨 [AUDIT FAILED]: {errors} desynchronizations found.")
        sys.exit(1)
        
    print("✨ [AUDIT PASSED]: Task Geography is Synchronized.")
    sys.exit(0)

if __name__ == "__main__":
    audit()
