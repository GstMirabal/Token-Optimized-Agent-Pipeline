"""Tests for scripts/extract_plan.py (Sprint 057, defect C-8)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import extract_plan


@pytest.fixture
def host(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A host root with a draft plan, as the cwd."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "draft.md").write_text("plan\n", encoding="utf-8")
    return tmp_path


def write_anchor(root: Path, body: object) -> None:
    """Write the anchor under `root`."""
    (root / "docs").mkdir(exist_ok=True)
    (root / "docs/active_state.json").write_text(json.dumps(body), encoding="utf-8")


def test_copy_into_absent_dest(host: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert extract_plan.main(["draft.md", "--sprint-dir", "docs/sprints/1"]) == 0
    dest = host / "docs/sprints/1/IMPLEMENTATION_PLAN.md"
    assert dest.read_text(encoding="utf-8") == "plan\n"
    assert "IMPLEMENTATION_PLAN.md" in capsys.readouterr().out


def test_identical_dest_is_unchanged(host: Path) -> None:
    (host / "s").mkdir()
    dest = host / "s/IMPLEMENTATION_PLAN.md"
    dest.write_text("plan\n", encoding="utf-8")
    before = dest.stat().st_mtime_ns
    assert extract_plan.main(["draft.md", "--sprint-dir", "s"]) == 0
    assert dest.stat().st_mtime_ns == before


def test_differing_dest_is_refused(host: Path, capsys: pytest.CaptureFixture[str]) -> None:
    (host / "s").mkdir()
    dest = host / "s/IMPLEMENTATION_PLAN.md"
    dest.write_text("other\n", encoding="utf-8")
    assert extract_plan.main(["draft.md", "--sprint-dir", "s"]) == 2
    assert dest.read_text(encoding="utf-8") == "other\n"
    assert "draft.md" in capsys.readouterr().err


def test_missing_source(host: Path) -> None:
    assert extract_plan.main(["nope.md", "--sprint-dir", "s"]) == 2
    assert not (host / "s").exists()


def test_source_is_a_directory(host: Path) -> None:
    (host / "d").mkdir()
    assert extract_plan.main(["d", "--sprint-dir", "s"]) == 2


def test_source_equals_dest(host: Path) -> None:
    (host / "s").mkdir()
    dest = host / "s/IMPLEMENTATION_PLAN.md"
    dest.write_text("plan\n", encoding="utf-8")
    assert extract_plan.main(["s/IMPLEMENTATION_PLAN.md", "--sprint-dir", "s"]) == 2
    assert dest.read_text(encoding="utf-8") == "plan\n"


def test_dir_from_anchor(host: Path) -> None:
    write_anchor(host, {"current_sprint": {"path": "docs/sprints/9-x"}})
    assert extract_plan.main(["draft.md"]) == 0
    assert (host / "docs/sprints/9-x/IMPLEMENTATION_PLAN.md").is_file()


def test_missing_anchor(host: Path) -> None:
    assert extract_plan.main(["draft.md"]) == 2


@pytest.mark.parametrize("body", [{}, {"current_sprint": {}}, [1]])
def test_anchor_without_path(host: Path, body: object) -> None:
    write_anchor(host, body)
    assert extract_plan.main(["draft.md"]) == 2


def test_malformed_anchor(host: Path) -> None:
    (host / "docs").mkdir()
    (host / "docs/active_state.json").write_text("{", encoding="utf-8")
    assert extract_plan.main(["draft.md"]) == 2
