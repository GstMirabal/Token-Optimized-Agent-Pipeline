"""Tests for scripts/check_role_artifact.py (Sprint 027 P2)."""

from __future__ import annotations

import importlib
import json
import subprocess
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
                        "host_path": "CHANGELOG.md",
                        "nucleus_path": "CHANGELOG.md",
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


# --- Sprint 052 D4 / F-051-R3: the hook resolved the wrong repository's
# sprint log when the session cwd and the repository the gate audits differ
# (a nested clone opened for `agents.md §4 feedback_upstream`). ---


def _init_repo(path: Path) -> None:
    """Create ``path`` and make it a git working tree (helper, not a test)."""
    path.mkdir(parents=True)
    subprocess.run(["git", "init", "-q"], cwd=path, check=True)


def _write_anchor(repo: Path, sprint_id: int) -> Path:
    """Write ``docs/active_state.json`` under ``repo``; return the sprint dir."""
    docs = repo / "docs"
    docs.mkdir(exist_ok=True)
    (docs / "active_state.json").write_text(
        json.dumps({"current_sprint": {"id": sprint_id, "layer": "core", "app": "pipeline"}}),
        encoding="utf-8",
    )
    sprint = docs / "sprints" / f"{sprint_id:03d}-core-pipeline"
    sprint.mkdir(parents=True)
    return sprint


