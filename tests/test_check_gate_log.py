"""Tests for scripts/check_gate_log.py.

A gate proven only on a healthy tree proves nothing — fixtures must fail.
Sprint ids below 31 are skipped (historical APPROVED/REJECTED without Class).

The `_strip_html_comments` / commented-row cases exercise U13's fix for
`KI-046-3`: `gate_tables()` used to scan raw lines, so a commented example
row placed below a real Verdict header was parsed as data.
"""

from __future__ import annotations

import importlib
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
CHECK = REPO / "scripts" / "check_gate_log.py"
SCRIPTS = REPO / "scripts"
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


# --- U20 (KI-046-3): HTML-comment stripping in gate_tables() -------------------


@pytest.fixture
def check_mod():
    """Import scripts/check_gate_log.py as ``check_gate_log`` (sibling style)."""
    sys.path.insert(0, str(SCRIPTS))
    sys.modules.pop("check_gate_log", None)
    try:
        yield importlib.import_module("check_gate_log")
    finally:
        sys.modules.pop("check_gate_log", None)
        if str(SCRIPTS) in sys.path:
            sys.path.remove(str(SCRIPTS))


def _gate_table(*rows: str) -> str:
    """A minimal SPRINT_LOG-shaped Quality Gate section."""
    lines = [
        "## Quality Gate",
        "",
        f"| {GATE_HEADER} |",
        "| :--- | :--- | :--- | :--- | :--- |",
        *rows,
        "",
    ]
    return "\n".join(lines)


def test_strip_removes_single_line_comment(check_mod) -> None:
    assert check_mod._strip_html_comments("keep <!-- drop --> tail") == "keep  tail"


def test_strip_removes_multiline_region(check_mod) -> None:
    text = "before\n<!--\n| fake | row |\n-->\nafter"
    assert check_mod._strip_html_comments(text) == "before\n\nafter"


def test_strip_unclosed_comment_truncates_to_eof(check_mod) -> None:
    text = "keep me\n<!-- dangling\n| QA | 1 | BOGUS | charter | x |\n"
    assert check_mod._strip_html_comments(text) == "keep me\n"


def test_strip_returns_text_without_comment_unchanged(check_mod) -> None:
    text = "line one\nline two\n"
    assert check_mod._strip_html_comments(text) == text


def _parsed_rows(check_mod, body: str) -> list[list[str]]:
    return [row for _, rows in check_mod.gate_tables(body) for row in rows]


def test_commented_bogus_row_is_not_parsed_or_flagged(check_mod) -> None:
    """A bogus verdict sealed inside <!-- ... --> yields no finding.

    The real row still parses. First half fails against HEAD, which scans
    raw lines and flags the commented ``BOGUS`` row.
    """
    body = _gate_table(
        "| QA Agent (Gate 1) | 1 | APPROVED |  | real row | <!--",
        "| QA Agent (Gate 1) | 1 | BOGUS | charter | example |",
        "-->",
    )
    rows = _parsed_rows(check_mod, body)
    assert any(row[:3] == ["QA Agent (Gate 1)", "1", "APPROVED"] for row in rows)
    assert not any("BOGUS" in cell for row in rows for cell in row)
    assert check_mod.collect_findings(body, 47) == []


def test_uncommented_bogus_row_is_flagged(check_mod) -> None:
    """Move the same bogus row out of the comment: a finding is raised."""
    body = _gate_table(
        "| QA Agent (Gate 1) | 1 | APPROVED |  | real row |",
        "| QA Agent (Gate 1) | 1 | BOGUS | charter | example |",
    )
    findings = check_mod.collect_findings(body, 47)
    assert any("BOGUS" in item for item in findings)


def test_valid_table_produces_zero_findings(check_mod) -> None:
    """Regression: every allowed verdict/class combination stays clean."""
    body = _gate_table(
        "| QA Agent (Gate 1) | 1 | APPROVED |  | ruff clean |",
        "| QA Agent (Gate 1) | 2 | REJECTED | charter | bounced |",
        "| Tester Agent (Gate 2) | 1 | REJECTED | instructing | logic gap |",
        "| Tester Agent (Gate 2) | 2 | RECORD | testifying | recorded |",
    )
    assert check_mod.collect_findings(body, 47) == []


def test_sprint_dir_with_commented_stub_exits_zero(tmp_path: Path) -> None:
    """A SPRINT_LOG stub whose example rows sit in a comment passes --sprint-dir."""
    sprint = tmp_path / "047-core-pipeline"
    sprint.mkdir()
    body = "\n".join(
        [
            "# Sprint Log",
            "",
            "## Quality Gate",
            "",
            "<!--",
            "Verdict vocabulary (rules/qa_and_testing.md §4, RA-17):",
            "  | QA Agent (Gate 1)     | 1 | BOGUS  | charter | example only |",
            "  | Tester Agent (Gate 2) | 1 | RECORD | testifying | example only |",
            "-->",
            "",
            f"| {GATE_HEADER} |",
            "| :--- | :--- | :--- | :--- | :--- |",
            "",
        ]
    )
    (sprint / "SPRINT_LOG.md").write_text(body, encoding="utf-8")
    result = _run("--sprint-dir", str(sprint))
    assert result.returncode == 0, result.stderr
