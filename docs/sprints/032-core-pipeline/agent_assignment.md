# Agent Assignment — Sprint 032 (`author-tier-trial`)

Source: `docs/sprints/032-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`).
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
`token_economy_agent` owns the trial map cell in `config/model_tiers.json`.

---

## Ola 0 — Map

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| C1 | `config/model_tiers.json` | modify | sequential / ruleset | `token_economy_agent` | `agents/token_economy_agent.md` |

## Ola 1 — Tests

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T1 | `tests/test_session_protocol.py` | modify | sequential / ruleset | `devops_agent` — deviation (tests/) | `agents/devops_agent.md` |

## Ola 2 — Mechanism

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| M1 | `scripts/session_probe.py` | modify | sequential / ruleset | `devops_agent` | `agents/devops_agent.md` |

## Ola 3 — Documentary (not closeout ledger)

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| D1 | `docs/guides/MODEL_TIER_TRIAL_GUIDE.md` | modify | sequential / ruleset | `doc_orchestrator` | `agents/doc_orchestrator.md` |
| D2 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | sequential / ruleset | `doc_orchestrator` | `agents/doc_orchestrator.md` |

## Quality Gate (Phase 7) — transcription

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| G1.q | verdict → `SPRINT_LOG.md` | emit | sequential | `qa_agent` | `agents/qa_agent.md` |
| G1.q | verdict → `SPRINT_LOG.md` | transcribe | sequential | `orchestrator` | `agents/orchestrator.md` |
| G1.t | verdict → `SPRINT_LOG.md` | emit | sequential | `tester_agent` | `agents/tester_agent.md` |
| G1.t | verdict → `SPRINT_LOG.md` | transcribe | sequential | `orchestrator` | `agents/orchestrator.md` |
