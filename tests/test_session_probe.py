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
