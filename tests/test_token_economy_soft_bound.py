"""Checks that `probe_cost` reports the absolute hard bound and stays silent below it."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


def _probe(monkeypatch: pytest.MonkeyPatch, peak: int, ratio: float) -> str | None:
    """Run `probe_cost` against one measured cycle.

    Args:
        monkeypatch: pytest fixture used to stub `measure_previous`.
        peak: the cycle's peak context size in tokens.
        ratio: the cycle's peak over first-turn ratio.

    Returns:
        str | None: the probe finding.
    """
    import session_probe as spr

    cycle = {"messages": 3, "first_turn": 10_000, "peak": peak, "ratio": ratio}
    monkeypatch.setattr(spr.session_cost, "measure_previous", lambda *a, **k: {
        "measurable": True, "session": "abcdef123456", "cycles": [cycle]})
    return spr.probe_cost({})


def test_probe_cost_is_silent_on_a_soft_breach(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A cycle at ratio 6 with a small peak yields no probe_cost finding."""
    assert _probe(monkeypatch, 60_000, 6) is None


def test_probe_cost_is_silent_one_token_below_the_bound(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A peak of 549,999 tokens is not reported."""
    assert _probe(monkeypatch, 549_999, 54.9) is None


def test_probe_cost_reports_a_peak_at_the_bound(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A peak of 550,000 tokens is reported with the absolute bound and the peak."""
    message = _probe(monkeypatch, 550_000, 55.0)
    assert message is not None
    assert "550,000" in message
    assert "cycle 1" in message


def test_probe_cost_ignores_a_high_ratio_under_the_bound(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A ratio of 20 with a peak of 200,000 tokens is not reported."""
    assert _probe(monkeypatch, 200_000, 20) is None
