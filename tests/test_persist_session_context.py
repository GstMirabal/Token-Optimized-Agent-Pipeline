"""Tests for scripts/persist_session_context.py (Sprint 027 P1)."""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


@pytest.fixture()
def persist(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.syspath_prepend(str(REPO))
    sys.modules.pop("persist_session_context", None)
    sys.modules.pop("scripts.persist_session_context", None)
    return importlib.import_module("scripts.persist_session_context")


def test_task_scope_path_from_anchor(persist) -> None:
    state = {"current_sprint": {"id": 27, "layer": "core", "app": "pipeline"}}
    path = persist.task_scope_path(state)
    assert path == Path("docs/sprints/027-core-pipeline/task_scope.md")


def test_main_mirrors_valid_anchor(
    persist, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys
) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "docs").mkdir()
    anchor = tmp_path / "docs" / "active_state.json"
    anchor.write_text(
        json.dumps(
            {
                "session_id": "test-sess",
                "status": "IN_PROGRESS",
                "current_sprint": {"id": 27, "layer": "core", "app": "pipeline"},
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(persist, "ACTIVE_STATE", Path("docs/active_state.json"))
    mirrored: list[bool] = []

    def _mirror() -> None:
        mirrored.append(True)
        (tmp_path / ".agent_state").mkdir(exist_ok=True)
        (tmp_path / ".agent_state" / "mirror.json").write_text(
            anchor.read_text(encoding="utf-8"), encoding="utf-8"
        )

    monkeypatch.setattr(persist, "mirror_active_state", _mirror)
    assert persist.main() == 0
    assert mirrored == [True]
    out = capsys.readouterr().out
    assert "test-sess" in out
    assert "027-core-pipeline/task_scope.md" in out


def test_main_rejects_invalid_json(
    persist, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "active_state.json").write_text("{not-json", encoding="utf-8")
    monkeypatch.setattr(persist, "ACTIVE_STATE", Path("docs/active_state.json"))
    assert persist.main() == 2
