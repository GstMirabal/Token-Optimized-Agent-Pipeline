"""Tests for scripts/session_cost.py.

Pairs the `F-116-N1` fix (Sprint 059 unit A-01): the cycle baseline is the
first turn's context size (`cache_read + cache_creation + input`), so a
cold-cache first turn no longer yields `first_turn` 0 and `ratio` None.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from types import ModuleType

import pytest

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


def test_cold_turn_with_an_unchanged_window_does_not_open_a_cycle() -> None:
    turns = [make_turn(read=200_000, creation=1_000),
             make_turn(read=0, creation=201_000),
             make_turn(read=201_000, creation=500)]
    assert len(sc.segment_cycles(turns)) == 1


def test_growth_with_one_cache_expiry_keeps_one_cycle_above_hard_ratio(
        tmp_path: Path) -> None:
    import session_probe as spr
    turns = [make_turn(read=20_000, creation=1_000),
             make_turn(read=150_000, creation=5_000),
             make_turn(read=0, creation=160_000),
             make_turn(read=165_000, creation=5_000),
             make_turn(read=420_000)]
    transcript = tmp_path / "x.jsonl"
    transcript.write_text("\n".join(json.dumps({"message": {"model": "m", "usage": {
        "input_tokens": t["input_tokens"], "output_tokens": 1,
        "cache_read_input_tokens": t["cache_read_input_tokens"],
        "cache_creation_input_tokens": t["cache_creation_input_tokens"]}}})
        for t in turns))
    result = sc.measure(transcript)
    assert len(result["cycles"]) == 1
    assert result["cycles"][0]["ratio"] > spr.HARD_RATIO


def _probe_with(monkeypatch: pytest.MonkeyPatch, ratio: float | None) -> tuple[ModuleType, str | None]:
    import session_probe as spr
    cycle = {"messages": 3, "first_turn": 10_000, "peak": 10_000,
             "ratio": ratio}
    monkeypatch.setattr(spr.session_cost, "measure_previous", lambda *a, **k: {
        "measurable": True, "session": "abcdef123456", "cycles": [cycle]})
    return spr, spr.probe_cost({})


def test_probe_cost_names_a_cycle_above_the_hard_ratio(
        monkeypatch: pytest.MonkeyPatch) -> None:
    import session_probe as spr
    message = _probe_with(monkeypatch, spr.HARD_RATIO + 0.1)[1]
    assert message is not None
    assert "cycle 1" in message
    assert "abcdef12" in message


def test_probe_cost_is_silent_at_or_below_the_hard_ratio(
        monkeypatch: pytest.MonkeyPatch) -> None:
    import session_probe as spr
    assert _probe_with(monkeypatch, float(spr.HARD_RATIO))[1] is None
    assert _probe_with(monkeypatch, 1.0)[1] is None


def _write_records(path: Path, records: list[tuple[str | None, int, int]]) -> Path:
    """Write a transcript of `(message id, output, cache_read)` records.

    Args:
        path: file to write.
        records: one tuple per record; an id of None omits `message.id`.

    Returns:
        Path: the transcript written.
    """
    lines = []
    for message_id, output, read in records:
        message: dict = {"model": "m", "usage": {
            "input_tokens": 1, "output_tokens": output,
            "cache_read_input_tokens": read, "cache_creation_input_tokens": 0}}
        if message_id is not None:
            message["id"] = message_id
        lines.append(json.dumps({"message": message}))
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def test_records_sharing_a_message_id_yield_one_turn_per_id(tmp_path: Path) -> None:
    transcript = _write_records(tmp_path / "x.jsonl", [
        ("a", 5, 10), ("a", 5, 10), ("a", 5, 10), ("b", 7, 20), ("b", 7, 20)])
    turns, skipped = sc.read_turns(transcript)
    assert [t["cache_read_input_tokens"] for t in turns] == [10, 20]
    assert skipped == 0
    result = sc.measure(transcript)
    assert result["messages"] == 2
    assert result["totals"]["output_tokens"] == 12
    assert result["cycles"][0]["messages"] == 2


def test_turns_keep_the_order_of_first_appearance(tmp_path: Path) -> None:
    transcript = _write_records(tmp_path / "x.jsonl", [
        ("a", 1, 10), ("b", 1, 20), ("a", 1, 10)])
    turns, _ = sc.read_turns(transcript)
    assert [t["cache_read_input_tokens"] for t in turns] == [10, 20]


def test_records_with_no_message_id_are_each_counted(tmp_path: Path) -> None:
    transcript = _write_records(tmp_path / "x.jsonl", [
        (None, 1, 10), (None, 1, 10), ("a", 1, 10), ("a", 1, 10)])
    turns, _ = sc.read_turns(transcript)
    assert len(turns) == 3


def test_records_of_one_id_with_differing_usage_keep_the_first(
        tmp_path: Path) -> None:
    transcript = _write_records(tmp_path / "x.jsonl", [
        ("a", 3, 10), ("a", 9, 10)])
    turns, _ = sc.read_turns(transcript)
    assert len(turns) == 1
    assert turns[0]["output_tokens"] == 3


def test_synthetic_records_are_skipped_and_counted_even_with_a_repeated_id(
        tmp_path: Path) -> None:
    synthetic = json.dumps({"message": {"id": "s", "model": sc.SYNTHETIC, "usage": {
        "input_tokens": 0, "output_tokens": 0}}})
    transcript = tmp_path / "x.jsonl"
    transcript.write_text(f"{synthetic}\n{synthetic}", encoding="utf-8")
    assert sc.read_turns(transcript) == ([], 2)
