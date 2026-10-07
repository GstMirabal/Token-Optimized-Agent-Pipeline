# Agent Assignment — Sprint 055 (sandbox-restrictions-and-secret-path)

Source: `docs/sprints/055-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`).
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

No new agent profile is created in Sprint 055: all 19 units are staffed from
the existing profiles in `agents/`, so every `Destination` is `N/A`.

---

## Staffing

### Wave 1 — measurement (human-launched)

`U01` is a measurement. The human launches a sandboxed session from the nucleus
with `claude --settings claude/settings.hooks.json`, runs every matrix command
there, and the human reports command, exit code and error signature per row.
`doc_orchestrator` does not run the commands: it only transcribes the
human-reported results into `SANDBOX_MEASUREMENT.md`. No correction unit
(`U02`..`U19`) starts before `U01` is committed (`D1`).

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U01 | `docs/sprints/055-core-pipeline/SANDBOX_MEASUREMENT.md` | create | sequential (human runs commands; assignee transcribes) | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |

### Wave 2 — wrapper and config

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U02 | `scripts/with_env.py` (+ `tests/test_with_env.py`) | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U03 | `config/with_env_allowlist.json` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |

### Wave 3 — installer, hook settings, Makefile

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U04 | `scripts/merge_json.py` (+ `tests/test_merge_json.py`) | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U05 | `scripts/install.py` (+ `tests/test_install_permission.py`) | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U06 | `scripts/session_start.py` (+ `tests/test_session_start.py`) | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U07 | `claude/settings.hooks.json` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U08 | `Makefile` (+ `tests/test_makefile_graphify.py`) | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |

### Wave 4 — rules, skill, workflows, concordance

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U09 | `rules/project_topology.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| U10 | `rules/qa_and_testing.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| U11 | `rules/graphify.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| U12 | `skills/graphify/SKILL.md` | modify (omitted if vendored) | sequential | `skill_architect` | N/A | `agents/skill_architect.md` |
| U13 | `agents.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| U14 | `workflows/pipeline_workflow.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| U15 | `workflows/deployment_workflow.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| U16 | `workflows/repository_hardening_workflow.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| U17 | `rules/LEGACY_RULE_CONCORDANCE.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |

### Wave 5 — closure records

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U18 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| U19 | `CHANGELOG.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| U20 | `agents/devops_agent.md` | modify | sequential | `agent_orchestrator` | N/A | `agents/agent_orchestrator.md` |
| U21 | `README.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |

## Disagreements with the plan

None. Every `Assignee (proposed)` in the plan stands. One clarification on
`U01`: the plan's note "lanza el humano" is recorded here as the execution
rule — the human runs the sandboxed commands, `doc_orchestrator` only
transcribes the results.
