# Task Scope — Sprint 027 (`autonomy-posture`)

**Branch**: `ai-sprint/027` · **Base**: `main` at `980f149`
**Plan**: `docs/sprints/027-core-pipeline/IMPLEMENTATION_PLAN.md`, committed `d874d7a`
**Phase**: 4.3 (Rule Audit) — after `agent_assignment.md` (4.1) and
`skill_assignment.md` (4.2).

**Agent assignment (Phase 4.1) lives in**
[`agent_assignment.md`](./agent_assignment.md). This file **repeats the assignee
per unit** in the `Assignee` column (required shape below) and keeps a full
index in § Agent assignment map so the ruleset is visible without leaving the
scope artifact.

**Table shape (Work units).** `# | File | Operation | Risk | Assignee | Status`

**Status legend.** `⏳` pending Phase 5; `✅ <sha>` after execution.

**Mode (all units).** Cursor `delegation_mode: sequential` — assignee = ruleset
the single session adopts for that write; no subagent dispatch.

---

## Agent assignment map

Canonical copy of Phase 4.1. If this table and `agent_assignment.md` disagree,
**`agent_assignment.md` wins** and this file must be patched in the same commit.

| # | File | Assignee | Ruleset file | Notes |
| :--- | :--- | :--- | :--- | :--- |
| A1 | `agents/tester_agent.md` | `agent_orchestrator` | `agents/agent_orchestrator.md` | Align prose to read-only grant (`F-026-A1`) |
| A1.1 | `agents/qa_agent.md` | `agent_orchestrator` | `agents/agent_orchestrator.md` | Verdict routing row |
| A1.2 | `agents/orchestrator.md` | `agent_orchestrator` | `agents/agent_orchestrator.md` | Phase 7 transcription ownership |
| A3 | `hooks/on_init.py` | `devops_agent` | `agents/devops_agent.md` | `F-086-A1` / hooks tree |
| A3.1 | `tests/test_on_init.py` | `devops_agent` | `agents/devops_agent.md` | **Deviation:** tests/; `tester_agent` has no Write/Edit |
| P1 | `scripts/persist_session_context.py` | `devops_agent` | `agents/devops_agent.md` | `F-086-A1` / scripts tree |
| P1.1 | `tests/test_persist_session_context.py` | `devops_agent` | `agents/devops_agent.md` | **Deviation:** tests/ |
| P2 | `scripts/check_role_artifact.py` | `devops_agent` | `agents/devops_agent.md` | |
| P2.1 | `tests/test_check_role_artifact.py` | `devops_agent` | `agents/devops_agent.md` | **Deviation:** tests/ |
| P2.2 | `Makefile` | `devops_agent` | `agents/devops_agent.md` | One physical file at commit time |
| P3 | `scripts/session_end_hook.py` | `devops_agent` | `agents/devops_agent.md` | |
| P3.1 | `tests/test_session_end_hook.py` | `devops_agent` | `agents/devops_agent.md` | **Deviation:** tests/ |
| C1 | `claude/settings.hooks.json` | `devops_agent` | `agents/devops_agent.md` | Template merge; Abort on deny loss |
| C2 | `docs/guides/AUTONOMY_POSTURE_GUIDE.md` | `doc_orchestrator` | `agents/doc_orchestrator.md` | |
| C3 | `workflows/start_workflow.md` | `doc_orchestrator` | `agents/doc_orchestrator.md` | Fixed to this path (not pipeline) |
| D1 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | `governance_learner` | `agents/governance_learner.md` | |
| D2 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | `orchestrator` | `agents/orchestrator.md` | |
| D3 | `CHANGELOG.md` | `principal_agent` | `agents/principal_agent.md` | |
| G1.q | `SPRINT_LOG.md` (verdict lines) | `qa_agent` → `orchestrator` | `agents/qa_agent.md` + `agents/orchestrator.md` | Gate emits; Orchestrator writes |
| G1.t | `SPRINT_LOG.md` (verdict lines) | `tester_agent` → `orchestrator` | `agents/tester_agent.md` + `agents/orchestrator.md` | Gate emits; Orchestrator writes |

---

## Declared deviations

