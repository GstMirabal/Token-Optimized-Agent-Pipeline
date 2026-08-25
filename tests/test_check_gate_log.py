"""Tests for scripts/check_gate_log.py.

A gate proven only on a healthy tree proves nothing — fixtures must fail.
Sprint ids below 31 are skipped (historical APPROVED/REJECTED without Class).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CHECK = REPO / "scripts" / "check_gate_log.py"
QA_RULE = REPO / "rules" / "qa_and_testing.md"

GATE_HEADER = "Gate | Round | Verdict | Class | Notes"


def _run(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECK), *args],
        cwd=cwd or REPO,
        capture_output=True,
        text=True,
        check=False,
    )


def _log(tmp_path: Path, sprint_name: str, body: str) -> Path:
    sprint = tmp_path / "docs" / "sprints" / sprint_name
    sprint.mkdir(parents=True)
    (sprint / "SPRINT_LOG.md").write_text(body, encoding="utf-8")
    return sprint


def _phase7(*rows: str) -> str:
    lines = [
        "# Sprint Log",
        "",
        "## Phase 7 — Quality Gate",
        "",
        f"| {GATE_HEADER} |",
        "| :--- | :--- | :--- | :--- | :--- |",
        *rows,
        "",
    ]
    return "\n".join(lines)


def _section_four(text: str) -> str:
    start = text.find("## 4.")
    if start < 0:
        return ""
    end = text.find("\n## ", start + 1)
    return text[start:] if end < 0 else text[start:end]


def test_historical_030_is_skipped() -> None:
    """Pre-031 logs have no Class column; skip must be exit 0."""
    result = _run("--sprint-dir", "docs/sprints/030-core-pipeline")
    assert result.returncode == 0, result.stderr


def test_rejected_without_class_fails(tmp_path: Path) -> None:
    sprint = _log(
        tmp_path,
        "031-core-pipeline",
        _phase7("| QA (structural) | 1 | **REJECTED** | | missing class |"),
    )
    result = _run("--sprint-dir", str(sprint))
    assert result.returncode == 2
    combined = result.stderr.lower() + result.stdout.lower()
    assert "class" in combined or "rejected" in combined


def test_record_with_testifying_passes(tmp_path: Path) -> None:
    sprint = _log(
        tmp_path,
        "031-core-pipeline",
        _phase7("| QA (structural) | 1 | **RECORD** | testifying | stale comment |"),
    )
    result = _run("--sprint-dir", str(sprint))
    assert result.returncode == 0, result.stderr


def test_three_record_rows_are_not_a_remediation_streak(tmp_path: Path) -> None:
    sprint = _log(
        tmp_path,
        "031-core-pipeline",
        _phase7(
            "| QA (structural) | 1 | **RECORD** | testifying | a |",
            "| QA (structural) | 2 | **RECORD** | testifying | b |",
            "| Tester (functional) | 1 | **RECORD** | testifying | c |",
        ),
    )
    result = _run("--sprint-dir", str(sprint))
    assert result.returncode == 0, result.stderr


def test_qa_and_testing_section_4_names_record() -> None:
    """Live instructing rule must name RECORD in §4 (fails until R1)."""
    section = _section_four(QA_RULE.read_text(encoding="utf-8"))
    assert "RECORD" in section
    assert "testifying" in section.lower() or "instruct" in section.lower()
