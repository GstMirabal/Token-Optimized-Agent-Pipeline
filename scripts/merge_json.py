"""Non-destructive JSON merge.

Adds a template's keys into a destination JSON file without overwriting
anything the host project already defined. Used to merge
claude/settings.hooks.json -> host .claude/settings.json and claude/mcp.json
-> host .mcp.json.

invoked_by: scripts/install.py (import; non-destructive settings/mcp merge).

MCP servers are the exception to "non-destructive": a server the template
defines is the template's, so its host entry is replaced whole, and a server
the template retired is removed when its launch is the one the framework
shipped (Hotfix H-008). An additive merge treated `args`, an ordered argv, as a
set, so a host bridged before `246cd20` received `-I` after the module name,
where it isolates nothing.

Hook entries are a second exception (`prune_shipped_hooks`): for each event the
template defines, a host hook entry whose `command` is one the template ships
for that event, or is in DEPRECATED_HOOK_COMMANDS, is removed and the template's
matcher is appended once. Host hook entries with any other command are kept.
"""
import copy
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
    # Pre-W45 SessionStart command (echo names the install.sh shim); W45 retires it.
    "if [ -f .agents/hooks/on_init.py ]; then python3 .agents/hooks/on_init.py; else echo '\u26a0\ufe0f [.agents] hooks unavailable \u2014 initialize the submodule: git submodule update --init .agents && .agents/scripts/install.sh'; fi",
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
# Why all ten retire: on CLI 2.1.119 any excluded entry lets a chained command
# run unsandboxed (QA Gate 1 round 3 N1), so the framework ships no exclusions
# and retires all ten it published on `ai-sprint/055`.
#   - the three `with_env.py graphify-*` entries: a cwd-relative exclusion runs
#     an agent-written impostor script outside the sandbox.
#   - `gh pr create *` / `gh release create *`: they can publish local files.
#   - the five gh inspection patterns: same chaining defect as any exclusion.
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
        "gh pr checks *",
        "gh pr list *",
        "gh repo view *",
        "gh release view *",
        "gh auth status",
    }),
    # KI-056-3: the sixteen per-subtree entries that `d70d00c` replaced with the
    # whole-submodule `./.agents` / `Edit(/.agents/**)`. Pruning them is safe:
    # each is a sub-path of an entry the current template ships and the merge
    # re-appends, and `prune_retired_values` keeps any value the template still
    # ships. `Read(/.env)` and `./.env` are not listed: the template still ships them.
    "permissions.deny": frozenset({
        "Edit(/.agents/scripts/with_env.py)",
        "Edit(/.agents/config/with_env_allowlist.json)",
        "Edit(/.agents/venv_skillopt/**)",
        "Edit(/.agents/hooks/**)",
        "Edit(/.agents/scripts/**)",
        "Edit(/.agents/config/**)",
        "Edit(/.agents/skills/**)",
        "Edit(/.agents/claude/**)",
    }),
    "sandbox.filesystem.denyWrite": frozenset({
        "./.agents/scripts/with_env.py",
        "./.agents/config/with_env_allowlist.json",
        "./.agents/venv_skillopt",
        "./.agents/hooks",
        "./.agents/scripts",
        "./.agents/config",
        "./.agents/skills",
        "./.agents/claude",
    }),
})


# MCP servers the template once shipped and retired, with the launch (command,
# args) it shipped them with. Removed from the host only when the host entry has
# that launch; a host that relaunched a retired name keeps its entry (H-008).
RETIRED_MCP_SERVERS: Mapping[str, tuple[str, tuple[str, ...]]] = MappingProxyType({
    "github-sentinel": ("/bin/bash", (".agents/mcp_servers/github_mcp/scripts/start_mcp.sh",)),
    "git-sync-agent": ("/bin/bash", (".agents/mcp_servers/github_mcp/scripts/start_mcp.sh",)),
})


def _launch(entry: Any) -> tuple[Any, tuple[Any, ...]] | None:
    """Return the launch of an MCP server entry: its command and its args.

    Args:
        entry: One `mcpServers` value from a host file.

    Returns:
        (command, args) when the entry is a mapping, else None.
    """
    if not isinstance(entry, dict):
        return None
    return entry.get("command"), tuple(entry.get("args") or ())


def _retire_mcp_servers(host: dict, shipped: dict) -> list[str]:
    """Remove the retired servers whose host launch is the one the framework shipped.

    Args:
        host: The host `mcpServers` mapping, mutated in place.
        shipped: The template `mcpServers` mapping; a name it still defines is skipped.

    Returns:
        One notice per retired name found in the host, removed or kept.
    """
    notices = []
    for name, launch in RETIRED_MCP_SERVERS.items():
        if name in shipped or name not in host:
            continue
        if _launch(host[name]) == launch:
            del host[name]
            notices.append(f"removed retired MCP server '{name}'")
        else:
            notices.append(f"kept MCP server '{name}': retired, but its launch was changed by the host")
    return notices


