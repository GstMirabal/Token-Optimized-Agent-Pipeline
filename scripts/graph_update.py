"""Rebuild the graphify code graph of the current directory under the Claude Code sandbox.

Cause: in graphifyy 0.8.30, `graphify.extract.extract` calls `_extract_parallel`
when `len(uncached_work) >= _PARALLEL_THRESHOLD` (20). `ProcessPoolExecutor.__init__`
runs `_check_system_limits`, whose `os.sysconf("SC_SEM_NSEMS_MAX")` raises
`PermissionError` under the sandbox, so `graphify update .` prints
`[graphify watch] Rebuild failed: [Errno 1] Operation not permitted`.
`GRAPHIFY_MAX_WORKERS=1` does not avoid the pool.

Workaround: raise `graphify.extract._PARALLEL_THRESHOLD` above any file count so
the extraction stays in-process, then call `graphify.watch._rebuild_code`.

Fail-closed on error: exit 1 with one stderr line when graphify cannot be imported,
when `graphify.extract` lacks `_PARALLEL_THRESHOLD`, when `graphify.watch` lacks
`_rebuild_code`, or when `_rebuild_code` returns False or raises. Exit 0 only when
it returns True.

invoked_by: Makefile targets graphify-update and graphify-rebuild, rules/graphify.md.

Usage:
    venv_skillopt/bin/python -I scripts/graph_update.py [--force]
    .agents/venv_skillopt/bin/python -I .agents/scripts/graph_update.py [--force]
"""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path
from typing import Any

NO_PARALLEL = 10**9


def _fail(message: str) -> int:
    """Print one stderr line and return the failure exit code.

    Args:
        message: Reason for the failure.

    Returns:
        int: Always 1.
    """
    print(f"graph_update: {message}", file=sys.stderr)
    return 1


def _load() -> tuple[Any, Any] | str:
    """Import the two graphify modules and check the attributes the workaround needs.

    Returns:
        tuple[Any, Any] | str: `(extract, watch)` modules, or the failure reason.
    """
    try:
        extract = importlib.import_module("graphify.extract")
        watch = importlib.import_module("graphify.watch")
    except Exception as exc:  # noqa: BLE001 - any import failure is a refusal
        return f"cannot import graphify: {exc!r}"
    if not hasattr(extract, "_PARALLEL_THRESHOLD"):
        return "graphify.extract has no _PARALLEL_THRESHOLD"
    if not hasattr(watch, "_rebuild_code"):
        return "graphify.watch has no _rebuild_code"
    return extract, watch


def main(argv: list[str] | None = None) -> int:
    """Rebuild the graph of the current working directory in-process.

    Args:
        argv: Command-line arguments; `None` reads `sys.argv`.

    Returns:
        int: 0 when `_rebuild_code` returned True, otherwise 1.
    """
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--force", action="store_true", help="rebuild even if unchanged")
    args = parser.parse_args(argv)
    loaded = _load()
    if isinstance(loaded, str):
        return _fail(loaded)
    extract, watch = loaded
    extract._PARALLEL_THRESHOLD = NO_PARALLEL
    try:
        ok = watch._rebuild_code(Path("."), force=args.force)
    except Exception as exc:  # noqa: BLE001 - fault boundary: report and exit non-zero
        return _fail(f"_rebuild_code raised {exc!r}")
    if ok is not True:
        return _fail("_rebuild_code returned False")
    return 0


if __name__ == "__main__":
    sys.exit(main())
