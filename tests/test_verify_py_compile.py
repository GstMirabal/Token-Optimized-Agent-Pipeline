"""Tests that verify py_compile does not use xargs / SC_ARG_MAX (Sprint 037 S2)."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from types import ModuleType

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"
MAKEFILE = REPO / "Makefile"


def test_verify_py_compile_recipe_avoids_xargs_and_find_exec() -> None:
    text = MAKEFILE.read_text(encoding="utf-8")
    verify_block = text.split("verify:", 1)[1].split("\n# ", 1)[0]
    assert "xargs" not in verify_block
    assert "-exec" not in verify_block
    assert "scripts/py_compile_tree.py" in verify_block


def test_py_compile_tree_compiles_without_sysconf(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.syspath_prepend(str(SCRIPTS))
    sys.modules.pop("py_compile_tree", None)
    mod = importlib.import_module("py_compile_tree")
    root = tmp_path / "repo"
    (root / "pkg").mkdir(parents=True)
    (root / "pkg" / "ok.py").write_text("x = 1\n", encoding="utf-8")
    monkeypatch.setattr(mod, "agents_root", lambda: root)

    def boom(_name: str) -> int:
        raise OSError("sysconf denied")

    monkeypatch.setattr("os.sysconf", boom)
    assert mod.main() == 0


def _load_module(monkeypatch: pytest.MonkeyPatch, root: Path) -> ModuleType:
    monkeypatch.syspath_prepend(str(SCRIPTS))
    sys.modules.pop("py_compile_tree", None)
    mod = importlib.import_module("py_compile_tree")
    monkeypatch.setattr(mod, "agents_root", lambda: root)
    return mod


def test_py_compile_tree_writes_no_pycache_into_scanned_tree(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    root = tmp_path / "repo"
    (root / "pkg").mkdir(parents=True)
    (root / "pkg" / "ok.py").write_text("x = 1\n", encoding="utf-8")
    mod = _load_module(monkeypatch, root)
    assert mod.main() == 0
    assert list(root.rglob("__pycache__")) == []


def test_py_compile_tree_reports_syntax_error_with_exit_1(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    (root / "bad.py").write_text("def (:\n", encoding="utf-8")
    mod = _load_module(monkeypatch, root)
    assert mod.main() == 1
    err = capsys.readouterr().err
    assert "bad.py" in err
    assert "1 failure(s)" in err
    assert list(root.rglob("__pycache__")) == []


def test_py_compile_tree_compiles_in_memory_without_tempfile(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    root = tmp_path / "repo"
    (root / "pkg").mkdir(parents=True)
    (root / "pkg" / "ok.py").write_text("x = 1\n", encoding="utf-8")
    mod = _load_module(monkeypatch, root)
    before = sorted(p for p in root.rglob("*"))

    def boom(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("tempfile.TemporaryDirectory must not be used")

    monkeypatch.setattr("tempfile.TemporaryDirectory", boom)
    assert mod.main() == 0
    assert sorted(p for p in root.rglob("*")) == before


def test_py_compile_tree_null_byte_source_fails_and_names_file(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    (root / "nul.py").write_bytes(b"x = 1\x00\n")
    mod = _load_module(monkeypatch, root)
    assert mod.main() == 1
    err = capsys.readouterr().err
    assert "nul.py" in err
    assert "1 failure(s)" in err


def test_py_compile_tree_non_utf8_source_without_cookie_fails_and_names_file(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    (root / "latin.py").write_bytes(b"x = '\xe9'\n")
    mod = _load_module(monkeypatch, root)
    assert mod.main() == 1
    err = capsys.readouterr().err
    assert "latin.py" in err
    assert "1 failure(s)" in err


def test_py_compile_tree_accepts_latin1_source_with_coding_cookie(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    (root / "cookie.py").write_bytes(b"# -*- coding: latin-1 -*-\nx = '\xe9'\n")
    mod = _load_module(monkeypatch, root)
    assert mod.main() == 0
