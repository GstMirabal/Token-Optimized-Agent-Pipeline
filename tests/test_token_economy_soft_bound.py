"""Checks that `probe_cost` reports the hard bound and stays silent below it."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


def test_probe_cost_is_silent_on_a_soft_breach(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A cycle at ratio 6 (soft, not hard) yields no probe_cost finding."""
    import session_probe as spr

    cycle = {"messages": 3, "first_turn": 10_000, "peak": 60_000, "ratio": 6}
    monkeypatch.setattr(spr.session_cost, "measure_previous", lambda *a, **k: {
        "measurable": True, "session": "abcdef123456", "cycles": [cycle]})
    assert 6 <= spr.HARD_RATIO
    assert spr.probe_cost({}) is None


def test_probe_cost_reports_a_hard_breach(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A cycle at ratio 16 (hard) yields a probe_cost finding."""
    import session_probe as spr

    cycle = {"messages": 3, "first_turn": 10_000, "peak": 160_000, "ratio": 16}
    monkeypatch.setattr(spr.session_cost, "measure_previous", lambda *a, **k: {
        "measurable": True, "session": "abcdef123456", "cycles": [cycle]})
    assert 16 > spr.HARD_RATIO
    assert spr.probe_cost({}) is not None
