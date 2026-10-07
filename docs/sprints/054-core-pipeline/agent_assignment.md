# Agent Assignment — Sprint 054 (core-pipeline)

Source: `docs/sprints/054-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`).
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

---

## Staffing

One table per wave. Shape is mandatory:

`# | Target | Operation | Mode | Assignee | Destination | Ruleset file`

### Wave 0 — intake records

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| W01 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| W02 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |

### Wave A — gates that pass without measuring

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| A01 | `scripts/quality_audit.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A02 | `hooks/on_commit.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A03 | `scripts/check_fix_reproduces.py` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A04 | `agents/qa_agent.md` | modify | sequential | `agent_orchestrator` | N/A | `agents/agent_orchestrator.md` |
| A05 | `rules/qa_and_testing.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| A06 | `rules/code_craft.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| A07 | `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A08 | `skills/token-saver-auditor/scripts/audit_plan.py` | modify | sequential | `skill_architect` | N/A | `agents/skill_architect.md` |
| A09 | `workflows/pipeline_workflow.md` | modify | sequential | `orchestrator` | N/A | `agents/orchestrator.md` |
| A10 | `docs/standards/templates/NOTICE_TEMPLATE.md` | create | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A11 | `workflows/close_workflow.md` | modify | sequential | `orchestrator` | N/A | `agents/orchestrator.md` |
| A12 | `workflows/standardization_workflow.md` | modify | sequential | `orchestrator` | N/A | `agents/orchestrator.md` |
| A13 | `config/template_gates.json` | modify | sequential | `orchestrator` | N/A | `agents/orchestrator.md` |

### Wave B — session and sprint state

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| B01 | `scripts/session_state.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| B02 | `scripts/session_state.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| B03 | `scripts/session_state.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| B04 | `scripts/install_lock.py` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| B05 | `scripts/session_start.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| B06 | `commands/start.md` | modify | sequential | `orchestrator` | N/A | `agents/orchestrator.md` |
| B07 | `workflows/start_workflow.md` | modify | sequential | `orchestrator` | N/A | `agents/orchestrator.md` |
| B08 | `workflows/pipeline_workflow.md` | modify | sequential | `orchestrator` | N/A | `agents/orchestrator.md` |

### Wave C — supply chain

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| C01 | `agents.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| C02 | `rules/code_craft.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| C03 | `README.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| C04 | `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` | modify (regenerate via `scripts/map_workflows.py`) | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |

### Wave Z — sprint records (Phase 8)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Z01 | `docs/sprints/054-core-pipeline/PHASE_REGISTER.md` | create | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| Z02 | `CHANGELOG.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| Z03 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| Z04 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |

No unit creates an agent profile; `Destination` is `N/A` on every row.

## Disagreements with the plan

One override (C04); the other 30 proposals stand (31 units). Each proposed
profile's `tools:` grant was checked against its write: `implementer_agent`,
`doc_orchestrator`, `orchestrator`, `rule_validator`, `agent_orchestrator` and
`skill_architect` all hold `Write`/`Edit`; no unit is assigned to `principal_agent`
or a read-only gate agent; every unit whose subject is under framework-root
`scripts/` or `hooks/` is `implementer_agent` (`ADR-0009`).

| Unit | Proposed | Assigned | Reason |
| :--- | :--- | :--- | :--- |
| C04 | `orchestrator` | `implementer_agent` | The unit is a script run (`python3 scripts/map_workflows.py`), and the guide is generated, never hand-edited (`agents.md §0`). `orchestrator`'s `tools:` grant is `Read, Glob, Grep, Write, Edit` with no `Bash`, so it can only hand-edit the file, which is prohibited. `implementer_agent` is the profile that holds both `Bash` and `Write`/`Edit` and owns the `scripts/` tree; `devops_agent` has `Bash` but no `Write`/`Edit`. |

Notes (not overrides):

| Unit | Note |
| :--- | :--- |
| A08 | Subject is `skills/token-saver-auditor/scripts/audit_plan.py`, so `skill_architect` (`skills/[name]/scripts/`). Its paired test `tests/test_token_saver_auditor.py` is a mandatory companion, not a separate subject (`§2 jurisdictional_lock`); `skill_architect` holds `Write`/`Edit` and authors it in the same commit. |
| A04 | `agents/qa_agent.md` is an agent profile, which is `agent_orchestrator`'s charter. Editing, not creating: no `Destination`. |
| A02, A03 | Paired tests under `tests/` are companions of the `scripts/`/`hooks/` subject, authored by the same `implementer_agent`. |
| A13 | Lands right after A10 (plan ordering constraint). |
| C03 | Follows C01 (`RA-14` propagation of the `§8` key spelling). |
| C04 | Runs after A09, A11, A12, B07 and B08, as the plan's ordering table requires. |
| W01, Z03 and W02, Z04 | Same subject in sequence (Wave 0 then Wave Z), never concurrent (`no_interference`). |
