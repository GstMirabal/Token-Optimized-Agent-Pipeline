"""Reviewed-copy check for the soft-bound claims in rules/token_economy.md.

Plan D23 (Sprint 059, unit A-25). QA Gate 1 judged two findings one family:
`rules/token_economy.md` section 3.1 described soft-threshold behaviour that
no instrument performs (N3: `session_probe.py` surfaces the breach; F1: the
soft threshold records and does not act). Per the `family_check` of
`workflows/remediation_workflow.md`, the check is reviewed-copy equality on
the two claim lines, plus a behavioural assertion behind the claim.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
RULE_FILE = ROOT / "rules" / "token_economy.md"

REVIEWED_SOFT_ROW = (
    "| **Soft** | turn > **5×** the cycle's first | Declare remaining cost in "
    "the plan's **Cost** section (work units left, delegation mode). "
    "`probe_cost` in `session_probe.py` reports only the hard bound, so no "
    "instrument surfaces a soft breach; the agent reads it with "
    "`session_cost.py --json` |"
)
REVIEWED_CALIBRATION = (
    "**Calibration that does not destroy its own data.** A binding hard "
    "threshold means the sprint always closes at the bound and the natural "
    "close is never observed. So the soft threshold **does not stop work**: "
    "the agent updates the plan's **Cost** section and continues, and no "
    "instrument records the breach. At the hard one the agent writes "
    "`forced: true` by hand, plus whether `task_scope.md` still held "
    "unfinished work. A forced close with pending work is the \"too tight\" "
    "signal; one on a complete sprint is not."
)

STALE_HINT = (
    "Re-review the claim against the instruments (session_probe.probe_cost, "
    "session_cost) before updating the reviewed copy in this test."
)


def find_line(text: str, prefix: str) -> str | None:
    """Return the first line of `text` that starts with `prefix`.

    Args:
        text: full text of the rule file.
        prefix: the line's required beginning.

    Returns:
        str | None: the whole line, or None when no line matches.
    """
    for line in text.splitlines():
        if line.startswith(prefix):
            return line
    return None


def check_claim(text: str, prefix: str, reviewed: str) -> None:
    """Assert the line beginning `prefix` in `text` equals `reviewed`.

    Args:
        text: full text of the rule file.
        prefix: the line's required beginning.
        reviewed: the reviewed literal copy.

    Raises:
        AssertionError: when the line is missing or differs.
    """
    line = find_line(text, prefix)
    assert line is not None, f"No line begins with {prefix!r}. {STALE_HINT}"
    assert line == reviewed, (
        f"Line beginning {prefix!r} changed.\n current: {line!r}\n"
        f" reviewed: {reviewed!r}\n{STALE_HINT}"
    )


@pytest.mark.parametrize(
    ("prefix", "reviewed"),
    [
        ("| **Soft** |", REVIEWED_SOFT_ROW),
        ("**Calibration that does not destroy its own data.**",
         REVIEWED_CALIBRATION),
    ],
)
def test_soft_bound_claim_matches_reviewed_copy(
    prefix: str, reviewed: str
) -> None:
    """The soft-bound claim lines equal their reviewed copies."""
    check_claim(RULE_FILE.read_text(encoding="utf-8"), prefix, reviewed)


def test_probe_cost_is_silent_on_a_soft_breach(monkeypatch) -> None:
    """A cycle at ratio 6 (soft, not hard) yields no probe_cost finding."""
    import session_probe as spr

    cycle = {"messages": 3, "first_turn": 10_000, "peak": 60_000, "ratio": 6}
    monkeypatch.setattr(spr.session_cost, "measure_previous", lambda *a, **k: {
        "measurable": True, "session": "abcdef123456", "cycles": [cycle]})
    assert 6 <= spr.HARD_RATIO
    assert spr.probe_cost({}) is None
