# Agent Assignment — Sprint 057 (core-pipeline)

Source: `docs/sprints/057-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`).
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

Sprint 057 creates no agent profile: all 14 existing profiles in `agents/*.md`
cover the 38 units, so `Destination` is `N/A` on every row.

---

## Staffing

### Ola A — criteria and scale

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| W00 | `docs/guides/PROMPT_CRITERIA_GUIDE.md` | create | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| W07 | `rules/qa_and_testing.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| W08 | `docs/standards/templates/SPRINT_LOG_TEMPLATE.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| W09 | `scripts/check_gate_log.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |

### Ola B — S0 lane (W01 blocks W02-W06)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| W01 | `docs/sprints/057-core-pipeline/SANDBOX_DB_MEASUREMENT.md` | create | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| W02 | `claude/settings.hooks.json` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W03 | `scripts/env_agent_check.py` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W04 | `scripts/db_probe.py` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W05 | `rules/project_topology.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| W06 | `agents.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |

### Ola C — block 1 defects

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| W10 | `scripts/session_state.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W11 | `workflows/deployment_workflow.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| W12 | `scripts/session_state.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W13 | `scripts/session_end_hook.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W14 | `scripts/py_compile_tree.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W15 | `scripts/_repro_grammar.py` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W16 | `hooks/on_commit.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W17 | `scripts/check_fix_reproduces.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W18 | `scripts/check_fix_reproduces.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W19 | `scripts/check_task_scope.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W20 | `scripts/model_ledger.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W21 | `scripts/detect_drift.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W22 | `workflows/reconciliation_workflow.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| W23 | `scripts/session_start.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W24 | `scripts/check_role_artifact.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W25 | `scripts/session_state.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W26 | `scripts/extract_plan.py` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W27 | `workflows/pipeline_workflow.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| W28 | `scripts/session_state.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W29 | `workflows/remediation_workflow.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| W30 | `scripts/merge_json.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W31 | `scripts/check_changelog_tags.py` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W32 | `Makefile` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |

### Ola D — S3 residues and documentation

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| W33 | `skills/mcp-registry/registry.json` | modify | sequential | `skill_architect` | N/A | `agents/skill_architect.md` |
| W34 | `tests/test_mcp_template.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W35 | `memory_index.json` | modify | sequential | `governance_learner` | N/A | `agents/governance_learner.md` |
| W36 | `scripts/install.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W37 | `skills/env-shielding-auditor/README.md` | modify | sequential | `skill_architect` | N/A | `agents/skill_architect.md` |

## Disagreements with the plan

| # | Plan proposed | Assigned | Reason |
| :--- | :--- | :--- | :--- |
| W01 | `devops_agent` | `doc_orchestrator` (authorship of the markdown file) | `agents/devops_agent.md` declares `tools: Read, Glob, Grep, Bash` with no `Write` or `Edit`, so it cannot create `SANDBOX_DB_MEASUREMENT.md`. `devops_agent` remains the role that RUNS the headless `claude -p` sessions for cases M1-M3 (at most 6 calls, via `Bash`) and hands the literal output of each case to `doc_orchestrator`, which writes the file without altering the output text. |

All other 37 proposals stand. Ownership checks: every path under `scripts/`,
`hooks/`, `tests/`, `claude/` and `Makefile` is `implementer_agent` (none is
`devops_agent`); `rules/` and `agents.md` are `rule_validator`; `workflows/` and
`docs/` prose are `doc_orchestrator`; `skills/[name]/` is `skill_architect`;
`memory_index.json` is `governance_learner`.
