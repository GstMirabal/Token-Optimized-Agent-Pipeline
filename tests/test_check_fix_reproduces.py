"""Tests for scripts/check_fix_reproduces.py, built on throwaway git repositories."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import check_fix_reproduces as cfr

BROKEN = "def add(a, b):\n    return a - b\n"
FIXED = "def add(a, b):\n    return a + b\n"
RED_TEST = "def test_add():\n    from calc import add\n    assert add(2, 3) == 5\n"
GREEN_TEST = "def test_add():\n    from calc import add\n    assert add(2, 3) == 5 or True\n"
TRAILER = "Repro: tests/test_calc.py::test_add — fails at {base}"


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=repo, capture_output=True, text=True, check=True
    ).stdout.strip()


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.email", "t@example.com")
    git(tmp_path, "config", "user.name", "Tester")
    git(tmp_path, "config", "commit.gpgsign", "false")
    (tmp_path / "calc.py").write_text(BROKEN)
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-qm", "chore: base")
    return tmp_path


def commit_fix(repo: Path, files: dict[str, str], trailer: str | None, subject: str = "fix(calc): add") -> str:
    base = git(repo, "rev-parse", "HEAD")
    for name, text in files.items():
        (repo / name).parent.mkdir(parents=True, exist_ok=True)
        (repo / name).write_text(text)
    git(repo, "add", "-A")
    msg = subject + "\n\nbody\n"
    if trailer:
        msg += "\n" + trailer.format(base=base[:7]) + "\n"
    git(repo, "commit", "-qm", msg)
    return base


def run(repo: Path, base: str, capsys: pytest.CaptureFixture[str]) -> tuple[int, str]:
    code = cfr.main(["--range", f"{base}..HEAD", "--repo", str(repo)])
    return code, capsys.readouterr().out


def test_red_to_green_fix_is_ok(repo, capsys):
    base = commit_fix(repo, {"calc.py": FIXED, "tests/test_calc.py": RED_TEST}, TRAILER)
    code, out = run(repo, base, capsys)
    assert code == 0
    assert " OK " in out


def test_test_passing_on_parent_is_refused(repo, capsys):
    base = commit_fix(repo, {"calc.py": FIXED, "tests/test_calc.py": GREEN_TEST}, TRAILER)
    code, out = run(repo, base, capsys)
    assert code == 2
    assert "PASSES_ON_PARENT" in out


def test_collection_error_on_parent_is_wrong_failure(repo, capsys):
    top_import = "from calc import add\n\n\ndef test_add():\n    assert add(2, 3) == 5\n"
    fixed = FIXED
    (repo / "calc.py").write_text("def sub(a, b):\n    return a - b\n")
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "chore: rename")
    base = commit_fix(repo, {"calc.py": fixed, "tests/test_calc.py": top_import}, TRAILER)
    code, out = run(repo, base, capsys)
    assert code == 2
    assert "WRONG_FAILURE" in out
    assert "fail by assertion" in out


def test_fix_without_trailer_is_missing_trailer(repo, capsys):
    base = commit_fix(repo, {"calc.py": FIXED}, None)
    code, out = run(repo, base, capsys)
    assert code == 2
    assert "MISSING_TRAILER" in out


def test_manual_trailer_is_skipped(repo, capsys):
    base = commit_fix(repo, {"calc.py": FIXED}, "Repro: manual -- SPRINT_LOG section 3")
    code, out = run(repo, base, capsys)
    assert code == 0
    assert "MANUAL" in out


def test_unsupported_suffix_is_unreplayed(repo, capsys):
    trailer = "Repro: tests/calc_spec.rb::adds — fails at {base}"
    base = commit_fix(repo, {"calc.py": FIXED, "tests/calc_spec.rb": "# t\n"}, trailer)
    code, out = run(repo, base, capsys)
    assert code == 2
    assert "UNREPLAYED" in out
    assert "no runner for tests/calc_spec.rb" in out


def test_test_failing_at_commit_is_refused(repo, capsys):
    always_red = "def test_add():\n    assert False\n"
    base = commit_fix(repo, {"calc.py": FIXED, "tests/test_calc.py": always_red}, TRAILER)
    code, out = run(repo, base, capsys)
    assert code == 2
    assert "FAILS_AT_COMMIT" in out


def test_zero_fix_commits_exits_zero_and_says_so(repo, capsys):
    base = commit_fix(repo, {"calc.py": FIXED}, None, subject="feat(calc): add")
    code, out = run(repo, base, capsys)
    assert code == 0
    assert "0 fix( commits in range" in out


def test_bad_range_exits_two(repo, capsys):
    code = cfr.main(["--range", "nope..HEAD", "--repo", str(repo)])
    assert code == 2
    assert "ERROR" in capsys.readouterr().err


def test_worktree_removed_after_exception(repo, monkeypatch):
    base = commit_fix(repo, {"calc.py": FIXED, "tests/test_calc.py": RED_TEST}, TRAILER)

    def boom(cwd, ids):
        raise RuntimeError("runner exploded")

    monkeypatch.setattr(cfr, "run_pytest", boom)
    with pytest.raises(RuntimeError, match="exploded"):
        cfr.main(["--range", f"{base}..HEAD", "--repo", str(repo)])
    listing = git(repo, "worktree", "list").splitlines()
    assert len(listing) == 1


def test_runner_without_pytest_is_runner_unavailable(repo, tmp_path, capsys):
    base = commit_fix(repo, {"calc.py": FIXED, "tests/test_calc.py": RED_TEST}, TRAILER)
    stub = tmp_path / "nopytest.sh"
    stub.write_text("#!/bin/sh\nexit 1\n")
    stub.chmod(0o755)
    code = cfr.main(["--range", f"{base}..HEAD", "--repo", str(repo), "--python", str(stub)])
    captured = capsys.readouterr()
    assert code == 2
    assert "RUNNER_UNAVAILABLE" in captured.err + captured.out
    assert str(stub) in captured.err + captured.out
    assert "FAILS_AT_COMMIT" not in captured.out
    assert "PASSES_ON_PARENT" not in captured.out
    assert len(git(repo, "worktree", "list").splitlines()) == 1


def test_default_interpreter_prefers_repo_venv(tmp_path):
    venv_python = tmp_path / "venv_skillopt" / "bin" / "python"
    venv_python.parent.mkdir(parents=True)
    venv_python.write_text("")
    assert cfr.resolve_python(tmp_path, None) == str(venv_python)


def test_default_interpreter_falls_back_to_sys_executable(tmp_path):
    assert cfr.resolve_python(tmp_path, None) == sys.executable


def test_explicit_python_overrides_default(tmp_path):
    assert cfr.resolve_python(tmp_path, "/x/python") == "/x/python"


def test_runner_unavailable_names_the_reason(repo, tmp_path, capsys):
    """QA Gate 1 round 2 R2-2: the preflight's cause reaches the operator."""
    base = commit_fix(repo, {"calc.py": FIXED, "tests/test_calc.py": RED_TEST}, TRAILER)
    missing = tmp_path / "absent" / "python"
    code = cfr.main(["--range", f"{base}..HEAD", "--repo", str(repo), "--python", str(missing)])
    captured = capsys.readouterr()
    assert code == 2
    assert "RUNNER_UNAVAILABLE" in captured.err
    assert "No such file" in captured.err


