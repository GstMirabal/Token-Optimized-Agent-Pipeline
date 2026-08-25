# Agent Assignment — Sprint 033 (`implementer-role`)

Source: `docs/sprints/033-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`).
Mode: **Cursor**, `delegation_mode: sequential` — the `Assignee` column names
which profile's ruleset the single session adopts for that write
(`workflows/pipeline_workflow.md` Phase 4.1).

## Scope of this artifact (Phase 4.1 only)

| Owns | Does **not** own |
| :--- | :--- |
| Which ruleset governs each unit | Cursor model / effort (`task_scope.md`) |
| Agent-forge destination on units that create agents | `tier_escalation` proposals |

**One unit creates an agent profile** (A1). Destination: `nucleus:PR`
(nucleus session; framework-wide profile under `agents/`).

## Declared condition — `F-021-A2` (this sprint closes it)

Until A1–A2 land, `devops_agent` still holds `Write`/`Edit` on framework-root
`scripts/` and `hooks/`. After A1–A2, those trees (plus `tests/`) assign to
`implementer_agent`. T1 must not run before A1 exists on the branch.

---

## Ola 0 — Decision record

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| A0 | `docs/decisions/ADR-0009-implementer-role.md` | create | sequential / ruleset | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |

## Ola 1 — Role map (creates then rewires)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| A1 | `agents/implementer_agent.md` | create | sequential / ruleset | `agent_orchestrator` | `nucleus:PR` | `agents/agent_orchestrator.md` |
| A2 | `agents/devops_agent.md` | modify | sequential / ruleset | `agent_orchestrator` | N/A | `agents/agent_orchestrator.md` |
| A3 | `agents.md` | modify | sequential / ruleset | `agent_orchestrator` | N/A | `agents/agent_orchestrator.md` |
| A4 | `agents/agent_orchestrator.md` | modify | sequential / ruleset | `agent_orchestrator` | N/A | `agents/agent_orchestrator.md` |

## Ola 2 — Pin (requires A1 on branch)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T1 | `tests/test_implementer_role.py` | create | sequential / ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` (after A1) |

## Ola 3 — Documentary (not closeout ledger)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| R1 | `README.md` | modify | sequential / ruleset | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| F1 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify | sequential / ruleset | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| Q1 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | sequential / ruleset | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |

## Quality Gate (Phase 7) — transcription

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| G1.q | verdict → `SPRINT_LOG.md` | emit | sequential | `qa_agent` | `agents/qa_agent.md` |
| G1.q | verdict → `SPRINT_LOG.md` | transcribe | sequential | `orchestrator` | `agents/orchestrator.md` |
| G1.t | verdict → `SPRINT_LOG.md` | emit | sequential | `tester_agent` | `agents/tester_agent.md` |
| G1.t | verdict → `SPRINT_LOG.md` | transcribe | sequential | `orchestrator` | `agents/orchestrator.md` |

## Disagreements with the plan

None. Plan assignees match staffing above. Destination for A1 recorded as
`nucleus:PR` per `agent_forge_destination` (c) in a nucleus session.
