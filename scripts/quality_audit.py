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

## JS/TS path -- declared scanner limits (`D4`)

No new dependency: a deterministic brace-depth and function-header scanner
written in stdlib Python, not a Node-equivalent parser. It recognises:

- `function` declarations and expressions (named or anonymous, `async`/`*`
  variants), when followed by a `{ ... }` body.
- Class/object method shorthand (`name(params) { ... }`), detected by excluding
  JS reserved keywords from the header-name position -- this also matches
  object-literal method shorthand, not class bodies exclusively.
- Arrow functions assigned to a binding with a parenthesised parameter list
  (`const foo = (...) => { ... }`), when the arrow has a block body. A
  single-bare-parameter arrow without parens (`const f = x => {}`) is NOT
  recognised. An expression-bodied arrow (`const f = (x) => x + 1`, no `{}`)
  has no measurable body and is not counted as a unit.

It explicitly does **not** parse JSX, TypeScript type-level syntax, or
decorators. A file/construct it cannot confidently handle is reported
`unparsed`, never silently counted as compliant (`F-049-7` was precisely a
parser over-crediting itself). Concretely:

- `.jsx` / `.tsx` files are always `unparsed` regardless of content -- embedded
  JSX markup breaks brace-depth scanning.
- Any file whose masked (string/comment-stripped) source contains `</` (a JSX
  closing-tag signature) or a decorator line (`@Name` at line start) is
  `unparsed`.
- `.ts` files carrying *any* colon-type annotation (interfaces, type aliases,
  enums, generic angle brackets, or a plain `: Type` on a parameter/return) are
  `unparsed`. This is deliberately broad -- a `.ts` file mixing typed and
  untyped functions is reported unparsed in full rather than partially scanned,
  because a colon can equally be an object-literal key, and guessing wrong in
  the compliant direction is the exact failure this sprint exists to end.
- A file whose braces do not balance (a truncated or malformed file) is
  `unparsed` -- brace-depth scanning has no reliable answer once the file's
  own braces never close.
- A bare-parameter arrow function without surrounding parentheses (`x => ...`
  rather than `(x) => ...`) makes the whole file `unparsed` -- this is the
  declared arrow-recognition limit above, surfaced in the register instead of
  silently producing zero units.

JS/TS line counting is physical-line granularity (non-blank lines inside the
matched `{ ... }` span, including any nested inner function's lines, which are
therefore double-counted between the outer and inner unit) -- a coarser,
explicitly declared approximation of `D1`, not the AST-exact Python count.
Nesting depth distinguishes block braces (preceded by `)`, `=>`, `else`, `try`,
`do`, `finally`) from object/array-literal braces via the single preceding
token only; it is a heuristic, not a parser.

## CLI

    python3 scripts/quality_audit.py [path ...]   # exit 2 on violation, 0 clean
    python3 scripts/quality_audit.py --report      # prints full register, exit 0

