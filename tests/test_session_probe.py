"""Graph freshness probe: built_at_commit ancestry, not mtime (Sprint 034 Track B)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import session_probe as spr

SOURCE_PY = "mod.py"


def _git(cwd: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=cwd, check=True, capture_output=True, text=True,
    )
    return result.stdout.strip()


def _repo(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    _git(path, "init", "-q", "-b", "main")
    _git(path, "config", "user.email", "t@example.com")
    _git(path, "config", "user.name", "T")
    (path / SOURCE_PY).write_text("x = 1\n", encoding="utf-8")
    _git(path, "add", SOURCE_PY)
    _git(path, "commit", "-qm", "source")
    return path


def _write_graph(path: Path, built_at: str | None) -> Path:
    graph_dir = path / "graphify-out"
    graph_dir.mkdir()
    payload: dict = {"directed": False, "graph": {}, "nodes": [], "links": []}
    if built_at is not None:
        payload["built_at_commit"] = built_at
    target = graph_dir / "graph.json"
    target.write_text(json.dumps(payload), encoding="utf-8")
    os.utime(target, (0, 0))
    return target


@pytest.fixture()
def graph_repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    repo = _repo(tmp_path / "repo")
    monkeypatch.chdir(repo)
    monkeypatch.setattr(spr, "GRAPH", repo / "graphify-out" / "graph.json")
    return repo


def test_stale_mtime_with_current_built_at_is_not_behind(graph_repo: Path) -> None:
    """Close used to rebuild the graph, then stamp changelog; mtime lost to HEAD %ct."""
    built = _git(graph_repo, "rev-parse", "HEAD")
    _write_graph(graph_repo, built)
    (graph_repo / "CHANGELOG.md").write_text("seal\n", encoding="utf-8")
    _git(graph_repo, "add", "CHANGELOG.md")
    _git(graph_repo, "commit", "-qm", "changelog after graph")
    os.utime(spr.GRAPH, (0, 0))
    assert spr.probe_graph() is None


def test_missing_built_at_does_not_claim_behind_from_mtime(graph_repo: Path) -> None:
    _write_graph(graph_repo, None)
    (graph_repo / "CHANGELOG.md").write_text("seal\n", encoding="utf-8")
    _git(graph_repo, "add", "CHANGELOG.md")
    _git(graph_repo, "commit", "-qm", "later non-source")
    os.utime(spr.GRAPH, (0, 0))
    assert spr.probe_graph() is None


def test_source_commit_after_graph_build_is_behind(graph_repo: Path) -> None:
    built = _git(graph_repo, "rev-parse", "HEAD")
    _write_graph(graph_repo, built)
    (graph_repo / SOURCE_PY).write_text("x = 2\n", encoding="utf-8")
    _git(graph_repo, "add", SOURCE_PY)
    _git(graph_repo, "commit", "-qm", "source after graph")
    report = spr.probe_graph()
    assert report is not None
    assert "behind" in report.lower() or "does not include" in report


def test_missing_graph_file_proposes_update(graph_repo: Path) -> None:
    assert spr.GRAPH.exists() is False
    report = spr.probe_graph()
    assert report is not None
    assert "graphify-out" in report


# --- probe_anchor_hygiene: sealed-status vocabulary (KI-052-2, Sprint 053 A2) -

def test_hygiene_fires_for_the_literal_release_writes() -> None:
    """`release()` writes `CLOSED_SUCCESSFULLY` (`session_state.CLOSED`), not
    the bare `"CLOSED"` this check compared against. Fails on HEAD: the
    finding never fires for the literal the writer actually produces."""
    state = {
        "status": "IN_PROGRESS",
        "current_sprint": {"id": 52, "status": "CLOSED_SUCCESSFULLY"},
    }

    finding = spr.probe_anchor_hygiene(state)

    assert finding is not None
    assert "CLOSED_SUCCESSFULLY" in finding


def test_hygiene_still_fires_for_the_legacy_closed_literal() -> None:
    """Regression guard: the legacy `"CLOSED"` alias (written before Sprint
    050) must keep firing once the comparison moves to `SEALED_STATUSES`."""
    state = {
        "status": "IN_PROGRESS",
        "current_sprint": {"id": 52, "status": "CLOSED"},
    }

    finding = spr.probe_anchor_hygiene(state)

    assert finding is not None


def test_hygiene_does_not_fire_for_an_open_sprint() -> None:
    state = {
        "status": "IN_PROGRESS",
        "current_sprint": {"id": 52, "status": "OPEN"},
    }

    assert spr.probe_anchor_hygiene(state) is None
