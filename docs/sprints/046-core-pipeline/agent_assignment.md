# Agent Assignment — Sprint 046 (nucleus-audit-mechanical-remediation)

Source: `docs/sprints/046-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`).
Phase 4.1 of `workflows/pipeline_workflow.md`. This file is the staffing
authority: it may overwrite the plan's `Assignee (proposed)` column. A Work row
is not closed until it appears here.

Mode: **claude-code**, `delegation_mode: native` — the `Assignee` column names
which profile's ruleset governs each write.

## Scope of this artifact (Phase 4.1 only)

| Owns | Does **not** own |
| :--- | :--- |
| Which ruleset governs each unit | Model / effort (`task_scope.md`, Phase 4.3) |
| Agent-forge destination on units that create agents | `tier_escalation` proposals |

No unit in this sprint creates an agent profile → `Destination` is `N/A` on every
row.

---

## Staffing

### Wave 1 — `agents.md` (strictly serial; single shared target, `no_interference`)

All seven units edit `agents.md`. They are dispatched one at a time on one
`ai-sprint/046` working tree, one commit each (`RA-08` atomic). `no_interference`
forbids a second subagent claiming `agents.md` while one holds it.

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U01 | `agents.md` | modify | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |
| U02 | `agents.md` | modify | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |
| U03 | `agents.md` | modify | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |
| U04 | `agents.md` | modify | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |
| U05 | `agents.md` | modify | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |
| U06 | `agents.md` | modify | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |
| U07 | `agents.md` | modify | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |

### Wave 2 — `rules/`, `workflows/`, templates (disjoint targets; RA-14 propagation gated on Wave 1)

`U08`/`U09` propagate `U04`; `U10` propagates `U06`; `U11` propagates `U07` — so
Wave 2 starts only after Wave 1 lands. Targets are otherwise disjoint.

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U08 | `rules/token_economy.md` | modify | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |
| U09 | `workflows/pipeline_workflow.md` | modify | ruleset | `doc-orchestrator` | N/A | `agents/doc_orchestrator.md` |
| U10 | `rules/LEGACY_RULE_CONCORDANCE.md` | modify | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |
| U11 | `docs/standards/templates/README_TEMPLATE.md` | modify | ruleset | `doc-orchestrator` | N/A | `agents/doc_orchestrator.md` |
| U12 | `rules/frontend_modular_standard.md` | modify | ruleset | `doc-orchestrator` | N/A | `agents/doc_orchestrator.md` |
| U13 | `rules/project_topology.md` | modify | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |
| U14 | `workflows/remediation_workflow.md` | modify | ruleset | `doc-orchestrator` | N/A | `agents/doc_orchestrator.md` |
| U15 | `workflows/standardization_workflow.md` | modify | ruleset | `doc-orchestrator` | N/A | `agents/doc_orchestrator.md` |
| U16 | `workflows/skill_forge_workflow.md` | modify | ruleset | `doc-orchestrator` | N/A | `agents/doc_orchestrator.md` |

### Wave 3 — `scripts/`, `hooks/`, `config/` (disjoint targets; parallel-safe)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U17 | `hooks/state_mirror.py` | modify | ruleset | `implementer-agent` | N/A | `agents/implementer_agent.md` |
| U18 | `scripts/check_gate_log.py` | modify | ruleset | `implementer-agent` | N/A | `agents/implementer_agent.md` |
| U19 | `hooks/on_commit.py` | modify | ruleset | `implementer-agent` | N/A | `agents/implementer_agent.md` |
| U20 | `scripts/merge_json.py` | modify | ruleset | `implementer-agent` | N/A | `agents/implementer_agent.md` |
| U21 | `scripts/cursor_adapter.py` | modify | ruleset | `implementer-agent` | N/A | `agents/implementer_agent.md` |
| U22 | `scripts/audit_cursor_era.py` | modify | ruleset | `implementer-agent` | N/A | `agents/implementer_agent.md` |
| U23 | `config/invocation_exceptions.json` | modify | ruleset | `implementer-agent` | N/A | `agents/implementer_agent.md` |

### Wave 4 — templates + evidence closeout (gated on Waves 1–3)

`U24` needs the RA-17 vocabulary settled (unchanged this sprint, but the stub
must match `check_gate_log.py`). `U25`–`U28` annotate the Sprint 045 audit
reports as applied and must run after every `S045-*` unit lands. `U25`–`U28`
target four different files → parallel-safe among themselves.

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U24 | `docs/standards/templates/SPRINT_LOG_TEMPLATE.md` | modify | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |
| U25 | `docs/audits/NUCLEUS_AUDIT_SYNTHESIS-045.md` | modify | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |
| U26 | `docs/audits/NUCLEUS_RULESET_AUDIT_REPORT-045.md` | modify | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |
| U27 | `docs/audits/NUCLEUS_WORKFLOW_AUDIT_REPORT-045.md` | modify | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |
| U28 | `docs/audits/NUCLEUS_MECHANISM_AUDIT_REPORT-045.md` | modify | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |

Each unit is dispatched in **fresh context**, one physical file per task
(`jurisdictional_lock`). `no_interference` is satisfied by construction: Wave 1
serialises on `agents.md`; Waves 2–4 carry disjoint targets within each wave.

## Disagreements with the plan

None. The plan's `Assignee (proposed)` column stands for every unit:

- `agents.md` and `rules/` amendments → `rule-validator` (Rule Auditor,
  `agents.md §6`; `agents.md` is the constitution it audits).
- `workflows/` prose and template (`README_TEMPLATE.md`,
  `frontend_modular_standard.md` structure) → `doc-orchestrator` (documentation
  authoring, `rules/documentation_standard.md` compliance).
- `scripts/` + `hooks/` + `config/` → `implementer-agent` (owns framework-root
  `scripts/`/`hooks/`; `ADR-0009`, Sprint 033). Not `devops_agent` — it holds no
  `Write` for those trees (`agents.md §6`).
- `SPRINT_LOG_TEMPLATE.md` + audit-report annotations → `rule-validator` (the
  stub is gated by `check_gate_log.py` / `RA-17`; the audit reports are its own
  Sprint 045 deliverables).
