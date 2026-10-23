"""Guards what the template claude/mcp.json launches (Sprint 056, D12, Q3; Hotfix H-007).

install.py merges the template into every host's .mcp.json, and Claude Code
launches each MCP server outside the sandbox with the host root as working
directory. A Python server started with `-m` and without `-I` puts that working
directory first on sys.path, so a host-root package named like the served
module (`graphify/`) shadows the installed one and runs unsandboxed
(SANDBOX_ENUMERATION.md E10). A server that fetches a package from a registry at launch runs
whatever the registry serves, unsandboxed (H-007), so every server must match a
reviewed launch.
"""
import json
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "claude" / "mcp.json"


def _python_servers() -> list[tuple[str, dict[str, Any]]]:
    """Return the template servers whose command is a Python interpreter path.

    Returns:
        (name, server) pairs whose command ends with `/python` or `/python3`.
    """
    servers = json.loads(TEMPLATE.read_text(encoding="utf-8"))["mcpServers"]
    return [
        (name, server) for name, server in servers.items()
        if server["command"].endswith(("/python", "/python3"))
    ]


def test_template_has_a_python_server() -> None:
    """The guard below is not vacuous: the template ships at least one Python server."""
    assert _python_servers()


@pytest.mark.parametrize("name,server", _python_servers())
def test_python_server_runs_isolated(name: str, server: dict[str, Any]) -> None:
    """Every Python MCP server passes `-I` as its first interpreter argument."""
    assert server["args"][:1] == ["-I"], name


# Every server the template may ship, reviewed: its command and the leading arguments
# that decide what runs. A server not listed here, or listed with another launch, fails
# until it is reviewed and added. This is an allowlist on purpose: two rounds of
# denylists over shell text (H-007 QA rounds 2 and 3) each let a registry fetch
# through, and agents.md §1 forbids calling a heuristic scan of that grammar fail-closed.
REVIEWED_LAUNCHES = {
    "graphify": (".agents/venv_skillopt/bin/python", ["-I", "-m", "graphify.serve"]),
}


def _servers() -> dict[str, dict[str, Any]]:
    """Return every server of the template.

    Returns:
        The `mcpServers` mapping of `claude/mcp.json`, keyed by server name.
    """
    return json.loads(TEMPLATE.read_text(encoding="utf-8"))["mcpServers"]


@pytest.mark.parametrize("name", sorted(_servers()))
def test_server_launch_is_reviewed(name: str) -> None:
    """Every template server launches exactly as its reviewed entry says (H-007)."""
    assert name in REVIEWED_LAUNCHES, f"{name}: unreviewed MCP server"
    command, leading = REVIEWED_LAUNCHES[name]
    server = _servers()[name]
    assert server["command"] == command, name
    assert server.get("args", [])[:len(leading)] == leading, name


@pytest.mark.parametrize("server", [
    {"command": "/bin/bash", "args": [".agents/mcp_servers/github_mcp/scripts/start_mcp.sh"]},
    {"command": "docker", "args": ["run", "-i", "--rm", "ghcr.io/github/github-mcp-server"]},
    {"command": ".agents/venv_skillopt/bin/python", "args": ["-I", "-c", "import os"]},
    {"command": ".agents/venv_skillopt/bin/python", "args": ["-m", "graphify.serve"]},
])
def test_unreviewed_launch_is_rejected(server: dict[str, Any]) -> None:
    """A launch that differs from the reviewed entry does not match it (the guard is not vacuous)."""
    command, leading = REVIEWED_LAUNCHES["graphify"]
    assert (server["command"], server["args"][:len(leading)]) != (command, leading)
