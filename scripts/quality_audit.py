"""Deterministic function-length and nesting-depth auditor (Sprint 050 `U2`).

invoked_by: Makefile `quality-audit` target.

Measures the two magnitudes `agents.md §1` names but, before this sprint, left
uninstrumented (`F-049-7`): `max_lines_per_func` (50 executable lines) and
`max_indentation` (block-nesting depth 3, violation at level 4).

Units of measure (`docs/sprints/050-core-pipeline/IMPLEMENTATION_PLAN.md` `D1`/`D2`):

- **Executable lines** (`D1`): statements in the function body, excluding blank
  lines, comment-only lines and the docstring. Not raw span (last line minus
  first line) -- raw span penalises the Google-style `Args:`/`Returns:` blocks
  `agents.md §1 python_style` mandates.
- **Nesting depth** (`D2`): the number of block-introducing ancestors
  (`FunctionDef`, `AsyncFunctionDef`, `ClassDef`, `If`, `For`, `While`, `With`,
  `Try`, `Match`) between a statement and the module root, counted over `ast`
  ancestors, never over character columns. A module-level `def` body is level 1;
  the limit of 3 is exceeded at level 4.

## Python path

Stdlib `ast`. Every `FunctionDef`/`AsyncFunctionDef` anywhere in the module
(including nested defs and methods) is measured as its own unit. A nested
def/class is a boundary for its *enclosing* unit's own measurement -- only its
header line counts toward the enclosing unit's executable-line total and depth,
never the lines inside it -- because the nested construct is measured
separately as its own unit. Counting both would double-count the same source
lines across two reported units.

## JS/TS: instrument withdrawn (Sprint 050 Abort 1, `AB1`)

This module scanned JS/TS files with a stdlib-only brace-depth heuristic
through three remediation rounds; rounds 2 and 3 found four consecutive
`REJECTED`/`charter` gate verdicts, the last two citing silent-absence defect
families present since the instrument's first commit. `IMPLEMENTATION_PLAN.md`'s
pre-declared Abort criterion #1 -- "If a correct-enough JS/TS function-boundary
scan cannot be written in stdlib Python, stop -- do not add a Node parser" --
was invoked; the JS/TS scanner (`scan_js_file` and its private helpers) was
withdrawn entirely rather than shipped with a known-defective heuristic.
JS/TS complexity measurement is re-planned as its own sprint (`KI-050-6`).

JS/TS files are still **discovered**, never silently dropped: each is counted
and reported as `not_measured` (`--report` prints "not measured (JS/TS
instrument withdrawn -- Sprint 050 Abort 1)" per file), and is **never**
counted toward the `compliant` figure or the exit-code decision -- an Abort
that silently ignored JS/TS files and reported `0 violations` on a JS-heavy
repo would be `F-049-7` recurring through the exit door instead of the
scanner (the exact failure this withdrawal exists to avoid).

## CLI

    python3 scripts/quality_audit.py [path ...]   # exit 2 on violation, 0 clean
    python3 scripts/quality_audit.py --report      # prints full register, exit 0

Default path when none is given: `.` (the caller's working directory), walked
recursively excluding `venv_skillopt/`, `node_modules/` and `.git/` -- the same
exclusions the Implementation Plan's own measurement commands use.

Compliance figure: `compliant_units / total_units`, with `unparsed` and
`not_measured` units counted separately and never counted as compliant.

Exit codes:
    0 -- no violation (or any run under `--report`)
    2 -- at least one function-length or nesting-depth violation
"""

from __future__ import annotations

import argparse
import ast
import sys
from dataclasses import dataclass
from pathlib import Path

MAX_EXECUTABLE_LINES = 50
MAX_NESTING_DEPTH = 3

DEFAULT_EXCLUDE_DIRS = frozenset({"venv_skillopt", "node_modules", ".git"})
PY_SUFFIXES = frozenset({".py"})
JS_SUFFIXES = frozenset({".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"})


@dataclass
class Unit:
    """One measured function/method, or one `unparsed`/`not_measured` file
    placeholder."""

    path: Path
    name: str
    lineno: int
    executable_lines: int
    max_depth: int
    language: str
    status: str  # "PASS" | "FAIL" | "unparsed" | "not_measured"
    reason: str = ""


def _status(executable_lines: int, max_depth: int) -> str:
    """PASS/FAIL per `D1`/`D2` thresholds."""
    if executable_lines > MAX_EXECUTABLE_LINES or max_depth > MAX_NESTING_DEPTH:
        return "FAIL"
    return "PASS"


# --------------------------------------------------------------------------
# Python path (ast)
# --------------------------------------------------------------------------

_MATCH_TYPE = getattr(ast, "Match", None)
_TRY_STAR_TYPE = getattr(ast, "TryStar", None)

