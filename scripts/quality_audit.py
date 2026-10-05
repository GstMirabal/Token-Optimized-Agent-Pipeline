"""Deterministic function-length and nesting-depth auditor (Sprint 050 `U2`;
JS/TS path added Sprint 053 `B3`, closing `KI-050-6`).

invoked_by: Makefile `quality-audit` target and `verify` target.

Measures the two magnitudes `agents.md §1` names: `max_lines_per_func` (50
executable lines) and `max_indentation` (block-nesting depth 3, violation at
level 4) -- for Python (stdlib `ast`) and, since Sprint 053, for JS/TS
(`tree-sitter`, `docs/sprints/053-core-pipeline/IMPLEMENTATION_PLAN.md` `D3`).

## Units of measure

- **Executable lines**: rows covered by statement nodes in the unit's body,
  excluding blank rows, comment-only rows and (Python) the docstring -- not
  raw span. An expression-bodied JS/TS arrow counts as 1 (`D3`).
- **Nesting depth**: block-nesting ancestor count from the root, never
  character columns. A module-level function/arrow's body is level 1; the
  limit of 3 is exceeded at level 4. Python ancestors: `FunctionDef`,
  `AsyncFunctionDef`, `ClassDef`, `If`, `For`, `While`, `With`, `Try`,
  `Match`. JS/TS ancestors (`D3`): `function_declaration`,
  `generator_function_declaration`, `function_expression`,
  `generator_function`, `arrow_function`, `method_definition`,
  `class_declaration`/`class`, `if_statement`, `for_statement`,
  `for_in_statement`, `while_statement`, `do_statement`, `try_statement`,
  `switch_statement`.

## Python path

Stdlib `ast`, unchanged since Sprint 050. Every `FunctionDef`/
`AsyncFunctionDef` anywhere in the module (including nested defs and
methods) is measured as its own unit. A nested def/class is a boundary for
its *enclosing* unit's own measurement -- only its header line counts
toward the enclosing unit's executable-line total and depth, never the
lines inside it, because the nested construct is measured separately.

## JS/TS path (Sprint 053 `D3`/`D4`)

`tree-sitter` with the `tree-sitter-javascript` and `tree-sitter-typescript`
grammars (`.ts` and `.tsx` select distinct grammars -- `D3`). A unit is a
`function_declaration`, `generator_function_declaration`,
`function_expression`/`generator_function`, `arrow_function` or
`method_definition`, found anywhere in the tree -- not only at statement
position, unlike Python `def` -- because JS/TS allows a function expression
anywhere an expression is legal (a call argument, an object value, a class
field, ...). `_scan_node` is one recursive walk that both measures the
currently-enclosing unit and discovers every nested unit, mirroring the
Python convention above: a nested unit's header line counts once toward its
enclosing unit; its own body is measured separately, starting one level
deeper (`depth + 1`).

`tree_sitter` is imported lazily, in `_load_grammars`, only when a
non-excluded JS/TS file is in scope (`audit`) -- the nucleus's own tree
(`scripts/`, `hooks/`, `tests/`) ships no JS/TS file, so `make verify`'s
`python3 scripts/quality_audit.py .` under the system interpreter (no
`tree_sitter` installed there) never needs it and stays green.

**Fails closed** (`D4`, superseding the Sprint 050 withdrawal `AB1` --
`KI-050-6`): if `tree_sitter` cannot be imported while a JS/TS file is in
scope, `main()` exits 2 naming `pip install -r requirements-quality.txt` --
never a silent skip. A file whose parse tree has an error
(`root_node.has_error`) yields one `unparsed` unit for the whole file --
non-compliant, never silently dropped and never counted toward `compliant`.

## CLI

    python3 scripts/quality_audit.py [path ...]   # exit 2 on violation, 0 clean
    python3 scripts/quality_audit.py --report      # prints full register, exit 0
                                                    # (unless tree_sitter is
                                                    # missing -- D4 overrides
                                                    # --report's own exit 0)

Default path when none is given: `.` (the caller's working directory), walked
recursively excluding `venv_skillopt/`, `node_modules/` and `.git/` -- the same
exclusions the Implementation Plan's own measurement commands use.

Compliance figure: `compliant_units / total_units`, with `unparsed` units
(Python or JS/TS) counted separately and never counted as compliant.

## Exclusions (Sprint 052 `D1`)

`config/quality_audit_exclusions.json` (schema: `_doc`, `exclusions: [{path,
reason, provenance}]`) names files this scan skips entirely -- their
violations never enter the register or the exit-code decision. An absent
file means no exclusions, not an error. An entry whose `path` no longer
exists under the audited root is a stale exemption and exits `2` (same
shape as `RA-16`'s stale-exception check, `scripts/verify_references.py`
check (d)); so does a malformed file. `--report` lists excluded files
separately (count + paths) so an exclusion is never silent.

Exit codes:
    0 -- no violation (or any run under `--report`, unless `tree_sitter` is
         missing and a non-excluded JS/TS file is in scope)
    2 -- at least one function-length or nesting-depth violation, an
         exclusion-file error (stale entry, malformed file), or a missing
         `tree_sitter` with a JS/TS file in scope (`D4`)
"""

