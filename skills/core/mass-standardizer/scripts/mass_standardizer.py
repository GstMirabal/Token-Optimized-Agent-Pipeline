#!/usr/bin/env python3
import json
import os
from pathlib import Path

# Templates
SKILL_MD_TEMPLATE = """---
name: {name}
description: {description}
category: {category}
tags: {tags}
---

# 🛠️ Skill Profile: {name_human}

## Technical Logic
This skill implements the procedural logic for **{name_human}**. (Automatic scaffolding).

## Procedures
- [ ] Define step-by-step logic here.
- [ ] Document I/O contracts.

## Governance Audit
- **Compliance:** Rule 1 & Rule 71 enforced.
- **Language:** Technical English.
"""

README_MD_TEMPLATE = """# 🛠️ {name_human}

{description}

## Category: {category}

## 📋 Standard Structure
This skill follows the `skill-creator` institutional standard.

## 🚀 Usage
Refer to `SKILL.md` for procedural logic or the scripts in `/scripts/` for technical execution.
"""

def standardize_skill(skill_data, base_dir):
    skill_path = Path(base_dir) / 'skills' / skill_data['path']
    skill_name = skill_data['name']
    name_human = skill_name.replace('-', ' ').title()
    
    # 1. Ensure Directory Structure
    skill_path.mkdir(parents=True, exist_ok=True)
    scripts_path = skill_path / 'scripts'
    scripts_path.mkdir(exist_ok=True)
    
    init_py = scripts_path / '__init__.py'
    if not init_py.exists():
        init_py.touch()
        print(f"  [+] Created {init_py.relative_to(base_dir)}")

    # 2. SKILL.md
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        content = SKILL_MD_TEMPLATE.format(
            name=skill_name,
            name_human=name_human,
            description=skill_data['description'],
            category=skill_data['category'],
            tags=json.dumps(skill_data.get('tags', []))
        )
        skill_md.write_text(content)
        print(f"  [+] Created {skill_md.relative_to(base_dir)}")

    # 3. README.md
    readme_md = skill_path / 'README.md'
    if not readme_md.exists():
        content = README_MD_TEMPLATE.format(
            name_human=name_human,
            description=skill_data['description'],
            category=skill_data['category']
        )
        readme_md.write_text(content)
        print(f"  [+] Created {readme_md.relative_to(base_dir)}")

def main():
    base_dir = Path(__file__).parent.parent.parent.parent.parent.resolve()
    manifest_path = base_dir / 'skills' / 'manifest_skills.json'
    
    if not manifest_path.exists():
        print(f"ERROR: Manifest not found at {manifest_path}")
        return

    with open(manifest_path, 'r') as f:
        manifest = json.load(f)

    print(f"🚀 Starting Mass Standardization of {len(manifest['skills'])} skills...")
    for skill in manifest['skills']:
        print(f"[*] Processing {skill['name']}...")
        standardize_skill(skill, base_dir)
    print("✅ Standardization complete.")

if __name__ == "__main__":
    main()
