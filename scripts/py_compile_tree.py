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
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _root import agents_root  # noqa: E402

SKIP_PARTS = frozenset({".git", "node_modules", "venv_skillopt"})


def iter_python_files(root: Path) -> list[Path]:
    """Return ``*.py`` paths under root, excluding known noise trees."""
    found: list[Path] = []
    for path in root.rglob("*.py"):
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        found.append(path)
    return sorted(found)


def main() -> int:
    """Compile every eligible ``*.py``; return 0 or 1 on compile failure."""
    root = agents_root()
    paths = iter_python_files(root)
    failures = 0
    for path in paths:
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            print(exc, file=sys.stderr)
            failures += 1
    if failures:
        print(f"py_compile_tree: {failures} failure(s)", file=sys.stderr)
        return 1
    print(f"py_compile_tree: OK ({len(paths)} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
