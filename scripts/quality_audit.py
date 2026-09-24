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
- Every arrow-function header (`=>`), wherever it occurs -- bound to a binding
  (`const foo = (...) => { ... }`), or unbound/anonymous, at any nesting
  level, including a bare call-argument callback with no enclosing named
  function or binding (`app.get('/', (req, res) => { ... })`, `app.get('/',
  req => { ... })`), parenthesised or single bare parameter, `async` or not.
  A block-bodied arrow (`=> { ... }`) is always measured as its own unit --
  named after its binding when the arrow is `const`/`let`/`var`-bound,
  `<anonymous>` otherwise (the same treatment an anonymous
  `function (...) {...}` already gets). A **bound** arrow with an expression
  body (`const f = x => x + 1;`, no `{}`) is measured as a 1-line unit
  (`C`). An **unbound** expression-bodied arrow (`.map(x => x + 1)`, not
  assigned to a binding) has no separately countable body of its own and is
  not its own unit -- its characters fall inside whatever source range
  encloses it, the same as any other statement, never `unparsed` on that
  account alone (`F-049-8`).
- **Fail-closed conservation check (`A`)**, run after every recogniser above,
  in two independent halves -- neither trusts that the recogniser it checks
  caught everything, both verify it:
  - `) {` **coverage**: every `) {` in the masked source is classified as
    either a control-flow block (`if`/`for`/`while`/`catch`/`switch`/`with`
    -- excluded) or a function/method body. If a function/method-shaped
    `) {` is found whose body span was not claimed by any unit created
    above -- e.g. a computed method name (`[Symbol.iterator]() { ... }`), or
    any other header shape the recognisers above do not cover -- the
    **whole file** is reported `unparsed`, citing the offending line.
  - `=> {` **coverage**: every `=> {` in the masked source must likewise fall
    inside a unit `_iter_arrow_units` actually produced. If it does not --
    e.g. a bare arrow parameter literally named `async`
    (`list.map(async => { ... })`), which `_match_arrow_params_backward`
    rejects because `async` is listed in `JS_KEYWORDS` even though it is a
    legal binding identifier there -- the **whole file** is reported
    `unparsed`, citing the offending line.

  Either half can independently trigger `unparsed`, rather than silently
  omitting a body from the register. This is the structural guarantee: a
  function-introducing construct either lands inside a measured unit's line
  range, or the file is `unparsed` -- there is no third, silent outcome.

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
- Any function/method-shaped (`) {`) or arrow-shaped (`=> {`) body the
  recognisers above could not attribute to a unit is caught by the
  fail-closed conservation check (`A`, above) and marks the whole file
  `unparsed`, with the reason citing the offending line.

JS/TS line counting is physical-line granularity (non-blank lines inside the
matched `{ ... }` span, including any nested inner function's lines, which are
therefore double-counted between the outer and inner unit -- e.g. an anonymous
callback argument is counted once as its own unit and again inside whatever
enclosing unit's span contains it, the same declared double-counting Python
nested `def`s already have with their enclosing scope) -- a coarser,
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


def _next_brace_depth(c: str, depth: int) -> int:
    """Depth after consuming one character of a brace-only stream.

    `{` increments, `}` decrements; any other character leaves `depth`
    unchanged. A `}` can only ever take `depth` down to `-1` from `0` here
    (it was never negative on entry -- the caller returns as soon as it is),
    so the caller's single `depth < 0` check catches every unmatched `}`.
    """
    if c == "{":
        return depth + 1
    if c == "}":
        return depth - 1
    return depth


def _has_unbalanced_braces(masked: str) -> bool:
    """True when `masked` is not a well-formed balanced brace sequence.

    A negative depth (an unmatched `}`) or a nonzero depth at end of file (an
    unmatched `{`) both mean the file is truncated or malformed -- brace-depth
    scanning has no reliable answer for it.
    """
    depth = 0
    for c in masked:
        depth = _next_brace_depth(c, depth)
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
    """Index of the `{` opening a function/method body starting at/after
    `idx`, or `None` if what follows isn't a block body (a bare `;` or a
    signature-only declaration, not a countable unit). Arrow bodies (which
    may also take `=> { ... }` or an expression body) are located separately
    by `_arrow_body_span` -- this function only serves `function`/method
    headers, which are never followed by `=>`.
    """
    n = len(text)
    i = idx
    while i < n and text[i] in " \t\r\n":
        i += 1
    return i if i < n and text[i] == "{" else None


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


