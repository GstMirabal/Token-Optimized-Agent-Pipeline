# Skill Assignment — Sprint 030 (`token-economy-enforcement`)

Phase 4.2 of `workflows/pipeline_workflow.md`. Implementation Plan at
`docs/sprints/030-core-pipeline/IMPLEMENTATION_PLAN.md`.

---

## 1. Priority-1 search performed first

`rules/skills_and_integrations.md §1`: read `skills/manifest_skills.json`.
Priority 2 (`autoskills-3rd`) **not** escalated — no unit blocked after Priority 1.

---

## 2. Per-unit tool resolution

| Unit(s) | File(s) | Resolution |
| :--- | :--- | :--- |
| A0, T0, C0 | tests | Class (b) — pytest. No new skill. |
| A1 | `__init__.py` | Class (b) — Three-File package marker. |
| A2 | `audit_plan.py` | Class (b) — new script under existing skill path. |
| A3, A4 | SKILL.md / README.md | Class (c) — skill docs. |
| C1, C2 | `session_cost.py` / `session_probe.py` | Class (b) — extend existing meters. |
| C3 | `rule_triggers.json` | Class (b) — existing registry. |
| C4 | `token_economy.md` | Class (c). |
| C5 | Implementation Plan template | Class (c). |
| C6 | `agents.md` | Class (c) — one trigger line. |
| F1 | `check_task_scope.py` | Class (b) — new script. |
| F2, F3 | agent profiles | Class (c). |
| F4 | upstream findings | Class (c). |
| I1, I2 | workflows | Class (c). |
| I3 | `Makefile` | Class (b). |
| E1 | trial guide | Class (c) — Diátaxis how-to. |
| E2, L1 | roadmap / CHANGELOG | Class (c). |

**Gates G1.q / G1.t:** `make verify` + pytest; no new skill.

---

## 3. Skills used

| Skill | Why |
| :--- | :--- |
| `token-saver-auditor` | **Body forged this sprint** (`scripts/audit_plan.py`); was knowledge-only |
| `mass-standardizer` (existing) | Regenerates `manifest_skills.json` after Three-File change |
| Built-in `make verify` | Invokes `audit_plan.py --current-sprint` and `check_task_scope.py --current-sprint` |

## 4. Skills considered and rejected

| Candidate | Why rejected |
| :--- | :--- |
| Retire `token-saver-auditor` | Rejected in Design D1 — Filters 1–4/6 would lose an invoker |
| New "task-scope-auditor" skill | One script under `scripts/` with RA-16 invokers is enough |
| `autoskills-3rd` | No unresolved tool gap |
| Reimplement Filter 5 inside `audit_plan.py` | Already owned by `scan_workflow_determinism.py` |

## 5. Gaps

None.
