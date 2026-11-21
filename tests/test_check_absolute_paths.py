"""Pin `scripts/check_absolute_paths.py` against index and untracked content (KI-058-1).

The check once ran `git grep` over tracked files only, so a home path in a new
file passed `make verify` before `git add` and failed after it. Each test runs
the script in a throwaway git repository built under `tmp_path`.

Stated subset (`fail_closed_claims`): the scan covers tracked files, the
staged content of the index, and untracked files that are not ignored.
`.gitignore`d files are out of scope and one test pins that boundary.

invoked_by: pytest tests/.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_absolute_paths.py"
# Concatenated so this file does not itself match the home-path pattern.
FORBIDDEN = "/" + "Users/" + "realperson/project"
ALLOWED = "/" + "Users/" + "developer/project"


def _git(repo: Path, *args: str) -> None:
    """Run a git command in `repo`, failing the test on a non-zero exit."""
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


def _run(repo: Path) -> subprocess.CompletedProcess[str]:
    """Run the check inside `repo` and return the finished process."""
    return subprocess.run(
        [sys.executable, str(SCRIPT)], cwd=repo, capture_output=True, text=True, check=False
    )


@pytest.fixture()
def repo(tmp_path: Path) -> Path:
    """A git repository holding one clean committed file."""
    root = tmp_path / "repo"
    root.mkdir()
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "t@example.com")
    _git(root, "config", "user.name", "t")
    (root / "clean.txt").write_text("nothing here\n", encoding="utf-8")
    _git(root, "add", "clean.txt")
    _git(root, "commit", "-q", "-m", "init")
    return root


def test_clean_repo_passes(repo: Path) -> None:
    """A repository with no home path exits 0."""
    assert _run(repo).returncode == 0


def test_allow_listed_user_passes_when_untracked(repo: Path) -> None:
    """The allow-list still applies to untracked files."""
    (repo / "new.txt").write_text(ALLOWED + "\n", encoding="utf-8")
    assert _run(repo).returncode == 0


def test_untracked_file_with_forbidden_path_fails(repo: Path) -> None:
    """An untracked file holding a forbidden path exits non-zero and is named."""
    (repo / "new_test.py").write_text(f'P = "{FORBIDDEN}"\n', encoding="utf-8")
    result = _run(repo)
    assert result.returncode != 0
    assert "new_test.py" in result.stdout


def test_staged_content_with_forbidden_path_fails(repo: Path) -> None:
    """A path present only in the index (worktree copy cleaned) exits non-zero."""
    target = repo / "staged.txt"
    target.write_text(FORBIDDEN + "\n", encoding="utf-8")
    _git(repo, "add", "staged.txt")
    target.write_text("cleaned after staging\n", encoding="utf-8")
    result = _run(repo)
    assert result.returncode != 0
    assert "staged.txt" in result.stdout


def test_ignored_file_is_out_of_scope(repo: Path) -> None:
    """A `.gitignore`d file with a forbidden path is not scanned (stated subset)."""
    (repo / ".gitignore").write_text("secret.txt\n", encoding="utf-8")
    (repo / "secret.txt").write_text(FORBIDDEN + "\n", encoding="utf-8")
    assert _run(repo).returncode == 0
