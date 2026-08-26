"""Census CE-1–CE-5 over Cursor-era sprints 026–033 (derived audit).

Walks ``docs/sprints/{026..033}-core-pipeline/``, skips missing directories, and
writes ``docs/audits/CURSOR_ERA_EXECUTION_AUDIT.md``. Always exits ``0`` — this
is a census, not a gate. Uses existing parsers only (no new table parsers).

invoked_by: Makefile target `cursor-era-audit`.

Usage:
    python3 scripts/audit_cursor_era.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _root import agents_root  # noqa: E402
from check_gate_log import gate_tables  # noqa: E402
from check_role_artifact import (  # noqa: E402
    load_registry,
    missing_for_role,
    missing_gate_row,
)
from check_task_scope import collect_findings, sprint_id_from_dir  # noqa: E402

ERA_START = 26
ERA_END = 33
GATE_ROLES = ("QA Agent", "Tester Agent")
OUT_REL = Path("docs/audits/CURSOR_ERA_EXECUTION_AUDIT.md")


def required_roles() -> list[str]:
    """Registry display names that own a required sprint-scoped artifact."""
    names = {
        entry.get("role")
        for entry in load_registry()
        if entry.get("scope") == "sprint"
        and entry.get("required")
        and entry.get("role")
    }
    return sorted(names)


def ce1_count(sprint_dir: Path) -> int:
    """CE-1: finding count from ``check_task_scope.collect_findings``."""
    path = sprint_dir / "task_scope.md"
    if not path.is_file():
        return 0
    text = path.read_text(encoding="utf-8")
    return len(collect_findings(text, sprint_id_from_dir(sprint_dir)))


def ce2_count(sprint_dir: Path) -> int:
    """CE-2: missing required artifacts across required roles."""
    total = 0
    for role in required_roles():
        total += len(missing_for_role(role, sprint_dir))
    return total


def ce3_count(sprint_dir: Path) -> int:
    """CE-3: gate roles missing a Gate row (qa_agent / tester_agent)."""
    return sum(1 for role in GATE_ROLES if missing_gate_row(role, sprint_dir))


def _col(header: list[str], row: list[str], name: str) -> str:
    try:
        index = header.index(name)
    except ValueError:
        return ""
    return row[index] if index < len(row) else ""


def ce4_count(sprint_dir: Path) -> int:
    """CE-4: Tester Notes name pytest but omit ``tests/`` as a path substring."""
    log = sprint_dir / "SPRINT_LOG.md"
    if not log.is_file():
        return 0
    for header, rows in gate_tables(log.read_text(encoding="utf-8")):
        if "Gate" not in header or "Notes" not in header:
            continue
        for row in rows:
            gate = _col(header, row, "Gate")
            notes = _col(header, row, "Notes")
            if not gate.startswith("Tester"):
                continue
            if "pytest" in notes and "tests/" not in notes:
                return 1
    return 0


def sprint_row(sprint_dir: Path) -> dict[str, int | str]:
    """Counts for one era sprint directory."""
    return {
        "sprint": sprint_dir.name.split("-", 1)[0],
        "CE-1": ce1_count(sprint_dir),
        "CE-2": ce2_count(sprint_dir),
        "CE-3": ce3_count(sprint_dir),
        "CE-4": ce4_count(sprint_dir),
    }


def iter_era_dirs(root: Path) -> list[Path]:
    """Existing ``NNN-core-pipeline`` dirs in the inclusive 026–033 window."""
    found: list[Path] = []
    for number in range(ERA_START, ERA_END + 1):
        path = root / "docs" / "sprints" / f"{number:03d}-core-pipeline"
        if path.is_dir():
            found.append(path)
    return found


def render_markdown(rows: list[dict[str, int | str]]) -> str:
    """Build the derived audit markdown (table + CE-5 protocol block)."""
    lines = [
        "# Cursor-era execution audit (026–033)",
        "",
        "Derived by `scripts/audit_cursor_era.py`. Do not edit by hand.",
        "",
        "| Sprint | CE-1 | CE-2 | CE-3 | CE-4 |",
        "| :--- | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            f"| {row['sprint']} | {row['CE-1']} | {row['CE-2']} | "
            f"{row['CE-3']} | {row['CE-4']} |"
        )
    lines.extend(
        [
            "",
            "## CE-5 — sandbox vs non-sandbox pytest protocol",
            "",
            "Do not record live pass/fail counts here: sandbox denial of",
            "`git init` produces false reds, and a live count needs a clean",
            "environment that this census must not assume. Reproduce both",
            "sides with the same invocation:",
            "",
            "```bash",
            "# Outside sandbox (git init allowed) — suite should pass:",
            "./venv_skillopt/bin/python3 -m pytest tests/ -q; echo $?",
            "",
            "# Inside Cursor sandbox (git init may be denied) — compare:",
            "./venv_skillopt/bin/python3 -m pytest tests/ -q; echo $?",
            "```",
            "",
            "If the sandbox run fails with git-init permission errors while the",
            "non-sandbox run passes, treat the red as CE-5 (measurement noise),",
            "not a suite regression.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    """Write the derived audit and always return 0."""
    root = agents_root()
    rows = [sprint_row(path) for path in iter_era_dirs(root)]
    out = root / OUT_REL
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_markdown(rows), encoding="utf-8")
    print(f"Wrote {OUT_REL} ({len(rows)} sprint rows).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
