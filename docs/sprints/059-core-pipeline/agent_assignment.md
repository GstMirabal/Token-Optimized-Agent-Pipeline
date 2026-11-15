# Agent Assignment — Sprint 059 (efficiency-and-sandbox-regime)

Source: `docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`).
Phase 4.1 of `workflows/pipeline_workflow.md`. This file is the staffing
authority: it may overwrite the plan's `Assignee (proposed)` column. A Work row
is not closed until it appears here.

Mode: **claude-code**, `delegation_mode: native` — the
`Assignee` column names which profile's ruleset governs each write.

## Scope of this artifact (Phase 4.1 only)

| Owns | Does **not** own |
| :--- | :--- |
| Which ruleset governs each unit | Cursor model / effort (`task_scope.md`) |
| Agent-forge destination on units that create agents | `tier_escalation` proposals |

`Destination` is **required** on every unit that **creates** an agent profile.
Values: `host:.claude/agents/` (default), `profile:<path>`, `nucleus:PR`.
Units that do not create a profile use `N/A`.

No unit of this sprint creates an agent profile: A-08 modifies the existing
`agents/qa_agent.md`. Every `Destination` cell is `N/A`.

Mode `parallel` marks a unit that `scripts/check_task_scope.py` may place in a
parallel batch once G-01 lands (plan D11, from Wave 3 onward). Waves 1 and 2
run `sequential`, because the batch calculator does not exist before G-01.
Recorded deviation (plan D16): A-11, A-13, A-08 and A-01 were dispatched together
without a rule allowing it. The declared mode stays `sequential` and this is no precedent.

---

## Staffing

### Wave 1 — cost levers

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| A-05 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-09 | `rules/code_craft.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| A-10 | `rules/project_topology.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| A-11 | `docs/guides/SELF_IMPROVEMENT_GUIDE.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-13 | `docs/guides/RULE_PRECEDENTS_GUIDE.md` | create | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-15 | `rules/skills_and_integrations.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| A-16 | `rules/qa_and_testing.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| A-17 | `rules/project_topology.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| A-12 | `agents.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| A-14 | `docs/decisions/ADR-0021-qa-agent-tier-trial.md` | create | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-08 | `agents/qa_agent.md` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A-01 | `scripts/session_cost.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A-19 | `CHANGELOG.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-20 | `docs/roadmaps/core/pipeline/014-identity-branding-hardening.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-21 | `docs/roadmaps/core/pipeline/015-terminology-and-nomenclature-hardening.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-22 | `docs/roadmaps/core/pipeline/016-folder-topology-migration.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-23 | `docs/roadmaps/core/pipeline/017-pre-publication-hardening.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-24 | `docs/sprints/023-core-pipeline/task_scope.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-25 | `tests/test_token_economy_soft_bound.py` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A-26 | `CHANGELOG.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-27 | `docs/roadmaps/core/pipeline/015-terminology-and-nomenclature-hardening.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-28 | `docs/roadmaps/core/pipeline/016-folder-topology-migration.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-29 | `docs/roadmaps/core/pipeline/017-pre-publication-hardening.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-30 | `workflows/reverse_documentation_workflow.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-31 | `tests/test_profile_references.py` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A-32 | `rules/qa_and_testing.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| A-33 | `agents/governance_learner.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| A-34 | `agents/rule_validator.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| A-35 | `workflows/remediation_workflow.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| A-36 | `agents.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| A-37 | `rules/documentation_standard.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| A-38 | `config/rule_triggers.json` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| A-39 | `agents.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| A-40 | `docs/roadmaps/core/pipeline/018-post-publication-field-hardening.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-41 | `skills/skillopt/data/scenarios.json` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-42 | `docs/roadmaps/core/pipeline/008-session-close-governance.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-43 | `skills/mcp-registry/README.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-44 | `profiles/example-project/mcp/registry.json` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-45 | `docs/guides/RULE_PRECEDENTS_GUIDE.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-46 | `docs/standards/templates/HOTFIX_TEMPLATE.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-47 | `docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-48 | `tests/test_profile_references.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A-49 | `scripts/check_log_append_only.py` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A-50 | `tests/test_check_log_append_only.py` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A-51 | `Makefile` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A-52 | `rules/documentation_standard.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| A-53 | `scripts/check_log_append_only.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A-54 | `docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |

