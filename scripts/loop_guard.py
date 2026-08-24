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
    python3 scripts/loop_guard.py check
    python3 scripts/loop_guard.py start --max-iterations N [--success "<condition>"]

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
TASK_SCOPE = Path("task_scope.md")
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


def status_hash() -> str:
    """Fingerprint of the Status column, so 'nothing moved' is measurable."""
    if not TASK_SCOPE.exists():
        return ""
    statuses = [line for line in TASK_SCOPE.read_text(encoding="utf-8").splitlines()
                if line.startswith("|")]
    return hashlib.sha256("\n".join(statuses).encode()).hexdigest()[:16]


def start(max_iterations: int, success_condition: str) -> int:
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
        "last_status_hash": status_hash(),
        "stagnant_iterations": 0,
        "last_updated": now(),
    }
    save_state(state)
    print(f"✅ Loop armed: max {max_iterations} iterations, success = {success_condition}")
    return 0


def check() -> int:
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

    sha, statuses = head_sha(), status_hash()
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
    sub.add_parser("check", help="Advance one iteration and enforce the stops.")
    start_parser = sub.add_parser("start", help="Arm the loop with its stop set.")
    start_parser.add_argument("--max-iterations", type=int, required=True)
    start_parser.add_argument("--success", default="", help="Machine-checkable success condition.")

    args = parser.parse_args()
    if args.command == "start":
        return start(args.max_iterations, args.success)
    return check()


if __name__ == "__main__":
    sys.exit(main())
