"""Tests for scripts/quality_audit.py (Sprint 050 `U2`, paired with `D6`).

Fixtures are inline source strings written to `tmp_path`, matching the
convention `tests/test_audit_cursor_models.py` already uses -- no committed
fixture directory, so `jurisdictional_lock` has nothing extra to claim.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import quality_audit as qa  # noqa: E402


# --------------------------------------------------------------------------
# Python path: executable-line counting (D1)
# --------------------------------------------------------------------------


def test_python_compliant_function_passes(tmp_path: Path) -> None:
    """Under 50 executable lines and under nesting level 4 -> compliant."""
    source = (
        "def compliant():\n"
        "    a = 1\n"
        "    b = 2\n"
        "    if a:\n"
        "        return a\n"
        "    return b\n"
    )
    path = tmp_path / "ok.py"
    path.write_text(source, encoding="utf-8")

    units = qa.scan_python_file(path)

    assert len(units) == 1
    unit = units[0]
    assert unit.name == "compliant"
    assert unit.status == "PASS"
    assert unit.executable_lines == 5
    assert unit.max_depth <= 3


def test_python_long_docstring_does_not_count_as_executable(tmp_path: Path) -> None:
    """A long docstring would falsely trip raw-span counting; D1 excludes it."""
    doc_lines = "\n    ".join(f"Detail line {i} of the docstring." for i in range(60))
    source = (
        "def long_doc():\n"
        '    """\n'
        f"    {doc_lines}\n"
        '    """\n'
        "    a = 1\n"
        "    b = 2\n"
        "    c = a + b\n"
        "    return c\n"
    )
    path = tmp_path / "doc.py"
    path.write_text(source, encoding="utf-8")
    # Raw span (last line - first line) is nowhere near compliant on its own.
    assert source.count("\n") > 60

    units = qa.scan_python_file(path)

    assert len(units) == 1
    unit = units[0]
    assert unit.executable_lines == 4  # a, b, c, return -- the docstring is excluded
    assert unit.status == "PASS"


def test_python_function_over_50_executable_lines_violates(tmp_path: Path) -> None:
    """Over 50 executable lines -> violation, with the correct line count reported."""
    statements = "\n    ".join(f"x{i} = {i}" for i in range(55))
    source = f"def many_statements():\n    {statements}\n    return x54\n"
    path = tmp_path / "long.py"
    path.write_text(source, encoding="utf-8")

    units = qa.scan_python_file(path)

    assert len(units) == 1
    unit = units[0]
    assert unit.executable_lines == 56  # 55 assignments + 1 return
    assert unit.status == "FAIL"


# --------------------------------------------------------------------------
# Python path: nesting depth (D2)
# --------------------------------------------------------------------------


def test_python_nesting_depth_4_violates(tmp_path: Path) -> None:
    """Nested to level 4+ -> violation (module-level def body is level 1)."""
    source = (
        "def deep():\n"
        "    if a:\n"
        "        if b:\n"
        "            if c:\n"
        "                if d:\n"
        "                    return 1\n"
        "    return 0\n"
    )
    path = tmp_path / "deep.py"
    path.write_text(source, encoding="utf-8")

    units = qa.scan_python_file(path)

    assert len(units) == 1
    unit = units[0]
    assert unit.max_depth >= 4
    assert unit.status == "FAIL"


def test_python_syntax_error_is_unparsed_not_compliant(tmp_path: Path) -> None:
    """A file that fails to parse is `unparsed`, never silently compliant."""
    path = tmp_path / "broken.py"
    path.write_text("def broken(:\n    pass\n", encoding="utf-8")

    units = qa.scan_python_file(path)

    assert len(units) == 1
    assert units[0].status == "unparsed"


# --------------------------------------------------------------------------
# JS/TS path (D4)
# --------------------------------------------------------------------------


def test_js_function_and_arrow_scanned_correctly(tmp_path: Path) -> None:
    """A recognisable `function`/arrow-function construct is scanned, not skipped."""
    source = (
        "function foo(a, b) {\n"
        "  if (a) {\n"
        "    return a;\n"
        "  }\n"
        "  return b;\n"
        "}\n"
        "\n"
        "const bar = (x) => {\n"
        "  return x + 1;\n"
        "};\n"
    )
    path = tmp_path / "sample.js"
    path.write_text(source, encoding="utf-8")

    units = qa.scan_js_file(path)

    names_and_status = {u.name: u.status for u in units}
    assert names_and_status == {"foo": "PASS", "bar": "PASS"}
    foo = next(u for u in units if u.name == "foo")
    assert foo.max_depth == 2  # function body (1) + the nested if block (2)
    bar = next(u for u in units if u.name == "bar")
    assert bar.executable_lines == 1