_DEF_TYPES: tuple[type, ...] = (ast.FunctionDef, ast.AsyncFunctionDef)
_TRY_TYPES: tuple[type, ...] = tuple(t for t in (ast.Try, _TRY_STAR_TYPE) if t is not None)
_BLOCK_STMT_TYPES: tuple[type, ...] = tuple(
    t
    for t in (
        ast.FunctionDef,
        ast.AsyncFunctionDef,
        ast.ClassDef,
        ast.If,
        ast.For,
        ast.AsyncFor,
        ast.While,
        ast.With,
        ast.AsyncWith,
        *_TRY_TYPES,
        _MATCH_TYPE,
    )
    if t is not None
)


def _child_stmt_lists(stmt: ast.stmt) -> list[list[ast.stmt]]:
    """Statement lists nested exactly one block-level deeper than `stmt`."""
    if isinstance(stmt, (ast.If, ast.For, ast.AsyncFor, ast.While)):
        lists = [stmt.body]
        if stmt.orelse:
            lists.append(stmt.orelse)
        return lists
    if isinstance(stmt, (ast.With, ast.AsyncWith)):
        return [stmt.body]
    if isinstance(stmt, _TRY_TYPES):
        lists = [stmt.body]
        lists.extend(handler.body for handler in stmt.handlers)
        if stmt.orelse:
            lists.append(stmt.orelse)
        if stmt.finalbody:
            lists.append(stmt.finalbody)
        return lists
    if _MATCH_TYPE is not None and isinstance(stmt, _MATCH_TYPE):
        return [case.body for case in stmt.cases]
    if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        return [stmt.body]
    return []


def _is_docstring_stmt(stmt: ast.stmt) -> bool:
    """True for the `Expr(Constant(str))` statement `ast.get_docstring` reads."""
    return (
        isinstance(stmt, ast.Expr)
        and isinstance(stmt.value, ast.Constant)
        and isinstance(stmt.value.value, str)
    )


def _measure_python_unit(func: ast.FunctionDef | ast.AsyncFunctionDef, body_depth: int) -> tuple[int, int]:
    """Executable-line count and max nesting depth for one function's own body.

    `body_depth` is the ancestor-count level of statements directly in
    `func.body` (`D2`). Nested `FunctionDef`/`AsyncFunctionDef`/`ClassDef`
    statements are boundaries: only their header line and depth contribute
    here, never their own bodies -- those are measured as separate units.
    """
    body = list(func.body)
    if body and _is_docstring_stmt(body[0]):
        body = body[1:]

    lines: set[int] = set()
    depth_box = [body_depth]

    def scan(stmts: list[ast.stmt], depth: int) -> None:
        for stmt in stmts:
            # Every statement's own depth counts (D2 applies to any statement,
            # not only compound-statement headers) -- a simple `return` two
            # levels inside a single `if` is level 2, not level 1.
            depth_box[0] = max(depth_box[0], depth)
            if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                lines.add(stmt.lineno)
                continue
            if isinstance(stmt, _BLOCK_STMT_TYPES):
                lines.add(stmt.lineno)
                for child_list in _child_stmt_lists(stmt):
                    scan(child_list, depth + 1)
                continue
            end = getattr(stmt, "end_lineno", stmt.lineno) or stmt.lineno
            lines.update(range(stmt.lineno, end + 1))

    scan(body, body_depth)
    return len(lines), depth_box[0]


def _discover_python_units(
    stmts: list[ast.stmt], depth: int, path: Path, out: list[Unit]
) -> None:
    """Recursively find every function/method unit in `stmts` (`depth` ancestors deep)."""
    for stmt in stmts:
        if isinstance(stmt, _DEF_TYPES):
            body_depth = depth + 1
            executable_lines, max_depth = _measure_python_unit(stmt, body_depth)
            out.append(
                Unit(
                    path=path,
                    name=stmt.name,
                    lineno=stmt.lineno,
                    executable_lines=executable_lines,
                    max_depth=max_depth,
                    language="python",
                    status=_status(executable_lines, max_depth),
                )
            )
            _discover_python_units(stmt.body, body_depth, path, out)
        elif isinstance(stmt, _BLOCK_STMT_TYPES):
            for child_list in _child_stmt_lists(stmt):
                _discover_python_units(child_list, depth + 1, path, out)


