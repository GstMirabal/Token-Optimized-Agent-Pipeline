"""Guards the interpreter isolation of the template claude/mcp.json (Sprint 056, D12, Q3).

install.py merges the template into every host's .mcp.json, and Claude Code
launches each MCP server outside the sandbox with the host root as working
directory. A Python server started with `-m` and without `-I` puts that working
directory first on sys.path, so a host-root package named like the served
module (`graphify/`) shadows the installed one and runs unsandboxed
(SANDBOX_ENUMERATION.md E10).
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
