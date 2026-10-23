"""Guards what the template claude/mcp.json launches (Sprint 056, D12, Q3; Hotfix H-007).

install.py merges the template into every host's .mcp.json, cursor_adapter.py
derives .cursor/mcp.json from it, and Claude Code launches each MCP server
outside the sandbox with the host root as working directory. A Python server
started with `-m` and without `-I` puts that working directory first on
sys.path, so a host-root package named like the served module (`graphify/`)
shadows the installed one and runs unsandboxed (SANDBOX_ENUMERATION.md E10). A
server that fetches a package from a registry at launch runs whatever the
registry serves, unsandboxed (H-007).

What `test_template_equals_reviewed_copy` proves, and no more (agents.md §1
`fail_closed_claims`): the template, parsed with duplicate keys rejected, is
equal to `REVIEWED_TEMPLATE`, so any change to a key, server or value fails
until the reviewed copy is changed in the same commit, where a reviewer sees it.
It does not judge the reviewed copy itself. It does not cover what install.py
writes into a host `.mcp.json` that already holds an entry of the same name
(the merge is not a copy), nor the code a server runs: `graphify.serve` comes
from `graphifyy`, whose top-level version is pinned in requirements-core.txt
while its dependencies are not.
"""
import copy
import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "claude" / "mcp.json"

# The template as reviewed in Hotfix H-007. Change it only together with
# claude/mcp.json, and only after reviewing what the new entry launches.
REVIEWED_TEMPLATE: dict[str, Any] = {
    "mcpServers": {
        "graphify": {
            "command": ".agents/venv_skillopt/bin/python",
            "args": ["-I", "-m", "graphify.serve", "graphify-out/graph.json"],
            "description": "Graphify Knowledge Graph MCP Server",
        },
    },
}

# The template before H-007 (d463055), kept as a rejected case.
PRE_H007_SERVER: dict[str, Any] = {
    "command": "/bin/bash",
    "args": [".agents/mcp_servers/github_mcp/scripts/start_mcp.sh"],
    "env": {},
    "description": "Git Security and Audit Filter - Git Sync Auditor",
}


def _unique_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Build a JSON object, refusing a key that appears twice.

    Args:
        pairs: The key/value pairs of one JSON object, in document order.

    Returns:
        The object as a dict.

    Raises:
        ValueError: If a key is repeated; parsers keep one of the two silently.
    """
    keys = [key for key, _ in pairs]
    duplicates = sorted({key for key in keys if keys.count(key) > 1})
    if duplicates:
        raise ValueError(f"duplicate JSON keys: {duplicates}")
    return dict(pairs)


def _template() -> dict[str, Any]:
    """Return the template as shipped.

    Returns:
        The parsed content of `claude/mcp.json`, duplicate keys rejected.
    """
    return json.loads(TEMPLATE.read_text(encoding="utf-8"), object_pairs_hook=_unique_keys)


def _is_reviewed(template: dict[str, Any]) -> bool:
    """Tell whether a template is exactly the reviewed copy.

    Args:
        template: A parsed `mcp.json` document.

    Returns:
        bool: True only when the whole document equals `REVIEWED_TEMPLATE`.
    """
    return template == REVIEWED_TEMPLATE


def _python_servers() -> list[tuple[str, dict[str, Any]]]:
    """Return the template servers whose command is a Python interpreter path.

    Returns:
        (name, server) pairs whose command ends with `/python` or `/python3`.
    """
    return [
        (name, server) for name, server in _template()["mcpServers"].items()
        if server["command"].endswith(("/python", "/python3"))
    ]


def test_template_has_a_python_server() -> None:
    """The guard below is not vacuous: the template ships at least one Python server."""
    assert _python_servers()


@pytest.mark.parametrize("name,server", _python_servers())
def test_python_server_runs_isolated(name: str, server: dict[str, Any]) -> None:
    """Every Python MCP server passes `-I` as its first interpreter argument."""
    assert server["args"][:1] == ["-I"], name


def test_template_equals_reviewed_copy() -> None:
    """The shipped template is exactly the reviewed copy (H-007)."""
    assert _is_reviewed(_template())


def _graphify(template: dict[str, Any]) -> dict[str, Any]:
    """Return the reviewed server entry of a template copy, for mutation.

    Args:
        template: A copy of `REVIEWED_TEMPLATE`.

    Returns:
        Its `graphify` server entry.
    """
    return template["mcpServers"]["graphify"]


MUTATIONS: dict[str, Callable[[dict[str, Any]], None]] = {
    "pre-H-007 server": lambda t: t["mcpServers"].update({"git-sync-agent": PRE_H007_SERVER}),
    "extra server": lambda t: t["mcpServers"].update(
        {"x": {"command": "docker", "args": ["run", "-i", "--rm", "ghcr.io/github/github-mcp-server"]}}),
    "env": lambda t: _graphify(t).update({"env": {"DYLD_INSERT_LIBRARIES": ".agents/x.dylib"}}),
    "type and url": lambda t: _graphify(t).update({"type": "sse", "url": "https://example.invalid/mcp"}),
    "cwd": lambda t: _graphify(t).update({"cwd": "/tmp"}),
    "command": lambda t: _graphify(t).update({"command": "/bin/bash"}),
    "-c code": lambda t: _graphify(t).update({"args": ["-I", "-c", "import os"]}),
    "no -I": lambda t: _graphify(t).update({"args": ["-m", "graphify.serve", "graphify-out/graph.json"]}),
    "extra trailing arg": lambda t: _graphify(t)["args"].append("--x"),
    "removed key": lambda t: _graphify(t).pop("description"),
    "top-level key": lambda t: t.update({"servers": {}}),
}


def test_duplicate_keys_are_refused() -> None:
    """A repeated key fails to parse instead of one copy being kept silently (F-R5-4)."""
    with pytest.raises(ValueError, match="duplicate JSON keys"):
        json.loads('{"command": "/bin/bash", "command": "x"}', object_pairs_hook=_unique_keys)


@pytest.mark.parametrize("mutation", sorted(MUTATIONS))
def test_any_change_is_rejected(mutation: str) -> None:
    """Each change to the reviewed copy makes the guard reject it (the guard is not vacuous)."""
    template = copy.deepcopy(REVIEWED_TEMPLATE)
    MUTATIONS[mutation](template)
    assert not _is_reviewed(template)
