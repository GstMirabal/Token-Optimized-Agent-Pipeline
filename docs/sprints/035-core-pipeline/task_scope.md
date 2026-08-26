# Task Scope — Sprint 035 (`core-pipeline`)

**Branch**: `ai-sprint/035` · **Base**: `main` at `c93e851` (`v4.17.0`)
**Plan**: `docs/sprints/035-core-pipeline/IMPLEMENTATION_PLAN.md`
**Phase**: 4.3 (Rule Audit) — after `agent_assignment.md` (4.1) and
`skill_assignment.md` (4.2).

**Table shape (Work units).** `# | File | Operation | Risk | Assignee | Model | Effort | Status`

**Status legend.** `⏳` pending Phase 6; `✅ <sha>` after execution.

**Mode.** Cursor `delegation_mode: sequential`.

**DAG (from plan).** `E0 → E1 → E2 → E3 → E4 → E5 → E6 → C5`; `H2` and `C5`
**after** E6; `C1 → C4`; `C2 → C3`; `H1 → H2 → H3 → H4`; `F3` parallel (no
file collision with E/H/C).

---

## Ownership map (who does what)

| Concern | Decides | Writes the artifact | Source of truth |
| :--- | :--- | :--- | :--- |
| Profile per unit | `agent_orchestrator` | `agent_assignment.md` | Phase 4.1 |
| File lock / risk / status | `rule_validator` | this file (Work tables) | Phase 4.3 |
| Tier escalation + Cursor model/effort | `token_economy_agent` | transcribed here by `rule_validator` | `tier_escalation` + **`make cursor-tiers` run this session** |
| Accept Cursor model into `config/model_tiers.json` | **Human** (H2 fills `gate` by structural ceiling) | map author/mechanical already set by Sprint 032 | Sprint 027 Design §D7; 035 D13/H2 |

---

## Measured Cursor state (this session, 2026-08-26)

```text
make cursor-tiers   # → python3 scripts/audit_cursor_models.py ; echo exit=$?
exit=0
Models after hard filters (excl. default): 35
Applied model (author cold-start candidate): grok-4.6
Proposed author (≤1, cold start): grok-4.6 (depth_lever yes)
Catalogue includes grok-4.5 (xai, depth_lever yes)
Proposed mechanical (no depth lever): composer-2.5, gemini-3.1-pro,
  gemini-3.5-flash, gpt-5-mini, gemini-2.5-flash
Proposed gate: (none) — Design §D7, not proven history
Proposals only — config/model_tiers.json was not modified
```

**Map in force (Sprint 032 promote).** `cursor.author` = `grok-4.5` / `high`;
`cursor.mechanical` = `composer-2.5`; `cursor.gate.model` = `null` until H2.
Reproduce:
`python3 -c "import json; a=json.load(open('config/model_tiers.json'))['tiers']['author']['cursor']; print(a['model'], a['effort'])"`.

Work rows use the **map** (`grok-4.5` / `high` for author; `composer-2.5` /
`N/A` for mechanical), not the cold-start proposal string `grok-4.6`.

## Cursor tier map (post-032; gate pending H2)

| Intent (phase) | Claude Code (reference only) | Cursor | Effort / depth |
| :--- | :--- | :--- | :--- |
| `mechanical` | `haiku` / `low` | **`composer-2.5`** | **N/A** |
| `author` | `sonnet` / `medium` | **`grok-4.5`** | **`high`** |
| `gate` | `opus` / `high` | **`null` → session** until H2 | — |

**Mechanical-eligible this sprint (plan Cost):** `C4`, `E4`, `H4`.

**No escalations.** No row keeps author when mechanical applies; no
mechanical+high without keep/escalation note (`F-026-A2`).

---

## Work — Track E

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| E0 | `docs/guides/MODEL_TIER_TRIAL_GUIDE.md` | modify | medium | `doc_orchestrator` | `grok-4.5` | `high` | ✅ `f636fdd` |
| E1 | `docs/decisions/ADR-0010-cursor-task-applies-tier-map.md` | create | high | `doc_orchestrator` | `grok-4.5` | `high` | ✅ `45ef87e` |
| E2 | `scripts/audit_cursor_models.py` | modify | high | `implementer_agent` | `grok-4.5` | `high` | ✅ `a181a11` |
| E3 | `workflows/pipeline_workflow.md` | modify | high | `orchestrator` | `grok-4.5` | `high` | ✅ `0ee4901` |
| E4 | `tests/test_audit_cursor_models.py` | create | medium | `implementer_agent` | `composer-2.5` | `N/A` | ✅ `baf42d0` |
| E5 | `scripts/audit_cursor_models.py` | modify | high | `implementer_agent` | `grok-4.5` | `high` | ✅ `e1d562e` |
| E6 | `scripts/audit_cursor_models.py` | modify | high | `implementer_agent` | `grok-4.5` | `high` | ⏳ |

## Work — Track C

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| C1 | `scripts/session_start.py` | create | high | `implementer_agent` | `grok-4.5` | `high` | ⏳ |
| C2 | `workflows/start_workflow.md` | modify | high | `orchestrator` | `grok-4.5` | `high` | ⏳ |
| C3 | `commands/start.md` | modify | low | `orchestrator` | `grok-4.5` | `high` | ⏳ |
| C4 | `tests/test_session_start.py` | create | medium | `implementer_agent` | `composer-2.5` | `N/A` | ⏳ |
| C5 | `Makefile` | modify | medium | `implementer_agent` | `grok-4.5` | `high` | ⏳ |

## Work — Track H

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| H1 | `docs/decisions/ADR-0011-gate-cell-by-structural-ceiling.md` | create | high | `doc_orchestrator` | `grok-4.5` | `high` | ⏳ |
| H2 | `config/model_tiers.json` | modify | high | `rule_validator` | `grok-4.5` | `high` | ⏳ |
| H3 | `scripts/verify_references.py` | modify | high | `implementer_agent` | `grok-4.5` | `high` | ⏳ |
| H4 | `tests/test_verify_references.py` | modify | medium | `implementer_agent` | `composer-2.5` | `N/A` | ⏳ |

## Work — Track F

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| F3 | `agents/token_economy_agent.md` | modify | medium | `agent_orchestrator` | `grok-4.5` | `high` | ⏳ |

---

## File locks (`jurisdictional_lock` / `no_interference`)

| File | Units (order) |
| :--- | :--- |
| `scripts/audit_cursor_models.py` | E2 → E5 → E6 (sequential commits; never concurrent) |
| `workflows/start_workflow.md` | C2 only in 035 (P3 already closed in 034) |
| `workflows/pipeline_workflow.md` | E3 only in 035 (M5 is 036) |
| `Makefile` | C5 only in 035 (L3 is 036) |
| `config/model_tiers.json` | H2 only |
| `agents/token_economy_agent.md` | F3 only |

No other in-progress sprint lists these paths in `task_scope.md`.
