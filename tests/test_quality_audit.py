"""Tests for scripts/quality_audit.py (Sprint 050 `U2`, paired with `D6`;
JS/TS scanner withdrawn `AB1` -- see `docs/sprints/050-core-pipeline/
SPRINT_LOG.md` `AB0`/`AB1`).

Fixtures are inline source strings written to `tmp_path`, matching the
convention `tests/test_audit_cursor_models.py` already uses -- no committed
fixture directory, so `jurisdictional_lock` has nothing extra to claim.
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
# JS/TS: instrument withdrawn (Sprint 050 Abort 1, `AB1`) -- the scanner
# (`scan_js_file` and its private helpers) no longer exists; JS/TS files
# must still be discovered and reported, never silently dropped and never
# counted as compliant.
# --------------------------------------------------------------------------


def test_js_files_reported_not_measured_never_compliant_exit_reflects_python_only(
    tmp_path: Path,
) -> None:
    """A directory mixing `.py` and `.js`/`.ts` files: the JS/TS files are
    reported `not measured (JS/TS instrument withdrawn -- Sprint 050 Abort
    1)`, are never counted toward `compliant`, and the exit code reflects
    only the Python violations present -- checked both clean and violating,
    so presence of unmeasured JS/TS files never masks or manufactures a
    violation (the abort-path recurrence of `F-049-7` this unit exists to
    prevent)."""
    js_source = "function foo(a, b) {\n  return a + b;\n}\n"

    clean_dir = tmp_path / "clean"
    clean_dir.mkdir()
    (clean_dir / "ok.py").write_text("def ok():\n    return 1\n", encoding="utf-8")
    (clean_dir / "sample.js").write_text(js_source, encoding="utf-8")
    (clean_dir / "types.ts").write_text(js_source, encoding="utf-8")

    report = qa.format_report(qa.audit([clean_dir]))
    assert report.count("not measured (JS/TS instrument withdrawn") == 2
    assert "1/1 (100.0%)" in report  # only the Python unit counts toward compliant
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
