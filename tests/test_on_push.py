"""Tests for hooks/on_push.py — force-push and history-rewrite rejection.

Four named tests (P9.2), symmetric with P8.1. Each drives ``on_push.py`` through
a real ``pre-push`` hook against a bare remote under ``/private/tmp``.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

HOOKS_ROOT = Path(__file__).resolve().parent.parent
ON_PUSH = HOOKS_ROOT / "hooks" / "on_push.py"


def _run(cwd: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    """Run a git/command in ``cwd`` with captured output."""
    return subprocess.run(
        list(args),
        cwd=cwd,
        check=check,
        capture_output=True,
        text=True,
    )


def _sandbox_pair(tmp_path: Path) -> tuple[Path, Path]:
    """Create a bare remote and a clone under ``/private/tmp`` when possible."""
    base = Path("/private/tmp")
    if not base.is_dir():
        base = tmp_path
    work = Path(tempfile.mkdtemp(prefix="p92-on-push-", dir=str(base)))
    bare = work / "remote.git"
    clone = work / "clone"
    _run(work, "git", "init", "--bare", str(bare))
    _run(work, "git", "clone", str(bare), str(clone))
    _run(clone, "git", "config", "user.email", "p92@test.local")
    _run(clone, "git", "config", "user.name", "p92")
    # First commit so the remote tip exists for force/rewrite cases.
    (clone / "README").write_text("seed\n", encoding="utf-8")
    _run(clone, "git", "add", "README")
    _run(clone, "git", "commit", "-m", "chore: seed #026")
    _run(clone, "git", "push", "-u", "origin", "HEAD")
    # Install pre-push that execs the framework hook.
    hooks = clone / ".git" / "hooks"
    hooks.mkdir(exist_ok=True)
    pre_push = hooks / "pre-push"
    pre_push.write_text(
        "#!/usr/bin/env bash\n"
        "set -euo pipefail\n"
        f'exec "{sys.executable}" "{ON_PUSH}" "$@"\n',
        encoding="utf-8",
    )
    pre_push.chmod(0o755)
    return bare, clone


def _advance_and_rewrite(clone: Path) -> None:
    """Leave remote at tip T and local tip at an ancestor of T (non-FF)."""
    (clone / "README").write_text("second\n", encoding="utf-8")
    _run(clone, "git", "add", "README")
    _run(clone, "git", "commit", "-m", "chore: second #026")
    _run(clone, "git", "push", "origin", "HEAD")
    # Move local tip back one commit without changing remote.
    _run(clone, "git", "reset", "--hard", "HEAD~1")


def test_force_push_long_flag_rejected(tmp_path: Path) -> None:
    """``git push --force`` that rewrites history must exit non-zero."""
    _bare, clone = _sandbox_pair(tmp_path)
    _advance_and_rewrite(clone)
    result = _run(
        clone,
        "git",
        "push",
        "--force",
        "origin",
        "HEAD",
        check=False,
    )
    assert result.returncode != 0
    assert "ON_PUSH" in (result.stderr + result.stdout)


def test_force_push_short_flag_rejected(tmp_path: Path) -> None:
    """``git push -f`` that rewrites history must exit non-zero."""
    _bare, clone = _sandbox_pair(tmp_path)
    _advance_and_rewrite(clone)
    result = _run(
        clone,
        "git",
        "push",
        "-f",
        "origin",
        "HEAD",
        check=False,
    )
    assert result.returncode != 0
    assert "ON_PUSH" in (result.stderr + result.stdout)


def test_history_rewrite_push_rejected(tmp_path: Path) -> None:
    """A non-fast-forward push over an existing ref must exit non-zero."""
    _bare, clone = _sandbox_pair(tmp_path)
    _advance_and_rewrite(clone)
    # No --force: git itself may also refuse; either way $? != 0. Prefer the
    # hook path by forcing through after confirming non-FF setup, still using
    # a rewrite (same tip ancestry as the force cases).
    result = _run(
        clone,
        "git",
        "push",
        "--force-with-lease",
        "origin",
        "HEAD",
        check=False,
    )
    assert result.returncode != 0


def test_normal_push_allowed(tmp_path: Path) -> None:
    """A fast-forward push must still exit 0 with the hook installed."""
    _bare, clone = _sandbox_pair(tmp_path)
    (clone / "README").write_text("ff\n", encoding="utf-8")
    _run(clone, "git", "add", "README")
    _run(clone, "git", "commit", "-m", "chore: fast-forward #026")
    result = _run(clone, "git", "push", "origin", "HEAD", check=False)
    assert result.returncode == 0