def test_runner_unavailable_shows_the_pytest_exit(repo, tmp_path, capsys):
    base = commit_fix(repo, {"calc.py": FIXED, "tests/test_calc.py": RED_TEST}, TRAILER)
    stub = tmp_path / "nopytest.sh"
    stub.write_text("#!/bin/sh\necho 'No module named pytest' >&2\nexit 1\n")
    stub.chmod(0o755)
    code = cfr.main(["--range", f"{base}..HEAD", "--repo", str(repo), "--python", str(stub)])
    captured = capsys.readouterr()
    assert code == 2
    assert "No module named pytest" in captured.err


def test_json_only_fix_is_judged_not_skipped(repo, capsys):
    """KI-056-2: a fix( commit whose only non-test file is .json is replayed."""
    base = commit_fix(repo, {"settings.json": "{}\n", "tests/test_calc.py": GREEN_TEST}, TRAILER)
    code, out = run(repo, base, capsys)
    assert "1 fix( commits in range" in out
    assert "PASSES_ON_PARENT" in out
    assert code == 2


@pytest.mark.parametrize(
    "trailer",
    [
        "Repro:tests/test_calc.py::test_add — fails at {base}",
        "Repro: tests/test_calc.py::test_add — because it was broken",
        "Repro: manual — ",
    ],
)
def test_trailer_outside_the_shared_grammar_is_missing_trailer(repo, capsys, trailer):
    """A-4: the replayer accepts exactly the grammar of the commit hook."""
    base = commit_fix(repo, {"calc.py": FIXED, "tests/test_calc.py": RED_TEST}, trailer)
    code, out = run(repo, base, capsys)
    assert code == 2
    assert "MISSING_TRAILER" in out


