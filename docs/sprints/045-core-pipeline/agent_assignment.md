# Agent Assignment — Sprint 045 (nucleus-ruleset-mechanism-audit)

Source: `docs/sprints/045-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`).
Phase 4.1 of `workflows/pipeline_workflow.md`. This file is the staffing
authority: it may overwrite the plan's `Assignee (proposed)` column. A Work row
is not closed until it appears here.

Mode: **claude-code**, `delegation_mode: native` — the `Assignee` column names
which profile's ruleset governs each write.

## Scope of this artifact (Phase 4.1 only)

| Owns | Does **not** own |
| :--- | :--- |
| Which ruleset governs each unit | Cursor model / effort (`task_scope.md`) |
| Agent-forge destination on units that create agents | `tier_escalation` proposals |

No unit in this sprint creates an agent profile → `Destination` is `N/A` on every row.

---

## Staffing

### Wave 1 — domain audits (parallel; disjoint target files, no `no_interference` conflict)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `docs/audits/NUCLEUS_RULESET_AUDIT_REPORT-045.md` | create | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |
| 2 | `docs/audits/NUCLEUS_WORKFLOW_AUDIT_REPORT-045.md` | create | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |
| 3 | `docs/audits/NUCLEUS_MECHANISM_AUDIT_REPORT-045.md` | create | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |

### Wave 2 — synthesis (depends on Wave 1; single writer)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 4 | `docs/audits/NUCLEUS_AUDIT_SYNTHESIS-045.md` | create | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |

Each unit is dispatched in **fresh context** (one physical file per task,
`jurisdictional_lock`). Wave 1's three units carry no shared target, so
`no_interference` (`task_scope.md` cross-check) is satisfied by construction.
Wave 2 starts only after units 1–3 land.

## Disagreements with the plan

None. The plan proposed `rule-validator` for all four units and `agent_orchestrator`
confirms it: `rule_validator` is the Rule Auditor (`agents.md §6`) and the
`audit_workflow.md` Phase 0 coordinator. `qa_agent` / `tester_agent` cannot write
(review-only), and `doc_orchestrator` would not carry the rule-introspection charter.
