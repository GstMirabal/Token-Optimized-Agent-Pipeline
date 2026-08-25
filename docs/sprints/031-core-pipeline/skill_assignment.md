# Skill Assignment — Sprint 031 (`gate-verdict-classes`)

Phase 4.2 of `workflows/pipeline_workflow.md`. Implementation Plan at
`docs/sprints/031-core-pipeline/IMPLEMENTATION_PLAN.md`.

---

## 1. Priority-1 search performed first

`rules/skills_and_integrations.md §1`: read `skills/manifest_skills.json`.
No existing skill implements gate-verdict vocabulary or `SPRINT_LOG` class
checks. `token-saver-auditor` audits Implementation Plans, not gate logs.
Priority 2 (`autoskills-3rd`) **not** escalated — no unit blocked after
Priority 1. No new skill forged (Priority 4): one `scripts/` checker with
`RA-16` invokers matches Sprint 030's `check_task_scope.py` pattern.

---

## 2. Per-unit tool resolution

| Unit(s) | File(s) | Resolution |
| :--- | :--- | :--- |
| T1 | `tests/test_check_gate_log.py` | Class (b) — pytest. No new skill. |
| R1 | `rules/qa_and_testing.md` | Class (c) — instructing rule. |
| R2, R3 | gate profiles | Class (c) — emit `APPROVED` \| `REJECTED` \| `RECORD`. |
| R4, R5, M3 | workflows | Class (c) — invokers + `RECORD` routing. |
| R6 | `agents/orchestrator.md` | Class (c) — `gate_transcription` columns. |
| R7 | `agents.md` | Class (c) — `RA-17` one-line index. |
| M1 | `scripts/check_gate_log.py` | Class (b) — new script, not a skill. |
| M2 | `Makefile` | Class (b) — `verify` invoker. |
| D1 | ADR-0008 | Class (c) — Nygard decision. |
| D2, D3 | trial guide / program queue | Class (c). |

**Gates G1.q / G1.t:** `make verify` + pytest; no new skill.

---

## 3. Skills used

| Skill | Why |
| :--- | :--- |
| `token-saver-auditor` (existing) | Phase 5 `audit_plan.py` on this plan |
| Built-in `make verify` | Will invoke `check_gate_log.py --current-sprint` after M2 |

## 4. Skills considered and rejected

| Candidate | Why rejected |
| :--- | :--- |
| New "gate-log-auditor" skill | One script under `scripts/` with RA-16 invokers is enough (030 precedent) |
| `autoskills-3rd` | No unresolved tool gap |
| Classify findings inside the script | Design D3: agent judgment (Filter 5); script checks vocabulary only |

## 5. Gaps

None.
