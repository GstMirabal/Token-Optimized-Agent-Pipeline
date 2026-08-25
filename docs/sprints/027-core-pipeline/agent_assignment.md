# Agent Assignment — Sprint 027 (`autonomy-posture`)

Source: `docs/sprints/027-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`).
Plan committed: `d874d7a`.
Mode: **Cursor**, `delegation_mode: sequential` — no subagent dispatch. The
`Assignee` column names which profile's ruleset the single session adopts for
that write (`workflows/pipeline_workflow.md` Phase 4.1).

## Declared condition — `F-021-A2` (open, not resolved here)

`devops_agent` remains the only profile with `Write`/`Edit` over framework-root
`scripts/` and `hooks/` (`F-086-A1`, `agents.md §6`). Every Ola 1/2 code unit
below assigned to `devops_agent` is that consequence. `F-021-A2` stays out of
scope per the plan.

## Declared condition — `F-026-A1` (this sprint closes it)

Gate profiles keep read-only `tools:`. Test-file writes use
`devops_agent — deviation (tests/)`. Verdict transcription stays with
`orchestrator`. Ola 0 units `A1`/`A1.1`/`A1.2` align prose to that grant.

---

## Ola 0 — Contradicciones

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| A1 | `agents/tester_agent.md` | modify | sequential / ruleset | `agent_orchestrator` | `agents/agent_orchestrator.md` |
| A1.1 | `agents/qa_agent.md` | modify | sequential / ruleset | `agent_orchestrator` | `agents/agent_orchestrator.md` |
| A1.2 | `agents/orchestrator.md` | modify | sequential / ruleset | `agent_orchestrator` | `agents/agent_orchestrator.md` |
| A3 | `hooks/on_init.py` | modify | sequential / ruleset | `devops_agent` | `agents/devops_agent.md` |
| A3.1 | `tests/test_on_init.py` | create | sequential / ruleset | `devops_agent` — deviation (tests/, tester_agent has no Write/Edit) | `agents/devops_agent.md` |

## Ola 1 — Portable

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| P1 | `scripts/persist_session_context.py` | create | sequential / ruleset | `devops_agent` | `agents/devops_agent.md` |
| P1.1 | `tests/test_persist_session_context.py` | create | sequential / ruleset | `devops_agent` — deviation (tests/) | `agents/devops_agent.md` |
| P2 | `scripts/check_role_artifact.py` | create | sequential / ruleset | `devops_agent` | `agents/devops_agent.md` |
| P2.1 | `tests/test_check_role_artifact.py` | create | sequential / ruleset | `devops_agent` — deviation (tests/) | `agents/devops_agent.md` |
| P2.2 | `Makefile` (or verify wiring file named at execution) | modify | sequential / ruleset | `devops_agent` | `agents/devops_agent.md` |
| P3 | `scripts/session_end_hook.py` | create | sequential / ruleset | `devops_agent` | `agents/devops_agent.md` |
| P3.1 | `tests/test_session_end_hook.py` | create | sequential / ruleset | `devops_agent` — deviation (tests/) | `agents/devops_agent.md` |

## Ola 2 — Template Claude Code

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| C1 | `claude/settings.hooks.json` | modify | sequential / ruleset | `devops_agent` | `agents/devops_agent.md` |
| C2 | `docs/guides/AUTONOMY_POSTURE_GUIDE.md` | create | sequential / ruleset | `doc_orchestrator` | `agents/doc_orchestrator.md` |
| C3 | `workflows/start_workflow.md` or `pipeline_workflow.md` | modify | sequential / ruleset | `doc_orchestrator` | `agents/doc_orchestrator.md` |

## Ola 3 — Cierre

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| D1 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify | sequential / ruleset | `governance_learner` | `agents/governance_learner.md` |
| D2 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | sequential / ruleset | `orchestrator` | `agents/orchestrator.md` |
| D3 | `CHANGELOG.md` | modify | sequential / ruleset | `principal_agent` | `agents/principal_agent.md` |

## Quality Gate (Phase 7) — transcription

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| G1.q | verdict → `SPRINT_LOG.md` | emit + transcribe | sequential | `qa_agent` emits; `orchestrator` writes | `agents/qa_agent.md` + `agents/orchestrator.md` |
| G1.t | verdict → `SPRINT_LOG.md` | emit + transcribe | sequential | `tester_agent` emits; `orchestrator` writes | `agents/tester_agent.md` + `agents/orchestrator.md` |

## Disagreements found

1. **None new beyond `F-026-A1`.** Plan Ola 0 already schedules the prose fix; assignment applies the same `tests/` deviation as Sprint 026 rather than granting gate Write.
2. **`P2.2` target file** may be `Makefile` or a workflow/verify script — fixed at execution to one physical file before the commit (`jurisdictional_lock`).
3. **`C3` target** is one of two workflows; execution picks exactly one path per the plan's "o".
