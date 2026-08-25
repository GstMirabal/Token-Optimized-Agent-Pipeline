# Skill Assignment — Sprint 032 (`author-tier-trial`)

Phase 4.2 of `workflows/pipeline_workflow.md`. Implementation Plan at
`docs/sprints/032-core-pipeline/IMPLEMENTATION_PLAN.md`.

---

## 1. Priority-1 search performed first

`rules/skills_and_integrations.md §1`: read `skills/manifest_skills.json`.
No existing skill implements `last_platform_probe` persistence or Cursor
author-tier trial execution. `token-saver-auditor` audits Implementation Plans
only. `audit_cursor_models.py` already proposes tiers (Makefile `cursor-tiers`)
and must not write `config/model_tiers.json` (Sprint 027 §D7). Priority 2
(`autoskills-3rd`) **not** escalated. No new skill forged (Priority 4).

---

## 2. Per-unit tool resolution

| Unit(s) | File(s) | Resolution |
| :--- | :--- | :--- |
| C1 | `config/model_tiers.json` | Class (c) — human-accepted map cell; script proposes only |
| T1 | `tests/test_session_protocol.py` | Class (b) — pytest extension. No new skill. |
| M1 | `scripts/session_probe.py` | Class (b) — existing script gains a writer; not a skill. |
| D1, D2 | trial guide / program queue | Class (c). |

**Gates G1.q / G1.t:** `make verify` + pytest; no new skill.

---

## 3. Skills used

| Skill | Why |
| :--- | :--- |
| `token-saver-auditor` (existing) | Phase 5 `audit_plan.py` on this plan |
| Built-in `make cursor-tiers` | Catalogue quote for `task_scope.md` Model/Effort |
| Built-in `make verify` | Regression after M1 / T1 |

## 4. Skills considered and rejected

| Candidate | Why rejected |
| :--- | :--- |
| New "platform-probe-cache" skill | One writer in existing `session_probe.py` with RA-16 invokers is enough |
| `autoskills-3rd` | No unresolved tool gap |
| Auto-promote `grok-4.5` from `audit_cursor_models.py` | Design §D7 / guide: Human OK only |

## 5. Gaps

None.
