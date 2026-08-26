# Agent Assignment — Sprint 038 (`core-pipeline` / family-trial)

Source: `docs/sprints/038-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`).
Phase 4.1 of `workflows/pipeline_workflow.md`. Drafted from
`docs/standards/templates/AGENT_ASSIGNMENT_TEMPLATE.md`.
Mode: **Cursor**, `delegation_mode: sequential` — the `Assignee` column names
which profile's ruleset the single session adopts for that write.

This file is the staffing authority. It may overwrite the plan's
`Assignee (proposed)` column. A Work row is not closed until it appears here.

## Scope of this artifact (Phase 4.1 only)

| Owns | Does **not** own |
| :--- | :--- |
| Which ruleset governs each unit | Cursor model / effort (`task_scope.md`) |
| Agent-forge destination on units that create agents | `tier_escalation` proposals |

No unit in 038 **creates** an agent profile. `Destination` is `N/A` on every row.

---

## Track T — family trial (`cursor.author`)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| C1 | `config/model_tiers.json` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| T1 | `tests/test_session_start.py` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| M1 | `scripts/session_start.py` | modify | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| D1 | `docs/guides/MODEL_TIER_TRIAL_GUIDE.md` | modify | sequential / ruleset | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| D2 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | sequential / ruleset | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |

## Track R — gate-replay (D16)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| R1 | `docs/sprints/038-core-pipeline/GATE_REPLAY.md` | create | sequential / ruleset | `orchestrator` | N/A | `agents/orchestrator.md` |

R1: `qa_agent` emits findings via fresh-context `Task` + `--resolve gate`
(`ADR-0010`); `orchestrator` transcribes into `GATE_REPLAY.md` (`F-026-A1`).

## Disagreements with the plan

| Unit | Plan proposed | Assigned | Reason |
| :--- | :--- | :--- | :--- |
| C1 | `token_economy_agent` | `implementer_agent` | `token_economy_agent` has no `Write`/`Edit`; `check_task_scope.py` rejects modify without those tools. Map ownership stays with `token_economy_agent` (`tier_ownership`); implementer applies the cell |
| R1 | `qa_agent` | `orchestrator` | Gate profiles are read-only (`F-026-A1`); Orchestrator owns sprint-record transcription |
