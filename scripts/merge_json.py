"""Non-destructive JSON merge.

Adds a template's keys into a destination JSON file without overwriting
anything the host project already defined. Used by install_claude.sh to merge
claude/settings.hooks.json -> host .claude/settings.json and claude/mcp.json
-> host .mcp.json.
"""
import json
import sys
from pathlib import Path

# Hook command strings shipped by PREVIOUS template versions. Pruned from the
# destination before merging so a re-install upgrades them instead of leaving
# a stale duplicate alongside the new guarded variant (list-merge only appends).
DEPRECATED_HOOK_COMMANDS = {
    "python3 .agents/hooks/on_init.py",
    "python3 .agents/hooks/on_commit.py",
    "python3 .agents/hooks/state_mirror.py",
}


def prune_deprecated_hooks(dest: dict) -> None:
    """Removes hook entries owned by older .agents templates from a settings dict."""
    for event, matchers in list(dest.get("hooks", {}).items()):
        if not isinstance(matchers, list):
            continue
        for matcher in matchers:
            hooks = matcher.get("hooks")
            if isinstance(hooks, list):
                matcher["hooks"] = [
                    h for h in hooks
                    if h.get("command") not in DEPRECATED_HOOK_COMMANDS
                ]
        dest["hooks"][event] = [m for m in matchers if m.get("hooks")]
        if not dest["hooks"][event]:
            del dest["hooks"][event]


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
    if "hooks" in template:
        prune_deprecated_hooks(dest)
    merged = merge(dest, template)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(json.dumps(merged, indent=2) + "\n")
    print(f"✅ Merged {template_path} -> {dest_path}")


if __name__ == "__main__":
    main()