from __future__ import annotations

import argparse
import ast
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from tree_sitter import Language, Node

MAX_EXECUTABLE_LINES = 50
MAX_NESTING_DEPTH = 3

DEFAULT_EXCLUDE_DIRS = frozenset({"venv_skillopt", "node_modules", ".git"})
PY_SUFFIXES = frozenset({".py"})
JS_SUFFIXES = frozenset({".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"})

DEFAULT_EXCLUSIONS_RELPATH = Path("config/quality_audit_exclusions.json")
_REQUIRED_EXCLUSION_KEYS = ("path", "reason", "provenance")


class ExclusionError(Exception):
    """Malformed `quality_audit_exclusions.json`, or an entry whose `path`
    no longer exists (stale exemption -- `D1`)."""


@dataclass
class Unit:
    """One measured function/method, or one `unparsed` file placeholder."""

    path: Path
    name: str
    lineno: int
    executable_lines: int
    max_depth: int
    language: str
    status: str  # "PASS" | "FAIL" | "unparsed"
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


def _scan_stmt(stmt: ast.stmt, depth: int, lines: set[int], depth_box: list[int]) -> None:
    """Record one statement's own line(s)/depth into `lines`/`depth_box`.

    Every statement's own depth counts (`D2` applies to any statement, not
    only compound-statement headers) -- a simple `return` two levels inside
    a single `if` is level 2, not level 1. A nested `FunctionDef`/
    `AsyncFunctionDef`/`ClassDef` is a boundary: only its header line/depth
    is recorded here, never its own body (measured as a separate unit). A
    compound statement recurses into its child blocks via `_scan_stmts`.

    Args:
        stmt: The statement to record.
        depth: `stmt`'s own ancestor-count level (`D2`).
        lines: Executable-line accumulator, mutated in place.
        depth_box: Single-element max-depth accumulator, mutated in place.
    """
    depth_box[0] = max(depth_box[0], depth)
    if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        lines.add(stmt.lineno)
        return
    if isinstance(stmt, _BLOCK_STMT_TYPES):
        lines.add(stmt.lineno)
        for child_list in _child_stmt_lists(stmt):
            _scan_stmts(child_list, depth + 1, lines, depth_box)
        return
    end = getattr(stmt, "end_lineno", stmt.lineno) or stmt.lineno
    lines.update(range(stmt.lineno, end + 1))


def _scan_stmts(stmts: list[ast.stmt], depth: int, lines: set[int], depth_box: list[int]) -> None:
    """Record every statement in `stmts` (all at ancestor level `depth`).

    Args:
        stmts: Statement list to record, one AST block level.
        depth: Ancestor-count level shared by every statement in `stmts`.
        lines: Executable-line accumulator, mutated in place.
        depth_box: Single-element max-depth accumulator, mutated in place.
    """
    for stmt in stmts:
        _scan_stmt(stmt, depth, lines, depth_box)


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
    _scan_stmts(body, body_depth, lines, depth_box)
    return len(lines), depth_box[0]


def _record_python_unit(
    stmt: ast.FunctionDef | ast.AsyncFunctionDef, depth: int, path: Path, out: list[Unit]
) -> None:
    """Measure one function/method `stmt`, append its `Unit` to `out`, and
    recurse into its body (at `depth + 1`) for nested units.

    Args:
        stmt: The function/method definition to measure.
        depth: `stmt`'s own ancestor-count level (`D2`).
        path: Source file `stmt` was found in.
        out: Unit register, appended to in place.
    """
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


