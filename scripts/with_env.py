"""Run a NAMED, allowlisted command with the working directory's ``.env`` loaded.

invoked_by: rules/project_topology.md sandbox table, agents.md RA-09, Makefile graphify-deep

Usage (nucleus): ``python3 -I scripts/with_env.py <name>``
Usage (host):    ``python3 -I .agents/scripts/with_env.py <name>``

These are the wrapper's own syntax. The wrapper is the HUMAN's path, run
directly or through ``make graphify-deep``. There is no sanctioned agent path
to it under the sandbox (it fails on the ``.env`` deny): the agent prepares the
command and the human runs it. Nobody may add a ``sandbox.excludedCommands``
entry: any excluded entry lets a chained command run unsandboxed (Sprint 055 QA
Gate 1 round 3 N1). The allowlist is nucleus-only.

``<name>`` is a key of ``commands`` in ``config/with_env_allowlist.json``.
Exactly one argument is accepted: the caller supplies a name, never an argv,
so the set of programs that can run with secrets is the allowlist and nothing
else. ``-I`` (isolated mode) is mandatory and checked first: without it the
current directory and the script directory join ``sys.path`` and a sibling
module could shadow this wrapper's standard-library imports.

The env file is fixed to ``.env`` in the current working directory and the
allowlist is fixed to this framework checkout. There is deliberately no flag
to change either: a flag would let a caller point the wrapper at a file the
caller wrote.

Security model: the wrapper itself is NOT a sandbox boundary. It reduces what a
human-run command receives: the child environment is ``os.environ`` without any
``PYTHON*`` variable, plus the ``.env`` pairs, and allowlisted Python entries
also run with ``-I``. The template's lack of sandbox exclusions and its
write-denies on the trees hooks execute (``.agents/hooks``, ``.agents/scripts``,
``.agents/config``; ``claude/settings.hooks.json``, sandbox table in
``rules/project_topology.md``) reduce exposure but are NOT a boundary
(``agents.md`` RA-19): known unsandboxed vectors remain open and are tracked in
``docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md``. Every allowlist entry runs with
secrets in its environment; ``pytest`` is not listed because it runs
agent-written code.

Output masking (``redact``) is NOT a security boundary: it only replaces exact
copies of values of length >= 4 in the child's stdout and stderr. Encoded or
split values, files the child writes and values shorter than 4 characters pass
through unmasked.

Exit codes: the child's code; ``2`` for a refusal (not isolated, wrong
argument count, unknown name, allowlist missing or malformed, ``.env``
missing); ``127`` when the child executable does not exist.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

FRAMEWORK_ROOT = Path(__file__).parent.parent
ENV_FILE = ".env"
MIN_REDACT_LEN = 4


def allowlist_path() -> Path:
    """Locate the fixed allowlist of this framework checkout.

    Returns:
        Path: ``config/with_env_allowlist.json`` under the framework checkout.
    """
    return FRAMEWORK_ROOT / "config" / "with_env_allowlist.json"


def load_allowlist(path: Path) -> dict[str, list[str]]:
    """Read the allowlist and return its named argv lists.

    Args:
        path: Location of the allowlist JSON file.

    Returns:
        dict[str, list[str]]: Command name to argv (``argv[0]`` relative to the checkout).

    Raises:
        ValueError: The file is missing, unreadable or has an entry without a valid ``argv``.
        TypeError: The file does not have the expected shape.
    """
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read {path.name}: {exc.__class__.__name__}") from exc
    commands = data.get("commands") if isinstance(data, dict) else None
    if not isinstance(commands, dict):
        raise TypeError(f"{path.name} has no 'commands' object")
    named: dict[str, list[str]] = {}
    for name, entry in commands.items():
        argv = entry.get("argv") if isinstance(entry, dict) else None
        if not (isinstance(argv, list) and argv and all(isinstance(t, str) for t in argv)):
            raise ValueError(f"{path.name} entry '{name}' has no valid 'argv'")
        named[name] = argv
    return named


def _parse_line(line: str) -> tuple[str, str] | None:
    """Parse one ``.env`` line into a pair.

    Args:
        line: A single stripped, non-comment line.

    Returns:
        tuple[str, str] | None: ``(key, value)``, or None when malformed.
    """
    if line.startswith("export "):
        line = line[len("export "):].lstrip()
    key, sep, value = line.partition("=")
    key = key.strip()
    if not sep or not key or not key.replace("_", "a").isalnum():
        return None
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
        value = value[1:-1]
    return key, value


def parse_env(text: str) -> dict[str, str]:
    """Parse ``.env`` text with the standard library only.

    A malformed line is skipped with a warning naming only its line number.

    Args:
        text: Full content of the env file.

    Returns:
        dict[str, str]: Parsed variables.
    """
    pairs: dict[str, str] = {}
    for number, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        pair = _parse_line(line)
        if pair is None:
            print(f"with_env: skipped malformed line {number} of {ENV_FILE}", file=sys.stderr)
            continue
        pairs[pair[0]] = pair[1]
    return pairs


def redact(text: str, values: list[str]) -> str:
    """Mask exact copies of secret values in ``text`` with ``***``.

    Best effort only, NOT a security boundary: encoded or split values, files
    the child writes and values shorter than 4 characters are not masked.

    Args:
        text: Captured child output.
        values: Parsed ``.env`` values; those shorter than 4 characters are ignored.

    Returns:
        str: ``text`` with the longest values replaced first.
    """
    for value in sorted({v for v in values if len(v) >= MIN_REDACT_LEN}, key=len, reverse=True):
        text = text.replace(value, "***")
    return text


def _isolated() -> bool:
    """Tell whether the interpreter runs in isolated mode (``-I``).

    Returns:
        bool: True when ``sys.flags.isolated`` is set.
    """
    return bool(sys.flags.isolated)


def _child_env(pairs: dict[str, str]) -> dict[str, str]:
    """Build the child environment.

    Args:
        pairs: Variables parsed from ``.env``.

    Returns:
        dict[str, str]: ``os.environ`` minus every ``PYTHON*`` variable, plus ``pairs``.
    """
    kept = {k: v for k, v in os.environ.items() if not k.startswith("PYTHON")}
    return {**kept, **pairs}


def _run_child(argv: list[str], pairs: dict[str, str]) -> int:
    """Run the child with the parsed variables and re-emit masked output.

    Args:
        argv: The allowlisted command, ``argv[0]`` already absolute.
        pairs: Variables parsed from ``.env``.

    Returns:
        int: The child's return code, or 127 when the executable is missing.
    """
    try:
        done = subprocess.run(argv, env=_child_env(pairs), capture_output=True, check=False)
    except FileNotFoundError:
        print(f"with_env: command not found: '{argv[0]}'", file=sys.stderr)
        return 127
    values = list(pairs.values())
    sys.stdout.write(redact(done.stdout.decode("utf-8", "replace"), values))
    sys.stderr.write(redact(done.stderr.decode("utf-8", "replace"), values))
    sys.stdout.flush()
    sys.stderr.flush()
    return done.returncode


def main(argv: list[str]) -> int:
    """Entry point.

    Args:
        argv: Arguments after the script name: exactly one allowlist name.

    Returns:
        int: Process exit code.
    """
    if not _isolated():
        print("with_env: run as 'python3 -I …' (isolated mode)", file=sys.stderr)
        return 2
    if len(argv) != 1:
        print("usage: python3 -I with_env.py <name>", file=sys.stderr)
        return 2
    try:
        commands = load_allowlist(allowlist_path())
    except (ValueError, TypeError) as exc:
        print(f"with_env: {exc}", file=sys.stderr)
        return 2
    if argv[0] not in commands:
        print(f"with_env: '{argv[0]}' is not in config/with_env_allowlist.json", file=sys.stderr)
        return 2
    entry = commands[argv[0]]
    child = [str(FRAMEWORK_ROOT / entry[0]), *entry[1:]]
    try:
        text = Path(ENV_FILE).read_text(encoding="utf-8")
    except OSError:
        print(f"with_env: cannot read {ENV_FILE} in the current directory", file=sys.stderr)
        return 2
    return _run_child(child, parse_env(text))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
