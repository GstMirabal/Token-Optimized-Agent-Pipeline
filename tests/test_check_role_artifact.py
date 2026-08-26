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
                ],
                "gate_evidence": {
                    "file": "SPRINT_LOG.md",
                    "roles": {"QA Agent": "QA", "Tester Agent": "Tester"},
                },
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


def test_role_from_agent_type_maps_frontmatter_names(check_mod) -> None:
    assert check_mod.role_from_agent_type("orchestrator") == "Orchestrator"
    assert check_mod.role_from_agent_type("agent-orchestrator") == "Agent Orchestrator"


# --- Sprint 034 D17: absence used to be reported as success. ---


def test_profile_name_is_accepted_like_the_display_name(check_mod, tmp_path: Path) -> None:
    """The bug: the framework writes `rule_validator`, the registry writes
    `Rule Validator`, and the literal comparison matched nothing — which the
    script called success. Both spellings must now reach the same verdict."""
    sprint = tmp_path / "sprint"
    sprint.mkdir()
    assert check_mod.main(["--role", "rule_validator", "--sprint-dir", str(sprint)]) == 2
    assert check_mod.main(["--role", "Rule Validator", "--sprint-dir", str(sprint)]) == 2


def test_unknown_role_is_refused_not_approved(check_mod, tmp_path: Path) -> None:
    sprint = tmp_path / "sprint"
    sprint.mkdir()
    assert check_mod.main(["--role", "no_such_role", "--sprint-dir", str(sprint)]) == 2


def test_no_title_case_fabrication(check_mod) -> None:
    """`qa-agent` used to become `Qa Agent`, which matched no entry."""
    assert check_mod.role_from_agent_type("qa-agent") == "QA Agent"
    assert check_mod.role_from_agent_type("not-a-profile") is None


def test_known_profile_absent_from_registry_says_so(check_mod, tmp_path: Path) -> None:
    sprint = tmp_path / "sprint"
    sprint.mkdir()
    assert check_mod.main(["--role", "implementer_agent", "--sprint-dir", str(sprint)]) == 0


def test_gate_role_needs_a_gate_row_not_just_the_file(check_mod, tmp_path: Path) -> None:
    """A gate owns no file: SPRINT_LOG.md exists from Phase 3, before any gate
    runs. Only a row naming the gate shows it ran."""
    sprint = tmp_path / "sprint"
    sprint.mkdir()
    log = sprint / "SPRINT_LOG.md"
    log.write_text("# log\n", encoding="utf-8")
    assert check_mod.main(["--role", "qa_agent", "--sprint-dir", str(sprint)]) == 2

    log.write_text(
        "| Gate | Round | Verdict | Class | Notes |\n"
        "| :--- | :--- | :--- | :--- | :--- |\n"
        "| QA (structural) | 1 | **APPROVED** | | ruff exit 0 |\n",
        encoding="utf-8",
    )
    assert check_mod.main(["--role", "qa_agent", "--sprint-dir", str(sprint)]) == 0
    assert check_mod.main(["--role", "tester_agent", "--sprint-dir", str(sprint)]) == 2


def test_from_hook_missing_sprint_skips(check_mod, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)
    payload = json.dumps({"agent_type": "orchestrator", "hook_event_name": "SubagentStop"})
    assert check_mod.main_from_hook(payload) == 0


def test_from_hook_enforces_when_anchor_and_sprint_exist(
    check_mod, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.chdir(tmp_path)
    sprint = tmp_path / "docs" / "sprints" / "027-core-pipeline"
    sprint.mkdir(parents=True)
    docs = tmp_path / "docs"
    docs.mkdir(exist_ok=True)
    (docs / "active_state.json").write_text(
        json.dumps(
            {
                "current_sprint": {
                    "id": 27,
                    "layer": "core",
                    "app": "pipeline",
                }
            }
        ),
        encoding="utf-8",
    )
    payload = json.dumps({"agent_type": "orchestrator"})
    assert check_mod.main_from_hook(payload) == 2
    (sprint / "SPRINT_LOG.md").write_text("# log\n", encoding="utf-8")
    assert check_mod.main_from_hook(payload) == 0
