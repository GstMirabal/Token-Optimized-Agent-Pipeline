"""Derived model/gate ledger from sprint SPRINT_LOG + task_scope.

Joins existing parsers only — no new markdown table scrapers.

invoked_by: Makefile target `model-ledger`, workflows/close_workflow.md.

Usage:
    python3 scripts/model_ledger.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _root import agents_root  # noqa: E402
from check_gate_log import gate_tables  # noqa: E402
from check_task_scope import (  # noqa: E402
    sprint_id_from_dir,
    work_tables,
)

SKIP_BEFORE = 31
OUT_REL = Path("docs/audits/MODEL_LEDGER.md")
SPRINT_DIR_RE = re.compile(r"^(\d{3})-")


def _plain(cell: str) -> str:
    return cell.replace("*", "").replace("`", "").strip()


def _col(header: list[str], row: list[str], name: str) -> str:
    try:
        index = header.index(name)
    except ValueError:
        return ""
    return row[index] if index < len(row) else ""


def list_sprint_dirs(root: Path) -> list[Path]:
    """Canonical sprint directories under docs/sprints/, sorted by id."""
    base = root / "docs" / "sprints"
    if not base.is_dir():
        return []
    found: list[Path] = []
    for path in sorted(base.iterdir()):
        if path.is_dir() and SPRINT_DIR_RE.match(path.name):
            found.append(path)
    return found


def gate_round_counts(log_text: str) -> tuple[int, int, str]:
    """Return (gate1_rounds, gate2_rounds, verdict classes joined)."""
    gate1 = 0
    gate2 = 0
    verdicts: list[str] = []
    for header, rows in gate_tables(log_text):
        for row in rows:
            gate = _plain(_col(header, row, "Gate"))
            verdict = _plain(_col(header, row, "Verdict")).upper()
            klass = _plain(_col(header, row, "Class")).lower()
            lower = gate.lower()
            if lower.startswith("qa"):
                gate1 += 1
            elif lower.startswith("tester"):
                gate2 += 1
            if verdict:
                label = verdict if not klass else f"{verdict}:{klass}"
                if label not in verdicts:
                    verdicts.append(label)
    return gate1, gate2, ", ".join(verdicts)


def work_summary(scope_text: str) -> tuple[int, str, str, str]:
    """Return (units, models, efforts, tiers) from Work tables."""
    units = 0
    models: set[str] = set()
    efforts: set[str] = set()
    for header, rows in work_tables(scope_text):
        for row in rows:
            if not any(cell.strip() for cell in row):
                continue
            units += 1
            model = _plain(_col(header, row, "Model"))
            effort = _plain(_col(header, row, "Effort"))
            if model:
                models.add(model)
            if effort and effort.upper() != "N/A":
                efforts.add(effort)
    model_id = ", ".join(sorted(models)) if models else ""
    effort = ", ".join(sorted(efforts)) if efforts else ""
    tier = ""
    if models:
        tier = "mixed" if len(models) > 1 else "mapped"
    return units, model_id, effort, tier


def sprint_row(sprint_dir: Path) -> dict[str, str | int] | None:
    """Build one ledger row, or None when the sprint is omitted."""
    sprint_id = sprint_id_from_dir(sprint_dir)
    if sprint_id is None:
        return None
    if sprint_id < SKIP_BEFORE:
        return None
    log_path = sprint_dir / "SPRINT_LOG.md"
    if not log_path.is_file():
        return None
    log_text = log_path.read_text(encoding="utf-8")
    tables = gate_tables(log_text)
    if not tables:
        return None
    gate1, gate2, verdicts = gate_round_counts(log_text)
    scope_path = sprint_dir / "task_scope.md"
    units, model_id, effort, tier = (0, "", "", "")
    if scope_path.is_file():
        units, model_id, effort, tier = work_summary(
            scope_path.read_text(encoding="utf-8")
        )
    return {
        "sprint_id": sprint_id,
        "tier": tier,
        "model_id": model_id,
        "effort": effort,
        "units": units,
        "gate1_rounds": gate1,
        "gate2_rounds": gate2,
        "verdicts": verdicts,
    }


def render_markdown(
    rows: list[dict[str, str | int]],
    omitted: list[str],
) -> str:
    """Build MODEL_LEDGER.md body."""
    lines = [
        "# Model / gate ledger",
        "",
        "Derived by `scripts/model_ledger.py`. Do not edit by hand.",
        "Regenerate: `make model-ledger`.",
        "",
        "| sprint_id | tier | model_id | effort | units | gate1_rounds |"
        " gate2_rounds | verdicts |",
        "| ---: | :--- | :--- | :--- | ---: | ---: | ---: | :--- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['sprint_id']} | {row['tier']} | {row['model_id']} | "
            f"{row['effort']} | {row['units']} | {row['gate1_rounds']} | "
            f"{row['gate2_rounds']} | {row['verdicts']} |"
        )
    if omitted:
        lines.extend(["", "## Omitted", ""])
        for note in omitted:
            lines.append(f"- {note}")
        lines.append("")
    else:
        lines.append("")
    return "\n".join(lines)


def collect(root: Path) -> tuple[list[dict[str, str | int]], list[str]]:
    """Scan sprint dirs; return (rows, omission notes)."""
    rows: list[dict[str, str | int]] = []
    omitted: list[str] = []
    for sprint_dir in list_sprint_dirs(root):
        sprint_id = sprint_id_from_dir(sprint_dir)
        log_path = sprint_dir / "SPRINT_LOG.md"
        if not log_path.is_file():
            omitted.append(f"{sprint_dir.name}: no SPRINT_LOG.md")
            continue
        if sprint_id is not None and sprint_id < SKIP_BEFORE:
            omitted.append(f"{sprint_dir.name}: sprint id < {SKIP_BEFORE}")
            continue
        if not gate_tables(log_path.read_text(encoding="utf-8")):
            omitted.append(f"{sprint_dir.name}: no gate table")
            continue
        row = sprint_row(sprint_dir)
        if row is not None:
            rows.append(row)
    return rows, omitted


def main() -> int:
    """Write the ledger and return 0."""
    root = agents_root()
    rows, omitted = collect(root)
    out = root / OUT_REL
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_markdown(rows, omitted), encoding="utf-8")
    print(f"Wrote {OUT_REL} ({len(rows)} sprint rows).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
