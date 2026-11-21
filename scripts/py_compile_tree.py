"""Compile all project ``*.py`` files without ``xargs`` / ``SC_ARG_MAX``.

The Cursor agent sandbox denies ``os.sysconf('SC_ARG_MAX')``, which breaks
both ``xargs`` and ``find … -exec … {} +``. A plain Python walk does not.

invoked_by: Makefile `verify`.

Usage:
    python3 scripts/py_compile_tree.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _root import agents_root

SKIP_PARTS = frozenset({".git", "node_modules", "venv_skillopt"})


def iter_python_files(root: Path) -> list[Path]:
    """Return ``*.py`` paths under root, excluding known noise trees.

    Args:
        root: Directory to scan recursively.

    Returns:
        list[Path]: Sorted paths with no part in ``SKIP_PARTS``.
    """
    found: list[Path] = []
    for path in root.rglob("*.py"):
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        found.append(path)
    return sorted(found)


def compile_one(path: Path) -> bool:
    """Compile one source in memory; print the path and error, return False on failure.

    The source is read as bytes so PEP 263 encoding declarations apply. Nothing is
    written to disk. Any ``Exception`` (syntax error, null byte, undecodable bytes,
    unreadable file) counts as a failure.

    Args:
        path: Python source file to compile.

    Returns:
        bool: True when the file compiles.
    """
    try:
        compile(path.read_bytes(), str(path), "exec", dont_inherit=True)
    except Exception as exc:  # noqa: BLE001 - one file must not stop the rest
        print(f"{path}: {type(exc).__name__}: {exc}", file=sys.stderr)
        return False
    return True


def compile_all(paths: list[Path]) -> int:
    """Compile each path in memory (nothing is written to disk).

    Args:
        paths: Python source files to compile.

    Returns:
        int: The number of files that failed to compile.
    """
    results = [compile_one(path) for path in paths]
    return results.count(False)


def main() -> int:
    """Compile every eligible ``*.py`` under the framework root.

    Returns:
        int: 0 when every file compiles, 1 on any compile failure.
    """
    root = agents_root()
    paths = iter_python_files(root)
    failures = compile_all(paths)
    if failures:
        print(f"py_compile_tree: {failures} failure(s)", file=sys.stderr)
        return 1
    print(f"py_compile_tree: OK ({len(paths)} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
