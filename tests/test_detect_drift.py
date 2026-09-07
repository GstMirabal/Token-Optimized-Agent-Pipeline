"""Tests for scripts/detect_drift.py — the routine `docs(state)` exclusion.

`F-BOOT-4`: every close and deployment appends a commit touching only
`docs/active_state.json` after `last_close_commit`. With `[Unreleased]` empty
those read as drift (verdict `U`/`A`) and force a no-op `/agents:reconcile` on
every session in between. They are outside the drift range by construction; a
commit that also touches another file, or one without the `docs(state)`
subject, is still counted.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import detect_drift as dd


@pytest.fixture
def repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A real repository — these checks are about git semantics."""
    monkeypatch.chdir(tmp_path)

    def run(*args: str) -> None:
        subprocess.run(
            ["git", *args], cwd=tmp_path, check=True, capture_output=True, text=True
        )

    run("init", "-q", "-b", "main")
    run("config", "user.email", "t@example.com")
    run("config", "user.name", "T")
    (tmp_path / "f.txt").write_text("base\n")
    run("add", "-A")
    run("commit", "-qm", "base")
    (tmp_path / "docs").mkdir()
    return tmp_path


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=repo, check=True, capture_output=True, text=True
    ).stdout.strip()


def _head(repo: Path) -> str:
    return _git(repo, "rev-parse", "HEAD")


def _commit_all(repo: Path, message: str) -> None:
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", message)


def _commit_state_only(repo: Path, message: str) -> None:
    """Commit only docs/active_state.json (staging that path alone)."""
    _git(repo, "add", "docs/active_state.json")
    _git(repo, "commit", "-qm", message)


def _write_anchor(repo: Path, **fields: object) -> None:
    (repo / "docs" / "active_state.json").write_text(json.dumps(fields))


def test_single_routine_state_commit_reads_clean(repo: Path) -> None:
    """The F-BOOT-4 case: the only commit past the baseline is a docs(state) write.

    Against the pre-Sprint-044 tree this is verdict `R` and exits 2.
    """
    baseline = _head(repo)
    _write_anchor(repo, status="X", last_close_commit=baseline)
    _commit_state_only(repo, "docs(state): open Sprint 099")
    assert dd.main() == 0


def test_a_docs_state_commit_that_also_touches_code_is_still_drift(repo: Path) -> None:
    """Both conditions are required — a smuggled file change is still counted."""
    baseline = _head(repo)
    _write_anchor(repo, status="X", last_close_commit=baseline)
    (repo / "f.txt").write_text("smuggled change\n")
    _commit_all(repo, "docs(state): open Sprint 099")
    assert dd.main() == 2


def test_a_state_only_commit_without_the_docs_state_subject_is_still_drift(
    repo: Path,
) -> None:
    """Subject must match `^docs\\(state\\)` — a state-only chore is still counted."""
    baseline = _head(repo)
    _write_anchor(repo, status="X", last_close_commit=baseline)
    _commit_state_only(repo, "chore: fiddle with the anchor")
    assert dd.main() == 2


def test_a_routine_commit_does_not_hide_a_real_one(repo: Path) -> None:
    """A routine state commit is dropped; a real out-of-protocol commit is not."""
    baseline = _head(repo)
    _write_anchor(repo, status="X", last_close_commit=baseline)
    _commit_state_only(repo, "docs(state): open Sprint 099")
    (repo / "g.txt").write_text("out of protocol\n")
    _commit_all(repo, "add g outside the protocol")
    assert dd.main() == 2


def test_routine_shas_helper_identifies_only_the_state_only_docs_commit(
    repo: Path,
) -> None:
    """Unit-level: `_routine_state_shas` picks the one qualifying commit."""
    _write_anchor(repo, status="X")
    _commit_state_only(repo, "docs(state): first")
    sha_routine = _head(repo)[:9]
    (repo / "f.txt").write_text("real\n")
    _commit_all(repo, "docs(state): but also code")
    lines = subprocess.run(
        ["git", "log", "--oneline", "-2"],
        cwd=repo, capture_output=True, text=True, check=True,
    ).stdout.splitlines()
    routine = dd._routine_state_shas(lines)
    assert len(routine) == 1
    assert next(iter(routine)).startswith(sha_routine[:7])
