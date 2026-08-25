"""Verify a role left the sprint artifact the registry assigns it.

Reads ``config/artifact_registry.json``. Given ``--role`` and ``--sprint-dir``,
exits ``2`` when any ``required`` sprint-scoped artifact whose ``role`` matches
is absent from that directory.

invoked_by: Makefile 'role-artifacts' target; claude/settings.hooks.json
SubagentStop (Sprint 027).

Usage:
    python3 scripts/check_role_artifact.py --role Orchestrator --sprint-dir docs/sprints/027-core-pipeline
    python3 scripts/check_role_artifact.py --role "Agent Orchestrator" --sprint-dir ...
    python3 scripts/check_role_artifact.py --from-hook   # SubagentStop: JSON on stdin

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

ACTIVE_STATE = Path("docs/active_state.json")

# Claude Code agent frontmatter ``name`` → artifact_registry role display name.
_AGENT_TYPE_TO_ROLE = {
    "principal-agent": "Principal Agent",
    "orchestrator": "Orchestrator",
    "agent-orchestrator": "Agent Orchestrator",
    "skill-architect": "Skill Architect",
    "rule-validator": "Rule Validator",
    "devops-agent": "DevOps Agent",
    "governance-learner": "Governance Learner",
}


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


def role_from_agent_type(agent_type: str) -> str | None:
    """Map a Claude Code ``agent_type`` to a registry role, or None if unknown."""
    key = agent_type.strip().lower().replace("_", "-")
    if not key:
        return None
    if key in _AGENT_TYPE_TO_ROLE:
        return _AGENT_TYPE_TO_ROLE[key]
    # Fallback: kebab → Title Case (qa-agent → Qa Agent — may miss registry).
    return " ".join(part.capitalize() for part in key.split("-"))


def sprint_dir_from_anchor(anchor: Path = ACTIVE_STATE) -> Path | None:
    """Derive ``docs/sprints/[ID]-[Stack]-[Layer]`` from the active anchor."""
    if not anchor.is_file():
        return None
    try:
        state = json.loads(anchor.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    sprint = state.get("current_sprint") or {}
    sprint_id = sprint.get("id")
    if sprint_id is None:
        return None
    layer = sprint.get("layer") or "core"
    app = sprint.get("app") or "pipeline"
    return Path(f"docs/sprints/{int(sprint_id):03d}-{layer}-{app}")


def _report(role: str, sprint_dir: Path) -> int:
    """Shared exit logic for CLI and --from-hook."""
    if not sprint_dir.is_dir():
        print(f"❌ [ROLE-ARTIFACT] sprint dir not found: {sprint_dir}", file=sys.stderr)
        return 2

    missing = missing_for_role(role, sprint_dir)
    if missing:
        print(
            f"❌ [ROLE-ARTIFACT] role={role!r} missing: {', '.join(missing)}",
            file=sys.stderr,
        )
        return 2
    print(f"✅ [ROLE-ARTIFACT] role={role!r} — required artifacts present")
    return 0


def main_from_hook(stdin_text: str | None = None) -> int:
    """SubagentStop path: read agent_type from stdin JSON; sprint from anchor.

    Exit 0 (advisory skip) when agent_type or sprint cannot be resolved — the
    portable guarantee remains ``make role-artifacts`` / close Phase 2.6.
    """
    raw = stdin_text if stdin_text is not None else sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        print("⚠️ [ROLE-ARTIFACT] --from-hook: invalid JSON on stdin; skip", file=sys.stderr)
        return 0

    role = role_from_agent_type(str(payload.get("agent_type") or ""))
    if not role:
        print("⚠️ [ROLE-ARTIFACT] --from-hook: no agent_type; skip", file=sys.stderr)
        return 0

    sprint_dir = sprint_dir_from_anchor()
    if sprint_dir is None:
        print("⚠️ [ROLE-ARTIFACT] --from-hook: no current_sprint; skip", file=sys.stderr)
        return 0

    return _report(role, sprint_dir)


def main(argv: list[str] | None = None) -> int:
    """CLI entry: exit 2 when required role artifacts are missing."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    parser.add_argument(
        "--from-hook",
        action="store_true",
        help="Read SubagentStop JSON from stdin; derive sprint from active_state",
    )
    parser.add_argument("--role", help="Registry role display name")
    parser.add_argument(
        "--sprint-dir",
        type=Path,
        help="Path to docs/sprints/[ID]-[Stack]-[Layer]/",
    )
    args = parser.parse_args(argv)

    if args.from_hook:
        return main_from_hook()

    if not args.role or not args.sprint_dir:
        parser.error("--role and --sprint-dir are required unless --from-hook is set")

    return _report(args.role, args.sprint_dir)


if __name__ == "__main__":
    sys.exit(main())
