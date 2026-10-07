"""Run an allowlisted command with the working directory's ``.env`` loaded.

invoked_by: rules/project_topology.md sandbox table, agents.md RA-09, Makefile graphify-deep

Usage (nucleus): ``python3 scripts/with_env.py <command> [args...]``
Usage (host):    ``python3 .agents/scripts/with_env.py .agents/venv_skillopt/bin/python -m graphify ...``

The env file is fixed to ``.env`` in the current working directory and the
allowlist is fixed to ``config/with_env_allowlist.json`` of this framework
checkout. There is deliberately no flag to change either: the wrapper runs
unsandboxed, and a flag would let an agent point it at a file the agent wrote.

Security model: this wrapper itself runs OUTSIDE the Claude Code sandbox,
through ``sandbox.excludedCommands``. It is therefore safe only while the
wrapper, its allowlist and the settings entry that excludes it are
write-denied (``claude/settings.hooks.json``, Sprint 055 U07).

Values read from ``.env`` are never printed. The child's stdout and stderr are
captured and every value of length >= 4 is replaced by ``***`` before output.

Exit codes: the child's code; ``2`` for a refusal (command off the allowlist,
allowlist missing or malformed, ``.env`` missing); ``127`` when the child
executable does not exist.
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


def load_allowlist(path: Path) -> list[list[str]]:
    """Read the allowlist and return its argv prefixes.

    Args:
        path: Location of the allowlist JSON file.

    Returns:
        list[list[str]]: One argv prefix per entry.

    Raises:
        ValueError: The file is missing or unreadable.
        TypeError: The file does not have the expected shape.
    """
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read {path.name}: {exc.__class__.__name__}") from exc
    commands = data.get("commands") if isinstance(data, dict) else None
    if not isinstance(commands, list):
        raise TypeError(f"{path.name} has no 'commands' list")
    prefixes: list[list[str]] = []
    for entry in commands:
        prefix = entry.get("argv_prefix") if isinstance(entry, dict) else None
        if not (isinstance(prefix, list) and prefix and all(isinstance(t, str) for t in prefix)):
            raise ValueError(f"{path.name} has an entry without a valid 'argv_prefix'")
        prefixes.append(prefix)
    return prefixes


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


def is_allowed(argv: list[str], prefixes: list[list[str]]) -> bool:
    """Tell whether ``argv`` starts with an allowlisted prefix.

    ``argv[0]`` is compared with ``os.path.abspath``, never ``realpath``: the
    framework venv interpreter is a symlink to the system interpreter, and
    resolving it would let any python match. Remaining tokens are literal.

    Args:
        argv: The command to run.
        prefixes: Allowlisted argv prefixes, ``prefix[0]`` relative to the checkout.

    Returns:
        bool: True when some prefix matches.
    """
    if not argv:
        return False
    head = os.path.abspath(argv[0])
    for prefix in prefixes:
        expected = os.path.abspath(os.path.join(FRAMEWORK_ROOT, prefix[0]))
        if head == expected and argv[1:len(prefix)] == prefix[1:] and len(argv) >= len(prefix):
            return True
    return False


def redact(text: str, values: list[str]) -> str:
    """Replace secret values in ``text`` with ``***``.

    Args:
        text: Captured child output.
        values: Parsed ``.env`` values; those shorter than 4 characters are ignored.

    Returns:
        str: ``text`` with the longest values replaced first.
    """
    for value in sorted({v for v in values if len(v) >= MIN_REDACT_LEN}, key=len, reverse=True):
        text = text.replace(value, "***")
    return text


def _run_child(argv: list[str], pairs: dict[str, str]) -> int:
    """Run the child with the parsed variables and re-emit redacted output.

    Args:
        argv: The allowlisted command.
        pairs: Variables parsed from ``.env``.

    Returns:
        int: The child's return code, or 127 when the executable is missing.
    """
    env = {**os.environ, **pairs}
    try:
        done = subprocess.run(argv, env=env, capture_output=True, check=False)
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
        argv: Arguments after the script name: the command and its arguments.

    Returns:
        int: Process exit code.
    """
    if not argv:
        print("usage: with_env.py <command> [args...]", file=sys.stderr)
        return 2
    try:
        prefixes = load_allowlist(allowlist_path())
    except (ValueError, TypeError) as exc:
        print(f"with_env: {exc}", file=sys.stderr)
        return 2
    if not is_allowed(argv, prefixes):
        print(f"with_env: '{argv[0]}' is not in config/with_env_allowlist.json", file=sys.stderr)
        return 2
    try:
        text = Path(ENV_FILE).read_text(encoding="utf-8")
    except OSError:
        print(f"with_env: cannot read {ENV_FILE} in the current directory", file=sys.stderr)
        return 2
    return _run_child(argv, parse_env(text))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
