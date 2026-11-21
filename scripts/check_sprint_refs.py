"""Fail when a sprint's artifacts cite an id with no home, or break plan D37's limits.

Plan D37 (Sprint 059) gives each fact of a sprint one home and lets the other
artifacts cite its id. This check covers a stated subset of that rule, and
nothing else:

| Check | Home | Cited where |
| :--- | :--- | :--- |
| Work units | the unit ids of the plan's ``## Work`` tables | the same set in ``task_scope.md`` ``## Work`` and ``agent_assignment.md`` ``## Staffing`` (set equality) |
| Decisions ``D<n>`` | the ``ID`` column of the plan's ``## Design`` table | the four artifacts |
| ``KI-<NNN>-<n>`` of this sprint | the ``KI ID`` column of ``SPRINT_LOG.md`` | the four artifacts |
| Gate findings ``R<round>-<n>`` | the ``ID`` column of ``### Gate findings`` | the four artifacts, from the first round the table covers |

It also checks that a known-issue row (a ``SPRINT_LOG.md`` table row whose last
cell is a ``KI-<sprint>-<n>`` id) which names a unit that ``task_scope.md`` marks
``✅`` followed by backticked SHAs cites one of those SHAs (plan D45). A unit id
is matched as a whole token (``C-01`` does not match ``C-01b``); a cited SHA of
7 or more hex characters matches by prefix in either direction. A missing
``task_scope.md`` or ``SPRINT_LOG.md`` skips this check with an ``[OK] ... (skip)``
line, as a missing plan skips the whole script.

It also checks two limits: every Design row from the first covered decision on
has a non-empty ``Check`` column or contains ``**Check**:``, and every Quality Gate ``Notes`` cell from the first
covered round on holds at most 400 characters. It does not detect a copied fact
that carries no id, such as a unit count written out in prose. Sprints before
059 are skipped.

invoked_by: Makefile `verify`.

Usage:
    python3 scripts/check_sprint_refs.py --sprint-dir docs/sprints/059-core-pipeline
    python3 scripts/check_sprint_refs.py --current-sprint

Exit codes:
    0 — pass, or skip (no anchor or ``current_sprint`` block, sprint before 059,
        no IMPLEMENTATION_PLAN.md yet; the known-issue SHA check alone skips when
        ``task_scope.md`` or ``SPRINT_LOG.md`` is missing)
    2 — a finding, a missing ``--sprint-dir``, or an anchor naming no existing
        sprint directory
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _current_sprint import CurrentSprintError, current_sprint_dir, project_root
from _md_table import split_cells
from check_task_scope import sprint_id_from_dir

FROM_SPRINT = 59
NOTES_LIMIT = 400
ARTIFACTS = ("IMPLEMENTATION_PLAN.md", "task_scope.md", "agent_assignment.md", "SPRINT_LOG.md")
# Sprint 059 adopted D37 mid-sprint: earlier decisions, rounds and gate rows are exempt.
CHECK_FROM_DECISION = {59: 37}
FINDINGS_FROM_ROUND = {59: 13}
NOTES_FROM_ROUND = {59: {"qa agent (gate 1)": 13, "tester agent (gate 2)": 2}}
UNIT = re.compile(r"^\| ([A-Z]-\d{2}[a-z]?) \|", re.MULTILINE)
DECISION = re.compile(r"\bD(\d+)\b")
FINDING = re.compile(r"\bR(\d+)-\d+\b")
UNIT_ID = re.compile(r"[A-Z]-\d{2}[a-z]?")
KI_ID = re.compile(r"KI-\d+-\d+")
SHA = re.compile(r"`([0-9a-f]{7,40})`")
HEX_TOKEN = re.compile(r"\b[0-9a-f]{7,40}\b")


def section(text: str, start: str, end: str) -> str:
    """The text from the first line starting with ``start`` to the next ``end`` line."""
    match = re.search(rf"^{re.escape(start)}.*?(?=^{re.escape(end)}|\Z)", text, re.MULTILINE | re.DOTALL)
    return match.group(0) if match else ""


def _is_separator(line: str) -> bool:
    return line.startswith("|") and set(line.strip()) <= set("|:- ")


def _rows_after(lines: list[str], start: int) -> list[list[str]]:
    """Cells of the consecutive table rows from ``start`` on."""
    rows = []
    for row in lines[start:]:
        if not row.startswith("|"):
            break
        rows.append(split_cells(row))
    return rows


def tables(text: str) -> list[tuple[list[str], list[list[str]]]]:
    """Every Markdown table in ``text`` as (header cells, data rows)."""
    lines = text.splitlines()
    return [
        (split_cells(line), _rows_after(lines, index + 2))
        for index, line in enumerate(lines[:-1])
        if line.startswith("|") and _is_separator(lines[index + 1])
        and not (index > 0 and lines[index - 1].startswith("|"))
    ]


def column(text: str, header_name: str) -> set[str]:
    """Every cell under a header named ``header_name``, across all tables."""
    cells: set[str] = set()
    for header, rows in tables(text):
        if header_name in header:
            position = header.index(header_name)
            cells.update(row[position].strip("`") for row in rows if len(row) > position)
    return cells


def unit_findings(texts: dict[str, str]) -> list[str]:
    """Unit ids of task_scope and agent_assignment must equal the plan's."""
    plan = set(UNIT.findall(section(texts["IMPLEMENTATION_PLAN.md"], "## Work", "## ")))
    mirrors = {
        "task_scope.md": section(texts.get("task_scope.md", ""), "## Work", "## Jurisdiction"),
        "agent_assignment.md": section(texts.get("agent_assignment.md", ""), "## Staffing", "## Disagreements"),
    }
    findings = []
    for name, body in mirrors.items():
        if name not in texts:
            continue
        units = set(UNIT.findall(body))
        for unit in sorted(plan - units):
            findings.append(f"{name}: unit {unit} of the plan is missing")
        for unit in sorted(units - plan):
            findings.append(f"{name}: unit {unit} is not in the plan")
    return findings


