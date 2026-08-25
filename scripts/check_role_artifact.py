"""Verify a role left the sprint artifact the registry assigns it.

Reads ``config/artifact_registry.json``. Given ``--role`` and ``--sprint-dir``,
exits ``2`` when any ``required`` sprint-scoped artifact whose ``role`` matches
is absent from that directory.

invoked_by: Makefile 'role-artifacts' target; claude/settings.hooks.json
SubagentStop (Sprint 027).

Usage:
    python3 scripts/check_role_artifact.py --role Orchestrator --sprint-dir docs/sprints/027-core-pipeline
    python3 scripts/check_role_artifact.py --role "Agent Orchestrator" --sprint-dir ...

Exit codes:
    0 — all matching required artifacts present (or none required for the role)
    2 — at least one required artifact missing (RA-11: only 2 blocks)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _root import agents_root  # noqa: E402


def load_registry() -> list[dict]:
    """Return the artifacts list from the framework registry."""
    path = agents_root() / "config" / "artifact_registry.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    return list(payload.get("artifacts") or [])


def missing_for_role(role: str, sprint_dir: Path) -> list[str]:
    """Filenames required for ``role`` that are absent under ``sprint_dir``."""
    missing: list[str] = []
    for entry in load_registry():
        if entry.get("scope") != "sprint":
            continue
        if not entry.get("required"):
            continue
        if entry.get("role") != role:
            continue
        filename = entry.get("filename")
        if not filename:
            continue
        if not (sprint_dir / filename).is_file():
            missing.append(str(filename))
    return missing


def main(argv: list[str] | None = None) -> int:
    """CLI entry: exit 2 when required role artifacts are missing."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    parser.add_argument("--role", required=True, help="Registry role display name")
    parser.add_argument(
        "--sprint-dir",
        required=True,
        type=Path,
        help="Path to docs/sprints/[ID]-[Stack]-[Layer]/",
    )
    args = parser.parse_args(argv)

    sprint_dir = args.sprint_dir
    if not sprint_dir.is_dir():
        print(f"❌ [ROLE-ARTIFACT] sprint dir not found: {sprint_dir}", file=sys.stderr)
        return 2

    missing = missing_for_role(args.role, sprint_dir)
    if missing:
        print(
            f"❌ [ROLE-ARTIFACT] role={args.role!r} missing: {', '.join(missing)}",
            file=sys.stderr,
        )
        return 2
    print(f"✅ [ROLE-ARTIFACT] role={args.role!r} — required artifacts present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
