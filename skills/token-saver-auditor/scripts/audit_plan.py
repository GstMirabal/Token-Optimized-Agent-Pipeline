"""Audit an Implementation Plan against structural token-economy filters.

Filter 5 (recurring mechanism vs script) is owned by
``scripts/scan_workflow_determinism.py`` and is not reimplemented here.
This script covers the plan artifact: Filters 1-4, 6, Mechanisms/Invoker,
and the Cost section required from Sprint 030.

invoked_by: workflows/pipeline_workflow.md Phases 1 and 5, Makefile `verify`.

Usage:
    python3 skills/token-saver-auditor/scripts/audit_plan.py <plan.md>
    python3 skills/token-saver-auditor/scripts/audit_plan.py --current-sprint

Blast radius (R-5): a Work row whose File cell matches a ``shared_globs``
pattern needs a Verification row whose Command contains ``full_suite_command``.
Source: ``<cwd>/.agents-blast-radius.json`` when it exists (the host root is the
current directory, as for ``--current-sprint``), which REPLACES the nucleus
``config/blast_radius.json`` wholesale (resolved from this script, never merged).
Neither file present: the check is skipped with a printed note.

Exit codes:
    0 — pass, or --current-sprint skipped (no plan, or sprint id < 30)
    2 — structural waste found (RA-11), or a malformed blast-radius list
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import sys
from pathlib import Path

COST_FROM_SPRINT = 30
EMPTY = {"", "—", "-"}
HOST_BLAST_FILE = ".agents-blast-radius.json"
NUCLEUS_BLAST_FILE = Path(__file__).resolve().parents[3] / "config" / "blast_radius.json"


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


def load_blast_radius(
    cwd: Path, nucleus_file: Path = NUCLEUS_BLAST_FILE
) -> tuple[str, list[str]] | None:
    """Read the blast-radius list: host override first, else the nucleus file.

    Args:
        cwd: Host root; ``<cwd>/.agents-blast-radius.json`` replaces the nucleus list.
        nucleus_file: Path of the nucleus ``config/blast_radius.json``.

    Returns:
        ``(full_suite_command, shared_globs)``, or ``None`` when neither file exists.

    Raises:
        ValueError: The chosen file is not valid JSON or lacks a well-formed key.
    """
    host_file = cwd / HOST_BLAST_FILE
    source = host_file if host_file.is_file() else nucleus_file
    if not source.is_file():
        return None
    try:
        data = json.loads(source.read_text(encoding="utf-8"))
        command, globs = data["full_suite_command"], data["shared_globs"]
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise ValueError(f"blast-radius list {source} is malformed: {error!r}") from error
    if not isinstance(command, str) or not command.strip():
        raise ValueError(f"blast-radius list {source}: full_suite_command must be a non-empty string")
    if not isinstance(globs, list) or not all(isinstance(g, str) for g in globs):
        raise ValueError(f"blast-radius list {source}: shared_globs must be a list of strings")
    return command.strip(), globs


def _work_files(text: str) -> list[str]:
    """Paths named in the File column of every Work table.

    Args:
        text: Full plan markdown.

    Returns:
        Backticked spans of each File cell, or the bare cell when it has none.
    """
    files: list[str] = []
    for header, rows in _tables(_section(text, "Work")):
        column = _column(header, "File")
        for row in rows if column is not None else []:
            cell = _cell(row, column)
            files += re.findall(r"`([^`]+)`", cell) or [cell.strip()]
    return files


def _blast_findings(text: str, cwd: Path) -> list[str]:
    """R-5 finding: shared file touched by Work with no full-suite Verification row.

    Args:
        text: Full plan markdown.
        cwd: Host root used to find the override list.

    Returns:
        One finding, or empty when the list is absent, nothing shared is touched,
        or a Verification Command contains the full-suite command.
    """
    loaded = load_blast_radius(cwd)
    if loaded is None:
        print("note: no blast-radius list found; R-5 check skipped.", file=sys.stderr)
        return []
    command, globs = loaded
    hits = [f for f in _work_files(text) if any(fnmatch.fnmatch(f, g) for g in globs)]
    commands = [
        _cell(row, 0).replace("`", "")
        for _, rows in _tables(_section(text, "Verification"))
        for row in rows
    ]
    if hits and not any(command in item for item in commands):
        return [f"R-5: Work touches shared {sorted(set(hits))} but no Verification row runs `{command}`."]
    return []


def collect_findings(text: str, cwd: Path | None = None) -> list[str]:
    """Structural wastes in one plan. Empty means pass.

    Args:
        text: Full plan markdown.
        cwd: Host root for the blast-radius override; defaults to the current directory.

    Returns:
        One message per structural waste found.

    Raises:
        ValueError: The blast-radius list is malformed.
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
    findings += _verification_findings(text) + _tests_findings(text)
    return findings + _blast_findings(text, cwd or Path.cwd())


def audit(path: Path) -> int:
    """Print findings for one file. Returns the process exit code."""
    if not path.is_file():
        print(f"⚠️  No plan at {path}; skip.", file=sys.stderr)
        return 0
    try:
        findings = collect_findings(path.read_text(encoding="utf-8"))
    except ValueError as error:
        print(f"❌ audit_plan: {error}", file=sys.stderr)
        return 2
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
