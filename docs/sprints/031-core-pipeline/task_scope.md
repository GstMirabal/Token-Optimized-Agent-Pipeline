# Task Scope — Sprint 031 (`gate-verdict-classes`)

**Branch**: `ai-sprint/031` · **Base**: `main` at `85f338e` (`v4.13.1`)
**Plan**: `docs/sprints/031-core-pipeline/IMPLEMENTATION_PLAN.md` (committed `61581b6`)
**Phase**: 4.3 (Rule Audit) — after `agent_assignment.md` (4.1) and
`skill_assignment.md` (4.2).

**Table shape (Work units).** `# | File | Operation | Risk | Assignee | Model | Effort | Status`

**Status legend.** `⏳` pending Phase 6; `✅ <sha>` after execution.

**Mode.** Cursor `delegation_mode: sequential`.

---

## Ownership map (who does what)

| Concern | Decides | Writes the artifact | Source of truth |
| :--- | :--- | :--- | :--- |
| Profile per unit | `agent_orchestrator` | `agent_assignment.md` | Phase 4.1 |
| File lock / risk / status | `rule_validator` | this file (Work tables) | Phase 4.3 |
| Tier escalation + Cursor model/effort | `token_economy_agent` | transcribed here by `rule_validator` | `tier_escalation` + **`make cursor-tiers` run this session** |
| Accept Cursor model into `config/model_tiers.json` | **Human** | `config/model_tiers.json` (separate unit if approved) | Sprint 027 Design §D7 — script proposes only |

---

## Measured Cursor state (this session, 2026-08-25)

```text
make cursor-tiers   # → python3 scripts/audit_cursor_models.py ; echo exit=$?
exit=0
Proposed author (≤1, cold start): grok-4.6 (depth_lever yes)
Proposed mechanical (no depth lever): composer-2.5, gemini-3.1-pro, gemini-3-flash,
  gemini-3.5-flash, gpt-5-mini
Proposed gate: (none) — Design §D7, not proven history
Proposals only — config/model_tiers.json was not modified
```

Config human-accepted Sprint 027 (unchanged by this run): `cursor.mechanical=composer-2.5`,
`cursor.author=grok-4.6` (effort `high`). `cursor.gate.model` stays **`null`**.

## Cursor tier map — **ACCEPTED** (Sprint 027, confirmed by catalogue above)

| Intent (phase) | Claude Code (reference only) | Cursor (accepted) | Effort / depth |
| :--- | :--- | :--- | :--- |
| `mechanical` | `haiku` / `low` | **`composer-2.5`** | **N/A** |
| `author` | `sonnet` / `medium` | **`grok-4.6`** | **`high`** |
| `gate` | `opus` / `high` | **`null` in config** | Operational: log applied model from disk at gate time |

---

## Declared escalations — `token_economy_agent` audit, transcribed per `tier_escalation`

Assignee and jurisdiction unchanged. Each entry is a **model** escalation for one
task (`F-026-A2` / Sprint 026 pattern).

| Unit | Default | Escalation | Justification |
| :--- | :--- | :--- | :--- |
| M1 | mechanical / `composer-2.5` | author / `grok-4.6` / `high` | New governance gate script (`check_gate_log.py`); high blast radius on every Phase 7 / close |

All other mechanical rows stay at `composer-2.5` (medium/low risk). Author-tier
profiles use `grok-4.6` / `high`. Gate-tier rows use log-from-disk / N/A.

---

## Ola 0 — Tests

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T1 | `tests/test_check_gate_log.py` | create | medium | `devops_agent` — deviation (tests/) | `composer-2.5` | N/A | ✅ `ebd3050` |

## Ola 1 — Documents that instruct

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| R1 | `rules/qa_and_testing.md` | modify | high | `governance_learner` | `grok-4.6` | `high` | ✅ `f62d193` |
| R2 | `agents/qa_agent.md` | modify | high | `qa_agent` | `grok-4.6` | `high` | ✅ `4b3b030` |
| R3 | `agents/tester_agent.md` | modify | high | `tester_agent` | `grok-4.6` | `high` | ✅ `5cd7cc2` |
| R4 | `workflows/pipeline_workflow.md` | modify | high | `governance_learner` | `grok-4.6` | `high` | ✅ `19a6d80` |
| R5 | `workflows/remediation_workflow.md` | modify | high | `governance_learner` | `grok-4.6` | `high` | ✅ `260b852` |
| R6 | `agents/orchestrator.md` | modify | medium | `orchestrator` | `grok-4.6` | `high` | ✅ `5e1fea3` |
| R7 | `agents.md` | modify | high | `governance_learner` | `grok-4.6` | `high` | ✅ `3dd3114` |

## Ola 2 — Mechanism

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| M1 | `scripts/check_gate_log.py` | create | high | `devops_agent` — escalated (mechanical → author; see Declared escalations) | `grok-4.6` | `high` | ✅ `91d1d90` |
| M2 | `Makefile` | modify | medium | `devops_agent` | `composer-2.5` | N/A | ✅ `2293287` |
| M3 | `workflows/close_workflow.md` | modify | high | `governance_learner` | `grok-4.6` | `high` | ✅ `3f3481e` |

## Ola 3 — Documentary (not closeout ledger)

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| D1 | `docs/decisions/ADR-0008-gate-verdict-classes.md` | create | medium | `doc_orchestrator` | `grok-4.6` | `high` | ✅ `e1cae67` |
| D2 | `docs/guides/MODEL_TIER_TRIAL_GUIDE.md` | modify | medium | `doc_orchestrator` | `grok-4.6` | `high` | ✅ `a169b20` |
| D3 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | low | `doc_orchestrator` | `grok-4.6` | `high` | ✅ `cbcea1e` |