def cited(texts: dict[str, str], pattern: re.Pattern[str]) -> set[str]:
    """Every match of ``pattern`` across the artifacts."""
    return {match.group(0) for text in texts.values() for match in pattern.finditer(text)}


def design_table(plan: str) -> list[tuple[list[str], list[str]]]:
    """(header, row) of each ``## Design`` table row whose ID is ``D<n>``."""
    body = section(plan, "## Design", "## Work")
    return [(header, row) for header, rows in tables(body) if header[:1] == ["ID"] for row in rows if DECISION.fullmatch(row[0])]


def design_rows(plan: str) -> list[list[str]]:
    """Data rows of the plan's ``## Design`` table whose ID is ``D<n>``."""
    return [row for _, row in design_table(plan)]


def _has_check(header: list[str], row: list[str]) -> bool:
    """A non-empty ``Check`` column, or ``**Check**:`` anywhere in the row."""
    if "Check" in header and len(row) > header.index("Check") and row[header.index("Check")]:
        return True
    return "**Check**:" in " | ".join(row)


def id_findings(texts: dict[str, str], sprint: int) -> list[str]:
    """Decision, KI and gate-finding ids cited anywhere must exist in their home."""
    rows = design_rows(texts["IMPLEMENTATION_PLAN.md"])
    decisions = {row[0] for row in rows}
    log = texts.get("SPRINT_LOG.md", "")
    kis = column(log, "KI ID")
    gate_ids = column(section(log, "### Gate findings", "### "), "ID")
    first_round = FINDINGS_FROM_ROUND.get(sprint, 1)
    findings = [f"decision {d} is cited but not in the Design table" for d in sorted(cited(texts, DECISION) - decisions)]
    own_ki = re.compile(rf"\bKI-{sprint:03d}-\d+\b")
    findings += [f"{k} is cited but not in the SPRINT_LOG.md KI table" for k in sorted(cited(texts, own_ki) - kis)]
    for finding in sorted(cited(texts, FINDING) - gate_ids):
        if int(FINDING.fullmatch(finding).group(1)) >= first_round:
            findings.append(f"{finding} is cited but not in the Gate findings table")
    return findings


def _check_findings(plan: str, sprint: int) -> list[str]:
    """Design rows from the first covered decision on need a check."""
    first = CHECK_FROM_DECISION.get(sprint, 0)
    return [
        f"Design row {row[0]} has no **Check**: and no Check column value"
        for header, row in design_table(plan)
        if int(row[0][1:]) >= first and not _has_check(header, row)
    ]


def _gate_rows(log: str) -> list[tuple[str, str, str]]:
    """(gate, round, notes) of every Quality Gate table row."""
    keys = ("Gate", "Round", "Notes")
    return [
        tuple(row[header.index(k)] for k in keys)
        for header, rows in tables(log)
        if {"Gate", "Round", "Verdict", "Notes"} <= set(header)
        for row in rows
    ]


def _notes_findings(log: str, sprint: int) -> list[str]:
    """Quality Gate Notes from the first covered round on stay within the limit."""
    rounds = NOTES_FROM_ROUND.get(sprint, {})
    return [
        f"{gate} round {round_cell}: Notes holds {len(notes)} characters (limit {NOTES_LIMIT})"
        for gate, round_cell, notes in _gate_rows(log)
        if round_cell.isdigit() and int(round_cell) >= rounds.get(gate.lower(), 1) and len(notes) > NOTES_LIMIT
    ]


def limit_findings(texts: dict[str, str], sprint: int) -> list[str]:
    """The two plan D37 limits: ``**Check**:`` in Design rows and the Notes cap."""
    return _check_findings(texts["IMPLEMENTATION_PLAN.md"], sprint) + _notes_findings(texts.get("SPRINT_LOG.md", ""), sprint)


