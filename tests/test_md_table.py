"""Tests for scripts/_md_table.py (`KI-057-3`)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from _md_table import split_cells


def test_plain_row_splits_on_every_pipe() -> None:
    assert split_cells("| a | b | c |") == ["a", "b", "c"]


def test_escaped_pipe_stays_inside_its_cell() -> None:
    assert split_cells(r"| a | x \| y | c |") == ["a", "x | y", "c"]


def test_row_without_outer_pipes_and_surrounding_space() -> None:
    assert split_cells("  a | b  ") == ["a", "b"]


def test_backticks_are_left_to_the_caller() -> None:
    assert split_cells("| `a` | b |") == ["`a`", "b"]


def test_empty_cells_are_kept() -> None:
    assert split_cells("| a |  | c |") == ["a", "", "c"]
