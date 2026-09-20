"""Tests for scripts/audit_cursor_era.py (Sprint 036 L2)."""

from __future__ import annotations

import importlib
import shutil
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"
SPRINT_033 = REPO / "docs" / "sprints" / "033-core-pipeline"


@pytest.fixture()
def audit_mod(monkeypatch: pytest.MonkeyPatch):
    """Import audit_cursor_era with scripts/ on sys.path."""
    monkeypatch.syspath_prepend(str(SCRIPTS))
    sys.modules.pop("audit_cursor_era", None)
    return importlib.import_module("audit_cursor_era")


def _copy_registry(root: Path) -> None:
    shutil.copytree(REPO / "config", root / "config")


def _write_sprint(
    root: Path,
    number: int,
    *,
    task_scope: str | None = None,
    tool: str | None = "cursor",
) -> Path:
    """A minimal sprint dir. ``tool`` writes the SPRINT_LOG.md Session line
    `era_sprint_ids` reads (`D5`); pass ``None`` to omit it entirely."""
    sprint = root / "docs" / "sprints" / f"{number:03d}-core-pipeline"
    sprint.mkdir(parents=True, exist_ok=True)
    if task_scope is not None:
        (sprint / "task_scope.md").write_text(task_scope, encoding="utf-8")
    if tool is not None:
        (sprint / "SPRINT_LOG.md").write_text(
            f"# Sprint Log: #{number}\n\n"
            f"**Session**: `x` · tool `{tool}` · `delegation_mode: sequential`\n",
            encoding="utf-8",
        )
    return sprint


def test_missing_sprint_dirs_omitted_and_main_exits_zero(
    audit_mod,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "repo"
    _write_sprint(root, 26, task_scope="# scope\n")
    _write_sprint(root, 30, task_scope="# scope\n")
    _copy_registry(root)
    monkeypatch.setattr(audit_mod, "agents_root", lambda: root)

    found = audit_mod.iter_era_dirs(root)
    assert [path.name for path in found] == ["026-core-pipeline", "030-core-pipeline"]

    assert audit_mod.main() == 0
    captured = capsys.readouterr()
    assert "2 sprint rows" in captured.out

    audit_text = (root / audit_mod.OUT_REL).read_text(encoding="utf-8")
    assert "| 026 |" in audit_text
    assert "| 030 |" in audit_text
    assert "| 027 |" not in audit_text
    assert "| 033 |" not in audit_text


# --- F-049-3 / D5: the era window is derived from SPRINT_LOG.md, not fixed ---


def test_era_sprint_ids_excludes_a_sprint_with_no_cursor_tool(
    audit_mod, tmp_path: Path
) -> None:
    """The exact defect this sprint fixes: a hardcoded 26-33 both included a
    sprint with no evidence and excluded 034-040, which had real evidence."""
    root = tmp_path / "repo"
    _write_sprint(root, 27, tool="cursor")
    _write_sprint(root, 28, tool="claude-code")
    _write_sprint(root, 29, tool=None)  # no Session line at all
    _write_sprint(root, 41, tool="cursor")

    assert audit_mod.era_sprint_ids(root) == [27, 41]


def test_era_sprint_ids_on_the_real_repository_matches_the_measured_window(
    audit_mod,
) -> None:
    """Reproduces the Phase 1 measurement: `grep -oE 'tool `[a-z-]+`'` across
    every docs/sprints/*/SPRINT_LOG.md gives cursor sprints 027-040, nothing
    before or after. Fails if the real sprint logs ever drift from that."""
    ids = audit_mod.era_sprint_ids(REPO)
    assert ids == list(range(27, 41))


def test_sprint_033_ce1_is_zero(audit_mod) -> None:
    assert SPRINT_033.is_dir(), "real sprint 033 tree required"
    assert audit_mod.ce1_count(SPRINT_033) == 0


def test_ce4_one_when_tester_notes_cite_pytest_without_tests_path(
    audit_mod,
    tmp_path: Path,
) -> None:
    sprint = tmp_path / "033-core-pipeline"
    sprint.mkdir()
    log = """## Gate log

| Gate | Round | Verdict | Class | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Tester (functional) | 1 | **APPROVED** | | `pytest test_implementer_role.py` 4 passed |
"""
    (sprint / "SPRINT_LOG.md").write_text(log, encoding="utf-8")
    assert audit_mod.ce4_count(sprint) == 1


def test_main_regenerates_deleted_audit_markdown(
    audit_mod,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    root = tmp_path / "repo"
    sprint = _write_sprint(root, 33)
    shutil.copy(SPRINT_033 / "task_scope.md", sprint / "task_scope.md")
    _copy_registry(root)
    monkeypatch.setattr(audit_mod, "agents_root", lambda: root)

    assert audit_mod.main() == 0
    out_path = root / audit_mod.OUT_REL
    first = out_path.read_text(encoding="utf-8")
    assert "Derived by `scripts/audit_cursor_era.py`" in first
    assert "Do not edit by hand." in first

    out_path.unlink()
    assert not out_path.exists()

    assert audit_mod.main() == 0
    second = out_path.read_text(encoding="utf-8")
    assert second == first
