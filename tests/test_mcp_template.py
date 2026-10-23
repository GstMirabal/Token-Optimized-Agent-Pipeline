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
import shlex
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


# Runners that fetch a package by name: those that take it as first operand, and the
# package managers whose `dlx` (or `run`) subcommand does.
DIRECT_RUNNERS = frozenset({"npx", "bunx", "uvx"})
SUBCOMMAND_RUNNERS = {"pnpm": "dlx", "yarn": "dlx", "pipx": "run"}
PINNED = re.compile(r"(?:@|==)\d+\.\d+\.\d+$")
LAUNCHER_SUFFIXES = (".sh", ".py", ".js", ".mjs", ".cjs")
VENV_PYTHON = ("/bin/python", "/bin/python3")


def _operands(tokens: list[str], start: int) -> list[str]:
    """Return the tokens after ``start`` that are not option flags.

    Args:
        tokens: One shell-split command line.
        start: Index of the token after which operands are collected.

    Returns:
        The non-flag tokens following ``start``, in order.
    """
    return [tok for tok in tokens[start + 1:] if not tok.startswith("-")]


def _fetched_specs(line: str) -> list[str]:
    """Return every package spec a shell line fetches through a package runner.

    A line that cannot be shell-split, and a spec that is a variable expansion,
    are returned as found: neither can be shown pinned, so they must not pass.

    Args:
        line: One line of a launcher script or a server command line.

    Returns:
        The package specs, quotes removed by the shell split.
    """
    try:
        tokens = shlex.split(line, comments=True)
    except ValueError:
        return [line] if any(r in line for r in (*DIRECT_RUNNERS, *SUBCOMMAND_RUNNERS)) else []
    return [spec for i in range(len(tokens)) for spec in _spec_at(tokens, i)]


def _spec_at(tokens: list[str], i: int) -> list[str]:
    """Return the package spec fetched by the runner at ``tokens[i]``, if it is one.

    Args:
        tokens: One shell-split command line.
        i: Index of the token to inspect.

    Returns:
        One spec when ``tokens[i]`` is a runner (the runner itself when it names no
        package, so the line cannot pass), or an empty list.
    """
    name = tokens[i].rsplit("/", 1)[-1]
    rest = _operands(tokens, i)
    if name in DIRECT_RUNNERS:
        return rest[:1] or [tokens[i]]
    if name in SUBCOMMAND_RUNNERS and rest[:1] == [SUBCOMMAND_RUNNERS[name]]:
        return rest[1:2] or [tokens[i]]
    return []


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
    texts = [shlex.join(parts)]
    for part in parts:
        launcher = ROOT / part.removeprefix(".agents/")
        if part.startswith(".agents/") and launcher.suffix in LAUNCHER_SUFFIXES and launcher.is_file():
            texts.append(launcher.read_text(encoding="utf-8"))
    return "\n".join(texts)


@pytest.mark.parametrize("line,specs", [
    ("pnpm dlx @scope/pkg", ["@scope/pkg"]),
    ('pnpm dlx "@scope/pkg"', ["@scope/pkg"]),
    ("pnpm --silent dlx @scope/pkg@1.2.3", ["@scope/pkg@1.2.3"]),
    ("npx -y 'pkg'", ["pkg"]),
    ("yarn dlx pkg", ["pkg"]),
    ("bunx pkg@1.0.0", ["pkg@1.0.0"]),
    ("uvx tool==2.0.0", ["tool==2.0.0"]),
    ("pipx run tool", ["tool"]),
    ("exec npx $PKG", ["$PKG"]),
    ("pnpm install", []),
    ("echo starting # npx pkg", []),
])
def test_fetched_specs_reads_every_runner_form(line: str, specs: list[str]) -> None:
    """The scanner finds quoted, flagged and variable specs of every runner (QA-H007-2)."""
    assert _fetched_specs(line) == specs


@pytest.mark.parametrize("spec,pinned", [
    ("@scope/pkg@1.2.3", True), ("tool==2.0.0", True), ("@scope/pkg", False),
    ("pkg@latest", False), ("pkg@^1.2.3", False), ("$PKG", False),
])
def test_pinned_requires_an_exact_version(spec: str, pinned: bool) -> None:
    """Only an exact `x.y.z` version counts as pinned."""
    assert bool(PINNED.search(spec)) is pinned


@pytest.mark.parametrize("name", sorted(_servers()))
def test_server_fetches_no_unpinned_package(name: str) -> None:
    """No server, nor a launcher it names, fetches a package without an exact version."""
    specs = [s for line in _launch_text(_servers()[name]).splitlines() for s in _fetched_specs(line)]
    assert all(PINNED.search(spec) for spec in specs), (name, specs)


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
