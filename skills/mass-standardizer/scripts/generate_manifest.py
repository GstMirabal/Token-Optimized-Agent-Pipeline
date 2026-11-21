"""Generates skills/manifest_skills.json from SKILL.md frontmatter.

Single source of truth: each skill's SKILL.md frontmatter (name/description).
Curated fields the frontmatter doesn't carry (category, tags) are preserved
from the existing manifest when present, defaulting for new skills.

Run from the .agents root:  python3 skills/mass-standardizer/scripts/generate_manifest.py
CI regenerates and fails on diff, so hand-editing the manifest is pointless.

Check mode (writes nothing):  python3 skills/mass-standardizer/scripts/generate_manifest.py --check
Compares the exact text a normal run would write with the bytes of the manifest.
Exit 0 when identical; exit 2 when they differ, the manifest is missing, or it is
not valid JSON; exit 1 when run from the wrong directory or a SKILL.md lacks
name/description, as in the normal mode.
"""
import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

SKILLS_DIR = Path("skills")
MANIFEST = SKILLS_DIR / "manifest_skills.json"


def _apply_frontmatter_line(line: str, fields: dict, current: str | None) -> str | None:
    """Applies one frontmatter line to `fields`, mutating it in place.

    Args:
        line: One raw line from the frontmatter block.
        fields: The fields dict accumulated so far; mutated in place.
        current: The key currently accepting continuation lines, or None.

    Returns:
        The key that should accept the next continuation line, or None.
    """
    km = re.match(r"^(name|description):\s*(.*)$", line)
    if km:
        current = km.group(1)
        fields[current] = km.group(2).strip().strip('"')
        return current
    if re.match(r"^(\w+):", line):
        return None  # other key, stop appending
    if current and line.startswith((" ", "\t")):
        fields[current] = (fields[current] + " " + line.strip()).strip()
    return current


def parse_frontmatter(skill_md: Path) -> dict:
    """Minimal YAML reader for name/description, tolerating multi-line
    (indent-continued) description values."""
    text = skill_md.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    fields = {}
    current = None
    for line in m.group(1).splitlines():
        current = _apply_frontmatter_line(line, fields, current)
    return {k: v for k, v in fields.items() if v}


def build_manifest() -> dict | None:
    """Builds the manifest dict from the SKILL.md files, without writing it.

    Returns:
        The manifest dict, or None after printing an error to stderr when a
        SKILL.md lacks the name/description frontmatter.
    """
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
            return None
        old = previous.get(skill_dir.name, {})
        skills.append({
            "name": fm["name"],
            "path": skill_dir.name,
            "description": fm["description"],
            "category": old.get("category", "Uncategorized"),
            "tags": old.get("tags", []),
        })

    # updated_at must be DETERMINISTIC: it only advances when the skill payload
    # actually changes. Stamping today's date unconditionally turns the CI
    # regenerate-and-diff check into a time bomb that fails at midnight.
    existing = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    unchanged = existing.get("skills") == skills
    today = str(datetime.now().astimezone().date())
    return {
        "version": existing.get("version", "1.0.0"),
        "updated_at": existing.get("updated_at", today) if unchanged else today,
        "_generated_by": "skills/mass-standardizer/scripts/generate_manifest.py — do not edit by hand",
        "skills": skills,
    }


def render_manifest(manifest: dict) -> str:
    """Renders the exact text a normal run writes to the manifest file.

    Args:
        manifest: The manifest dict from `build_manifest`.

    Returns:
        The JSON text, indented, with a trailing newline.
    """
    return json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"


def manifest_is_readable() -> bool:
    """Reports whether the manifest exists and holds a JSON object, writing nothing.

    Returns:
        True when the manifest can be read as a JSON object; False after printing
        one line to stderr naming the manifest and the generator.
    """
    try:
        loaded = json.loads(MANIFEST.read_bytes().decode("utf-8"))
        if not isinstance(loaded, dict):
            raise TypeError("top level is not a JSON object")
    except (OSError, ValueError, TypeError) as exc:
        print(f"❌ {MANIFEST} is missing or invalid ({exc}); "
              "run generate_manifest.py without --check.", file=sys.stderr)
        return False
    return True


def check_manifest() -> int:
    """Compares the manifest bytes with a fresh render; never writes.

    Returns:
        0 when identical, 2 when they differ or the manifest is unreadable,
        1 when a SKILL.md lacks name/description frontmatter.
    """
    if not manifest_is_readable():
        return 2
    manifest = build_manifest()
    if manifest is None:
        return 1
    if MANIFEST.read_bytes() != render_manifest(manifest).encode("utf-8"):
        print(f"❌ {MANIFEST} is out of date; run "
              "python3 skills/mass-standardizer/scripts/generate_manifest.py",
              file=sys.stderr)
        return 2
    print(f"✅ Manifest up to date: {len(manifest['skills'])} skills.")
    return 0


def main() -> int:
    """Regenerates the manifest, or only verifies it under --check.

    Returns:
        The process exit code.
    """
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true",
                        help="compare the manifest with a fresh render; write nothing")
    args = parser.parse_args()
    if not SKILLS_DIR.is_dir():
        print(f"❌ Run from the .agents root ({SKILLS_DIR} not found).", file=sys.stderr)
        return 1
    if args.check:
        return check_manifest()
    manifest = build_manifest()
    if manifest is None:
        return 1
    MANIFEST.write_text(render_manifest(manifest))
    print(f"✅ Manifest regenerated: {len(manifest['skills'])} skills.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
