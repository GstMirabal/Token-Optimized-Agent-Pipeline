# Agent Assignment — Sprint 039 (`core-pipeline` / start-close-lifecycle)

Source: `docs/sprints/039-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`).
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

No unit in 039 **creates** an agent profile. `Destination` is `N/A` on every row.

---

## Track L — baseline post-deploy

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| L1 | `scripts/session_state.py` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| L2 | `workflows/deployment_workflow.md` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| L3 | `scripts/detect_drift.py` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| L4 | `tests/test_session_protocol.py` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |

L4 includes P2 probe fixtures (plan: same physical file).

## Track B — boot path

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| B1 | `scripts/session_start.py` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| B2 | `tests/test_session_start.py` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| B3 | `commands/start.md` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| B4 | `workflows/start_workflow.md` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |

## Track C — bridge freshness

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| C1 | `scripts/cursor_adapter.py` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C2 | `tests/test_cursor_adapter.py` | create | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |

## Track R — registry / mapa

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| R1 | `config/artifact_registry.json` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| R2 | `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` | modify (generated) | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |

## Track P — probe higiene

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| P1 | `scripts/session_probe.py` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |

P2 folded into L4.

## Track D — docs

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| D1 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | sequential / ruleset | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| D2 | `docs/decisions/ADR-0002-drift-verdict-exit-codes.md` | modify | sequential / ruleset | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |

## Disagreements with the plan

| Unit | Plan proposed | Assigned | Reason |
| :--- | :--- | :--- | :--- |
| None | — | — | Plan assignees stand. R2 confirmed as separate generated-guide unit. P2 → L4 as planned. |
