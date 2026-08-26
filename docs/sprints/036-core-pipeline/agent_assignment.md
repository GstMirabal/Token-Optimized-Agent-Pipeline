# Agent Assignment — Sprint 036 (`core-pipeline`)

Source: `docs/sprints/036-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`).
Phase 4.1 of `workflows/pipeline_workflow.md`. Drafted from
`docs/standards/templates/AGENT_ASSIGNMENT_TEMPLATE.md`.
Mode: **Cursor**, `delegation_mode: sequential` — the `Assignee` column names
which profile's ruleset the single session adopts for that write.

This file is the staffing authority. It may overwrite the plan's
`Assignee (proposed)` column. A Work row is not closed until it appears here.

## Scope of this artifact (Phase 4.1 only)

| Owns | Does **not** own |
| :--- | :--- |
| Which ruleset governs each unit | Cursor model / effort (`task_scope.md`) |
| Agent-forge destination on units that create agents | `tier_escalation` proposals |

No unit in 036 **creates** an agent profile. `Destination` is `N/A` on every
row. M3/M7/M8/M9 modify existing profiles; that is not a forge. M1 tests the
forge ladder against a **fixture** host layout — it does not author a live
profile under `agents/`.

---

## Track L — Cursor-era execution census (`D18`)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| L1 | `scripts/audit_cursor_era.py` | create | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| L2 | `tests/test_audit_cursor_era.py` | create | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| L3 | `Makefile` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |

## Track M — forge ladder + gate instructing (`D19`)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| M1 | `scripts/check_forge_ladder.py` | create | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| M2 | `tests/test_check_forge_ladder.py` | create | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| M3 | `agents/skill_architect.md` | modify | sequential / ruleset | `agent_orchestrator` | N/A | `agents/agent_orchestrator.md` |
| M4 | `docs/standards/templates/SKILL_ASSIGNMENT_TEMPLATE.md` | create | sequential / ruleset | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| M5 | `workflows/pipeline_workflow.md` | modify | sequential / ruleset | `orchestrator` | N/A | `agents/orchestrator.md` |
| M6 | `tests/test_agent_profile_census.py` | create | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| M7 | `agents/qa_agent.md` | modify | sequential / ruleset | `agent_orchestrator` | N/A | `agents/agent_orchestrator.md` |
| M8 | `agents/tester_agent.md` | modify | sequential / ruleset | `agent_orchestrator` | N/A | `agents/agent_orchestrator.md` |
| M9 | `agents/principal_agent.md` | modify | sequential / ruleset | `agent_orchestrator` | N/A | `agents/agent_orchestrator.md` |

## Disagreements with the plan

None. Plan assignees stand. Out-of-sprint tracks (G, family-trial) stay on
037–038.