def _done_row(row: list[str], position: int) -> tuple[str, list[str]] | None:
    """(unit id, SHAs) when ``row`` is a unit whose status cell holds ✅ and backticked SHAs."""
    status = row[position] if len(row) > position else ""
    unit = row[0].strip("`")
    shas = SHA.findall(status) if "✅" in status else []
    return (unit, shas) if shas and UNIT_ID.fullmatch(unit) else None


def done_units(task_scope: str) -> dict[str, list[str]]:
    """Unit id -> backticked SHAs, for each task_scope row whose status cell holds ✅ and SHAs."""
    pairs = [
        _done_row(row, header.index("Status"))
        for header, rows in tables(task_scope)
        if "Status" in header
        for row in rows
    ]
    return dict(pair for pair in pairs if pair)


def _cites(row_text: str, shas: list[str]) -> bool:
    """True when ``row_text`` holds a hex token that prefixes, or is prefixed by, one of ``shas``."""
    tokens = HEX_TOKEN.findall(row_text)
    return any(sha.startswith(token) or token.startswith(sha) for token in tokens for sha in shas)


def _ki_rows(log: str) -> list[list[str]]:
    """Rows of every ``SPRINT_LOG.md`` table whose last cell is a ``KI-<sprint>-<n>`` id."""
    return [row for _, rows in tables(log) for row in rows if KI_ID.fullmatch(row[-1].strip("`"))]


def _row_findings(row: list[str], done: dict[str, list[str]]) -> list[str]:
    """Findings for one KI row: each done unit it names without citing one of that unit's SHAs."""
    text = " | ".join(row)
    return [
        f"{row[-1]} names unit {unit} (done) without its SHA: expected one of {', '.join(shas)}"
        for unit, shas in sorted(done.items())
        if re.search(rf"(?<![\w-]){re.escape(unit)}(?!\w)", text) and not _cites(text, shas)
    ]


def _missing_ki_inputs(texts: dict[str, str]) -> list[str]:
    return [name for name in ("task_scope.md", "SPRINT_LOG.md") if name not in texts]


def ki_sha_findings(texts: dict[str, str]) -> list[str]:
    """A KI row that names a done unit must cite one of that unit's SHAs (plan D45)."""
    if _missing_ki_inputs(texts):
        return []
    done = done_units(texts["task_scope.md"])
    return [item for row in _ki_rows(texts["SPRINT_LOG.md"]) for item in _row_findings(row, done)]


def check(sprint_dir: Path) -> int:
    """Audit one sprint directory. Returns the process exit code."""
    sprint = sprint_id_from_dir(sprint_dir)
    if sprint is not None and sprint < FROM_SPRINT:
        print(f"[OK] check_sprint_refs: sprint {sprint} predates {FROM_SPRINT} (skip)")
        return 0
    try:
        texts = {name: (sprint_dir / name).read_text(encoding="utf-8") for name in ARTIFACTS if (sprint_dir / name).is_file()}
    except (OSError, UnicodeDecodeError) as exc:
        print(f"❌ check_sprint_refs: cannot read an artifact under {sprint_dir}: {exc}", file=sys.stderr)
        return 2
    if "IMPLEMENTATION_PLAN.md" not in texts:
        print(f"[OK] check_sprint_refs: no IMPLEMENTATION_PLAN.md under {sprint_dir} yet (skip)")
        return 0
    number = sprint if sprint is not None else FROM_SPRINT
    findings = unit_findings(texts) + id_findings(texts, number) + limit_findings(texts, number)
    for name in _missing_ki_inputs(texts):
        print(f"[OK] check_sprint_refs: no {name} under {sprint_dir} yet, known-issue SHA check (skip)")
    findings += ki_sha_findings(texts)
    if not design_rows(texts["IMPLEMENTATION_PLAN.md"]):
        findings.append("IMPLEMENTATION_PLAN.md has no ## Design table with D<n> rows")
    if not findings:
        print(f"[OK] check_sprint_refs: {sprint_dir}")
        return 0
    print(f"❌ check_sprint_refs: {sprint_dir}", file=sys.stderr)
    for item in findings:
        print(f"   • {item}", file=sys.stderr)
    return 2


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--sprint-dir", type=Path, help="Canonical sprint directory")
    parser.add_argument("--current-sprint", action="store_true")
    args = parser.parse_args()
    if args.current_sprint:
        try:
            target = current_sprint_dir(project_root())
        except CurrentSprintError as exc:
            print(f"❌ check_sprint_refs: {exc}", file=sys.stderr)
            return 2
        if target is None:
            print("[OK] check_sprint_refs: no current sprint (skip)")
            return 0
        return check(target)
    if args.sprint_dir is None:
        parser.error("--sprint-dir or --current-sprint is required")
    if not args.sprint_dir.is_dir():
        print(f"❌ check_sprint_refs: --sprint-dir {args.sprint_dir} is not a directory", file=sys.stderr)
        return 2
    return check(args.sprint_dir)


if __name__ == "__main__":
    sys.exit(main())
