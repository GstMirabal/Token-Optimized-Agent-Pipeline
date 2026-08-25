# Agent Assignment — Sprint 029 (`documentation-truth`)

Source: `docs/sprints/029-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`).
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

## Ola 0 — Intake

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| R0 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify | sequential / ruleset | `governance_learner` | `agents/governance_learner.md` |
| R1 | `CHANGELOG.md` | modify | sequential / ruleset | `principal_agent` | `agents/principal_agent.md` |
| R2 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | sequential / ruleset | `orchestrator` | `agents/orchestrator.md` |

## Ola 1 — T1 counted set

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T1.0 | `tests/test_check_readme_counts.py` | create | sequential / ruleset | `devops_agent` — deviation (tests/) | `agents/devops_agent.md` |
| T1.1 | `scripts/check_readme_counts.py` | modify | sequential / ruleset | `devops_agent` | `agents/devops_agent.md` |
| T1.2 | `README.md` | modify | sequential / ruleset | `doc_orchestrator` | `agents/doc_orchestrator.md` |
| T1.3 | `workflows/close_workflow.md` | modify | sequential / ruleset | `governance_learner` | `agents/governance_learner.md` |

## Ola 2 — T3 guide + registry

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| G1 | `config/artifact_registry.json` | modify | sequential / ruleset | `devops_agent` | `agents/devops_agent.md` |
| G2 | `docs/guides/AGENTS_SLASH_COMMANDS_GUIDE.md` | modify | sequential / ruleset | `doc_orchestrator` | `agents/doc_orchestrator.md` |
| G3 | `skills/slash-commander/scripts/verify_commands.py` | modify | sequential / ruleset | `devops_agent` | `agents/devops_agent.md` |

## Ola 3 — T4 ADRs

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| A3 | `docs/decisions/ADR-0003-gates-never-drop-tier.md` | create | sequential / ruleset | `doc_orchestrator` | `agents/doc_orchestrator.md` |
| A4 | `docs/decisions/ADR-0004-no-model-selector-agent.md` | create | sequential / ruleset | `doc_orchestrator` | `agents/doc_orchestrator.md` |
| A5 | `docs/decisions/ADR-0005-prices-stay-out-of-config.md` | create | sequential / ruleset | `doc_orchestrator` | `agents/doc_orchestrator.md` |
| A6 | `docs/decisions/ADR-0006-session-bound-before-tiering.md` | create | sequential / ruleset | `doc_orchestrator` | `agents/doc_orchestrator.md` |
| A7 | `docs/decisions/ADR-0007-cursor-without-api-delegation.md` | create | sequential / ruleset | `doc_orchestrator` | `agents/doc_orchestrator.md` |

## Ola 4 — T5, J1, J6

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| P1 | `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md` | modify | sequential / ruleset | `governance_learner` | `agents/governance_learner.md` |
| P2 | `rules/documentation_standard.md` | modify | sequential / ruleset | `governance_learner` | `agents/governance_learner.md` |
| J6.0 | `tests/test_verify_references.py` | modify/create | sequential / ruleset | `devops_agent` — deviation (tests/) | `agents/devops_agent.md` |
| J6.1 | `scripts/verify_references.py` | modify | sequential / ruleset | `devops_agent` | `agents/devops_agent.md` |

## Ola 5 — Close ledger

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| C1 | `CHANGELOG.md` | modify | sequential / ruleset | `principal_agent` | `agents/principal_agent.md` |

## Quality Gate (Phase 7) — transcription

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| G1.q | verdict → `SPRINT_LOG.md` | emit | sequential | `qa_agent` | `agents/qa_agent.md` |
| G1.q | verdict → `SPRINT_LOG.md` | transcribe | sequential | `orchestrator` | `agents/orchestrator.md` |
| G1.t | verdict → `SPRINT_LOG.md` | emit | sequential | `tester_agent` | `agents/tester_agent.md` |
| G1.t | verdict → `SPRINT_LOG.md` | transcribe | sequential | `orchestrator` | `agents/orchestrator.md` |

## Disagreements found

1. **T1.0 / J6.0** — plan first assigned `tester_agent`. Corrected to `devops_agent` (tests/ deviation) because `F-026-A1` keeps gate profiles read-only.
2. **None else.** Script writes map to `devops_agent`; docs/ADRs to `doc_orchestrator`; rules/template/findings to `governance_learner`.