def _discover_block_children(stmt: ast.stmt, depth: int, path: Path, out: list[Unit]) -> None:
    """Recurse into every child statement list of a non-def compound `stmt`.

    Args:
        stmt: A block-introducing statement (`If`/`For`/`While`/... ) that is
            not itself a function/method definition.
        depth: `stmt`'s own ancestor-count level (`D2`); children are one
            level deeper.
        path: Source file `stmt` was found in.
        out: Unit register, appended to in place.
    """
    for child_list in _child_stmt_lists(stmt):
        _discover_python_units(child_list, depth + 1, path, out)


def _discover_python_units(
    stmts: list[ast.stmt], depth: int, path: Path, out: list[Unit]
) -> None:
    """Recursively find every function/method unit in `stmts` (`depth` ancestors deep)."""
    for stmt in stmts:
        if isinstance(stmt, _DEF_TYPES):
            _record_python_unit(stmt, depth, path, out)
            continue
        if isinstance(stmt, _BLOCK_STMT_TYPES):
            _discover_block_children(stmt, depth, path, out)


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
# JS/TS path (tree-sitter, Sprint 053 `D3`/`D4`)
# --------------------------------------------------------------------------


class TreeSitterImportError(Exception):
    """`tree_sitter` (or a grammar package) is not importable, but a JS/TS
    file is in scope -- fails closed (`D4`), never a silent skip."""


_TREE_SITTER_INSTALL_HINT = (
    "quality_audit: a JS/TS file is in scope but tree_sitter is not "
    "installed -- run: pip install -r requirements-quality.txt"
)

TsBundle = tuple[Any, Any, Any]
Acc = tuple[set[int], list[int]]

FUNCTION_UNIT_TYPES = frozenset(
    {
        "function_declaration",
        "generator_function_declaration",
        "function_expression",
        "generator_function",
        "arrow_function",
        "method_definition",
    }
)
CLASS_TYPES = frozenset({"class_declaration", "class"})
BLOCK_HEADER_TYPES = frozenset(
    {
        "if_statement",
        "for_statement",
        "for_in_statement",
        "while_statement",
        "do_statement",
        "try_statement",
        "switch_statement",
    }
)
TRANSPARENT_TYPES = frozenset(
    {
        "statement_block",
        "else_clause",
        "catch_clause",
        "finally_clause",
        "switch_body",
        "switch_case",
        "switch_default",
    }
)
_HEADER_FIELDS: dict[str, tuple[str, ...]] = {
    "if_statement": ("condition",),
    "for_statement": ("initializer", "condition", "increment"),
    "for_in_statement": ("left", "right"),
    "while_statement": ("condition",),
    "do_statement": ("condition",),
    "switch_statement": ("value",),
}
_BODY_FIELDS: dict[str, tuple[str, ...]] = {
    "if_statement": ("consequence", "alternative"),
    "for_statement": ("body",),
    "for_in_statement": ("body",),
    "while_statement": ("body",),
    "do_statement": ("body",),
    "try_statement": ("body", "handler", "finalizer"),
    "switch_statement": ("body",),
}


def _load_grammars() -> TsBundle:
    """Import `tree_sitter` and the JS/TS grammar packages -- only called
    when a non-excluded JS/TS file is in scope (`audit`), so the Python-only
    path never imports them (`D5`). Fails closed: raises
    `TreeSitterImportError`, never a silent skip (`D4`)."""
    try:
        import tree_sitter
        import tree_sitter_javascript
        import tree_sitter_typescript
    except ImportError as exc:
        raise TreeSitterImportError(_TREE_SITTER_INSTALL_HINT) from exc
    return tree_sitter, tree_sitter_javascript, tree_sitter_typescript


def _language_for_suffix(suffix: str, ts_bundle: TsBundle) -> Language:
    """`.ts` and `.tsx` select distinct grammars from plain JS (`D3`) --
    TypeScript's type syntax is not valid in the plain JS grammar."""
    ts, ts_js, ts_tsx = ts_bundle
    if suffix == ".ts":
        return ts.Language(ts_tsx.language_typescript())
    if suffix == ".tsx":
        return ts.Language(ts_tsx.language_tsx())
    return ts.Language(ts_js.language())


