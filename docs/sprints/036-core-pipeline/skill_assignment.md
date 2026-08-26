# Skill Assignment — Sprint 036 (`core-pipeline`)

Phase 4.2 of `workflows/pipeline_workflow.md`. Implementation Plan at
`docs/sprints/036-core-pipeline/IMPLEMENTATION_PLAN.md`.

---

## 1. Priority-1 search performed first

`rules/skills_and_integrations.md §1`: read `skills/manifest_skills.json`.
No existing skill audits Cursor-era sprint folders (CE-1–CE-5), checks a host
forge ladder against Phase 4.1/4.2 artifacts, or pinneas a 14-profile tools
census. Those are framework-root scripts (`implementer_agent`) or profile /
workflow / template prose (`agent_orchestrator` / `orchestrator` /
`doc_orchestrator`). Priority 2 (`autoskills-3rd`) **not** escalated.
Priority 3 (`https://skills.sh/`) **not** queried — no unresolved tool gap.
No new skill forged (Priority 4).

---

## 2. Per-unit tool resolution

| Unit(s) | File(s) | Resolution |
| :--- | :--- | :--- |
| L1 | `scripts/audit_cursor_era.py` | Class (b) — script wrapping existing parsers. No skill. |
| L2, M2, M6 | tests | Class (b) — pytest. No skill. |
| L3 | `Makefile` | Class (b)/(c) — make target. No skill. |
| M1 | `scripts/check_forge_ladder.py` | Class (b) — deterministic gate; P3 simulated. No skill. |
| M3, M7, M8, M9 | `agents/*.md` profiles | Class (c) — instructing prose. No skill. |
| M4 | `SKILL_ASSIGNMENT_TEMPLATE.md` | Class (c) — template. No skill. |
| M5 | `workflows/pipeline_workflow.md` | Class (c) — names M1 invoker. No skill. |

**Gates G1.q / G1.t (later):** `make verify` + targeted pytest; no new skill.

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
| New "cursor-era-audit" skill | One script under `scripts/` with `RA-16` invoker (`make cursor-era-audit`) |
| New "forge-ladder" skill | Logic belongs in `check_forge_ladder.py`; Phase 4.1/4.2 invoke it |
| HTTP client for `skills.sh` | P3 simulated in tests; real HTTP behind a flag, never in `verify` |
| `graphify` full rebuild | Not required for M/L units |

## 5. Gaps

None for 036. Track G (`model_ledger.py`) is 037. Rider **S** (sandbox
`xargs` / nucleus `.bridge_cursor.lock`) queued on 037 in
`021-030-program-queue.md`. Triage of census `new` rows (O5) is at close, not
a skill forge.
