# Agent Assignment — Sprint 027 (`autonomy-posture`)

Source: `docs/sprints/027-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`).
Plan committed: `d874d7a`.
Mode: **Cursor**, `delegation_mode: sequential` — no subagent dispatch. The
`Assignee` column names which profile's ruleset the single session adopts for
that write (`workflows/pipeline_workflow.md` Phase 4.1).

**Model / effort** come from `config/model_tiers.json` (`claude_code` column)
matched to the assignee's `tier:` in `agents/*.md`. Under Cursor the `cursor`
column is still `null` (not proven history, Sprint 026 `P4.4`); the values
below are the **declared intent** the session must select manually before the
unit. Escalations are jurisdiction-preserving (`tier_escalation`): same
assignee, higher tier — see `task_scope.md` § Declared escalations.

| Tier | Default model | Default effort | Profiles used this sprint |
| :--- | :--- | :--- | :--- |
| `mechanical` | `haiku` | `low` | `devops_agent` |
| `author` | `sonnet` | `medium` | `agent_orchestrator`, `doc_orchestrator`, `orchestrator`, `governance_learner` |
| `gate` | `opus` | `high` | `qa_agent`, `tester_agent`, `principal_agent` |

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

| # | Target | Operation | Mode | Assignee | Ruleset file | Model | Effort |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| A1 | `agents/tester_agent.md` | modify | sequential / ruleset | `agent_orchestrator` | `agents/agent_orchestrator.md` | `sonnet` | `medium` |
| A1.1 | `agents/qa_agent.md` | modify | sequential / ruleset | `agent_orchestrator` | `agents/agent_orchestrator.md` | `sonnet` | `medium` |
| A1.2 | `agents/orchestrator.md` | modify | sequential / ruleset | `agent_orchestrator` | `agents/agent_orchestrator.md` | `sonnet` | `medium` |
| A3 | `hooks/on_init.py` | modify | sequential / ruleset | `devops_agent` | `agents/devops_agent.md` | `sonnet` ↑ | `medium` ↑ |
| A3.1 | `tests/test_on_init.py` | create | sequential / ruleset | `devops_agent` — deviation (tests/) | `agents/devops_agent.md` | `haiku` | `low` |

↑ = escalated from profile default `haiku`/`low` — see `task_scope.md` § Declared escalations.

## Ola 1 — Portable

| # | Target | Operation | Mode | Assignee | Ruleset file | Model | Effort |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| P1 | `scripts/persist_session_context.py` | create | sequential / ruleset | `devops_agent` | `agents/devops_agent.md` | `sonnet` ↑ | `medium` ↑ |
| P1.1 | `tests/test_persist_session_context.py` | create | sequential / ruleset | `devops_agent` — deviation (tests/) | `agents/devops_agent.md` | `haiku` | `low` |
| P2 | `scripts/check_role_artifact.py` | create | sequential / ruleset | `devops_agent` | `agents/devops_agent.md` | `sonnet` ↑ | `medium` ↑ |
| P2.1 | `tests/test_check_role_artifact.py` | create | sequential / ruleset | `devops_agent` — deviation (tests/) | `agents/devops_agent.md` | `haiku` | `low` |
| P2.2 | `Makefile` | modify | sequential / ruleset | `devops_agent` | `agents/devops_agent.md` | `haiku` | `low` |
| P3 | `scripts/session_end_hook.py` | create | sequential / ruleset | `devops_agent` | `agents/devops_agent.md` | `sonnet` ↑ | `medium` ↑ |
| P3.1 | `tests/test_session_end_hook.py` | create | sequential / ruleset | `devops_agent` — deviation (tests/) | `agents/devops_agent.md` | `haiku` | `low` |

## Ola 2 — Template Claude Code

| # | Target | Operation | Mode | Assignee | Ruleset file | Model | Effort |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| C1 | `claude/settings.hooks.json` | modify | sequential / ruleset | `devops_agent` | `agents/devops_agent.md` | `sonnet` ↑ | `medium` ↑ |
| C2 | `docs/guides/AUTONOMY_POSTURE_GUIDE.md` | create | sequential / ruleset | `doc_orchestrator` | `agents/doc_orchestrator.md` | `sonnet` | `medium` |
| C3 | `workflows/start_workflow.md` | modify | sequential / ruleset | `doc_orchestrator` | `agents/doc_orchestrator.md` | `sonnet` | `medium` |

## Ola 3 — Cierre

| # | Target | Operation | Mode | Assignee | Ruleset file | Model | Effort |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| D1 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify | sequential / ruleset | `governance_learner` | `agents/governance_learner.md` | `sonnet` | `medium` |
| D2 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | sequential / ruleset | `orchestrator` | `agents/orchestrator.md` | `sonnet` | `medium` |
| D3 | `CHANGELOG.md` | modify | sequential / ruleset | `principal_agent` | `agents/principal_agent.md` | `opus` | `high` |

## Quality Gate (Phase 7) — transcription

| # | Target | Operation | Mode | Assignee | Ruleset file | Model | Effort |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| G1.q | verdict → `SPRINT_LOG.md` | emit | sequential | `qa_agent` | `agents/qa_agent.md` | `opus` | `high` |
| G1.q | verdict → `SPRINT_LOG.md` | transcribe | sequential | `orchestrator` | `agents/orchestrator.md` | `sonnet` | `medium` |
| G1.t | verdict → `SPRINT_LOG.md` | emit | sequential | `tester_agent` | `agents/tester_agent.md` | `opus` | `high` |
| G1.t | verdict → `SPRINT_LOG.md` | transcribe | sequential | `orchestrator` | `agents/orchestrator.md` | `sonnet` | `medium` |

## Disagreements found

1. **None new beyond `F-026-A1`.** Plan Ola 0 already schedules the prose fix; assignment applies the same `tests/` deviation as Sprint 026 rather than granting gate Write.
2. **`P2.2` target file** fixed to `Makefile` in `task_scope.md`.
3. **`C3` target** fixed to `workflows/start_workflow.md`.
4. **Cursor `model: null` in `model_tiers.json`.** Declared intent uses the `claude_code` tier defaults; the human selects the Cursor model before each unit. Closing that null is out of scope (`F-026-A2` / post-026 history).
