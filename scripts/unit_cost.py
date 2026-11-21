"""Measure what each committed unit of a sprint cost, in `fresh` tokens.

Method: rule C of `docs/sprints/059-core-pipeline/TOKEN_ECONOMY_STUDY.md` section 6.4,
the rule P of section 6.2 with batch pooling. Cost is in `fresh` tokens
(`input + output + cache_creation`, ADR-0018 decision 3a); `cache_read` is excluded
because it scales with the context size, not with the difficulty of the unit.

* Units are the Work rows of `<sprint-dir>/task_scope.md` whose Status is committed;
  every short SHA in the Status cell is one commit of the unit. The `Est. cost`
  column, when present, is read for the comparison.
* Sprint commits: `git rev-list --reverse --topo-order <tip> --not <base>`, where
  `<tip>` is the unit SHA with the latest commit time.
* A turn is one API message of a main transcript or a `subagents/*.jsonl` file of
  the project directory, deduplicated by `message.id` per file, `<synthetic>`
  skipped. Its time is the timestamp of the first record for its id.
* A turn at time `t` belongs to the first commit whose commit time `ct >= t`, that
  is the interval `(ct[k-1], ct[k]]`. A turn at or before the first sprint commit,
  or after the last unit commit, is excluded. Turns of a non-unit commit are
  overhead.
* Pooling: a unit commit with an empty interval joins a pending batch. The batch is
  charged the cost of the next commit that has turns, split evenly across the
  batch's units (a unit repeated in the batch counts once).

Limits, as recorded in section 6.7 of the study:

* A pending batch absorbs the whole cost of the next commit that has turns even
  when that commit is not a unit commit; that cost is not counted as overhead.
* The even split inside a batch blurs per-unit differences.
* Overlapping subagent work is charged by time, not by task.
* Commit time stands for work time; this is unverified.
* A unit whose SHA is outside the tip's chain, or whose batch finds no commit with
  turns, is listed as unattributed.
* The turn reader keeps timestamps, which `session_cost.read_turns` drops, so only
  its project slug and field names are reused.

Advisory: exit 0 whenever something was measured, whatever the differences with
`Est. cost`. Exit 2, with one `unit_cost: error:` line on stderr, when it cannot
measure: no `task_scope.md`, no work units, no committed unit, a git failure, an
unresolved SHA, no transcript directory, or no unit attributable.

invoked_by: workflows/close_workflow.md.

Usage:
    python3 scripts/unit_cost.py --sprint-dir docs/sprints/059-core-pipeline
    python3 scripts/unit_cost.py --sprint-dir <dir> --base main --json
"""

from __future__ import annotations

import argparse
import bisect
import collections
import datetime
import json
import re
import subprocess
import sys
from collections.abc import Iterator
from pathlib import Path
from typing import NamedTuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_task_scope
from session_cost import FIELDS, PROJECTS, SYNTHETIC, project_slug

SHA = re.compile(r"\b[0-9a-f]{7,40}\b")
MAX_TRANSCRIPT_BYTES = 1 << 30


class UnitCostError(Exception):
    """The measurement cannot be made; the message is the stderr line."""


class CostUnit(NamedTuple):
    """One committed unit: id, short SHAs of its Status cell and its `Est. cost`."""

    id: str
    shas: tuple[str, ...]
    est: int | None


def _row_estimate(header: list[str], row: list[str]) -> tuple[str, int] | None:
    """(unit id, `Est. cost`) of a Work row, or None when either cell is absent or not a count."""
    if "Est. cost" not in header or "#" not in header:
        return None
    position = header.index("Est. cost")
    cost = row[position].strip() if len(row) > position else ""
    if not (cost.isascii() and cost.isdigit()):
        return None
    return row[header.index("#")], int(cost)


def parse_units(sprint_dir: Path) -> list[CostUnit]:
    """Committed units of a sprint's `task_scope.md`, with their estimates.

    Args:
        sprint_dir: directory holding `task_scope.md`.

    Returns:
        list[CostUnit]: units whose Status starts with the committed mark.

    Raises:
        UnitCostError: no file, no work unit, or no committed unit.
    """
    path = sprint_dir / "task_scope.md"
    if not path.is_file():
        raise UnitCostError(f"no task_scope.md in {sprint_dir}")
    tables = check_task_scope.work_tables(path.read_text(encoding="utf-8"))
    units = check_task_scope.work_units(tables)
    if not units:
        raise UnitCostError(f"no work units in {path}")
    estimates = dict(filter(None, (_row_estimate(h, r) for h, rows in tables for r in rows)))
    committed = [
        CostUnit(unit.id, tuple(SHA.findall(unit.status)), estimates.get(unit.id))
        for unit in units
        if unit.status.startswith("✅")
    ]
    if not committed:
        raise UnitCostError(f"no committed unit in {path}")
    return committed


