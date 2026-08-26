"""Verify a role left the sprint artifact the registry assigns it.

Reads ``config/artifact_registry.json``. Given ``--role`` and ``--sprint-dir``,
exits ``2`` when any ``required`` sprint-scoped artifact whose ``role`` matches
is absent from that directory, or when a Double-Gate role left no Gate row in
``SPRINT_LOG.md`` (registry ``gate_evidence``).

``--role`` accepts either form: the registry display name (``Rule Validator``)
or the profile name the rest of the framework uses (``rule_validator``). Until
Sprint 034 only the first worked, and the second returned zero matches — which
this script reported as success. Every caller using the framework's own role
vocabulary was therefore approving empty directories (D17).

invoked_by: Makefile 'role-artifacts' target; claude/settings.hooks.json
SubagentStop (Sprint 027).

Usage:
    python3 scripts/check_role_artifact.py --role Orchestrator --sprint-dir docs/sprints/027-core-pipeline
    python3 scripts/check_role_artifact.py --role rule_validator --sprint-dir ...
    python3 scripts/check_role_artifact.py --from-hook   # SubagentStop: JSON on stdin

Exit codes:
    0 — required artifacts present, or the registry declares none for the role
    2 — a required artifact or Gate row is missing, or the role is unknown
        (RA-11: only 2 blocks)

The CLI refuses an unrecognised role; ``--from-hook`` only warns, because a
SubagentStop payload carries arbitrary agent types including the runtime's own
built-ins, and blocking those would stop unrelated subagents.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _root import agents_root

ACTIVE_STATE = Path("docs/active_state.json")

# Profile name (agent frontmatter ``name``, or the snake_case filename the
# framework writes in task_scope.md) → artifact_registry role display name.
# Every profile in agents/ is listed: an absent one used to fall through to a
# fabricated Title Case string that no registry entry matched, and zero matches
# read as success.
_AGENT_TYPE_TO_ROLE = {
    "principal-agent": "Principal Agent",
    "orchestrator": "Orchestrator",
    "agent-orchestrator": "Agent Orchestrator",
    "skill-architect": "Skill Architect",
    "rule-validator": "Rule Validator",
    "devops-agent": "DevOps Agent",
    "governance-learner": "Governance Learner",
    "qa-agent": "QA Agent",
    "tester-agent": "Tester Agent",
    "doc-orchestrator": "Doc Orchestrator",
    "implementer-agent": "Implementer Agent",
    "token-economy-agent": "Token Economy Agent",
    "git-sync-agent": "Git Sync Agent",
    "topology-mapper": "Topology Mapper",
}


def _registry() -> dict:
    """Return the parsed framework registry."""
    path = agents_root() / "config" / "artifact_registry.json"
    return json.loads(path.read_text(encoding="utf-8"))


def load_registry() -> list[dict]:
    """Return the artifacts list from the framework registry."""
    return list(_registry().get("artifacts") or [])


def gate_evidence() -> dict[str, str]:
    """Registry role display name -> token its ``Gate`` cell must start with."""
    block = _registry().get("gate_evidence") or {}
    return dict(block.get("roles") or {})


def known_roles() -> set[str]:
    """Role display names the registry declares, artifacts and gates alike."""
    roles = {entry.get("role") for entry in load_registry() if entry.get("role")}
    return roles | set(gate_evidence())


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
    """Map a profile name to a registry role display name, or None if unknown.

    Purely lexical: it does not assert the registry declares the result. The
    Title Case fallback this function used to have is gone — it manufactured
    names like ``Qa Agent`` that matched nothing, and matching nothing was
    reported as success.

    Args:
        agent_type (str): Profile name in any case, ``-`` or ``_`` separated.

    Returns:
        str | None: Registry display name, or None when unrecognised.
    """
    key = agent_type.strip().lower().replace("_", "-")
    if not key:
        return None
    return _AGENT_TYPE_TO_ROLE.get(key)


def resolve_role(name: str) -> str | None:
    """Accept a display name or a profile name; return the display name.

    Args:
        name (str): ``Rule Validator`` or ``rule_validator``, either accepted.

    Returns:
        str | None: Registry display name, or None when unrecognised.
    """
    raw = name.strip()
    if not raw:
        return None
    if raw in known_roles():
        return raw
    return role_from_agent_type(raw)


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


def missing_gate_row(role: str, sprint_dir: Path) -> str | None:
    """Describe the absent ``Gate`` row for ``role``, or None when it is there.

    A Double-Gate role owns no file of its own, so file existence cannot show
    it ran: ``SPRINT_LOG.md`` is written at Phase 3, long before any gate. The
    evidence is a row inside it.

    Args:
        role (str): Registry role display name.
        sprint_dir (Path): Sprint directory to inspect.

    Returns:
        str | None: What is missing, or None when the role owes no gate row.
    """
    block = _registry().get("gate_evidence") or {}
    token = (block.get("roles") or {}).get(role)
    if not token:
        return None
    log = sprint_dir / (block.get("file") or "SPRINT_LOG.md")
    if not log.is_file():
        return f"{log.name} (no gate log to carry the {token!r} row)"

    from check_gate_log import gate_tables

    for header, rows in gate_tables(log.read_text(encoding="utf-8")):
        if "Gate" not in header:
            continue
        column = header.index("Gate")
        cells = [row[column].strip() for row in rows if len(row) > column]
        if any(cell.startswith(token) for cell in cells):
            return None
    return f"{token!r} row in {log.name}"


def _report(role: str, sprint_dir: Path) -> int:
    """Shared exit logic for CLI and --from-hook."""
    if not sprint_dir.is_dir():
        print(f"❌ [ROLE-ARTIFACT] sprint dir not found: {sprint_dir}", file=sys.stderr)
        return 2

    missing = missing_for_role(role, sprint_dir)
    gate_gap = missing_gate_row(role, sprint_dir)
    if gate_gap:
        missing.append(gate_gap)
    if missing:
        print(
            f"❌ [ROLE-ARTIFACT] role={role!r} missing: {', '.join(missing)}",
            file=sys.stderr,
        )
        return 2
    if role not in known_roles():
        print(f"✅ [ROLE-ARTIFACT] role={role!r} — registry declares no artifact")
        return 0
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

    agent_type = str(payload.get("agent_type") or "")
    role = resolve_role(agent_type)
    if not role:
        print(
            f"⚠️ [ROLE-ARTIFACT] --from-hook: unrecognised agent_type {agent_type!r}; skip",
            file=sys.stderr,
        )
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
    parser.add_argument(
        "--role",
        help="Registry display name ('Rule Validator') or profile name ('rule_validator')",
    )
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

    role = resolve_role(args.role)
    if role is None:
        print(
            f"❌ [ROLE-ARTIFACT] unknown role {args.role!r} — known: "
            f"{', '.join(sorted(known_roles()))}",
            file=sys.stderr,
        )
        return 2

    return _report(role, args.sprint_dir)


if __name__ == "__main__":
    sys.exit(main())