def _locate_paren_body(masked: str, m: re.Match[str]) -> tuple[int, int] | None:
    """Body span for a `function`/method header match.

    Finds the matching `)` of the parameter list right after the header, then
    confirms a `{` body after it (`_confirm_body_start`). `None` when there is
    no `(` immediately after the header, no matching `)`, or no block body --
    a plain call, or a signature-only declaration, not a unit. Arrow headers
    never reach this function -- see `_arrow_body_span`.
    """
    open_paren = m.end()
    if open_paren >= len(masked) or masked[open_paren] != "(":
        return None
    close_paren = _find_matching(masked, open_paren, "(", ")")
    if close_paren == -1:
        return None
    body_start = _confirm_body_start(masked, close_paren + 1)
    if body_start is None:
        return None
    return body_start, _find_matching(masked, body_start, "{", "}")


def _resolve_header_name(m: re.Match[str]) -> str | None:
    """Unit name for one `_HEADER_RE` match (`function`/method only), or
    `None` when `method_name` resolved to a JS reserved keyword (not a real
    header -- e.g. `if (` briefly matching before its `(` is excluded)."""
    if m.group("func_kw") is not None:
        return m.group("func_name") or "<anonymous>"
    name = m.group("method_name") or ""
    return None if name in JS_KEYWORDS else name


def _locate_header_body(masked: str, m: re.Match[str]) -> tuple[str, int, int] | None:
    """Name and body span for one `_HEADER_RE` match (`function`/method), or
    `None` if not a unit. Arrow headers (bound and unbound, block and
    expression body) are handled separately by `_iter_arrow_units` (`B`/`C`).
    """
    name = _resolve_header_name(m)
    if name is None:
        return None
    located = _locate_paren_body(masked, m)
    if located is None:
        return None
    body_start, body_end = located
    if body_end == -1:
        return None
    return name, body_start, body_end


# --------------------------------------------------------------------------
# Arrow-function scanning (`B`/`C`): every `=>` header, bound or not, block
# or expression body -- independent of `_HEADER_RE`, which no longer matches
# arrows at all.
# --------------------------------------------------------------------------


def _find_matching_backward(text: str, close_idx: int, open_ch: str, close_ch: str) -> int:
    """Index of the `open_ch` matching `text[close_idx]` (must be `close_ch`),
    scanning backward, or -1. Mirrors `_find_matching`, reversed; flattened
    (sequential, not nested, ifs) to stay within `max_indentation` (`D`)."""
    depth = 0
    i = close_idx
    while i >= 0:
        if text[i] == close_ch:
            depth += 1
        if text[i] == open_ch:
            depth -= 1
        if depth == 0 and text[i] == open_ch:
            return i
        i -= 1
    return -1


def _match_arrow_params_backward(masked: str, arrow_idx: int) -> tuple[int, int] | None:
    """`(params_start, params_end)` for the parameter head ending right
    before the `=>` at `arrow_idx`, or `None` if what precedes it isn't a
    valid arrow parameter shape -- a parenthesised list or a single bare
    identifier."""
    i = arrow_idx - 1
    while i >= 0 and masked[i] in " \t\r\n":
        i -= 1
    if i < 0:
        return None
    if masked[i] == ")":
        open_idx = _find_matching_backward(masked, i, "(", ")")
        return None if open_idx == -1 else (open_idx, i + 1)
    j = i
    while j >= 0 and (masked[j].isalnum() or masked[j] in "_$"):
        j -= 1
    if j == i:
        return None
    ident = masked[j + 1 : i + 1]
    if not ident or ident in JS_KEYWORDS:
        return None
    return j + 1, i + 1


def _skip_async_backward(masked: str, idx: int) -> int:
    """Start index including a preceding `async` keyword, or `idx` unchanged
    when there isn't one immediately before it."""
    i = idx - 1
    while i >= 0 and masked[i] in " \t\r\n":
        i -= 1
    j = i
    while j >= 0 and masked[j].isalnum():
        j -= 1
    return j + 1 if masked[j + 1 : i + 1] == "async" else idx


def _preceded_by_binding_keyword(masked: str, ident_end: int) -> bool:
    """True when the token immediately before index `ident_end` (exclusive)
    is `const`, `let`, or `var`."""
    i = ident_end
    while i >= 0 and masked[i] in " \t\r\n":
        i -= 1
    k = i
    while k >= 0 and masked[k].isalnum():
        k -= 1
    return masked[k + 1 : i + 1] in ("const", "let", "var")


def _detect_arrow_binding(masked: str, header_start: int) -> str | None:
    """Bound name if `header_start` is directly preceded by `const|let|var
    NAME =`, else `None` (an unbound/anonymous arrow header -- a call
    argument, object-literal property, default parameter, etc.)."""
    i = header_start - 1
    while i >= 0 and masked[i] in " \t\r\n":
        i -= 1
    if i < 0 or masked[i] != "=":
        return None
    i -= 1
    while i >= 0 and masked[i] in " \t\r\n":
        i -= 1
    j = i
    while j >= 0 and (masked[j].isalnum() or masked[j] in "_$"):
        j -= 1
    name = masked[j + 1 : i + 1]
    if not name or name in JS_KEYWORDS:
        return None
    return name if _preceded_by_binding_keyword(masked, j) else None


