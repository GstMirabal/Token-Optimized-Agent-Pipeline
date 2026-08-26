# Skill Assignment — Sprint 037 (`core-pipeline`)

Source: `docs/sprints/037-core-pipeline/IMPLEMENTATION_PLAN.md`.
Phase 4.2 of `workflows/pipeline_workflow.md`. Drafted from
`docs/standards/templates/SKILL_ASSIGNMENT_TEMPLATE.md`.

Mode: **Cursor**, `delegation_mode: sequential`.

After writing this file, run:
`python3 scripts/check_forge_ladder.py --sprint-dir docs/sprints/037-core-pipeline`

---

## 1. Priority-1 search performed first

`rules/skills_and_integrations.md §1`: read `skills/manifest_skills.json`.
No existing skill generates a gate/task_scope ledger, patches Makefile
py_compile without `xargs`, or writes nucleus `.bridge_cursor.lock`. Those are
framework-root scripts (`implementer_agent`) or workflow prose (`orchestrator`).
Priority 2 (`autoskills-3rd`) **not** escalated.
Priority 3 (`https://skills.sh/`) **not** queried — no unresolved tool gap.
No new skill forged (Priority 4).

---

## 2. Per-unit tool resolution

| Unit | File(s) | Resolution |
| :--- | :--- | :--- |
| G1 | `scripts/model_ledger.py` | Class (b) — script wrapping existing parsers. No skill. |
| G2 | `tests/test_model_ledger.py` | Class (b) — pytest. No skill. |
| G3 | `workflows/close_workflow.md` | Class (c) — names `make model-ledger`. No skill. |
| S1 | `Makefile` | Class (b)/(c) — make recipe. No skill. |
| S2 | `tests/test_verify_py_compile.py` | Class (b) — pytest. No skill. |
| S3 | `scripts/install.py` | Class (b) — installer. No skill. |
| S4 | `tests/test_installer.sh` | Class (b) — shell fixture. No skill. |

---

## 3. Skills used

| Skill | Why |
| :--- | :--- |
| `token-saver-auditor` (existing) | Phase 1/5 `audit_plan.py` on this plan |
| Built-in `make cursor-tiers` | Catalogue quote for `task_scope.md` Model/Effort |

## 4. Skills considered and rejected

| Candidate | Why rejected |
| :--- | :--- |
| New "model-ledger" skill | One script under `scripts/` with `RA-16` invoker (`make model-ledger` + close) |
| New "py-compile-tree" skill | Q1 chose Makefile `find -exec`; no separate skill |
| `autoskills-3rd` | No unresolved tool gap |
| HTTP client for `skills.sh` | Real HTTP not required; P3 not queried |

## 5. Gaps

None for 037. Family-trial remains **038**.
