import os
import shutil
import re

DOCS_DIR = "docs"

def migrate():
    # 1. Identify all sprint directories
    # Pattern: docs/[stack]/[layer]/[sprint_id] where sprint_id is 3 digits
    sprint_dirs = []
    for root, dirs, files in os.walk(DOCS_DIR):
        for d in dirs:
            if re.match(r"^\d{3}$", d):
                full_path = os.path.join(root, d)
                # Extract stack and layer
                parts = full_path.split(os.sep)
                # full_path is docs/[stack]/[layer]/[id]
                if len(parts) >= 4:
                    stack = parts[1]
                    layer = parts[2]
                    sprint_id = d
                    sprint_dirs.append({
                        "old_path": full_path,
                        "id": sprint_id,
                        "stack": stack,
                        "layer": layer
                    })

    # 2. Create new flat structure for sprints
    for item in sprint_dirs:
        new_dir_name = f"{item['id']}-{item['stack']}-{item['layer']}"
        new_path = os.path.join(DOCS_DIR, new_dir_name)
        
        print(f"Migrating {item['old_path']} -> {new_path}")
        os.makedirs(new_path, exist_ok=True)
        
        # Move contents
        old_dir = item['old_path']
        
        # Implementation Plan
        impl_plan_old = os.path.join(old_dir, "implementation_plan.md")
        if not os.path.exists(impl_plan_old):
             # Try inside implementation_plan folder
             impl_plan_old = os.path.join(old_dir, "implementation_plan", "implementation_plan.md")
        
        if os.path.exists(impl_plan_old):
            shutil.copy2(impl_plan_old, os.path.join(new_path, "0_implementation_plan.md"))
        
        # Roadmap
        # Check if there is a roadmap folder with a file
        roadmap_folder = os.path.join(old_dir, "roadmap")
        if os.path.exists(roadmap_folder) and os.path.isdir(roadmap_folder):
            roadmap_files = os.listdir(roadmap_folder)
            if roadmap_files:
                # Use the first .md file
                md_files = [f for f in roadmap_files if f.endswith(".md")]
                if md_files:
                    shutil.copy2(os.path.join(roadmap_folder, md_files[0]), os.path.join(new_path, "1_roadmap.md"))
        
        # Tasks (Sprints)
        tasks_old = os.path.join(old_dir, "sprints")
        tasks_new = os.path.join(new_path, "tasks")
        if os.path.exists(tasks_old):
            if os.path.exists(tasks_new):
                shutil.rmtree(tasks_new)
            shutil.copytree(tasks_old, tasks_new)
        
        # Remove old sprint dir if empty or after moving everything
        # (We'll do a cleanup later to avoid deleting parents too early)

    # 3. Handle Architecure and general files
    # We'll move docs/[stack]/[layer]/ARCHITECTURE.md to docs/architecture/[stack]/[layer]/
    arch_files = []
    for root, dirs, files in os.walk(DOCS_DIR):
        # Skip the new flat dirs we just created
        if any(re.match(r"^\d{3}-", p) for p in root.split(os.sep)):
            continue
            
        for f in files:
            if f.endswith(".md") or f.endswith(".json") or f.endswith(".yml"):
                full_path = os.path.join(root, f)
                parts = full_path.split(os.sep)
                # Skip active_state.json
                if f == "active_state.json" and root == DOCS_DIR:
                    continue
                
                # If it's a generic file in a stack/layer
                if len(parts) >= 3:
                    stack = parts[1]
                    layer = parts[2]
                    # Check if this is not a sprint folder (already handled)
                    if not re.match(r"^\d{3}$", layer):
                         arch_files.append({
                             "old_path": full_path,
                             "stack": stack,
                             "layer": layer,
                             "filename": f,
                             "rel_root": root
                         })

    for item in arch_files:
        # Keep them in a structured way but maybe under 'architecture' or 'core'
        # Actually, let's keep the stack/layer folders but clean them of sprint folders
        pass # For now, we only move sprints to flat.

    print("Migration complete for sprint folders.")

if __name__ == "__main__":
    migrate()
