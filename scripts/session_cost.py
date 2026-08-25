"""Measure what a session cost, from transcripts already on disk.

`rules/token_economy.md` governs what goes into a prompt and `loop_governance.md`
bounds `/loop` iterations, but nothing measured what a session actually spent —
so the token budget in `loop_governance.md` was declared advisory with this
reason: *"no agent reads its own spend reliably, and making it binding would
force a field nobody can fill truthfully"*. That premise stops being true here.
Spend is read from the transcript, not self-declared.

**Zero network, zero credentials, zero dependencies.** Claude Code already writes
`~/.claude/projects/<slug>/<session-uid>.jsonl` with a `usage` block per message,
carrying `input_tokens`, `output_tokens`, `cache_read_input_tokens` and
`cache_creation_input_tokens`, alongside the model that produced them.

**A session is a sawtooth, and that is the whole point of this script.** An
earlier measurement of this repository reported cost growing monotonically with
message position — quartiles of 7/15/23/54%. Re-measured over a full session the
quartiles are 157K/681K/245K/485K, because compaction resets the context window.
The first measurement covered only the first cycle, at a scope never declared.

So the unit is the **context cycle**, not the session: cost is the area under the
sawtooth, and compaction resets the x axis without reducing that area. Measured
across four cycles of one session — peaks of 849K, 995K, 361K and 631K against a
reset point of ~22K — the cycle that cost most per message was the *shortest*:
113 messages reached 995K and spent 99.5M, nearly matching a 414-message cycle.
**Cost tracks peak height, not message count.**

Reported in tokens, never in currency. The per-family price ratio belongs to
`config/model_tiers.json`, which is what needs it to compare families; a price
copied here would be stale the day it was written, which is the defect this whole
program pursues.

invoked_by: scripts/session_probe.py, rules/token_economy.md#session_bound.

Usage:
    python3 scripts/session_cost.py                 # newest session, this project
    python3 scripts/session_cost.py --session <uid>
    python3 scripts/session_cost.py --json

Exit codes:
    0 — measured, or nothing measurable and said so
    1 — the named session does not exist
"""

import argparse
import json
import sys
from pathlib import Path

PROJECTS = Path.home() / ".claude" / "projects"

# A context reset shows as a collapse in cache_read: the window was rebuilt from
# a summary. Both bounds matter — the floor keeps ordinary small turns early in a
# cycle from registering as resets, and the ratio keeps normal variation out.
RESET_FLOOR = 100_000
RESET_RATIO = 0.5

SYNTHETIC = "<synthetic>"
FIELDS = ("input_tokens", "output_tokens",
          "cache_read_input_tokens", "cache_creation_input_tokens")


def project_slug(path: Path) -> str:
    """Claude Code's directory name for a project path."""
    return str(path.resolve()).replace("/", "-").replace(".", "-")


def read_turns(transcript: Path) -> tuple[list[dict], int]:
    """Every usage-bearing turn in a transcript, and how many were synthetic.

    Args:
        transcript: path to a `<session-uid>.jsonl` file.

    Returns:
        tuple: (turns as dicts with `model` plus the four token fields,
            count of `<synthetic>` entries skipped).
    """
    turns, skipped = [], 0
    for line in transcript.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        message = record.get("message") or {}
        usage = message.get("usage")
        if not usage:
            continue
        model = message.get("model", "unknown")
        if model == SYNTHETIC:
            # Not an API call: counting these inflates every total.
            skipped += 1
            continue
        turn = {"model": model}
        turn.update({field: usage.get(field, 0) for field in FIELDS})
        turns.append(turn)
    return turns, skipped


def segment_cycles(turns: list[dict]) -> list[list[dict]]:
    """Split turns into context cycles at each window reset.

    Compaction rebuilds the window from a summary, so `cache_read` collapses.
    Measuring a bound against the *session's* first turn would therefore stop
    firing after the first reset; the cycle is the unit that keeps meaning.

    Args:
        turns: usage-bearing turns in transcript order.

    Returns:
        list: one list of turns per cycle, in order.
    """
    if not turns:
        return []
    cuts = [0]
    for index in range(1, len(turns)):
        previous = turns[index - 1]["cache_read_input_tokens"]
        current = turns[index]["cache_read_input_tokens"]
        if previous > RESET_FLOOR and current < previous * RESET_RATIO:
            cuts.append(index)
    cuts.append(len(turns))
    return [turns[a:b] for a, b in zip(cuts, cuts[1:]) if b > a]


def cycle_summary(cycle: list[dict]) -> dict:
    """First turn, peak, ratio and totals for one context cycle."""
    reads = [turn["cache_read_input_tokens"] for turn in cycle]
    first, peak = reads[0], max(reads)
    return {
        "messages": len(cycle),
        "first_turn": first,
        "peak": peak,
        "ratio": round(peak / first, 1) if first else None,
        **{field: sum(turn[field] for turn in cycle) for field in FIELDS},
    }


def by_model(turns: list[dict]) -> dict[str, dict]:
    """Token totals per model, which is what tier decisions are compared against."""
    totals: dict[str, dict] = {}
    for turn in turns:
        entry = totals.setdefault(turn["model"], dict.fromkeys(FIELDS, 0))
        for field in FIELDS:
            entry[field] += turn[field]
    return totals


