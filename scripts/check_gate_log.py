"""Fail when a sprint's SPRINT_LOG.md gate rows violate verdict vocabulary.

Sprint ids below 31 are skipped (historical APPROVED/REJECTED without Class).
From 031, each Gate-1 and Gate-2 row emits APPROVED | REJECTED | RECORD.
REJECTED requires class charter or instructing. RECORD requires testifying.
RECORD rows do not count toward consecutive-rejection remediation.

Remediation notes (R-4, "the gate is never the first verifier"). Before work is
re-sent to a gate, the remediator runs each command of that gate and records
its exit code, read with `$?` and never through a pipe, in a Markdown table
whose header names the columns Gate, Round, Command and Exit:

    | Gate | Round | Command | Exit |
    | :--- | :--- | :--- | :--- |
    | QA Agent \\| Gate 1 | 1 | `make verify` | 0 |

Gate repeats the gate cell of the gate table. Round is the round that was
REJECTED and is being remediated. Command holds at least one backticked
command. Exit is a non-negative integer. A gate row with Round N >= 2 needs
one such row for the same Gate (case-insensitive) with Round N-1; a row with
no backticked command or a non-integer Exit is a finding, as is a Round cell
that is not an integer.

Scope of the remediation-notes check: it runs only when the sprint id parsed
from the directory name is >= 58 (`NOTES_FROM`). Earlier sprint logs carry
round >= 2 rows with no notes table and are not examined by it.

invoked_by: workflows/close_workflow.md Phase 2.6, workflows/pipeline_workflow.md
Phase 7, Makefile `verify`.

Usage:
    python3 scripts/check_gate_log.py --sprint-dir docs/sprints/031-core-pipeline
    python3 scripts/check_gate_log.py --current-sprint

Output: after the verdict line, `escape rows: <N>` (advisory; never changes
the exit code).

Exit codes:
    0 — pass, skip (historical / no file / no rows)
    2 — vocabulary or class mismatch (RA-17; exit-code-2 blocking per RA-11 semantics)
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _md_table import split_cells
from _root import agents_root
from check_task_scope import current_sprint_dir, sprint_id_from_dir

SKIP_BEFORE = 31
NOTES_FROM = 58
VERDICTS = frozenset({"APPROVED", "REJECTED", "RECORD"})
REJECTED_CLASSES = frozenset({"charter", "instructing"})
RECORD_CLASS = "testifying"
_HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
_ESCAPE = re.compile(r"\bescape\b")


def _strip_html_comments(text: str) -> str:
    """Remove every ``<!-- ... -->`` region so no commented line is parsed.

    Well-formed comments are deleted whether they sit on a single line or
    span several lines. A comment that opens with ``<!--`` and is never
    closed swallows the rest of the file, mirroring how HTML and Markdown
    renderers treat an unterminated comment.

    Args:
        text: The full SPRINT_LOG.md content.

    Returns:
        The content with every comment region removed.
    """
    without_closed = _HTML_COMMENT.sub("", text)
    unclosed = without_closed.find("<!--")
    if unclosed != -1:
        return without_closed[:unclosed]
    return without_closed


def _cells(line: str) -> list[str]:
    return [cell.strip("`") for cell in split_cells(line)]


def _is_separator(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and set(stripped) <= set("|:- ")


def _plain(cell: str) -> str:
    return cell.replace("*", "").replace("`", "").strip()


def _parse_gate_table(lines: list[str], index: int) -> tuple[list[list[str]], int]:
    """Parse the row block that follows one Verdict-bearing header line.

    Args:
        lines: All (comment-stripped) lines of the SPRINT_LOG.md content.
        index: Index of the line right after the header line.

    Returns:
        tuple[list[list[str]], int]: (rows, next_index) — the table's data
        rows and the index to resume scanning from.
    """
    if index < len(lines) and _is_separator(lines[index]):
        index += 1
    rows: list[list[str]] = []
    while index < len(lines) and lines[index].strip().startswith("|"):
        if not _is_separator(lines[index]):
            rows.append(_cells(lines[index]))
        index += 1
    return rows, index


def gate_tables(text: str) -> list[tuple[list[str], list[list[str]]]]:
    """Tables whose header includes Verdict."""
    tables: list[tuple[list[str], list[list[str]]]] = []
    lines = _strip_html_comments(text).splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if not (line.strip().startswith("|") and not _is_separator(line)):
            index += 1
            continue
        header = _cells(line)
        if "Verdict" not in header:
            index += 1
            continue
        rows, index = _parse_gate_table(lines, index + 1)
        tables.append((header, rows))
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


def _table_findings(header: list[str], rows: list[list[str]]) -> list[str]:
    """Vocabulary findings for every row of one gate table, in row order.

    Args:
        header: Column header names for the table.
        rows: The table's data rows.

    Returns:
        list[str]: Non-empty finding messages.
    """
    return [item for row in rows if (item := _row_finding(header, row))]


def collect_findings(text: str, sprint_id: int | None) -> list[str]:
    """Vocabulary mismatches. Empty means pass or skip."""
    if sprint_id is not None and sprint_id < SKIP_BEFORE:
        return []
    findings: list[str] = []
    for header, rows in gate_tables(text):
        findings.extend(_table_findings(header, rows))
    if sprint_id is not None and sprint_id >= NOTES_FROM:
        findings.extend(remediation_findings(text))
    return findings


def _note_tables(text: str) -> tuple[set[tuple[str, int]], list[str]]:
    """Collect the (gate, round) pairs recorded by Remediation notes tables.

    A table qualifies when its header names Gate, Round, Command and Exit.

    Args:
        text: The full SPRINT_LOG.md content.

    Returns:
        tuple: (recorded pairs, findings for malformed note rows).
    """
    recorded: set[tuple[str, int]] = set()
    findings: list[str] = []
    header: list[str] = []
    for line in _strip_html_comments(text).splitlines():
        if not line.strip().startswith("|"):
            header = []
            continue
        if _is_separator(line):
            continue
        cells = [_plain_keep(cell) for cell in split_cells(line)]
        if {"Gate", "Round", "Command", "Exit"} <= {_plain(c) for c in cells}:
            header = [_plain(c) for c in cells]
            continue
        if header:
            _note_row(header, cells, recorded, findings)
    return recorded, findings


def _plain_keep(cell: str) -> str:
    return cell.replace("*", "").strip()


def _note_row(
    header: list[str],
    cells: list[str],
    recorded: set[tuple[str, int]],
    findings: list[str],
) -> None:
    """Validate one note row and add its pair to ``recorded`` when well formed."""
    row = dict(zip(header, cells, strict=False))
    gate = _plain(row.get("Gate", "")).casefold()
    round_text = _plain(row.get("Round", ""))
    command = row.get("Command", "")
    exit_text = _plain(row.get("Exit", ""))
    if not round_text.isdigit() or not re.search(r"`[^`]+`", command) or not exit_text.isdigit():
        findings.append(f"malformed Remediation notes row for gate {gate!r}: {cells}")
        return
    recorded.add((gate, int(round_text)))


def _round_finding(
    header: list[str], row: list[str], recorded: set[tuple[str, int]]
) -> str | None:
    """Finding for one gate row, or None when the row needs no note or has one."""
    if not _plain(_col(header, row, "Verdict")):
        return None
    gate = _plain(_col(header, row, "Gate"))
    round_text = _plain(_col(header, row, "Round"))
    if not round_text.isdigit():
        return f"gate {gate!r}: Round {round_text!r} is not an integer"
    previous = int(round_text) - 1
    if previous >= 1 and (gate.casefold(), previous) not in recorded:
        return (
            f"gate {gate!r} round {round_text}: no Remediation notes row for "
            f"round {previous} with a backticked command and an Exit code"
        )
    return None


def remediation_findings(text: str) -> list[str]:
    """Findings for gate rows of Round >= 2 lacking a note for the prior round.

    Args:
        text: The full SPRINT_LOG.md content.

    Returns:
        list[str]: Non-empty finding messages; empty means the rule holds.
    """
    recorded, findings = _note_tables(text)
    for header, rows in gate_tables(text):
        items = (_round_finding(header, row, recorded) for row in rows)
        findings.extend(item for item in items if item)
    return findings


def count_escape_rows(text: str) -> int:
    """Count gate rows whose Notes cell holds the whole word ``escape``.

    Advisory only (rules/qa_and_testing.md §4, convergence rule 2): the count
    never feeds an exit code. Only the Notes cell is matched, so ``escaped``
    or ``escape`` in another column is not counted. A table with no Notes
    column contributes 0.

    Args:
        text: The full SPRINT_LOG.md content.

    Returns:
        int: Number of gate rows marked ``escape``.
    """
    return sum(
        1
        for header, rows in gate_tables(text)
        for row in rows
        if _ESCAPE.search(_col(header, row, "Notes"))
    )


def check(sprint_dir: Path) -> int:
    """Audit one sprint directory. Returns the process exit code."""
    path = sprint_dir / "SPRINT_LOG.md"
    if not path.is_file():
        print(f"[OK] check_gate_log: no SPRINT_LOG.md under {sprint_dir} (skip)")
        return 0
    sprint_id = sprint_id_from_dir(sprint_dir)
    text = path.read_text(encoding="utf-8")
    findings = collect_findings(text, sprint_id)
    if not findings:
        print(f"[OK] check_gate_log: {path}")
        print(f"escape rows: {count_escape_rows(text)}")
        return 0
    print(f"❌ check_gate_log: {path}", file=sys.stderr)
    for item in findings:
        print(f"   • {item}", file=sys.stderr)
    print(f"escape rows: {count_escape_rows(text)}")
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
