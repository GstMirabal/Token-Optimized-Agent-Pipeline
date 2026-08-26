"""Tests for scripts/session_start.py briefing caps (Sprint 035 C4)."""

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
def session_start(monkeypatch: pytest.MonkeyPatch):
    """Import session_start with scripts/ on sys.path."""
    monkeypatch.syspath_prepend(str(SCRIPTS))
    sys.modules.pop("session_start", None)
    return importlib.import_module("session_start")


def _write_minimal_root(root: Path, *, upstream_body: str | None = None) -> Path:
    """Scaffold a fake repo root with anchor + optional UPSTREAM file."""
    docs = root / "docs"
    docs.mkdir(parents=True)
    (docs / "active_state.json").write_text(
        json.dumps(
            {
                "status": "IN_PROGRESS",
                "session_id": "test-sess-035",
                "current_sprint": {"id": 35, "layer": "core", "app": "pipeline"},
                "session_tool": "cursor",
                "delegation_mode": "sequential",
            }
        ),
        encoding="utf-8",
    )
    (root / "scripts").mkdir(exist_ok=True)
    (root / "config").mkdir(exist_ok=True)
    (root / "config" / "model_tiers.json").write_text(
        json.dumps({"tiers": {"author": {"cursor": {"model": "test-model"}}}}),
        encoding="utf-8",
    )
    if upstream_body is not None:
        audits = docs / "audits"
        audits.mkdir(parents=True)
        (audits / "UPSTREAM_FINDINGS_FROM_HOSTS.md").write_text(
            upstream_body, encoding="utf-8"
        )
    return root


def test_main_exits_zero_and_respects_line_cap(
    session_start, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys
) -> None:
    root = _write_minimal_root(tmp_path / "repo")
    monkeypatch.setattr(session_start, "repo_root", lambda: root)
    assert session_start.main() == 0
    out = capsys.readouterr().out
    lines = out.splitlines()
    assert len(lines) <= session_start.LINE_CAP
    assert lines[0] == "# /start briefing"
    assert "test-sess-035" in out


def test_upstream_section_reports_size_not_full_dump(
    session_start, tmp_path: Path
) -> None:
    marker = "UNIQUE_UPSTREAM_PAYLOAD_SHOULD_NOT_APPEAR"
    huge = "\n".join(
        [f"# dump line {i} {marker}" for i in range(500)]
        + [
            "**Status at Sprint 033 (test).**",
            "",
            "| | |",
            "| :--- | :--- |",
            "| **Still open** | F-999 |",
        ]
    )
    root = _write_minimal_root(tmp_path / "repo", upstream_body=huge)
    briefing = session_start.apply_line_cap(session_start.build_briefing(root))
    text = "\n".join(briefing)
    assert len(briefing) <= session_start.LINE_CAP
    assert "file lines:" in text
    assert "do not load full UPSTREAM" in text
    assert "rows (non-empty):" in text
    assert marker not in text
    assert text.count("| **Still open** |") <= 1


def test_upstream_still_open_uses_highest_sprint_status_only(
    session_start, tmp_path: Path
) -> None:
    """Sprint 038 M1: historical Status snapshots must not inflate the count.

    Fixture: Sprint 027 Still open non-empty + Sprint 033 *(none…)* → expect 0.
    Fails against the pre-M1 counter that summed every Still-open row.
    """
    body = "\n".join(
        [
            "**Status at Sprint 027 (2026-08-25).**",
            "",
            "| | |",
            "| :--- | :--- |",
            "| **Still open** | **`F-021-A2`**, **`F-026-A2`** |",
            "",
            "**Status at Sprint 033 (2026-08-25, `ai-sprint/033`).**",
            "",
            "| | |",
            "| :--- | :--- |",
            "| **Still open** | *(none in this file's open set)* |",
        ]
    )
    root = _write_minimal_root(tmp_path / "repo", upstream_body=body)
    section = "\n".join(session_start.section_upstream(root))
    assert "rows (non-empty): 0" in section


def test_upstream_still_open_counts_latest_nonempty_status(
    session_start, tmp_path: Path
) -> None:
    """When the highest Status sprint still lists opens, count that row only."""
    body = "\n".join(
        [
            "**Status at Sprint 027 (2026-08-25).**",
            "",
            "| | |",
            "| :--- | :--- |",
            "| **Still open** | **`F-021-A2`**, **`F-026-A2`** |",
            "",
            "**Status at Sprint 030 (2026-08-25).**",
            "",
            "| | |",
            "| :--- | :--- |",
            "| **Still open** | **`F-021-A2`** |",
        ]
    )
    root = _write_minimal_root(tmp_path / "repo", upstream_body=body)
    section = "\n".join(session_start.section_upstream(root))
    assert "rows (non-empty): 1" in section


def test_cli_against_real_repo_stays_under_line_cap() -> None:
    """Integration: real checkout still exits 0 and never dumps UPSTREAM path body."""
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / "session_start.py")],
        cwd=str(REPO),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    lines = proc.stdout.splitlines()
    assert len(lines) <= 80
    assert "UPSTREAM_FINDINGS_FROM_HOSTS.md" in proc.stdout or "file lines:" in proc.stdout
    # Full dump would be hundreds of lines; cap already enforces this.
    assert "Framework-class findings under" not in proc.stdout
