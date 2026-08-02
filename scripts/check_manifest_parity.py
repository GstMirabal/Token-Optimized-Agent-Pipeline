"""Verify skills/manifest_skills.json lists exactly the directories in skills/.

The manifest is the static routing table the Orchestrator reads instead of
crawling `skills/` (rules/token_economy.md §2). A manifest that has drifted
from the tree routes an agent to a skill that no longer exists, or hides one
that does — both fail silently at the moment an agent needs the tool.

invoked_by: Makefile `verify` target (and therefore .github/workflows/ci.yml,
which invokes `make verify`). Extracted from a CI-inline heredoc so the same
check can run locally — a check that only exists inside CI cannot be run where
the decision to push is made (RA-16, agents.md §7).

Usage:
    python3 scripts/check_manifest_parity.py

Exit codes:
    0 — manifest and tree agree
    1 — drift found, listed on stdout
"""

import json
import sys
from pathlib import Path

SKILLS_DIR = Path("skills")
MANIFEST = SKILLS_DIR / "manifest_skills.json"


def main() -> int:
    if not MANIFEST.exists():
        print(f"❌ {MANIFEST} not found — run from the .agents root.")
        return 1

    listed = {entry["path"] for entry in json.loads(MANIFEST.read_text())["skills"]}
    on_disk = {p.name for p in SKILLS_DIR.iterdir() if p.is_dir()}

    missing = sorted(listed - on_disk)
    unlisted = sorted(on_disk - listed)

    if missing or unlisted:
        print("❌ Manifest/tree parity broken:")
        if missing:
            print(f"  listed in manifest, absent from tree: {missing}")
        if unlisted:
            print(f"  present in tree, absent from manifest: {unlisted}")
        return 1

    print(f"✅ Manifest parity OK ({len(listed)} skills).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