### Wave 1b — method (plan D37)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| M-01 | `scripts/_current_sprint.py` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| M-02 | `scripts/check_task_scope.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| M-03 | `scripts/check_gate_log.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| M-04 | `skills/token-saver-auditor/scripts/audit_plan.py` | modify | sequential | `skill_architect` | N/A | `agents/skill_architect.md` |
| M-12 | `scripts/loop_guard.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| M-05 | `tests/test_current_sprint_matrix.py` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| M-06 | `scripts/check_sprint_refs.py` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| M-07 | `Makefile` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| M-08 | `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| M-09 | `docs/standards/templates/SPRINT_LOG_TEMPLATE.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| M-10 | `docs/standards/templates/AGENT_ASSIGNMENT_TEMPLATE.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| M-11 | `docs/sprints/059-core-pipeline/SPRINT_LOG.md` | modify | sequential | `orchestrator` | N/A | `agents/orchestrator.md` |
| M-13 | `skills/token-saver-auditor/scripts/audit_plan.py` | modify | sequential | `skill_architect` | N/A | `agents/skill_architect.md` |
| M-14 | `docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md` | modify | sequential | `orchestrator` | N/A | `agents/orchestrator.md` |
| M-15 | `scripts/_current_sprint.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| M-16 | `scripts/check_task_scope.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |

### Wave 2 — pace and autonomy

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| M-17 | `scripts/_current_sprint.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| G-01 | `scripts/check_task_scope.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| G-02 | `workflows/pipeline_workflow.md` | modify | sequential | `orchestrator` | N/A | `agents/orchestrator.md` |
| B-01 | `scripts/prompt_count.py` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| B-07 | `workflows/close_workflow.md` | modify | sequential | `orchestrator` | N/A | `agents/orchestrator.md` |
| B-02 | `docs/sprints/059-core-pipeline/PROMPT_MEASUREMENT.md` | create | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| B-06 | `scripts/install.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| E-01 | `scripts/session_state.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| E-01c | `scripts/session_state.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| M-18 | `scripts/check_task_scope.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| M-19 | `scripts/prompt_count.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| M-20 | `scripts/prompt_count.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| M-21 | `docs/plans/README.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| B-08 | `docs/sprints/059-core-pipeline/PROMPT_MEASUREMENT.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| B-09 | `docs/sprints/059-core-pipeline/SPRINT_LOG.md` | modify | sequential | `orchestrator` | N/A | `agents/orchestrator.md` |
| M-22 | `scripts/check_task_scope.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| M-23 | `scripts/install.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| B-10 | `docs/sprints/059-core-pipeline/SPRINT_LOG.md` | modify | sequential | `orchestrator` | N/A | `agents/orchestrator.md` |
| M-24 | `scripts/check_task_scope.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| B-11 | `docs/sprints/059-core-pipeline/SPRINT_LOG.md` | modify | sequential | `orchestrator` | N/A | `agents/orchestrator.md` |
| M-25 | `workflows/pipeline_workflow.md` | modify | sequential | `orchestrator` | N/A | `agents/orchestrator.md` |
| B-12 | `docs/sprints/059-core-pipeline/SPRINT_LOG.md` | modify | sequential | `orchestrator` | N/A | `agents/orchestrator.md` |
| M-26 | `workflows/pipeline_workflow.md` | modify | sequential | `orchestrator` | N/A | `agents/orchestrator.md` |
| M-27 | `scripts/check_task_scope.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| B-13 | `docs/sprints/059-core-pipeline/SPRINT_LOG.md` | modify | sequential | `orchestrator` | N/A | `agents/orchestrator.md` |
| B-14 | `docs/sprints/059-core-pipeline/SPRINT_LOG.md` | modify | sequential | `orchestrator` | N/A | `agents/orchestrator.md` |
| B-15 | `docs/sprints/059-core-pipeline/task_scope.md` | modify | sequential | `orchestrator` | N/A | `agents/orchestrator.md` |
| M-28 | `agents/rule_validator.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| M-29 | `rules/project_topology.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| M-30 | `rules/django_backend_standard.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| M-31 | `rules/code_craft.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| M-32 | `rules/graphify.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |

### Wave 3 — in-session token economy

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| A-18 | `scripts/session_cost.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A-00 | `docs/sprints/059-core-pipeline/TOKEN_ECONOMY_STUDY.md` | create | parallel | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-06 | `docs/sprints/059-core-pipeline/TOKEN_ECONOMY_STUDY.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-07 | `docs/decisions/ADR-0018-in-session-token-economy.md` | create | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-02 | `scripts/session_cost.py` | modify | parallel | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A-55 | `scripts/session_probe.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A-56 | `scripts/check_task_scope.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A-03 | `rules/token_economy.md` | modify | parallel | `rule_validator` | N/A | `agents/rule_validator.md` |
| H-01 | `config/unit_cost_estimates.json` | create | parallel | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| H-02 | `scripts/check_task_scope.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| H-04 | `scripts/unit_cost.py` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| H-03 | `workflows/close_workflow.md` | modify | sequential | `orchestrator` | N/A | `agents/orchestrator.md` |
| A-04 | `workflows/pipeline_workflow.md` | modify | sequential | `orchestrator` | N/A | `agents/orchestrator.md` |

