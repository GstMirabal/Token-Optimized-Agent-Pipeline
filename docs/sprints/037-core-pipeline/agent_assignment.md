# Agent Assignment — Sprint 037 (`core-pipeline`)

Source: `docs/sprints/037-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`).
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

No unit in 037 **creates** an agent profile. `Destination` is `N/A` on every row.

---

## Track G — derived ledger (D11)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| G1 | `scripts/model_ledger.py` | create | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| G2 | `tests/test_model_ledger.py` | create | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| G3 | `workflows/close_workflow.md` | modify | sequential / ruleset | `orchestrator` | N/A | `agents/orchestrator.md` |

## Track S — Cursor agent sandbox false reds

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| S1 | `Makefile` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| S2 | `tests/test_verify_py_compile.py` | create | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| S3 | `scripts/install.py` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| S4 | `tests/test_installer.sh` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |

## Disagreements with the plan

None. Plan assignees stand.
