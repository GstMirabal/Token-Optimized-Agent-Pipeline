"""Tests that verify py_compile does not use xargs / SC_ARG_MAX (Sprint 037 S2)."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

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
