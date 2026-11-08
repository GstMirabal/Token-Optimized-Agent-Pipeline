"""Count the permission decisions a Claude Code transcript records.

Sprint 059 decision D4: authorizations are counted from transcripts by a
deterministic script, not self-declared.

**What the transcript records (measured, Sprint 059 unit B-01).** Every tool
result is a `user` record that carries a `permissionDecision` object next to the
`tool_result` block: `{"decision": "accept", "source": <who>, ...}`. Across the
sessions measured, `decision` was always `"accept"` and `source` was one of
`config` (an allow rule or the permission mode answered, no human) or
`user_temporary` (a human answered a prompt; newer records add
`grantScope: "once"` and a `reasonCode`).

**What it cannot show.** A tool call the human *rejected* leaves no
`permissionDecision` record, and neither does a call that never ran. The
transcript therefore holds approvals only: this script does not report a
"denied" count and never calls a partial number "authorizations". Tool uses
with no recorded decision are reported as `tool_uses_without_decision`, which
is an upper bound on rejections plus unresolved calls, not a rejection count.

Counted keys:

- `tool_use_total`: distinct `tool_use` block ids in `assistant` records.
- `decisions_user_approved`: decisions with `source == "user_temporary"`.
- `decisions_user_approved_once`: the subset with `grantScope == "once"`.
- `decisions_by_config`: decisions with `source == "config"`.
- `decisions_other_source`: decisions with any other `source`.
- `tool_uses_without_decision`: `tool_use` ids with no recorded decision.

A `message.id` repeats across the records one API response is split into, so
tool uses are keyed by `tool_use` block id and decisions by `tool_use_id`.

invoked_by: workflows/close_workflow.md (advisory step, Sprint 059 unit B-07).

Usage:
    python3 scripts/prompt_count.py --session <uid> [--json]

Exit codes:
    0 - counted
    2 - transcript missing or unreadable
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

from session_cost import find_transcript

LOG = logging.getLogger("prompt_count")
USER_SOURCE = "user_temporary"
CONFIG_SOURCE = "config"


def _blocks(record: dict) -> list[dict]:
    """Content blocks of a record's message, or an empty list.

    Args:
        record: one parsed transcript line.

    Returns:
        list: dict blocks only; strings and malformed content are dropped.
    """
    message = record.get("message")
    content = message.get("content") if isinstance(message, dict) else None
    if not isinstance(content, list):
        return []
    return [block for block in content if isinstance(block, dict)]


def parse_records(text: str) -> list[dict]:
    """Parse JSONL text, skipping lines that are not JSON objects.

    Args:
        text: transcript file contents.

    Returns:
        list: parsed records in file order.
    """
    records = []
    for line in text.splitlines():
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            LOG.warning("skipped a malformed transcript line")
            continue
        if isinstance(record, dict):
            records.append(record)
    return records


def _record_ids(record: dict) -> tuple[set[str], dict[str, dict]]:
    """Tool-use ids and decisions found in one record.

    Args:
        record: one parsed transcript line.

    Returns:
        tuple: (`tool_use` ids, decision dict keyed by `tool_use_id`).
    """
    uses: set[str] = set()
    decided: dict[str, dict] = {}
    decision = record.get("permissionDecision")
    is_assistant = record.get("type") == "assistant"
    for block in _blocks(record):
        kind = block.get("type")
        if is_assistant and kind == "tool_use":
            uses.add(str(block.get("id")))
        if isinstance(decision, dict) and kind == "tool_result":
            decided[str(block.get("tool_use_id"))] = decision
    return uses, decided


def collect(records: list[dict]) -> tuple[set[str], dict[str, dict]]:
    """Tool-use ids and the permission decision recorded per tool-use id.

    Args:
        records: parsed transcript records.

    Returns:
        tuple: (distinct `tool_use` ids, decision dict keyed by `tool_use_id`).
    """
    tool_uses: set[str] = set()
    decisions: dict[str, dict] = {}
    for record in records:
        uses, decided = _record_ids(record)
        tool_uses |= uses
        decisions.update(decided)
    return tool_uses, decisions


def count_records(records: list[dict], session: str) -> dict:
    """Counts for one session; see the module docstring for each key.

    Args:
        records: parsed transcript records.
        session: session id to report.

    Returns:
        dict: `session` plus the counted keys.
    """
    tool_uses, decisions = collect(records)
    values = list(decisions.values())
    user = [d for d in values if d.get("source") == USER_SOURCE]
    config = [d for d in values if d.get("source") == CONFIG_SOURCE]
    return {
        "session": session,
        "tool_use_total": len(tool_uses),
        "decisions_user_approved": len(user),
        "decisions_user_approved_once": sum(1 for d in user if d.get("grantScope") == "once"),
        "decisions_by_config": len(config),
        "decisions_other_source": len(values) - len(user) - len(config),
        "tool_uses_without_decision": len(tool_uses - decisions.keys()),
    }


def count_transcript(transcript: Path) -> dict:
    """Read one transcript file and count it.

    Args:
        transcript: path to a `<session-uid>.jsonl` file.

    Returns:
        dict: as `count_records`.

    Raises:
        OSError: the file cannot be read.
    """
    text = transcript.read_text(encoding="utf-8", errors="replace")
    return count_records(parse_records(text), transcript.stem)


def render(result: dict) -> None:
    """Print the counts as `key: value` lines.

    Args:
        result: a `count_records` return value.
    """
    for key, value in result.items():
        print(f"{key}: {value}")


def main(argv: list[str] | None = None) -> int:
    """Count one session's recorded permission decisions.

    Args:
        argv: arguments; defaults to `sys.argv[1:]`.

    Returns:
        int: 0 counted, 2 transcript missing or unreadable.
    """
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--session", help="session UID; default is the newest")
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args(argv)
    try:
        transcript = find_transcript(args.session, args.project)
        if transcript is None:
            target = args.session or f"any session for {args.project.name}"
            print(f"No transcript found for {target}.", file=sys.stderr)
            return 2
        result = count_transcript(transcript)
    except Exception as error:  # noqa: BLE001 - total fault boundary: any failure is exit 2, logged
        LOG.error("cannot read transcript: %s", error)
        print(f"Cannot read transcript: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2)) if args.json else render(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
