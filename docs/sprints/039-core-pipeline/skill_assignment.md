# Skill Assignment — Sprint 039 (`core-pipeline` / start-close-lifecycle)

Source: `docs/sprints/039-core-pipeline/IMPLEMENTATION_PLAN.md`.
Phase 4.2 of `workflows/pipeline_workflow.md`. Drafted from
`docs/standards/templates/SKILL_ASSIGNMENT_TEMPLATE.md`.

Mode: **Cursor**, `delegation_mode: sequential`.

After writing this file, run:
`python3 scripts/check_forge_ladder.py --sprint-dir docs/sprints/039-core-pipeline`

---

## 1. Priority-1 search performed first

`rules/skills_and_integrations.md §1`: read `skills/manifest_skills.json`.
No existing skill implements `--boot` for `/start`, `refresh-baseline` after
deploy, bridge command-body freshness, or anchor higiene probes. Those are
framework scripts/workflows/docs under `implementer_agent` and
`doc_orchestrator`.
Priority 2 (`autoskills-3rd`) **not** escalated.
Priority 3 (`https://skills.sh/`) **not** queried — no unresolved tool gap.
No new skill forged (Priority 4).

---

## 2. Per-unit tool resolution

| Unit | File(s) | Resolution |
| :--- | :--- | :--- |
| L1 | `scripts/session_state.py` | Class (b) — framework script. No skill. |
| L2 | `workflows/deployment_workflow.md` | Class (c) — workflow prose. No skill. |
| L3 | `scripts/detect_drift.py` | Class (b) — framework script. No skill. |
| L4 | `tests/test_session_protocol.py` | Class (b) — pytest (+ P2 fixtures). No skill. |
| B1 | `scripts/session_start.py` | Class (b) — framework script. No skill. |
| B2 | `tests/test_session_start.py` | Class (b) — pytest. No skill. |
| B3 | `commands/start.md` | Class (c) — slash command. No skill. |
| B4 | `workflows/start_workflow.md` | Class (c) — workflow prose. No skill. |
| C1 | `scripts/cursor_adapter.py` | Class (b) — framework script. No skill. |
| C2 | `tests/test_cursor_adapter.py` | Class (b) — pytest. No skill. |
| R1 | `config/artifact_registry.json` | Class (c) — config. No skill. |
| R2 | `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` | Class (c) — generated via `map_workflows.py`. No skill. |
| P1 | `scripts/session_probe.py` | Class (b) — framework script. No skill. |
| D1 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | Class (c) — roadmap Status. No skill. |
| D2 | `docs/decisions/ADR-0002-drift-verdict-exit-codes.md` | Class (c) — ADR consequences. No skill. |

---

## 3. Skills used

| Skill | Why |
| :--- | :--- |
| `token-saver-auditor` (existing) | Phase 1/5 `audit_plan.py` on this plan |
| Built-in `make cursor-tiers` | Catalogue quote for `task_scope.md` Model/Effort |
| Built-in `scripts/map_workflows.py` | R2 regenerates WORKFLOWS_STEP_MAP_GUIDE |

## 4. Skills considered and rejected

| Candidate | Why rejected |
| :--- | :--- |
| New skill for `--boot` / baseline refresh | Deterministic script surface; Filter 5 → script, not skill |
| graphify / omni-minimizer | Not required for these file-scoped edits |

## 5. Forge trail

No skill was forged. P3 not escalated (no tool gap after Priority 1).
