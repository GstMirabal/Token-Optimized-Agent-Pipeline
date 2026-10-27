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

### Wave A — criteria and scale

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| W00 | `docs/guides/PROMPT_CRITERIA_GUIDE.md` | create | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| W07 | `rules/qa_and_testing.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| W08 | `docs/standards/templates/SPRINT_LOG_TEMPLATE.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| W09 | `scripts/check_gate_log.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |

### Wave B — S0 lane (W01 blocks W02-W06)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| W01 | `docs/sprints/057-core-pipeline/SANDBOX_DB_MEASUREMENT.md` | create | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| W02 | `claude/settings.hooks.json` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W03 | `scripts/env_agent_check.py` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W04 | `scripts/db_probe.py` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W05 | `rules/project_topology.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| W06 | `agents.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |

### Wave C — block 1 defects

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

### Wave D — S3 residues and documentation

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| W33 | `skills/mcp-registry/registry.json` | modify | sequential | `skill_architect` | N/A | `agents/skill_architect.md` |
| W34 | `tests/test_mcp_template.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W35 | `memory_index.json` | modify | sequential | `governance_learner` | N/A | `agents/governance_learner.md` |
| W36 | `scripts/install.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W37 | `skills/env-shielding-auditor/README.md` | modify | sequential | `skill_architect` | N/A | `agents/skill_architect.md` |

### Added in execution — W38, W39 (human decision 2026-10-24)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| W38 | `scripts/session_state.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W39 | `.github/workflows/ci.yml` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |

### Wave E — `install.sh` residue (`KI-057-5`, human decision 2026-10-25)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| W40 | `scripts/session_start.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W41 | `scripts/bridge_state.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W42 | `scripts/_root.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W43 | `tests/test_root_resolution.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W44 | `scripts/merge_json.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W45 | `claude/settings.hooks.json` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W46 | `config/invocation_exceptions.json` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W47 | `.gitignore` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W48 | `workflows/start_workflow.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| W49 | `workflows/deployment_workflow.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| W50 | `rules/project_topology.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| W51 | `docs/guides/AUTONOMY_POSTURE_GUIDE.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| W52 | `docs/guides/SELF_IMPROVEMENT_GUIDE.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| W53 | `docs/standards/templates/SYSTEM_OVERVIEW_TEMPLATE.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| W54 | `docs/architecture/global_topology.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| W55 | `docs/architecture/topology_map.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| W56 | `profiles/example-project/README.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| W57 | `.github/ISSUE_TEMPLATE/bug_report.yml` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| W58 | `skills/slash-commander/README.md` | modify | sequential | `skill_architect` | N/A | `agents/skill_architect.md` |
| W59 | `skills/slash-commander/SKILL.md` | modify | sequential | `skill_architect` | N/A | `agents/skill_architect.md` |

### Wave F — Gate 1 round 1 remediation (human decision 2026-10-26)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| W60 | `scripts/session_state.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W61 | `scripts/_repro_grammar.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W62 | `scripts/check_fix_reproduces.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W63 | `scripts/check_fix_reproduces.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W64 | `hooks/on_commit.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W65 | `rules/code_craft.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| W66 | `agents.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| W67 | `scripts/install_claude.sh` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W68 | `docs/sprints/057-core-pipeline/task_scope.md` | modify | sequential | `orchestrator` | N/A | `agents/orchestrator.md` |
| W69 | `scripts/session_start.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W70 | `scripts/check_changelog_tags.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W71 | `scripts/check_changelog_tags.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W72 | `scripts/py_compile_tree.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W73 | `scripts/check_role_artifact.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W74 | `workflows/pipeline_workflow.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| W75 | `workflows/remediation_workflow.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| W76 | `workflows/deployment_workflow.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |

### Wave G — Gate 1 round 2 remediation (human decision 2026-10-26)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| W77 | `tests/test_session_state.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W78 | `agents/implementer_agent.md` | modify | sequential | `agent_orchestrator` | N/A | `agents/agent_orchestrator.md` |
| W79 | `agents/rule_validator.md` | modify | sequential | `agent_orchestrator` | N/A | `agents/agent_orchestrator.md` |
| W80 | `memory_index.json` | modify | sequential | `governance_learner` | N/A | `agents/governance_learner.md` |
| W81 | `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| W82 | `workflows/pipeline_workflow.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| W83 | `hooks/on_commit.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W84 | `scripts/_repro_grammar.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W85 | `tests/test_check_changelog_tags.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W86 | `docs/sprints/057-core-pipeline/agent_assignment.md` | modify | sequential | `orchestrator` | N/A | `agents/orchestrator.md` |
| W87 | `docs/sprints/057-core-pipeline/task_scope.md` | modify | sequential | `orchestrator` | N/A | `agents/orchestrator.md` |
| W88 | `tests/test_fix_route_wording.py` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |

### Wave H — Gate 1 round 3 record remediation (human decision 2026-10-26)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| W89 | `tests/test_code_craft_gates.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W90 | `hooks/on_commit.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W91 | `tests/test_session_state.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W92 | `docs/sprints/057-core-pipeline/task_scope.md` | modify | sequential | `orchestrator` | N/A | `agents/orchestrator.md` |

### Wave I — Gate 1 round 4 record remediation (human decision 2026-10-26)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| W93 | `hooks/on_commit.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W94 | `tests/test_code_craft_gates.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |

### Wave J — Gate 1 round 5 record remediation (human decision 2026-10-26)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| W95 | `hooks/on_commit_msg.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W96 | `hooks/on_commit.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W97 | `hooks/on_commit_msg.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W98 | `tests/test_code_craft_gates.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W99 | `tests/test_code_craft_gates.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |

### Wave K — Gate 1 round 6 record remediation (human decision 2026-10-26)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| W100 | `hooks/on_commit.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W101 | `CONTRIBUTING.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| W102 | `tests/test_code_craft_gates.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| W103 | `tests/test_code_craft_gates.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |

## Disagreements with the plan

| # | Plan proposed | Assigned | Reason |
| :--- | :--- | :--- | :--- |
| W01 | `devops_agent` | `doc_orchestrator` (authorship of the markdown file) | `agents/devops_agent.md` declares `tools: Read, Glob, Grep, Bash` with no `Write` or `Edit`, so it cannot create `SANDBOX_DB_MEASUREMENT.md`. `devops_agent` remains the role that RUNS the headless `claude -p` sessions for cases M1-M3 (at most 6 calls, via `Bash`) and hands the literal output of each case to `doc_orchestrator`, which writes the file without altering the output text. |

All other 37 proposals stand. Ownership checks: every path under `scripts/`,
`hooks/`, `tests/`, `claude/` and `Makefile` is `implementer_agent` (none is
`devops_agent`); `rules/` and `agents.md` are `rule_validator`; `workflows/` and
`docs/` prose are `doc_orchestrator`; `skills/[name]/` is `skill_architect`;
`memory_index.json` is `governance_learner`.
