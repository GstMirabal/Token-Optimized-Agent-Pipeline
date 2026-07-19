"""Non-destructive JSON merge.

Adds a template's keys into a destination JSON file without overwriting
anything the host project already defined. Used by install_claude.sh to merge
claude/settings.hooks.json -> host .claude/settings.json and claude/mcp.json
-> host .mcp.json.
"""
import json
import sys
from pathlib import Path


def merge(dest: dict, template: dict) -> dict:
    for key, value in template.items():
        if key not in dest:
            dest[key] = value
        elif isinstance(dest[key], dict) and isinstance(value, dict):
            merge(dest[key], value)
        elif isinstance(dest[key], list) and isinstance(value, list):
            for item in value:
                if item not in dest[key]:
                    dest[key].append(item)
        # else: host already has a conflicting scalar value here -> leave it alone.
    return dest


def main() -> None:
    template_path, dest_path = Path(sys.argv[1]), Path(sys.argv[2])
    template = json.loads(template_path.read_text())
    dest = json.loads(dest_path.read_text()) if dest_path.exists() else {}
    merged = merge(dest, template)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(json.dumps(merged, indent=2) + "\n")
    print(f"✅ Merged {template_path} -> {dest_path}")


if __name__ == "__main__":
    main()
