#!/usr/bin/env python3
"""Batch-normalizes `skills/` against the Three-File Skill Standard (`agents.md §3`).

Framework-scoped: the root is this file's repository, never the caller's
directory. It climbed **five** `.parent` levels where four are correct, so
`manifest_skills.json` was looked up one directory *above* the framework and the
auditor `agents.md §3 enforcement` calls official could not run at all — not from
the nucleus root, not from anywhere else. It then reported that failure on stdout
and returned exit `0`, so any caller reading the status code was told the
standardization had succeeded.

A skill that vendors its own nested `SKILL.md` is **pointed at, never scaffolded
over**: whatever sits at the skill's root is what `generate_manifest.py` and
Claude Code's discovery both read, so a stub there is what the whole framework
gets instead of the skill. The vendored file itself is never written to
(`rules/skills_and_integrations.md §3`), and neither is any root file this
script did not itself produce — see `render_skill_md` for why that distinction
had to be exact rather than approximate.

The third defect was invisible while the second one hid it, and only a live run
exposed it: `scripts/` was created for **every** skill in the manifest, so this
auditor violated the standard it exists to enforce — `agents.md §3` prohibits
padding a knowledge skill with empty scaffolding, and the first run that reached
this library added it to 11 of them. Executable and knowledge skills are now
told apart before anything is written, by the same criterion the rule uses.

invoked_by: human:skills/mass-standardizer/README.md
"""
import json
import os
import sys
from pathlib import Path

# Locating `_root.py` is the one path this module must spell itself; the root it
# reports is then `agents_root()`'s single definition rather than a sixth local
# copy. A wrong level here raises ImportError instead of silently resolving to
# the wrong tree, which is the defect this file carried.
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from _root import agents_root  # noqa: E402

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
This skill follows the `skill-creator` standard.

