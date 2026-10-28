"""Extract a Phase 1 plan draft into the sprint's `IMPLEMENTATION_PLAN.md`.

invoked_by: workflows/pipeline_workflow.md.

**Host-scoped**: the root is the process working directory, the project being
worked. `docs/active_state.json` and the sprint directory belong to that
project, so this script MUST NOT adopt `scripts/_root.py` `agents_root()`
(same scoping as `scripts/detect_drift.py`).

Why it exists: `pipeline_workflow.md` Phase 3 says to extract Phase 1's plan
into `IMPLEMENTATION_PLAN.md` and commit it, and nothing performed the
extraction. A draft left in `docs/plans/` or `~/.cursor/plans/` can be lost to
ephemeral storage (`agents.md §0`, Implementation Plan row).

Usage: `python3 scripts/extract_plan.py <source> [--sprint-dir <dir>]`.
Without `--sprint-dir`, `current_sprint.path` is read from
`docs/active_state.json`. The destination is `<sprint-dir>/IMPLEMENTATION_PLAN.md`.

Behaviour:

| Situation | Result |
| :--- | :--- |
| Destination absent | Copy the source; the sprint directory is created if missing, because Phase 3 instantiates it. Exit 0, print the destination |
| Destination byte-identical to the source | Write nothing, print that nothing changed. Exit 0 |
| Destination exists and differs | Write nothing, exit 2, name both paths; reconcile by hand. Never overwritten |
| Source missing or not a file, source equals destination, anchor missing, malformed or without `current_sprint.path` | Write nothing, exit 2 |

Fail-closed on error in the `agents.md §1 fail_closed_claims` sense only; no
coverage claim is made.
"""

from __future__ import annotations

import argparse
import filecmp
import json
import shutil
import sys
from pathlib import Path

ACTIVE_STATE = Path("docs/active_state.json")
PLAN_NAME = "IMPLEMENTATION_PLAN.md"


def fail(message: str) -> int:
    """Print an error to stderr.

    Args:
        message: Text to report.

    Returns:
        The blocking exit code, 2.
    """
    print(f"extract_plan: {message}", file=sys.stderr)
    return 2


def sprint_dir_from_anchor() -> Path:
    """Read `current_sprint.path` from the anchor under the cwd.

    Returns:
        The sprint directory named by the anchor.

    Raises:
        ValueError: The anchor is missing, malformed or lacks the field.
    """
    try:
        data = json.loads(ACTIVE_STATE.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ValueError(f"cannot read {ACTIVE_STATE}: {exc}") from exc
    sprint = data.get("current_sprint") if isinstance(data, dict) else None
    path = sprint.get("path") if isinstance(sprint, dict) else None
    if not isinstance(path, str) or not path:
        raise ValueError(f"{ACTIVE_STATE} has no current_sprint.path")
    return Path(path)


def extract(source: Path, sprint_dir: Path) -> int:
    """Copy `source` to `<sprint_dir>/IMPLEMENTATION_PLAN.md` without overwriting.

    Args:
        source: The Phase 1 plan draft.
        sprint_dir: The sprint directory receiving the plan.

    Returns:
        0 on copy or identical destination, 2 on any refusal.
    """
    if not source.is_file():
        return fail(f"source is missing or not a file: {source}")
    dest = sprint_dir / PLAN_NAME
    if dest.exists() and source.resolve() == dest.resolve():
        return fail(f"source equals destination: {source}")
    if dest.exists():
        if dest.is_file() and filecmp.cmp(source, dest, shallow=False):
            print(f"{dest}: already identical, nothing changed")
            return 0
        return fail(
            f"{dest} exists and differs from {source}; "
            "reconcile by hand, nothing was written"
        )
    sprint_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, dest)
    print(dest)
    return 0


def main(argv: list[str] | None = None) -> int:
    """Run the extraction.

    Args:
        argv: Arguments without the program name; defaults to `sys.argv`.

    Returns:
        The process exit code.
    """
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("source", type=Path, help="Phase 1 plan draft")
    parser.add_argument("--sprint-dir", type=Path, default=None)
    args = parser.parse_args(argv)
    sprint_dir = args.sprint_dir
    if sprint_dir is None:
        try:
            sprint_dir = sprint_dir_from_anchor()
        except ValueError as exc:
            return fail(str(exc))
    return extract(args.source, sprint_dir)


if __name__ == "__main__":
    sys.exit(main())
