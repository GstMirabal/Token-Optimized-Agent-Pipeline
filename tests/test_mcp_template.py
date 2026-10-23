"""Guards what the template claude/mcp.json launches (Sprint 056, D12, Q3; Hotfix H-007).

install.py merges the template into every host's .mcp.json, and Claude Code
launches each MCP server outside the sandbox with the host root as working
directory. A Python server started with `-m` and without `-I` puts that working
directory first on sys.path, so a host-root package named like the served
module (`graphify/`) shadows the installed one and runs unsandboxed
(SANDBOX_ENUMERATION.md E10). A server that fetches a package from a registry at launch runs
whatever the registry serves, unsandboxed (H-007), so none may.
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


# Any token that fetches and runs a package from a registry. Matched as a word anywhere
# in the launch text, quoted, flagged, nested in `bash -c` or commented alike: a shell
# line is not parsed here, so the check fails closed instead (agents.md §1 forbids
# crediting a heuristic scanner over a context-sensitive grammar as fail-closed).
FETCH_RUNNER = re.compile(
    r"\b(?:dlx|npx|bunx|uvx|pipx|npm\s+(?:exec|x)|bun\s+x)\b|\bpnpm\b.*\bexec\b"
)
LAUNCHER_SUFFIXES = (".sh", ".py", ".js", ".mjs", ".cjs")
VENV_PYTHON = ("/bin/python", "/bin/python3")


def _servers() -> dict[str, dict[str, Any]]:
    """Return every server of the template.

    Returns:
        The `mcpServers` mapping of `claude/mcp.json`, keyed by server name.
    """
    return json.loads(TEMPLATE.read_text(encoding="utf-8"))["mcpServers"]


def _launch_text(server: dict[str, Any]) -> str:
    """Return the command line of a server plus the text of each launcher file it names.

    Args:
        server: One `mcpServers` entry.

    Returns:
        The command line, then the contents of every part of it (the command
        included) that is a `.agents/` path to an existing script of this framework.
    """
    parts = [server["command"], *server.get("args", [])]
    texts = [" ".join(parts)]
    for part in parts:
        launcher = ROOT / part.removeprefix(".agents/")
        if part.startswith(".agents/") and launcher.suffix in LAUNCHER_SUFFIXES and launcher.is_file():
            texts.append(launcher.read_text(encoding="utf-8"))
    return "\n".join(texts)


@pytest.mark.parametrize("line", [
    "pnpm dlx @scope/pkg",
    'pnpm --silent dlx "@scope/pkg"',
    "pnpm --reporter silent dlx @scope/pkg",
    "pnpm -C /tmp dlx @scope/pkg@1.2.3",
    "npx -y 'pkg'",
    "exec env FOO=1 npx -y pkg",
    "npm exec -y pkg",
    "npm x -y pkg",
    "yarn dlx pkg",
    "bunx pkg@1.0.0",
    "bun x pkg",
    "uvx tool==2.0.0",
    "pipx run tool",
    'bash -c "npx -y pkg"',
    "# pnpm dlx in a comment",
])
def test_fetch_runner_fails_closed_on_every_form(line: str) -> None:
    """Every runner form is caught, pinned or not, quoted, flagged or nested (QA-H007-2, R2-1)."""
    assert FETCH_RUNNER.search(line)


@pytest.mark.parametrize("line", [
    ".agents/venv_skillopt/bin/python -I -m graphify.serve graphify-out/graph.json",
    "pnpm install --frozen-lockfile",
    "python3 -I scripts/session_state.py suspend",
])
def test_fetch_runner_ignores_non_fetching_lines(line: str) -> None:
    """A line that runs local code only is not reported."""
    assert not FETCH_RUNNER.search(line)


@pytest.mark.parametrize("name", sorted(_servers()))
def test_server_fetches_no_package_at_launch(name: str) -> None:
    """No server, nor a launcher it names, fetches a package from a registry when started."""
    found = FETCH_RUNNER.findall(_launch_text(_servers()[name]))
    assert not found, (name, found)


@pytest.mark.parametrize("name", sorted(_servers()))
def test_server_launcher_paths_exist(name: str) -> None:
    """Every `.agents/` file a server names exists, except the interpreter of the host venv."""
    server = _servers()[name]
    paths = [p for p in [server["command"], *server.get("args", [])] if p.startswith(".agents/")]
    missing = [
        p for p in paths
        if not p.endswith(VENV_PYTHON) and not (ROOT / p.removeprefix(".agents/")).exists()
    ]
    assert not missing, (name, missing)
