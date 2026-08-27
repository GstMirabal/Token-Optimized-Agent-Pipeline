# Skill Assignment — Sprint 040 (`core-pipeline` / cursor-bridge-incremental)

Source: `docs/sprints/040-core-pipeline/IMPLEMENTATION_PLAN.md`.
Phase 4.2 of `workflows/pipeline_workflow.md`. Drafted from
`docs/standards/templates/SKILL_ASSIGNMENT_TEMPLATE.md`.

Mode: **Cursor**, `delegation_mode: sequential`.

After writing this file, run:
`python3 scripts/check_forge_ladder.py --sprint-dir docs/sprints/040-core-pipeline`

---

## 1. Priority-1 search performed first

`rules/skills_and_integrations.md §1`: read `skills/manifest_skills.json`.
No existing skill implements incremental `.cursor/` install, lock-only bridge
refresh, or boot soft-fail on `PermissionError`. Those are framework scripts
and workflows under `implementer_agent` / `doc_orchestrator`.
Priority 2 (`autoskills-3rd`) **not** escalated.
Priority 3 (`https://skills.sh/`) **not** queried — no unresolved tool gap.
No new skill forged (Priority 4).

---

## 2. Per-unit tool resolution

| Unit | File(s) | Resolution |
| :--- | :--- | :--- |
| I1 | `scripts/cursor_adapter.py` | Class (b) — framework script. No skill. |
| I2 | `tests/test_cursor_adapter.py` | Class (b) — pytest. No skill. |
| S1 | `scripts/session_start.py` | Class (b) — framework script. No skill. |
| S2 | `tests/test_session_start.py` | Class (b) — pytest. No skill. |
| W1 | `workflows/start_workflow.md` | Class (c) — workflow prose. No skill. |
| D1 | `workflows/deployment_workflow.md` | Class (c) — workflow prose. No skill. |
| R1 | `scripts/session_state.py` | Class (b) — framework script. No skill. |
| R2 | `tests/test_session_protocol.py` | Class (b) — pytest. No skill. |
| P1 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | Class (c) — roadmap Status. No skill. |

---

## 3. Skills used

| Skill | Why |
| :--- | :--- |
| `token-saver-auditor` (existing) | Phase 1/5 `audit_plan.py` on this plan |
| Built-in `make cursor-tiers` | Catalogue quote for `task_scope.md` Model/Effort |

## 4. Skills considered and rejected

| Candidate | Why rejected |
| :--- | :--- |
| New skill for bridge install | Would duplicate `scripts/cursor_adapter.py` / `install.py` |

## 5. Forge declaration

**No skill was forged.** P1–P3: no tool gap; framework scripts cover the work.
P3 trail: Priority-1 search of `skills/manifest_skills.json` found no match;
Priorities 2–3 not escalated because the gap is framework-owned scripts, not a
missing computational skill.