def _wrapper_children(node: Node) -> list[Node]:
    """Named content children of a transparent wrapper node -- never its
    own keyword/punctuation tokens, so a bare `{` or `case N:` row is never
    credited as if it were a statement."""
    if node.type in ("switch_case", "switch_default"):
        return list(node.children_by_field_name("body"))
    if node.type in ("catch_clause", "finally_clause"):
        body = node.child_by_field_name("body")
        return [body] if body is not None else []
    return list(node.named_children)


def _binding_name(func_node: Node) -> str | None:
    """The declared name, or the binding a function/arrow expression is
    assigned to (`const NAME = ...`, `{ NAME: ... }`, `this.NAME = ...`),
    or a class method's (possibly control-keyword) name -- else None."""
    name_field = func_node.child_by_field_name("name")
    if name_field is not None:
        return name_field.text.decode("utf-8")
    parent = func_node.parent
    if parent is None:
        return None
    if parent.type == "variable_declarator":
        target = parent.child_by_field_name("name")
        return target.text.decode("utf-8") if target is not None else None
    if parent.type == "pair":
        key = parent.child_by_field_name("key")
        return key.text.decode("utf-8") if key is not None else None
    if parent.type == "assignment_expression":
        left = parent.child_by_field_name("left")
        return left.text.decode("utf-8") if left is not None else None
    return None


def _unit_name(func_node: Node) -> str:
    """Declared/bound name, else `<anonymous>:<line>` -- an unnamed unit
    must still be locatable in `--report`."""
    name = _binding_name(func_node)
    return name if name else f"<anonymous>:{func_node.start_point.row + 1}"


def _build_js_unit(
    path: Path, name: str, func_node: Node, executable_lines: int, max_depth: int
) -> Unit:
    """One measured JS/TS `Unit`, PASS/FAIL under the shared `_status`
    thresholds -- `D3` uses the same magnitudes as the Python path."""
    return Unit(
        path=path,
        name=name,
        lineno=func_node.start_point.row + 1,
        executable_lines=executable_lines,
        max_depth=max_depth,
        language="js",
        status=_status(executable_lines, max_depth),
    )


def _measure_function_unit(func_node: Node, depth: int, path: Path, out: list[Unit]) -> None:
    """Measure one `FUNCTION_UNIT_TYPES` node and append its `Unit` to
    `out` (`D3`); `depth` is the node's own ancestor level, so its body
    starts at `depth + 1` -- the same convention as the Python `D2` path.
    """
    body = func_node.child_by_field_name("body")
    if body is None:
        return  # signature-only (TS `method_signature`/`abstract_method_signature`
        # are not in FUNCTION_UNIT_TYPES, so this should not occur)
    name = _unit_name(func_node)
    body_depth = depth + 1
    if body.type != "statement_block":
        # Expression-bodied arrow: fixed size 1 (`D3`); still discover any
        # unit nested in the expression (e.g. an object-literal method).
        _scan_node(body, body_depth, path, out, None)
        out.append(_build_js_unit(path, name, func_node, 1, body_depth))
        return
    lines: set[int] = set()
    depth_box = [body_depth]
    for stmt in body.named_children:
        _scan_node(stmt, body_depth, path, out, (lines, depth_box))
    out.append(_build_js_unit(path, name, func_node, len(lines), depth_box[0]))


def _discover_class_members(class_node: Node, depth: int, path: Path, out: list[Unit]) -> None:
    """Every class-body member is discovered one level deeper than the
    class itself; never contributes lines to any enclosing unit (a method
    is measured as its own unit, `D3`)."""
    class_body = class_node.child_by_field_name("body")
    if class_body is None:
        return
    for member in class_body.named_children:
        _scan_node(member, depth + 1, path, out, None)


def _scan_block_header(
    node: Node, depth: int, path: Path, out: list[Unit], acc: Acc | None
) -> None:
    """Header-expression children (may embed a unit -- an arrow-function
    callback in an `if` condition, say) are discovery-only, at `node`'s own
    depth, never credited to `acc` -- mirrors the Python `D2` single-header-
    line rule (a multi-line condition still counts as one header line).
    Body-content children recurse at `depth + 1`, inheriting `acc`.
    """
    for field in _HEADER_FIELDS.get(node.type, ()):
        header_child = node.child_by_field_name(field)
        if header_child is not None:
            _scan_node(header_child, depth, path, out, None)
    for field in _BODY_FIELDS.get(node.type, ()):
        for body_child in node.children_by_field_name(field):
            _scan_node(body_child, depth + 1, path, out, acc)


