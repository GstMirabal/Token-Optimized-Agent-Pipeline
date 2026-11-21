"""Collection must survive a root ``.env`` that ``stat()`` refuses (plan D75, D76).

The nucleus ``pytest.ini`` carries ``--ignore-glob=.env*`` so that collection
does not stat a root ``.env`` that the sandbox ``denyRead`` list refuses. Outside
the sandbox ``chmod 000`` does not stop ``stat()`` for the owner, so these cases
inject a plugin into the pytest subprocess: it wraps ``os.stat`` and
``os.lstat`` so that any path whose basename starts with ``.env`` raises
``PermissionError``, the same errno the sandbox returns. Collection starts from
the repository root with ``.`` as the path argument, the invocation shape that
makes pytest visit the root ``.env`` (``pytest_ignore_collect`` calls
``Path.is_dir()`` on it).
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

NUCLEUS_INI = Path(__file__).resolve().parent.parent / "pytest.ini"

DENY_PLUGIN = '''\
"""Model the sandbox denyRead list: stat() of a ``.env*`` path is refused."""

import os

_real_stat = os.stat
_real_lstat = os.lstat


def _check(path: object) -> None:
    """Raise PermissionError when the basename of ``path`` starts with ``.env``."""
    try:
        name = os.path.basename(os.fspath(path))
    except TypeError:
        return
    if isinstance(name, bytes):
        name = name.decode(errors="ignore")
    if name.startswith(".env"):
        raise PermissionError(13, "Operation not permitted", str(path))


def _stat(path, *args, **kwargs):
    _check(path)
    return _real_stat(path, *args, **kwargs)


def _lstat(path, *args, **kwargs):
    _check(path)
    return _real_lstat(path, *args, **kwargs)


os.stat = _stat
os.lstat = _lstat
'''


@pytest.fixture
def mini_repo(tmp_path: Path) -> Path:
    """Build a temporary repository with a trivial test, a root ``.env`` and the plugin.

    Args:
        tmp_path: pytest temporary directory.

    Returns:
        The repository root, holding the nucleus ``pytest.ini``.
    """
    shutil.copy(NUCLEUS_INI, tmp_path / "pytest.ini")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_trivial.py").write_text("def test_trivial() -> None:\n    pass\n")
    (tmp_path / ".env").write_text("DUMMY=value\n")
    (tmp_path / "deny_env_stat.py").write_text(DENY_PLUGIN)
    return tmp_path


def _collect(root: Path, extra: tuple[str, ...] = ()) -> subprocess.CompletedProcess[str]:
    """Run ``pytest --collect-only`` on ``.`` from ``root`` with ``.env*`` stat refused.

    Args:
        root: Directory holding the ``pytest.ini`` and the plugin under test.
        extra: Additional pytest arguments, placed before the path argument.

    Returns:
        The completed process with captured text output.
    """
    env = {**os.environ, "PYTHONPATH": str(root)}
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-p",
            "deny_env_stat",
            "-p",
            "no:cacheprovider",
            "--collect-only",
            "-q",
            *extra,
            ".",
        ],
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def test_collection_succeeds_with_refused_env(mini_repo: Path) -> None:
    """The nucleus ``pytest.ini`` collects the trivial test and exits 0."""
    result = _collect(mini_repo)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "test_trivial" in result.stdout


def test_nucleus_ini_ignores_env_files() -> None:
    """The nucleus ``pytest.ini`` keeps the ``--ignore-glob=.env*`` option."""
    assert "--ignore-glob=.env*" in NUCLEUS_INI.read_text()


def test_collection_without_option_fails(mini_repo: Path) -> None:
    """Control: without the option, collection fails with ``PermissionError``."""
    result = _collect(mini_repo, ("-o", "addopts="))
    output = result.stdout + result.stderr
    assert result.returncode != 0, output
    assert "PermissionError" in output, output
