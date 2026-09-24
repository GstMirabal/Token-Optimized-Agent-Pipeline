"""Enforce the stop conditions of an unattended loop, and fail closed.

**Host-scoped**: the root is the project being worked, not the framework. The
loop block and the sprint it measures progress against belong to the host, so
this script MUST NOT adopt `scripts/_root.py` (Sprint 023 `C0.3`).

`pipeline_workflow.md` allowed `/loop` to wrap Phases 6-8 in a single line of
boundary text: it may not wrap the Approval Gate. That is where the governance
ended. Nothing capped iterations, nothing detected a loop making no progress,
and nothing could halt one that was burning turns without advancing.

**Fail-closed is the whole design.** If the `loop` block is missing, incomplete
or stale, this exits `2`. An agent that forgets to increment the counter does
not get a free pass — it gets a stop. The alternative was the PR #28 defect:
a guard that computes a verdict and consults it only when convenient.

Progress is measured from artifacts that already exist, so nothing new has to
be trusted: a new commit on the sprint branch, or a change in the `Status`
column of `task_scope.md`. Two consecutive iterations with neither is not
progress, whatever the transcript says.

invoked_by: pipeline_workflow.md#loop_guard (first action of every iteration).

Usage:
    python3 scripts/loop_guard.py check [--sprint-dir DIR]
    python3 scripts/loop_guard.py start --max-iterations N [--success "<condition>"]
        [--sprint-dir DIR]

``--sprint-dir`` names the directory holding ``task_scope.md``; omitted, it comes
from the anchor's ``current_sprint.path``. Same flag as the sibling checks
``check_task_scope.py`` and ``check_forge_ladder.py``.

Exit codes:
    0 — the loop may continue
    2 — a binding stop was reached, or the loop state is untrustworthy
"""

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ACTIVE_STATE = Path("docs/active_state.json")
TASK_SCOPE_NAME = "task_scope.md"
REQUIRED_FIELDS = ("iteration", "max_iterations", "success_condition")


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_state() -> dict:
    if not ACTIVE_STATE.exists():
        return {}
    try:
        return json.loads(ACTIVE_STATE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def save_state(state: dict) -> None:
    ACTIVE_STATE.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def head_sha() -> str:
    result = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else ""


def task_scope_path(sprint_dir: str | None = None) -> Path:
    """Where this sprint's ``task_scope.md`` is, host-scoped.

    ``agents.md §5 mandatory_topology`` puts it inside the sprint directory,
    ``docs/sprints/[Sprint_ID]-[Stack]-[Layer]/``, and the anchor's
    ``current_sprint.path`` names that directory. A bare ``Path("task_scope.md")``
    resolved to the repository root instead, where the file does not exist in any
    host — and ``status_hash`` returns ``""`` for a missing file, so the failure
    was **silent**: the fingerprint was empty on every iteration, which means the
    Status-column half of the progress signal never fired. A guard that cannot
    see movement cannot see its absence either, and fail-closed is the whole
    design of this script.

    Resolved without ``scripts/_root.py``: this script is host-scoped by charter
    (Sprint 023 ``C0.3``), and the sprint belongs to the host, not the framework.

    Args:
        sprint_dir: explicit override, the ``--sprint-dir`` of this script's
            siblings ``check_task_scope.py`` and ``check_forge_ladder.py``.

    Returns:
        Path: the sprint directory's file when one is named, else the
        repository-root path, which keeps the pre-Sprint-051 behaviour for a
        repository that really does keep it there.
    """
    if sprint_dir:
        return Path(sprint_dir) / TASK_SCOPE_NAME
    declared = (load_state().get("current_sprint") or {}).get("path")
    if declared:
        candidate = Path(declared) / TASK_SCOPE_NAME
        if candidate.exists():
            return candidate
    return Path(TASK_SCOPE_NAME)


def status_hash(sprint_dir: str | None = None) -> str:
    """Fingerprint of the Status column, so 'nothing moved' is measurable."""
    path = task_scope_path(sprint_dir)
    if not path.exists():
        return ""
    statuses = [line for line in path.read_text(encoding="utf-8").splitlines()
                if line.startswith("|")]
    return hashlib.sha256("\n".join(statuses).encode()).hexdigest()[:16]


def start(max_iterations: int, success_condition: str,
          sprint_dir: str | None = None) -> int:
    """Declare the stop set before the first iteration runs."""
    if not success_condition:
        print("❌ A loop needs a machine-checkable success condition declared up "
              "front. Without one the agent grades its own work and the loop is "
              "not a loop.", file=sys.stderr)
        return 2

    state = load_state()
    state["loop"] = {
        "iteration": 0,
        "max_iterations": max_iterations,
        "success_condition": success_condition,
        "last_commit_sha": head_sha(),
        "last_status_hash": status_hash(sprint_dir),
        "stagnant_iterations": 0,
        "last_updated": now(),
    }
    save_state(state)
    print(f"✅ Loop armed: max {max_iterations} iterations, success = {success_condition}")
    return 0


def check(sprint_dir: str | None = None) -> int:
    """Advance the counter and decide whether the loop may continue."""
    state = load_state()
    loop = state.get("loop")

    if not loop or any(field not in loop for field in REQUIRED_FIELDS):
        print("❌ No usable `loop` block in the state anchor. Arm the loop first "
              "with `loop_guard.py start --max-iterations N --success \"...\"`.\n"
              "   Failing closed is deliberate: an unbounded loop that runs "
              "because its guard could not read its own state is the failure "
              "this guard exists to prevent.", file=sys.stderr)
        return 2

    iteration = loop["iteration"] + 1
    if iteration > loop["max_iterations"]:
        print(f"❌ Iteration cap reached ({loop['max_iterations']}). Stopping.\n"
              f"   Success condition was: {loop['success_condition']}", file=sys.stderr)
        return 2

    sha, statuses = head_sha(), status_hash(sprint_dir)
    moved = sha != loop.get("last_commit_sha") or statuses != loop.get("last_status_hash")
    # This check runs at the START of an iteration, so the first one compares
    # against the baseline written by `start` before any work could happen.
    # Counting it as stagnation would stop the loop after a single unproductive
    # iteration, not the two the rule specifies.
    stagnant = 0 if (moved or iteration == 1) else loop.get("stagnant_iterations", 0) + 1

    loop.update({
        "iteration": iteration,
        "last_commit_sha": sha,
        "last_status_hash": statuses,
        "stagnant_iterations": stagnant,
        "last_updated": now(),
    })
    state["loop"] = loop
    save_state(state)

    if stagnant >= 2:
        print(f"❌ No progress for {stagnant} consecutive iterations: no new commit "
              f"on the sprint branch and no change in the task_scope.md Status "
              f"column. Stopping.\n"
              f"   A loop that repeats without advancing burns budget and "
              f"produces confidence, not work.", file=sys.stderr)
        return 2

    print(f"✅ Iteration {iteration}/{loop['max_iterations']}"
          f"{' (no progress last round)' if stagnant else ''}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    # Both subcommands take --sprint-dir, matching this script's siblings
    # `check_task_scope.py` and `check_forge_ladder.py`. Omitted, the sprint
    # directory comes from the anchor's `current_sprint.path`.
    scope_help = "Sprint directory holding task_scope.md; default: the anchor's."
    # `--current-sprint` is not an alias for the default. The default falls back
    # to the repository root when the anchor names no sprint; this flag refuses
    # to, which is the fail-closed behaviour this script is built on. A caller
    # who means "the sprint the anchor names" should get a stop, not a silent
    # fingerprint of a file that is not there.
    current_help = "Require the anchor to name a sprint; fail closed if it does not."
    for name, helptext in (("check", "Advance one iteration and enforce the stops."),
                           ("start", "Arm the loop with its stop set.")):
        sub_parser = sub.add_parser(name, help=helptext)
        sub_parser.add_argument("--sprint-dir", default=None, help=scope_help)
        sub_parser.add_argument("--current-sprint", action="store_true",
                                help=current_help)
        if name == "start":
            sub_parser.add_argument("--max-iterations", type=int, required=True)
            sub_parser.add_argument("--success", default="",
                                    help="Machine-checkable success condition.")

    args = parser.parse_args()
    sprint_dir = args.sprint_dir
    if args.current_sprint:
        if sprint_dir:
            print("❌ --current-sprint and --sprint-dir name the same thing two "
                  "ways. Pass one.", file=sys.stderr)
            return 2
        sprint_dir = (load_state().get("current_sprint") or {}).get("path")
        if not sprint_dir:
            print("❌ --current-sprint was passed and the anchor names no sprint "
                  "(`current_sprint.path`). Refusing to fall back to the "
                  "repository root: a loop measuring progress from a file that is "
                  "not there reads every iteration as stagnant.", file=sys.stderr)
            return 2
        # Naming a path is not having one. Gate 2 reached the original defect
        # straight through this flag: the anchor named a directory that did not
        # exist, `status_hash` returned "" as it does for any missing file, and the
        # loop reported "no change in the Status column" for three iterations
        # instead of "task_scope.md not found".
        declared = Path(sprint_dir) / TASK_SCOPE_NAME
        if not declared.exists():
            print(f"❌ --current-sprint resolved to {declared}, which does not "
                  f"exist. The anchor names a sprint whose task_scope.md is not "
                  f"there, so progress cannot be measured from it — and an "
                  f"unmeasurable loop must stop, not read as stagnant.",
                  file=sys.stderr)
            return 2

    if args.command == "start":
        return start(args.max_iterations, args.success, sprint_dir)
    return check(sprint_dir)


if __name__ == "__main__":
    sys.exit(main())
