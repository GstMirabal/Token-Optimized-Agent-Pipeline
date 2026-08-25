"""Tests for scripts/check_readme_counts.py (Sprint 029 T1.0)."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"


@pytest.fixture()
def check_mod(monkeypatch: pytest.MonkeyPatch) -> object:
    monkeypatch.syspath_prepend(str(SCRIPTS))
    sys.modules.pop("check_readme_counts", None)
    return importlib.import_module("check_readme_counts")


def test_checks_include_scripts_and_config(check_mod) -> None:
    """Sprint 029 T1: At a Glance must verify scripts/ and config/ counts."""
    assert "scripts" in check_mod.CHECKS
    assert "config" in check_mod.CHECKS


def test_scripts_counter_counts_py_files_only(check_mod, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(REPO)
    _, counter = check_mod.CHECKS["scripts"]
    actual = counter()
    expected = len(list(Path("scripts").glob("*.py")))
    assert actual == expected
    assert actual >= 1


def test_config_counter_counts_json_files(check_mod, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(REPO)
    _, counter = check_mod.CHECKS["config"]
    actual = counter()
    expected = len(list(Path("config").glob("*.json")))
    assert actual == expected
    assert actual >= 1


def test_main_ignores_pytest_argv(check_mod, monkeypatch: pytest.MonkeyPatch) -> None:
    """T1.1 argparse must not treat pytest's sys.argv as script flags."""
    monkeypatch.chdir(REPO)
    monkeypatch.setattr(
        sys, "argv", ["pytest", "tests/test_check_readme_counts.py", "-q"]
    )
    assert check_mod.main() == 0
