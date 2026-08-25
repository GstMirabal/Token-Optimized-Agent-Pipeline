# Task Scope — Sprint 032 (`author-tier-trial`)

**Branch**: `ai-sprint/032` · **Base**: `main` at `0429f03` (`v4.14.0`)
**Plan**: `docs/sprints/032-core-pipeline/IMPLEMENTATION_PLAN.md` (committed `35f2331`)
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
| Accept Cursor model into `config/model_tiers.json` | **Human** | `config/model_tiers.json` (unit C1 + Phase 8 promote/revert) | Sprint 027 Design §D7 — script proposes only |

---

## Measured Cursor state (this session, 2026-08-25)

```text
make cursor-tiers   # → python3 scripts/audit_cursor_models.py ; echo exit=$?
exit=0
Models after hard filters (excl. default): 35
Applied model (author cold-start candidate): grok-4.6
Proposed author (≤1, cold start): grok-4.6 (depth_lever yes)
Catalogue includes grok-4.5 (xai, depth_lever yes) — trial candidate
Proposed mechanical (no depth lever): composer-2.5, gemini-3.1-pro, gemini-3-flash,
  gemini-3.5-flash, gpt-5-mini
Proposed gate: (none) — Design §D7, not proven history
Proposals only — config/model_tiers.json was not modified
```

**Trial precondition (Design D2).** Before Phase 6, the human selects
`grok-4.5` in Cursor. Each authoring unit opens with
`python3 scripts/audit_cursor_models.py` and requires
`Applied model …: grok-4.5`. Current applied model is still `grok-4.6`
(measured above) — that is expected until the human switches.

Config before C1: `cursor.mechanical=composer-2.5`, `cursor.author=grok-4.6`
(effort `high`). `cursor.gate.model` stays **`null`**.

## Cursor tier map — **TRIAL** (Sprint 032; promote or revert at Phase 8)

| Intent (phase) | Claude Code (reference only) | Cursor (trial) | Effort / depth |
| :--- | :--- | :--- | :--- |
| `mechanical` | `haiku` / `low` | **`composer-2.5`** | **N/A** |
| `author` | `sonnet` / `medium` | **`grok-4.5`** (was `grok-4.6`) | **`high`** |
| `gate` | `opus` / `high` | **`null` in config** | Operational: log applied model from disk at gate time |

---

## Declared escalations — `token_economy_agent` audit, transcribed per `tier_escalation`

Assignee and jurisdiction unchanged. Each entry is a **model** escalation for one
task (`F-026-A2` / Sprint 026 pattern).

| Unit | Default | Escalation | Justification |
| :--- | :--- | :--- | :--- |
| M1 | mechanical / `composer-2.5` | author / `grok-4.5` / `high` | Session-start platform probe writer; high blast radius on every `/agents:start` |

All other mechanical rows stay at `composer-2.5`. Author-tier profiles use the
**trial** `grok-4.5` / `high`. Gate-tier rows use log-from-disk / N/A.

---

## Ola 0 — Map

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| C1 | `config/model_tiers.json` | modify | medium | `token_economy_agent` | `grok-4.5` | `high` | ⏳ |

## Ola 1 — Tests

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T1 | `tests/test_session_protocol.py` | modify | medium | `devops_agent` — deviation (tests/) | `composer-2.5` | N/A | ⏳ |

## Ola 2 — Mechanism

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| M1 | `scripts/session_probe.py` | modify | high | `devops_agent` — escalated (mechanical → author; see Declared escalations) | `grok-4.5` | `high` | ⏳ |

## Ola 3 — Documentary (not closeout ledger)

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| D1 | `docs/guides/MODEL_TIER_TRIAL_GUIDE.md` | modify | medium | `doc_orchestrator` | `grok-4.5` | `high` | ⏳ |
| D2 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | low | `doc_orchestrator` | `grok-4.5` | `high` | ⏳ |