**1. `tests/` writes → `devops_agent`.** Same as Sprint 026: `tester_agent` has no
`Write`/`Edit`. Ola 0 aligns tester prose (`A1`) but will **not** grant Write.
Affected: `A3.1`, `P1.1`, `P2.1`, `P3.1`.

**2. Gate verdicts → Orchestrator transcription.** Confirmed by
`config/artifact_registry.json` (`SPRINT_LOG.md` role) and plan Design §D2.
Affected at Phase 7: `G1.q`, `G1.t`.

**3. `F-021-A2` unresolved.** `scripts/`/`hooks/` authoring stays on `devops_agent`.

---

## Ola 0 — Contradicciones

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| A1 | `agents/tester_agent.md` | modify | medium | `agent_orchestrator` (`agents/agent_orchestrator.md`) | ⏳ |
| A1.1 | `agents/qa_agent.md` | modify | low | `agent_orchestrator` (`agents/agent_orchestrator.md`) | ⏳ |
| A1.2 | `agents/orchestrator.md` | modify | low | `agent_orchestrator` (`agents/agent_orchestrator.md`) | ⏳ |
| A3 | `hooks/on_init.py` | modify | high | `devops_agent` (`agents/devops_agent.md`) | ⏳ |
| A3.1 | `tests/test_on_init.py` | create | medium | `devops_agent` — deviation (tests/, `tester_agent` has no Write/Edit) | ⏳ |

## Ola 1 — Portable

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| P1 | `scripts/persist_session_context.py` | create | medium | `devops_agent` (`agents/devops_agent.md`) | ⏳ |
| P1.1 | `tests/test_persist_session_context.py` | create | medium | `devops_agent` — deviation (tests/) | ⏳ |
| P2 | `scripts/check_role_artifact.py` | create | medium | `devops_agent` (`agents/devops_agent.md`) | ⏳ |
| P2.1 | `tests/test_check_role_artifact.py` | create | medium | `devops_agent` — deviation (tests/) | ⏳ |
| P2.2 | `Makefile` | modify | medium | `devops_agent` (`agents/devops_agent.md`) | ⏳ |
| P3 | `scripts/session_end_hook.py` | create | medium | `devops_agent` (`agents/devops_agent.md`) | ⏳ |
| P3.1 | `tests/test_session_end_hook.py` | create | low | `devops_agent` — deviation (tests/) | ⏳ |

## Ola 2 — Template Claude Code

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| C1 | `claude/settings.hooks.json` | modify | high | `devops_agent` (`agents/devops_agent.md`) | ⏳ |
| C2 | `docs/guides/AUTONOMY_POSTURE_GUIDE.md` | create | low | `doc_orchestrator` (`agents/doc_orchestrator.md`) | ⏳ |
| C3 | `workflows/start_workflow.md` | modify | medium | `doc_orchestrator` (`agents/doc_orchestrator.md`) | ⏳ |

## Ola 3 — Cierre

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| D1 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify | low | `governance_learner` (`agents/governance_learner.md`) | ⏳ |
| D2 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | low | `orchestrator` (`agents/orchestrator.md`) | ⏳ |
| D3 | `CHANGELOG.md` | modify | low | `principal_agent` (`agents/principal_agent.md`) | ⏳ |

## Phase 7 — Quality Gate (transcription)

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| G1.q | `docs/sprints/027-core-pipeline/SPRINT_LOG.md` | modify (verdict lines) | medium | `qa_agent` (verdict) → `orchestrator` (write) | ⏳ |
| G1.t | `docs/sprints/027-core-pipeline/SPRINT_LOG.md` | modify (verdict lines) | medium | `tester_agent` (verdict) → `orchestrator` (write) | ⏳ |

---

## Isolation notes

- `A3` before `A3.1` (tests fail on current tree, then pass).
- Ola 1 scripts before their tests; `P2` before `P2.2` (invoker needs the script).
- Ola 2 `C1` after Ola 1 (hooks must point at existing scripts) — Abort criterion on merge loss of deny rules.
- Ola 3 only after `make verify` green.

## RA-16

New scripts `P1`/`P2`/`P3` must declare `invoked_by:` in the module docstring.
`C1` is the Claude-side invoker; `P2.2` / guide `C2` cover Cursor/portable invokers.
