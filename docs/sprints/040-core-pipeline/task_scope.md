# Task Scope — Sprint 040 (`core-pipeline` / cursor-bridge-incremental)

**Branch**: `ai-sprint/040` · **Base**: `main` at `8268fc1` (`v4.22.0`)
**Plan**: `docs/sprints/040-core-pipeline/IMPLEMENTATION_PLAN.md`
**Phase**: 4.3 (Rule Audit) — after `agent_assignment.md` (4.1) and
`skill_assignment.md` (4.2).

**Table shape (Work units).** `# | File | Operation | Risk | Assignee | Model | Effort | Status`

**Status legend.** `⏳` pending Phase 6; `✅ <sha>` after execution.

**Mode.** Cursor `delegation_mode: sequential`.

**DAG (from plan).** `I1 → (I2 ∥ S1)` → `S2` ∥ `W1` ∥ `D1` (after S1) ∥
`R1 → R2` ∥ `P1`. Prefer I1 before S1 (boot assumes incremental install).

---

## Ownership map (who does what)

| Concern | Decides | Writes the artifact | Source of truth |
| :--- | :--- | :--- | :--- |
| Profile per unit | `agent_orchestrator` | `agent_assignment.md` | Phase 4.1 |
| File lock / risk / status | `rule_validator` | this file (Work tables) | Phase 4.3 |
| Tier escalation + Cursor model/effort | `token_economy_agent` | transcribed here by `rule_validator` | `tier_escalation` + **`make cursor-tiers` run this session** |
| Accept Cursor model into `config/model_tiers.json` | **Human** | not in scope this sprint | — |

---

## Measured Cursor state (this session, 2026-08-27)

```text
make cursor-tiers   # → python3 scripts/audit_cursor_models.py --check
exit=0
Map author cell: glm-5.2 / zhipu / high
Proposed mechanical (no depth lever): composer-2.5, …
Proposed gate (structural ceiling; family ≠ map author): claude-opus-5 et al.
--check OK — gate proposals present.
Proposals only — config/model_tiers.json was not modified.
--resolve author → modelId=glm-5.2 effort=high
--resolve mechanical → modelId=composer-2.5
--resolve gate → modelId=claude-opus-5 effort=max
```

## Cursor tier map (in force)

| Intent (phase) | Claude Code (reference only) | Cursor | Effort / depth |
| :--- | :--- | :--- | :--- |
| `mechanical` | `haiku` / `low` | **`composer-2.5`** | **N/A** |
| `author` | `sonnet` / `medium` | **`glm-5.2`** | **`high`** |
| `gate` | `opus` / `high` | **`claude-opus-5`** | **`max`** |

**Mechanical-eligible this sprint:** `I2`, `S2`, `R2`, `P1`.

**Author (non-mechanical):** `I1`, `S1`, `W1`, `D1`, `R1`.

**Gate unit:** none in Phase 6 Work (Double-Gate Phase 7 uses `--resolve gate`).

**No escalations.** No mechanical+high without keep/escalation note (`F-026-A2`).

---

## Work — Track I

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| I1 | `scripts/cursor_adapter.py` | modify | high | `implementer_agent` | `glm-5.2` | `high` | ✅ `309ccbd` |
| I2 | `tests/test_cursor_adapter.py` | modify | medium | `implementer_agent` | `composer-2.5` | `N/A` | ✅ `5a93c99` |

## Work — Track S

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| S1 | `scripts/session_start.py` | modify | high | `implementer_agent` | `glm-5.2` | `high` | ✅ `4f29a8b` |
| S2 | `tests/test_session_start.py` | modify | medium | `implementer_agent` | `composer-2.5` | `N/A` | ✅ `7c3f52a` |

## Work — Track W / D

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| W1 | `workflows/start_workflow.md` | modify | medium | `implementer_agent` | `glm-5.2` | `high` | ✅ `9c3a080` |
| D1 | `workflows/deployment_workflow.md` | modify | medium | `implementer_agent` | `glm-5.2` | `high` | ✅ `c233d9e` |

## Work — Track R

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| R1 | `scripts/session_state.py` | modify | medium | `implementer_agent` | `glm-5.2` | `high` | ✅ `7b670ef` |
| R2 | `tests/test_session_protocol.py` | modify | low | `implementer_agent` | `composer-2.5` | `N/A` | ✅ `3ba1d1d` |

## Work — Track P

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| P1 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | low | `doc_orchestrator` | `composer-2.5` | `N/A` | ✅ `f127e6d` |

---

## Interference / jurisdictional notes

| Rule | Check |
| :--- | :--- |
| `jurisdictional_lock` | One physical file per unit (plan Work tables) |
| `no_interference` | No overlapping targets across in-progress rows |
