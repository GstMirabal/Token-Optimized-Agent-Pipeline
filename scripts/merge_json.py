"""Non-destructive JSON merge.

Adds a template's keys into a destination JSON file without overwriting
anything the host project already defined. Used to merge
claude/settings.hooks.json -> host .claude/settings.json and claude/mcp.json
-> host .mcp.json.

invoked_by: scripts/install.py (import; non-destructive settings/mcp merge).
"""
import json
import sys
from collections.abc import Mapping
from pathlib import Path
from types import MappingProxyType
from typing import Any

# Hook command strings shipped by PREVIOUS template versions. Pruned from the
# destination before merging so a re-install upgrades them instead of leaving
# a stale duplicate alongside the new guarded variant (list-merge only appends).
DEPRECATED_HOOK_COMMANDS = {
    "python3 .agents/hooks/on_init.py",
    "python3 .agents/hooks/on_commit.py",
    "python3 .agents/hooks/state_mirror.py",
}

# String values shipped by PREVIOUS template versions and since retired, keyed
# by the dotted JSON path of the list that held them.
# Pruned from the destination list on every merge (list-merge only appends, so
# a dangerous entry retired from a published template would otherwise survive
# on every host forever). Exact string match only; a value the current template
# still ships is kept; entries the host added are never touched.
# Why these five retire:
#   - the three `with_env.py graphify-*` entries: a cwd-relative exclusion runs
#     an agent-written impostor script outside the sandbox.
#   - `gh pr create *` / `gh release create *`: they can publish local files.
# Caveat (R2-8): exact-match pruning cannot tell a host's deliberate re-add of
# a retired string from a stale leftover, so a host that wants such an entry
# loses it on each re-merge and must use a different string.
RETIRED_VALUES: Mapping[str, frozenset[str]] = MappingProxyType({
    "sandbox.excludedCommands": frozenset({
        "python3 -I .agents/scripts/with_env.py graphify-extract",
        "python3 -I .agents/scripts/with_env.py graphify-extract-deep",
        "python3 -I .agents/scripts/with_env.py graphify-label",
        "gh pr create *",
        "gh release create *",
    }),
})


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


def _get_path(data: Any, path: str) -> Any:
    """Walks a dotted key path through nested dicts.

    Args:
        data: Root mapping to descend into.
        path: Dotted key path such as "sandbox.filesystem.denyRead".

    Returns:
        The value at path, or None when any segment is missing or not a dict.
    """
    for part in path.split("."):
        if not isinstance(data, dict) or part not in data:
            return None
        data = data[part]
    return data


def prune_retired_values(
    dest: dict,
    template: dict,
    retired: Mapping[str, frozenset[str]] | None = None,
) -> None:
    """Removes retired template strings from the destination lists, in place.

    A value is removed only when it is a string exactly equal to a member of
    the retired set for that list path. The current template wins: a retired
    value the template still ships at the same path is kept.

    Args:
        dest: Destination settings dict, mutated in place.
        template: Template dict about to be merged; its values are never pruned.
        retired: Mapping of dotted list path to retired strings. Defaults to
            RETIRED_VALUES when None.
    """
    mapping = RETIRED_VALUES if retired is None else retired
    for path, values in mapping.items():
        target = _get_path(dest, path)
        if not isinstance(target, list):
            continue
        shipped = _get_path(template, path)
        keep = set(shipped) if isinstance(shipped, list) else set()
        target[:] = [
            item for item in target
            if not (isinstance(item, str) and item in values and item not in keep)
        ]


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
        _merge_tree(dest[key], value)
        return
    if isinstance(dest[key], list) and isinstance(value, list):
        _merge_list_append(dest[key], value)
    # else: host already has a conflicting scalar value here -> leave it alone.


def _merge_tree(dest: dict, template: dict) -> dict:
    """Recursive append-only merge of template into dest, in place."""
    for key, value in template.items():
        _merge_value(dest, key, value)
    return dest


def merge(
    dest: dict,
    template: dict,
    retired: Mapping[str, frozenset[str]] | None = None,
) -> dict:
    """Non-destructively merges template's keys into dest, recursing into dicts.

    Retired template values are pruned from dest first (`prune_retired_values`),
    so every caller, including `install.merge_into`, upgrades on re-install.

    Args:
        dest: Destination dict, mutated in place.
        template: Template dict to merge in.
        retired: Retired-value mapping; defaults to RETIRED_VALUES when None.

    Returns:
        The merged dest.
    """
    prune_retired_values(dest, template, retired)
    return _merge_tree(dest, template)


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
