# Task Scope — Sprint 027 (`autonomy-posture`)

**Branch**: `ai-sprint/027` · **Base**: `main` at `980f149`
**Plan**: `docs/sprints/027-core-pipeline/IMPLEMENTATION_PLAN.md`, committed `d874d7a`
**Phase**: 4.3 (Rule Audit) — after `agent_assignment.md` (4.1) and
`skill_assignment.md` (4.2).

**Agent assignment (Phase 4.1) lives in**
[`agent_assignment.md`](./agent_assignment.md). This file **repeats the assignee
per unit** in the `Assignee` column (required shape below) and keeps a full
index in § Agent assignment map so ruleset, **model**, and **effort** are visible
without leaving the scope artifact.

**Table shape (Work units).** `# | File | Operation | Risk | Assignee | Status`

**Status legend.** `⏳` pending Phase 5; `✅ <sha>` after execution.

**Mode (all units).** Cursor `delegation_mode: sequential` — assignee = ruleset
the single session adopts for that write; no subagent dispatch. **Select the
declared Model/Effort in the Cursor UI before starting each unit** (`config/model_tiers.json`
`cursor` column is still `null`).

---

## Agent assignment map

Canonical copy of Phase 4.1 + tier defaults from `config/model_tiers.json`
(`claude_code`). If this table and `agent_assignment.md` disagree,
**`agent_assignment.md` wins** and this file must be patched in the same commit.

| # | File | Assignee | Ruleset file | Model | Effort | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| A1 | `agents/tester_agent.md` | `agent_orchestrator` | `agents/agent_orchestrator.md` | `sonnet` | `medium` | tier `author` default |
| A1.1 | `agents/qa_agent.md` | `agent_orchestrator` | `agents/agent_orchestrator.md` | `sonnet` | `medium` | tier `author` default |
| A1.2 | `agents/orchestrator.md` | `agent_orchestrator` | `agents/agent_orchestrator.md` | `sonnet` | `medium` | tier `author` default |
| A3 | `hooks/on_init.py` | `devops_agent` | `agents/devops_agent.md` | `sonnet` | `medium` | **Escalated** mechanical→author |
| A3.1 | `tests/test_on_init.py` | `devops_agent` | `agents/devops_agent.md` | `haiku` | `low` | Deviation tests/; default mechanical |
| P1 | `scripts/persist_session_context.py` | `devops_agent` | `agents/devops_agent.md` | `sonnet` | `medium` | **Escalated** mechanical→author |
| P1.1 | `tests/test_persist_session_context.py` | `devops_agent` | `agents/devops_agent.md` | `haiku` | `low` | Deviation tests/ |
| P2 | `scripts/check_role_artifact.py` | `devops_agent` | `agents/devops_agent.md` | `sonnet` | `medium` | **Escalated** mechanical→author |
| P2.1 | `tests/test_check_role_artifact.py` | `devops_agent` | `agents/devops_agent.md` | `haiku` | `low` | Deviation tests/ |
| P2.2 | `Makefile` | `devops_agent` | `agents/devops_agent.md` | `haiku` | `low` | Wiring only |
| P3 | `scripts/session_end_hook.py` | `devops_agent` | `agents/devops_agent.md` | `sonnet` | `medium` | **Escalated** mechanical→author |
| P3.1 | `tests/test_session_end_hook.py` | `devops_agent` | `agents/devops_agent.md` | `haiku` | `low` | Deviation tests/ |
| C1 | `claude/settings.hooks.json` | `devops_agent` | `agents/devops_agent.md` | `sonnet` | `medium` | **Escalated** mechanical→author |
| C2 | `docs/guides/AUTONOMY_POSTURE_GUIDE.md` | `doc_orchestrator` | `agents/doc_orchestrator.md` | `sonnet` | `medium` | tier `author` default |
| C3 | `workflows/start_workflow.md` | `doc_orchestrator` | `agents/doc_orchestrator.md` | `sonnet` | `medium` | tier `author` default |
| D1 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | `governance_learner` | `agents/governance_learner.md` | `sonnet` | `medium` | tier `author` default |
| D2 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | `orchestrator` | `agents/orchestrator.md` | `sonnet` | `medium` | tier `author` default |
| D3 | `CHANGELOG.md` | `principal_agent` | `agents/principal_agent.md` | `opus` | `high` | tier `gate` default |
| G1.q | `SPRINT_LOG.md` (emit) | `qa_agent` | `agents/qa_agent.md` | `opus` | `high` | tier `gate` |
| G1.q | `SPRINT_LOG.md` (write) | `orchestrator` | `agents/orchestrator.md` | `sonnet` | `medium` | transcription |
| G1.t | `SPRINT_LOG.md` (emit) | `tester_agent` | `agents/tester_agent.md` | `opus` | `high` | tier `gate` |
| G1.t | `SPRINT_LOG.md` (write) | `orchestrator` | `agents/orchestrator.md` | `sonnet` | `medium` | transcription |

---

## Declared deviations

**1. `tests/` writes → `devops_agent`.** Same as Sprint 026: `tester_agent` has no
`Write`/`Edit`. Ola 0 aligns tester prose (`A1`) but will **not** grant Write.
Affected: `A3.1`, `P1.1`, `P2.1`, `P3.1`. Model/effort stay mechanical (`haiku`/`low`).

**2. Gate verdicts → Orchestrator transcription.** Confirmed by
`config/artifact_registry.json` (`SPRINT_LOG.md` role) and plan Design §D2.
Affected at Phase 7: `G1.q`, `G1.t` (two model rows each: emit vs write).

**3. `F-021-A2` unresolved.** `scripts/`/`hooks/` authoring stays on `devops_agent`.

---

## Declared escalations — `token_economy_agent` `tier_escalation`