def git(project: Path, *args: str) -> str:
    """Standard output of a git command run in `project`.

    Raises:
        UnitCostError: git is missing or exits non-zero.
    """
    try:
        done = subprocess.run(
            ["git", "-C", str(project), *args],
            capture_output=True, text=True, check=False,
        )
    except OSError as error:
        raise UnitCostError(f"git failed: {error}") from error
    if done.returncode != 0:
        first = (done.stderr.strip().splitlines() or ["no message"])[0]
        raise UnitCostError(f"git {args[0]} failed: {first}")
    return done.stdout


def unit_shas(units: list[CostUnit]) -> list[tuple[str, str]]:
    """(unit id, short SHA) pairs of every committed unit."""
    return [(unit.id, sha) for unit in units for sha in unit.shas]


def resolve(project: Path, units: list[CostUnit]) -> dict[str, tuple[str, int]]:
    """Full SHA and commit time of every short SHA of the units.

    Raises:
        UnitCostError: a SHA resolves to no commit.
    """
    resolved: dict[str, tuple[str, int]] = {}
    for unit_id, sha in unit_shas(units):
        try:
            out = git(project, "show", "-s", "--format=%H %ct", f"{sha}^{{commit}}")
        except UnitCostError as error:
            raise UnitCostError(f"unresolved SHA {sha} of unit {unit_id}") from error
        full, stamp = out.split()
        resolved[sha] = (full, int(stamp))
    return resolved


def sprint_commits(project: Path, tip: str, base: str) -> list[tuple[str, int]]:
    """(full SHA, commit time) of `<tip> --not <base>`, oldest first."""
    out = git(project, "rev-list", "--reverse", "--topo-order", "--format=%H %ct", tip,
              "--not", base)
    pairs = [line.split() for line in out.splitlines() if re.match(r"^[0-9a-f]{40} \d+$", line)]
    return [(full, int(stamp)) for full, stamp in pairs]


def _epoch(stamp: str) -> float | None:
    try:
        return datetime.datetime.fromisoformat(stamp.replace("Z", "+00:00")).timestamp()
    except (ValueError, AttributeError):
        return None


def _record_turn(line: str, seen: set[str]) -> tuple[float, int] | None:
    """(time, fresh) of a usage-bearing first record of a message id, or None."""
    try:
        record = json.loads(line)
    except json.JSONDecodeError:
        return None
    message = record.get("message") if isinstance(record, dict) else None
    if not isinstance(message, dict) or not message.get("usage"):
        return None
    if message.get("model") == SYNTHETIC or message.get("id") in seen:
        return None
    moment = _epoch(record.get("timestamp"))
    if moment is None:
        return None
    if message.get("id"):
        seen.add(message["id"])
    usage = message["usage"]
    inp, out, _read, created = (usage.get(field) or 0 for field in FIELDS)
    return moment, inp + out + created


def _file_turns(path: Path) -> Iterator[tuple[float, int]]:
    seen: set[str] = set()
    with path.open(encoding="utf-8", errors="replace") as handle:
        yield from filter(None, (_record_turn(line, seen) for line in handle))


def _load(path: Path, turns: list[tuple[float, int]]) -> None:
    """Append the turns of `path`; report and skip a file that cannot be read."""
    try:
        if not path.is_file() or path.stat().st_size > MAX_TRANSCRIPT_BYTES:
            print(f"unit_cost: skipped {path.name}: not a regular file or too large",
                  file=sys.stderr)
            return
        turns.extend(_file_turns(path))
    except Exception as error:  # noqa: BLE001 - one transcript must not stop the rest
        print(f"unit_cost: skipped {path.name}: {error}", file=sys.stderr)


def read_turns(directory: Path) -> list[tuple[float, int]]:
    """Turns of every main transcript and `subagents/*.jsonl`, sorted by time.

    A file that is not a regular file, is over `MAX_TRANSCRIPT_BYTES`, or fails to
    read is reported on stderr and skipped; the other files still count.
    """
    paths = sorted(directory.glob("*.jsonl")) + sorted(directory.glob("*/subagents/*.jsonl"))
    turns: list[tuple[float, int]] = []
    for path in paths:
        _load(path, turns)
    return sorted(turns)


class Attribution(NamedTuple):
    """Rule C result: unit id to [fresh, turns], overhead and excluded counts."""

    per_unit: dict[str, list[float]]
    overhead: list[int]
    excluded: int


def _charge_commits(
    commits: list[tuple[str, int]], last_unit_ct: int, turns: list[tuple[float, int]]
) -> tuple[dict[str, list[int]], int]:
    """Charge each turn to the first commit with `ct >= t`; count excluded turns."""
    cts = [ct for _, ct in commits]
    per_commit: dict[str, list[int]] = collections.defaultdict(lambda: [0, 0])
    excluded = 0
    for moment, fresh in turns:
        index = bisect.bisect_left(cts, moment)
        if moment <= cts[0] or moment > last_unit_ct or index >= len(commits):
            excluded += 1
            continue
        cell = per_commit[commits[index][0]]
        cell[0] += fresh
        cell[1] += 1
    return per_commit, excluded


