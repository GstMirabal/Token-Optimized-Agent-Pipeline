# Skill Assignment — Sprint 035 (`core-pipeline`)

Phase 4.2 of `workflows/pipeline_workflow.md`. Implementation Plan at
`docs/sprints/035-core-pipeline/IMPLEMENTATION_PLAN.md`.

---

## 1. Priority-1 search performed first

`rules/skills_and_integrations.md §1`: read `skills/manifest_skills.json`.
No existing skill prints a `/start` briefing, resolves Cursor tier→model,
inverts `--check` for gate proposals, or adds `verify_references` check `(f)`.
Those are framework-root scripts (`implementer_agent`) or workflow/ADR prose
(`orchestrator` / `doc_orchestrator`). Priority 2 (`autoskills-3rd`) **not**
escalated. No new skill forged (Priority 4).

---

## 2. Per-unit tool resolution

| Unit(s) | File(s) | Resolution |
| :--- | :--- | :--- |
| E0, E1, H1 | trial guide + ADRs | Class (c) — documentation. No skill. |
| E2, E5, E6 | `scripts/audit_cursor_models.py` | Class (b) — script + pytest. No skill. |
| E3, C2 | `workflows/pipeline_workflow.md`, `start_workflow.md` | Class (c). Sequential touches. No skill. |
| E4, C4, H4 | tests | Class (b). No skill. |
| C1 | `scripts/session_start.py` | Class (b) — orchestrates existing probes. No skill. |
| C3 | `commands/start.md` | Class (c). No skill. |
| C5 | `Makefile` | Class (b)/(c) — make targets. No skill. |
| H2 | `config/model_tiers.json` | Class (c) — policy JSON. No skill. |
| H3 | `scripts/verify_references.py` | Class (b). No skill. |
| F3 | `agents/token_economy_agent.md` | Class (c) — profile prose. No skill. |

**Gates G1.q / G1.t (later):** `make verify` + pytest; no new skill.

---

## 3. Skills used

| Skill | Why |
| :--- | :--- |
| `token-saver-auditor` (existing) | Phase 1/5 `audit_plan.py` on this plan |
| Built-in `make cursor-tiers` | Catalogue quote for `task_scope.md` Model/Effort |

## 4. Skills considered and rejected

| Candidate | Why rejected |
| :--- | :--- |
| `autoskills-3rd` | No unresolved tool gap |
| New "session-briefing" skill | One script under `scripts/` with `RA-16` invoker (`start_workflow` + `make session-start`) |
| New "model-resolve" skill | Logic belongs in `audit_cursor_models.py` already in tree |
| `graphify` full rebuild | Not required for C/E/H/F units |

## 5. Gaps

None for 035. Track G (`model_ledger.py`) is 037; C5 only stubs the make target.