**Assignee and jurisdiction are unchanged.** Each row is a **model escalation for
one task**, not a reassignment. Profile default for `devops_agent` is
`mechanical` / `haiku` / `effort: low` (`config/model_tiers.json`).

| # | File | Default | Escalated to | Why |
| :--- | :--- | :--- | :--- | :--- |
| A3 | `hooks/on_init.py` | mechanical/haiku/low | **author/sonnet/medium** | Host-vs-nucleus path resolution; false-green class defect (`F-026-A3`) |
| P1 | `scripts/persist_session_context.py` | mechanical/haiku/low | **author/sonnet/medium** | New session-memory protocol; wrong persist blinds resume |
| P2 | `scripts/check_role_artifact.py` | mechanical/haiku/low | **author/sonnet/medium** | Drift gate against `artifact_registry`; false negative skips Phase 2.6 intent |
| P3 | `scripts/session_end_hook.py` | mechanical/haiku/low | **author/sonnet/medium** | Must call `suspend` never `release`; wrong choice blinds `detect_drift` |
| C1 | `claude/settings.hooks.json` | mechanical/haiku/low | **author/sonnet/medium** | `hard_deny` / sandbox / bypass close; Abort criterion on merge loss of deny |

**Not escalated:** prose units on `author`/`gate` defaults; `P2.2` Makefile wiring;
all `tests/` deviation rows (deterministic assertions once the parent script exists).

Affected Work rows' `Assignee` cells read
`devops_agent — escalated (mechanical/haiku → author/sonnet, effort medium; see Declared escalations)`.

---

## Ola 0 — Contradicciones

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| A1 | `agents/tester_agent.md` | modify | medium | `agent_orchestrator` · `sonnet`/`medium` | ⏳ |
| A1.1 | `agents/qa_agent.md` | modify | low | `agent_orchestrator` · `sonnet`/`medium` | ⏳ |
| A1.2 | `agents/orchestrator.md` | modify | low | `agent_orchestrator` · `sonnet`/`medium` | ⏳ |
| A3 | `hooks/on_init.py` | modify | high | `devops_agent` — escalated (mechanical/haiku → author/sonnet, effort medium; see Declared escalations) | ⏳ |
| A3.1 | `tests/test_on_init.py` | create | medium | `devops_agent` — deviation (tests/) · `haiku`/`low` | ⏳ |

## Ola 1 — Portable

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| P1 | `scripts/persist_session_context.py` | create | medium | `devops_agent` — escalated (mechanical/haiku → author/sonnet, effort medium; see Declared escalations) | ⏳ |
| P1.1 | `tests/test_persist_session_context.py` | create | medium | `devops_agent` — deviation (tests/) · `haiku`/`low` | ⏳ |
| P2 | `scripts/check_role_artifact.py` | create | medium | `devops_agent` — escalated (mechanical/haiku → author/sonnet, effort medium; see Declared escalations) | ⏳ |
| P2.1 | `tests/test_check_role_artifact.py` | create | medium | `devops_agent` — deviation (tests/) · `haiku`/`low` | ⏳ |
| P2.2 | `Makefile` | modify | medium | `devops_agent` · `haiku`/`low` | ⏳ |
| P3 | `scripts/session_end_hook.py` | create | medium | `devops_agent` — escalated (mechanical/haiku → author/sonnet, effort medium; see Declared escalations) | ⏳ |
| P3.1 | `tests/test_session_end_hook.py` | create | low | `devops_agent` — deviation (tests/) · `haiku`/`low` | ⏳ |

## Ola 2 — Template Claude Code

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| C1 | `claude/settings.hooks.json` | modify | high | `devops_agent` — escalated (mechanical/haiku → author/sonnet, effort medium; see Declared escalations) | ⏳ |
| C2 | `docs/guides/AUTONOMY_POSTURE_GUIDE.md` | create | low | `doc_orchestrator` · `sonnet`/`medium` | ⏳ |
| C3 | `workflows/start_workflow.md` | modify | medium | `doc_orchestrator` · `sonnet`/`medium` | ⏳ |

## Ola 3 — Cierre

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| D1 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify | low | `governance_learner` · `sonnet`/`medium` | ⏳ |
| D2 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | low | `orchestrator` · `sonnet`/`medium` | ⏳ |
| D3 | `CHANGELOG.md` | modify | low | `principal_agent` · `opus`/`high` | ⏳ |

## Phase 7 — Quality Gate (transcription)

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| G1.q | `docs/sprints/027-core-pipeline/SPRINT_LOG.md` | emit verdict | medium | `qa_agent` · `opus`/`high` | ⏳ |
| G1.q | `docs/sprints/027-core-pipeline/SPRINT_LOG.md` | transcribe | medium | `orchestrator` · `sonnet`/`medium` | ⏳ |
| G1.t | `docs/sprints/027-core-pipeline/SPRINT_LOG.md` | emit verdict | medium | `tester_agent` · `opus`/`high` | ⏳ |
| G1.t | `docs/sprints/027-core-pipeline/SPRINT_LOG.md` | transcribe | medium | `orchestrator` · `sonnet`/`medium` | ⏳ |

---

## Isolation notes

- `A3` before `A3.1` (tests fail on current tree, then pass).
- Ola 1 scripts before their tests; `P2` before `P2.2` (invoker needs the script).
- Ola 2 `C1` after Ola 1 (hooks must point at existing scripts) — Abort criterion on merge loss of deny rules.
- Ola 3 only after `make verify` green.

## RA-16

New scripts `P1`/`P2`/`P3` must declare `invoked_by:` in the module docstring.
`C1` is the Claude-side invoker; `P2.2` / guide `C2` cover Cursor/portable invokers.
