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

Exit codes:
    0 — pass, skip (historical / no file / no anchor)
    2 — shape or undeclared mechanical-high row (RA-11)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _root import agents_root  # noqa: E402

MODEL_FROM_SPRINT = 28
MECHANICAL_PROFILES = frozenset({"devops_agent", "git_sync_agent", "topology_mapper"})
MECHANICAL_MODELS = frozenset({"haiku", "composer-2.5", "composer-2"})
WORK_KEYS = ("File", "Operation", "Risk", "Assignee")


def sprint_id_from_dir(sprint_dir: Path) -> int | None:
    """Leading digits of ``030-core-pipeline`` → 30."""
    name = sprint_dir.name
    if len(name) >= 3 and name[:3].isdigit() and name[3:4] == "-":
        return int(name.split("-", 1)[0])
    return None


def current_sprint_dir(root: Path) -> Path | None:
    """Canonical sprint directory for the anchor's ``current_sprint.id``."""
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
    matches = sorted((root / "docs" / "sprints").glob(f"{sprint_id:03d}-*"))
    dirs = [path for path in matches if path.is_dir()]
    return dirs[0] if dirs else None


def _cells(line: str) -> list[str]:
    raw = [part.strip().strip("`") for part in line.strip().strip("|").split("|")]
    return raw


def _is_separator(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and set(stripped) <= set("|:- ")


def work_tables(text: str) -> list[tuple[list[str], list[list[str]]]]:
    """Work tables: headers that include File, Operation, Risk, Assignee."""
    tables: list[tuple[list[str], list[list[str]]]] = []
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.strip().startswith("|") and not _is_separator(line):
            header = _cells(line)
            if all(key in header for key in WORK_KEYS):
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


def collect_findings(text: str, sprint_id: int | None) -> list[str]:
    """Shape and undeclared mechanical-high rows. Empty means pass or skip."""
    tables = work_tables(text)
    if not tables:
        return []
    if not requires_model_columns(sprint_id, text):
        return []
    findings: list[str] = []
    for header, rows in tables:
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
    if not path.is_file():
        print(f"[OK] check_task_scope: no task_scope.md under {sprint_dir} (skip)")
        return 0
    sprint_id = sprint_id_from_dir(sprint_dir)
    findings = collect_findings(path.read_text(encoding="utf-8"), sprint_id)
    if not findings:
        print(f"[OK] check_task_scope: {path}")
        return 0
    print(f"❌ check_task_scope: {path}", file=sys.stderr)
    for item in findings:
        print(f"   • {item}", file=sys.stderr)
    return 2


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--sprint-dir", type=Path, help="Canonical sprint directory")
    parser.add_argument("--current-sprint", action="store_true")
    args = parser.parse_args()
    root = agents_root() if (Path.cwd() / "scripts" / "check_task_scope.py").is_file() else Path.cwd()
    if args.current_sprint:
        target = current_sprint_dir(root)
        if target is None:
            print("[OK] check_task_scope: no current sprint directory (skip)")
            return 0
        return check(target)
    if args.sprint_dir is None:
        parser.error("--sprint-dir or --current-sprint is required")
    return check(args.sprint_dir)


if __name__ == "__main__":
    sys.exit(main())