def attribute(
    commits: list[tuple[str, int]],
    units_of: dict[str, list[str]],
    turns: list[tuple[float, int]],
) -> Attribution:
    """Rule C over the sprint commits (oldest first).

    Args:
        commits: (full SHA, commit time) pairs of the sprint.
        units_of: full SHA of a unit commit to the ids of its units.
        turns: (time, fresh) pairs.

    Returns:
        Attribution: per-unit [fresh, turns] (a unit with several batches sums them),
        overhead [fresh, turns] and the excluded turn count.
    """
    unit_cts = [ct for sha, ct in commits if sha in units_of]
    if not unit_cts:
        return Attribution({}, [0, 0], len(turns))
    per_commit, excluded = _charge_commits(commits, max(unit_cts), turns)
    per_unit: dict[str, list[float]] = {}
    overhead = [0, 0]
    pending: list[str] = []
    for sha, _ in commits:
        pending.extend(units_of.get(sha, []))
        cell = per_commit.get(sha)
        if not cell:
            continue
        if not pending:
            overhead[0] += cell[0]
            overhead[1] += cell[1]
            continue
        batch = list(dict.fromkeys(pending))
        for unit_id in batch:
            share = per_unit.setdefault(unit_id, [0.0, 0.0])
            share[0] += cell[0] / len(batch)
            share[1] += cell[1] / len(batch)
        pending = []
    return Attribution(per_unit, overhead, excluded)


def measure(
    units: list[CostUnit], project: Path, base: str, directory: Path
) -> dict:
    """The report for `units`: per-unit rows, unattributed ids and totals.

    Raises:
        UnitCostError: unresolved SHA, git failure, no transcripts, nothing attributable.
    """
    resolved = resolve(project, units)
    tip = max((ct, full) for full, ct in resolved.values())[1]
    commits = sprint_commits(project, tip, base)
    in_chain = {full for full, _ in commits}
    units_of: dict[str, list[str]] = collections.defaultdict(list)
    for unit_id, sha in unit_shas(units):
        if resolved[sha][0] in in_chain:
            units_of[resolved[sha][0]].append(unit_id)
    result = attribute(commits, units_of, read_turns(directory))
    rows = []
    for unit in units:
        if unit.id not in result.per_unit:
            continue
        fresh, count = result.per_unit[unit.id]
        diff = None if unit.est is None else round(fresh) - unit.est
        rows.append({"id": unit.id, "fresh": round(fresh), "turns": round(count, 1),
                     "est_cost": unit.est, "diff": diff})
    if not rows:
        raise UnitCostError("no unit could be attributed")
    return {
        "units": rows,
        "unattributed": [u.id for u in units if u.id not in result.per_unit],
        "totals": {
            "fresh": sum(row["fresh"] for row in rows),
            "turns": round(sum(row["turns"] for row in rows), 1),
            "overhead_fresh": result.overhead[0],
            "overhead_turns": result.overhead[1],
            "excluded_turns": result.excluded,
        },
    }


def _number(value: float) -> str:
    return f"{value:g}" if isinstance(value, float) else str(value)


def render(report: dict) -> list[str]:
    """Text lines: one per unit, the totals line and the unattributed line."""
    lines = []
    for row in report["units"]:
        line = f"{row['id']}  fresh={row['fresh']}  turns={row['turns']:g}"
        if row["est_cost"] is not None:
            line += f"  est={row['est_cost']}  diff={row['diff']:+d}"
        lines.append(line)
    totals = report["totals"]
    lines.append("total  " + "  ".join(f"{key}={_number(value)}" for key, value in totals.items()))
    missing = report["unattributed"]
    lines.append(f"unattributed={len(missing)}" + (f"  ids={','.join(missing)}" if missing else ""))
    return lines


def main() -> int:
    """Measure a sprint's per-unit cost; advisory unless it cannot measure."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--sprint-dir", type=Path, required=True)
    parser.add_argument("--base", default="main")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument("--project", type=Path, default=Path.cwd(),
                        help="repository holding the sprint commits (default: cwd)")
    parser.add_argument("--projects-dir", type=Path, default=PROJECTS,
                        help="directory of Claude Code project transcripts")
    args = parser.parse_args()
    try:
        units = parse_units(args.sprint_dir)
        directory = args.projects_dir / project_slug(args.project)
        if not directory.is_dir():
            raise UnitCostError(f"no transcript directory {directory}")
        report = measure(units, args.project, args.base, directory)
    except UnitCostError as error:
        print(f"unit_cost: error: {error}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2) if args.json else "\n".join(render(report)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
