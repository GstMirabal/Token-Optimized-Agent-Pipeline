# Task Scope — Sprint 030 (`token-economy-enforcement`)

**Branch**: `ai-sprint/030` · **Base**: `main` at `65dbaaf`
**Plan**: `docs/sprints/030-core-pipeline/IMPLEMENTATION_PLAN.md` (committed `9d5ce94`)
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
| A2 | mechanical / `composer-2.5` | author / `grok-4.6` / `high` | New governance gate script (`audit_plan.py`); high blast radius on every Phase 5 |
| C1 | mechanical / `composer-2.5` | author / `grok-4.6` / `high` | Session-bound meter; wrong exclusion blinds `§3.1` |
| C2 | mechanical / `composer-2.5` | author / `grok-4.6` / `high` | Probe wires the meter; Cursor/Claude mismatch is the defect |
| F1 | mechanical / `composer-2.5` | author / `grok-4.6` / `high` | Closes `F-026-A2`; false positives block every Cursor close |

All other mechanical rows stay at `composer-2.5` (medium/low risk). Author-tier
profiles use `grok-4.6` / `high`. Gate-tier rows use log-from-disk / N/A.

---

## Ola 0 — Tests

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| A0 | `tests/test_token_saver_auditor.py` | create | medium | `devops_agent` — deviation (tests/) | `composer-2.5` | N/A | ✅ `f794b19` |
| T0 | `tests/test_check_task_scope.py` | create | medium | `devops_agent` — deviation (tests/) | `composer-2.5` | N/A | ✅ `f794b19` |
| C0 | `tests/test_session_protocol.py` | modify | medium | `devops_agent` — deviation (tests/) | `composer-2.5` | N/A | ✅ `f794b19` |

## Ola 1 — Auditor

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| A1 | `skills/token-saver-auditor/scripts/__init__.py` | create | low | `skill_architect` | `grok-4.6` | `high` | ✅ `f794b19` |
| A2 | `skills/token-saver-auditor/scripts/audit_plan.py` | create | high | `devops_agent` — escalated (mechanical → author; see Declared escalations) | `grok-4.6` | `high` | ✅ `f794b19` |
| A3 | `skills/token-saver-auditor/SKILL.md` | modify | medium | `token_economy_agent` | `grok-4.6` | `high` | ✅ `f794b19` |
| A4 | `skills/token-saver-auditor/README.md` | modify | low | `skill_architect` | `grok-4.6` | `high` | ✅ `f794b19` |

## Ola 2 — Consumo

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| C1 | `scripts/session_cost.py` | modify | high | `devops_agent` — escalated (mechanical → author; see Declared escalations) | `grok-4.6` | `high` | ✅ `f794b19` |
| C2 | `scripts/session_probe.py` | modify | high | `devops_agent` — escalated (mechanical → author; see Declared escalations) | `grok-4.6` | `high` | ✅ `f794b19` |
| C3 | `config/rule_triggers.json` | modify | medium | `devops_agent` | `composer-2.5` | N/A | ✅ `f794b19` |
| C4 | `rules/token_economy.md` | modify | medium | `token_economy_agent` | `grok-4.6` | `high` | ✅ `f794b19` |
| C5 | `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md` | modify | medium | `governance_learner` | `grok-4.6` | `high` | ✅ `f794b19` |
| C6 | `agents.md` | modify | high | `governance_learner` | `grok-4.6` | `high` | ✅ `f794b19` |

## Ola 3 — F-026-A2

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| F1 | `scripts/check_task_scope.py` | create | high | `devops_agent` — escalated (mechanical → author; see Declared escalations) | `grok-4.6` | `high` | ✅ `f794b19` |
| F2 | `agents/rule_validator.md` | modify | medium | `rule_validator` | `grok-4.6` | `high` | ✅ `f794b19` |
| F3 | `agents/token_economy_agent.md` | modify | medium | `token_economy_agent` | `grok-4.6` | `high` | ✅ `f794b19` |
| F4 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify | low | `governance_learner` | `grok-4.6` | `high` | ✅ `f794b19` |

## Ola 4 — Invocadores

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| I1 | `workflows/pipeline_workflow.md` | modify | medium | `orchestrator` | `grok-4.6` | `high` | ✅ `f794b19` |
| I2 | `workflows/close_workflow.md` | modify | medium | `orchestrator` | `grok-4.6` | `high` | ✅ `f794b19` |
| I3 | `Makefile` | modify | medium | `devops_agent` | `composer-2.5` | N/A | ✅ `f794b19` |

## Ola 5 — Protocolo y ledger

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| E1 | `docs/guides/MODEL_TIER_TRIAL_GUIDE.md` | create | low | `doc_orchestrator` | `grok-4.6` | `high` | ✅ `f794b19` |
| E2 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | low | `orchestrator` | `grok-4.6` | `high` | ✅ `f794b19` |
| L1 | `CHANGELOG.md` | modify | low | `principal_agent` | log from disk | N/A | ✅ `f794b19` |
