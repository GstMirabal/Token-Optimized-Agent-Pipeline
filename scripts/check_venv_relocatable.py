"""Fail when venv_skillopt was built for a path other than this checkout's.

A Python virtualenv is not relocatable: every console-script under
``venv_skillopt/bin/`` carries an absolute shebang to
``<build-path>/venv_skillopt/bin/python3.x``, and ``pyvenv.cfg`` records the
build path on its ``command =`` line. When ``.agents`` is embedded as a
submodule at a path different from where the venv was created — a copied tree, a
renamed nucleus, a reused host — ``venv_skillopt/bin/graphify`` and
``venv_skillopt/bin/pip`` fail with ``bad interpreter`` while
``venv_skillopt/bin/python`` (a symlink to the system interpreter) still works,
so the breakage stays silent until a console-script is called.

``workflows/start_workflow.md`` ``pip_setup`` rebuilds the venv only when
``installed.lock`` is absent, so a stale venv with the lock present is never
revalidated. This check closes that gap: it runs every session and exits ``2``
when the recorded build path does not match this checkout.

invoked_by: workflows/start_workflow.md#pip_setup

Usage:
    python3 scripts/check_venv_relocatable.py
    python3 scripts/check_venv_relocatable.py --venv path/to/venv_skillopt

Exit codes:
    0 — venv matches this checkout, or no venv present yet (pip_setup builds it)
    2 — venv was built for a different path; pip_setup must rebuild with --clear
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _root import agents_root

_PROBE_SCRIPTS = ("bin/pip", "bin/pip3")


def _recorded_build_path(pyvenv_cfg: Path) -> Path | None:
    """Venv destination path from the ``command =`` line of ``pyvenv.cfg``.

    The destination is always the final argument of ``python -m venv [opts] DEST``,
    so the last whitespace-separated token is taken rather than the one after
    ``venv`` (which would be a flag such as ``--clear``).

    Args:
        pyvenv_cfg: Path to the venv's ``pyvenv.cfg``.

    Returns:
        The path passed to ``-m venv`` at build time, or ``None`` when the line
        is absent or malformed.
    """
    try:
        lines = pyvenv_cfg.read_text(encoding="utf-8").splitlines()
    except OSError:
        return None
    for line in lines:
        key, _, value = line.partition("=")
        if key.strip() != "command":
            continue
        parts = value.split()
        if "venv" in parts and len(parts) > parts.index("venv") + 1:
            return Path(parts[-1])
    return None


def _shebang_interpreter(script: Path) -> Path | None:
    """Interpreter path from a console-script's ``#!`` first line.

    Args:
        script: Path to a generated console-script (e.g. ``bin/pip``).

    Returns:
        The interpreter path, or ``None`` when the file is missing or its first
        line is not a shebang.
    """
    try:
        text = script.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    first = text.splitlines()[0] if text else ""
    if not first.startswith("#!"):
        return None
    return Path(first[2:].strip())


def check(venv: Path) -> list[str]:
    """Mismatches between the venv's recorded build path and its location.

    Args:
        venv: Path to the ``venv_skillopt`` directory to inspect.

    Returns:
        Human-readable mismatch descriptions. Empty means the venv is consistent
        with its current location, or is absent (nothing to check).
    """
    if not venv.is_dir():
        return []
    expected = venv.resolve()
    problems: list[str] = []

    recorded = _recorded_build_path(venv / "pyvenv.cfg")
    if recorded is not None and recorded.resolve() != expected:
        problems.append(
            f"pyvenv.cfg build path {recorded} != current location {expected}"
        )

    for name in _PROBE_SCRIPTS:
        interpreter = _shebang_interpreter(venv / name)
        if interpreter is None:
            continue
        if interpreter.parent.parent.resolve() != expected:
            problems.append(f"{name} shebang {interpreter} is outside {expected}")
        break

    return problems


def main() -> int:
    """Entry point. See the module docstring for exit codes."""
    parser = argparse.ArgumentParser(description="venv relocatability gate")
    parser.add_argument(
        "--venv",
        type=Path,
        default=agents_root() / "venv_skillopt",
        help="venv directory to inspect (default: <checkout>/venv_skillopt)",
    )
    args = parser.parse_args()

    problems = check(args.venv)
    if problems:
        print("[FAIL] check_venv_relocatable: venv built for another path")
        for problem in problems:
            print(f"  - {problem}")
        print(
            "  fix: python3 -m venv --clear venv_skillopt && "
            "venv_skillopt/bin/python -m pip install -r requirements-core.txt"
        )
        return 2
    print("[OK] check_venv_relocatable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
