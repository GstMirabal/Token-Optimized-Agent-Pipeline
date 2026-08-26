"""Print a compact /start session briefing (≤80 lines).

Orchestrates existing local tools into a short English briefing for
`/agents:start`. No network. Does not read `.env`. Does not dump
`docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md`.

invoked_by: workflows/start_workflow.md, make session-start

Usage:
    python3 scripts/session_start.py

Exit codes:
    0 — briefing printed (always; drift/findings are reported, not fatal)
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

LINE_CAP = 80
DRIFT_OUTPUT_LINES = 15
TRUNCATION_MARK = "… truncated (session_start line cap)"


def repo_root() -> Path:
    """Repository root as the parent of ``scripts/`` (nucleus-friendly)."""
    return Path(__file__).resolve().parent.parent


def load_anchor(root: Path) -> dict[str, object] | None:
    path = root / "docs" / "active_state.json"
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def section_anchor(state: dict[str, object] | None) -> list[str]:
    lines = ["## Session / anchor"]
    if state is None:
        lines.append("docs/active_state.json: absent or unreadable")
        return lines
    sprint = state.get("current_sprint")
    sprint_id: object = "(none)"
    if isinstance(sprint, dict):
        sprint_id = sprint.get("id", "(none)")
    lines.extend(
        [
            f"status: {state.get('status', '(none)')}",
            f"session_id: {state.get('session_id', '(none)')}",
            f"current_sprint.id: {sprint_id}",
            f"session_tool: {state.get('session_tool', '(none)')}",
            f"delegation_mode: {state.get('delegation_mode', '(none)')}",
        ]
    )
    return lines


def section_drift(root: Path) -> list[str]:
    lines = ["## Drift"]
    script = root / "scripts" / "detect_drift.py"
    if not script.is_file():
        lines.append("scripts/detect_drift.py: missing")
        return lines
    try:
        proc = subprocess.run(
            [sys.executable, str(script)],
            cwd=str(root),
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as exc:
        lines.append(f"detect_drift failed to spawn: {exc}")
        return lines
    lines.append(f"exit: {proc.returncode}")
    combined = (proc.stdout or "") + (proc.stderr or "")
    body = [ln for ln in combined.splitlines() if ln.strip()]
    if not body:
        lines.append("(no output)")
        return lines
    for ln in body[:DRIFT_OUTPUT_LINES]:
        lines.append(ln[:200])
    if len(body) > DRIFT_OUTPUT_LINES:
        lines.append(f"… ({len(body) - DRIFT_OUTPUT_LINES} more drift lines omitted)")
    return lines


def section_upstream(root: Path) -> list[str]:
    lines = ["## Open upstream findings"]
    path = root / "docs" / "audits" / "UPSTREAM_FINDINGS_FROM_HOSTS.md"
    if not path.is_file():
        lines.append(
            "UPSTREAM_FINDINGS_FROM_HOSTS.md absent — "
            "see Status tables; open set empty as of last closed sprint"
        )
        return lines
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        lines.append(f"unreadable: {exc}")
        return lines
    file_lines = text.count("\n") + (0 if text.endswith("\n") or not text else 1)
    open_rows = _still_open_rows_from_latest_status(text)
    lines.append(f"file lines: {file_lines} — do not load full UPSTREAM at start")
    lines.append(f"| **Still open** | rows (non-empty): {open_rows}")
    return lines


_STATUS_SPRINT = re.compile(r"^\*\*Status at Sprint (\d+)\b", re.MULTILINE)


def _still_open_rows_from_latest_status(text: str) -> int:
    """Count Still-open rows in the Status table with the highest sprint id.

    Historical Status snapshots keep closed findings visible; summing them
    inflates the /start briefing (Sprint 038 M1). No Status table → 0.
    """
    matches = list(_STATUS_SPRINT.finditer(text))
    if not matches:
        return 0
    best_i = max(range(len(matches)), key=lambda i: int(matches[i].group(1)))
    start = matches[best_i].end()
    end = matches[best_i + 1].start() if best_i + 1 < len(matches) else len(text)
    span = text[start:end]
    open_rows = 0
    for raw in span.splitlines():
        if "| **Still open" not in raw:
            continue
        cells = [c.strip() for c in raw.split("|")]
        value = cells[2] if len(cells) >= 3 else ""
        if not value or "*(none" in value.lower():
            continue
        open_rows += 1
    return open_rows


def section_chat_vs_map(root: Path) -> list[str]:
    lines = ["## Chat vs map (Cursor tiers)"]
    path = root / "config" / "model_tiers.json"
    if not path.is_file():
        lines.append("config/model_tiers.json: missing")
        return lines
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        lines.append(f"unreadable: {exc}")
        return lines
    author_model: object = "(unset)"
    tiers = data.get("tiers") if isinstance(data, dict) else None
    if isinstance(tiers, dict):
        author = tiers.get("author")
        if isinstance(author, dict):
            cursor = author.get("cursor")
            if isinstance(cursor, dict):
                author_model = cursor.get("model", "(unset)")
    lines.append(f"map author (cursor): {author_model}")
    lines.append(
        "Applied chat model may differ from the map — run `make cursor-tiers`."
    )
    return lines


def build_briefing(root: Path) -> list[str]:
    state = load_anchor(root)
    parts: list[str] = [
        "# /start briefing",
        "",
        *section_anchor(state),
        "",
        *section_drift(root),
        "",
        *section_upstream(root),
        "",
        *section_chat_vs_map(root),
    ]
    return parts


def apply_line_cap(lines: list[str], cap: int = LINE_CAP) -> list[str]:
    if len(lines) <= cap:
        return lines
    kept = lines[: cap - 1]
    kept.append(TRUNCATION_MARK)
    return kept


def main() -> int:
    root = repo_root()
    briefing = apply_line_cap(build_briefing(root))
    sys.stdout.write("\n".join(briefing) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
