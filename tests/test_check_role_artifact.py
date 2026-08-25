"""Tests for scripts/check_role_artifact.py (Sprint 027 P2)."""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"


@pytest.fixture()
def check_mod(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    monkeypatch.syspath_prepend(str(SCRIPTS))
    monkeypatch.syspath_prepend(str(REPO))
    # Minimal registry under a fake agents_root.
    config = tmp_path / "config"
    config.mkdir()
    (config / "artifact_registry.json").write_text(
        json.dumps(
            {
                "artifacts": [
                    {
                        "filename": "SPRINT_LOG.md",
                        "role": "Orchestrator",
                        "scope": "sprint",
                        "required": True,
                    },
                    {
                        "filename": "task_scope.md",
                        "role": "Rule Validator",
                        "scope": "sprint",
                        "required": True,
                    },
                    {
                        "filename": "CHANGELOG.md",
                        "role": "Principal Agent",
                        "scope": "repository",
                        "required": True,
                    },
                ]
            }
        ),
        encoding="utf-8",
    )
    sys.modules.pop("check_role_artifact", None)
    mod = importlib.import_module("check_role_artifact")
    monkeypatch.setattr(mod, "agents_root", lambda: tmp_path)
    return mod


def test_missing_required_artifact_exits_2(check_mod, tmp_path: Path) -> None:
    sprint = tmp_path / "sprint"
    sprint.mkdir()
    assert check_mod.main(["--role", "Orchestrator", "--sprint-dir", str(sprint)]) == 2


def test_present_required_artifact_exits_0(check_mod, tmp_path: Path) -> None:
    sprint = tmp_path / "sprint"
    sprint.mkdir()
    (sprint / "SPRINT_LOG.md").write_text("# log\n", encoding="utf-8")
    assert check_mod.main(["--role", "Orchestrator", "--sprint-dir", str(sprint)]) == 0


def test_repository_scope_ignored(check_mod, tmp_path: Path) -> None:
    sprint = tmp_path / "sprint"
    sprint.mkdir()
    # Principal Agent's CHANGELOG is repository-scoped — not required here.
    assert (
        check_mod.main(["--role", "Principal Agent", "--sprint-dir", str(sprint)]) == 0
    )
