# Agent Assignment — Sprint 035 (`core-pipeline`)

Source: `docs/sprints/035-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`).
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

No unit in 035 **creates** an agent profile. `Destination` is `N/A` on every
row. F3 modifies an existing profile (`token_economy_agent.md`); that is not
a forge.

---

## Track E — apply map at runtime (`ADR-0010`)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| E0 | `docs/guides/MODEL_TIER_TRIAL_GUIDE.md` | modify | sequential / ruleset | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| E1 | `docs/decisions/ADR-0010-cursor-task-applies-tier-map.md` | create | sequential / ruleset | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| E2 | `scripts/audit_cursor_models.py` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| E3 | `workflows/pipeline_workflow.md` | modify | sequential / ruleset | `orchestrator` | N/A | `agents/orchestrator.md` |
| E4 | `tests/test_audit_cursor_models.py` | create | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| E5 | `scripts/audit_cursor_models.py` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| E6 | `scripts/audit_cursor_models.py` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |

## Track C — `/start` briefing

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| C1 | `scripts/session_start.py` | create | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C2 | `workflows/start_workflow.md` | modify | sequential / ruleset | `orchestrator` | N/A | `agents/orchestrator.md` |
| C3 | `commands/start.md` | modify | sequential / ruleset | `orchestrator` | N/A | `agents/orchestrator.md` |
| C4 | `tests/test_session_start.py` | create | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C5 | `Makefile` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |

## Track H — structural ceiling for `gate` (`D13`)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| H1 | `docs/decisions/ADR-0011-gate-cell-by-structural-ceiling.md` | create | sequential / ruleset | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| H2 | `config/model_tiers.json` | modify | sequential / ruleset | `rule_validator` | N/A | `agents/rule_validator.md` |
| H3 | `scripts/verify_references.py` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| H4 | `tests/test_verify_references.py` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |

## Track F — Phase 4.3 ownership

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| F3 | `agents/token_economy_agent.md` | modify | sequential / ruleset | `agent_orchestrator` | N/A | `agents/agent_orchestrator.md` |

## Disagreements with the plan

None. Plan assignees stand. Out-of-sprint tracks (M/L, G, family-trial) stay
on 036–038.
