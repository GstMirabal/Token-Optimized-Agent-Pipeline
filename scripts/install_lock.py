"""Record and verify which requirement set the venv was installed from.

``workflows/start_workflow.md`` ``pip_setup`` used to reinstall only when
``installed.lock`` was absent, so a changed ``requirements-core.txt`` (or any
file it includes with ``-r``) left a stale venv undetected (``KI-053-1``). This
script hashes the whole requirement set with SHA-256 and compares it with the
hash recorded in ``installed.lock``: a presence test cannot see that the set
changed, a hash can.

The requirement set is ``requirements-core.txt`` plus every file it includes via
``-r`` / ``--requirement`` lines, recursively (paths relative to the including
file), hashed in sorted relative-path order as ``path NUL content NUL``. An
include cycle is broken by a visited set.

invoked_by: workflows/start_workflow.md#pip_setup, scripts/session_start.py

Usage:
    python3 scripts/install_lock.py check [--root <framework root>]
    python3 scripts/install_lock.py write [--root <framework root>]

Exit codes:
    0 - ``check``: lock matches the requirement set; ``write``: lock written
    2 - ``check``: lock absent, unreadable, legacy (no hash) or stale, or the
        requirement set cannot be read (missing file)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _root import agents_root

REQUIREMENTS_FILE = "requirements-core.txt"
LOCK_FILE = "installed.lock"
_INCLUDE = re.compile(r"^(?:-r|--requirement)(?:\s+|=)(\S+)")
REINSTALL = (
    "venv_skillopt/bin/python -m pip install -r requirements-core.txt "
    "&& python3 scripts/install_lock.py write"
)


class RequirementSetError(Exception):
    """The requirement set cannot be read completely."""


def _includes(text: str) -> list[str]:
    """Paths named by ``-r`` / ``--requirement`` lines of a requirements file.

    Args:
        text: Content of one requirements file.

    Returns:
        Include targets as written, in file order.
    """
    found: list[str] = []
    for line in text.splitlines():
        match = _INCLUDE.match(line.split(" #", 1)[0].strip())
        if match:
            found.append(match.group(1))
    return found


def _read(path: Path) -> str:
    """Read one requirements file.

    Args:
        path: File to read.

    Returns:
        Its text.

    Raises:
        RequirementSetError: When the file is missing or unreadable.
    """
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise RequirementSetError(f"cannot read {path}: {exc}") from exc


def collect(root: Path) -> dict[str, str]:
    """Collect the requirement set: the core file plus recursive includes.

    Args:
        root: Framework root holding ``requirements-core.txt``.

    Returns:
        Mapping of POSIX path relative to ``root`` to file content.

    Raises:
        RequirementSetError: When any file in the set cannot be read.
    """
    root = root.resolve()
    files: dict[str, str] = {}
    pending = [root / REQUIREMENTS_FILE]
    while pending:
        path = pending.pop().resolve()
        rel = path.relative_to(root).as_posix() if path.is_relative_to(root) else str(path)
        if rel in files:
            continue
        files[rel] = _read(path)
        pending.extend(path.parent / name for name in _includes(files[rel]))
    return files


def digest(files: dict[str, str]) -> str:
    """SHA-256 over the set in sorted relative-path order.

    Args:
        files: Mapping returned by ``collect``.

    Returns:
        Lowercase hex digest.
    """
    sha = hashlib.sha256()
    for rel in sorted(files):
        sha.update(rel.encode("utf-8") + b"\0" + files[rel].encode("utf-8") + b"\0")
    return sha.hexdigest()


def _recorded_hash(lock: Path) -> str | None:
    """Hash recorded in a lock file, or ``None`` when absent/unreadable/legacy.

    Args:
        lock: Path to ``installed.lock``.

    Returns:
        The ``requirements_sha256`` string, or ``None``.
    """
    try:
        data = json.loads(lock.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    value = data.get("requirements_sha256") if isinstance(data, dict) else None
    return value if isinstance(value, str) else None


def run_check(root: Path) -> int:
    """Compare the recorded hash with the current requirement set.

    Args:
        root: Framework root.

    Returns:
        ``0`` when current, ``2`` otherwise (message printed).
    """
    try:
        current = digest(collect(root))
    except RequirementSetError as exc:
        print(f"[FAIL] install_lock: {exc}")
        return 2
    recorded = _recorded_hash(root / LOCK_FILE)
    if recorded == current:
        print("[OK] install_lock")
        return 0
    state = "absent, unreadable or legacy (no hash)" if recorded is None else "stale"
    print(f"[FAIL] install_lock: {LOCK_FILE} is {state}")
    print(f"  fix: {REINSTALL}")
    return 2


def run_write(root: Path) -> int:
    """Write ``installed.lock`` for the current requirement set.

    Args:
        root: Framework root.

    Returns:
        ``0`` on success, ``2`` when the requirement set cannot be read.
    """
    try:
        files = collect(root)
    except RequirementSetError as exc:
        print(f"[FAIL] install_lock: {exc}")
        return 2
    record = {
        "installed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "requirements_sha256": digest(files),
        "files": sorted(files),
    }
    (root / LOCK_FILE).write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(f"[OK] install_lock: wrote {LOCK_FILE}")
    return 0


def main() -> int:
    """Entry point. See the module docstring for exit codes."""
    parser = argparse.ArgumentParser(description="installed.lock requirement-set gate")
    parser.add_argument("command", choices=("check", "write"))
    parser.add_argument("--root", type=Path, default=agents_root())
    args = parser.parse_args()
    if args.command == "write":
        return run_write(args.root)
    return run_check(args.root)


if __name__ == "__main__":
    raise SystemExit(main())