def test_jsx_file_reported_unparsed(tmp_path: Path) -> None:
    """A JSX file the scanner cannot confidently handle -> unparsed, not compliant."""
    path = tmp_path / "component.tsx"
    path.write_text(
        "function Widget() {\n  return <div>hello</div>;\n}\n", encoding="utf-8"
    )

    units = qa.scan_js_file(path)

    assert len(units) == 1
    assert units[0].status == "unparsed"
    assert units[0].name == "<file>"


def test_ts_type_level_syntax_reported_unparsed(tmp_path: Path) -> None:
    """A .ts file with type-level syntax -> unparsed, not compliant."""
    path = tmp_path / "types.ts"
    path.write_text(
        "interface Point {\n  x: number;\n  y: number;\n}\n"
        "function origin() {\n  return 0;\n}\n",
        encoding="utf-8",
    )

    units = qa.scan_js_file(path)

    assert len(units) == 1
    assert units[0].status == "unparsed"


def test_js_unbalanced_braces_reported_unparsed_not_silently_dropped(
    tmp_path: Path,
) -> None:
    """A malformed/truncated file (unbalanced braces) -> unparsed, never absent.

    Gate 2 finding (F-049-7 follow-up): before the fix this produced an empty
    register (0 entries) -- neither `compliant` nor `unparsed` -- which is
    indistinguishable, at the exit-code level, from a file with no violations.
    """
    path = tmp_path / "truncated.js"
    path.write_text("function foo(a, b) {\n  return a + b;\n", encoding="utf-8")

    units = qa.scan_js_file(path)

    assert len(units) == 1
    assert units[0].status == "unparsed"
    assert units[0].name == "<file>"
    compliant, _measured, unparsed = qa.compliance_figure(units)
    assert compliant == 0
    assert unparsed == 1


def test_js_bound_bare_arrow_expression_body_measured_as_one_line_unit(
    tmp_path: Path,
) -> None:
    """A bound, expression-bodied bare arrow (`const f = x => x + 1;`, no
    `{}`) IS measured -- as a 1-line unit (`C`, Sprint 050 attempt 3). Not
    `unparsed` (the pre-fix over-broad whole-file signal, `F-049-8`) and not
    silently absent either (the defect this row previously asserted, which
    `RA-14` forbids papering over -- a test edited to expect the defect is
    not a fix).
    """
    path = tmp_path / "bare_arrow.js"
    path.write_text("const f = x => x + 1;\n", encoding="utf-8")

    units = qa.scan_js_file(path)

    assert len(units) == 1
    unit = units[0]
    assert unit.name == "f"
    assert unit.status == "PASS"
    assert unit.executable_lines == 1


def test_js_inline_bare_arrow_callbacks_measured_not_unparsed(tmp_path: Path) -> None:
    """Idiomatic inline single-param arrow callbacks (`.map`/`.filter`/
    `.reduce`) inside a normal declared function must be measured as part of
    the enclosing function, not flag the whole file `unparsed` (F-049-8: the
    prior fix's `_BARE_ARROW_SIGNAL_RE` fired on ANY bare arrow anywhere).
    """
    source = (
        "function processItems(items) {\n"
        "  return items.map(x => x + 1)"
        ".filter(x => x > 0)"
        ".reduce((acc, x) => acc + x, 0);\n"
        "}\n"
    )
    path = tmp_path / "process.js"
    path.write_text(source, encoding="utf-8")

    units = qa.scan_js_file(path)

    assert len(units) == 1
    unit = units[0]
    assert unit.name == "processItems"
    assert unit.status == "PASS"
    assert unit.executable_lines < 50
    assert unit.max_depth <= 3