def _classify_expr_char(c: str, depth: int) -> str:
    """Classify one masked character for `_locate_expression_body_end`:
    `"open"` (a nested `(`/`[`/`{`), `"close"` (closes a nested one, still
    inside the expression), `"stop"` (this char ends the expression body --
    an unmatched close bracket, `;`, or newline at depth 0), or `"other"`."""
    if c in "([{":
        return "open"
    if c in ")]}":
        return "stop" if depth == 0 else "close"
    if depth == 0 and c in ";\n":
        return "stop"
    return "other"


def _locate_expression_body_end(masked: str, start: int) -> int:
    """End index (exclusive) of a single-statement expression-arrow body
    starting at `start` (`C`) -- a coarse single-statement scan, not a full
    expression parser."""
    depth = 0
    i = start
    n = len(masked)
    while i < n:
        kind = _classify_expr_char(masked[i], depth)
        if kind == "stop":
            break
        if kind == "open":
            depth += 1
        if kind == "close":
            depth -= 1
        i += 1
    return i


def _skip_ws_forward(masked: str, idx: int) -> int:
    """First index at/after `idx` that isn't whitespace."""
    i = idx
    while i < len(masked) and masked[i] in " \t\r\n":
        i += 1
    return i


def _block_arrow_span(masked: str, body_idx: int) -> tuple[int, int, int, int, bool] | None:
    """`(body_start, body_end, executable_lines, max_depth, True)` for a
    block-bodied arrow whose `{` is at `body_idx`, or `None` if its `}` never
    closes (malformed -- the caller's caller reports the file `unparsed` via
    the pre-existing unbalanced-braces check, never silently)."""
    body_end = _find_matching(masked, body_idx, "{", "}")
    if body_end == -1:
        return None
    lines, depth = _measure_js_body(masked, body_idx, body_end)
    return body_idx, body_end, lines, depth, True


def _expression_arrow_span(masked: str, body_idx: int) -> tuple[int, int, int, int, bool]:
    """`(body_start, body_end, executable_lines, 1, False)` for an
    expression-bodied arrow starting at `body_idx` (`C`)."""
    body_end = _locate_expression_body_end(masked, body_idx)
    span = masked[body_idx:body_end]
    lines = sum(1 for line in span.split("\n") if line.strip())
    return body_idx, body_end, max(lines, 1), 1, False


def _arrow_body_span(masked: str, arrow_idx: int) -> tuple[int, int, int, int, bool] | None:
    """`(body_start, body_end, executable_lines, max_depth, is_block)` for
    the body following the `=>` at `arrow_idx` -- a block body
    (`_block_arrow_span`) or a single expression body
    (`_expression_arrow_span`, `C`)."""
    body_idx = _skip_ws_forward(masked, arrow_idx + 2)
    if body_idx < len(masked) and masked[body_idx] == "{":
        return _block_arrow_span(masked, body_idx)
    return _expression_arrow_span(masked, body_idx)


def _iter_arrow_units(
    masked: str,
) -> list[tuple[str, int, int, int, int, int]]:
    """Every arrow-function header in `masked`:
    `(name, lineno, body_start, body_end, executable_lines, max_depth)`.

    Covers block-bodied arrows regardless of binding (bound or anonymous --
    `B`) and bound expression-bodied arrows (`C`). An *unbound*
    expression-bodied arrow (an inline callback like `.map(x => x + 1)`) has
    no separately countable body and is not itself a unit -- it is folded
    into whatever source range encloses it, unchanged from before this fix.
    """
    results: list[tuple[str, int, int, int, int, int]] = []
    for m in re.finditer(r"=>", masked):
        params = _match_arrow_params_backward(masked, m.start())
        if params is None:
            continue
        header_start = _skip_async_backward(masked, params[0])
        bound_name = _detect_arrow_binding(masked, header_start)
        span = _arrow_body_span(masked, m.start())
        if span is None:
            continue
        body_start, body_end, executable_lines, max_depth, is_block = span
        if not is_block and bound_name is None:
            continue
        name = bound_name if bound_name is not None else "<anonymous>"
        lineno = masked.count("\n", 0, header_start) + 1
        results.append((name, lineno, body_start, body_end, executable_lines, max_depth))
    return results


# --------------------------------------------------------------------------
# Fail-closed conservation check (`A`): every `) {` is either a control-flow
# block or a function/method body -- if the latter and uncovered, `unparsed`.
# --------------------------------------------------------------------------

_CONTROL_KEYWORDS = frozenset({"if", "for", "while", "catch", "switch", "with"})
_PAREN_BRACE_RE = re.compile(r"\)\s*\{")


