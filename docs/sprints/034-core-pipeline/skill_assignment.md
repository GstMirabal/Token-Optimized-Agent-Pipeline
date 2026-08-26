# Skill Assignment — Sprint 034 (`core-pipeline`)

Phase 4.2 of `workflows/pipeline_workflow.md`. Implementation Plan at
`docs/sprints/034-core-pipeline/IMPLEMENTATION_PLAN.md`.

**Backfill.** Written 2026-08-26 after Phase 6 had started. Priority-1 search
was performed at write time, not before the early units.

---

## 1. Priority-1 search performed first

`rules/skills_and_integrations.md §1`: read `skills/manifest_skills.json`.
No existing skill chains close to deploy, stamps `built_at_commit` on
`graphify-out/graph.json`, auto-pins a submodule, or emits Cursor
`.cursor/agents/` files. Those are framework-root scripts (`implementer_agent`)
or workflow prose (`orchestrator` / `doc_orchestrator`).
Priority 2 (`autoskills-3rd`) **not** escalated. No new skill forged
(Priority 4).

---

## 2. Per-unit tool resolution

| Unit(s) | File(s) | Resolution |
| :--- | :--- | :--- |
| A1, A2 | `commands/close.md`, `workflows/close_workflow.md` | Class (c) — protocol prose. No skill. |
| B1, B2 | `scripts/session_probe.py`, `tests/test_session_probe.py` | Class (b) — pytest pin of ancestry vs mtime. `graphify` skill not invoked; the probe only *reads* `graph.json`. |
| P1, P2, P3 | `scripts/sync_agents_pin.py`, tests, `workflows/start_workflow.md` | Class (b)/(c). No skill. |
| I1, I7 | plan / agent-assignment templates | Class (c). No skill. |
| I2, K6 | `workflows/pipeline_workflow.md` | Class (c). Sequential touches. No skill. |
| I3 | `agents/agent_orchestrator.md` | Class (c) — profile prose. No skill. |
| I4, I5, K3, K5 | `scripts/check_task_scope.py` + tests | Class (b). No skill. |
| I6 | `docs/hotfixes/H-005-pipeline.md` | Class (c). No skill. |
| K1, K4 | `scripts/check_role_artifact.py` + tests | Class (b). No skill. |
| K2 | `config/artifact_registry.json` | Class (c). No skill. |
| J1 | `AGENTS.md` | Class (c) — constitution clause. No skill. |
| N1–N5 | adapter / gitignore / installer + tests | Class (b). No skill. |
| N6 | `docs/guides/AGENTS_SLASH_COMMANDS_GUIDE.md` | Class (c). No skill. |

**Gates G1.q / G1.t:** `make verify` + pytest; no new skill.

---

## 3. Skills used

| Skill | Why |
| :--- | :--- |
| `token-saver-auditor` (existing) | Phase 5 `audit_plan.py` on this plan |
| Built-in `make cursor-tiers` | Catalogue quote for `task_scope.md` Model/Effort |
| Built-in `make verify` | Regression after B1+B2 |

## 4. Skills considered and rejected

| Candidate | Why rejected |
| :--- | :--- |
| `graphify` (full rebuild) | Advisory for B; freshness is `session_probe.py`, not a skill invocation |
| `autoskills-3rd` | No unresolved tool gap |
| New "submodule-pin" skill | Pin logic is one script under `scripts/` (`RA-16` invoker: start workflow) |
| New "cursor-agents" skill | Emission belongs to `cursor_adapter.py` already in tree |

## 5. Gaps

None for 034. Track M (036) may still forge if the host-submodule ladder needs a
skill; that is out of this file.
