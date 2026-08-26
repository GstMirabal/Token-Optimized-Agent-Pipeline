# Task Scope — Sprint 036 (`core-pipeline`)

**Branch**: `ai-sprint/036` · **Base**: `main` at `ba80a55` (`v4.18.0`)
**Plan**: `docs/sprints/036-core-pipeline/IMPLEMENTATION_PLAN.md`
**Phase**: 4.3 (Rule Audit) — after `agent_assignment.md` (4.1) and
`skill_assignment.md` (4.2).

**Table shape (Work units).** `# | File | Operation | Risk | Assignee | Model | Effort | Status`

**Status legend.** `⏳` pending Phase 6; `✅ <sha>` after execution.

**Mode.** Cursor `delegation_mode: sequential`.

**DAG (from plan).** `L1+L2 → L3` ∥ `M1+M2 → M3 → M4 → M5 → M6 → M7 → M8 → M9`
(M3/M4/M6 reorderable after M2 if no file collision; M7→M8→M9 fixed).
L3 = second `Makefile` touch (after C5/035). M5 = `pipeline_workflow.md`
after E3/035.

---

## Ownership map (who does what)

| Concern | Decides | Writes the artifact | Source of truth |
| :--- | :--- | :--- | :--- |
| Profile per unit | `agent_orchestrator` | `agent_assignment.md` | Phase 4.1 |
| File lock / risk / status | `rule_validator` | this file (Work tables) | Phase 4.3 |
| Tier escalation + Cursor model/effort | `token_economy_agent` | transcribed here by `rule_validator` | `tier_escalation` + **`make cursor-tiers` run this session** |
| Accept Cursor model into `config/model_tiers.json` | **Human** (map already set; gate filled in 035 H2) | Sprint 032 author/mechanical; 035 H2 gate | Sprint 027 Design §D7; ADR-0011 |

---

## Measured Cursor state (this session, 2026-08-26)

```text
make cursor-tiers   # → python3 scripts/audit_cursor_models.py --check
exit=0
Models after hard filters (excl. default): 35
Map author cell: grok-4.5
Applied model (discrepancy): grok-4.6 — differs from map author grok-4.5
Proposed author (map cell): grok-4.5
Proposed mechanical (no depth lever): composer-2.5, gemini-3.1-pro,
  gemini-3.5-flash, gpt-5-mini, gemini-2.5-flash
Proposed gate (structural ceiling; family ≠ map author): claude-opus-5 et al.
--check OK — gate proposals present.
Proposals only — config/model_tiers.json was not modified.
```

**Map in force.** `cursor.author` = `grok-4.5` / `high`;
`cursor.mechanical` = `composer-2.5`; `cursor.gate` = `claude-opus-5` / `max`
(035 H2). Reproduce:
`python3 scripts/audit_cursor_models.py --resolve author` → `grok-4.5`/`high`;
`--resolve mechanical` → `composer-2.5`; `--resolve gate` → `claude-opus-5`/`max`.

Work rows use the **map**, not the applied discrepancy `grok-4.6`.

## Cursor tier map (post-035)

| Intent (phase) | Claude Code (reference only) | Cursor | Effort / depth |
| :--- | :--- | :--- | :--- |
| `mechanical` | `haiku` / `low` | **`composer-2.5`** | **N/A** |
| `author` | `sonnet` / `medium` | **`grok-4.5`** | **`high`** |
| `gate` | `opus` / `high` | **`claude-opus-5`** | **`max`** |

**Mechanical-eligible this sprint (plan Cost):** `L2`, `M2`, `M6`.

**No escalations.** No row keeps author when mechanical applies; no
mechanical+high without keep/escalation note (`F-026-A2`).

---

## Work — Track L

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| L1 | `scripts/audit_cursor_era.py` | create | high | `implementer_agent` | `grok-4.5` | `high` | ⏳ |
| L2 | `tests/test_audit_cursor_era.py` | create | medium | `implementer_agent` | `composer-2.5` | `N/A` | ⏳ |
| L3 | `Makefile` | modify | medium | `implementer_agent` | `grok-4.5` | `high` | ⏳ |

## Work — Track M

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| M1 | `scripts/check_forge_ladder.py` | create | high | `implementer_agent` | `grok-4.5` | `high` | ⏳ |
| M2 | `tests/test_check_forge_ladder.py` | create | medium | `implementer_agent` | `composer-2.5` | `N/A` | ⏳ |
| M3 | `agents/skill_architect.md` | modify | high | `agent_orchestrator` | `grok-4.5` | `high` | ⏳ |
| M4 | `docs/standards/templates/SKILL_ASSIGNMENT_TEMPLATE.md` | create | medium | `doc_orchestrator` | `grok-4.5` | `high` | ⏳ |
| M5 | `workflows/pipeline_workflow.md` | modify | high | `orchestrator` | `grok-4.5` | `high` | ⏳ |
| M6 | `tests/test_agent_profile_census.py` | create | medium | `implementer_agent` | `composer-2.5` | `N/A` | ⏳ |
| M7 | `agents/qa_agent.md` | modify | high | `agent_orchestrator` | `grok-4.5` | `high` | ⏳ |
| M8 | `agents/tester_agent.md` | modify | high | `agent_orchestrator` | `grok-4.5` | `high` | ⏳ |
| M9 | `agents/principal_agent.md` | modify | high | `agent_orchestrator` | `grok-4.5` | `high` | ⏳ |

---

## Jurisdictional lock notes

| File | Units (order) | Rule |
| :--- | :--- | :--- |
| `Makefile` | L3 only this sprint | Second touch after C5/035; do not merge with verify recipe |
| `workflows/pipeline_workflow.md` | M5 only this sprint | After E3/035; name `check_forge_ladder.py` in 4.1 and 4.2 |
| `agents/qa_agent.md` / `tester_agent.md` / `principal_agent.md` | M7 → M8 → M9 | Sequential; no Write/Edit added |
| `scripts/audit_cursor_era.py` | L1 then L2 tests | L1+L2 may share one commit (plan) |
| `scripts/check_forge_ladder.py` | M1 then M2 tests | M1+M2 may share one commit (plan) |

`no_interference`: no other IN_PROGRESS subtask lists these paths.
