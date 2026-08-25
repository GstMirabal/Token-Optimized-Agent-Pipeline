# Task Scope — Sprint 033 (`implementer-role`)

**Branch**: `ai-sprint/033` · **Base**: `main` at `8b3fb6d` (`v4.15.0`)
**Plan**: `docs/sprints/033-core-pipeline/IMPLEMENTATION_PLAN.md` (committed `b078360`)
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
| Accept Cursor model into `config/model_tiers.json` | **Human** | map already set by Sprint 032 | Sprint 027 Design §D7 |

---

## Measured Cursor state (this session, 2026-08-25)

```text
make cursor-tiers   # → python3 scripts/audit_cursor_models.py ; echo exit=$?
exit=0
Models after hard filters (excl. default): 35
Applied model (author cold-start candidate): grok-4.6
Proposed author (≤1, cold start): grok-4.6 (depth_lever yes)
Catalogue includes grok-4.5 (xai, depth_lever yes)
Proposed mechanical (no depth lever): composer-2.5, gemini-3.1-pro, gemini-3-flash,
  gemini-3.5-flash, gpt-5-mini
Proposed gate: (none) — Design §D7, not proven history
Proposals only — config/model_tiers.json was not modified
```

**Map in force (Sprint 032 promote).** `cursor.author` = `grok-4.5` / `high`;
`cursor.mechanical` = `composer-2.5`; `cursor.gate.model` = `null`. Reproduce:
`python3 -c "import json; a=json.load(open('config/model_tiers.json'))['tiers']['author']['cursor']; print(a['model'], a['effort'])"`.

Global medidor may still report `grok-4.6` (per-chat override invisible to
`applicationOpenModelAppliedConfig`). Work rows use the **map** (`grok-4.5` /
`high`), not the cold-start proposal string.

## Cursor tier map (post-032 promote)

| Intent (phase) | Claude Code (reference only) | Cursor | Effort / depth |
| :--- | :--- | :--- | :--- |
| `mechanical` | `haiku` / `low` | **`composer-2.5`** | **N/A** |
| `author` | `sonnet` / `medium` | **`grok-4.5`** | **`high`** |
| `gate` | `opus` / `high` | **`null` in config** | Operational: log applied model from disk at gate time |

---

## Declared escalations — `token_economy_agent` audit, transcribed per `tier_escalation`

None. Every Work unit assignee is already `tier: author` (`agent_orchestrator`,
`doc_orchestrator`, `implementer_agent`). No mechanical→author row.

---

## Ola 0 — Decision record

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| A0 | `docs/decisions/ADR-0009-implementer-role.md` | create | high | `doc_orchestrator` | `grok-4.5` | `high` | ✅ `3c47367` |

## Ola 1 — Role map

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| A1 | `agents/implementer_agent.md` | create | high | `agent_orchestrator` | `grok-4.5` | `high` | ✅ `bdc5b89` |
| A2 | `agents/devops_agent.md` | modify | high | `agent_orchestrator` | `grok-4.5` | `high` | ✅ `a5b7eec` |
| A3 | `agents.md` | modify | high | `agent_orchestrator` | `grok-4.5` | `high` | ✅ `546b5fa` |
| A4 | `agents/agent_orchestrator.md` | modify | medium | `agent_orchestrator` | `grok-4.5` | `high` | ✅ `681d27b` |

## Ola 2 — Pin (after A1)

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T1 | `tests/test_implementer_role.py` | create | medium | `implementer_agent` | `grok-4.5` | `high` | ✅ `b53e629` |

## Ola 3 — Documentary (not closeout ledger)

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| R1 | `README.md` | modify | low | `doc_orchestrator` | `grok-4.5` | `high` | ✅ `130431b` |
| F1 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify | medium | `doc_orchestrator` | `grok-4.5` | `high` | ✅ `fd5c7f8` |
| Q1 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | low | `doc_orchestrator` | `grok-4.5` | `high` | ✅ `ed876fa` |
