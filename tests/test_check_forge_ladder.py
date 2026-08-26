"""Tests for scripts/check_forge_ladder.py host forge ladder (Sprint 036 M2).

Fixture layout mirrors tests/test_installer.sh: a host tree with
``.agents/.git`` as a ``gitdir:`` pointer plus ``.claude/agents/`` and
``.claude/skills/``. ``_mode.is_nucleus`` and ``agents_root`` are patched so
the real checkout mode never affects outcomes.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"

AGENT_NAME = "forged_agent.md"
SKILL_NAME = "demo-skill"

AGENT_ASSIGNMENT = f"""\
# Agent Assignment — fixture

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| F1 | `agents/{AGENT_NAME}` | create | sequential | `agent_orchestrator` | `host:.claude/agents/` | `agents/agent_orchestrator.md` |
"""

SKILL_ASSIGNMENT = f"""\
# Skill Assignment — fixture

P3 miss recorded for ``{SKILL_NAME}``.

{{"source": "skills.sh", "hit": false}}

Forged to `.claude/skills/{SKILL_NAME}/SKILL.md`.
"""


def _host_layout(tmp_path: Path) -> tuple[Path, Path]:
    """Return ``(host_root, agents_root)`` matching test_installer.sh layout."""
    host = tmp_path / "host"
    agents = host / ".agents"
    agents.mkdir(parents=True)
    (agents / ".git").write_text("gitdir: ../.git/modules/.agents\n")
    (host / ".claude" / "agents").mkdir(parents=True)
    (host / ".claude" / "skills").mkdir(parents=True)
    (agents / "agents").mkdir(parents=True)
    (agents / "skills").mkdir(parents=True)
    return host, agents


@pytest.fixture()
def forge_mod(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    host, agents = _host_layout(tmp_path)
    monkeypatch.syspath_prepend(str(SCRIPTS))
    sys.modules.pop("check_forge_ladder", None)
    mod = importlib.import_module("check_forge_ladder")
    monkeypatch.setattr(mod, "is_nucleus", lambda: False)
    monkeypatch.setattr(mod, "agents_root", lambda: agents)
    sprint = tmp_path / "sprint"
    sprint.mkdir()
    return mod, host, agents, sprint


def _write_assignments(sprint: Path, *, agent: bool, skill: bool) -> None:
    if agent:
        (sprint / "agent_assignment.md").write_text(AGENT_ASSIGNMENT, encoding="utf-8")
    if skill:
        (sprint / "skill_assignment.md").write_text(SKILL_ASSIGNMENT, encoding="utf-8")


def test_host_agent_missing_forge_file_exits_2(
    forge_mod: tuple, capsys: pytest.CaptureFixture[str]
) -> None:
    mod, _host, _agents, sprint = forge_mod
    _write_assignments(sprint, agent=True, skill=False)

    assert mod.check(sprint) == 2
    err = capsys.readouterr().err
    assert "missing host forge file" in err


def test_host_agent_forged_under_claude_agents_exits_0(
    forge_mod: tuple, capsys: pytest.CaptureFixture[str]
) -> None:
    mod, host, _agents, sprint = forge_mod
    _write_assignments(sprint, agent=True, skill=False)
    (host / ".claude" / "agents" / AGENT_NAME).write_text("# forged\n", encoding="utf-8")

    assert mod.check(sprint) == 0
    assert "OK" in capsys.readouterr().out


def test_host_agent_forged_under_agents_submodule_exits_2(
    forge_mod: tuple, capsys: pytest.CaptureFixture[str]
) -> None:
    mod, _host, agents, sprint = forge_mod
    _write_assignments(sprint, agent=True, skill=False)
    (agents / "agents" / AGENT_NAME).write_text("# contamination\n", encoding="utf-8")

    assert mod.check(sprint) == 2
    err = capsys.readouterr().err
    assert "contamination" in err


def test_host_skill_missing_forge_file_exits_2(
    forge_mod: tuple, capsys: pytest.CaptureFixture[str]
) -> None:
    mod, _host, _agents, sprint = forge_mod
    _write_assignments(sprint, agent=False, skill=True)

    assert mod.check(sprint) == 2
    err = capsys.readouterr().err
    assert f"missing host skill file" in err
    assert SKILL_NAME in err


def test_host_skill_forged_under_claude_skills_exits_0(
    forge_mod: tuple, capsys: pytest.CaptureFixture[str]
) -> None:
    mod, host, _agents, sprint = forge_mod
    _write_assignments(sprint, agent=False, skill=True)
    skill_dir = host / ".claude" / "skills" / SKILL_NAME
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("---\nname: demo-skill\n---\n", encoding="utf-8")

    assert mod.check(sprint) == 0
    assert "OK" in capsys.readouterr().out


def test_host_skill_forged_under_agents_skills_exits_2(
    forge_mod: tuple, capsys: pytest.CaptureFixture[str]
) -> None:
    mod, _host, agents, sprint = forge_mod
    _write_assignments(sprint, agent=False, skill=True)
    skill_dir = agents / "skills" / SKILL_NAME
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("---\nname: demo-skill\n---\n", encoding="utf-8")

    assert mod.check(sprint) == 2
    err = capsys.readouterr().err
    assert "contamination" in err
    assert SKILL_NAME in err
