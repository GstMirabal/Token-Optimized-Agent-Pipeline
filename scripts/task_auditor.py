import os
import re
import sys

# 🛡️ CryptoBot Task Auditor (Rule 36/50)
# Version: 1.0.0
# Logic: Cross-check task.md with the physical file system clusters.

TASK_FILE = ".agents/task/task.md"
FOLDERS = [".agents/task/sprints/", ".agents/task/roadmaps/", ".agents/task/history/", ".agents/task/topology/"]

def audit_task_integrity():
    print("🔍 [TASK AUDITOR] ANALYZING REPOSITORY CONSISTENCY (V3)...")
    
    if not os.path.exists(TASK_FILE):
        print(f"🚨 Error: Master Index {TASK_FILE} not found.")
        sys.exit(1)

    with open(TASK_FILE, "r") as f:
        content = f.read()

    errors = 0
    # 1. Verification of Mandatory Folders
    for folder in FOLDERS:
        if not os.path.exists(folder):
            print(f"⚠️ Warning: Cluster {folder} does not exist. Rule 50 Violation!")
            errors += 1
            continue
            
        found_files = [f for f in os.listdir(folder) if f.endswith(".md")]
        for file_name in found_files:
            # Extract Sprint ID (e.g., "009") from filename "009-something.md"
            match = re.search(r'(\d{3})', file_name)
            if match:
                sprint_id = match.group(1)
                # Check if this ID is in task.md
                if sprint_id not in content:
                    print(f"❌ [SOVEREIGNTY BREACH]: File '{file_name}' (ID {sprint_id}) is NOT in Master Index.")
                    errors += 1
                else:
                    print(f"✅ Verified Sprint: {file_name}")
            else:
                # For Roadmaps or Implementation Plans (V3, PHASE_0, etc.)
                identifier = file_name.replace(".md", "")
                # We extract the core identifier (e.g., PHASE_4 from PHASE_4_ROADMAP.md)
                core_id = identifier.split('_ROADMAP')[0]
                if core_id not in content:
                    print(f"❌ [SOVEREIGNTY BREACH]: Roadmap '{file_name}' is NOT in Master Index.")
                    errors += 1
                else:
                    print(f"✅ Verified Roadmap: {file_name}")

    if errors > 0:
        print(f"🚨 [AUDIT FAILED]: Matrix Task Geography is desynchronized.")
        sys.exit(1)
    
    print("✨ [AUDIT PASSED]: Matrix Task Geography is 100% Synchronized.")
    sys.exit(0)

if __name__ == "__main__":
    audit_task_integrity()