def _scan_node(node: Node, depth: int, path: Path, out: list[Unit], acc: Acc | None) -> None:
    """Record `node` into the enclosing unit's `(lines, depth_box)`
    accumulator `acc` (or perform pure discovery when `acc` is None, e.g.
    at module scope) and discover every function/method/class unit nested
    anywhere inside it, at the correct `D3` block-nesting depth.

    Unlike Python `ast.stmt`, a JS/TS function-like node can appear
    anywhere an expression can (a call argument, an object value, ...), so
    discovery and enclosing-unit measurement are the same walk, not two
    passes.
    """
    node_type = node.type
    if node_type == "comment":
        return  # `D3`: comment-only rows are not executable and open no unit
    if acc is not None:
        acc[1][0] = max(acc[1][0], depth)
    if node_type in FUNCTION_UNIT_TYPES:
        if acc is not None:
            acc[0].add(node.start_point.row + 1)
        _measure_function_unit(node, depth, path, out)
        return
    if node_type in CLASS_TYPES:
        if acc is not None:
            acc[0].add(node.start_point.row + 1)
        _discover_class_members(node, depth, path, out)
        return
    if node_type in BLOCK_HEADER_TYPES:
        if acc is not None:
            acc[0].add(node.start_point.row + 1)
        _scan_block_header(node, depth, path, out, acc)
        return
    if node_type in TRANSPARENT_TYPES:
        for child in _wrapper_children(node):
            _scan_node(child, depth, path, out, acc)
        return
    if acc is not None:
        acc[0].update(range(node.start_point.row + 1, node.end_point.row + 2))
    for child in node.named_children:
        _scan_node(child, depth, path, out, acc)


def scan_js_file(path: Path, ts_bundle: TsBundle) -> list[Unit]:
    """All function/method units in one JS/TS file (`D3`), or one
    `unparsed` unit if it cannot be read or its parse tree has an error
    (`D4` -- never silently skipped, never silently compliant)."""
    try:
        source = path.read_bytes()
    except OSError as exc:
        return [Unit(path, "<file>", 1, 0, 0, "js", "unparsed", f"could not read: {exc}")]
    ts, _ts_js, _ts_tsx = ts_bundle
    language = _language_for_suffix(path.suffix.lower(), ts_bundle)
    tree = ts.Parser(language).parse(source)
    if tree.root_node.has_error:
        return [
            Unit(path, "<file>", 1, 0, 0, "js", "unparsed", "parse error (tree-sitter has_error)")
        ]
    units: list[Unit] = []
    for stmt in tree.root_node.named_children:
        _scan_node(stmt, 0, path, units, None)
    return units


# --------------------------------------------------------------------------
# File discovery and CLI
# --------------------------------------------------------------------------


def _add_if_source_file(path: Path, all_suffixes: frozenset[str], found: set[Path]) -> None:
    """Add `path` to `found` if its suffix is a scanned Python/JS/TS suffix.

    Args:
        path: Candidate file.
        all_suffixes: Scanned suffixes (`PY_SUFFIXES | JS_SUFFIXES`).
        found: Accumulator set, mutated in place.
    """
    if path.suffix.lower() in all_suffixes:
        found.add(path)


def _walk_directory(directory: Path, all_suffixes: frozenset[str], found: set[Path]) -> None:
    """Add every non-excluded source file under `directory` (recursive).

    Args:
        directory: Directory to walk.
        all_suffixes: Scanned suffixes (`PY_SUFFIXES | JS_SUFFIXES`).
        found: Accumulator set, mutated in place.
    """
    for child in directory.rglob("*"):
        if not child.is_file():
            continue
        # Only components BELOW the given root count: a root that itself sits
        # under `node_modules/` is scanned (`D1`, Sprint 054).
        if any(part in DEFAULT_EXCLUDE_DIRS for part in child.relative_to(directory).parts):
            continue
        _add_if_source_file(child, all_suffixes, found)


