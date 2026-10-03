"""Tests for scripts/quality_audit.py (Sprint 050 `U2`, paired with `D6`;
JS/TS path added Sprint 053 `B3`/`B4`, closing `KI-050-6` -- see
`docs/sprints/053-core-pipeline/IMPLEMENTATION_PLAN.md` `D3`/`D4`).

Fixtures are inline source strings written to `tmp_path`, matching the
convention `tests/test_audit_cursor_models.py` already uses -- no committed
fixture directory, so `jurisdictional_lock` has nothing extra to claim.

The JS/TS family tests below reproduce, with a real parser, the five
failure families the Sprint 050 stdlib-only heuristic scanner could not
survive (`docs/sprints/050-core-pipeline/SPRINT_LOG.md` lines ~150-260,
Gate rounds 2-3): arrow over-detection, unenclosed module-level callbacks,
nested-arrow depth loss, control-keyword method names, and regex-literal
masking desync. Every expected figure is hand-computed in the test's own
comments before being asserted, then was independently confirmed by
running the implementation once (not the other way around).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import quality_audit as qa

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
    """The printed register names the file:line, PASS/UNPARSED and the figure."""
    good = tmp_path / "good.py"
    good.write_text("def ok():\n    return 1\n", encoding="utf-8")
    unparsed = tmp_path / "weird.py"
    unparsed.write_text("def broken(:\n    pass\n", encoding="utf-8")

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


# --------------------------------------------------------------------------
# JS/TS: real measurement via tree-sitter (Sprint 053 `D3`/`D4`, `KI-050-6`).
# A directory mixing `.py` and `.js`/`.ts` files: both languages are
# measured for real, and the exit code reflects the combined violations.
# --------------------------------------------------------------------------


def test_js_files_are_measured_not_skipped_mixed_with_python(tmp_path: Path) -> None:
    """A `.py`/`.js`/`.ts` directory: every language is measured for real
    (never a `not_measured` placeholder -- that instrument was withdrawn in
    Sprint 050 and superseded here, `D3`), and the exit code reflects the
    combined violations, checked both clean and violating."""
    js_source = "function foo(a, b) {\n  return a + b;\n}\n"

    clean_dir = tmp_path / "clean"
    clean_dir.mkdir()
    (clean_dir / "ok.py").write_text("def ok():\n    return 1\n", encoding="utf-8")
    (clean_dir / "sample.js").write_text(js_source, encoding="utf-8")
    (clean_dir / "types.ts").write_text(js_source, encoding="utf-8")

    report = qa.format_report(qa.audit([clean_dir]))
    # 3 real PASS units (ok, foo x2), 0 unparsed, 0 not_measured.
    assert "3/3 (100.0%)" in report
    assert "not measured" not in report
    assert qa.main([str(clean_dir)]) == 0

    violating_dir = tmp_path / "violating"
    violating_dir.mkdir()
    statements = "\n    ".join(f"x{i} = {i}" for i in range(55))
    (violating_dir / "bad.py").write_text(
        f"def many_statements():\n    {statements}\n", encoding="utf-8"
    )
    (violating_dir / "sample.js").write_text(js_source, encoding="utf-8")

    assert qa.main([str(violating_dir)]) == 2


# --------------------------------------------------------------------------
# The five Sprint 050 failure families (`SPRINT_LOG.md` lines ~150-260),
# reproduced against the tree-sitter path. Each figure below was derived by
# hand from the D3 unit-of-measure rules, then confirmed by one execution of
# `qa.audit`/`qa.scan_js_file` against the same source (never the reverse).
# --------------------------------------------------------------------------


def test_family1_arrow_chain_is_not_over_detected_as_unparsed(tmp_path: Path) -> None:
    """Sprint 050 finding: ANY `ident =>` occurrence anywhere in a file made
    the stdlib heuristic report the whole file UNPARSED, even a normal,
    fully-measurable declared function with idiomatic inline callbacks. A
    real parser never confuses a call argument for a top-level construct.

    Hand computation: `processItems` is a module-level function (depth 0),
    so its body starts at depth 1; its body is one `return` statement (1
    executable line, depth 1 -> `max_depth=1`). Each of the three arrows
    (`x => x + 1`, `x => x > 0`, `(acc, x) => acc + x`) is discovered
    nested inside that same `return` statement -- a generic leaf statement
    passes discovery through at its OWN depth (1), so each arrow is found
    at depth 1 and its own body starts at `depth + 1 = 2`. Each is
    expression-bodied -- fixed size 1 (`D3`) -- so every arrow measures
    `lines=1 depth=2`.
    """
    source = (
        "function processItems(items) {\n"
        "  return items.map(x => x + 1).filter(x => x > 0)"
        ".reduce((acc, x) => acc + x, 0);\n"
        "}\n"
    )
    path = tmp_path / "chain.js"
    path.write_text(source, encoding="utf-8")

    units = qa.scan_js_file(path, qa._load_grammars())

    assert all(u.status != "unparsed" for u in units)
    assert len(units) == 4  # processItems + 3 arrows
    outer = next(u for u in units if u.name == "processItems")
    assert (outer.executable_lines, outer.max_depth, outer.status) == (1, 1, "PASS")
    arrows = [u for u in units if u.name != "processItems"]
    assert len(arrows) == 3
    assert all((u.executable_lines, u.max_depth, u.status) == (1, 2, "PASS") for u in arrows)


def test_family2_module_level_unenclosed_callback_is_its_own_unit(tmp_path: Path) -> None:
    """Sprint 050 finding: a callback passed straight to a module-level call
    (`app.get('/', function(req, res) {...})`, no enclosing named function
    or binding) produced zero register entries -- neither measured nor
    `unparsed` -- silently absent (`F-049-7` recurring).

    Hand computation: the `function(req, res) {...}` expression is found
    inside the top-level `expression_statement` at module depth 0 (no
    enclosing binding, so its name is `<anonymous>:1`); its body starts at
    depth 1 and holds 2 statements (`const users = ...;`, `res.send(...);`),
    each on its own line -> 2 executable lines, max depth 1.
    """
    source = (
        "app.get('/users', function(req, res) {\n"
        "  const users = getUsers();\n"
        "  res.send(users);\n"
        "});\n"
    )
    path = tmp_path / "unenclosed.js"
    path.write_text(source, encoding="utf-8")

    units = qa.scan_js_file(path, qa._load_grammars())

    assert len(units) == 1
    unit = units[0]
    assert unit.name == "<anonymous>:1"
    assert (unit.executable_lines, unit.max_depth, unit.status) == (2, 1, "PASS")


def test_family2_bare_param_unenclosed_callback_over_50_lines_fails(tmp_path: Path) -> None:
    """Same family, bare-parameter arrow form (`req => {...}`, the specific
    construct the Sprint 050 heuristic's over-broad bare-arrow signal
    mis-detected -- SPRINT_LOG.md finding 'Arrow-function over-correction').
    51 statements -> 51 executable lines (> 50) -> FAIL, not silently
    dropped and not UNPARSED."""
    statements = "\n  ".join(f"const a{i} = {i};" for i in range(51))
    source = f"app.get('/users', req => {{\n  {statements}\n}});\n"
    path = tmp_path / "bare_unenclosed.js"
    path.write_text(source, encoding="utf-8")

    units = qa.scan_js_file(path, qa._load_grammars())

    assert len(units) == 1
    assert (units[0].executable_lines, units[0].status) == (51, "FAIL")


def test_family3_nested_method_depth_in_returned_object_is_not_lost(tmp_path: Path) -> None:
    """Sprint 050 finding: a method nested inside an object literal returned
    by an expression-bodied arrow (`(arr) => ({ [Symbol.iterator]() {...} })`)
    had its depth hard-coded to 1 by the heuristic's `covered_spans`
    mechanism, so real nesting inside it (`for`/`if`/`while`) was silently
    lost -- 100% compliant, exit 0, on a genuinely deep construct.

    Hand computation: `makeIter` is an expression-bodied arrow at module
    depth 0 -> fixed size 1, own depth = 0 + 1 = 1 (D3), regardless of what
    is nested inside the returned object. Discovery of the returned
    expression starts at the arrow's body level (depth 1), because the arrow
    is an ancestor of everything inside it. The computed-key method
    `[Symbol.iterator]` is therefore found at depth 1 and its body starts at
    depth 2. Its one statement, `for (const x of arr) {...}`, sits at depth 2
    (header line credited, depth_box=2); `if (x) {...}` nested inside, at
    depth 3 (header line, depth_box=3); `while (x) {...}` nested inside that,
    at depth 4 (header line, depth_box=4); `break;` inside the while, at
    depth 5 (depth_box=5) -- its ancestors are arrow, method, for, if, while.
    Four distinct header/leaf rows -> 4 executable lines, max depth 5
    (violates the JS/TS `D3` limit of 3, mirroring the Python
    `max_indentation` threshold) -- FAIL, not the old bogus `depth=1 PASS`.
    """
    source = (
        "const makeIter = (arr) => ({\n"
        "  [Symbol.iterator]() {\n"
        "    for (const x of arr) {\n"
        "      if (x) {\n"
        "        while (x) {\n"
        "          break;\n"
        "        }\n"
        "      }\n"
        "    }\n"
        "  }\n"
        "});\n"
    )
    path = tmp_path / "nested_depth.js"
    path.write_text(source, encoding="utf-8")

    units = qa.scan_js_file(path, qa._load_grammars())

    assert len(units) == 2
    make_iter = next(u for u in units if u.name == "makeIter")
    assert (make_iter.executable_lines, make_iter.max_depth, make_iter.status) == (1, 1, "PASS")
    method = next(u for u in units if u.name != "makeIter")
    assert method.name == "[Symbol.iterator]"
    assert (method.executable_lines, method.max_depth, method.status) == (4, 5, "FAIL")


def test_family4_control_keyword_method_names_are_measured(tmp_path: Path) -> None:
    """Sprint 050 finding: a class method NAMED after a control keyword
    (`catch`, `if`, `for`, `while`, `with`, `switch`) was skipped by the
    heuristic's `_is_control_paren`/`JS_KEYWORDS` check -- a 58-statement
    `catch(onRejected)` scored 1/1 (100%) compliant, exit 0, the literal
    `F-049-7` pattern on a Promise-idiomatic method name. A real parser has
    no such confusion: `catch` in method-name position is a
    `property_identifier`, not the `catch` keyword.

    Hand computation: the class is at module depth 0, so its members are
    discovered at depth 1 and each method's own body starts at depth 2
    (mirrors the existing Python class-method convention -- see
    `test_python_compliant_function_passes`-adjacent class fixtures in this
    module's history). `catch` holds 5 statements (`const a0`..`a4`) -> 5
    executable lines, depth 2, PASS. `if`/`for`/`while` each hold 1
    statement -> 1 executable line, depth 2, PASS. None is silently
    skipped -- the whole point of this family.
    """
    source = (
        "class Deferred {\n"
        "  catch(onRejected) {\n"
        "    const a0 = 0;\n"
        "    const a1 = 1;\n"
        "    const a2 = 2;\n"
        "    const a3 = 3;\n"
        "    const a4 = 4;\n"
        "  }\n"
        "  if(x) {\n"
        "    return x;\n"
        "  }\n"
        "  for(x) {\n"
        "    return x;\n"
        "  }\n"
        "  while(x) {\n"
        "    return x;\n"
        "  }\n"
        "}\n"
    )
    path = tmp_path / "control_keyword_methods.js"
    path.write_text(source, encoding="utf-8")

    units = qa.scan_js_file(path, qa._load_grammars())

    by_name = {u.name: u for u in units}
    assert set(by_name) == {"catch", "if", "for", "while"}
    assert (by_name["catch"].executable_lines, by_name["catch"].max_depth) == (5, 2)
    for name in ("if", "for", "while"):
        assert (by_name[name].executable_lines, by_name[name].max_depth) == (1, 2)
    assert all(u.status == "PASS" for u in units)


def test_family5_regex_literal_with_quotes_does_not_desync_masking(tmp_path: Path) -> None:
    """Sprint 050 finding: a regex literal containing a quote character
    (`/^["']|["']$/g`) desynced the heuristic's naive quote-tracking state
    across the rest of the file, silently erasing every later function from
    the register (`total scanned: 0`, exit 0). Tree-sitter parses a regex
    literal as its own `regex` node, never touching string-tracking state,
    so nothing after it can be masked away.

    Hand computation: `afterRegex` holds 51 `const` statements -> 51
    executable lines (> 50), depth 1 -> FAIL, correctly measured and
    reported, not silently dropped.
    """
    statements = "\n  ".join(f"const a{i} = {i};" for i in range(51))
    regex_line = "const RE = /^[\"']|[\"']$/g;\n"  # the exact SPRINT_LOG desync trigger
    source = regex_line + f"function afterRegex() {{\n  {statements}\n}}\n"
    path = tmp_path / "regex_desync.js"
    path.write_text(source, encoding="utf-8")

    units = qa.scan_js_file(path, qa._load_grammars())

    assert len(units) == 1  # only afterRegex -- RE is a plain variable, not a unit
    assert units[0].name == "afterRegex"
    assert (units[0].executable_lines, units[0].status) == (51, "FAIL")


# --------------------------------------------------------------------------
# .ts / .tsx grammar selection (`D3`): distinct grammars from plain JS.
# --------------------------------------------------------------------------


def test_ts_file_uses_the_typescript_grammar(tmp_path: Path) -> None:
    """A `.ts` file with type annotations parses cleanly under the
    TypeScript grammar (the plain JS grammar rejects type syntax)."""
    source = "function typed(a: number, b: number): number {\n  return a + b;\n}\n"
    path = tmp_path / "typed.ts"
    path.write_text(source, encoding="utf-8")

    units = qa.scan_js_file(path, qa._load_grammars())

    assert len(units) == 1
    assert units[0].status == "PASS"
    assert units[0].executable_lines == 1


def test_tsx_file_uses_the_tsx_grammar(tmp_path: Path) -> None:
    """A `.tsx` file with JSX parses cleanly under the TSX grammar."""
    source = (
        "function Component(props: { name: string }) {\n"
        "  return <div>{props.name}</div>;\n"
        "}\n"
        "const Arrow = () => <span>hi</span>;\n"
    )
    path = tmp_path / "component.tsx"
    path.write_text(source, encoding="utf-8")

    units = qa.scan_js_file(path, qa._load_grammars())

    assert len(units) == 2
    by_name = {u.name: u for u in units}
    assert by_name["Component"].status == "PASS"
    assert by_name["Arrow"].status == "PASS"
    assert by_name["Arrow"].executable_lines == 1  # expression-bodied JSX arrow


# --------------------------------------------------------------------------
# Threshold boundaries (`D3`): 50 vs 51 executable lines; depth 3 vs 4.
# --------------------------------------------------------------------------


def test_js_50_executable_lines_passes_51_fails(tmp_path: Path) -> None:
    """Exact boundary: 50 statements PASS, 51 FAIL -- mirrors the Python
    `MAX_EXECUTABLE_LINES` boundary tests above."""
    fifty = "\n  ".join(f"const b{i} = {i};" for i in range(50))
    ok_path = tmp_path / "fifty.js"
    ok_path.write_text(f"app.get('/x', req => {{\n  {fifty}\n}});\n", encoding="utf-8")
    fifty_one = "\n  ".join(f"const b{i} = {i};" for i in range(51))
    bad_path = tmp_path / "fifty_one.js"
    bad_path.write_text(f"app.get('/x', req => {{\n  {fifty_one}\n}});\n", encoding="utf-8")

    ok_units = qa.scan_js_file(ok_path, qa._load_grammars())
    bad_units = qa.scan_js_file(bad_path, qa._load_grammars())

    assert (ok_units[0].executable_lines, ok_units[0].status) == (50, "PASS")
    assert (bad_units[0].executable_lines, bad_units[0].status) == (51, "FAIL")


def test_js_nesting_depth_3_passes_depth_4_fails(tmp_path: Path) -> None:
    """Exact boundary: 2 nested `if`s -> depth 3 PASS; 3 nested `if`s ->
    depth 4 FAIL. Hand computation (mirrors the Python `_scan_stmts`
    convention this path deliberately reproduces): a module-level function's
    body starts at depth 1; each nested `if`'s header is recorded at its
    enclosing depth and its own body is one level deeper, so N nested `if`s
    put the innermost `return` at depth `N + 1`."""
    ok_source = (
        "function depthOk(a, b) {\n"
        "  if (a) {\n"
        "    if (b) {\n"
        "      return 1;\n"
        "    }\n"
        "  }\n"
        "  return 0;\n"
        "}\n"
    )
    bad_source = (
        "function depthBad(a, b, c) {\n"
        "  if (a) {\n"
        "    if (b) {\n"
        "      if (c) {\n"
        "        return 1;\n"
        "      }\n"
        "    }\n"
        "  }\n"
        "  return 0;\n"
        "}\n"
    )
    ok_path = tmp_path / "depth_ok.js"
    ok_path.write_text(ok_source, encoding="utf-8")
    bad_path = tmp_path / "depth_bad.js"
    bad_path.write_text(bad_source, encoding="utf-8")

    ok_units = qa.scan_js_file(ok_path, qa._load_grammars())
    bad_units = qa.scan_js_file(bad_path, qa._load_grammars())

    assert (ok_units[0].max_depth, ok_units[0].status) == (3, "PASS")
    assert (bad_units[0].max_depth, bad_units[0].status) == (4, "FAIL")


# --------------------------------------------------------------------------
# Comment-only and blank rows are not executable (`D3`): "rows covered by
# statement nodes of the body, excluding comment-only and blank rows".
# --------------------------------------------------------------------------


def _measure_js_function(tmp_path: Path, source: str, name: str) -> int:
    path = tmp_path / f"{name}.js"
    path.write_text(source, encoding="utf-8")
    units = {u.name: u for u in qa.scan_js_file(path, qa._load_grammars())}
    return units[name].executable_lines


def test_js_comment_and_blank_rows_in_function_body_are_not_executable(tmp_path: Path) -> None:
    """Hand derivation (`D3`): rows 2-4 are `//` comment-only, row 6 is
    blank; the statement rows are row 5 (`const a = 1;`) and row 7
    (`return a;`) -> 2 executable lines. The defect measured 5 (the three
    comment rows were credited as statement rows)."""
    source = (
        "function withComments(){\n"
        "  // c1\n"
        "  // c2\n"
        "  // c3\n"
        "  const a = 1;\n"
        "\n"
        "  return a;\n"
        "}\n"
    )
    assert _measure_js_function(tmp_path, source, "withComments") == 2


def test_js_comment_and_blank_rows_in_switch_case_are_not_executable(tmp_path: Path) -> None:
    """Hand derivation (`D3`): row 2 is the `switch` header row (a block
    header is one statement row); rows 3 and 7 (`case 1:`/`default:`) are
    labels, not statements; row 4 (`//`), row 5 (blank) and rows 8-9 (a
    two-row `/* */`) are not executable; statement rows are 6 (`return 1;`)
    and 10 (`return 0;`) -> rows {2, 6, 10} = 3."""
    source = (
        "function sw(x) {\n"
        "  switch (x) {\n"
        "    case 1:\n"
        "      // note\n"
        "\n"
        "      return 1;\n"
        "    default:\n"
        "      /* a\n"
        "         b */\n"
        "      return 0;\n"
        "  }\n"
        "}\n"
    )
    assert _measure_js_function(tmp_path, source, "sw") == 3


def test_js_comment_and_blank_rows_in_catch_block_are_not_executable(tmp_path: Path) -> None:
    """Hand derivation (`D3`): row 2 is the `try` header row, row 3 is
    `risky();`, row 4 is the `} catch (e) {` clause row (not a statement
    row), row 5 (`//`) and row 6 (blank) are not executable, row 7 is
    `log(e);` -> rows {2, 3, 7} = 3. The defect credited row 5 -> 4."""
    source = (
        "function ct() {\n"
        "  try {\n"
        "    risky();\n"
        "  } catch (e) {\n"
        "    // swallow\n"
        "\n"
        "    log(e);\n"
        "  }\n"
        "}\n"
    )
    assert _measure_js_function(tmp_path, source, "ct") == 3


def test_js_multirow_block_comment_in_function_body_is_not_executable(tmp_path: Path) -> None:
    """Hand derivation (`D3`): rows 2-4 are one `/* ... */` spanning three
    rows, none a statement row; statement rows are 5 (`const a = 1;`) and 6
    (`return a;`) -> 2."""
    source = (
        "function blk() {\n"
        "  /* a\n"
        "     b\n"
        "     c */\n"
        "  const a = 1;\n"
        "  return a;\n"
        "}\n"
    )
    assert _measure_js_function(tmp_path, source, "blk") == 2


def test_js_trailing_comment_does_not_reduce_the_count(tmp_path: Path) -> None:
    """Hand derivation (`D3`): rows 2 and 3 each hold a statement plus a
    trailing comment; a row holding a statement is a statement row, so the
    comment must not remove it -> 2."""
    source = (
        "function tr() {\n"
        "  const a = 1; // trailing\n"
        "  return a; /* t */\n"
        "}\n"
    )
    assert _measure_js_function(tmp_path, source, "tr") == 2


# --------------------------------------------------------------------------
# UNPARSED on a genuine syntax error (`D4`) -- never silently skipped, never
# silently compliant, and (unlike the withdrawn Sprint 050 instrument) also
# makes `main()` exit 2 outside `--report`.
# --------------------------------------------------------------------------


def test_js_syntax_error_is_unparsed_and_exits_2(tmp_path: Path) -> None:
    path = tmp_path / "broken.js"
    path.write_text("function broken( {\n  return 1;\n", encoding="utf-8")

    units = qa.scan_js_file(path, qa._load_grammars())

    assert len(units) == 1
    assert units[0].status == "unparsed"
    assert "has_error" in units[0].reason
    assert qa.main([str(path)]) == 2


# --------------------------------------------------------------------------
# Fail closed when tree_sitter cannot be imported (`D4`) -- never a silent
# skip. Simulated via `sys.modules`, restored after each test.
# --------------------------------------------------------------------------


def test_missing_tree_sitter_exits_2_naming_the_install_command(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A JS/TS file in scope with `tree_sitter` unimportable -> exit 2,
    naming `pip install -r requirements-quality.txt` (`D4`) -- never a
    skip, never a `not_measured`/`unparsed` placeholder standing in for a
    real answer."""
    path = tmp_path / "sample.js"
    path.write_text("function f() {\n  return 1;\n}\n", encoding="utf-8")
    for name in ("tree_sitter", "tree_sitter_javascript", "tree_sitter_typescript"):
        monkeypatch.setitem(sys.modules, name, None)  # `import X` raises ImportError

    code = qa.main([str(path)])
    err = capsys.readouterr().err

    assert code == 2
    assert "pip install -r requirements-quality.txt" in err


def test_load_grammars_raises_tree_sitter_import_error_not_bare_import_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Unit-level check: `_load_grammars` itself raises the named
    exception, so a caller needs one except clause (`D4`)."""
    monkeypatch.setitem(sys.modules, "tree_sitter", None)

    with pytest.raises(qa.TreeSitterImportError):
        qa._load_grammars()


def test_python_only_tree_never_imports_tree_sitter(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`D5`: a tree with no JS/TS file never calls `_load_grammars` --
    proven by making it raise if called, on a Python-only directory."""

    def _must_not_be_called() -> None:
        raise AssertionError("_load_grammars must not be called for a Python-only tree")

    monkeypatch.setattr(qa, "_load_grammars", _must_not_be_called)
    (tmp_path / "ok.py").write_text("def ok():\n    return 1\n", encoding="utf-8")

    units = qa.audit([tmp_path])

    assert len(units) == 1
    assert units[0].status == "PASS"


# --------------------------------------------------------------------------
# Decorators (Sprint 052 `D8`, `#13`): a decorator line sits in
# `decorator_list`, outside `FunctionDef.body` -- it must never count toward
# the executable-line total. Regression guard: the instrument already
# behaves this way (`_measure_python_unit` measures `func.body` only).
# --------------------------------------------------------------------------


def test_decorator_line_excluded_from_executable_line_count(tmp_path: Path) -> None:
    """A single-line decorator is outside `FunctionDef.body` -- `D8`."""
    source = (
        "@some_decorator\n"
        "def decorated():\n"
        "    a = 1\n"
        "    b = 2\n"
        "    return a + b\n"
    )
    path = tmp_path / "dec.py"
    path.write_text(source, encoding="utf-8")

    units = qa.scan_python_file(path)

    assert len(units) == 1
    unit = units[0]
    assert unit.name == "decorated"
    assert unit.executable_lines == 3  # a, b, return -- decorator line excluded
    assert unit.status == "PASS"


def test_multiline_decorator_excluded_from_executable_line_count(tmp_path: Path) -> None:
    """A decorator call spanning several source lines is still entirely
    outside `FunctionDef.body` -- `D8`."""
    source = (
        "@some_decorator(\n"
        "    option_one=True,\n"
        "    option_two=False,\n"
        ")\n"
        "def decorated():\n"
        "    a = 1\n"
        "    b = 2\n"
        "    return a + b\n"
    )
    path = tmp_path / "multidec.py"
    path.write_text(source, encoding="utf-8")

    units = qa.scan_python_file(path)

    assert len(units) == 1
    unit = units[0]
    assert unit.executable_lines == 3  # a, b, return -- all decorator lines excluded
    assert unit.status == "PASS"


# --------------------------------------------------------------------------
# Exclusions (Sprint 052 `D1`): `config/quality_audit_exclusions.json` names
# files the scan skips entirely. Absent file -> no exclusions, not an error.
# A stale entry (path no longer exists) or a malformed file -> exit 2, same
# shape as RA-16's stale-exception check (`scripts/verify_references.py`
# check (d)). `--report` lists excluded files separately so an exclusion is
# never silent.
# --------------------------------------------------------------------------


def _write_exclusions(path: Path, entries: list[dict[str, object]]) -> None:
    """Write a minimal, schema-valid `quality_audit_exclusions.json` fixture."""
    path.write_text(
        json.dumps({"_doc": "test fixture", "exclusions": entries}), encoding="utf-8"
    )


def test_absent_exclusions_file_is_not_an_error(tmp_path: Path) -> None:
    """No `quality_audit_exclusions.json` on disk -> empty exclusion set,
    not a raised error (`D1`)."""
    missing = tmp_path / "config" / "quality_audit_exclusions.json"

    assert qa.load_exclusions(missing, tmp_path) == frozenset()


def test_excluded_file_violations_do_not_fail_the_scan(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A file named in `exclusions` is skipped entirely: its violations
    never enter the register or the exit-code decision (`D1`)."""
    monkeypatch.chdir(tmp_path)
    statements = "\n    ".join(f"x{i} = {i}" for i in range(55))
    (tmp_path / "bad.py").write_text(
        f"def many_statements():\n    {statements}\n", encoding="utf-8"
    )
    (tmp_path / "good.py").write_text("def ok():\n    return 1\n", encoding="utf-8")
    exclusions_path = tmp_path / "quality_audit_exclusions.json"
    _write_exclusions(
        exclusions_path,
        [{"path": "bad.py", "reason": "vendored", "provenance": {"source": "test"}}],
    )

    exclude = qa.load_exclusions(exclusions_path, tmp_path)
    units = qa.audit([Path(".")], exclude)
    assert [u.name for u in units] == ["ok"]

    code = qa.main([".", "--exclusions", str(exclusions_path)])
    assert code == 0


def test_stale_exclusion_entry_exits_2(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """An exclusion `path` that no longer exists is a stale exemption ->
    exit 2, naming the entry in stderr (`D1`)."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "good.py").write_text("def ok():\n    return 1\n", encoding="utf-8")
    exclusions_path = tmp_path / "quality_audit_exclusions.json"
    _write_exclusions(
        exclusions_path,
        [{"path": "no_longer_here.py", "reason": "vendored", "provenance": {}}],
    )

    code = qa.main([".", "--exclusions", str(exclusions_path)])
    err = capsys.readouterr().err

    assert code == 2
    assert "no_longer_here.py" in err
    assert "stale" in err.lower()


def test_stale_exclusion_entry_raises_from_load_exclusions(tmp_path: Path) -> None:
    """Unit-level check: `load_exclusions` itself raises on a stale entry."""
    exclusions_path = tmp_path / "quality_audit_exclusions.json"
    _write_exclusions(
        exclusions_path,
        [{"path": "ghost.py", "reason": "vendored", "provenance": {}}],
    )

    with pytest.raises(qa.ExclusionError, match="ghost.py"):
        qa.load_exclusions(exclusions_path, tmp_path)


def test_malformed_exclusions_file_exits_2(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Invalid JSON in the exclusions file -> exit 2 (`D1`)."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "good.py").write_text("def ok():\n    return 1\n", encoding="utf-8")
    exclusions_path = tmp_path / "quality_audit_exclusions.json"
    exclusions_path.write_text("{not valid json", encoding="utf-8")

    code = qa.main([".", "--exclusions", str(exclusions_path)])
    err = capsys.readouterr().err

    assert code == 2
    assert "malformed" in err.lower()


def test_exclusion_entry_missing_required_key_raises(tmp_path: Path) -> None:
    """An entry without `path`/`reason`/`provenance` is malformed (`D1`)."""
    exclusions_path = tmp_path / "quality_audit_exclusions.json"
    _write_exclusions(exclusions_path, [{"path": "x.py", "reason": "vendored"}])

    with pytest.raises(qa.ExclusionError):
        qa.load_exclusions(exclusions_path, tmp_path)


def test_report_lists_excluded_files_separately(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """`--report` names the excluded file and its count distinctly from the
    unit register, and never folds it into the compliance figure (`D1`)."""
    monkeypatch.chdir(tmp_path)
    statements = "\n    ".join(f"x{i} = {i}" for i in range(55))
    (tmp_path / "vendored.py").write_text(
        f"def many_statements():\n    {statements}\n", encoding="utf-8"
    )
    (tmp_path / "good.py").write_text("def ok():\n    return 1\n", encoding="utf-8")
    exclusions_path = tmp_path / "quality_audit_exclusions.json"
    _write_exclusions(
        exclusions_path,
        [{"path": "vendored.py", "reason": "vendored", "provenance": {"source": "test"}}],
    )

    code = qa.main(["--report", ".", "--exclusions", str(exclusions_path)])
    out = capsys.readouterr().out

    assert code == 0
    assert "Excluded files: 1" in out
    assert "vendored.py" in out
    assert "vendored.py" not in out.split("Excluded files:")[0]  # not in the unit register
    assert "1/1 (100.0%)" in out  # only good.py counts toward compliant
