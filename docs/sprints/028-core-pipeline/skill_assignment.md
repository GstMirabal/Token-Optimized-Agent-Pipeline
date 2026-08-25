# Skill Assignment — Sprint 028 (`self-improvement-unblock`)

Phase 4.2 of `workflows/pipeline_workflow.md`. Implementation Plan at
`docs/sprints/028-core-pipeline/IMPLEMENTATION_PLAN.md`.

---

## 1. Priority-1 search performed first

`rules/skills_and_integrations.md §1`: read `skills/manifest_skills.json`.
Priority 2 (`autoskills-3rd`) **not** escalated — no unit blocked after Priority 1.

---

## 2. Per-unit tool resolution

| Unit(s) | File(s) | Resolution |
| :--- | :--- | :--- |
| A1 | `agents/agent_orchestrator.md` | Class (c) — governance prose. Mirror `skill_forge_workflow forge_destination` pattern; no skill. |
| A2 | `workflows/pipeline_workflow.md` | Class (c). `slash-commander` at gate if command surface changes (none planned). |
| P1 | `scripts/install.py` | Class (b) — extend existing installer; sibling `install.sh` wrapper. No new skill. |
| P1.1 | tests | Class (b) — pytest / shell harness `tests/test_installer.sh`. |
| P2 | `agents.md` | Class (c) — governance amendment prose. |
| P2.1 | profile README | Class (c). |
| M1, M2 | workflows | Class (c). |
| D1 | new guide | Class (c) — Diátaxis how-to per `documentation_standard`. |
| D2–D3 | roadmap / CHANGELOG | Class (c). |

**Gates G1.q / G1.t:** `make verify` + pytest; no new skill.

---

## 3. Skills used

| Skill | Why |
| :--- | :--- |
| *(none forged)* | No computational gap |
| `omni-context-minimizer` (on demand) | If `scripts/install.py` edit requires skeleton (>200 lines) |
| Built-in `make verify` | RA-16, reference checks, pytest |

## 4. Skills considered and rejected

| Candidate | Why rejected |
| :--- | :--- |
| "agent-forge" skill | One-time doctrine + installer change; knowledge lives in workflow/agent prose |
| `autoskills-3rd` | No unresolved tool gap |

## 5. Gaps

None.
