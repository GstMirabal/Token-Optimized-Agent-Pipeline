"""Tests for scripts/session_cost.py.

Pairs the `F-116-N1` fix (Sprint 059 unit A-01): the cycle baseline is the
first turn's context size (`cache_read + cache_creation + input`), so a
cold-cache first turn no longer yields `first_turn` 0 and `ratio` None.
"""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import session_cost as sc


def make_turn(read: int = 0, creation: int = 0, new_input: int = 0) -> dict:
    """A usage-bearing turn as `read_turns` returns it.

    Args:
        read: `cache_read_input_tokens`.
        creation: `cache_creation_input_tokens`.
        new_input: `input_tokens`.

    Returns:
        dict: the turn with the four token fields and a model name.
    """
    return {"model": "m", "input_tokens": new_input, "output_tokens": 0,
            "cache_read_input_tokens": read,
            "cache_creation_input_tokens": creation}


def test_cold_cache_first_turn_has_a_baseline_and_a_ratio() -> None:
    cycle = [make_turn(read=0, creation=44_000, new_input=4),
             make_turn(read=44_004, creation=1_000),
             make_turn(read=88_000, creation=2_000)]
    summary = sc.cycle_summary(cycle)
    assert summary["first_turn"] == 44_004
    assert summary["peak"] == 90_000
    assert summary["ratio"] == 2.0


def test_warm_cycle_ratio_is_peak_over_first_context() -> None:
    cycle = [make_turn(read=20_000, creation=1_000, new_input=0),
             make_turn(read=40_000, creation=500),
             make_turn(read=100_000, creation=500, new_input=0)]
    summary = sc.cycle_summary(cycle)
    assert summary["first_turn"] == 21_000
    assert summary["peak"] == 100_500
    assert summary["ratio"] == 4.8
    assert summary["messages"] == 3


def test_all_zero_first_turn_keeps_ratio_none() -> None:
    summary = sc.cycle_summary([make_turn(), make_turn(read=5_000)])
    assert summary["first_turn"] == 0
    assert summary["ratio"] is None


def test_compaction_collapse_still_opens_a_cycle() -> None:
    turns = [make_turn(read=300_000, creation=1_000),
             make_turn(read=0, creation=22_000)]
    assert len(sc.segment_cycles(turns)) == 2
