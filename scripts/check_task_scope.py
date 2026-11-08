"""Fail when the current sprint's task_scope.md omits Model/Effort.

``F-026-A2``: ``tier_escalation`` worked when a human asked, and slept for three
sprints when nobody did. This check makes the absence a deterministic finding.

Historical sprints before 028 are skipped (their tables never claimed those
columns). A ``--sprint-dir`` whose tables *claim* Model/Effort, or whose prose
declares Cursor, is always checked.

invoked_by: workflows/close_workflow.md Phase 2.6, workflows/pipeline_workflow.md
Phase 4.3, Makefile `verify`.

Usage:
    python3 scripts/check_task_scope.py --sprint-dir docs/sprints/030-core-pipeline
    python3 scripts/check_task_scope.py --current-sprint
    python3 scripts/check_task_scope.py --sprint-dir docs/sprints/059-core-pipeline --batches

An optional ``Depends on`` column in a Work table lists, per unit, ``-`` or an
empty cell (none) or comma-separated unit ids from the ``#`` column. When the
column is present the check refuses an id naming no unit, a unit depending on
itself, and a dependency cycle. ``--batches`` prints the remaining order, one
``batch N: id id`` line per batch of at most ``MAX_BATCH`` units whose
dependencies landed and whose ``File`` cells differ (plan D11 of Sprint 059).

Also refuses a row whose assignee cannot perform the operation it is given: a
profile with no ``Write``/``Edit`` tool cannot ``create``/``modify``/``delete`` a
file. Sprints 030 and 031 recorded such rows as executed successfully.

Exit codes:
    0 — pass, or skip (historical columns / non-canonical dir / no anchor or
        no ``current_sprint`` block)
    2 — a bad ``Depends on`` value, units ``--batches`` cannot schedule, an anchor that names no existing sprint directory, shape, undeclared mechanical-high row, incapable assignee, or a
        canonical sprint directory holding no task_scope.md at all (RA-11)
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import NamedTuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _current_sprint import CurrentSprintError, current_sprint_dir, project_root
from _md_table import split_cells
from _root import agents_root

MODEL_FROM_SPRINT = 28
MECHANICAL_PROFILES = frozenset({"devops_agent", "git_sync_agent", "topology_mapper"})
MECHANICAL_MODELS = frozenset({"haiku", "composer-2.5", "composer-2"})
WORK_KEYS = ("File", "Operation", "Risk", "Assignee")
MAX_BATCH = 4
WRITE_TOOLS = frozenset({"Write", "Edit"})
# Matched as substrings: real tables write "modify/create", "create + delete"
# and "modify (hito 2 gate)", so equality missed most of them. Deliberately
# excludes "emit verdict" — a gate emits, the orchestrator transcribes, and
# ADR-0008 gives the emitting role no file to write.
MUTATING_OPERATIONS = (
    "create",
    "modify",
    "delete",
    "move",
    "regenerate",
    "append",
    "transcribe",
)


def sprint_id_from_dir(sprint_dir: Path) -> int | None:
    """Leading digits of ``030-core-pipeline`` → 30."""
    name = sprint_dir.name
    prefix, separator, _ = name.partition("-")
    if separator and len(prefix) >= 3 and prefix.isascii() and prefix.isdigit():
        return int(prefix)
    return None


def _cells(line: str) -> list[str]:
    """Split a Markdown table row into cells, honouring the ``\\|`` escape.

    Args:
        line: One raw table row.

    Returns:
        list[str]: Stripped cells; an escaped pipe stays inside its cell as ``|``.
    """
    return [cell.strip("`") for cell in split_cells(line)]


def _is_separator(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and set(stripped) <= set("|:- ")


def _is_work_header(line: str) -> bool:
    """True when this line is a table header row naming every WORK_KEYS.

    Args:
        line: One raw line from the source document.
    """
    return (line.strip().startswith("|") and not _is_separator(line)
            and all(key in _cells(line) for key in WORK_KEYS))


def _collect_rows(lines: list[str], start: int) -> tuple[list[list[str]], int]:
    """Collect the body rows of a table starting at ``start``.

    Args:
        lines: All lines of the source document.
        start: Index of the first line after the header (and its
            separator, if already skipped by the caller).

    Returns:
        tuple[list[list[str]], int]: The parsed rows, and the index of the
        first line that is no longer part of this table.
    """
    rows: list[list[str]] = []
    index = start
    while index < len(lines) and lines[index].strip().startswith("|"):
        if not _is_separator(lines[index]):
            rows.append(_cells(lines[index]))
        index += 1
    return rows, index


def work_tables(text: str) -> list[tuple[list[str], list[list[str]]]]:
    """Work tables: headers that include File, Operation, Risk, Assignee."""
    tables: list[tuple[list[str], list[list[str]]]] = []
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if not _is_work_header(line):
            index += 1
            continue
        header = _cells(line)
        index += 1
        if index < len(lines) and _is_separator(lines[index]):
            index += 1
        rows, index = _collect_rows(lines, index)
        tables.append((header, rows))
    return tables


def requires_model_columns(sprint_id: int | None, text: str) -> bool:
    """True when this file must carry Model and Effort on every Work table."""
    if sprint_id is not None and sprint_id >= MODEL_FROM_SPRINT:
        return True
    lowered = text.lower()
    if "cursor" in lowered and (
        "session_tool" in lowered or "delegation_mode" in lowered or "**mode.**" in lowered
    ):
        return True
    return "Model | Effort" in text or "Model \\| Effort" in text


def _col(header: list[str], row: list[str], name: str) -> str:
    try:
        position = header.index(name)
    except ValueError:
        return ""
    return row[position] if position < len(row) else ""


def profile_tools(profile: str, root: Path) -> frozenset[str] | None:
    """Tools declared in a profile's frontmatter, or None when it has no file.

    Args:
        profile (str): Snake_case profile name as written in the Assignee cell.
        root (Path): Framework root holding ``agents/``.

    Returns:
        frozenset[str] | None: Declared tool names, or None if no such profile.
    """
    candidates = [root / "agents" / f"{profile}.md"]
    candidates.extend(sorted(root.glob(f"profiles/*/agents/{profile}.md")))
    for path in candidates:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        match = re.search(r"^tools:\s*(.+)$", text, re.MULTILINE)
        if match is None:
            return frozenset()
        return frozenset(part.strip() for part in match.group(1).split(",") if part.strip())
    return None


def _capability_findings(
    header: list[str], rows: list[list[str]], root: Path
) -> list[str]:
    """Rows whose assignee cannot perform the operation the row assigns it."""
    findings: list[str] = []
    for row in rows:
        operation = _col(header, row, "Operation").strip().lower()
        assignee = _col(header, row, "Assignee")
        profile = assignee.split()[0].strip("`,") if assignee else ""
        mutates = any(verb in operation for verb in MUTATING_OPERATIONS)
        if not mutates or not profile:
            continue
        unit = _col(header, row, "#") or "?"
        tools = profile_tools(profile, root)
        if tools is None:
            findings.append(f"Unit {unit}: assignee {profile!r} has no profile file.")
            continue
        if not tools & WRITE_TOOLS:
            findings.append(
                f"Unit {unit}: {profile} is assigned a {operation!r} but declares "
                f"no Write/Edit tool (declares: {', '.join(sorted(tools)) or 'none'})."
            )
    return findings


class Unit(NamedTuple):
    """One Work row: id, claimed file, committed flag, declared dependencies."""

    id: str
    file: str
    committed: bool
    deps: tuple[str, ...]
    has_column: bool


def _parse_deps(cell: str) -> tuple[str, ...]:
    """Unit ids of a ``Depends on`` cell; ``-`` and empty mean none."""
    parts = (part.strip().strip("`") for part in cell.split(","))
    return tuple(part for part in parts if part and part != "-")


def _row_unit(header: list[str], row: list[str]) -> Unit | None:
    unit_id = _col(header, row, "#")
    if not unit_id:
        return None
    return Unit(
        unit_id,
        _col(header, row, "File"),
        "\u2705" in _col(header, row, "Status"),
        _parse_deps(_col(header, row, "Depends on")),
        "Depends on" in header,
    )


def work_units(tables: list[tuple[list[str], list[list[str]]]]) -> list[Unit]:
    """Units of every Work table, in table order, rows without an id skipped."""
    parsed = (_row_unit(header, row) for header, rows in tables for row in rows)
    return [unit for unit in parsed if unit is not None]


def _dependency_problem(unit: Unit, dep: str, known: set[str]) -> str | None:
    if dep == unit.id:
        return f"Unit {unit.id}: depends on itself."
    if dep not in known:
        return f"Unit {unit.id}: depends on {dep!r}, which names no unit."
    return None


def _unit_dependency_findings(unit: Unit, known: set[str]) -> list[str]:
    problems = (_dependency_problem(unit, dep, known) for dep in unit.deps)
    return [problem for problem in problems if problem is not None]


def _cycle_members(units: list[Unit], known: set[str]) -> list[str]:
    """Units left after peeling every unit whose dependencies are all peeled."""
    waiting = {
        unit.id: {dep for dep in unit.deps if dep in known and dep != unit.id}
        for unit in units
    }
    while True:
        free = [name for name, deps in waiting.items() if not deps]
        if not free:
            return sorted(waiting)
        for name in free:
            del waiting[name]
        for deps in waiting.values():
            deps.difference_update(free)


def dependency_findings(units: list[Unit]) -> list[str]:
    """Unknown ids, self-dependencies and cycles. Empty without the column."""
    if not any(unit.has_column for unit in units):
        return []
    known = {unit.id for unit in units}
    findings: list[str] = []
    for unit in units:
        findings.extend(_unit_dependency_findings(unit, known))
    cyclic = _cycle_members(units, known)
    if cyclic:
        findings.append(
            "Dependency cycle among or behind units: " + ", ".join(cyclic) + "."
        )
    return findings


def _fill_batch(ready: list[Unit]) -> list[Unit]:
    """First units of ``ready`` (table order) with distinct files, up to MAX_BATCH."""
    batch: list[Unit] = []
    files: set[str] = set()
    for unit in ready:
        if len(batch) >= MAX_BATCH:
            break
        if unit.file and unit.file in files:
            continue
        files.add(unit.file)
        batch.append(unit)
    return batch


def schedule(units: list[Unit]) -> tuple[list[list[str]], list[str]]:
    """Batches of pending unit ids, and the ids that could not be scheduled.

    Args:
        units: Work units in table order.

    Returns:
        tuple[list[list[str]], list[str]]: Batches in dispatch order; each batch
        treats the earlier ones as landed. The second item is empty on success.
    """
    landed = {unit.id for unit in units if unit.committed}
    remaining = [unit for unit in units if not unit.committed]
    batches: list[list[str]] = []
    while remaining:
        ready = [unit for unit in remaining if landed.issuperset(unit.deps)]
        batch = _fill_batch(ready)
        if not batch:
            return batches, [unit.id for unit in remaining]
        ids = [unit.id for unit in batch]
        batches.append(ids)
        landed.update(ids)
        remaining = [unit for unit in remaining if unit.id not in ids]
    return batches, []


def collect_findings(
    text: str, sprint_id: int | None, root: Path | None = None
) -> list[str]:
    """Dependency, shape, mechanical-high and capability findings. Empty means pass."""
    tables = work_tables(text)
    if not tables:
        return []
    findings = dependency_findings(work_units(tables))
    if not requires_model_columns(sprint_id, text):
        return findings
    resolved_root = root if root is not None else agents_root()
    for header, rows in tables:
        findings.extend(_capability_findings(header, rows, resolved_root))
        if "Model" not in header or "Effort" not in header:
            findings.append(
                "Work table is missing Model/Effort columns "
                f"(header: {' | '.join(header)})."
            )
            continue
        findings.extend(_mechanical_high_findings(header, rows))
    return findings


def _mechanical_high_findings(header: list[str], rows: list[list[str]]) -> list[str]:
    findings: list[str] = []
    for row in rows:
        assignee = _col(header, row, "Assignee")
        risk = _col(header, row, "Risk").lower()
        model = _col(header, row, "Model").lower()
        profile = assignee.split()[0].strip("`,") if assignee else ""
        if profile not in MECHANICAL_PROFILES or risk != "high":
            continue
        note = assignee.lower() + " " + " ".join(row).lower()
        escalated = "escalat" in note or "keep" in note
        still_mechanical = any(token in model for token in MECHANICAL_MODELS) or not model
        if still_mechanical and not escalated:
            unit = _col(header, row, "#") or "?"
            findings.append(
                f"Unit {unit}: mechanical profile {profile} at high risk with "
                f"model {model or '(empty)'} and no escalation/keep note."
            )
    return findings


def check(sprint_dir: Path) -> int:
    """Audit one sprint directory. Returns the process exit code."""
    path = sprint_dir / "task_scope.md"
    sprint_id = sprint_id_from_dir(sprint_dir)
    if not path.is_file():
        if sprint_id is None:
            print(f"[OK] check_task_scope: {sprint_dir} is not a sprint directory (skip)")
            return 0
        print(
            f"❌ check_task_scope: no task_scope.md under {sprint_dir}. Phase 4.3 did "
            "not run, and jurisdictional_lock and no_interference are both applied by "
            "reading that file — they are disabled while appearing enforced.",
            file=sys.stderr,
        )
        return 2
    findings = collect_findings(path.read_text(encoding="utf-8"), sprint_id)
    if not findings:
        print(f"[OK] check_task_scope: {path}")
        return 0
    print(f"❌ check_task_scope: {path}", file=sys.stderr)
    for item in findings:
        print(f"   • {item}", file=sys.stderr)
    return 2


def print_batches(sprint_dir: Path) -> int:
    """Print the remaining batches of one sprint directory; exit code 0 or 2."""
    path = sprint_dir / "task_scope.md"
    if not path.is_file():
        print(f"❌ check_task_scope: no task_scope.md under {sprint_dir}", file=sys.stderr)
        return 2
    units = work_units(work_tables(path.read_text(encoding="utf-8")))
    findings = dependency_findings(units)
    batches, stuck = ([], []) if findings else schedule(units)
    if stuck:
        findings.append("Pending units cannot be scheduled: " + ", ".join(stuck) + ".")
    if findings:
        print(f"❌ check_task_scope: {path}", file=sys.stderr)
        for item in findings:
            print(f"   • {item}", file=sys.stderr)
        return 2
    for number, ids in enumerate(batches, start=1):
        print(f"batch {number}: {' '.join(ids)}")
    if not batches:
        print("no pending units")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--sprint-dir", type=Path, help="Canonical sprint directory")
    parser.add_argument("--current-sprint", action="store_true")
    parser.add_argument(
        "--batches", action="store_true",
        help="Print the remaining parallel batches instead of auditing",
    )
    args = parser.parse_args()
    if args.current_sprint:
        try:
            target = current_sprint_dir(project_root())
        except CurrentSprintError as exc:
            print(f"❌ check_task_scope: {exc}", file=sys.stderr)
            return 2
        if target is None:
            print("[OK] check_task_scope: no current sprint directory (skip)")
            return 0
        return print_batches(target) if args.batches else check(target)
    if args.sprint_dir is None:
        parser.error("--sprint-dir or --current-sprint is required")
    return print_batches(args.sprint_dir) if args.batches else check(args.sprint_dir)


if __name__ == "__main__":
    sys.exit(main())
