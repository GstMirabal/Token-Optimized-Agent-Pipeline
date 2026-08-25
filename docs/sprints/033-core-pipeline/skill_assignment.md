# Skill Assignment — Sprint 033 (`implementer-role`)

Phase 4.2 of `workflows/pipeline_workflow.md`. Implementation Plan at
`docs/sprints/033-core-pipeline/IMPLEMENTATION_PLAN.md`.

---

## 1. Priority-1 search performed first

`rules/skills_and_integrations.md §1`: read `skills/manifest_skills.json`.
No existing skill forges agent profiles or closes role-map findings.
`agent_orchestrator` authors profiles under Phase 4.1 / forge destination —
not a skill. Priority 2 (`autoskills-3rd`) **not** escalated. No new skill
forged (Priority 4).

---

## 2. Per-unit tool resolution

| Unit(s) | File(s) | Resolution |
| :--- | :--- | :--- |
| A0 | `docs/decisions/ADR-0009-implementer-role.md` | Class (c) — ADR from template. No skill. |
| A1–A4 | `agents/implementer_agent.md`, `agents/devops_agent.md`, `agents.md`, `agents/agent_orchestrator.md` | Class (c) — governance / profile prose. No skill. |
| T1 | `tests/test_implementer_role.py` | Class (b) — pytest pin. No new skill. |
| R1, F1, Q1 | README / upstream findings / program queue | Class (c). |

**Gates G1.q / G1.t:** `make verify` + pytest; no new skill.

---

## 3. Skills used

| Skill | Why |
| :--- | :--- |
| `token-saver-auditor` (existing) | Phase 5 `audit_plan.py` on this plan |
| Built-in `make cursor-tiers` | Catalogue quote for `task_scope.md` Model/Effort |
| Built-in `make verify` | Regression after A1–T1 / R1 |

## 4. Skills considered and rejected

| Candidate | Why rejected |
| :--- | :--- |
| New "agent-forge" skill | Profile authoring is `agent_orchestrator` jurisdiction |
| `autoskills-3rd` | No unresolved tool gap |
| graphify (full rebuild) | Advisory only; not required to staff or pin the role |

## 5. Gaps

None.
