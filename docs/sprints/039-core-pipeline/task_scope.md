# Task Scope — Sprint 039 (`core-pipeline` / start-close-lifecycle)

**Branch**: `ai-sprint/039` · **Base**: `main` at `147868f` (`v4.21.0`)
**Plan**: `docs/sprints/039-core-pipeline/IMPLEMENTATION_PLAN.md`
**Phase**: 4.3 (Rule Audit) — after `agent_assignment.md` (4.1) and
`skill_assignment.md` (4.2).

**Table shape (Work units).** `# | File | Operation | Risk | Assignee | Model | Effort | Status`

**Status legend.** `⏳` pending Phase 6; `✅ <sha>` after execution.

**Mode.** Cursor `delegation_mode: sequential`.

**DAG (from plan).** `L1 → (L2 ∥ L3) → L4` ∥ `C1 → B1 → (B2 ∥ B3 ∥ B4)` ∥
`R1 → R2` ∥ `P1` ∥ `D1` ∥ `D2`. Prefer L1 before L3 tests that call
`refresh-baseline`; C1 before B1 if boot imports stale-check.

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

**Mechanical-eligible this sprint:** `L4`, `B2`, `B3`, `C2`, `R1`, `R2`.

**Gate unit:** none in Phase 6 Work (Double-Gate Phase 7 uses `--resolve gate`).

**No escalations.** No mechanical+high without keep/escalation note (`F-026-A2`).

---

## Work — Track L

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| L1 | `scripts/session_state.py` | modify | high | `implementer_agent` | `glm-5.2` | `high` | ✅ `67142c6` |
| L2 | `workflows/deployment_workflow.md` | modify | medium | `implementer_agent` | `glm-5.2` | `high` | ✅ `46bd454` |
| L3 | `scripts/detect_drift.py` | modify | medium | `implementer_agent` | `glm-5.2` | `high` | ✅ `2421b9d` |
| L4 | `tests/test_session_protocol.py` | modify | medium | `implementer_agent` | `composer-2.5` | `N/A` | ✅ `6a4f6b7` |

## Work — Track B

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| B1 | `scripts/session_start.py` | modify | high | `implementer_agent` | `glm-5.2` | `high` | ✅ `53510da` |
| B2 | `tests/test_session_start.py` | modify | medium | `implementer_agent` | `composer-2.5` | `N/A` | ✅ `00d5a91` |
| B3 | `commands/start.md` | modify | low | `implementer_agent` | `composer-2.5` | `N/A` | ✅ `78856eb` |
| B4 | `workflows/start_workflow.md` | modify | medium | `implementer_agent` | `glm-5.2` | `high` | ✅ `2e07d36` |

## Work — Track C

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| C1 | `scripts/cursor_adapter.py` | modify | medium | `implementer_agent` | `glm-5.2` | `high` | ✅ `4b6bc68` |
| C2 | `tests/test_cursor_adapter.py` | create | medium | `implementer_agent` | `composer-2.5` | `N/A` | ✅ `b20e329` |

## Work — Track R

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| R1 | `config/artifact_registry.json` | modify | low | `implementer_agent` | `composer-2.5` | `N/A` | ✅ `154403a` |
| R2 | `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` | modify | low | `implementer_agent` | `composer-2.5` | `N/A` | ✅ `d81f2fe` |

## Work — Track P

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| P1 | `scripts/session_probe.py` | modify | medium | `implementer_agent` | `glm-5.2` | `high` | ✅ `c7e4146` |

## Work — Track D

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| D1 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | low | `doc_orchestrator` | `glm-5.2` | `high` | ✅ `4a044c6` |
| D2 | `docs/decisions/ADR-0002-drift-verdict-exit-codes.md` | modify | low | `doc_orchestrator` | `glm-5.2` | `high` | ✅ `743dc92` |

---

## Isolation notes

- `jurisdictional_lock`: one physical file per unit / commit.
- P2 fixtures live in L4 (`tests/test_session_protocol.py`) — no second commit
  to that path.
- B1 must not land before C1 if B1 imports `commands_stale` from
  `cursor_adapter` (DAG above).