def _is_control_paren(masked: str, open_paren_idx: int) -> bool:
    """True when `open_paren_idx` opens an `if`/`for`/`while`/`catch`/
    `switch`/`with` condition, not a function/method parameter list."""
    i = open_paren_idx - 1
    while i >= 0 and masked[i] in " \t\r\n":
        i -= 1
    j = i
    while j >= 0 and masked[j].isalnum():
        j -= 1
    return masked[j + 1 : i + 1] in _CONTROL_KEYWORDS


def _find_unattributed_function_body(
    masked: str, covered_spans: list[tuple[int, int]]
) -> int | None:
    """1-based line of the first `) {` function/method header whose body is
    not covered by any measured unit's span, or `None` if every such header
    is accounted for (`A`).

    A `)` directly followed by `{` is either a control-flow block
    (`_is_control_paren`, excluded) or a function/method body -- there is no
    third JS construct shaped this way. This check covers only that `) {`
    shape; a `)` closing an arrow's parameter list is followed by `=>`, never
    directly by `{`, so `_PAREN_BRACE_RE` never matches an arrow header.
    Arrow headers (`=> {`) get their own independent check,
    `_find_unattributed_arrow_body` -- this function does not verify arrow
    coverage and must not be read as doing so.
    """
    for m in _PAREN_BRACE_RE.finditer(masked):
        open_paren = _find_matching_backward(masked, m.start(), "(", ")")
        if open_paren == -1 or _is_control_paren(masked, open_paren):
            continue
        body_start = m.end() - 1
        if not any(start <= body_start <= end for start, end in covered_spans):
            return masked.count("\n", 0, body_start) + 1
    return None


_ARROW_BRACE_RE = re.compile(r"=>\s*\{")


def _find_unattributed_arrow_body(
    masked: str, covered_spans: list[tuple[int, int]]
) -> int | None:
    """1-based line of the first `=> {` arrow header whose body is not
    covered by any unit `_iter_arrow_units` produced, or `None` if every
    such header is accounted for.

    This is the arrow-side counterpart to `_find_unattributed_function_body`
    (`A`, extended). It does not trust that `_iter_arrow_units` recognised
    every arrow header -- it independently locates every `=> {` occurrence
    and verifies its body span is covered by a unit that recogniser actually
    produced. This is a real gap, not a hypothetical one:
    `_match_arrow_params_backward` rejects a bare parameter whose identifier
    is listed in `JS_KEYWORDS`, but `async` in that set is a contextual
    keyword, not a reserved word -- `list.map(async => { ... })` is valid JS
    with a parameter literally named `async`, and before this check existed
    that arrow's body silently produced zero units rather than being
    measured or reported `unparsed`.
    """
    for m in _ARROW_BRACE_RE.finditer(masked):
        body_start = m.end() - 1
        if not any(start <= body_start <= end for start, end in covered_spans):
            return masked.count("\n", 0, body_start) + 1
    return None


def scan_js_file(path: Path) -> list[Unit]:
    """All recognised function/arrow/method units in one JS/TS file.

    Returns one `unparsed` unit (never a partial scan) when
    `_detect_unparsed_reason` finds JSX, a decorator, or (for `.ts`)
    type-level syntax -- or when either half of the fail-closed conservation
    check (`A`) finds a header-shaped body no recogniser above attributed to
    a unit: `_find_unattributed_function_body` for `) {` (function/method)
    headers, `_find_unattributed_arrow_body` for `=> {` (arrow) headers. Both
    run independently and either can trigger `unparsed` on its own.
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
    covered_spans: list[tuple[int, int]] = []
    for m in _HEADER_RE.finditer(masked):
        located = _locate_header_body(masked, m)
        if located is None:
            continue
        name, body_start, body_end = located
        lineno = masked.count("\n", 0, m.start()) + 1
        executable_lines, max_depth = _measure_js_body(masked, body_start, body_end)
        units.append(
            Unit(path, name, lineno, executable_lines, max_depth, "js",
                 _status(executable_lines, max_depth))
        )
        covered_spans.append((body_start, body_end))

    for name, lineno, body_start, body_end, executable_lines, max_depth in _iter_arrow_units(
        masked
    ):
        units.append(
            Unit(path, name, lineno, executable_lines, max_depth, "js",
                 _status(executable_lines, max_depth))
        )
        covered_spans.append((body_start, body_end))

    gap_line = _find_unattributed_function_body(masked, covered_spans)
    if gap_line is None:
        gap_line = _find_unattributed_arrow_body(masked, covered_spans)
    if gap_line is not None:
        reason = (
            f"function-introducing header at line {gap_line} produced a "
            "block body no recognised unit could be attributed to"
        )
        return [Unit(path, "<file>", gap_line, 0, 0, "js", "unparsed", reason)]
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
