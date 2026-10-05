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


def test_non_python_test_is_unreplayed(repo, capsys):
    trailer = "Repro: tests/calc.test.ts::adds — fails at {base}"
    base = commit_fix(repo, {"calc.py": FIXED, "tests/calc.test.ts": "// t\n"}, trailer)
    code, out = run(repo, base, capsys)
    assert code == 2
    assert "UNREPLAYED" in out


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