## 🚀 Usage
Refer to `SKILL.md` for procedural logic or the scripts in `/scripts/` for technical execution.
"""

def render_skill_md(skill_data: dict) -> str:
    """Exactly what this script would write for a skill that has no `SKILL.md`.

    Rendered rather than pattern-matched, because it is also the **licence to
    delete**: a root file byte-identical to this string is one nobody has
    touched since this script produced it, and nothing else qualifies. The first
    attempt at `C4` tested for the template's `(Automatic scaffolding)` sentence
    instead and deleted `skills/django-expert-3rd/SKILL.md`, which carried that
    sentence in its Technical Logic section *and* three authored directives in
    its Procedures section — among them the mandate that `RA-02` states. A
    substring cannot tell generated from generated-then-edited; the whole file
    can.

    Args:
        skill_data: One `manifest_skills.json` entry.

    Returns:
        str: The rendered scaffold.
    """
    skill_name = skill_data['name']
    return SKILL_MD_TEMPLATE.format(
        name=skill_name,
        name_human=skill_name.replace('-', ' ').title(),
        description=skill_data['description'],
        category=skill_data['category'],
        tags=json.dumps(skill_data.get('tags', []))
    )


def vendored_skill_md(skill_path: Path) -> Path | None:
    """The `SKILL.md` a third-party skill ships *below* its own root.

    `is_file()` is the guard that keeps a dangling symlink out: pointing the
    root at one would produce a `SKILL.md` that resolves to nothing while this
    script reported success, and `generate_manifest.py` would then drop the
    skill from the manifest without saying why.

    Args:
        skill_path: The skill's directory inside `skills/`.

    Returns:
        Path | None: The shallowest nested file, ties broken alphabetically, or
            `None` when the skill vendors none. One skill in this library
            vendors one, so the ordering has no real case to decide yet and is
            fixed only so that repeated runs agree.
    """
    nested = sorted((p for p in skill_path.rglob('SKILL.md')
                     if p.parent != skill_path and p.is_file()),
                    key=lambda p: (len(p.relative_to(skill_path).parts), p))
    return nested[0] if nested else None


def point_at_vendored(skill_md: Path, vendored: Path, scaffold: str, base_dir: Path) -> None:
    """Make a skill's root `SKILL.md` resolve to the vendored one it shadowed.

    A symlink rather than a copied frontmatter block: `generate_manifest.py`
    reads `<skill>/SKILL.md` and Claude Code discovers by that same path, so both
    then read the vendored content, and no second copy of the description exists
    to drift out of step (`RA-14`).

    **Only this script's own untouched output is ever deleted.** Anything else
    is reported and left exactly where it is, because a root file that is not
    scaffolding is content somebody wrote, and `agents.md §2 destructive_flags`
    reserves that decision for a human.

    Args:
        skill_md: The skill's root `SKILL.md`, present or not.
        vendored: The nested file it must point at.
        scaffold: What this script would have written here, from
            `render_skill_md`.
        base_dir: The framework root, for relative reporting.

    Returns:
        None.
    """
    target = Path(os.path.relpath(vendored, skill_md.parent))
    if skill_md.is_symlink():
        if Path(os.readlink(skill_md)) == target:
            return
        skill_md.unlink()
    elif skill_md.exists():
        if skill_md.read_text() != scaffold:
            print(f"  [!] {skill_md.relative_to(base_dir)} is not this script's scaffolding "
                  f"and shadows {target} — left untouched, resolve by hand.")
            return
        skill_md.unlink()
    skill_md.symlink_to(target)
    print(f"  [+] {skill_md.relative_to(base_dir)} -> {target}")


def is_executable_skill(skill_path: Path) -> bool:
    """Does this skill ship a `/scripts/` folder?

    `agents.md §3 three_file_standard` defines an executable skill by exactly
    that, and states that padding a knowledge skill with empty scaffolding is
    PROHIBITED noise. So this is a **read, never a create**. The previous
    version called `mkdir()` on `scripts/` unconditionally, which made every
    skill executable by the act of asking: measured on the first run that
    reached this library, it wrote an empty `scripts/__init__.py` into **11**
    knowledge skills and a template `README.md` into 9 of them.

    Args:
        skill_path: The skill's directory inside `skills/`.

    Returns:
        bool: True when the skill already ships `scripts/`.
    """
    return (skill_path / 'scripts').is_dir()


def ensure_skill_md(skill_path: Path, skill_data: dict, base_dir: Path) -> None:
    """Guarantee a root `SKILL.md`, pointing at a vendored one where it exists.

    Args:
        skill_path: The skill's directory inside `skills/`.
        skill_data: One `manifest_skills.json` entry.
        base_dir: The framework root, for relative reporting.

    Returns:
        None.
    """
    skill_md = skill_path / 'SKILL.md'
    scaffold = render_skill_md(skill_data)
    vendored = vendored_skill_md(skill_path)
    if vendored is not None:
        point_at_vendored(skill_md, vendored, scaffold, base_dir)
        return
    if skill_md.exists():
        return

    skill_md.write_text(scaffold)
    print(f"  [+] Created {skill_md.relative_to(base_dir)}")


def standardize_skill(skill_data: dict, base_dir: Path) -> None:
    """Inject whatever the Three-File Standard requires and this skill lacks.

    A knowledge skill needs its `SKILL.md` and nothing else; the `/scripts/`
    package and `README.md` are required of **executable** skills alone
    (`agents.md §3`).

    Args:
        skill_data: One `manifest_skills.json` entry.
        base_dir: The framework root.

    Returns:
        None.
    """
    skill_path = Path(base_dir) / 'skills' / skill_data['path']
    executable = is_executable_skill(skill_path)
    skill_path.mkdir(parents=True, exist_ok=True)

    ensure_skill_md(skill_path, skill_data, base_dir)
    if not executable:
        return

    init_py = skill_path / 'scripts' / '__init__.py'
    if not init_py.exists():
        init_py.touch()
        print(f"  [+] Created {init_py.relative_to(base_dir)}")

    readme_md = skill_path / 'README.md'
    if not readme_md.exists():
        skill_name = skill_data['name']
        readme_md.write_text(README_MD_TEMPLATE.format(
            name_human=skill_name.replace('-', ' ').title(),
            description=skill_data['description'],
            category=skill_data['category']
        ))
        print(f"  [+] Created {readme_md.relative_to(base_dir)}")


def main() -> int:
    """Standardize every skill the manifest lists.

    Returns:
        int: `0` when every skill was processed, `1` when the manifest file is
            absent. Previously that path printed its error and returned `0`, so
            a caller reading the status code was told the run had succeeded. A
            manifest that exists but is malformed still raises, deliberately:
            the file is generated by `generate_manifest.py` and checked by
            `check_manifest_parity.py`, so a corrupt one is a broken repository
            rather than a condition this script should absorb.
    """
    base_dir = agents_root()
    manifest_path = base_dir / 'skills' / 'manifest_skills.json'

    if not manifest_path.exists():
        print(f"ERROR: Manifest not found at {manifest_path}")
        return 1

    manifest = json.loads(manifest_path.read_text())

    print(f"🚀 Starting Mass Standardization of {len(manifest['skills'])} skills...")
    for skill in manifest['skills']:
        print(f"[*] Processing {skill['name']}...")
        standardize_skill(skill, base_dir)
    print("✅ Standardization complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
