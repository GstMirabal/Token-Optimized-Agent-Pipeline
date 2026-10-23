"""Guards what the template claude/mcp.json launches (Sprint 056, D12, Q3; Hotfix H-007).

install.py merges the template into every host's .mcp.json, and Claude Code
launches each MCP server outside the sandbox with the host root as working
directory. A Python server started with `-m` and without `-I` puts that working
directory first on sys.path, so a host-root package named like the served
module (`graphify/`) shadows the installed one and runs unsandboxed
(SANDBOX_ENUMERATION.md E10). A server that fetches a package by name with no
version runs whatever the registry serves, unsandboxed (H-007).
"""
import json
import re
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


# A package spec fetched by `pnpm dlx` or `npx`: scoped or bare name, optional `@version`.
FETCH = re.compile(r"\b(?:pnpm\s+dlx|npx(?:\s+-y)?)\s+(?P<spec>@?[\w./-]+(?:@[\w.^~<>=*-]+)?)")
PINNED = re.compile(r"@\d+\.\d+\.\d+$")
LAUNCHER_SUFFIXES = (".sh", ".py", ".js", ".mjs", ".cjs")


def _servers() -> dict[str, dict[str, Any]]:
    """Return every server of the template."""
    return json.loads(TEMPLATE.read_text(encoding="utf-8"))["mcpServers"]


def _launch_text(server: dict[str, Any]) -> str:
    """Return the command line of a server plus the text of each launcher file it names.

    Args:
        server: One `mcpServers` entry.

    Returns:
        The command, its arguments, and the contents of every argument that is a
        `.agents/` path to an existing script of this framework (the command is an
        interpreter, never read).
    """
    args = server.get("args", [])
    texts = [" ".join([server["command"], *args])]
    for arg in args:
        launcher = ROOT / arg.removeprefix(".agents/")
        if arg.startswith(".agents/") and launcher.suffix in LAUNCHER_SUFFIXES and launcher.is_file():
            texts.append(launcher.read_text(encoding="utf-8"))
    return "\n".join(texts)


@pytest.mark.parametrize("name", sorted(_servers()))
def test_server_fetches_no_unpinned_package(name: str) -> None:
    """No server, nor a launcher it names, fetches a package without an exact version."""
    specs = [m.group("spec") for m in FETCH.finditer(_launch_text(_servers()[name]))]
    assert all(PINNED.search(spec) for spec in specs), (name, specs)


@pytest.mark.parametrize("name", sorted(_servers()))
def test_server_launcher_paths_exist(name: str) -> None:
    """Every `.agents/` file a server names exists, except the interpreter of the host venv."""
    server = _servers()[name]
    paths = [p for p in [server["command"], *server.get("args", [])] if p.startswith(".agents/")]
    missing = [
        p for p in paths
        if "/bin/python" not in p and not (ROOT / p.removeprefix(".agents/")).exists()
    ]
    assert not missing, (name, missing)
