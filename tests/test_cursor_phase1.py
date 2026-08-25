"""Pins H-004: Cursor Plan mode must not be Phase 1.

The sentence ``Where the environment offers planning mode, Phase 1 runs in it``
sent every Cursor session into a mode that forbids writing
``IMPLEMENTATION_PLAN.md``. That file is ``triple_lock`` lock 1.

A grep that only checks *this* file would miss the same instruction in
``agents.md`` (always loaded) or ``principal_agent.md`` (owns Phase 1).
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Unqualified. The Cursor exception lives beside it after H-004; this exact
# clause without a prohibition is the defect.
UNQUALIFIED_PLAN_MODE = (
    "Where the environment offers planning mode, Phase 1 runs in it"
)


def test_pipeline_phase1_does_not_unconditionally_enter_plan_mode() -> None:
    text = (ROOT / "workflows" / "pipeline_workflow.md").read_text(encoding="utf-8")
    assert UNQUALIFIED_PLAN_MODE not in text
    assert "SwitchMode" in text
    assert "PROHIBITED" in text
    assert "session_tool: cursor" in text or "session_tool` is `cursor`" in text


def test_agents_md_indexes_ra18() -> None:
    text = (ROOT / "agents.md").read_text(encoding="utf-8")
    assert "RA-18" in text
    assert "CURSOR_PHASE1_NO_PLAN_MODE" in text


def test_principal_agent_phase1_forbids_cursor_switchmode() -> None:
    text = (ROOT / "agents" / "principal_agent.md").read_text(encoding="utf-8")
    assert "SwitchMode" in text
    assert "cursor" in text.lower()


def test_start_pipeline_handoff_names_cursor_phase1() -> None:
    text = (ROOT / "workflows" / "start_workflow.md").read_text(encoding="utf-8")
    idx = text.index("`pipeline_invocation`")
    window = text[idx : idx + 1200]
    assert "SwitchMode" in window
    assert "cursor" in window.lower()
