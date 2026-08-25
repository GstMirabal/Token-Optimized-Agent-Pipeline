# Task Scope — Sprint 027 (`autonomy-posture`)

**Branch**: `ai-sprint/027` · **Base**: `main` at `980f149`
**Plan**: `docs/sprints/027-core-pipeline/IMPLEMENTATION_PLAN.md`, committed `d874d7a`
**Phase**: 4.3 (Rule Audit) — after `agent_assignment.md` (4.1) and
`skill_assignment.md` (4.2).

**Table shape.** `# | File | Operation | Risk | Assignee | Status`

**Status legend.** `⏳` pending Phase 5; `✅ <sha>` after execution.

---

## Declared deviations

**1. `tests/` writes → `devops_agent`.** Same as Sprint 026: `tester_agent` has no
`Write`/`Edit`. Ola 0 will align tester prose (`A1`) but will **not** grant Write.
Affected: `A3.1`, `P1.1`, `P2.1`, `P3.1`.

**2. Gate verdicts → Orchestrator transcription.** Confirmed by
`config/artifact_registry.json` (`SPRINT_LOG.md` role) and plan Design §D2.
Affected at Phase 7: `G1.q`, `G1.t`.

**3. `F-021-A2` unresolved.** `scripts/`/`hooks/` authoring stays on `devops_agent`.

---

## Ola 0 — Contradicciones

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| A1 | `agents/tester_agent.md` | modify | medium | `agent_orchestrator` | ⏳ |
| A1.1 | `agents/qa_agent.md` | modify | low | `agent_orchestrator` | ⏳ |
| A1.2 | `agents/orchestrator.md` | modify | low | `agent_orchestrator` | ⏳ |
| A3 | `hooks/on_init.py` | modify | high | `devops_agent` | ⏳ |
| A3.1 | `tests/test_on_init.py` | create | medium | `devops_agent` — deviation (tests/) | ⏳ |

## Ola 1 — Portable

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| P1 | `scripts/persist_session_context.py` | create | medium | `devops_agent` | ⏳ |
| P1.1 | `tests/test_persist_session_context.py` | create | medium | `devops_agent` — deviation (tests/) | ⏳ |
| P2 | `scripts/check_role_artifact.py` | create | medium | `devops_agent` | ⏳ |
| P2.1 | `tests/test_check_role_artifact.py` | create | medium | `devops_agent` — deviation (tests/) | ⏳ |
| P2.2 | `Makefile` | modify | medium | `devops_agent` | ⏳ |
| P3 | `scripts/session_end_hook.py` | create | medium | `devops_agent` | ⏳ |
| P3.1 | `tests/test_session_end_hook.py` | create | low | `devops_agent` — deviation (tests/) | ⏳ |

## Ola 2 — Template Claude Code

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| C1 | `claude/settings.hooks.json` | modify | high | `devops_agent` | ⏳ |
| C2 | `docs/guides/AUTONOMY_POSTURE_GUIDE.md` | create | low | `doc_orchestrator` | ⏳ |
| C3 | `workflows/start_workflow.md` | modify | medium | `doc_orchestrator` | ⏳ |

## Ola 3 — Cierre

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| D1 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify | low | `governance_learner` | ⏳ |
| D2 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | low | `orchestrator` | ⏳ |
| D3 | `CHANGELOG.md` | modify | low | `principal_agent` | ⏳ |

## Isolation notes

- `A3` before `A3.1` (tests fail on current tree, then pass).
- Ola 1 scripts before their tests; `P2` before `P2.2` (invoker needs the script).
- Ola 2 `C1` after Ola 1 (hooks must point at existing scripts) — Abort criterion on merge loss of deny rules.
- Ola 3 only after `make verify` green.

## RA-16

New scripts `P1`/`P2`/`P3` must declare `invoked_by:` in the module docstring.
`C1` is the Claude-side invoker; `P2.2` / guide `C2` cover Cursor/portable invokers.
