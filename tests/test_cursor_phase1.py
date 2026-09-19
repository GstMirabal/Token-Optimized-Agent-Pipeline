"""Pins H-004: Cursor Plan mode must not be Phase 1.

The sentence ``Where the environment offers planning mode, Phase 1 runs in it``
sent every Cursor session into a mode that forbids writing
``IMPLEMENTATION_PLAN.md``. That file is ``triple_lock`` lock 1.

A grep that only checks *this* file would miss the same instruction in
``agents.md`` (always loaded) or ``principal_agent.md`` (owns Phase 1).

`F-049-5` (Sprint 049): the four tests above assert the *documents* stay
consistent — none of them exercised the mechanism that actually stops a
violation from reaching a human. Nothing in this framework can intercept
Cursor's own `SwitchMode` tool call (`IMPLEMENTATION_PLAN.md` `## Out of
scope`, this sprint) — that is an IDE feature, not something this repository
controls. What IS controlled, and what Phase 5's own done-criterion names, is
the consequence: a Plan-mode session that skipped writing
`IMPLEMENTATION_PLAN.md` leaves nothing at the canonical path, and
`current_sprint_plan()` — the resolver `skills/token-saver-auditor/scripts/
audit_plan.py --current-sprint` uses, which `pipeline_workflow.md` Phase 5
cites by name — genuinely cannot find a plan to approve. The tests below pin
that behaviour directly, not its description in prose.
"""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "skills" / "token-saver-auditor" / "scripts"))
import audit_plan

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


# --- F-049-5: the consequence of a RA-18 violation is mechanically caught --


def _write_anchor(root: Path, sprint_id: int) -> None:
    anchor_dir = root / "docs"
    anchor_dir.mkdir(parents=True, exist_ok=True)
    (anchor_dir / "active_state.json").write_text(
        f'{{"current_sprint": {{"id": {sprint_id}}}}}', encoding="utf-8"
    )


def test_plan_mode_session_that_never_wrote_the_file_resolves_to_none(
    tmp_path: Path,
) -> None:
    """The exact H-004 scenario: Plan mode ran, IMPLEMENTATION_PLAN.md was
    never written. Phase 5's own resolver must find nothing to approve.

    `current_sprint_plan()` is not a description of the safeguard — it is the
    safeguard: `pipeline_workflow.md` Phase 5 names it, `skills/
    token-saver-auditor/scripts/audit_plan.py --current-sprint` runs it in
    `make verify`, and it is what this sprint's own Phase 5 ran before the
    human authorization was requested.
    """
    _write_anchor(tmp_path, sprint_id=49)
    (tmp_path / "docs" / "sprints" / "049-core-pipeline").mkdir(parents=True)
    # Deliberately no IMPLEMENTATION_PLAN.md — the Plan-mode failure mode.
    assert audit_plan.current_sprint_plan(tmp_path) is None


def test_plan_mode_session_that_did_write_the_file_resolves_to_it(
    tmp_path: Path,
) -> None:
    """The positive control: a plan actually written at the canonical path
    is found, so the negative test above is a real distinction, not a
    resolver that always returns None."""
    _write_anchor(tmp_path, sprint_id=49)
    sprint_dir = tmp_path / "docs" / "sprints" / "049-core-pipeline"
    sprint_dir.mkdir(parents=True)
    plan_path = sprint_dir / "IMPLEMENTATION_PLAN.md"
    plan_path.write_text("# Implementation Plan\n", encoding="utf-8")
    assert audit_plan.current_sprint_plan(tmp_path) == plan_path


def test_audit_plan_cli_reports_skip_not_pass_when_plan_absent(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """`audit_plan.py --current-sprint` must say "skip", never "[OK]" plain,
    for a plan that was never written — a session reading only stdout would
    otherwise mistake "nothing to check" for "checked and clean"."""
    _write_anchor(tmp_path, sprint_id=49)
    (tmp_path / "docs" / "sprints" / "049-core-pipeline").mkdir(parents=True)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["audit_plan.py", "--current-sprint"])
    code = audit_plan.main()
    out = capsys.readouterr().out
    assert code == 0
    assert "skip" in out