Default path when none is given: `.` (the caller's working directory), walked
recursively excluding `venv_skillopt/`, `node_modules/` and `.git/` -- the same
exclusions the Implementation Plan's own measurement commands use.

Compliance figure: `compliant_units / total_units`, with `unparsed` units
counted separately and never counted as compliant.

Exit codes:
    0 -- no violation (or any run under `--report`)
    2 -- at least one function-length or nesting-depth violation
"""

from __future__ import annotations

import argparse
import ast
import re
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
# JS/TS path (stdlib brace-depth scanner -- D4)
# --------------------------------------------------------------------------

JS_KEYWORDS = frozenset(
    {
        "if", "for", "while", "switch", "catch", "function", "else", "do", "with",
        "return", "typeof", "new", "in", "of", "instanceof", "yield", "await",
        "delete", "void", "throw", "class", "extends", "super", "this", "const",
        "let", "var", "case", "default", "break", "continue", "export", "import",
        "from", "as", "try", "finally", "static", "get", "set", "async",
    }
)

_HEADER_RE = re.compile(
    r"(?P<func_kw>\bfunction\b)\s*\*?\s*(?P<func_name>[A-Za-z_$][\w$]*)?\s*(?=\()"
    r"|\b(?:const|let|var)\s+(?P<arrow_name>[A-Za-z_$][\w$]*)\s*(?::[^=(]*)?=\s*(?:async\s+)?(?=\()"
    r"|(?<![\w$.])(?P<method_name>[A-Za-z_$][\w$]*)\s*(?=\()"
)

_JSX_SIGNAL_RE = re.compile(r"</\s*[A-Za-z]")
_DECORATOR_SIGNAL_RE = re.compile(r"(?m)^\s*@[A-Za-z_$]")
_TS_TYPE_SIGNAL_RE = re.compile(
    r"\binterface\s+[A-Za-z_$]"
    r"|\benum\s+[A-Za-z_$]"
    r"|\btype\s+[A-Za-z_$][\w$]*\s*="
    r"|<[A-Za-z_$][\w$]*(?:\s*,\s*[A-Za-z_$][\w$]*)*>\s*\("
    r"|:\s*[A-Za-z_$]"
)

# A bare identifier immediately followed by `=>` (whitespace only in between)
# is a single-parameter arrow function without surrounding parens -- the
# declared arrow-recognition limit. Excludes `) =>` (a real, recognised
# parenthesised parameter list, whose token immediately before `=>` is `)`,
# not the parameter name).
_BARE_ARROW_SIGNAL_RE = re.compile(r"(?<!\))\b[A-Za-z_$][\w$]*\s*=>")

_KEYWORD_BLOCK_PRECEDERS = frozenset({"else", "try", "do", "finally"})


def _mask_non_code(source: str) -> str:
    """Replace string/comment/template-literal text with spaces.

    Preserves length and every newline position so line numbers computed from
    the masked text stay aligned with the original source. `${ ... }` template
    interpolations re-enter code scanning (including nested braces), because
    JS/TS code inside an interpolation is real code, not literal text.
    """
    out: list[str] = []
    stack: list[dict[str, object]] = [{"state": "code"}]
    i = 0
    n = len(source)
    while i < n:
        top = stack[-1]
        state = top["state"]
        c = source[i]
        nxt = source[i + 1] if i + 1 < n else ""
        if state in ("code", "interp"):
            if c == "/" and nxt == "/":
                stack.append({"state": "linecomment"})
                out.append("  ")
                i += 2
                continue
            if c == "/" and nxt == "*":
                stack.append({"state": "blockcomment"})
                out.append("  ")
                i += 2
                continue
            if c == "'":
                stack.append({"state": "squote"})
                out.append(" ")
                i += 1
                continue
            if c == '"':
                stack.append({"state": "dquote"})
                out.append(" ")
                i += 1
                continue
            if c == "`":
                stack.append({"state": "template"})
                out.append(" ")
                i += 1
                continue
            if state == "interp" and c == "{":
                top["depth"] = int(top.get("depth", 0)) + 1
                out.append(c)
                i += 1
                continue
            if state == "interp" and c == "}":
                depth = int(top.get("depth", 0))
                if depth == 0:
                    stack.pop()
                    out.append(" ")
                else:
                    top["depth"] = depth - 1
                    out.append(c)
                i += 1
                continue
            out.append(c)
            i += 1
            continue
        if state == "linecomment":
            if c == "\n":
                stack.pop()
                out.append("\n")
            else:
                out.append(" ")
            i += 1
            continue
        if state == "blockcomment":
            if c == "*" and nxt == "/":
                stack.pop()
                out.append("  ")
                i += 2
                continue
            out.append("\n" if c == "\n" else " ")
            i += 1
            continue
        if state in ("squote", "dquote"):
            quote = "'" if state == "squote" else '"'
            if c == "\\" and i + 1 < n:
                out.append("  " if source[i + 1] != "\n" else " \n")
                i += 2
                continue
            if c == quote:
                stack.pop()
                out.append(" ")
                i += 1
                continue
            out.append("\n" if c == "\n" else " ")
            i += 1
            continue
        if state == "template":
            if c == "\\" and i + 1 < n:
                out.append("  " if source[i + 1] != "\n" else " \n")
                i += 2
                continue
            if c == "`":
                stack.pop()
                out.append(" ")
                i += 1
                continue
            if c == "$" and nxt == "{":
                stack.append({"state": "interp", "depth": 0})
                out.append("  ")
                i += 2
                continue
            out.append("\n" if c == "\n" else " ")
            i += 1
            continue
        # Unreachable: every pushed state is handled above.
        out.append(c)
        i += 1
    return "".join(out)


def _has_unbalanced_braces(masked: str) -> bool:
    """True when `masked` is not a well-formed balanced brace sequence.

    A negative depth (an unmatched `}`) or a nonzero depth at end of file (an
    unmatched `{`) both mean the file is truncated or malformed -- brace-depth
    scanning has no reliable answer for it.
    """
    depth = 0
    for c in masked:
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth < 0:
                return True
    return depth != 0


def _detect_unparsed_reason(masked: str, suffix: str) -> str | None:
    """A declared-limit reason string, or `None` if the file is confidently scannable."""
    if suffix in (".jsx", ".tsx"):
        return "JSX file extension (.jsx/.tsx): scanner does not parse JSX markup"
    if _has_unbalanced_braces(masked):
        return "unbalanced braces detected: malformed or truncated file"
    if _JSX_SIGNAL_RE.search(masked):
        return "JSX markup detected (`</Tag`): scanner does not parse JSX"
    if _DECORATOR_SIGNAL_RE.search(masked):
        return "decorator syntax detected (`@Name`): scanner does not parse decorators"
    if suffix == ".ts" and _TS_TYPE_SIGNAL_RE.search(masked):
        return "TypeScript type-level syntax detected (interface/type/enum/generic/annotation)"
    if _BARE_ARROW_SIGNAL_RE.search(masked):
        return (
            "bare-parameter arrow function detected (`x =>` without parens): "
            "scanner does not recognise this construct"
        )
    return None


def _find_matching(text: str, open_idx: int, open_ch: str, close_ch: str) -> int:
    """Index of the char matching `text[open_idx]` (which must be `open_ch`), or -1."""
    depth = 0
    i = open_idx
    n = len(text)
    while i < n:
        if text[i] == open_ch:
            depth += 1
        elif text[i] == close_ch:
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def _confirm_body_start(text: str, idx: int) -> int | None:
    """Index of the `{` opening a block body starting at/after `idx`, or `None`.

    Accepts a `{` immediately, or `=>` followed by a `{` (arrow function block
    body). Anything else (`;`, a bare expression, end of file) is a signature
    or expression body, not a countable unit.
    """
    n = len(text)
    i = idx
    while i < n and text[i] in " \t\r\n":
        i += 1
    if i < n and text[i] == "{":
        return i
    if text[i : i + 2] == "=>":
        i += 2
        while i < n and text[i] in " \t\r\n":
            i += 1
        if i < n and text[i] == "{":
            return i
    return None


def _preceding_token(text: str, idx: int) -> str:
    """The significant token immediately before `idx`, skipping whitespace."""
    i = idx - 1
    while i >= 0 and text[i] in " \t\r\n":
        i -= 1
    if i < 0:
        return ""
    if text[i - 1 : i + 1] == "=>":
        return "=>"
    if text[i] == ")":
        return ")"
    j = i
    while j >= 0 and (text[j].isalnum() or text[j] in "_$"):
        j -= 1
    return text[j + 1 : i + 1]


def _measure_js_body(masked: str, body_start: int, body_end: int) -> tuple[int, int]:
    """Executable-line count and max block-nesting depth of one `{ ... }` span.

    `body_start`/`body_end` are the indices of the function's own opening and
    matching closing brace. Object/array-literal braces are excluded from
    depth via `_preceding_token`; only braces preceded by `)`, `=>`, `else`,
    `try`, `do` or `finally` count as block-introducing (heuristic, declared).
    """
    stack: list[bool] = [True]
    depth = 1
    max_depth = 1
    for i in range(body_start + 1, body_end):
        c = masked[i]
        if c == "{":
            prev = _preceding_token(masked, i)
            is_block = prev in (")", "=>") or prev in _KEYWORD_BLOCK_PRECEDERS
            stack.append(is_block)
            if is_block:
                depth += 1
                max_depth = max(max_depth, depth)
        elif c == "}":
            popped = stack.pop() if stack else True
            if popped:
                depth -= 1
    inner = masked[body_start + 1 : body_end]
    executable_lines = sum(1 for line in inner.split("\n") if line.strip())
    return executable_lines, max_depth


def scan_js_file(path: Path) -> list[Unit]:
    """All recognised function/arrow/method units in one JS/TS file.

    Returns one `unparsed` unit (never a partial scan) when `_detect_unparsed_reason`
    finds JSX, a decorator, or (for `.ts`) type-level syntax.
    """
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return [Unit(path, "<file>", 1, 0, 0, "js", "unparsed", f"could not read: {exc}")]

    masked = _mask_non_code(text)
    reason = _detect_unparsed_reason(masked, path.suffix.lower())
    if reason is not None:
        return [Unit(path, "<file>", 1, 0, 0, "js", "unparsed", reason)]

    units: list[Unit] = []
    for m in _HEADER_RE.finditer(masked):
        if m.group("func_kw") is not None:
            name = m.group("func_name") or "<anonymous>"
        elif m.group("arrow_name") is not None:
            name = m.group("arrow_name")
        else:
            name = m.group("method_name") or ""
            if name in JS_KEYWORDS:
                continue

        open_paren = m.end()
        if open_paren >= len(masked) or masked[open_paren] != "(":
            continue
        close_paren = _find_matching(masked, open_paren, "(", ")")
        if close_paren == -1:
            continue
        body_start = _confirm_body_start(masked, close_paren + 1)
        if body_start is None:
            continue
        body_end = _find_matching(masked, body_start, "{", "}")
        if body_end == -1:
            continue

        lineno = masked.count("\n", 0, m.start()) + 1
        executable_lines, max_depth = _measure_js_body(masked, body_start, body_end)
        units.append(
            Unit(
                path=path,
                name=name,
                lineno=lineno,
                executable_lines=executable_lines,
                max_depth=max_depth,
                language="js",
                status=_status(executable_lines, max_depth),
            )
        )
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


def audit(paths: list[Path]) -> list[Unit]:
    """Scan `paths`, returning every measured/unparsed unit found."""
    units: list[Unit] = []
    for file_path in iter_source_files(paths):
        if file_path.suffix.lower() in PY_SUFFIXES:
            units.extend(scan_python_file(file_path))
        else:
            units.extend(scan_js_file(file_path))
    return units


def compliance_figure(units: list[Unit]) -> tuple[int, int, int]:
    """`(compliant, measured, unparsed)`. `measured` excludes `unparsed` units."""
    unparsed = sum(1 for u in units if u.status == "unparsed")
    measured = len(units) - unparsed
    compliant = sum(1 for u in units if u.status == "PASS")
    return compliant, measured, unparsed


def format_report(units: list[Unit]) -> str:
    """Full register: one line per unit, plus the compliance figure."""
    lines: list[str] = []
    for u in units:
        location = f"{u.path}:{u.lineno}"
        if u.status == "unparsed":
            lines.append(f"UNPARSED  {location}  {u.name}  ({u.reason})")
        else:
            lines.append(
                f"{u.status}  {location}  {u.name}  "
                f"lines={u.executable_lines} depth={u.max_depth}"
            )
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
