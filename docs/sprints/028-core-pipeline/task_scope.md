# Task Scope — Sprint 028 (`self-improvement-unblock`)

**Branch**: `ai-sprint/028` · **Base**: `main` at `0a175a2`
**Plan**: `docs/sprints/028-core-pipeline/IMPLEMENTATION_PLAN.md`
**Phase**: 4.3 (Rule Audit) — after `agent_assignment.md` (4.1) and
`skill_assignment.md` (4.2).

**Table shape (Work units).** `# | File | Operation | Risk | Assignee | Status`

**Status legend.** `⏳` pending Phase 6; `✅ <sha>` after execution.

**Mode.** Cursor `delegation_mode: sequential`.

---

## Cursor tier map — ACCEPTED (Sprint 027 precedent)

Bindings from `config/model_tiers.json` `cursor` column (human accepted
2026-08-25). Re-run `make cursor-tiers` 2026-08-25 this session: exit 0; 35
models; config not rewritten.

| Intent | Cursor model | Effort |
| :--- | :--- | :--- |
| `mechanical` | `composer-2.5` | N/A |
| `author` | `grok-4.6` | `high` |
| `gate` | `null` in config | log applied model at gate time |

---

## Declared escalations — `token_economy_agent` audit (Cursor)

Default for `devops_agent`: `mechanical` → `composer-2.5`.

| # | File | From | To | Cursor model | Effort | Why |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| P1 | `scripts/install.py` | mechanical | **author** | `grok-4.6` | `high` | External profile path + symlink semantics; high regression surface |

All other units stay at their profile's default intent tier.

---

## Declared deviations

**1. `tests/` writes → `devops_agent`.** `tester_agent` has no `Write`/`Edit`.
Affected: `P1.1`.

**2. Gate verdicts → Orchestrator transcription.** Registry precedent (027).

---

## Ola 0 — Doctrina agente

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| A1 | `agents/agent_orchestrator.md` | modify | medium | `agent_orchestrator`; Cursor `grok-4.6`, effort `high` | ⏳ |
| A2 | `workflows/pipeline_workflow.md` | modify | medium | `doc_orchestrator`; Cursor `grok-4.6`, effort `high` | ⏳ |

## Ola 1 — Perfil instalable

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| P1 | `scripts/install.py` | modify | high | `devops_agent` — escalated (mechanical → author; Cursor `grok-4.6`, effort `high`) | ⏳ |
| P1.1 | `tests/test_installer.sh` or `tests/test_install_profile_path.py` | modify/create | medium | `devops_agent` — deviation (tests/); Cursor `composer-2.5` | ⏳ |
| P2 | `agents.md` | modify | medium | `governance_learner`; Cursor `grok-4.6`, effort `high` | ⏳ |
| P2.1 | `profiles/example-project/README.md` | modify | low | `doc_orchestrator`; Cursor `grok-4.6`, effort `high` | ⏳ |

## Ola 2 — Memoria

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| M1 | `workflows/extract_workflow.md` | modify | medium | `governance_learner`; Cursor `grok-4.6`, effort `high` | ⏳ |
| M2 | `workflows/close_workflow.md` | modify | medium | `governance_learner`; Cursor `grok-4.6`, effort `high` | ⏳ |

## Ola 3 — Promoción y cierre

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| D1 | `docs/guides/SELF_IMPROVEMENT_GUIDE.md` | create | low | `doc_orchestrator`; Cursor `grok-4.6`, effort `high` | ⏳ |
| D2 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | low | `orchestrator`; Cursor `grok-4.6`, effort `high` | ⏳ |
| D3 | `CHANGELOG.md` | modify | low | `principal_agent`; Cursor gate config `null` | ⏳ |

## Phase 7 — Quality Gate (transcription)

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| G1.q | `docs/sprints/028-core-pipeline/SPRINT_LOG.md` | emit verdict | medium | `qa_agent`; Cursor gate config `null` | ⏳ |
| G1.q | `docs/sprints/028-core-pipeline/SPRINT_LOG.md` | transcribe | medium | `orchestrator`; Cursor `grok-4.6`, effort `high` | ⏳ |
| G1.t | `docs/sprints/028-core-pipeline/SPRINT_LOG.md` | emit verdict | medium | `tester_agent`; Cursor gate config `null` | ⏳ |
| G1.t | `docs/sprints/028-core-pipeline/SPRINT_LOG.md` | transcribe | medium | `orchestrator`; Cursor `grok-4.6`, effort `high` | ⏳ |

---

## Isolation notes

- Ola 0 before Ola 1 (doctrine before installer).
- `P1` before `P1.1`.
- Ola 2 after Ola 1; Ola 3 after `make verify` green.

## RA-16

`P1` retains/extends `invoked_by:` in module docstring. New guide `D1` names
invokers in prose only (knowledge artifact — no script).
