# Agent Assignment — Sprint 034 (`core-pipeline`)

Source: `docs/sprints/034-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`).
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

No unit in 034 **creates** an agent profile. `Destination` is `N/A` on every
row. Track N emits generated `.cursor/agents/` files from existing `agents/*.md`;
that is adapter output, not a forge.

**Backfill.** This file was written after several units had already landed
(Phase 6 started without Phase 4). Assignees below match the plan; they are
not retroactive permission.

---

## Track A — close chains deploy

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| A1 | `commands/close.md` | modify | sequential / ruleset | `orchestrator` | N/A | `agents/orchestrator.md` |
| A2 | `workflows/close_workflow.md` | modify | sequential / ruleset | `orchestrator` | N/A | `agents/orchestrator.md` |

## Track B — graph probe truth

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| B1 | `scripts/session_probe.py` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| B2 | `tests/test_session_probe.py` | create | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |

## Track P — auto-pin on `/start`

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| P1 | `scripts/sync_agents_pin.py` | create | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| P2 | `tests/test_sync_agents_pin.py` | create | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| P3 | `workflows/start_workflow.md` | modify | sequential / ruleset | `orchestrator` | N/A | `agents/orchestrator.md` |

## Track I — assignment authority

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| I1 | `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md` | modify | sequential / ruleset | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| I2 | `workflows/pipeline_workflow.md` | modify | sequential / ruleset | `orchestrator` | N/A | `agents/orchestrator.md` |
| I3 | `agents/agent_orchestrator.md` | modify | sequential / ruleset | `agent_orchestrator` | N/A | `agents/agent_orchestrator.md` |
| I4 | `scripts/check_task_scope.py` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| I5 | `tests/test_check_task_scope.py` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| I6 | `docs/hotfixes/H-005-pipeline.md` | create | sequential / ruleset | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| I7 | `docs/standards/templates/AGENT_ASSIGNMENT_TEMPLATE.md` | create | sequential / ruleset | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |

## Track K — absence gates

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| K1 | `scripts/check_role_artifact.py` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| K2 | `config/artifact_registry.json` | modify | sequential / ruleset | `rule_validator` | N/A | `agents/rule_validator.md` |
| K3 | `scripts/check_task_scope.py` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| K4 | `tests/test_check_role_artifact.py` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| K5 | `tests/test_check_task_scope.py` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| K6 | `workflows/pipeline_workflow.md` | modify | sequential / ruleset | `orchestrator` | N/A | `agents/orchestrator.md` |

K6 is the **second** touch of `workflows/pipeline_workflow.md` in this sprint
(after I2). Same assignee `orchestrator`. Sequential, not concurrent.

## Track J — constitution anchor

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| J1 | `AGENTS.md` | modify | sequential / ruleset | `rule_validator` | N/A | `agents/rule_validator.md` |

## Track N — Cursor agent emission

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| N1 | `scripts/cursor_adapter.py` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| N2 | `tests/test_cursor_adapter.py` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| N3 | `.gitignore` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| N4 | `scripts/install.py` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| N5 | `tests/test_installer.sh` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| N6 | `docs/guides/AGENTS_SLASH_COMMANDS_GUIDE.md` | modify | sequential / ruleset | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |

## Quality Gate (Phase 7) — transcription

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| G1.q | verdict → `SPRINT_LOG.md` | emit | sequential | `qa_agent` | `agents/qa_agent.md` |
| G1.q | verdict → `SPRINT_LOG.md` | transcribe | sequential | `orchestrator` | `agents/orchestrator.md` |
| G1.t | verdict → `SPRINT_LOG.md` | emit | sequential | `tester_agent` | `agents/tester_agent.md` |
| G1.t | verdict → `SPRINT_LOG.md` | transcribe | sequential | `orchestrator` | `agents/orchestrator.md` |

## Disagreements with the plan

None. Plan assignees stand. Out-of-sprint tracks (C/E/H/F, M/L, G, family-trial)
are not staffed here.
