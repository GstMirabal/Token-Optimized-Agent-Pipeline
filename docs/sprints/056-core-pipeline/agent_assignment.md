# Agent Assignment — Sprint 056 (core-pipeline)

Source: `docs/sprints/056-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`).
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
Units that do not create a profile use `N/A`. No unit in Sprint 056 creates an
agent profile, so every row is `N/A` and no new profile is authored.

Rows that share a structural subject (`agents.md`: A8, A16, B7; `scripts/quality_audit.py`: A6, A7; `scripts/verify_references.py`: A2, A3; `scripts/install.py`: A9, A10, B5; `rules/project_topology.md`: A15, B6; `tests/test_install_with_env_render.py`: A12 and the paired tests of A9, A10, B5; `SANDBOX_ENUMERATION.md`: B1, B4) are `sequential` by `agents.md §2 no_interference`: the later row starts only after the earlier one has landed.

---

## Staffing

### Wave A

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| A1 | `scripts/docs_freshness_check.py` (+ paired test) | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A2 | `scripts/verify_references.py` (+ paired test) | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A3 | `scripts/verify_references.py` (+ paired test) | modify | sequential (after A2) | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A4 | `tests/test_root_resolution.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A5 | `skills/env-shielding-auditor/README.md` | modify | sequential | `skill_architect` | N/A | `agents/skill_architect.md` |
| A6 | `scripts/quality_audit.py` (+ paired test) | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A7 | `scripts/quality_audit.py` (+ paired test) | modify | sequential (after A6) | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A8 | `agents.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| A9 | `scripts/install.py` (+ paired test) | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A10 | `scripts/install.py` (+ paired test) | modify | sequential (after A9) | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A11 | `tests/test_template_sandbox.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A12 | `tests/test_install_with_env_render.py` | modify | sequential (after A9, A10) | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A13 | `scripts/session_state.py` (+ paired test) | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A14 | `workflows/audit_workflow.md` | modify | sequential (after A13) | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A15 | `rules/project_topology.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| A16 | `agents.md` | modify | sequential (after A8, A15) | `rule_validator` | N/A | `agents/rule_validator.md` |
| A17 | `workflows/deployment_workflow.md` | modify | sequential (after A15) | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A18 | `rules/qa_and_testing.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| A19 | `workflows/pipeline_workflow.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A20 | `docs/standards/templates/README_TEMPLATE.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A21 | `agents/devops_agent.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |

### Wave B

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| B1 | `docs/sprints/056-core-pipeline/SANDBOX_ENUMERATION.md` | create | sequential | `doc_orchestrator` (writes the document; the `claude -p` measurement is run by the parent session, since `principal_agent` holds no `Bash`/`Write` — `task_scope.md` F-1) | N/A | `agents/principal_agent.md`; `agents/doc_orchestrator.md` |
| B2 | `claude/settings.hooks.json` (+ `tests/test_template_sandbox.py`) | modify | sequential (after B1) | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| B3 | `claude/mcp.json` (+ MCP template test) | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| B4 | `docs/sprints/056-core-pipeline/SANDBOX_ENUMERATION.md` | modify | sequential (after B1, B2, B3) | `doc_orchestrator` (writes the document; the `claude -p` measurement is run by the parent session, since `principal_agent` holds no `Bash`/`Write` — `task_scope.md` F-1) | N/A | `agents/principal_agent.md`; `agents/doc_orchestrator.md` |
| B5 | `scripts/install.py` (+ paired test) | modify | sequential (after A9, A10) | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| B6 | `rules/project_topology.md` | modify | sequential (after A15, B4) | `rule_validator` | N/A | `agents/rule_validator.md` |
| B7 | `agents.md` | modify | sequential (after A16, B2, B4) | `rule_validator` | N/A | `agents/rule_validator.md` |
| B8 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify | sequential (after B4) | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| B9 | `scripts/session_start.py` (+ `tests/test_session_start.py`) | modify | parallel | `implementer_agent` | N/A | `agents/implementer_agent.md` |

## Disagreements with the plan

| # | Proposed | Assigned | Reason |
| :--- | :--- | :--- | :--- |
| A5 | `doc_orchestrator` | `skill_architect` | The target sits inside `skills/env-shielding-auditor/`, an executable skill governed by the Three-File Standard (`agents.md §3 three_file_standard`). `skill_architect` owns skill content under `skills/[name]/`; `doc_orchestrator` owns docs, workflows, templates and agent profiles, not skill directories. |

Rows where the plan's assignee stands but the plan text needed a decision recorded:

| # | Decision |
| :--- | :--- |
| B1, B4 | Two roles are recorded per row, as the plan proposed. `principal_agent` runs the measurement (headless `claude -p` sandbox runs, one case per call, fixture host with a fixture `.env` value). `doc_orchestrator` materializes the measured results into `SANDBOX_ENUMERATION.md` and records no result it was not handed. Neither role edits the other's output; B4 starts only after B2 and B3 have landed. |
| B2, B3 | `claude/settings.hooks.json` and `claude/mcp.json` are outside `scripts/`, `hooks/` and `tests/`, so `ADR-0009` does not assign them by path. `implementer_agent` is kept because (1) each unit is a `fix(` commit that must carry a paired test under `tests/` (`rules/code_craft.md §6`), and only `implementer_agent` holds `Write`/`Edit` there, so a second writer would split one commit across two profiles; (2) both files are machine-read templates consumed by `scripts/install.py` and by hook and test code, so the change is code-class rather than prose; (3) `devops_agent` is rejected because it holds no `Write`/`Edit` for the tests and its charter is environment and Docker health; (4) `doc_orchestrator` is rejected because the content is a security-relevant JSON template, not documentation. The structural subject of each commit is the JSON file; the test is the mandatory companion, not a second subject. |
| A8, A16, B7 | Same file `agents.md`, same profile `rule_validator`. Order A8, then A16, then B7, so no two tasks claim it at once. |
| A15, B6 | Same file `rules/project_topology.md`, same profile `rule_validator`. A15 lands before B6. |
