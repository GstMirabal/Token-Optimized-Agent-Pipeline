# Agent Assignment — Sprint 028 (`self-improvement-unblock`)

Source: `docs/sprints/028-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`).
Mode: **Cursor**, `delegation_mode: sequential` — the `Assignee` column names
which profile's ruleset the single session adopts for that write
(`workflows/pipeline_workflow.md` Phase 4.1).

## Scope of this artifact (Phase 4.1 only)

| Owns | Does **not** own |
| :--- | :--- |
| Which ruleset governs each unit | Cursor model / effort (`task_scope.md`) |
| Agent-forge destination field on units that create agents | `tier_escalation` proposals |

**New this sprint:** units **A1** and **A2** introduce `agent_forge_destination`
doctrine; Phase 4.1 records profile assignees only. Destination choice is
documented in the plan (Design §D2) and will appear in `task_scope.md` notes
where an agent profile is created (none in this sprint's Work table — all units
modify existing framework files).

## Declared condition — `F-021-A2` (open, out of scope)

`devops_agent` remains sole `Write`/`Edit` holder for framework-root `scripts/`
and `hooks/` (`agents.md §6`). Ola 1 installer work stays on `devops_agent`.

---

## Ola 0 — Doctrina agente

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| A1 | `agents/agent_orchestrator.md` | modify | sequential / ruleset | `agent_orchestrator` | `agents/agent_orchestrator.md` |
| A2 | `workflows/pipeline_workflow.md` | modify | sequential / ruleset | `doc_orchestrator` | `agents/doc_orchestrator.md` |

## Ola 1 — Perfil instalable

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| P1 | `scripts/install.py` | modify | sequential / ruleset | `devops_agent` | `agents/devops_agent.md` |
| P1.1 | `tests/test_installer.sh` or `tests/test_install_profile_path.py` | modify/create | sequential / ruleset | `devops_agent` — deviation (tests/) | `agents/devops_agent.md` |
| P2 | `agents.md` | modify | sequential / ruleset | `governance_learner` | `agents/governance_learner.md` |
| P2.1 | `profiles/example-project/README.md` | modify | sequential / ruleset | `doc_orchestrator` | `agents/doc_orchestrator.md` |

## Ola 2 — Memoria

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| M1 | `workflows/extract_workflow.md` | modify | sequential / ruleset | `governance_learner` | `agents/governance_learner.md` |
| M2 | `workflows/close_workflow.md` | modify | sequential / ruleset | `governance_learner` | `agents/governance_learner.md` |

## Ola 3 — Promoción y cierre

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| D1 | `docs/guides/SELF_IMPROVEMENT_GUIDE.md` | create | sequential / ruleset | `doc_orchestrator` | `agents/doc_orchestrator.md` |
| D2 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | sequential / ruleset | `orchestrator` | `agents/orchestrator.md` |
| D3 | `CHANGELOG.md` | modify | sequential / ruleset | `principal_agent` | `agents/principal_agent.md` |

## Quality Gate (Phase 7) — transcription

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| G1.q | verdict → `SPRINT_LOG.md` | emit | sequential | `qa_agent` | `agents/qa_agent.md` |
| G1.q | verdict → `SPRINT_LOG.md` | transcribe | sequential | `orchestrator` | `agents/orchestrator.md` |
| G1.t | verdict → `SPRINT_LOG.md` | emit | sequential | `tester_agent` | `agents/tester_agent.md` |
| G1.t | verdict → `SPRINT_LOG.md` | transcribe | sequential | `orchestrator` | `agents/orchestrator.md` |

## Disagreements found

1. **None.** All units map to profiles with sufficient `Write`/`Edit` for their
   targets, except tests/ deviation to `devops_agent` (Sprint 026–027 precedent).
2. **P1.1 target file** left to implementer: extend `tests/test_installer.sh` if
   sufficient, else create `tests/test_install_profile_path.py` — one physical
   file per commit.
3. **Correction 2026-08-25.** First `task_scope.md` omitted explicit `Model`/`Effort`
   columns and a full `token_economy_agent` audit — corrected in a follow-up commit
   by `rule_validator` transcription (see `task_scope.md` § Failure analysis).
