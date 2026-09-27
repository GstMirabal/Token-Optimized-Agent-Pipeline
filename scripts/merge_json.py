"""Non-destructive JSON merge.

Adds a template's keys into a destination JSON file without overwriting
anything the host project already defined. Used to merge
claude/settings.hooks.json -> host .claude/settings.json and claude/mcp.json
-> host .mcp.json.

invoked_by: scripts/install.py (import; non-destructive settings/mcp merge).
"""
import json
import sys
from pathlib import Path
from typing import Any

# Hook command strings shipped by PREVIOUS template versions. Pruned from the
# destination before merging so a re-install upgrades them instead of leaving
# a stale duplicate alongside the new guarded variant (list-merge only appends).
DEPRECATED_HOOK_COMMANDS = {
    "python3 .agents/hooks/on_init.py",
    "python3 .agents/hooks/on_commit.py",
    "python3 .agents/hooks/state_mirror.py",
}


def _prune_matcher_hooks(matcher: dict) -> None:
    """Strips deprecated hook commands from a single settings.json matcher, in place.

    Args:
        matcher: One entry of a `hooks.<event>` list (a `{"hooks": [...]}` dict).
    """
    hooks = matcher.get("hooks")
    if isinstance(hooks, list):
        matcher["hooks"] = [
            h for h in hooks
            if h.get("command") not in DEPRECATED_HOOK_COMMANDS
        ]


def prune_deprecated_hooks(dest: dict) -> None:
    """Removes hook entries owned by older .agents templates from a settings dict."""
    for event, matchers in list(dest.get("hooks", {}).items()):
        if not isinstance(matchers, list):
            continue
        for matcher in matchers:
            _prune_matcher_hooks(matcher)
        dest["hooks"][event] = [m for m in matchers if m.get("hooks")]
        if not dest["hooks"][event]:
            del dest["hooks"][event]


def _merge_list_append(dest_list: list, value_list: list) -> None:
    """Appends template list items not already present, into dest_list in place.

    Args:
        dest_list: Destination list being appended to, in place.
        value_list: Template list whose new items should be appended.
    """
    for item in value_list:
        if item not in dest_list:
            dest_list.append(item)


def _merge_value(dest: dict, key: str, value: Any) -> None:
    """Merges a single template value into dest[key], in place, per its JSON kind.

    Args:
        dest: Destination mapping being merged into, in place.
        key: The key being merged.
        value: The template's value for key.
    """
    if key not in dest:
        dest[key] = value
        return
    if isinstance(dest[key], dict) and isinstance(value, dict):
        merge(dest[key], value)
        return
    if isinstance(dest[key], list) and isinstance(value, list):
        _merge_list_append(dest[key], value)
    # else: host already has a conflicting scalar value here -> leave it alone.


def merge(dest: dict, template: dict) -> dict:
    """Non-destructively merges template's keys into dest, recursing into dicts."""
    for key, value in template.items():
        _merge_value(dest, key, value)
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
