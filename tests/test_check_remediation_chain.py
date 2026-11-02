"""Tests for scripts/check_remediation_chain.py (A-1) on throwaway git repos."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

CHECK = Path(__file__).resolve().parent.parent / "scripts" / "check_remediation_chain.py"


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@example.com",
         "-c", "commit.gpgsign=false", *args],
        cwd=repo, capture_output=True, text=True, check=True,
    ).stdout.strip()


def _commit(repo: Path, name: str, text: str, subject: str) -> str:
    (repo / name).write_text(text)
    _git(repo, "add", name)
    _git(repo, "commit", "-q", "-m", subject)
    return _git(repo, "rev-parse", "HEAD")


def _run(repo: Path, rng: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECK), "--range", rng],
        cwd=repo, capture_output=True, text=True, check=False,
    )


@pytest.fixture()
def repo(tmp_path: Path) -> Path:
    _git(tmp_path, "init", "-q")
    _commit(tmp_path, "base.txt", "x\n", "chore: base")
    return tmp_path


def test_no_fix_commits_exit_0(repo: Path) -> None:
    base = _git(repo, "rev-parse", "HEAD")
    _commit(repo, "a.txt", "1\n", "feat(a): add")
    r = _run(repo, f"{base}..HEAD")
    assert r.returncode == 0
    assert "chains: 0" in r.stdout


def test_one_chain_printed_exit_0(repo: Path) -> None:
    base = _git(repo, "rev-parse", "HEAD")
    a = _commit(repo, "a.txt", "1\n2\n", "fix(a): first")
    b = _commit(repo, "a.txt", "1\n2b\n", "fix(a): second")
    r = _run(repo, f"{base}..HEAD")
    assert r.returncode == 0
    assert "chains: 1" in r.stdout
    assert a[:7] in r.stdout and b[:7] in r.stdout


def test_three_link_chain_is_one_chain(repo: Path) -> None:
    base = _git(repo, "rev-parse", "HEAD")
    _commit(repo, "a.txt", "1\n", "fix: one")
    _commit(repo, "a.txt", "2\n", "fix: two")
    _commit(repo, "a.txt", "3\n", "fix: three")
    r = _run(repo, f"{base}..HEAD")
    assert r.returncode == 0
    assert "chains: 1" in r.stdout


def test_breaking_fix_subject_is_a_link(repo: Path) -> None:
    subject = "fix!: breaking"
    base = _git(repo, "rev-parse", "HEAD")
    a = _commit(repo, "a.txt", "1\n2\n", "fix(a): first")
    b = _commit(repo, "a.txt", "1\n2b\n", subject)
    r = _run(repo, f"{base}..HEAD")
    assert r.returncode == 0
    assert "chains: 1" in r.stdout
    assert a[:7] in r.stdout and b[:7] in r.stdout


def test_two_independent_chains_exit_2(repo: Path) -> None:
    base = _git(repo, "rev-parse", "HEAD")
    for name in ("a.txt", "b.txt"):
        _commit(repo, name, "1\n", f"fix({name[0]}): first")
        _commit(repo, name, "2\n", f"fix({name[0]}): second")
    r = _run(repo, f"{base}..HEAD")
    assert r.returncode == 2
    assert "chains: 2" in r.stdout


def test_fix_outside_range_is_not_a_link(repo: Path) -> None:
    _commit(repo, "a.txt", "1\n", "fix(a): earlier sprint")
    base = _git(repo, "rev-parse", "HEAD")
    _commit(repo, "a.txt", "2\n", "fix(a): in range")
    r = _run(repo, f"{base}..HEAD")
    assert r.returncode == 0
    assert "chains: 0" in r.stdout


def test_feat_touching_fix_line_is_not_a_link(repo: Path) -> None:
    base = _git(repo, "rev-parse", "HEAD")
    _commit(repo, "a.txt", "1\n", "fix(a): first")
    _commit(repo, "a.txt", "2\n", "feat(a): rewrite")
    r = _run(repo, f"{base}..HEAD")
    assert r.returncode == 0
    assert "chains: 0" in r.stdout


def test_added_only_hunk_and_deleted_file_do_not_crash(repo: Path) -> None:
    base = _git(repo, "rev-parse", "HEAD")
    _commit(repo, "a.txt", "1\n", "fix(a): first")
    _commit(repo, "a.txt", "1\n2\n", "fix(a): append only")
    (repo / "a.txt").unlink()
    _git(repo, "commit", "-q", "-am", "fix(a): delete")
    r = _run(repo, f"{base}..HEAD")
    assert r.returncode == 0
    assert "chains: 1" in r.stdout


def test_invalid_range_exit_2(repo: Path) -> None:
    r = _run(repo, "nope..HEAD")
    assert r.returncode == 2
    assert "error" in r.stderr
