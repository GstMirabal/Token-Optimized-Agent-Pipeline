"""Tests for scripts/model_ledger.py (Sprint 037 G2)."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"

GATE_HEADER = """\
## Phase 7 — Quality Gate

| Gate | Round | Verdict | Class | Notes |
| :--- | :--- | :--- | :--- | :--- |
"""


@pytest.fixture()
def ledger_mod(monkeypatch: pytest.MonkeyPatch):
    """Import model_ledger with scripts/ on sys.path."""
    monkeypatch.syspath_prepend(str(SCRIPTS))
    sys.modules.pop("model_ledger", None)
    return importlib.import_module("model_ledger")


def _write_sprint(
    root: Path,
    number: int,
    *,
    log: str | None = None,
    scope: str | None = None,
) -> Path:
    sprint = root / "docs" / "sprints" / f"{number:03d}-core-pipeline"
    sprint.mkdir(parents=True, exist_ok=True)
    if log is not None:
        (sprint / "SPRINT_LOG.md").write_text(log, encoding="utf-8")
    if scope is not None:
        (sprint / "task_scope.md").write_text(scope, encoding="utf-8")
    return sprint


def test_no_sprint_log_omitted(
    ledger_mod,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    root = tmp_path / "repo"
    _write_sprint(root, 32)  # directory only — no SPRINT_LOG.md
    monkeypatch.setattr(ledger_mod, "agents_root", lambda: root)
    rows, omitted = ledger_mod.collect(root)
    assert rows == []
    assert any("no SPRINT_LOG.md" in note for note in omitted)
    body = ledger_mod.render_markdown(rows, omitted)
    assert "| 32 |" not in body
    assert "032-core-pipeline: no SPRINT_LOG.md" in body


def test_pre_031_omitted(
    ledger_mod,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    root = tmp_path / "repo"
    log = GATE_HEADER + "| QA (structural) | 1 | **APPROVED** | | ok |\n"
    _write_sprint(root, 30, log=log)
    monkeypatch.setattr(ledger_mod, "agents_root", lambda: root)
    rows, omitted = ledger_mod.collect(root)
    assert rows == []
    assert any("sprint id < 31" in note for note in omitted)


def test_gate1_two_rounds_counted(
    ledger_mod,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    root = tmp_path / "repo"
    log = (
        GATE_HEADER
        + "| QA (structural) | 1 | **REJECTED** | charter | first |\n"
        + "| QA (structural) | 2 | **APPROVED** | | second |\n"
        + "| Tester (functional) | 1 | **APPROVED** | | ok |\n"
    )
    scope = """\
## Work

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U1 | `scripts/x.py` | create | high | `implementer_agent` | `grok-4.5` | `high` | ✅ |
"""
    _write_sprint(root, 32, log=log, scope=scope)
    monkeypatch.setattr(ledger_mod, "agents_root", lambda: root)
    rows, _omitted = ledger_mod.collect(root)
    assert len(rows) == 1
    assert rows[0]["gate1_rounds"] == 2
    assert rows[0]["gate2_rounds"] == 1
    assert rows[0]["units"] == 1
    assert rows[0]["model_id"] == "grok-4.5"
    assert ledger_mod.main() == 0
    text = (root / ledger_mod.OUT_REL).read_text(encoding="utf-8")
    assert "| 32 |" in text
