"""Fail when venv_skillopt was built for a path other than this checkout's.

A Python virtualenv is not relocatable: every console-script under
``venv_skillopt/bin/`` carries an absolute reference to
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

Both detectors are whitespace-immune: a checkout path containing a space (for
example ``.../My Projects/host/.agents``) must not be misread as a relocated
venv. The ``pyvenv.cfg`` ``command`` line is matched as a whole substring, never
tokenised, and pip's POSIX ``/bin/sh`` console-script wrapper is followed to the
interpreter it execs rather than stopping at ``/bin/sh``.

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
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _root import agents_root

_PROBE_SCRIPTS = ("bin/pip", "bin/pip3")
_POSIX_WRAPPER_SHELLS = ("sh", "bash")
_EXEC_LINE = re.compile(r"'exec'\s+(['\"])(.*?)\1")


def _command_line_problem(pyvenv_cfg: Path, venv: Path) -> str | None:
    """Problem when ``pyvenv.cfg``'s ``command`` line targets another path.

    The venv destination is compared as a whole substring — never tokenised —
    so a build path containing whitespace is matched intact.

    Args:
        pyvenv_cfg: Path to the venv's ``pyvenv.cfg``.
        venv: Path to the ``venv_skillopt`` directory.

    Returns:
        A one-line description, or ``None`` when the line already references this
        location or is absent. A normal but old venv legitimately has no
        ``command`` line (recorded only since Python 3.11), so failing closed on
        its absence would false-positive — a missing line returns ``None``.
    """
    try:
        lines = pyvenv_cfg.read_text(encoding="utf-8").splitlines()
    except OSError:
        return None
    expected = venv.resolve()
    for line in lines:
        key, sep, _ = line.partition("=")
        if not sep or key.strip() != "command":
            continue
        # Match the resolved absolute form only. The shipped invoker passes an
        # already-resolved path (`agents_root() / "venv_skillopt"`), so this is
        # unchanged for it; a bare `str(venv)` disjunct additionally accepted a
        # relative `--venv` argument by its literal spelling, which is not a
        # location reference (`C6`, Sprint 044).
        if str(expected) in line:
            return None
        return (
            f"pyvenv.cfg command line does not reference {expected} "
            "(venv built for another path)"
        )
    return None


def _script_text(venv: Path) -> str | None:
    """Body of the first readable console-script among ``bin/pip``, ``bin/pip3``.

    Args:
        venv: Path to the ``venv_skillopt`` directory.

    Returns:
        The full text of the first probe script that reads, or ``None`` when
        none is present or readable.
    """
    for name in _PROBE_SCRIPTS:
        try:
            return (venv / name).read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
    return None


def _interpreter_ref(text: str) -> str | None:
    """Interpreter path a console-script hands control to.

    Handles the direct ``#!<interpreter>`` form and pip's POSIX space-safe
    wrapper (``#!/bin/sh`` followed on line 2 by
    ``'''exec' '<interpreter>' "$0" "$@"``, single- or double-quoted).

    Args:
        text: Full text of the console-script.

    Returns:
        The interpreter path as written (not resolved), or ``None`` when no
        shebang is present or the wrapper's exec line cannot be parsed.
    """
    lines = text.splitlines()
    first = lines[0] if lines else ""
    if not first.startswith("#!"):
        return None
    shebang = first[2:].strip()
    token = shebang.split()[0] if shebang else ""
    if Path(token).name not in _POSIX_WRAPPER_SHELLS:
        return shebang
    exec_line = lines[1] if len(lines) > 1 else ""
    match = _EXEC_LINE.search(exec_line)
    return match.group(2) if match else None


def _console_script_problem(venv: Path) -> str | None:
    """Problem when pip's console-script interpreter points outside this venv.

    A relocated venv leaves ``bin/pip`` (or its POSIX wrapper) referencing an
    interpreter that no longer exists or lives under a different tree. The
    reference is compared literally: ``.resolve()`` is not called on it, because
    that would follow ``bin/python3.x`` to the system interpreter and break the
    check on a correctly-located venv.

    Args:
        venv: Path to the ``venv_skillopt`` directory.

    Returns:
        A one-line description, or ``None`` when the venv is consistent or no
        parseable console-script is present.
    """
    text = _script_text(venv)
    if text is None:
        return None
    ref = _interpreter_ref(text)
    if ref is None:
        return None
    expected = venv.resolve()
    ref_path = Path(ref)
    if ref_path.exists() and expected in ref_path.parents:
        return None
    return (
        f"console-script interpreter {ref} is not under {expected} "
        "(venv built for another path)"
    )


def check(venv: Path) -> list[str]:
    """Mismatches between the venv's recorded build path and its location.

    Two independent, whitespace-immune detectors run: the ``pyvenv.cfg``
    ``command`` line (whole-substring match) and pip's console-script
    interpreter (direct shebang or POSIX ``/bin/sh`` wrapper). A venv with
    neither a ``command`` line nor a readable ``bin/pip*`` yields no problem
    (fails open on an exotic venv rather than false-positive on a valid one).

    Args:
        venv: Path to the ``venv_skillopt`` directory to inspect.

    Returns:
        Human-readable mismatch descriptions. Empty means the venv is consistent
        with its current location, or is absent (nothing to check).
    """
    if not venv.is_dir():
        return []
    problems: list[str] = []
    command_problem = _command_line_problem(venv / "pyvenv.cfg", venv)
    if command_problem is not None:
        problems.append(command_problem)
    script_problem = _console_script_problem(venv)
    if script_problem is not None:
        problems.append(script_problem)
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
