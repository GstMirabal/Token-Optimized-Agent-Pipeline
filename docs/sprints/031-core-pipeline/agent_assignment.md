# Agent Assignment — Sprint 031 (`gate-verdict-classes`)

Source: `docs/sprints/031-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`).
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
and `hooks/` (`agents.md §6`). Script, Makefile, and test units stay on
`devops_agent`. Gate profiles remain read-only for product writes (`F-026-A1`);
R2/R3 modify those profiles' own instructing text.

---

## Ola 0 — Tests

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T1 | `tests/test_check_gate_log.py` | create | sequential / ruleset | `devops_agent` — deviation (tests/) | `agents/devops_agent.md` |

## Ola 1 — Documents that instruct

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| R1 | `rules/qa_and_testing.md` | modify | sequential / ruleset | `governance_learner` | `agents/governance_learner.md` |
| R2 | `agents/qa_agent.md` | modify | sequential / ruleset | `qa_agent` | `agents/qa_agent.md` |
| R3 | `agents/tester_agent.md` | modify | sequential / ruleset | `tester_agent` | `agents/tester_agent.md` |
| R4 | `workflows/pipeline_workflow.md` | modify | sequential / ruleset | `governance_learner` | `agents/governance_learner.md` |
| R5 | `workflows/remediation_workflow.md` | modify | sequential / ruleset | `governance_learner` | `agents/governance_learner.md` |
| R6 | `agents/orchestrator.md` | modify | sequential / ruleset | `orchestrator` | `agents/orchestrator.md` |
| R7 | `agents.md` | modify | sequential / ruleset | `governance_learner` | `agents/governance_learner.md` |

## Ola 2 — Mechanism

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| M1 | `scripts/check_gate_log.py` | create | sequential / ruleset | `devops_agent` | `agents/devops_agent.md` |
| M2 | `Makefile` | modify | sequential / ruleset | `devops_agent` | `agents/devops_agent.md` |
| M3 | `workflows/close_workflow.md` | modify | sequential / ruleset | `governance_learner` | `agents/governance_learner.md` |

## Ola 3 — Documentary (not closeout ledger)

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| D1 | `docs/decisions/ADR-0008-gate-verdict-classes.md` | create | sequential / ruleset | `doc_orchestrator` | `agents/doc_orchestrator.md` |
| D2 | `docs/guides/MODEL_TIER_TRIAL_GUIDE.md` | modify | sequential / ruleset | `doc_orchestrator` | `agents/doc_orchestrator.md` |
| D3 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | sequential / ruleset | `doc_orchestrator` | `agents/doc_orchestrator.md` |

## Quality Gate (Phase 7) — transcription

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| G1.q | verdict → `SPRINT_LOG.md` | emit | sequential | `qa_agent` | `agents/qa_agent.md` |
| G1.q | verdict → `SPRINT_LOG.md` | transcribe | sequential | `orchestrator` | `agents/orchestrator.md` |
| G1.t | verdict → `SPRINT_LOG.md` | emit | sequential | `tester_agent` | `agents/tester_agent.md` |
| G1.t | verdict → `SPRINT_LOG.md` | transcribe | sequential | `orchestrator` | `agents/orchestrator.md` |
