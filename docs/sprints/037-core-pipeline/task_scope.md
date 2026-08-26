# Task Scope — Sprint 037 (`core-pipeline`)

**Branch**: `ai-sprint/037` · **Base**: `main` at `6a87cf0` (`v4.19.0`)
**Plan**: `docs/sprints/037-core-pipeline/IMPLEMENTATION_PLAN.md`
**Phase**: 4.3 (Rule Audit) — after `agent_assignment.md` (4.1) and
`skill_assignment.md` (4.2).

**Table shape (Work units).** `# | File | Operation | Risk | Assignee | Model | Effort | Status`

**Status legend.** `⏳` pending Phase 6; `✅ <sha>` after execution.

**Mode.** Cursor `delegation_mode: sequential`.

**DAG (from plan).** `G1+G2 → G3` ∥ `S1+S2` ∥ `S3+S4`. S independent of G.
S1 = third `Makefile` touch (after C5/035, L3/036).

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

**Mechanical-eligible this sprint (plan Cost):** `G2`, `S2`, `S4`.

**No escalations.** No row keeps author when mechanical applies; no
mechanical+high without keep/escalation note (`F-026-A2`).

---

## Work — Track G

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| G1 | `scripts/model_ledger.py` | create | high | `implementer_agent` | `grok-4.5` | `high` | ✅ `b360904` |
| G2 | `tests/test_model_ledger.py` | create | medium | `implementer_agent` | `composer-2.5` | `N/A` | ✅ `b360904` |
| G3 | `workflows/close_workflow.md` | modify | medium | `orchestrator` | `grok-4.5` | `high` | ✅ `925a62d` |

## Work — Track S

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| S1 | `Makefile` | modify | high | `implementer_agent` | `grok-4.5` | `high` | ✅ `82ee3ba` |
| S2 | `tests/test_verify_py_compile.py` | create | medium | `implementer_agent` | `composer-2.5` | `N/A` | ✅ `82ee3ba` |
| S3 | `scripts/install.py` | modify | high | `implementer_agent` | `grok-4.5` | `high` | ✅ `668196a` |
| S4 | `tests/test_installer.sh` | modify | medium | `implementer_agent` | `composer-2.5` | `N/A` | ✅ `668196a` |

---

## Jurisdictional lock notes

| File | Units (order) | Rule |
| :--- | :--- | :--- |
| `scripts/model_ledger.py` | G1 then G2 tests | G1+G2 may share one commit (plan) |
| `workflows/close_workflow.md` | G3 after G1+G2 | Names `make model-ledger` (`RA-16`) |
| `scripts/py_compile_tree.py` | S1 prerequisite | `find -exec` still hits `SC_ARG_MAX` in agent sandbox; script is the compile path |
| `Makefile` | S1 only this sprint | Third touch after C5/035 and L3/036; wires `py_compile_tree` + live `model-ledger` |
| `tests/test_verify_py_compile.py` | S2 with S1 | Same commit as S1 Makefile wire |
| `scripts/install.py` | S3 then S4 | S3+S4 may share one commit (plan) |

`no_interference`: no other IN_PROGRESS subtask lists these paths.