def test_from_hook_declared_audited_repository_overrides_payload_cwd(
    check_mod, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """The rework (U17/U18 contract): a subagent starts in, and cannot
    change, the parent session's own cwd — so the payload's ``cwd`` is the
    **host's** directory even when the gate audited a separate nucleus
    clone. The gate's own ``last_assistant_message`` declaring ``Audited
    repository:`` must win over ``cwd``: the hook reads the nucleus's
    sprint log, never the host's, whose ``current_sprint`` names a
    different sprint entirely (`112` vs `51`)."""
    host = tmp_path / "host"
    _init_repo(host)
    _write_anchor(host, 112)  # the host's own, unrelated, sprint — must not be read

    nucleus = tmp_path / "nucleus-clone"
    _init_repo(nucleus)
    nucleus_sprint = _write_anchor(nucleus, 51)

    monkeypatch.chdir(tmp_path)  # neither host nor nucleus — proves declaration, not cwd, wins
    payload = json.dumps(
        {
            "agent_type": "orchestrator",
            "cwd": str(host),
            "last_assistant_message": f"Findings below.\nAudited repository: `{nucleus}`\nDone.",
        }
    )
    assert check_mod.main_from_hook(payload) == 2
    (nucleus_sprint / "SPRINT_LOG.md").write_text("# log\n", encoding="utf-8")
    assert check_mod.main_from_hook(payload) == 0


def test_from_hook_no_declaration_uses_payload_cwd(
    check_mod, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """No ``Audited repository:`` line in ``last_assistant_message``: the
    payload's own ``cwd`` is priority (2), read instead of the process's own
    cwd — which this test points at an unrelated, anchor-less directory to
    prove it is not what gets read."""
    other_repo = tmp_path / "cwd-repo"
    _init_repo(other_repo)
    sprint = _write_anchor(other_repo, 33)

    empty_cwd = tmp_path / "process-cwd"
    empty_cwd.mkdir()
    monkeypatch.chdir(empty_cwd)

    payload = json.dumps(
        {"agent_type": "orchestrator", "cwd": str(other_repo), "last_assistant_message": "No line here."}
    )
    assert check_mod.main_from_hook(payload) == 2
    (sprint / "SPRINT_LOG.md").write_text("# log\n", encoding="utf-8")
    assert check_mod.main_from_hook(payload) == 0


def test_from_hook_declared_path_outside_git_falls_back_to_cwd(
    check_mod, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Documented edge case (D4): the declared ``Audited repository:`` path
    is not inside any git working tree. Chosen behaviour cascades to the
    next candidate (the payload's own ``cwd``) rather than failing closed —
    `main_from_hook` already treats an unresolved sprint as an advisory
    skip, and an unresolvable declaration is not evidence of a missing
    artifact."""
    outside = tmp_path / "no-git-here"
    outside.mkdir()

    cwd_repo = tmp_path / "cwd-repo"
    _init_repo(cwd_repo)
    sprint = _write_anchor(cwd_repo, 27)

    monkeypatch.chdir(tmp_path)
    payload = json.dumps(
        {
            "agent_type": "orchestrator",
            "cwd": str(cwd_repo),
            "last_assistant_message": f"Audited repository: `{outside}`",
        }
    )
    assert check_mod.main_from_hook(payload) == 2
    (sprint / "SPRINT_LOG.md").write_text("# log\n", encoding="utf-8")
    assert check_mod.main_from_hook(payload) == 0


def test_from_hook_falls_back_to_process_cwd_when_no_path_given(
    check_mod, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Neither a declaration nor a ``cwd`` key on the payload: behaviour is
    the pre-fix cwd resolution, unchanged (D4's stated ultimate fallback)."""
    monkeypatch.chdir(tmp_path)
    sprint = _write_anchor(tmp_path, 27)
    payload = json.dumps({"agent_type": "orchestrator"})
    assert check_mod.main_from_hook(payload) == 2
    (sprint / "SPRINT_LOG.md").write_text("# log\n", encoding="utf-8")
    assert check_mod.main_from_hook(payload) == 0


# --- Sprint 057 B-7: the Tester row was demanded before the Tester phase was
# due (host H1). The SubagentStop hook fires on every tester-agent stop,
# including a mid-sprint dispatch, long before Gate 1 has approved. ---

_GATE_HEADER = (
    "| Gate | Round | Verdict | Class | Notes |\n"
    "| :--- | :--- | :--- | :--- | :--- |\n"
)


def _tester_sprint(tmp_path: Path, rows: str) -> Path:
    """Sprint dir whose SPRINT_LOG.md holds the gate table with ``rows``."""
    sprint = tmp_path / "sprint"
    sprint.mkdir()
    (sprint / "SPRINT_LOG.md").write_text(_GATE_HEADER + rows, encoding="utf-8")
    return sprint


def test_tester_row_not_demanded_before_qa_gate_approved(check_mod, tmp_path: Path) -> None:
    """Gate 1 has not approved (no row, then REJECTED): the Tester phase is
    not due, so a tester-agent stop must not be blocked for a missing row."""
    sprint = _tester_sprint(tmp_path, "")
    assert check_mod.main(["--role", "tester_agent", "--sprint-dir", str(sprint)]) == 0
    (sprint / "SPRINT_LOG.md").write_text(
        _GATE_HEADER + "| QA (structural) | 1 | **REJECTED** | charter | ruff |\n",
        encoding="utf-8",
    )
    assert check_mod.main(["--role", "tester_agent", "--sprint-dir", str(sprint)]) == 0


def test_tester_row_required_once_qa_gate_approved(check_mod, tmp_path: Path) -> None:
    """The requirement stays at close: QA approved, Tester row absent -> 2."""
    sprint = _tester_sprint(tmp_path, "| QA (structural) | 2 | **APPROVED** | | ok |\n")
    assert check_mod.main(["--role", "tester_agent", "--sprint-dir", str(sprint)]) == 2
    (sprint / "SPRINT_LOG.md").write_text(
        _GATE_HEADER
        + "| QA (structural) | 2 | **APPROVED** | | ok |\n"
        + "| Tester (functional) | 1 | **APPROVED** | | ok |\n",
        encoding="utf-8",
    )
    assert check_mod.main(["--role", "tester_agent", "--sprint-dir", str(sprint)]) == 0


# --- Sprint 059 F-03 / D81: --owner-commit bounds a ledger seal by the
# ADR-0020 owner_writes lines. ---

_SEAL_BASE = "# Changelog\n\n## [Unreleased]\n\n### Added\n- one\n- two\n- three\n"
_SEAL_HEAD = "## [Unreleased]\n\n## [1.2.3] - 2026-01-01\n\n"
_BOUNDS = {"max_added_lines": 5, "max_deleted_lines": 2}


def _git(repo: Path, *args: str) -> str:
    """Run git in ``repo`` with a fixed identity; return stdout (helper)."""
    env = {
        "GIT_AUTHOR_NAME": "t",
        "GIT_AUTHOR_EMAIL": "t@example.invalid",
        "GIT_COMMITTER_NAME": "t",
        "GIT_COMMITTER_EMAIL": "t@example.invalid",
        "PATH": "/usr/bin:/bin:/usr/local/bin:/opt/homebrew/bin",
        "HOME": str(repo),
    }
    done = subprocess.run(
        ["git", *args], cwd=repo, env=env, check=True, capture_output=True, text=True
    )
    return done.stdout.strip()


def _commit(repo: Path, files: dict[str, str]) -> str:
    """Write ``files`` under ``repo``, commit them and return the new sha."""
    for name, text in files.items():
        (repo / name).write_text(text, encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "change")
    return _git(repo, "rev-parse", "HEAD")


def _owner_repo(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, bounds: dict | None
) -> Path:
    """Temp git repo holding ``_SEAL_BASE``; registry CHANGELOG entry gets ``bounds``."""
    registry = tmp_path / "config" / "artifact_registry.json"
    data = json.loads(registry.read_text(encoding="utf-8"))
    for entry in data["artifacts"]:
        if entry["filename"] == "CHANGELOG.md" and bounds is not None:
            entry["owner_writes"] = bounds
    registry.write_text(json.dumps(data), encoding="utf-8")
    repo = tmp_path / "work"
    _init_repo(repo)
    _commit(repo, {"CHANGELOG.md": _SEAL_BASE})
    monkeypatch.chdir(repo)
    return repo


def test_owner_commit_two_added_seal_passes(check_mod, monkeypatch, tmp_path: Path) -> None:
    repo = _owner_repo(monkeypatch, tmp_path, _BOUNDS)
    sha = _commit(repo, {"CHANGELOG.md": _SEAL_BASE.replace("## [Unreleased]\n\n", _SEAL_HEAD)})
    assert check_mod.main(["--owner-commit", sha]) == 0


def test_owner_commit_five_one_seal_passes(check_mod, monkeypatch, tmp_path: Path) -> None:
    repo = _owner_repo(monkeypatch, tmp_path, _BOUNDS)
    text = _SEAL_BASE.replace("## [Unreleased]\n\n", _SEAL_HEAD).replace(
        "- three\n", "- three, replaced\n- a\n- b\n"
    )
    assert check_mod.main(["--owner-commit", _commit(repo, {"CHANGELOG.md": text})]) == 0


def test_owner_commit_six_added_fails(check_mod, monkeypatch, tmp_path: Path, capsys) -> None:
    repo = _owner_repo(monkeypatch, tmp_path, _BOUNDS)
    text = _SEAL_BASE.replace("## [Unreleased]\n\n", _SEAL_HEAD) + "- x\n- y\n- z\n- w\n"
    assert check_mod.main(["--owner-commit", _commit(repo, {"CHANGELOG.md": text})]) != 0
    assert "added 6" in capsys.readouterr().err


def test_owner_commit_three_deleted_fails(check_mod, monkeypatch, tmp_path: Path, capsys) -> None:
    repo = _owner_repo(monkeypatch, tmp_path, _BOUNDS)
    text = "# Changelog\n\n" + _SEAL_HEAD + "### Added\n"
    assert check_mod.main(["--owner-commit", _commit(repo, {"CHANGELOG.md": text})]) != 0
    assert "deleted 3" in capsys.readouterr().err


def test_owner_commit_not_a_seal_fails(check_mod, monkeypatch, tmp_path: Path, capsys) -> None:
    repo = _owner_repo(monkeypatch, tmp_path, _BOUNDS)
    sha = _commit(repo, {"CHANGELOG.md": _SEAL_BASE + "- four\n"})
    assert check_mod.main(["--owner-commit", sha]) != 0
    assert "not a ledger seal" in capsys.readouterr().err


def test_owner_commit_missing_bound_fails(check_mod, monkeypatch, tmp_path: Path, capsys) -> None:
    repo = _owner_repo(monkeypatch, tmp_path, {"max_added_lines": 5})
    sha = _commit(repo, {"CHANGELOG.md": _SEAL_BASE.replace("## [Unreleased]\n\n", _SEAL_HEAD)})
    assert check_mod.main(["--owner-commit", sha]) != 0
    assert "max_deleted_lines" in capsys.readouterr().err


def test_owner_commit_other_artifact_fails(check_mod, monkeypatch, tmp_path: Path) -> None:
    repo = _owner_repo(monkeypatch, tmp_path, _BOUNDS)
    sha = _commit(
        repo,
        {
            "CHANGELOG.md": _SEAL_BASE.replace("## [Unreleased]\n\n", _SEAL_HEAD),
            "SPRINT_LOG.md": "# log\n",
        },
    )
    assert check_mod.main(["--owner-commit", sha]) != 0


def test_owner_commit_seal_with_unregistered_file_exits_1(
    check_mod, monkeypatch, tmp_path: Path, capsys
) -> None:
    """R32-2: a seal that also edits a file outside the registry is refused, naming it."""
    repo = _owner_repo(monkeypatch, tmp_path, _BOUNDS)
    (repo / "scripts").mkdir()
    sha = _commit(
        repo,
        {
            "CHANGELOG.md": _SEAL_BASE.replace("## [Unreleased]\n\n", _SEAL_HEAD),
            "scripts/install.py": "x = 1\n",
        },
    )
    assert check_mod.main(["--owner-commit", sha]) == 1
    assert "scripts/install.py" in capsys.readouterr().err


def test_owner_commit_seal_with_nested_same_name_file_exits_1(
    check_mod, monkeypatch, tmp_path: Path, capsys
) -> None:
    """R33-1: a nested CHANGELOG.md is not the registry artifact; the seal is refused, naming it."""
    repo = _owner_repo(monkeypatch, tmp_path, _BOUNDS)
    (repo / "skills" / "probe").mkdir(parents=True)
    sha = _commit(
        repo,
        {
            "CHANGELOG.md": _SEAL_BASE.replace("## [Unreleased]\n\n", _SEAL_HEAD),
            "skills/probe/CHANGELOG.md": "# probe\n",
        },
    )
    assert check_mod.main(["--owner-commit", sha]) == 1
    assert "skills/probe/CHANGELOG.md" in capsys.readouterr().err


def test_owner_commit_nested_same_name_file_alone_exits_1(
    check_mod, monkeypatch, tmp_path: Path, capsys
) -> None:
    """R33-1: a nested CHANGELOG.md alone satisfies neither the seal nor the bound check."""
    repo = _owner_repo(monkeypatch, tmp_path, _BOUNDS)
    (repo / "skills" / "probe").mkdir(parents=True)
    sha = _commit(repo, {"skills/probe/CHANGELOG.md": "# probe\n"})
    assert check_mod.main(["--owner-commit", sha]) == 1
    assert "skills/probe/CHANGELOG.md" in capsys.readouterr().err


def test_owner_commit_bad_sha_exits_2(check_mod, monkeypatch, tmp_path: Path, capsys) -> None:
    _owner_repo(monkeypatch, tmp_path, _BOUNDS)
    assert check_mod.main(["--owner-commit", "deadbeef"]) == 2
    assert "Traceback" not in capsys.readouterr().err
