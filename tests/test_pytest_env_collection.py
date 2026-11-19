"""Collection must survive an unreadable root ``.env`` (plan D75, R29-1).

The nucleus ``pytest.ini`` carries ``--ignore-glob=.env*`` so that collection
does not stat a root ``.env`` the sandbox ``denyRead`` list refuses. This test
builds a minimal repository in a temporary directory, with a ``chmod 000``
``.env`` and the real ``pytest.ini``, and runs collection in a subprocess.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from collections.abc import Iterator
from pathlib import Path

import pytest

NUCLEUS_INI = Path(__file__).resolve().parent.parent / "pytest.ini"


@pytest.fixture
def mini_repo(tmp_path: Path) -> Iterator[Path]:
    """Build a temporary repository with a trivial test and a ``chmod 000`` ``.env``.

    Args:
        tmp_path: pytest temporary directory.

    Yields:
        The repository root. Permissions on ``.env`` are restored on teardown
        so the temporary directory can be removed.
    """
    shutil.copy(NUCLEUS_INI, tmp_path / "pytest.ini")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_trivial.py").write_text("def test_trivial() -> None:\n    pass\n")
    env_file = tmp_path / ".env"
    env_file.write_text("DUMMY=value\n")
    env_file.chmod(0o000)
    try:
        yield tmp_path
    finally:
        env_file.chmod(0o600)


def _collect(root: Path) -> subprocess.CompletedProcess[str]:
    """Run ``pytest --collect-only`` with ``root`` as the working directory.

    Args:
        root: Directory holding the ``pytest.ini`` under test.

    Returns:
        The completed process with captured text output.
    """
    return subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )


def test_collection_succeeds_with_unreadable_env(mini_repo: Path) -> None:
    """The nucleus ``pytest.ini`` collects the trivial test and exits 0."""
    result = _collect(mini_repo)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "test_trivial" in result.stdout


def test_nucleus_ini_ignores_env_files() -> None:
    """The nucleus ``pytest.ini`` keeps the ``--ignore-glob=.env*`` option."""
    assert "--ignore-glob=.env*" in NUCLEUS_INI.read_text()


def test_collection_without_option_fails(mini_repo: Path) -> None:
    """Control: without the option, collection fails on an unstattable ``.env``.

    Outside the sandbox no portable way reproduces the failure (measured on
    darwin: ``chmod 000`` and a self-referencing symlink both still collect
    with exit 0, because ``testpaths`` never walks the root and the owner can
    stat the file). The refusal exists only under the sandbox ``denyRead``
    list, so the control is skipped rather than faked.
    """
    (mini_repo / "pytest.ini").write_text("[pytest]\ntestpaths = tests\n")
    result = _collect(mini_repo)
    if result.returncode == 0:
        pytest.skip(
            "failure without --ignore-glob=.env* reproduces only under the sandbox "
            "denyRead list; chmod 000 does not stop stat() for the owner"
        )
    assert result.returncode != 0
