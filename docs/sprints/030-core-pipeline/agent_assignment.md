# Agent Assignment — Sprint 030 (`token-economy-enforcement`)

Source: `docs/sprints/030-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`).
Mode: **Cursor**, `delegation_mode: sequential` — the `Assignee` column names
which profile's ruleset the single session adopts for that write
(`workflows/pipeline_workflow.md` Phase 4.1).

## Scope of this artifact (Phase 4.1 only)

| Owns | Does **not** own |
| :--- | :--- |
| Which ruleset governs each unit | Cursor model / effort (`task_scope.md`) |
| Agent-forge destination field on units that create agents | `tier_escalation` proposals |

**No unit creates an agent profile.** Destination column: N/A.

## Declared condition — `F-021-A2` (open, out of scope)

`devops_agent` remains sole `Write`/`Edit` holder for framework-root `scripts/`
and `hooks/` (`agents.md §6`). Script and test units stay on `devops_agent`.
Gate profiles remain read-only (`F-026-A1`).

---

## Ola 0 — Tests

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| A0 | `tests/test_token_saver_auditor.py` | create | sequential / ruleset | `devops_agent` — deviation (tests/) | `agents/devops_agent.md` |
| T0 | `tests/test_check_task_scope.py` | create | sequential / ruleset | `devops_agent` — deviation (tests/) | `agents/devops_agent.md` |
| C0 | `tests/test_session_protocol.py` | modify | sequential / ruleset | `devops_agent` — deviation (tests/) | `agents/devops_agent.md` |

## Ola 1 — Auditor

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| A1 | `skills/token-saver-auditor/scripts/__init__.py` | create | sequential / ruleset | `skill_architect` | `agents/skill_architect.md` |
| A2 | `skills/token-saver-auditor/scripts/audit_plan.py` | create | sequential / ruleset | `devops_agent` | `agents/devops_agent.md` |
| A3 | `skills/token-saver-auditor/SKILL.md` | modify | sequential / ruleset | `token_economy_agent` | `agents/token_economy_agent.md` |
| A4 | `skills/token-saver-auditor/README.md` | modify | sequential / ruleset | `skill_architect` | `agents/skill_architect.md` |

## Ola 2 — Consumo

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| C1 | `scripts/session_cost.py` | modify | sequential / ruleset | `devops_agent` | `agents/devops_agent.md` |
| C2 | `scripts/session_probe.py` | modify | sequential / ruleset | `devops_agent` | `agents/devops_agent.md` |
| C3 | `config/rule_triggers.json` | modify | sequential / ruleset | `devops_agent` | `agents/devops_agent.md` |
| C4 | `rules/token_economy.md` | modify | sequential / ruleset | `token_economy_agent` | `agents/token_economy_agent.md` |
| C5 | `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md` | modify | sequential / ruleset | `governance_learner` | `agents/governance_learner.md` |
| C6 | `agents.md` | modify | sequential / ruleset | `governance_learner` | `agents/governance_learner.md` |

## Ola 3 — F-026-A2

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| F1 | `scripts/check_task_scope.py` | create | sequential / ruleset | `devops_agent` | `agents/devops_agent.md` |
| F2 | `agents/rule_validator.md` | modify | sequential / ruleset | `rule_validator` | `agents/rule_validator.md` |
| F3 | `agents/token_economy_agent.md` | modify | sequential / ruleset | `token_economy_agent` | `agents/token_economy_agent.md` |
| F4 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify | sequential / ruleset | `governance_learner` | `agents/governance_learner.md` |

## Ola 4 — Invocadores

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| I1 | `workflows/pipeline_workflow.md` | modify | sequential / ruleset | `orchestrator` | `agents/orchestrator.md` |
| I2 | `workflows/close_workflow.md` | modify | sequential / ruleset | `orchestrator` | `agents/orchestrator.md` |
| I3 | `Makefile` | modify | sequential / ruleset | `devops_agent` | `agents/devops_agent.md` |

## Ola 5 — Protocolo y ledger

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| E1 | `docs/guides/MODEL_TIER_TRIAL_GUIDE.md` | create | sequential / ruleset | `doc_orchestrator` | `agents/doc_orchestrator.md` |
| E2 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | sequential / ruleset | `orchestrator` | `agents/orchestrator.md` |
| L1 | `CHANGELOG.md` | modify | sequential / ruleset | `principal_agent` | `agents/principal_agent.md` |

## Quality Gate (Phase 7) — transcription

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| G1.q | verdict → `SPRINT_LOG.md` | emit | sequential | `qa_agent` | `agents/qa_agent.md` |
| G1.q | verdict → `SPRINT_LOG.md` | transcribe | sequential | `orchestrator` | `agents/orchestrator.md` |
| G1.t | verdict → `SPRINT_LOG.md` | emit | sequential | `tester_agent` | `agents/tester_agent.md` |
| G1.t | verdict → `SPRINT_LOG.md` | transcribe | sequential | `orchestrator` | `agents/orchestrator.md` |