### Wave 4 — sandbox measurement

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| B-03 | `scripts/py_compile_tree.py` | modify | parallel | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| B-04 | `skills/mass-standardizer/scripts/generate_manifest.py` | modify | parallel | `skill_architect` | N/A | `agents/skill_architect.md` |
| B-05 | `Makefile` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| B-16 | `Makefile` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| B-17 | `scripts/upstream_intake.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| B-18 | `tests/test_upstream_outbox.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| B-19 | `tests/test_upstream_intake.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| B-20 | `tests/test_check_fix_reproduces.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| B-21 | `Makefile` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C-01 | `docs/sprints/059-core-pipeline/SANDBOX_ENUMERATION.md` | create | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| C-01b | `docs/sprints/059-core-pipeline/SANDBOX_ENUMERATION.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| C-02 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| C-01c | `docs/sprints/059-core-pipeline/SANDBOX_ENUMERATION.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| C-03 | `scripts/session_cost.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C-04 | `docs/sprints/059-core-pipeline/SANDBOX_ENUMERATION.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| C-05 | `scripts/check_sprint_refs.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C-06 | `scripts/check_sprint_refs.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C-07 | `tests/test_check_sprint_refs.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C-08 | `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| C-09 | `tests/test_check_sprint_refs.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C-10 | `docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md` | modify | sequential | `orchestrator` | N/A | `agents/orchestrator.md` |
| C-11 | `docs/sprints/059-core-pipeline/task_scope.md` | modify | sequential | `orchestrator` | N/A | `agents/orchestrator.md` |
| C-12 | `docs/sprints/059-core-pipeline/SPRINT_LOG.md` | modify | sequential | `orchestrator` | N/A | `agents/orchestrator.md` |
| C-13 | `docs/sprints/059-core-pipeline/SPRINT_LOG.md` | modify | sequential | `orchestrator` | N/A | `agents/orchestrator.md` |
| C-14 | `docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md` | modify | sequential | `orchestrator` | N/A | `agents/orchestrator.md` |
| C-15 | `docs/sprints/059-core-pipeline/SPRINT_LOG.md` | modify | sequential | `orchestrator` | N/A | `agents/orchestrator.md` |

### Wave 5 — regime

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| S-01 | `docs/sprints/059-core-pipeline/HARNESS_MEASUREMENT.md` | create | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| S-02 | `docs/sprints/059-core-pipeline/HARNESS_MEASUREMENT.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| S-03 | `docs/sprints/059-core-pipeline/HARNESS_MEASUREMENT.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| S-04 | `docs/sprints/059-core-pipeline/HARNESS_MEASUREMENT.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| S-05 | `docs/sprints/059-core-pipeline/HARNESS_MEASUREMENT.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| S-06 | `docs/sprints/059-core-pipeline/HARNESS_MEASUREMENT.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| S-07 | `docs/sprints/059-core-pipeline/HARNESS_MEASUREMENT.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| S-08 | `docs/sprints/059-core-pipeline/HARNESS_MEASUREMENT.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| S-09 | `docs/sprints/059-core-pipeline/HARNESS_MEASUREMENT.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| S-10 | `docs/sprints/059-core-pipeline/HARNESS_MEASUREMENT.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| S-11 | `docs/sprints/059-core-pipeline/HARNESS_MEASUREMENT.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| S-12 | `docs/sprints/059-core-pipeline/HARNESS_MEASUREMENT.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| S-13 | `scripts/sandbox_probe.py` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| S-14 | `tests/test_sandbox_probe.py` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| S-15 | `Makefile` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| S-16 | `docs/sprints/059-core-pipeline/HARNESS_ATTACK_SCOPE.md` | create | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| D-01 | `docs/decisions/ADR-0019-sandbox-regime.md` | create | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| D-02 | `agents.md` | modify | parallel | `rule_validator` | N/A | `agents/rule_validator.md` |
| D-03 | `rules/project_topology.md` | modify | parallel | `rule_validator` | N/A | `agents/rule_validator.md` |
| D-04 | `claude/settings.hooks.json` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| E-01b | `claude/settings.hooks.json` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| P-01 | `docs/sprints/059-core-pipeline/HARNESS_MEASUREMENT.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| P-02 | `docs/sprints/059-core-pipeline/HARNESS_MEASUREMENT.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| P-03 | `docs/decisions/ADR-0022-sandbox-regime-amendment.md` | create | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| P-05 | `docs/sprints/059-core-pipeline/HARNESS_MEASUREMENT.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| P-06 | `docs/sprints/059-core-pipeline/HARNESS_MEASUREMENT.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| P-07 | `docs/sprints/059-core-pipeline/HARNESS_MEASUREMENT.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| R-01 | `claude/settings.hooks.json` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| R-02 | `.claude/settings.json` | install (human runs) | sequential | `devops_agent` | N/A | `agents/devops_agent.md` |
| R-03 | `docs/sprints/059-core-pipeline/HARNESS_MEASUREMENT.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| R-04 | `scripts/sandbox_probe.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| R-05 | `requirements-core.txt` | modify | parallel | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| R-06 | `requirements-quality.txt` | modify | parallel | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| R-07 | `requirements-skillopt.txt` | modify | parallel | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| R-08 | `workflows/repository_hardening_workflow.md` | modify | parallel | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| R-12 | `docs/sprints/059-core-pipeline/HARNESS_MEASUREMENT.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| R-13 | `.github/workflows/ci.yml` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| R-14 | `scripts/install.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| R-15 | `scripts/quality_audit.py` | fix | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| R-16 | `pytest.ini` | fix | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| R-17 | `tests/test_installer.sh` | fix | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| T-01 | `docs/sprints/059-core-pipeline/HARNESS_MEASUREMENT.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| V-01 | `docs/sprints/059-core-pipeline/HARNESS_ATTACK_RESULT.md` | create | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| V-02 | `docs/decisions/ADR-0023-sandbox-boundary-result.md` | create | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |

