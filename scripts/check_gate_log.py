"""Fail when a sprint's SPRINT_LOG.md gate rows violate verdict vocabulary.

Sprint ids below 31 are skipped (historical APPROVED/REJECTED without Class).
From 031, each Gate-1 and Gate-2 row emits APPROVED | REJECTED | RECORD.
REJECTED requires class charter or instructing. RECORD requires testifying.
RECORD rows do not count toward consecutive-rejection remediation.

invoked_by: workflows/close_workflow.md Phase 2.6, workflows/pipeline_workflow.md
Phase 7, Makefile `verify`.

Usage:
    python3 scripts/check_gate_log.py --sprint-dir docs/sprints/031-core-pipeline
    python3 scripts/check_gate_log.py --current-sprint

Exit codes:
    0 — pass, skip (historical / no file / no rows)
    2 — vocabulary or class mismatch (RA-11)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _root import agents_root  # noqa: E402
from check_task_scope import current_sprint_dir, sprint_id_from_dir  # noqa: E402

SKIP_BEFORE = 31
VERDICTS = frozenset({"APPROVED", "REJECTED", "RECORD"})
REJECTED_CLASSES = frozenset({"charter", "instructing"})
RECORD_CLASS = "testifying"


def _cells(line: str) -> list[str]:
    raw = [part.strip().strip("`") for part in line.strip().strip("|").split("|")]
    return raw


def _is_separator(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and set(stripped) <= set("|:- ")


def _plain(cell: str) -> str:
    return cell.replace("*", "").replace("`", "").strip()


def gate_tables(text: str) -> list[tuple[list[str], list[list[str]]]]:
    """Tables whose header includes Verdict."""
    tables: list[tuple[list[str], list[list[str]]]] = []
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.strip().startswith("|") and not _is_separator(line):
            header = _cells(line)
            if "Verdict" in header:
                index += 1
                if index < len(lines) and _is_separator(lines[index]):
                    index += 1
                rows: list[list[str]] = []
                while index < len(lines) and lines[index].strip().startswith("|"):
                    if not _is_separator(lines[index]):
                        rows.append(_cells(lines[index]))
                    index += 1
                tables.append((header, rows))
                continue
        index += 1
    return tables


def _col(header: list[str], row: list[str], name: str) -> str:
    try:
        position = header.index(name)
    except ValueError:
        return ""
    return row[position] if position < len(row) else ""


def _row_finding(header: list[str], row: list[str]) -> str | None:
    verdict = _plain(_col(header, row, "Verdict")).upper()
    klass = _plain(_col(header, row, "Class")).lower()
    if not verdict:
        return None
    if verdict not in VERDICTS:
        return f"unknown verdict {verdict!r} (emit APPROVED | REJECTED | RECORD)"
    if verdict == "REJECTED" and klass not in REJECTED_CLASSES:
        return f"REJECTED requires class charter or instructing, got {klass!r}"
    if verdict == "RECORD" and klass != RECORD_CLASS:
        return f"RECORD requires class testifying, got {klass!r}"
    if verdict == "APPROVED" and klass:
        return f"APPROVED must have empty Class, got {klass!r}"
    return None


def collect_findings(text: str, sprint_id: int | None) -> list[str]:
    """Vocabulary mismatches. Empty means pass or skip."""
    if sprint_id is not None and sprint_id < SKIP_BEFORE:
        return []
    findings: list[str] = []
    for header, rows in gate_tables(text):
        for row in rows:
            item = _row_finding(header, row)
            if item:
                findings.append(item)
    return findings


def check(sprint_dir: Path) -> int:
    """Audit one sprint directory. Returns the process exit code."""
    path = sprint_dir / "SPRINT_LOG.md"
    if not path.is_file():
        print(f"[OK] check_gate_log: no SPRINT_LOG.md under {sprint_dir} (skip)")
        return 0
    sprint_id = sprint_id_from_dir(sprint_dir)
    findings = collect_findings(path.read_text(encoding="utf-8"), sprint_id)
    if not findings:
        print(f"[OK] check_gate_log: {path}")
        return 0
    print(f"❌ check_gate_log: {path}", file=sys.stderr)
    for item in findings:
        print(f"   • {item}", file=sys.stderr)
    return 2


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--sprint-dir", type=Path, help="Canonical sprint directory")
    parser.add_argument("--current-sprint", action="store_true")
    args = parser.parse_args()
    root = agents_root() if (Path.cwd() / "scripts" / "check_gate_log.py").is_file() else Path.cwd()
    if args.current_sprint:
        target = current_sprint_dir(root)
        if target is None:
            print("[OK] check_gate_log: no current sprint directory (skip)")
            return 0
        return check(target)
    if args.sprint_dir is None:
        parser.error("--sprint-dir or --current-sprint is required")
    return check(args.sprint_dir)


if __name__ == "__main__":
    sys.exit(main())
