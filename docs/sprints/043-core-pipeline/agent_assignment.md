# Agent Assignment — Sprint 043 (submodule-runtime-parity)

Source: `docs/sprints/043-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`).
Phase 4.1 of `workflows/pipeline_workflow.md`. This file is the staffing
authority.

Mode: **claude-code**, `delegation_mode: native` — the `Assignee` column names
which profile's ruleset governs each write.

## Scope of this artifact (Phase 4.1 only)

| Owns | Does **not** own |
| :--- | :--- |
| Which ruleset governs each unit | Model / effort (`task_scope.md`) |
| Agent-forge destination on units that create agents | `tier_escalation` proposals |

No unit in this sprint creates an agent profile → `Destination` is `N/A` on
every row.

---

## Staffing

`# | Target | Operation | Mode | Assignee | Destination | Ruleset file`

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| A1 | `workflows/start_workflow.md` | modify | native | `orchestrator` | N/A | `agents/orchestrator.md` |
| A2 | `rules/graphify.md` | modify | native | `rule_validator` | N/A | `agents/rule_validator.md` |
| D1 | `scripts/check_venv_relocatable.py` | create | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| D2 | `tests/test_check_venv_relocatable.py` | create | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C1 | `agents.md` | modify | native | `rule_validator` | N/A | `agents/rule_validator.md` |
| C2 | `docs/guides/SELF_IMPROVEMENT_GUIDE.md` | modify | native | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |

## Disagreements with the plan

None. The plan's `Assignee (proposed)` column stands for all six units:

- A1 is pipeline-protocol prose → `orchestrator` (Roadmap Author owns workflow
  step text).
- A2 and C1 are `rules/` and constitutional text → `rule_validator` (Rule
  Auditor owns `rules/` and `agents.md` amendments).
- D1, D2 are framework-root `scripts/` and `tests/` → `implementer_agent`
  (`ADR-0009` — sole author of those trees).
- C2 is a `docs/guides/` explanatory doc → `doc_orchestrator`.

`jurisdictional_lock` holds: one physical file per unit, no file appears twice.