def scan_python_file(path: Path) -> list[Unit]:
    """All function/method units in one Python file, or one `unparsed` unit."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [
            Unit(path, "<file>", 1, 0, 0, "python", "unparsed", f"could not read: {exc}")
        ]
    try:
        tree = ast.parse(text, filename=str(path))
    except SyntaxError as exc:
        return [Unit(path, "<file>", 1, 0, 0, "python", "unparsed", f"SyntaxError: {exc}")]
    units: list[Unit] = []
    _discover_python_units(tree.body, 0, path, units)
    return units


# --------------------------------------------------------------------------
# File discovery and CLI
# --------------------------------------------------------------------------


def iter_source_files(paths: list[Path]) -> list[Path]:
    """Every Python/JS/TS file under `paths`, excluding `DEFAULT_EXCLUDE_DIRS`."""
    all_suffixes = PY_SUFFIXES | JS_SUFFIXES
    found: set[Path] = set()
    for given in paths:
        if given.is_file():
            if given.suffix.lower() in all_suffixes:
                found.add(given)
            continue
        if not given.is_dir():
            continue
        for child in given.rglob("*"):
            if not child.is_file():
                continue
            if any(part in DEFAULT_EXCLUDE_DIRS for part in child.parts):
                continue
            if child.suffix.lower() in all_suffixes:
                found.add(child)
    return sorted(found)


NOT_MEASURED_REASON = "not measured (JS/TS instrument withdrawn — Sprint 050 Abort 1)"


def _not_measured_unit(path: Path) -> Unit:
    """Placeholder for a JS/TS file the withdrawn scanner no longer measures.

    Counted and reported, never silently dropped and never counted toward the
    `compliant` figure (Sprint 050 `AB1`,
    `docs/sprints/050-core-pipeline/SPRINT_LOG.md` `AB0`/`AB1`) -- the JS/TS
    scanner (`scan_js_file` and its private helpers) was withdrawn after four
    consecutive gate `REJECTED`/`charter` verdicts on stdlib-only JS/TS
    function-boundary detection.
    """
    return Unit(path, "<file>", 1, 0, 0, "js", "not_measured", NOT_MEASURED_REASON)


def audit(paths: list[Path]) -> list[Unit]:
    """Scan `paths`: every Python function/method is measured; every JS/TS
    file is discovered but reported `not_measured` (the JS/TS scanner was
    withdrawn -- Sprint 050 `AB1`), never silently dropped.
    """
    units: list[Unit] = []
    for file_path in iter_source_files(paths):
        if file_path.suffix.lower() in PY_SUFFIXES:
            units.extend(scan_python_file(file_path))
        else:
            units.append(_not_measured_unit(file_path))
    return units


def compliance_figure(units: list[Unit]) -> tuple[int, int, int]:
    """`(compliant, measured, unparsed)`. `measured` excludes `unparsed` units
    and `not_measured` units (JS/TS, instrument withdrawn -- Sprint 050
    `AB1`) alike -- both are folded into the `unparsed` return slot so
    neither bucket is ever counted toward `compliant`."""
    unparsed = sum(1 for u in units if u.status in ("unparsed", "not_measured"))
    measured = len(units) - unparsed
    compliant = sum(1 for u in units if u.status == "PASS")
    return compliant, measured, unparsed


def _format_unit_line(u: Unit) -> str:
    """One register line for `u` -- `not_measured`, `unparsed`, or PASS/FAIL."""
    location = f"{u.path}:{u.lineno}"
    if u.status == "not_measured":
        return f"NOT MEASURED  {location}  ({u.reason})"
    if u.status == "unparsed":
        return f"UNPARSED  {location}  {u.name}  ({u.reason})"
    return f"{u.status}  {location}  {u.name}  lines={u.executable_lines} depth={u.max_depth}"


def format_report(units: list[Unit]) -> str:
    """Full register: one line per unit, plus the compliance figure."""
    lines: list[str] = [_format_unit_line(u) for u in units]
    compliant, measured, unparsed = compliance_figure(units)
    pct = (compliant / measured * 100) if measured else 0.0
    lines.append("")
    lines.append(
        f"Compliant units: {compliant}/{measured} ({pct:.1f}%); "
        f"unparsed: {unparsed}; total scanned: {len(units)}"
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Deterministic function-length and nesting-depth auditor."
    )
    parser.add_argument("paths", nargs="*", type=Path, help="Files or directories to scan")
    parser.add_argument(
        "--report", action="store_true", help="Print the full register and exit 0 regardless"
    )
    args = parser.parse_args(argv)
    targets = args.paths or [Path(".")]

    units = audit(targets)

    if args.report:
        print(format_report(units))
        return 0

    violations = [u for u in units if u.status == "FAIL"]
    if violations:
        print(f"❌ quality_audit: {len(violations)} violation(s)", file=sys.stderr)
        for u in violations:
            print(
                f"   • {u.path}:{u.lineno} {u.name} "
                f"lines={u.executable_lines} depth={u.max_depth}",
                file=sys.stderr,
            )
        return 2
    print(f"[OK] quality_audit: {len(units)} unit(s) scanned, 0 violations")
    return 0


if __name__ == "__main__":
    sys.exit(main())
