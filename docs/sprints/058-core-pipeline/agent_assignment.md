# Agent Assignment — Sprint 058 (upstream-channel-and-reproduce-first)

Source: `docs/sprints/058-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`).
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

**Agent-profile creation this sprint: none.** No row creates a file under `agents/`, `.claude/agents/` or a profile path. B-12 modifies the existing `agents/qa_agent.md`. Every `Destination` below is `N/A`.

---

## Staffing

One table per wave. Shape is mandatory:

`# | Target | Operation | Mode | Assignee | Destination | Ruleset file`

### Wave A — upstream channel (D1-D4)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| A-01 | `docs/standards/templates/UPSTREAM_OUTBOX_TEMPLATE.json` | create | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-02 | `scripts/upstream_outbox.py` | create (paired test `tests/test_upstream_outbox.py`) | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A-03 | `config/upstream_intake.json` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A-04 | `scripts/upstream_intake.py` | create (paired test `tests/test_upstream_intake.py`) | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A-05 | `.gitignore` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A-06 | `scripts/session_start.py` | modify (paired test `tests/test_session_start.py`) | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A-07 | `.github/ISSUE_TEMPLATE/host-finding.yml` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A-08 | `.github/workflows/host-finding-intake.yml` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A-09 | `scripts/sync_agents_pin.py` | modify (paired test `tests/test_sync_agents_pin.py`) | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A-10 | `docs/standards/templates/CHANGELOG_TEMPLATE.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-11 | `agents.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| A-12 | `workflows/extract_workflow.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-13 | `workflows/pipeline_workflow.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-14 | `workflows/close_workflow.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-15 | `docs/guides/SELF_IMPROVEMENT_GUIDE.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-16 | `SECURITY.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-17 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |

### Wave C — Known Issues of Sprint 057 (D6)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| C-01 | `scripts/_md_table.py` | create (paired test `tests/test_md_table.py`) | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C-02 | `scripts/check_task_scope.py` | refactor (`tests/test_check_task_scope.py` unchanged and green) | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C-03 | `scripts/check_gate_log.py` | modify, fix `KI-057-3` (paired test `tests/test_check_gate_log.py`) | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C-04 | `scripts/check_forge_ladder.py` | modify, fix `KI-057-3` (paired test `tests/test_check_forge_ladder.py`) | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C-05 | `scripts/detect_new_models.py` | modify, fix `KI-057-3` (new paired test `tests/test_detect_new_models.py`) | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C-06 | `claude/settings.hooks.json` | modify (paired test `tests/test_template_sandbox.py`) | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C-07 | `scripts/merge_json.py` | modify (paired test `tests/test_merge_json.py`) | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C-08 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| C-09 | `scripts/session_state.py` | modify, fix `KI-057-6` (paired test `tests/test_session_state.py`) | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |

### Wave B — reproduce-first rules (D5)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| B-01 | `rules/qa_and_testing.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| B-02 | `rules/code_craft.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| B-03 | `docs/standards/templates/SPRINT_LOG_TEMPLATE.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| B-04 | `scripts/check_gate_log.py` | modify (paired test `tests/test_check_gate_log.py`) | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| B-05 | `scripts/check_remediation_chain.py` | create (paired test `tests/test_check_remediation_chain.py`) | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| B-06 | `hooks/on_commit.py` | modify (paired test `tests/test_on_commit.py`) | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| B-07 | `config/blast_radius.json` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| B-08 | `skills/token-saver-auditor/scripts/audit_plan.py` | modify (paired test `tests/test_token_saver_auditor.py` is a companion, not a second subject) | sequential | `skill_architect` | N/A | `agents/skill_architect.md` |
| B-09 | `scripts/check_plan_closure.py` | create (paired test `tests/test_check_plan_closure.py`) | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| B-10 | `workflows/close_workflow.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| B-11 | `workflows/pipeline_workflow.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| B-12 | `agents/qa_agent.md` | modify (existing profile, no creation) | sequential | `agent_orchestrator` | N/A | `agents/agent_orchestrator.md` |
| B-13 | `scripts/check_fix_reproduces.py` | modify (paired test `tests/test_check_fix_reproduces.py`) | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| B-14 | `scripts/check_fix_reproduces.py` | modify (paired test `tests/test_check_fix_reproduces.py`) | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| B-15 | `agents.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |

### Wave D — Dependabot (D7)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| D-01 | `requirements-skillopt.txt` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| D-02 | `docs/sprints/058-core-pipeline/GRAPHIFY_09_MEASUREMENT.md` | create (writer; `devops_agent` runs measurements (a)-(c) with `Bash` beforehand and hands the literal output over) | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| D-03 | `requirements-core.txt` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| D-04 | `Makefile` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| D-05 | `rules/graphify.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| D-06 | `rules/project_topology.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| D-07 | `config/with_env_allowlist.json` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |

## Disagreements with the plan

None.

Notes on rows where the proposal stands:

| # | Note |
| :--- | :--- |
| D-02 | Proposal stands. `doc_orchestrator` holds `Write` and is the writer. `devops_agent` is not the row assignee: it only runs the measurements (a)-(c) through `Bash` and returns literal output, so the file has exactly one writer. Any secret-needing command is prepared for the human (`RA-09`). |
| B-08 | Proposal stands. `skill_architect` owns `skills/[name]/scripts/`. The paired `tests/test_token_saver_auditor.py` is the mandatory companion of a `fix(`/behavior change and not an independent subject (`jurisdictional_lock`). |
| A-07, A-08 | Proposal stands. `.github/` is outside the `scripts/`, `hooks/`, `tests/` trees but A-08 is executable CI code; `implementer_agent` is the only code-authoring profile with `Write`. |
| A-11, B-15, B-01, B-02, D-05, D-06 | Proposal stands. `rule_validator` holds `Write`/`Edit` and owns indexing systemic rule changes into `agents.md` and `rules/`. |
| B-12 | Proposal stands. Edits an existing profile only; no creation, so no `Destination`. |
| Same-file rows | `agents.md` (A-11, B-15), `workflows/pipeline_workflow.md` (A-13, B-11), `workflows/close_workflow.md` (A-14, B-10), `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` (A-17, C-08), `scripts/check_gate_log.py` (C-03, B-04) and `scripts/check_fix_reproduces.py` (B-13, B-14) share a subject across rows. They run sequentially in the plan's order (A, C, B, D), never concurrently (`no_interference`). |