def test_js_bound_bare_arrow_block_body_recognised_and_measured(
    tmp_path: Path,
) -> None:
    """A bare-parameter arrow assigned to a binding, WITH a block body
    (`const f = x => { ... }`), is a recognised function header (`D4`) and
    is measured -- reported FAIL when it exceeds the length threshold, never
    `unparsed` and never silently dropped.
    """
    body_lines = "\n  ".join(f"const x{i} = {i};" for i in range(60))
    source = f"const handler = x => {{\n  {body_lines}\n  return x59;\n}};\n"
    path = tmp_path / "handler.js"
    path.write_text(source, encoding="utf-8")

    units = qa.scan_js_file(path)

    assert len(units) == 1
    unit = units[0]
    assert unit.name == "handler"
    assert unit.status == "FAIL"
    assert unit.executable_lines > 50


# --------------------------------------------------------------------------
# Fail-closed conservation matrix (Sprint 050 attempt 3, `A`/`B`/`C`)
#
# {function decl, function expr, method shorthand, arrow-with-parens,
# arrow-bare} x {block body, expression body} x {bound, module-level call
# argument, call argument nested inside another function}. Not every cell is
# syntactically meaningful (a `function` declaration/expression and a method
# shorthand cannot have an expression body in JS at all), so those cells are
# omitted rather than padded with N/A rows. Every included cell asserts one
# of two outcomes -- MEASURED (>=1 unit, none `unparsed`) or the
# `EXEMPT_EMPTY` cells, the one documented exception (an *unbound*
# expression-bodied arrow has no separately countable body and is folded
# into its enclosing statement, same as before this fix, `F-049-8`) -- never
# silent absence disguised as a clean scan.
# --------------------------------------------------------------------------

MEASURED = "measured"
EXEMPT_EMPTY = "exempt_empty"

_MATRIX_CASES = [
    ("function_decl_block_module", "function foo() { return 1; }\n", MEASURED),
    (
        "function_decl_block_nested",
        "function outer() { function inner() { return 1; } return inner(); }\n",
        MEASURED,
    ),
    ("function_expr_block_bound", "const foo = function() { return 1; };\n", MEASURED),
    (
        "function_expr_block_module_call_arg",
        "setTimeout(function() { return 1; }, 0);\n",
        MEASURED,
    ),
    (
        "function_expr_block_nested_call_arg",
        "function outer() { setTimeout(function() { return 1; }, 0); }\n",
        MEASURED,
    ),
    ("method_shorthand_block_module", "const obj = { method() { return 1; } };\n", MEASURED),
    (
        "method_shorthand_block_nested",
        "function outer() { return { method() { return 1; } }; }\n",
        MEASURED,
    ),
    ("arrow_paren_block_bound", "const f = (x) => { return x; };\n", MEASURED),
    (
        "arrow_paren_block_module_call_arg",
        "app.get('/', (req, res) => { return 1; });\n",
        MEASURED,
    ),
    (
        "arrow_paren_block_nested_call_arg",
        "function outer() { items.forEach((x) => { return x; }); }\n",
        MEASURED,
    ),
    ("arrow_paren_expr_bound", "const f = (x) => x + 1;\n", MEASURED),
    ("arrow_paren_expr_module_call_arg", "items.map((x) => x + 1);\n", EXEMPT_EMPTY),
    (
        "arrow_paren_expr_nested_call_arg",
        "function outer() { return items.map((x) => x + 1); }\n",
        MEASURED,
    ),
    ("arrow_bare_block_bound", "const f = x => { return x; };\n", MEASURED),
    ("arrow_bare_block_module_call_arg", "app.get('/', req => { return 1; });\n", MEASURED),
    (
        "arrow_bare_block_nested_call_arg",
        "function outer() { items.forEach(x => { return x; }); }\n",
        MEASURED,
    ),
    ("arrow_bare_expr_bound", "const f = x => x + 1;\n", MEASURED),
    ("arrow_bare_expr_module_call_arg", "items.map(x => x + 1);\n", EXEMPT_EMPTY),
    (
        "arrow_bare_expr_nested_call_arg",
        "function outer() { return items.map(x => x + 1); }\n",
        MEASURED,
    ),
]


@pytest.mark.parametrize(
    "source,expected_kind", [(src, kind) for _id, src, kind in _MATRIX_CASES],
    ids=[case_id for case_id, _src, _kind in _MATRIX_CASES],
)
def test_conservation_matrix_never_silently_absent(
    tmp_path: Path, source: str, expected_kind: str
) -> None:
    """Every header-kind x body-kind x position cell either measures at
    least one non-`unparsed` unit, or is the single documented exemption
    (an unbound expression-bodied arrow) -- silent absence (0 units, exit 0,
    scored compliant) is never a third outcome (`A`)."""
    path = tmp_path / "case.js"
    path.write_text(source, encoding="utf-8")

    units = qa.scan_js_file(path)

    if expected_kind == EXEMPT_EMPTY:
        assert units == []
        return
    assert len(units) >= 1
    assert all(u.status != "unparsed" for u in units)


