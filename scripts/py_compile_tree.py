"""Compile all project ``*.py`` files without ``xargs`` / ``SC_ARG_MAX``.

The Cursor agent sandbox denies ``os.sysconf('SC_ARG_MAX')``, which breaks
both ``xargs`` and ``find … -exec … {} +``. A plain Python walk does not.

invoked_by: Makefile `verify`.

Usage:
    python3 scripts/py_compile_tree.py
"""

from __future__ import annotations

import py_compile
import sys
import tempfile
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


def compile_one(path: Path, cfile: Path) -> bool:
    """Compile one source into ``cfile``; print the error and return False on failure.

    Args:
        path: Python source file to compile.
        cfile: Destination of the bytecode.

    Returns:
        bool: True when the file compiles.
    """
    try:
        py_compile.compile(str(path), cfile=str(cfile), doraise=True)
    except py_compile.PyCompileError as exc:
        print(exc, file=sys.stderr)
        return False
    return True


def compile_all(paths: list[Path]) -> int:
    """Compile each path into a temp dir (nothing written in the tree).

    Args:
        paths: Python source files to compile.

    Returns:
        int: The number of files that failed to compile.
    """
    with tempfile.TemporaryDirectory() as tmp:
        results = [compile_one(path, Path(tmp) / f"{i}.pyc") for i, path in enumerate(paths)]
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