SETUP_ERROR_TEST = (
    "import pytest\n\n\n"
    "@pytest.fixture\n"
    "def service():\n"
    "    from calc import add\n"
    "    if add(2, 3) != 5:\n"
    "        raise RuntimeError('service is not running')\n\n\n"
    "def test_add(service):\n"
    "    assert True\n"
)


def test_setup_error_on_parent_is_wrong_failure(repo, capsys):
    """B-4: a fixture that raises on the parent is an error, not a reproduction."""
    base = commit_fix(repo, {"calc.py": FIXED, "tests/test_calc.py": SETUP_ERROR_TEST}, TRAILER)
    code, out = run(repo, base, capsys)
    assert code == 2
    assert "WRONG_FAILURE" in out
    assert "setup error" in out


def test_script_runs_under_isolated_mode() -> None:
    """`python3 -I` drops the script directory from `sys.path` (QA1-6)."""
    script = Path(__file__).resolve().parent.parent / "scripts" / "check_fix_reproduces.py"
    result = subprocess.run(
        [sys.executable, "-I", str(script), "--help"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr


JS_TRAILER = "Repro: tests/calc.test.ts::adds — fails at {base}"
PASS_XML = '<testsuites><testsuite><testcase name="adds"/></testsuite></testsuites>'
FAIL_XML = '<testsuites><testsuite><testcase name="adds"><failure message="x"/></testcase></testsuite></testsuites>'
ERROR_XML = '<testsuites><testsuite><testcase name="adds"><error message="x"/></testcase></testsuite></testsuites>'


@pytest.fixture
def js_repo(repo: Path) -> Path:
    (repo / "node_modules").mkdir()
    return repo


def fake_vitest(monkeypatch, parent_xml, commit_xml="", calls=None):
    """Simulated runner: writes fixture JUnit XML instead of running pnpm."""
    real = subprocess.run
    monkeypatch.setattr(cfr.shutil, "which", lambda name: "/fake/pnpm")

    def fake(cmd, *a, **kw):
        if cmd[0] != "pnpm":
            return real(cmd, *a, **kw)
        if calls is not None:
            calls.append(cmd)
        out = next(c for c in cmd if c.startswith("--outputFile=")).split("=", 1)[1]
        on_parent = (Path(kw["cwd"]) / "calc.py").read_text() == BROKEN
        xml = parent_xml if on_parent else commit_xml
        if xml:
            Path(out).write_text(xml)
        return subprocess.CompletedProcess(cmd, 0, "", "")

    monkeypatch.setattr(cfr.subprocess, "run", fake)


def commit_js(repo: Path) -> str:
    return commit_fix(repo, {"calc.py": FIXED, "tests/calc.test.ts": "// t\n"}, JS_TRAILER)


def test_vitest_failure_then_pass_is_ok(js_repo, capsys, monkeypatch):
    calls: list[list[str]] = []
    fake_vitest(monkeypatch, FAIL_XML, PASS_XML, calls)
    code, out = run(js_repo, commit_js(js_repo), capsys)
    assert code == 0
    assert " OK " in out
    assert calls[0][:5] == ["pnpm", "exec", "vitest", "run", "tests/calc.test.ts"]
    assert "-t" in calls[0] and "--reporter=junit" in calls[0]


def test_vitest_error_on_parent_is_wrong_failure(js_repo, capsys, monkeypatch):
    fake_vitest(monkeypatch, ERROR_XML, PASS_XML)
    code, out = run(js_repo, commit_js(js_repo), capsys)
    assert code == 2
    assert "WRONG_FAILURE" in out


def test_vitest_missing_report_is_wrong_failure(js_repo, capsys, monkeypatch):
    fake_vitest(monkeypatch, "", PASS_XML)
    code, out = run(js_repo, commit_js(js_repo), capsys)
    assert code == 2
    assert "WRONG_FAILURE" in out


def test_vitest_pass_on_parent_is_refused(js_repo, capsys, monkeypatch):
    fake_vitest(monkeypatch, PASS_XML, PASS_XML)
    code, out = run(js_repo, commit_js(js_repo), capsys)
    assert code == 2
    assert "PASSES_ON_PARENT" in out


def test_vitest_failing_at_commit_is_refused(js_repo, capsys, monkeypatch):
    fake_vitest(monkeypatch, FAIL_XML, FAIL_XML)
    code, out = run(js_repo, commit_js(js_repo), capsys)
    assert code == 2
    assert "FAILS_AT_COMMIT" in out


def test_missing_node_modules_is_explicit_unreplayed(repo, capsys, monkeypatch):
    fake_vitest(monkeypatch, FAIL_XML, PASS_XML)
    code, out = run(repo, commit_js(repo), capsys)
    assert code == 2
    assert "UNREPLAYED" in out
    assert "no node_modules" in out


def test_missing_pnpm_is_explicit_unreplayed(js_repo, capsys, monkeypatch):
    fake_vitest(monkeypatch, FAIL_XML, PASS_XML)
    monkeypatch.setattr(cfr.shutil, "which", lambda name: None)
    code, out = run(js_repo, commit_js(js_repo), capsys)
    assert code == 2
    assert "UNREPLAYED" in out
    assert "pnpm is not on PATH" in out


# --- SOURCE_TEXT warning (R-8): denylist of five literal substrings, no coverage claim ---

PATTERN_BODIES = {
    "readFileSync(": "    data = lambda: readFileSync('x')\n",
    "?raw": "    data = '?raw'\n",
    ".read_text(": "    data = lambda: Path('calc.py').read_text()\n",
    ".read_bytes(": "    data = lambda: Path('calc.py').read_bytes()\n",
    "open(": "    data = lambda: open('calc.py')\n",
}


def _py_test(body: str) -> str:
    return "def test_add():\n    from calc import add\n" + body + "    assert add(2, 3) == 5\n"


@pytest.mark.parametrize("pattern", sorted(PATTERN_BODIES))
def test_each_pattern_triggers_source_text(repo, capsys, pattern):
    text = _py_test(PATTERN_BODIES[pattern])
    base = commit_fix(repo, {"calc.py": FIXED, "tests/test_calc.py": text}, TRAILER)
    code, out = run(repo, base, capsys)
    sha = git(repo, "rev-parse", "--short=7", "HEAD")
    assert f"SOURCE_TEXT {sha} tests/test_calc.py::test_add: {pattern}" in out
    assert code == 0 and " OK " in out


def test_behaviour_test_has_no_source_text(repo, capsys):
    base = commit_fix(repo, {"calc.py": FIXED, "tests/test_calc.py": RED_TEST}, TRAILER)
    _, out = run(repo, base, capsys)
    assert "SOURCE_TEXT" not in out


def test_source_text_does_not_change_verdict_or_exit(repo, capsys):
    text = _py_test(PATTERN_BODIES["open("]).replace("== 5", "== 5 or True")
    base = commit_fix(repo, {"calc.py": FIXED, "tests/test_calc.py": text}, TRAILER)
    code, out = run(repo, base, capsys)
    assert "SOURCE_TEXT" in out and "PASSES_ON_PARENT" in out
    assert code == 2


def test_class_qualified_id_resolves_to_method(repo, capsys):
    text = (
        "class TestCalc:\n    def test_add(self):\n        from calc import add\n"
        "        data = lambda: open('calc.py')\n        assert add(2, 3) == 5\n"
    )
    trailer = "Repro: tests/test_calc.py::TestCalc::test_add — fails at {base}"
    base = commit_fix(repo, {"calc.py": FIXED, "tests/test_calc.py": text}, trailer)
    code, out = run(repo, base, capsys)
    assert code == 0
    assert "TestCalc::test_add: open(" in out
    assert "function not located" not in out


def test_hit_in_sibling_function_does_not_trigger(repo, capsys):
    text = RED_TEST + "\n\ndef test_other():\n    open('calc.py')\n"
    base = commit_fix(repo, {"calc.py": FIXED, "tests/test_calc.py": text}, TRAILER)
    _, out = run(repo, base, capsys)
    assert "SOURCE_TEXT" not in out


def test_unlocated_python_function_falls_back_to_whole_file(repo):
    sha_base = commit_fix(repo, {"calc.py": FIXED, "tests/test_calc.py": "x = open('a')\n"}, TRAILER)
    sha = git(repo, "rev-parse", "HEAD")
    lines = cfr.source_text_hits(repo, sha, ["tests/test_calc.py::test_add"])
    assert sha_base and lines == [
        f"SOURCE_TEXT {sha[:7]} tests/test_calc.py::test_add: open( (whole file: function not located)"
    ]


def test_js_id_inspects_whole_file(repo):
    js = "import fs from 'fs';\nconst a = 1;\ntest('t', () => {});\nfs.readFileSync('x');\n"
    commit_fix(repo, {"calc.py": FIXED, "web/a.test.ts": js}, "Repro: web/a.test.ts::t — fails at {base}")
    sha = git(repo, "rev-parse", "HEAD")
    lines = cfr.source_text_hits(repo, sha, ["web/a.test.ts::t"])
    assert lines == [f"SOURCE_TEXT {sha[:7]} web/a.test.ts::t: readFileSync("]
