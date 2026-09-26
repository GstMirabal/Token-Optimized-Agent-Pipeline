"""Tests for scripts/graph_reconcile.py -- the REVDOC-G1 reconciliation
between `git ls-files` and the graph's `source_file` set
(docs/sprints/052-core-pipeline/IMPLEMENTATION_PLAN.md `D5`).

A reconciliation script proven only on a graph that already matches the
tree proves nothing -- every fixture below carries a deliberate mismatch.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import graph_reconcile as gr


def _repo_with_tracked(tmp_path: Path, files: dict[str, str]) -> Path:
    """Builds a throwaway git repository with `files` staged (precedent:
    tests/test_on_commit.py `_repo_with_staged`)."""
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    for name, body in files.items():
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding="utf-8")
        subprocess.run(["git", "add", "-f", name], cwd=tmp_path, check=True)
    return tmp_path


def _write_graph(path: Path, source_files: list[str]) -> None:
    graph = {
        "nodes": [
            {"id": f"n{i}", "source_file": source_file}
            for i, source_file in enumerate(source_files)
        ],
        "links": [],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(graph), encoding="utf-8")


# --- one tracked file missing from the graph --------------------------------

def test_a_tracked_file_missing_from_the_graph_is_reported_unmapped(tmp_path):
    _repo_with_tracked(tmp_path, {
        "scripts/mapped.py": "x = 1\n",
        "scripts/orphan.py": "y = 2\n",
    })
    graph_path = tmp_path / "graphify-out" / "graph.json"
    _write_graph(graph_path, ["scripts/mapped.py"])

    exit_code = gr.main(["--root", str(tmp_path), "--graph", str(graph_path)])

    assert exit_code == 0
    report_path = tmp_path / "graphify-out" / "unmapped_files.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["unmapped"] == ["scripts/orphan.py"]
    assert report["count"] == 1
    assert report["by_extension"] == {".py": 1}


def test_build_report_returns_the_same_unmapped_set_directly(tmp_path):
    _repo_with_tracked(tmp_path, {
        "a.md": "# a\n",
        "b.md": "# b\n",
    })
    graph_path = tmp_path / "graphify-out" / "graph.json"
    _write_graph(graph_path, ["a.md"])

    report = gr.build_report(tmp_path, graph_path)

    assert report["unmapped"] == ["b.md"]
    assert report["count"] == 1


# --- graph absent -----------------------------------------------------------

def test_absent_graph_exits_zero_and_is_advisory(tmp_path, capsys):
    _repo_with_tracked(tmp_path, {"scripts/orphan.py": "y = 2\n"})
    graph_path = tmp_path / "graphify-out" / "graph.json"  # never written

    exit_code = gr.main(["--root", str(tmp_path), "--graph", str(graph_path)])

    assert exit_code == 0
    captured = capsys.readouterr()
    assert "advisory" in captured.out
    assert not graph_path.exists()
    assert not (tmp_path / "graphify-out" / "unmapped_files.json").exists()


def test_absent_graph_at_default_location_is_also_advisory(tmp_path, capsys):
    _repo_with_tracked(tmp_path, {"scripts/orphan.py": "y = 2\n"})

    exit_code = gr.main(["--root", str(tmp_path)])

    assert exit_code == 0
    assert "advisory" in capsys.readouterr().out


# --- path normalisation ------------------------------------------------------

def test_an_absolute_source_file_inside_root_counts_as_mapped(tmp_path):
    _repo_with_tracked(tmp_path, {"scripts/mapped.py": "x = 1\n"})
    graph_path = tmp_path / "graphify-out" / "graph.json"
    absolute_source = str((tmp_path / "scripts" / "mapped.py").resolve())
    _write_graph(graph_path, [absolute_source])

    report = gr.build_report(tmp_path.resolve(), graph_path)

    assert report["unmapped"] == []
    assert report["count"] == 0


def test_normalize_source_file_handles_relative_and_absolute(tmp_path):
    root = tmp_path.resolve()
    assert gr.normalize_source_file("scripts/foo.py", root) == "scripts/foo.py"
    absolute = str(root / "scripts" / "foo.py")
    assert gr.normalize_source_file(absolute, root) == "scripts/foo.py"


# --- extension breakdown -----------------------------------------------------

def test_extension_breakdown_buckets_by_suffix_and_handles_none():
    counts = gr.extension_breakdown(["a.py", "b.py", "c.md", "Makefile"])
    assert counts == {"(none)": 1, ".md": 1, ".py": 2}