def measure(transcript: Path) -> dict:
    """Full measurement of one transcript.

    Returns:
        dict: `measurable` False when the transcript carries no usage data —
            stated rather than returned as zero, because a silent zero reads as
            "this session was free".
    """
    turns, skipped = read_turns(transcript)
    if not turns:
        return {"session": transcript.stem, "measurable": False,
                "reason": "no usage data in this transcript", "synthetic_skipped": skipped}
    cycles = [cycle_summary(cycle) for cycle in segment_cycles(turns)]
    return {
        "session": transcript.stem,
        "measurable": True,
        "messages": len(turns),
        "synthetic_skipped": skipped,
        "cycles": cycles,
        "by_model": by_model(turns),
        "totals": {field: sum(turn[field] for turn in turns) for field in FIELDS},
    }


def measure_previous(
    project: Path,
    *,
    exclude_session: str | None = None,
    session_tool: str | None = None,
) -> dict | None:
    """The most recent completed session for a project, for `session_probe.py`.

    Args:
        project: Repository root (used to locate Claude Code transcripts).
        exclude_session: Live session UID to skip — otherwise the probe measures
            the session that is asking (Sprint 023 unrouted finding).
        session_tool: Harness from the anchor (`claude-code` | `cursor` |
            `terminal`). Claude Code transcripts live under
            ``~/.claude/projects/``. When ``session_tool`` is ``cursor``, those
            files are not this session's spend — return None rather than a
            foreign Claude measurement.

    Returns:
        dict | None: Measurement, or None when nothing measurable exists.
    """
    if session_tool == "cursor":
        return None
    directory = PROJECTS / project_slug(project)
    if not directory.is_dir():
        return None
    transcripts = sorted(directory.glob("*.jsonl"), key=lambda p: p.stat().st_mtime)
    if exclude_session:
        skip = {exclude_session, f"{exclude_session}.jsonl"}
        transcripts = [path for path in transcripts if path.name not in skip
                       and path.stem != exclude_session]
    return measure(transcripts[-1]) if transcripts else None


def render(result: dict) -> None:
    """Print a measurement in tokens. Never in currency — see the module docstring."""
    if not result["measurable"]:
        print(f"⚠️  Cannot measure {result['session']}: {result['reason']}.")
        print("   Reporting this rather than zero: a silent zero reads as free.")
        return

    print(f"📊 Session {result['session']} — {result['messages']} turns"
          + (f", {result['synthetic_skipped']} synthetic skipped"
             if result["synthetic_skipped"] else ""))

    print(f"\n  {'cycle':<7}{'msgs':>6}{'first':>12}{'peak':>12}{'ratio':>8}{'cache_read':>16}")
    for number, cycle in enumerate(result["cycles"], start=1):
        print(f"  {number:<7}{cycle['messages']:>6}{cycle['first_turn']:>12,}"
              f"{cycle['peak']:>12,}{cycle['ratio'] or 0:>7}x"
              f"{cycle['cache_read_input_tokens']:>16,}")

    print(f"\n  {'model':<24}{'output':>14}{'cache_read':>16}{'cache_write':>14}")
    for model, totals in sorted(result["by_model"].items()):
        print(f"  {model:<24}{totals['output_tokens']:>14,}"
              f"{totals['cache_read_input_tokens']:>16,}"
              f"{totals['cache_creation_input_tokens']:>14,}")

    peak_ratio = max((c["ratio"] or 0) for c in result["cycles"])
    print(f"\n  Highest cycle ratio: {peak_ratio}x. Cost is the area under the sawtooth —"
          f"\n  compaction resets the axis without reducing it.")


def find_transcript(session: str | None, project: Path) -> Path | None:
    """The named session's transcript, or the newest one for this project."""
    directory = PROJECTS / project_slug(project)
    if not directory.is_dir():
        return None
    if session:
        candidate = directory / f"{session}.jsonl"
        return candidate if candidate.exists() else None
    transcripts = sorted(directory.glob("*.jsonl"), key=lambda p: p.stat().st_mtime)
    return transcripts[-1] if transcripts else None


def load_anchor(project: Path) -> dict:
    """Parse ``docs/active_state.json`` if present; else empty dict."""
    path = project / "docs" / "active_state.json"
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def main() -> int:
    """Measure a session and report it in tokens, per context cycle."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--session", help="session UID; default is the newest")
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument(
        "--from-anchor",
        action="store_true",
        help="Measure previous session using active_state.json (excludes live id; "
             "skips when session_tool is cursor)",
    )
    args = parser.parse_args()

    if args.from_anchor:
        state = load_anchor(args.project)
        result = measure_previous(
            args.project,
            exclude_session=state.get("session_id"),
            session_tool=state.get("session_tool"),
        )
        if result is None:
            payload = {"measurable": False, "reason": "no prior Claude transcript",
                       "session_tool": state.get("session_tool")}
            if args.json:
                print(json.dumps(payload, indent=2))
            else:
                print("⚠️  No prior Claude transcript to measure "
                      f"(session_tool={state.get('session_tool')!r}).")
            return 0
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            render(result)
        return 0

    transcript = find_transcript(args.session, args.project)
    if transcript is None:
        target = args.session or f"any session for {args.project}"
        print(f"⚠️  No transcript found for {target}.", file=sys.stderr)
        return 1

    result = measure(transcript)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        render(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
