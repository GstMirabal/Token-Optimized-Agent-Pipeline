"""Fail when a sprint's SPRINT_LOG.md does not record the plan's closure rows.

Reads ``<sprint-dir>/IMPLEMENTATION_PLAN.md`` and ``<sprint-dir>/SPRINT_LOG.md``.
Two tables of the log are read, each identified by its header cells (the same
approach ``scripts/check_gate_log.py`` uses for ``Remediation notes``):

Abort criteria (R-9). Header Criterion, Command, Exit, Observation:

    | Criterion | Command | Exit | Observation |
    | :--- | :--- | :--- | :--- |
    | 1 | `rg -c "x" scripts/` | 1 | measured at the phase 4 boundary |

Criterion is the integer of a numbered item of the plan's ``## Abort criterion``
section. Command holds at least one backticked command. Exit is a non-negative
integer. Each numbered item needs at least one such row. A criterion is closed
by the observation it names; the instrument checks that a command and an exit
code are present and does not judge them.

Plan results (R-10). Header Section, Row, Check, Result:

    | Section | Row | Check | Result |
    | :--- | :--- | :--- | :--- |
    | Tests | 1 | `test -f scripts/x.py` | exit 0 |

Section is ``Tests`` or ``Verification``. Row is the 1-based index of a data
row in that table of the plan (the table under ``## Tests`` or
``## Verification``). The log table holds one row per plan row: same row count
as the two plan tables together, each (Section, Row) pair once, and a non-empty
Result cell.

Findings: a missing file, section or table, a malformed row, a numbered
criterion with no valid row, a count mismatch, a duplicated or unknown
(Section, Row) pair, or an empty Result. The script reads only the tables and
the section named above.

invoked_by: workflows/close_workflow.md Phase 2.6 (wired by B-10).

Usage:
    python3 scripts/check_plan_closure.py --sprint-dir docs/sprints/058-core-pipeline

Exit codes:
    0 - no finding
    2 - at least one finding, or an unreadable input (fail closed on error)
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _md_table import split_cells
from check_gate_log import _strip_html_comments

_BACKTICKED = re.compile(r"`[^`]+`")
_NUMBERED = re.compile(r"^(\d+)\.\s")
ABORT_HEADER = ("Criterion", "Command", "Exit", "Observation")
RESULTS_HEADER = ("Section", "Row", "Check", "Result")
SECTIONS = ("Tests", "Verification")


class ClosureError(Exception):
    """Raised when an input cannot be read or lacks a required part."""


def _plain(cell: str) -> str:
    """Strip Markdown emphasis and code marks from a table cell.

    Args:
        cell: One cell of a Markdown table row.

    Returns:
        str: The cell without ``*`` and backtick characters, trimmed.
    """
    return cell.replace("*", "").replace("`", "").strip()


def _is_separator(line: str) -> bool:
    """Tell whether a line is the ``|---|---|`` separator of a Markdown table.

    Args:
        line: One line of text.

    Returns:
        bool: True when the line starts with ``|`` and holds only ``|``, ``:``,
        ``-`` and spaces.
    """
    stripped = line.strip()
    return stripped.startswith("|") and set(stripped) <= set("|:- ")


def _section_lines(text: str, title: str) -> list[str]:
    """Return the lines under the ``## <title>`` heading, up to the next ``## ``.

    Args:
        text: Comment-stripped Markdown.
        title: Heading text after ``## `` (prefix match).

    Returns:
        list[str]: The section body lines.

    Raises:
        ClosureError: When the heading is absent.
    """
    lines = text.splitlines()
    start = next(
        (i for i, ln in enumerate(lines) if ln.startswith("## ") and ln[3:].strip().startswith(title)),
        None,
    )
    if start is None:
        raise ClosureError(f"missing section '## {title}'")
    body: list[str] = []
    for line in lines[start + 1 :]:
        if line.startswith("## "):
            break
        body.append(line)
    return body


def _pipe_blocks(lines: list[str]) -> list[list[str]]:
    """Group consecutive pipe-led lines, dropping separator lines.

    Args:
        lines: Lines of one section.

    Returns:
        list[list[str]]: One non-empty list of table lines per table; a line
        that does not start with ``|`` ends the current table.
    """
    blocks: list[list[str]] = [[]]
    for line in lines:
        if not line.strip().startswith("|"):
            blocks.append([])
            continue
        if not _is_separator(line):
            blocks[-1].append(line)
    return [block for block in blocks if block]


def _table_rows(lines: list[str]) -> list[list[str]] | None:
    """Return the data rows of the first table in ``lines``.

    Args:
        lines: Lines of one section.

    Returns:
        list[list[str]] | None: The cells of every row after the header row, or
        None when ``lines`` holds no table.
    """
    blocks = _pipe_blocks(lines)
    if not blocks:
        return None
    return [split_cells(line) for line in blocks[0][1:]]


def plan_row_counts(plan_text: str) -> dict[str, int]:
    """Count the data rows of the plan's Tests and Verification tables.

    Args:
        plan_text: Comment-stripped plan content.

    Returns:
        dict[str, int]: Row count per section name.

    Raises:
        ClosureError: When a section or its table is missing.
    """
    counts: dict[str, int] = {}
    for name in SECTIONS:
        rows = _table_rows(_section_lines(plan_text, name))
        if rows is None:
            raise ClosureError(f"no table under '## {name}' in the plan")
        counts[name] = len(rows)
    return counts


def plan_criteria(plan_text: str) -> list[int]:
    """Return the numbers of the numbered items under ``## Abort criterion``.

    Args:
        plan_text: Comment-stripped plan content.

    Returns:
        list[int]: Criterion numbers in plan order.

    Raises:
        ClosureError: When the section is missing or holds no numbered item.
    """
    found = [int(m.group(1)) for ln in _section_lines(plan_text, "Abort criterion") if (m := _NUMBERED.match(ln))]
    if not found:
        raise ClosureError("no numbered item under '## Abort criterion' in the plan")
    return found


def log_table(text: str, header: tuple[str, ...]) -> list[dict[str, str]]:
    """Return the rows of the log table whose header cells include ``header``.

    Args:
        text: Comment-stripped SPRINT_LOG.md content.
        header: Required column names.

    Returns:
        list[dict[str, str]]: One dict per data row, keyed by column name.

    Raises:
        ClosureError: When no table carries that header.
    """
    for block in _pipe_blocks(text.splitlines()):
        names = [_plain(c) for c in split_cells(block[0])]
        if set(header) <= set(names):
            return [dict(zip(names, split_cells(ln), strict=False)) for ln in block[1:]]
    raise ClosureError(f"no table with header {' | '.join(header)} in SPRINT_LOG.md")


def abort_findings(criteria: list[int], rows: list[dict[str, str]]) -> list[str]:
    """Check the Abort criteria table against the plan's numbered items.

    Args:
        criteria: Numbers of the plan's Abort criteria.
        rows: Rows of the log's Abort criteria table, keyed by header name.

    Returns:
        list[str]: One finding per malformed row and per criterion with no
        closing row; empty when the table is complete.
    """
    findings: list[str] = []
    closed: set[int] = set()
    for row in rows:
        number, command, code = _plain(row.get("Criterion", "")), row.get("Command", ""), _plain(row.get("Exit", ""))
        if not number.isdigit() or not _BACKTICKED.search(command) or not code.isdigit():
            findings.append(f"Abort criteria: malformed row (need integer Criterion, backticked Command, integer Exit): {row}")
            continue
        closed.add(int(number))
    findings.extend(f"Abort criteria: criterion {n} has no row with a command and an exit code" for n in criteria if n not in closed)
    return findings


def _result_key(row: dict[str, str]) -> tuple[str, int] | None:
    """Read the (Section, Row) key of a Plan results row.

    Args:
        row: One row of the Plan results table, keyed by header name.

    Returns:
        tuple[str, int] | None: The section name and row number, or None when
        the section is not in ``SECTIONS`` or the row is not an integer.
    """
    section, index = _plain(row.get("Section", "")), _plain(row.get("Row", ""))
    if section not in SECTIONS or not index.isdigit():
        return None
    return section, int(index)


def _row_finding(row: dict[str, str], counts: dict[str, int], seen: set[tuple[str, int]]) -> str | None:
    """Check one Plan results row and record it when valid.

    Args:
        row: One row of the Plan results table, keyed by header name.
        counts: Data-row count of each plan section.
        seen: Keys of the rows accepted so far; a valid row is added to it.

    Returns:
        str | None: The finding for this row, or None when the row is valid.
    """
    key = _result_key(row)
    if key is None or key[1] < 1 or key[1] > counts[key[0]]:
        return f"Plan results: Section/Row names no plan row: {row}"
    if key in seen:
        return f"Plan results: {key[0]} row {key[1]} appears twice"
    if not _plain(row.get("Result", "")):
        return f"Plan results: {key[0]} row {key[1]} has an empty Result"
    seen.add(key)
    return None


def result_findings(counts: dict[str, int], rows: list[dict[str, str]]) -> list[str]:
    """Check the Plan results table against the plan's row counts.

    Args:
        counts: Data-row count of each plan section.
        rows: Rows of the log's Plan results table, keyed by header name.

    Returns:
        list[str]: One finding per invalid row, per count mismatch and per plan
        row with no result; empty when the table is complete.
    """
    seen: set[tuple[str, int]] = set()
    findings = [item for row in rows if (item := _row_finding(row, counts, seen))]
    expected = sum(counts.values())
    if len(rows) != expected:
        findings.append(f"Plan results: {len(rows)} rows, the plan has {expected} (Tests {counts['Tests']} + Verification {counts['Verification']})")
    for name in SECTIONS:
        findings.extend(f"Plan results: no row for {name} row {i}" for i in range(1, counts[name] + 1) if (name, i) not in seen)
    return findings


def _read(path: Path) -> str:
    """Read a UTF-8 file with its HTML comments removed.

    Args:
        path: File to read.

    Returns:
        str: The text of the file without HTML comments.

    Raises:
        ClosureError: When the file cannot be read.
    """
    try:
        return _strip_html_comments(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise ClosureError(f"cannot read {path}: {error}") from error


def check(sprint_dir: Path) -> int:
    """Audit one sprint directory.

    Args:
        sprint_dir: Directory holding IMPLEMENTATION_PLAN.md and SPRINT_LOG.md.

    Returns:
        int: ``0`` without findings, ``2`` otherwise.
    """
    try:
        plan = _read(sprint_dir / "IMPLEMENTATION_PLAN.md")
        log = _read(sprint_dir / "SPRINT_LOG.md")
        criteria = plan_criteria(plan)
        counts = plan_row_counts(plan)
        findings = abort_findings(criteria, log_table(log, ABORT_HEADER))
        findings += result_findings(counts, log_table(log, RESULTS_HEADER))
    except ClosureError as error:
        print(f"check_plan_closure: {error}", file=sys.stderr)
        return 2
    if not findings:
        print(f"[OK] check_plan_closure: {sprint_dir}")
        return 0
    print(f"check_plan_closure: {sprint_dir}", file=sys.stderr)
    for item in findings:
        print(f"   - {item}", file=sys.stderr)
    return 2


def main() -> int:
    """Parse arguments and run the check.

    Returns:
        int: The exit code of ``check`` for the ``--sprint-dir`` argument.
    """
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--sprint-dir", type=Path, required=True)
    return check(parser.parse_args().sprint_dir)


if __name__ == "__main__":
    sys.exit(main())