### Wave 6 — hardening, roles and Sprint 058 residues

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| E-02 | `claude/mcp.json` | modify | parallel | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| E-03 | `.github/workflows/ci.yml` | modify | parallel | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| F-01 | `docs/decisions/ADR-0020-owner-writer-dispatch.md` | create | parallel | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| F-02 | `config/artifact_registry.json` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| I-01 | `scripts/check_absolute_paths.py` | modify | parallel | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| I-02 | `scripts/upstream_outbox.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| I-03 | `scripts/upstream_outbox.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| I-04 | `scripts/upstream_outbox.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| I-05 | `scripts/upstream_outbox.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| I-06 | `hooks/on_commit.py` | modify | parallel | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| I-07 | `scripts/check_fix_reproduces.py` | modify | parallel | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| K-01 | `config/invocation_exceptions.json` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| K-02 | `scripts/detect_drift.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| K-03 | `tests/test_detect_drift.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| K-04 | `agents.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| L-01 | `scripts/graph_update.py` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| L-02 | `Makefile` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| L-03 | `rules/graphify.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| L-04 | `rules/project_topology.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| L-05 | `agents.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| I-08 | `scripts/check_task_scope.py` | modify (replaced by M-02, D37) | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| I-09 | `scripts/check_gate_log.py` | modify (replaced by M-03, D37) | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| I-10 | `skills/token-saver-auditor/scripts/audit_plan.py` | modify (replaced by M-04, D37) | sequential | `skill_architect` | N/A | `agents/skill_architect.md` |

