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


def collect_findings(text: str) -> list[str]:
    """Structural wastes in one plan. Empty means pass."""
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
    return findings


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
