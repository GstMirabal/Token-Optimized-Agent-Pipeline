# Skill Assignment — Sprint 038 (`core-pipeline` / family-trial)

Source: `docs/sprints/038-core-pipeline/IMPLEMENTATION_PLAN.md`.
Phase 4.2 of `workflows/pipeline_workflow.md`. Drafted from
`docs/standards/templates/SKILL_ASSIGNMENT_TEMPLATE.md`.

Mode: **Cursor**, `delegation_mode: sequential`.

After writing this file, run:
`python3 scripts/check_forge_ladder.py --sprint-dir docs/sprints/038-core-pipeline`

---

## 1. Priority-1 search performed first

`rules/skills_and_integrations.md §1`: read `skills/manifest_skills.json`.
No existing skill edits `config/model_tiers.json` for a family trial, fixes the
`session_start` UPSTREAM Status counter, or records a D16 gate-replay. Those
are framework config/scripts/docs under `implementer_agent`,
`doc_orchestrator`, and `orchestrator`.
Priority 2 (`autoskills-3rd`) **not** escalated.
Priority 3 (`https://skills.sh/`) **not** queried — no unresolved tool gap.
No new skill forged (Priority 4).

---

## 2. Per-unit tool resolution

| Unit | File(s) | Resolution |
| :--- | :--- | :--- |
| C1 | `config/model_tiers.json` | Class (c) — config map edit. No skill. |
| T1 | `tests/test_session_start.py` | Class (b) — pytest. No skill. |
| M1 | `scripts/session_start.py` | Class (b) — framework script. No skill. |
| D1 | `docs/guides/MODEL_TIER_TRIAL_GUIDE.md` | Class (c) — guide prose. No skill. |
| D2 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | Class (c) — roadmap Status. No skill. |
| R1 | `docs/sprints/038-core-pipeline/GATE_REPLAY.md` | Class (c) — sprint record of D16. Protocol already in `MODEL_TIER_TRIAL_GUIDE.md`. No skill. |

---

## 3. Skills used

| Skill | Why |
| :--- | :--- |
| `token-saver-auditor` (existing) | Phase 1/5 `audit_plan.py` on this plan |
| Built-in `make cursor-tiers` | Catalogue quote for `task_scope.md` Model/Effort |
| Built-in `make model-ledger` | Close regenerates promotion evidence |

## 4. Skills considered and rejected

| Candidate | Why rejected |
| :--- | :--- |
| New "gate-replay" skill | One-off sprint record; protocol lives in the guide (E0/035) |
| New "upstream-status-counter" skill | One function in `session_start.py` with start-workflow invoker |
| `autoskills-3rd` | No unresolved tool gap |
| HTTP client for `skills.sh` | Real HTTP not required; P3 not queried |

## 5. Gaps

None for 038.
