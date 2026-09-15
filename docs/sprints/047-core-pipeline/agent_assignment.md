# Agent Assignment — Sprint 047 (nucleus-audit-design-remediation)

Source: `docs/sprints/047-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`).
Phase 4.1 of `workflows/pipeline_workflow.md`. This file is the staffing
authority: it may overwrite the plan's `Assignee (proposed)` column. A Work row
is not closed until it appears here.

Mode: **claude-code** (nucleus), `delegation_mode: native` — the `Assignee`
column names which profile's ruleset governs each write.

## Scope of this artifact (Phase 4.1 only)

| Owns | Does **not** own |
| :--- | :--- |
| Which ruleset governs each unit | Model / effort (`task_scope.md`, Phase 4.3) |
| Agent-forge destination on units that create agents | `tier_escalation` proposals |

**No unit in this sprint creates a new agent profile.** Every U1–U29 assignee is
an existing core or auxiliary role (`rule_validator`, `implementer_agent`), so no
`Destination` value is required — `Destination` is `N/A` on every row and
`check_forge_ladder.py` has no forge row to validate. (U24–U29 are 6 units
discovered mid-execution beyond the plan's original U1–U23; see `task_scope.md`
for the finding that produced each.)

---

## Staffing

Shape is mandatory:

`# | Target | Operation | Mode | Assignee | Destination | Ruleset file`

### Wave 1 — governance prose (`agents.md`, `rules/*.md`, `workflows/*.md`); gate: `make verify`

U1–U10 are governance-prose amendments: the drafted Sprint 045 amendment texts
(`A2`, `A3`, `A6`, `A7` and the Unit 1 rewrites) applied **after** re-verification
against the current tree (`IMPLEMENTATION_PLAN.md` D1). Each is a distinct
physical file — `no_interference` satisfied by construction. Dispatched one
commit each (`RA-08` atomic).

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U1 | `agents.md` | modify | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |
| U2 | `rules/django_backend_standard.md` | modify | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |
| U3 | `rules/LEGACY_RULE_CONCORDANCE.md` | modify | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |
| U4 | `workflows/audit_workflow.md` | modify | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |
| U5 | `rules/skills_and_integrations.md` | modify | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |
| U6 | `workflows/close_workflow.md` | modify | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |
| U7 | `workflows/skill_forge_workflow.md` | modify | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |
| U8 | `workflows/reverse_documentation_workflow.md` | modify | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |
| U9 | `workflows/repository_hardening_workflow.md` | modify | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |
| U10 | `workflows/standardization_workflow.md` | modify | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |

### Wave 2 — framework-root `scripts/` behaviour (`ADR-0009`, Sprint 033)

U11–U17 change executable behaviour under framework-root `scripts/`. That tree is
authored by `implementer_agent` (`agents.md §6`; `devops_agent` holds no
`Write`/`Edit` for it after Sprint 033). Targets are disjoint physical files;
U12's commit also carries the regenerated
`docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` (generator output, never hand-edited).

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U11 | `scripts/verify_references.py` | modify | ruleset | `implementer-agent` | N/A | `agents/implementer_agent.md` |
| U12 | `scripts/map_workflows.py` | modify | ruleset | `implementer-agent` | N/A | `agents/implementer_agent.md` |
| U13 | `scripts/check_gate_log.py` | modify | ruleset | `implementer-agent` | N/A | `agents/implementer_agent.md` |
| U14 | `scripts/session_start.py` | modify | ruleset | `implementer-agent` | N/A | `agents/implementer_agent.md` |
| U15 | `scripts/detect_drift.py` | modify | ruleset | `implementer-agent` | N/A | `agents/implementer_agent.md` |
| U16 | `scripts/_mode.py` | modify | ruleset | `implementer-agent` | N/A | `agents/implementer_agent.md` |
| U17 | `scripts/submodule_purity.py` | modify | ruleset | `implementer-agent` | N/A | `agents/implementer_agent.md` |

### Wave 3 — pytest suites under `tests/`

U18–U23 are pytest files under framework-root `tests/` (`ADR-0009`). Authored by
`implementer_agent`, which holds `Write`/`Edit`; `tester_agent` executes the
suite but does not write test files (`F-026-A1`, `IMPLEMENTATION_PLAN.md` D10).
Targets are disjoint physical files.

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U18 | `tests/test_verify_references.py` | modify/create | ruleset | `implementer-agent` | N/A | `agents/implementer_agent.md` |
| U19 | `tests/test_map_workflows.py` | modify/create | ruleset | `implementer-agent` | N/A | `agents/implementer_agent.md` |
| U20 | `tests/test_check_gate_log.py` | modify/create | ruleset | `implementer-agent` | N/A | `agents/implementer_agent.md` |
| U21 | `tests/test_mode.py` | modify/create | ruleset | `implementer-agent` | N/A | `agents/implementer_agent.md` |
| U22 | `tests/test_session_start.py` | modify/create | ruleset | `implementer-agent` | N/A | `agents/implementer_agent.md` |
| U23 | `tests/test_submodule_purity.py` | modify/create | ruleset | `implementer-agent` | N/A | `agents/implementer_agent.md` |

### Wave 4 — discovered mid-execution (U24–U29)

Each a direct, same-sprint consequence of a unit above (finding recorded in
`task_scope.md` discovery notes), not new scope. Same staffing rule: `rule-
validator` for governance prose, `implementer-agent` for scripts/tests.

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U24 | `config/invocation_exceptions.json` | modify | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |
| U25 | `workflows/pipeline_workflow.md` | modify | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |
| U26 | `rules/token_economy.md` | modify | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |
| U27 | `workflows/standardization_workflow.md` | modify | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |
| U28 | `scripts/session_start.py` | modify | ruleset | `implementer-agent` | N/A | `agents/implementer_agent.md` |
| U29 | `tests/test_session_start.py` | modify | ruleset | `implementer-agent` | N/A | `agents/implementer_agent.md` |

## Assignee breakdown

| Assignee | Units | Count |
| :--- | :--- | :--- |
| `rule-validator` | U1–U10, U24–U27 | 14 |
| `implementer-agent` | U11–U23, U28–U29 | 15 |
| **Total** | U1–U29 | **29** |

## Disagreements with the plan

None. The plan's `Assignee (proposed)` column stands for every unit:

- U1–U10 (`agents.md`, `rules/*.md`, `workflows/*.md` prose) → `rule-validator`
  (Rule Auditor, `agents.md §6`; `agents.md` is the constitution it audits and
  these are governance-prose amendments applying re-verified Sprint 045 texts).
- U11–U17 (`scripts/*.py` behaviour) → `implementer-agent` (owns framework-root
  `scripts/`; `ADR-0009`, Sprint 033). Not `devops_agent` — it holds no `Write`
  for that tree.
- U18–U23 (`tests/*.py`) → `implementer-agent` (holds `Write`/`Edit` for
  framework-root `tests/`; `tester_agent` does not author test files —
  `F-026-A1`).
