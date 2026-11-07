"""Tests for scripts/_current_sprint.py: only an absent anchor or sprint block skips."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from _current_sprint import (
    CurrentSprintError,
    current_sprint_dir,
    project_root,
)


def _repo(tmp_path: Path, anchor: str | None, sprint_dir: str | None = "059-core-x") -> Path:
    """Build a fixture repository with an optional anchor text and sprint directory."""
    (tmp_path / ".git").mkdir()
    (tmp_path / "docs" / "sprints").mkdir(parents=True)
    if sprint_dir:
        (tmp_path / "docs" / "sprints" / sprint_dir).mkdir()
    if anchor is not None:
        (tmp_path / "docs" / "active_state.json").write_text(anchor, encoding="utf-8")
    return tmp_path


@pytest.mark.parametrize("sprint_id", [59, "059", "59"])
def test_integer_and_string_ids_resolve(tmp_path: Path, sprint_id: object) -> None:
    root = _repo(tmp_path, json.dumps({"current_sprint": {"id": sprint_id}}))
    assert current_sprint_dir(root) == root / "docs" / "sprints" / "059-core-x"


@pytest.mark.parametrize("anchor", [None, json.dumps({"status": "IN_PROGRESS"})])
def test_absent_anchor_or_sprint_block_skips(tmp_path: Path, anchor: str | None) -> None:
    assert current_sprint_dir(_repo(tmp_path, anchor)) is None


@pytest.mark.parametrize(
    "anchor",
    [
        '{"current_sprint": {"id": 59',
        "[]",
        json.dumps({"current_sprint": "059"}),
        json.dumps({"current_sprint": {}}),
        json.dumps({"current_sprint": {"id": True}}),
        json.dumps({"current_sprint": {"id": "not-a-sprint"}}),
    ],
)
def test_unusable_anchor_raises(tmp_path: Path, anchor: str) -> None:
    with pytest.raises(CurrentSprintError):
        current_sprint_dir(_repo(tmp_path, anchor))


def test_missing_sprint_directory_raises(tmp_path: Path) -> None:
    root = _repo(tmp_path, json.dumps({"current_sprint": {"id": 59}}), sprint_dir=None)
    with pytest.raises(CurrentSprintError):
        current_sprint_dir(root)


def test_project_root_climbs_to_the_git_ancestor(tmp_path: Path) -> None:
    root = _repo(tmp_path, None)
    assert project_root(root / "docs" / "sprints") == root.resolve()


def test_project_root_without_git_is_the_start(tmp_path: Path) -> None:
    assert project_root(tmp_path) == tmp_path.resolve()
