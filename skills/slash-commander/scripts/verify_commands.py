import re
import sys
from pathlib import Path

# Configuration
COMMANDS_DIR = Path("commands")
WORKFLOW_DIR = Path("workflows")
REFERENCE_REGEX = r"@\.agents/(workflows/[\w\-./]+\.md)"


def verify() -> bool:
    """Checks that every commands/*.md file references a workflow that actually exists.

    Real Claude Code discovers commands/skills/agents by scanning .claude/ directly —
    there is no generation step anymore (this used to emit fictional .ts skill stubs).
    What still matters is keeping commands/*.md in sync with workflows/*.md, so this
    script is a lint check, not a generator.
    """
    print("🔍 Verifying commands/ <-> workflows/ links...")

    if not COMMANDS_DIR.exists():
        print(f"❌ Error: {COMMANDS_DIR} not found.")
        return False

    broken = []
    for command_file in sorted(COMMANDS_DIR.glob("*.md")):
        content = command_file.read_text()
        match = re.search(REFERENCE_REGEX, content)
        if not match:
            # Not every command must reference a workflow (e.g. graphify.md references a skill).
            continue
        referenced = Path(match.group(1))
        if not referenced.exists():
            broken.append((command_file.name, str(referenced)))

    if broken:
        for cmd, target in broken:
            print(f"❌ {cmd} references missing workflow: {target}")
        return False

    print(f"✅ All command references resolve ({len(list(COMMANDS_DIR.glob('*.md')))} commands checked).")
    return True


if __name__ == "__main__":
    sys.exit(0 if verify() else 1)
