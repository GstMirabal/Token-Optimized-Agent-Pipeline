"""Tests for scripts/install_lock.py (Sprint 054, B04, D12 / KI-053-1)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "install_lock.py"


def _run(command: str, root: Path) -> int:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), command, "--root", str(root)],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    return proc.returncode


def _tree(root: Path, files: dict[str, str]) -> None:
    for name, text in files.items():
        (root / name).write_text(text, encoding="utf-8")


def test_absent_lock_exits_2(tmp_path: Path) -> None:
    _tree(tmp_path, {"requirements-core.txt": "pkg==1\n"})
    assert _run("check", tmp_path) == 2


def test_write_then_check_exits_0(tmp_path: Path) -> None:
    _tree(tmp_path, {"requirements-core.txt": "pkg==1\n-r q.txt\n", "q.txt": "x==2\n"})
    assert _run("write", tmp_path) == 0
    assert _run("check", tmp_path) == 0


def test_edited_include_exits_2(tmp_path: Path) -> None:
    _tree(tmp_path, {"requirements-core.txt": "-r q.txt\n", "q.txt": "x==2\n"})
    _run("write", tmp_path)
    (tmp_path / "q.txt").write_text("x==3\n", encoding="utf-8")
    assert _run("check", tmp_path) == 2


def test_recursive_include_followed(tmp_path: Path) -> None:
    _tree(
        tmp_path,
        {
            "requirements-core.txt": "-r b.txt\n",
            "b.txt": "--requirement c.txt\n",
            "c.txt": "x==1\n",
        },
    )
    _run("write", tmp_path)
    (tmp_path / "c.txt").write_text("x==2\n", encoding="utf-8")
    assert _run("check", tmp_path) == 2


def test_include_cycle_terminates(tmp_path: Path) -> None:
    _tree(
        tmp_path,
        {
            "requirements-core.txt": "-r b.txt\n",
            "b.txt": "-r requirements-core.txt\n",
        },
    )
    assert _run("write", tmp_path) == 0
    assert _run("check", tmp_path) == 0


def test_legacy_free_text_lock_exits_2(tmp_path: Path) -> None:
    _tree(
        tmp_path,
        {
            "requirements-core.txt": "pkg==1\n",
            "installed.lock": "2026-01-01T00:00:00Z requirements-core.txt\n",
        },
    )
    assert _run("check", tmp_path) == 2


def test_missing_included_file_exits_2(tmp_path: Path) -> None:
    _tree(tmp_path, {"requirements-core.txt": "-r gone.txt\n"})
    assert _run("check", tmp_path) == 2
    assert _run("write", tmp_path) == 2


def test_missing_core_file_exits_2(tmp_path: Path) -> None:
    assert _run("check", tmp_path) == 2
