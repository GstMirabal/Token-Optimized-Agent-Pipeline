"""Generates skills/manifest_skills.json from SKILL.md frontmatter.

Single source of truth: each skill's SKILL.md frontmatter (name/description).
Curated fields the frontmatter doesn't carry (category, tags) are preserved
from the existing manifest when present, defaulting for new skills.

Run from the .agents root:  python3 skills/mass-standardizer/scripts/generate_manifest.py
CI regenerates and fails on diff, so hand-editing the manifest is pointless.
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

SKILLS_DIR = Path("skills")
MANIFEST = SKILLS_DIR / "manifest_skills.json"


def parse_frontmatter(skill_md: Path) -> dict:
    """Minimal YAML reader for name/description, tolerating multi-line
    (indent-continued) description values."""
    text = skill_md.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return {}
    fields = {}
    current = None
    for line in m.group(1).splitlines():
        km = re.match(r"^(name|description):\s*(.*)$", line)
        if km:
            current = km.group(1)
            fields[current] = km.group(2).strip().strip('"')
        elif re.match(r"^(\w+):", line):
            current = None  # other key, stop appending
        elif current and line.startswith((" ", "\t")):
            fields[current] = (fields[current] + " " + line.strip()).strip()
    return {k: v for k, v in fields.items() if v}


def main() -> int:
    if not SKILLS_DIR.is_dir():
        print(f"❌ Run from the .agents root ({SKILLS_DIR} not found).", file=sys.stderr)
        return 1

    previous = {}
    if MANIFEST.exists():
        for entry in json.loads(MANIFEST.read_text()).get("skills", []):
            previous[entry["path"]] = entry

    skills = []
    for skill_dir in sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir()):
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            print(f"⚠️ {skill_dir.name}: no SKILL.md, skipped.", file=sys.stderr)
            continue
        fm = parse_frontmatter(skill_md)
        if "name" not in fm or "description" not in fm:
            print(f"❌ {skill_dir.name}: SKILL.md missing name/description frontmatter.",
                  file=sys.stderr)
            return 1
        old = previous.get(skill_dir.name, {})
        skills.append({
            "name": fm["name"],
            "path": skill_dir.name,
            "description": fm["description"],
            "category": old.get("category", "Uncategorized"),
            "tags": old.get("tags", []),
        })

    manifest = {
        "version": json.loads(MANIFEST.read_text())["version"] if MANIFEST.exists() else "1.0.0",
        "updated_at": str(date.today()),
        "_generated_by": "skills/mass-standardizer/scripts/generate_manifest.py — do not edit by hand",
        "skills": skills,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    print(f"✅ Manifest regenerated: {len(skills)} skills.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