def iter_source_files(paths: list[Path]) -> list[Path]:
    """Every Python/JS/TS file under `paths`, excluding `DEFAULT_EXCLUDE_DIRS`."""
    all_suffixes = PY_SUFFIXES | JS_SUFFIXES
    found: set[Path] = set()
    for given in paths:
        if given.is_file():
            _add_if_source_file(given, all_suffixes, found)
            continue
        if given.is_dir():
            _walk_directory(given, all_suffixes, found)
    return sorted(found)


def _validate_exclusion_entry(entry: object, exclusions_path: Path, root: Path) -> Path:
    """One exclusion entry -> its resolved, existing path.

    Args:
        entry: One element of the `exclusions` list.
        exclusions_path: File the entry came from, for error messages.
        root: Directory the entry's `path` is resolved against (`D1`).

    Returns:
        Path: the resolved, existing excluded file.

    Raises:
        ExclusionError: a required key is missing, or the resolved path does
            not exist (stale exemption).
    """
    if not isinstance(entry, dict) or any(k not in entry for k in _REQUIRED_EXCLUSION_KEYS):
        raise ExclusionError(
            f"{exclusions_path}: entry {entry!r} missing one of "
            f"{_REQUIRED_EXCLUSION_KEYS} -- malformed exclusion."
        )
    resolved = (root / str(entry["path"])).resolve()
    if not resolved.exists():
        raise ExclusionError(
            f"{exclusions_path}: '{entry['path']}' does not exist -- stale exemption."
        )
    return resolved


def load_exclusions(exclusions_path: Path, root: Path) -> frozenset[Path]:
    """Load and validate `config/quality_audit_exclusions.json` (`D1`).

    Args:
        exclusions_path: Path to the exclusion-list file. An absent file
            means no exclusions -- not an error.
        root: Directory each entry's `path` is resolved against (the
            audited root).

    Returns:
        frozenset[Path]: resolved, existing files the scan must skip.

    Raises:
        ExclusionError: the file is malformed (bad JSON, or an entry
            missing `path`/`reason`/`provenance`), or an entry's `path`
            does not exist under `root` (stale exemption).
    """
    if not exclusions_path.exists():
        return frozenset()
    try:
        entries = json.loads(exclusions_path.read_text(encoding="utf-8"))["exclusions"]
        return frozenset(
            _validate_exclusion_entry(entry, exclusions_path, root) for entry in entries
        )
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        raise ExclusionError(
            f"{exclusions_path}: malformed exclusion file -- {exc}"
        ) from exc


def _excluded_files(paths: list[Path], exclude: frozenset[Path]) -> list[Path]:
    """Discovered files skipped by `exclude`, sorted for a stable `--report`.

    Kept separate from the unit register so an exclusion is never silent
    (`D1`) -- `--report` lists these files distinctly from PASS/FAIL/
    unparsed units.

    Args:
        paths: Root paths passed to the audit (files or directories).
        exclude: Resolved paths the exclusion file marked as skipped.
    """
    return sorted(p for p in iter_source_files(paths) if p.resolve() in exclude)


def audit(
    paths: list[Path], exclude: frozenset[Path] = frozenset(), ts_bundle: TsBundle | None = None
) -> list[Unit]:
    """Scan `paths`: every Python function/method and every JS/TS
    function/method/arrow/method-definition unit is measured (`D3`); a
    JS/TS file that fails to parse yields one `unparsed` unit for the whole
    file (`D4`). Files resolved in `exclude` are skipped entirely: their
    violations never enter the register or the exit-code decision (`D1`).
    `tree_sitter` is imported lazily, only if a non-excluded JS/TS file is
    in scope, so a Python-only tree never needs it (`D5`).
    """
    files = iter_source_files(paths)
    js_files = [f for f in files if f.suffix.lower() in JS_SUFFIXES and f.resolve() not in exclude]
    if js_files and ts_bundle is None:
        ts_bundle = _load_grammars()
    units: list[Unit] = []
    for file_path in files:
        if file_path.resolve() in exclude:
            continue
        if file_path.suffix.lower() in PY_SUFFIXES:
            units.extend(scan_python_file(file_path))
        else:
            units.extend(scan_js_file(file_path, ts_bundle))
    return units


