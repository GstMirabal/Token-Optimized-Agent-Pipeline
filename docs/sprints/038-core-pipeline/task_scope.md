# Task Scope — Sprint 038 (`core-pipeline` / family-trial)

**Branch**: `ai-sprint/038` · **Base**: `main` at `171531a` (`v4.20.0` + reconcile)
**Plan**: `docs/sprints/038-core-pipeline/IMPLEMENTATION_PLAN.md`
**Phase**: 4.3 (Rule Audit) — after `agent_assignment.md` (4.1) and
`skill_assignment.md` (4.2).

**Table shape (Work units).** `# | File | Operation | Risk | Assignee | Model | Effort | Status`

**Status legend.** `⏳` pending Phase 6; `✅ <sha>` after execution.

**Mode.** Cursor `delegation_mode: sequential`.

**DAG (from plan).** `C1 → (T1 → M1)` ∥ `D1` ∥ `D2` ∥ `R1`. Prefer C1 before any
other authorship so T/D units run under the trial author map.

---

## Ownership map (who does what)

| Concern | Decides | Writes the artifact | Source of truth |
| :--- | :--- | :--- | :--- |
| Profile per unit | `agent_orchestrator` | `agent_assignment.md` | Phase 4.1 |
| File lock / risk / status | `rule_validator` | this file (Work tables) | Phase 4.3 |
| Tier escalation + Cursor model/effort | `token_economy_agent` | transcribed here by `rule_validator` | `tier_escalation` + **`make cursor-tiers` run this session** |
| Accept Cursor model into `config/model_tiers.json` | **Human** at Phase 8 (promote or revert C1) | C1 writes trial cell; close seals | D6 / D12; Q1 Human OK |

---

## Measured Cursor state (this session, 2026-08-26, pre-C1)

```text
make cursor-tiers   # → python3 scripts/audit_cursor_models.py --check
exit=0
Models after hard filters (excl. default): 35
Map author cell: grok-4.5
Applied model (discrepancy): grok-4.6 — differs from map author grok-4.5
Proposed author (map cell): grok-4.5
Proposed mechanical (no depth lever): composer-2.5, …
Proposed gate (structural ceiling; family ≠ map author): claude-opus-5 et al.
--check OK — gate proposals present.
Proposals only — config/model_tiers.json was not modified.
```

**Map in force before C1.** `cursor.author` = `grok-4.5` / `high`;
`cursor.mechanical` = `composer-2.5`; `cursor.gate` = `claude-opus-5` / `max`.

**Trial map after C1 (Q1).** `cursor.author` = `glm-5.2` / `zhipu` / `high`
(gate family remains `anthropic` — D15). Work rows below use the **trial**
author slug for T/D units; R1 uses gate. Reproduce after C1:
`python3 scripts/audit_cursor_models.py --resolve author` → `glm-5.2`/`high`;
`--resolve mechanical` → `composer-2.5`; `--resolve gate` → `claude-opus-5`/`max`.

## Cursor tier map (trial intent)

| Intent (phase) | Claude Code (reference only) | Cursor | Effort / depth |
| :--- | :--- | :--- | :--- |
| `mechanical` | `haiku` / `low` | **`composer-2.5`** | **N/A** |
| `author` (trial) | `sonnet` / `medium` | **`glm-5.2`** | **`high`** |
| `gate` | `opus` / `high` | **`claude-opus-5`** | **`max`** |

**Mechanical-eligible this sprint (plan Cost):** `T1`.

**Gate unit:** `R1` — `qa_agent` emits via `Task` + `--resolve gate`;
`orchestrator` writes `GATE_REPLAY.md` (`ADR-0010`, `F-026-A1`).

**C1 staffing:** `implementer_agent` applies the map cell; `token_economy_agent`
remains accountable owner (`tier_ownership`) without `Write`/`Edit`.

**No escalations.** No mechanical+high without keep/escalation note (`F-026-A2`).

---

## Work — Track T

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| C1 | `config/model_tiers.json` | modify | medium | `implementer_agent` | `glm-5.2` | `high` | ⏳ |
| T1 | `tests/test_session_start.py` | modify | medium | `implementer_agent` | `composer-2.5` | `N/A` | ⏳ |
| M1 | `scripts/session_start.py` | modify | high | `implementer_agent` | `glm-5.2` | `high` | ⏳ |
| D1 | `docs/guides/MODEL_TIER_TRIAL_GUIDE.md` | modify | low | `doc_orchestrator` | `glm-5.2` | `high` | ⏳ |
| D2 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | low | `doc_orchestrator` | `glm-5.2` | `high` | ⏳ |

## Work — Track R

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| R1 | `docs/sprints/038-core-pipeline/GATE_REPLAY.md` | create | medium | `orchestrator` | `claude-opus-5` | `max` | ⏳ |

---

## Jurisdictional lock notes

| File | Units (order) | Rule |
| :--- | :--- | :--- |
| `config/model_tiers.json` | C1 only | Trial author cell; Phase 8 promote or revert same file |
| `tests/test_session_start.py` | T1 before M1 | `RA-13` — fail against current tree first |
| `scripts/session_start.py` | M1 after T1 | Max-sprint Status table only |
| `docs/guides/MODEL_TIER_TRIAL_GUIDE.md` | D1 | Candidate 038 = `glm-5.2` |
| `docs/roadmaps/core/pipeline/021-030-program-queue.md` | D2 | Status in flight |
| `docs/sprints/038-core-pipeline/GATE_REPLAY.md` | R1 | 032 then 033; ADR-0008 vocab; no family ranking |

`no_interference`: no other IN_PROGRESS subtask lists these paths.
