"""Print a compact /start session briefing (≤80 lines), optionally boot.

Orchestrates existing local tools into a short English briefing for
`/agents:start`. No network. Does not read `.env`. Does not dump
`docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md`.

With ``--boot``: run drift → claim → probe → sync → bridge, then print the
briefing. Drift exit ``2`` propagates and skips claim (Sprint 039 B1).

The bridge step asks ``scripts/bridge_state.py`` whether **this** target's
mirror is missing or diverged, for every target rather than for Cursor alone
(Sprint 041). It never inspects or touches the other harness's tree.

invoked_by: workflows/start_workflow.md, make session-start, commands/start.md

Usage:
    python3 scripts/session_start.py
    python3 scripts/session_start.py --boot --tool cursor

Exit codes:
    0 — briefing printed (no --boot), or boot completed (including bridge
        PermissionError advisory — Sprint 040)
    2 — drift requires reconcile, claim refused, or non-permission bridge
        install failure (RA-11)
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from bridge_state import bridge_stale
from bridge_state import lock_stale as _bridge_lock_stale

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


def build_briefing(root: Path, tool: str | None = None) -> list[str]:
    """Assemble the briefing, including only the sections this tool needs.

    Args:
        root: Framework checkout.
        tool: Harness this session claimed. ``None`` falls back to the
            anchor's ``session_tool``, which is what a briefing-only run reads.

    Returns:
        list[str]: Briefing lines, before the line cap is applied.
    """
    state = load_anchor(root)
    effective = tool or (state or {}).get("session_tool")
    parts: list[str] = [
        "# /start briefing",
        "",
        *section_anchor(state),
        "",
        *section_drift(root),
        "",
        *section_upstream(root),
    ]
    # `make cursor-tiers` is a Cursor instrument; proposing it to a session
    # that does not run Cursor is noise the briefing's line cap pays for.
    if effective == "cursor":
        parts.extend(["", *section_chat_vs_map(root)])
    return parts


def apply_line_cap(lines: list[str], cap: int = LINE_CAP) -> list[str]:
    if len(lines) <= cap:
        return lines
    kept = lines[: cap - 1]
    kept.append(TRUNCATION_MARK)
    return kept


def _run_script(root: Path, relative: str, *args: str) -> int:
    script = root / relative
    if not script.is_file():
        print(f"boot: missing {relative}", file=sys.stderr)
        return 2
    proc = subprocess.run(
        [sys.executable, str(script), *args],
        cwd=str(root),
        check=False,
    )
    return int(proc.returncode)


def _bridge_target(tool: str) -> str | None:
    if tool == "cursor":
        return "cursor"
    if tool == "claude-code":
        return "claude"
    return None


def _lock_path(root: Path, target: str) -> Path:
    return root / f".bridge_{target}.lock"


def _lock_stale(root: Path, target: str) -> bool:
    """True when this target's lock is absent or behind ``HEAD``."""
    return _bridge_lock_stale(root, target)


def _commands_body_stale(root: Path, target: str) -> bool:
    """True when this target's bridge needs reinstalling.

    Mirror missing or incomplete, **or** rendered content diverged — the union
    `workflows/start_workflow.md` Phase 1.5 has always described. Until Sprint
    041 this returned ``False`` for every target but ``cursor``, so the Claude
    path could only ever reach the lock-only branch below and reported a
    checkout with no ``.claude/`` directory as fresh.

    The name is kept: it is the seam the suite patches, and renaming it would
    be churn without a behavioural difference.
    """
    return bridge_stale(root, target, nucleus=True)


def _refresh_bridge_lock(root: Path, target: str) -> int:
    """Write ``.bridge_<target>.lock`` to ``HEAD`` without reinstalling the mirror."""
    proc = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0 or not proc.stdout.strip():
        print(
            "boot: cannot refresh bridge lock (git rev-parse failed).",
            file=sys.stderr,
        )
        return 2
    commit = proc.stdout.strip()
    lock = _lock_path(root, target)
    lock.write_text(commit + "\n", encoding="utf-8")
    print(f"boot: bridge lock refreshed to {commit[:12]} (content fresh).")
    return 0