def sync_template_mcp_servers(dest: dict, template: dict) -> list[str]:
    """Make every template-defined MCP server equal to the template, in place.

    Args:
        dest: Destination document; its `mcpServers` mapping is mutated.
        template: Template document.

    Returns:
        Notices for each host entry replaced because it differed, and for each
        retired server removed or kept. Empty when the template has no servers.
        When the destination's `mcpServers` is not a mapping it is left as is,
        no template server is added, and the one notice says so.
    """
    shipped = template.get("mcpServers")
    if not isinstance(shipped, dict):
        return []
    host = dest.setdefault("mcpServers", {})
    if not isinstance(host, dict):
        return ["kept host 'mcpServers': not a mapping, so no template MCP server was merged"]
    notices = [
        f"replaced MCP server '{name}' with the template entry"
        for name, entry in shipped.items() if name in host and host[name] != entry
    ]
    for name, entry in shipped.items():
        host[name] = copy.deepcopy(entry)
    return notices + _retire_mcp_servers(host, shipped)


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


def _matcher_commands(matcher: Any) -> set[str]:
    """Collect the string `command` values of one matcher's `hooks` list.

    Args:
        matcher: One entry of a `hooks.<event>` list.

    Returns:
        The commands found; empty when the matcher is not a mapping or has no list.
    """
    hooks = matcher.get("hooks") if isinstance(matcher, dict) else None
    if not isinstance(hooks, list):
        return set()
    return {
        h["command"] for h in hooks
        if isinstance(h, dict) and isinstance(h.get("command"), str)
    }


def _hook_commands(matchers: Any) -> set[str]:
    """Collect the `command` strings of the hook entries in a list of matchers.

    Args:
        matchers: A `hooks.<event>` value; anything but a list yields an empty set.

    Returns:
        The string `command` values found in the matchers' `hooks` lists.
    """
    found: set[str] = set()
    for matcher in matchers if isinstance(matchers, list) else []:
        found |= _matcher_commands(matcher)
    return found


def _drop_commands(matchers: list, commands: set[str]) -> list:
    """Return the matchers without the hook entries whose command is in `commands`.

    A matcher left with no hooks is dropped; a matcher that had none to begin
    with, or any non-mapping item, is kept as found.

    Args:
        matchers: One `hooks.<event>` list from a host file.
        commands: Exact `command` strings to remove.

    Returns:
        A new list of matchers.
    """
    kept = []
    for matcher in matchers:
        hooks = matcher.get("hooks") if isinstance(matcher, dict) else None
        if not isinstance(hooks, list):
            kept.append(matcher)
            continue
        left = [h for h in hooks if not (isinstance(h, dict) and h.get("command") in commands)]
        if left:
            kept.append({**matcher, "hooks": left})
    return kept


def prune_shipped_hooks(dest: dict, template: dict) -> None:
    """Remove from the host the hook entries the template re-adds, in place.

    For each `hooks.<event>` the template defines, a host hook entry is removed
    when its `command` is exactly one the template ships for that event or a
    member of DEPRECATED_HOOK_COMMANDS; matchers left empty and events left
    empty are dropped. Entries with any other command, and events the template
    does not define, are untouched. The tree merge then appends the template
    matchers once, so a changed matcher shape does not leave the old one beside it.

    Args:
        dest: Destination settings dict, mutated in place.
        template: Template settings dict; never mutated.
    """
    shipped = template.get("hooks")
    host = dest.get("hooks")
    if not isinstance(shipped, dict) or not isinstance(host, dict):
        return
    for event, matchers in shipped.items():
        if not isinstance(host.get(event), list):
            continue
        host[event] = _drop_commands(
            host[event], _hook_commands(matchers) | DEPRECATED_HOOK_COMMANDS)
        if not host[event]:
            del host[event]


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
    Hook entries whose command the template ships for the same event are then
    removed from dest (`prune_shipped_hooks`) so the tree merge appends them once.
    Template-defined MCP servers then replace their host entries whole, and
    retired ones are removed (`sync_template_mcp_servers`); each notice is
    printed to stderr.

    Args:
        dest: Destination dict, mutated in place.
        template: Template dict to merge in.
        retired: Retired-value mapping; defaults to RETIRED_VALUES when None.

    Returns:
        The merged dest.
    """
    prune_retired_values(dest, template, retired)
    prune_shipped_hooks(dest, template)
    for notice in sync_template_mcp_servers(dest, template):
        print(f"ℹ️  merge_json: {notice}", file=sys.stderr)
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