def compliance_figure(units: list[Unit]) -> tuple[int, int, int]:
    """`(compliant, measured, unparsed)`. `unparsed` (a file that failed to
    parse, Python or JS/TS alike) is never counted toward `compliant`."""
    unparsed = sum(1 for u in units if u.status == "unparsed")
    measured = len(units) - unparsed
    compliant = sum(1 for u in units if u.status == "PASS")
    return compliant, measured, unparsed


def _format_unit_line(u: Unit) -> str:
    """One register line for `u` -- `unparsed` or PASS/FAIL."""
    location = f"{u.path}:{u.lineno}"
    if u.status == "unparsed":
        return f"UNPARSED  {location}  {u.name}  ({u.reason})"
    return f"{u.status}  {location}  {u.name}  lines={u.executable_lines} depth={u.max_depth}"


def format_report(units: list[Unit], excluded: list[Path] | None = None) -> str:
    """Full register: one line per unit, the compliance figure, and --
    listed separately so an exclusion is never silent (`D1`) -- the
    excluded files."""
    excluded = excluded if excluded is not None else []
    lines: list[str] = [_format_unit_line(u) for u in units]
    compliant, measured, unparsed = compliance_figure(units)
    pct = (compliant / measured * 100) if measured else 0.0
    lines.append("")
    lines.append(
        f"Compliant units: {compliant}/{measured} ({pct:.1f}%); "
        f"unparsed: {unparsed}; total scanned: {len(units)}"
    )
    lines.append(f"Excluded files: {len(excluded)}")
    lines.extend(f"  {p}" for p in excluded)
    return "\n".join(lines)


def _unusable_input_message(targets: list[Path], files: list[Path]) -> str | None:
    """Describe why the scan input is unusable, or `None` when it is usable.

    Args:
        targets: Paths given on the command line.
        files: Source files discovered under `targets`.

    Returns:
        str | None: a message naming the offending paths and the current
        working directory (relative paths are never resolved against a
        repository root), or `None` when every path exists and at least
        one source file was found.
    """
    cwd = Path.cwd()
    missing = [str(t) for t in targets if not (t.is_file() or t.is_dir())]
    if missing:
        return (
            f"quality_audit: path(s) not found: {', '.join(missing)} "
            f"(cwd: {cwd}) -- neither a file nor a directory."
        )
    if not files:
        given = ", ".join(str(t) for t in targets)
        return f"quality_audit: 0 source files found under: {given} (cwd: {cwd})."
    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Deterministic function-length and nesting-depth auditor."
    )
    parser.add_argument("paths", nargs="*", type=Path, help="Files or directories to scan")
    parser.add_argument(
        "--report", action="store_true", help="Print the full register and exit 0 regardless"
    )
    parser.add_argument(
        "--exclusions",
        type=Path,
        default=None,
        help="Exclusion-list file (default: <root>/config/quality_audit_exclusions.json)",
    )
    args = parser.parse_args(argv)
    targets = args.paths or [Path(".")]
    root = Path(".")
    exclusions_path = args.exclusions or (root / DEFAULT_EXCLUSIONS_RELPATH)

    try:
        exclude = load_exclusions(exclusions_path, root)
    except ExclusionError as exc:
        print(f"quality_audit: {exc}", file=sys.stderr)
        return 2

    problem = _unusable_input_message(targets, iter_source_files(targets))
    if problem:
        print(problem, file=sys.stderr)
        return 2

    try:
        units = audit(targets, exclude)
    except TreeSitterImportError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if args.report:
        print(format_report(units, _excluded_files(targets, exclude)))
        return 0

    # `unparsed` counts as a violation here (`D4`): a file the parser could
    # not understand must never exit 0 silently, for Python or JS/TS alike.
    violations = [u for u in units if u.status in ("FAIL", "unparsed")]
    if violations:
        print(f"❌ quality_audit: {len(violations)} violation(s)", file=sys.stderr)
        for u in violations:
            print(f"   • {_format_unit_line(u)}", file=sys.stderr)
        return 2
    n_files = len(iter_source_files(targets)) - len(_excluded_files(targets, exclude))
    print(
        f"[OK] quality_audit: {n_files} file(s), {len(units)} unit(s) scanned, 0 violations"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