def _run_bridge_install(root: Path, target: str) -> tuple[int, str]:
    installer = root / "scripts" / "install.sh"
    if not installer.is_file():
        msg = "boot: scripts/install.sh missing"
        print(msg, file=sys.stderr)
        return 2, msg
    proc = subprocess.run(
        ["bash", str(installer), "--target", target],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=False,
    )
    combined = (proc.stdout or "") + (proc.stderr or "")
    if proc.stdout:
        sys.stdout.write(proc.stdout)
    if proc.stderr:
        sys.stderr.write(proc.stderr)
    return int(proc.returncode), combined


def _bridge_permission_denied(output: str) -> bool:
    lowered = output.lower()
    if "bridge: permission denied on .cursor" in lowered:
        return True
    return "permissionerror" in lowered and ".cursor" in lowered


def _bridge_triage(root: Path, target: str | None) -> tuple[int, list[str]]:
    """Repair this target's bridge, leaving every other target untouched.

    Three outcomes, unchanged in shape since Sprint 040: (a) lock stale while
    the mirror is intact → refresh the lock only; (b) mirror missing or content
    diverged → incremental install; (c) ``PermissionError`` on the mirror
    directory → advisory, boot still succeeds. What changed in Sprint 041 is
    that (b) is reachable for every target, not for Cursor alone.

    Args:
        root: Framework checkout.
        target: ``claude``, ``cursor``, or None for a harness with no bridge.

    Returns:
        tuple[int, list[str]]: exit code (``2`` stops the boot) and any
        advisory notes to fold into the briefing.
    """
    if target is None:
        return 0, []
    if _commands_body_stale(root, target):
        install_rc, install_out = _run_bridge_install(root, target)
        if install_rc == 0:
            return 0, []
        if not _bridge_permission_denied(install_out):
            print(
                f"boot: bridge install --target {target} failed "
                f"(exit {install_rc}).",
                file=sys.stderr,
            )
            return 2, []
        note = (
            f"⚠️  Bridge: PermissionError on the `{target}` mirror "
            f"(run `bash scripts/install.sh --target {target}` "
            "outside the agent sandbox)."
        )
        print(note, file=sys.stderr)
        return 0, [note]
    if _lock_stale(root, target) and _refresh_bridge_lock(root, target) != 0:
        return 2, []
    return 0, []


def run_boot(root: Path, tool: str) -> int:
    """Execute binding steps; return 2 on hard stop, else 0 after briefing."""
    drift_rc = _run_script(root, "scripts/detect_drift.py")
    if drift_rc == 2:
        print(
            "boot: drift exit 2 — run /agents:reconcile before claim.",
            file=sys.stderr,
        )
        return 2

    claim_rc = _run_script(
        root, "scripts/session_state.py", "claim", "--tool", tool
    )
    if claim_rc == 2:
        print("boot: claim refused (exit 2).", file=sys.stderr)
        return 2

    _run_script(root, "scripts/session_probe.py")  # advisory; ignore exit 1

    sync_rc = _run_script(root, "scripts/sync_agents_pin.py")
    if sync_rc == 2:
        print("boot: pin sync exit 2 — stop until clean.", file=sys.stderr)
        return 2

    target = _bridge_target(tool)
    bridge_rc, bridge_notes = _bridge_triage(root, target)
    if bridge_rc != 0:
        return bridge_rc

    briefing = apply_line_cap(build_briefing(root, tool))
    if bridge_notes:
        # Keep under LINE_CAP: insert after the title line when present.
        insert_at = 1 if briefing and briefing[0].startswith("#") else 0
        merged = briefing[:insert_at] + bridge_notes + briefing[insert_at:]
        briefing = apply_line_cap(merged)
    sys.stdout.write("\n".join(briefing) + "\n")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument(
        "--boot",
        action="store_true",
        help="Run drift→claim→probe→sync→bridge before the briefing.",
    )
    parser.add_argument(
        "--tool",
        choices=["claude-code", "cursor", "terminal"],
        default="terminal",
        help="Harness for claim/bridge when --boot (default: terminal, "
             "matching session_state.py; naming an IDE here claims the anchor "
             "as that IDE).",
    )
    args = parser.parse_args(argv)
    root = repo_root()
    if args.boot:
        return run_boot(root, args.tool)
    briefing = apply_line_cap(build_briefing(root))
    sys.stdout.write("\n".join(briefing) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
