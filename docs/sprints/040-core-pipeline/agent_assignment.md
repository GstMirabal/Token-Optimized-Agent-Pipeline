# Agent Assignment — Sprint 040 (`core-pipeline` / cursor-bridge-incremental)

Source: `docs/sprints/040-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`).
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

No unit in 040 **creates** an agent profile. `Destination` is `N/A` on every row.

---

## Track I — install incremental

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| I1 | `scripts/cursor_adapter.py` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| I2 | `tests/test_cursor_adapter.py` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |

## Track S — boot triage + soft-fail

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| S1 | `scripts/session_start.py` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| S2 | `tests/test_session_start.py` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |

## Track W / D — protocolos

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| W1 | `workflows/start_workflow.md` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| D1 | `workflows/deployment_workflow.md` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |

## Track R — resume_pointer rider

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| R1 | `scripts/session_state.py` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| R2 | `tests/test_session_protocol.py` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |

## Track P — program queue

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| P1 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | sequential / ruleset | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |

## Disagreements with the plan

| Unit | Plan proposed | Assigned | Reason |
| :--- | :--- | :--- | :--- |
| None | — | — | Plan assignees stand. |
