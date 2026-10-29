"""Tests for scripts/detect_new_models.py catalogue parsing (`KI-057-3`)."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def _module():
    sys.path.insert(0, str(REPO / "scripts"))
    try:
        sys.modules.pop("detect_new_models", None)
        return importlib.import_module("detect_new_models")
    finally:
        sys.path.remove(str(REPO / "scripts"))


def test_plain_row_is_parsed(tmp_path: Path) -> None:
    path = tmp_path / "models.md"
    path.write_text(
        "| Name | Alias | Status |\n"
        "| Foo | `claude-foo-1` | Legacy, retires 2027-01-31 |\n",
        encoding="utf-8",
    )
    assert _module().parse_catalogue(path) == {
        "claude-foo-1": {"status": "Legacy", "retires": "2027-01-31"}
    }


def test_escaped_pipe_in_a_cell_does_not_shift_the_alias_column(tmp_path: Path) -> None:
    """An escaped pipe in the first cell keeps the alias in the second cell."""
    path = tmp_path / "models.md"
    path.write_text(
        "| Name | Alias | Status |\n"
        "| Foo \\| Bar | `claude-foo-1` | Active |\n",
        encoding="utf-8",
    )
    assert _module().parse_catalogue(path) == {
        "claude-foo-1": {"status": "Active", "retires": None}
    }