# --------------------------------------------------------------------------
# Gate 2 round-2 regression samples: a module-level callback with no
# enclosing named function or binding must never silently vanish (`A`/`B`).
# --------------------------------------------------------------------------


def test_module_level_parenthesised_arrow_callback_not_silently_absent(
    tmp_path: Path,
) -> None:
    """`app.get('/', (req, res) => { <64 lines> });` at module level
    (parenthesised form, exact Gate 2 round-2 sample) -- must be measured (as
    `<anonymous>`, `B`) or `unparsed` (`A`), never 0 entries/exit 0."""
    body = "\n  ".join(f"const x{i} = {i};" for i in range(64))
    source = f"app.get('/', (req, res) => {{\n  {body}\n  return x63;\n}});\n"
    path = tmp_path / "server.js"
    path.write_text(source, encoding="utf-8")

    units = qa.scan_js_file(path)

    assert units != []
    if units[0].status == "unparsed":
        return
    assert units[0].name == "<anonymous>"
    assert units[0].executable_lines > 50
    assert units[0].status == "FAIL"


def test_module_level_bare_arrow_callback_not_silently_absent(tmp_path: Path) -> None:
    """`app.get('/', req => { <62 lines> });` at module level (bare-param
    form, exact Gate 2 round-2 sample) -- must be measured (as `<anonymous>`,
    `B`) or `unparsed` (`A`), never 0 entries/exit 0."""
    body = "\n  ".join(f"const x{i} = {i};" for i in range(62))
    source = f"app.get('/', req => {{\n  {body}\n  return x61;\n}});\n"
    path = tmp_path / "server.js"
    path.write_text(source, encoding="utf-8")

    units = qa.scan_js_file(path)

    assert units != []
    if units[0].status == "unparsed":
        return
    assert units[0].name == "<anonymous>"
    assert units[0].executable_lines > 50
    assert units[0].status == "FAIL"


def test_mixed_file_with_unenclosed_callback_not_scored_100_percent_compliant(
    tmp_path: Path,
) -> None:
    """A file mixing `function small(){return 1;}` with an unenclosed 62-line
    module-level callback must NOT score 100% compliant while the 62-line
    callback goes unmeasured -- the literal `F-049-7` over-credit pattern
    this sprint exists to eliminate. Either the callback becomes its own
    violating unit, or the whole file is `unparsed` (`A`/`B`)."""
    body = "\n  ".join(f"const x{i} = {i};" for i in range(62))
    source = (
        "function small(){return 1;}\n"
        f"app.get('/', req => {{\n  {body}\n  return x61;\n}});\n"
    )
    path = tmp_path / "mixed.js"
    path.write_text(source, encoding="utf-8")

    units = qa.scan_js_file(path)

    assert units != []
    if len(units) == 1 and units[0].status == "unparsed":
        return
    compliant, measured, _unparsed = qa.compliance_figure(units)
    assert not (compliant == measured and measured == 1)


def test_bare_arrow_param_named_async_unattributed_body_reported_unparsed(
    tmp_path: Path,
) -> None:
    """`list.map(async => { ... })` -- a bare-parameter arrow whose parameter
    is literally named `async` -- is valid JS (`async` is a contextual
    keyword, not a reserved word, so it is a legal binding identifier here).

    `_match_arrow_params_backward` rejects it: it checks the identifier
    against `JS_KEYWORDS`, which lists `async`, so `_iter_arrow_units`
    produces zero units for this arrow and its `=> {` body is claimed by no
    covered span. Before the arrow half of the fail-closed conservation
    check existed, this meant `scan_js_file` returned an EMPTY register for
    the file (0 units) -- not `unparsed`, not a violation, indistinguishable
    from a file with nothing to measure -- while a 60-executable-line body
    went completely uncounted. The extended check must catch this and mark
    the whole file `unparsed`, proving the check is load-bearing rather than
    decorative (it fails closed on a real recogniser gap, not a
    hypothetical one).
    """
    body = "\n  ".join(f"const x{i} = {i};" for i in range(60))
    source = f"list.map(async => {{\n  {body}\n  return x59;\n}});\n"
    path = tmp_path / "async_param.js"
    path.write_text(source, encoding="utf-8")

    # Confirm the recogniser gap directly: `_iter_arrow_units` really does
    # miss this header, so the conservation check below is proven, not assumed.
    masked = qa._mask_non_code(source)
    assert qa._iter_arrow_units(masked) == []

    units = qa.scan_js_file(path)

    assert len(units) == 1
    assert units[0].status == "unparsed"
    assert "function-introducing header" in units[0].reason


