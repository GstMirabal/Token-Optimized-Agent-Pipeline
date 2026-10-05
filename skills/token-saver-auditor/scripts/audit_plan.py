"""Audit an Implementation Plan against structural token-economy filters.

Filter 5 (recurring mechanism vs script) is owned by
``scripts/scan_workflow_determinism.py`` and is not reimplemented here.
This script covers the plan artifact: Filters 1-4, 6, Mechanisms/Invoker,
and the Cost section required from Sprint 030.

invoked_by: workflows/pipeline_workflow.md Phases 1 and 5, Makefile `verify`.

Usage:
    python3 skills/token-saver-auditor/scripts/audit_plan.py <plan.md>
    python3 skills/token-saver-auditor/scripts/audit_plan.py --current-sprint

Exit codes:
    0 — pass, or --current-sprint skipped (no plan, or sprint id < 30)
    2 — structural waste found (RA-11)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

COST_FROM_SPRINT = 30
EMPTY = {"", "—", "-"}


def sprint_id_from_path(path: Path) -> int | None:
    """Leading ``NNN-`` directory under ``docs/sprints/``, if present."""
    for part in path.parts:
        if len(part) >= 3 and part[:3].isdigit() and part[3:4] == "-":
            return int(part.split("-", 1)[0])
    return None


def current_sprint_plan(root: Path) -> Path | None:
    """IMPLEMENTATION_PLAN.md for ``current_sprint.id``, or None to skip."""
    anchor = root / "docs" / "active_state.json"
    if not anchor.is_file():
        return None
    try:
        data = json.loads(anchor.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    sprint_id = data.get("current_sprint", {}).get("id")
    if not isinstance(sprint_id, int):
        return None
    if sprint_id < COST_FROM_SPRINT:
        return None
    matches = sorted((root / "docs" / "sprints").glob(f"{sprint_id:03d}-*/IMPLEMENTATION_PLAN.md"))
    return matches[0] if matches else None


def _has_heading(text: str, title: str) -> bool:
    return re.search(rf"^##\s+{re.escape(title)}\b", text, re.MULTILINE) is not None


def _mechanisms_has_invoker(text: str) -> bool:
    match = re.search(r"^##\s+Mechanisms\b.*?(?=^##\s|\Z)", text, re.MULTILINE | re.DOTALL)
    if match is None:
        return False
    header = next((line for line in match.group(0).splitlines() if line.startswith("|") and "Mechanism" in line), "")
    return "Invoker" in header


def _section(text: str, title: str) -> str:
    """Body of the ``## title`` section, or an empty string.

    Args:
        text: Full plan markdown.
        title: Section heading text following ``##``.

    Returns:
        The section text including its heading, or ``""`` when absent.
    """
    match = re.search(rf"^##\s+{re.escape(title)}\b.*?(?=^##\s|\Z)", text, re.MULTILINE | re.DOTALL)
    return match.group(0) if match else ""


def _split_row(line: str) -> list[str]:
    """Cells of one table row, splitting only on unescaped pipes outside backticks.

    Args:
        line: One markdown table row.

    Returns:
        The stripped cell texts, without the outer empty edge cells.
    """
    cells: list[str] = []
    current: list[str] = []
    in_code = False
    previous = ""
    for char in line.strip():
        if char == "`":
            in_code = not in_code
        if char == "|" and not in_code and previous != "\\":
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(char)
        previous = char
    cells.append("".join(current).strip())
    return cells[1:-1] if line.strip().endswith("|") else cells[1:]


def _tables(section: str) -> list[tuple[list[str], list[list[str]]]]:
    """Each table in a section as ``(header cells, body rows)``.

    Args:
        section: Section markdown text.

    Returns:
        One ``(header, rows)`` tuple per table, separator rows excluded.
    """
    tables: list[tuple[list[str], list[list[str]]]] = []
    in_table = False
    for line in section.splitlines():
        if not line.lstrip().startswith("|"):
            in_table = False
            continue
        cells = _split_row(line)
        if cells and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        if in_table:
            tables[-1][1].append(cells)
        else:
            tables.append((cells, []))
            in_table = True
    return tables


def _column(header: list[str], prefix: str) -> int | None:
    """Index of the first header cell starting with ``prefix``.

    Args:
        header: Header cells of a table.
        prefix: Text the wanted header cell starts with.

    Returns:
        The column index, or ``None`` when no header cell matches.
    """
    for index, cell in enumerate(header):
        if cell.startswith(prefix):
            return index
    return None


def _cell(row: list[str], index: int) -> str:
    """Cell at ``index`` of a row, tolerating short rows.

    Args:
        row: Cells of one table row.
        index: Zero-based column index.

    Returns:
        The cell text, or ``""`` when the row is shorter than ``index``.
    """
    return row[index] if index < len(row) else ""


def _pipe_findings(rows: list[list[str]], where: str) -> list[str]:
    """Flag an escaped pipe inside a backticked command.

    Args:
        rows: Body rows of one table.
        where: Section name used as the finding prefix.

    Returns:
        A one-item list with the finding, or an empty list.
    """
    spans = (span for row in rows for cell in row for span in re.findall(r"`([^`]*)`", cell))
    if any("\\|" in span and span.replace("\\|", "").strip() for span in spans):
        return [f"{where}: escaped pipe inside a backticked command; use -e a -e b."]
    return []


def _is_absence_claim(expected: str, command: str) -> bool:
    """True when ``Expected`` asserts silence or zero hits, not an exit code.

    Args:
        expected: Text of the Expected cell.
        command: Text of the command cell, checked for ``$?``.

    Returns:
        ``True`` for an absence claim, ``False`` otherwise.
    """
    plain = expected.replace("`", "").strip().lower()
    if plain.startswith("no output") or plain in {"0 hits", "0 matches"}:
        return True
    return plain == "0" and "$?" not in command


def _verification_row(header: list[str], row: list[str]) -> list[str]:
    """Findings for one Verification row.

    Args:
        header: Header cells of the Verification table.
        row: Cells of one body row.

    Returns:
        Findings for a missing Positive control or an empty Dry run cell.
    """
    command = _cell(row, 0)
    control = _column(header, "Positive control")
    dry = _column(header, "Dry run")
    found: list[str] = []
    if control is not None and _is_absence_claim(_cell(row, 1), command) and _cell(row, control) in EMPTY:
        found.append(f"Verification: no-output/zero expectation without a Positive control: {command}")
    if dry is not None and not _cell(row, dry):
        found.append(f"Verification: empty Dry run cell: {command}")
    return found


def _verification_findings(text: str) -> list[str]:
    """Findings across every table of the Verification section.

    Args:
        text: Full plan markdown.

    Returns:
        All pipe and row findings; empty when the section is absent or clean.
    """
    findings: list[str] = []
    for header, rows in _tables(_section(text, "Verification")):
        findings += _pipe_findings(rows, "Verification")
        for row in rows:
            findings += _verification_row(header, row)
    return findings


def _tests_row(observed: int | None, row: list[str]) -> list[str]:
    """Findings for one Tests row.

    Args:
        observed: Index of the ``Observed at base`` column, or ``None``.
        row: Cells of one body row.

    Returns:
        A one-item list when a ``**Yes**`` row has an empty observed cell, else empty.
    """
    if observed is not None and _cell(row, 1).startswith("**Yes**") and not _cell(row, observed):
        return [f"Tests: **Yes** row with an empty Observed at base cell: {_cell(row, 0)}"]
    return []


def _tests_findings(text: str) -> list[str]:
    """Findings across every table of the Tests section.

    Args:
        text: Full plan markdown.

    Returns:
        All pipe and row findings; empty when the section is absent or clean.
    """
    findings: list[str] = []
    for header, rows in _tables(_section(text, "Tests")):
        findings += _pipe_findings(rows, "Tests")
        observed = _column(header, "Observed at base")
        for row in rows:
            findings += _tests_row(observed, row)
    return findings


def collect_findings(text: str) -> list[str]:
    """Structural wastes in one plan. Empty means pass.

    Args:
        text: Full plan markdown.

    Returns:
        One message per structural waste found.
    """
    findings: list[str] = []
    lowered = text.lower()
    if "review the whole system" in lowered:
        findings.append("Filter 3: plan says 'review the whole system' (1-Agent : 1-File).")
    if "raw json dump" in lowered or "complete csv" in lowered:
        findings.append("Filter 4: plan dumps raw JSON or a complete CSV into chat.")
    if "/loop" in lowered and "loop_guard.py" not in lowered:
        findings.append("Filter 6: `/loop` without `loop_guard.py start`.")
    if not _has_heading(text, "Mechanisms"):
        findings.append("Mechanisms section is missing.")
    elif not _mechanisms_has_invoker(text):
        findings.append("Mechanisms table has no Invoker column (RA-16).")
    if not _has_heading(text, "Cost"):
        findings.append("Cost section is missing (required from Sprint 030).")
    return findings + _verification_findings(text) + _tests_findings(text)


def audit(path: Path) -> int:
    """Print findings for one file. Returns the process exit code."""
    if not path.is_file():
        print(f"⚠️  No plan at {path}; skip.", file=sys.stderr)
        return 0
    findings = collect_findings(path.read_text(encoding="utf-8"))
    if not findings:
        print(f"[OK] audit_plan: {path}")
        return 0
    print(f"❌ audit_plan: {path}", file=sys.stderr)
    for item in findings:
        print(f"   • {item}", file=sys.stderr)
    return 2


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("plan", nargs="?", type=Path, help="IMPLEMENTATION_PLAN.md")
    parser.add_argument(
        "--current-sprint",
        action="store_true",
        help="Audit docs/sprints/[ID]/IMPLEMENTATION_PLAN.md when ID >= 30",
    )
    args = parser.parse_args()
    if args.current_sprint:
        target = current_sprint_plan(Path.cwd())
        if target is None:
            print("[OK] audit_plan: no current-sprint plan to audit (skip)")
            return 0
        return audit(target)
    if args.plan is None:
        parser.error("plan path or --current-sprint is required")
    return audit(args.plan)


if __name__ == "__main__":
    sys.exit(main())