### Close

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Z-01 | `CHANGELOG.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| Z-02 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |

## Disagreements with the plan

Every overwrite below follows one cause: the proposed assignee declares no
`Write`/`Edit` tool in its `agents/<role>.md` frontmatter, so it cannot perform
the `create`/`modify` the row assigns it, and `scripts/check_task_scope.py`
(`_capability_findings`) exits 2 on that row. The proposed role keeps its
function as owner or measurer and hands literal output to the single writer, so
each file has exactly one writer.

| # | Plan proposal | Assignee here | Reason |
| :--- | :--- | :--- | :--- |
| A-00 | `token_economy_agent` | `doc_orchestrator` | `agents/token_economy_agent.md` declares `Read, Glob, Grep, Bash`. `token_economy_agent` runs the measurements (`session_cost.py --json`, transcript-to-commit cost attribution) with `Bash` and returns literal output; `doc_orchestrator` writes the study. |
| A-07 | `principal_agent` (owner) / `doc_orchestrator` (writer) | `doc_orchestrator` | Plan already names `doc_orchestrator` as writer (`ADR-0017`); `principal_agent` declares no `Write`/`Edit`. The Assignee cell carries the writer. |
| H-01 | `token_economy_agent` | `implementer_agent` | Same tool gap as A-00. `token_economy_agent` supplies each figure with its A-00 source; `implementer_agent` writes the JSON, as it writes `config/model_tiers.json` in A-08. |
| C-01 | `devops_agent` | `doc_orchestrator` | `agents/devops_agent.md` declares `Read, Glob, Grep, Bash`. `devops_agent` runs the `RA-19` measurements with `Bash` and returns literal output; `doc_orchestrator` writes `SANDBOX_ENUMERATION.md` (Sprint 058 `D-02` precedent). Any secret-needing or `gh` command is prepared for the human (`RA-09`), except the read-only `gh` commands of the C-01 viability measurement (human decision 2026-11-08). |
| D-01 | `principal_agent` (owner) / `doc_orchestrator` (writer) | `doc_orchestrator` | As A-07. |
| F-01 | `principal_agent` (owner) / `doc_orchestrator` (writer) | `doc_orchestrator` | As A-07. |

All other rows: the plan proposal stands. B-07, E-01c and H-03 were added to the plan by the Phase 4.3 resolutions (F-3, F-5); D-04 targets `claude/settings.hooks.json` and runs before E-01b on the same file (F-1).
