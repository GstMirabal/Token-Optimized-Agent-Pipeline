"""Lint commands/*.md against workflows and the slash-commands guide.

Real Claude Code / Cursor discover commands by scanning the bridged directories —
there is no generation step anymore (this used to emit fictional .ts skill stubs).
What still matters is keeping ``commands/*.md`` in sync with ``workflows/*.md``
and with ``docs/guides/AGENTS_SLASH_COMMANDS_GUIDE.md`` §3.2, so this script is a
lint check, not a generator.

invoked_by: Makefile `verify` target, audit_workflow.md#link_audit.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

COMMANDS_DIR = Path("commands")
WORKFLOW_DIR = Path("workflows")
GUIDE_PATH = Path("docs/guides/AGENTS_SLASH_COMMANDS_GUIDE.md")
REFERENCE_REGEX = r"@\.agents/(workflows/[\w\-./]+\.md)"
# §3.2 tables use **`/agents:stem`** — require every commands/*.md stem to appear.
GUIDE_COMMAND_REGEX = re.compile(r"/agents:([\w\-]+)")


def command_stems() -> set[str]:
    """Basenames of ``commands/*.md`` without the ``.md`` suffix."""
    return {path.stem for path in COMMANDS_DIR.glob("*.md")}


def guide_named_stems(text: str) -> set[str]:
    """Command stems named in the guide body (typically §3.2 tables)."""
    return set(GUIDE_COMMAND_REGEX.findall(text))


def verify() -> bool:
    """Return True when every command link and guide row is consistent."""
    print("🔍 Verifying commands/ <-> workflows/ links...")

    if not COMMANDS_DIR.exists():
        print(f"❌ Error: {COMMANDS_DIR} not found.")
        return False

    broken: list[tuple[str, str]] = []
    for command_file in sorted(COMMANDS_DIR.glob("*.md")):
        content = command_file.read_text(encoding="utf-8")
        match = re.search(REFERENCE_REGEX, content)
        if not match:
            # Not every command must reference a workflow (e.g. graphify.md
            # references a skill).
            continue
        referenced = Path(match.group(1))
        if not referenced.exists():
            broken.append((command_file.name, str(referenced)))

    if broken:
        for cmd, target in broken:
            print(f"❌ {cmd} references missing workflow: {target}")
        return False

    stems = command_stems()
    print(
        f"✅ All command references resolve ({len(stems)} commands checked)."
    )

    if not GUIDE_PATH.exists():
        print(f"❌ Error: {GUIDE_PATH} not found.")
        return False

    guide_text = GUIDE_PATH.read_text(encoding="utf-8")
    named = guide_named_stems(guide_text)
    missing = sorted(stems - named)
    extra = sorted(named - stems)
    if missing or extra:
        print(
            f"❌ {GUIDE_PATH} §3.2 must name every commands/*.md stem "
            "(and no others):"
        )
        for stem in missing:
            print(f"  • missing `/agents:{stem}`")
        for stem in extra:
            print(f"  • guide names `/agents:{stem}` but no commands/{stem}.md")
        return False

    print(
        f"✅ {GUIDE_PATH} names every command stem "
        f"({len(stems)} /agents:* entries)."
    )
    return True


if __name__ == "__main__":
    # Exit 1 keeps historical Makefile behavior; RA-11 exit-2 applies to hooks.
    sys.exit(0 if verify() else 1)