def test_computed_method_name_unattributed_body_reported_unparsed(tmp_path: Path) -> None:
    """A computed method name (`[Symbol.iterator]() { ... }`) is a real
    function header `_HEADER_RE` does not recognise -- the fail-closed
    conservation check (`A`) must catch this rather than silently drop it.
    Demonstrates `A` guards constructs beyond the specific gaps `B`/`C` fix.
    """
    source = "const obj = {\n  [Symbol.iterator]() {\n    return 1;\n  }\n};\n"
    path = tmp_path / "iterable.js"
    path.write_text(source, encoding="utf-8")

    units = qa.scan_js_file(path)

    assert len(units) == 1
    assert units[0].status == "unparsed"
    assert "function-introducing header" in units[0].reason


# --------------------------------------------------------------------------
# CLI: exit codes and --report
# --------------------------------------------------------------------------


def test_main_exit_2_on_violation(tmp_path: Path) -> None:
    statements = "\n    ".join(f"x{i} = {i}" for i in range(55))
    source = f"def many_statements():\n    {statements}\n"
    path = tmp_path / "bad.py"
    path.write_text(source, encoding="utf-8")

    code = qa.main([str(path)])

    assert code == 2


def test_main_exit_0_when_clean(tmp_path: Path) -> None:
    path = tmp_path / "good.py"
    path.write_text("def ok():\n    return 1\n", encoding="utf-8")

    code = qa.main([str(path)])

    assert code == 0


def test_main_report_exits_0_even_with_violation(tmp_path: Path) -> None:
    """`--report` is informational, not a gate: exit 0 regardless of findings."""
    statements = "\n    ".join(f"x{i} = {i}" for i in range(55))
    source = f"def many_statements():\n    {statements}\n"
    path = tmp_path / "bad.py"
    path.write_text(source, encoding="utf-8")

    code = qa.main(["--report", str(path)])

    assert code == 0


def test_report_output_format(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The printed register names the file:line, PASS/FAIL/unparsed and the figure."""
    good = tmp_path / "good.py"
    good.write_text("def ok():\n    return 1\n", encoding="utf-8")
    unparsed = tmp_path / "weird.tsx"
    unparsed.write_text("function W() { return <div/>; }\n", encoding="utf-8")

    code = qa.main(["--report", str(good), str(unparsed)])
    out = capsys.readouterr().out

    assert code == 0
    assert "PASS" in out
    assert f"{good}:1" in out
    assert "UNPARSED" in out
    assert "unparsed" in out.lower()
    assert "Compliant units:" in out
    # The unparsed unit must not be folded into the compliant count.
    assert "1/1 (100.0%)" in out


# --------------------------------------------------------------------------
# File discovery
# --------------------------------------------------------------------------


def test_iter_source_files_excludes_default_dirs(tmp_path: Path) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "mod.py").write_text("def f():\n    return 1\n", encoding="utf-8")
    excluded_dir = tmp_path / "venv_skillopt" / "lib"
    excluded_dir.mkdir(parents=True)
    (excluded_dir / "vendored.py").write_text("def g():\n    return 1\n", encoding="utf-8")

    files = qa.iter_source_files([tmp_path])

    assert (tmp_path / "src" / "mod.py") in files
    assert not any("venv_skillopt" in p.parts for p in files)


def test_compliance_figure_never_counts_unparsed_as_compliant() -> None:
    units = [
        qa.Unit(Path("a.py"), "a", 1, 1, 1, "python", "PASS"),
        qa.Unit(Path("b.js"), "<file>", 1, 0, 0, "js", "unparsed", "JSX"),
    ]

    compliant, measured, unparsed = qa.compliance_figure(units)

    assert compliant == 1
    assert measured == 1
    assert unparsed == 1
