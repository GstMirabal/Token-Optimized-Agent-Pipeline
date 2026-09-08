"""Tests for hooks/state_mirror.py mirror_active_state().

Covers the Sprint 046 change (S045-21 / F-7): a corrupt anchor must log to
stderr and return without raising or blocking — the Stop hook may never
interrupt a session. Also guards the happy path and the absent-anchor no-op,
which the rest of the suite only ever monkeypatches away
(rules/qa_and_testing.md §3.1, "what green cannot see").
"""
from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


def _fresh_module(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    """Import hooks.state_mirror with its module-level relative Paths rebased
    onto tmp_path, so no test ever touches the real docs/active_state.json."""
    monkeypatch.chdir(tmp_path)
    sys.path.insert(0, str(REPO))
    sys.modules.pop("hooks.state_mirror", None)
    mod = importlib.import_module("hooks.state_mirror")
    monkeypatch.setattr(mod, "ACTIVE_STATE", Path("docs/active_state.json"))
    monkeypatch.setattr(mod, "MIRROR_STATE", Path(".agent_state/mirror.json"))
    return mod


def test_valid_anchor_is_mirrored(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    mod = _fresh_module(monkeypatch, tmp_path)
    (tmp_path / "docs").mkdir()
    payload = {"status": "IN_PROGRESS", "current_sprint": {"id": 46}}
    (tmp_path / "docs" / "active_state.json").write_text(json.dumps(payload), encoding="utf-8")

    mod.mirror_active_state()

    mirror = tmp_path / ".agent_state" / "mirror.json"
    assert mirror.exists()
    assert json.loads(mirror.read_text(encoding="utf-8")) == payload


def test_corrupt_anchor_logs_and_does_not_raise(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    mod = _fresh_module(monkeypatch, tmp_path)
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "active_state.json").write_text("{ not valid json", encoding="utf-8")

    mod.mirror_active_state()  # must not raise

    captured = capsys.readouterr()
    assert "mirror skipped" in captured.err
    assert captured.out == ""
    assert not (tmp_path / ".agent_state" / "mirror.json").exists()


def test_absent_anchor_is_a_noop(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    mod = _fresh_module(monkeypatch, tmp_path)

    mod.mirror_active_state()  # no docs/active_state.json at all

    assert not (tmp_path / ".agent_state").exists()
