# Skill Assignment — Sprint 029 (`documentation-truth`)

Phase 4.2 of `workflows/pipeline_workflow.md`. Implementation Plan at
`docs/sprints/029-core-pipeline/IMPLEMENTATION_PLAN.md`.

---

## 1. Priority-1 search performed first

`rules/skills_and_integrations.md §1`: read `skills/manifest_skills.json`.
Priority 2 (`autoskills-3rd`) **not** escalated — no unit blocked after Priority 1.

---

## 2. Per-unit tool resolution

| Unit(s) | File(s) | Resolution |
| :--- | :--- | :--- |
| R0 | upstream findings | Class (c) — governance register prose. |
| R1, C1 | `CHANGELOG.md` | Class (c). |
| R2 | program queue | Class (c). |
| T1.0, J6.0 | tests | Class (b) — pytest. No new skill. |
| T1.1 | `check_readme_counts.py` | Class (b) — extend existing counter. |
| T1.2 | `README.md` | Class (c). |
| T1.3 | `close_workflow.md` | Class (c). |
| G1 | `artifact_registry.json` | Class (b) — existing registry schema. |
| G2 | slash-commands guide | Class (c) — Diátaxis how-to. |
| G3 | `verify_commands.py` | Class (b) — extend `slash-commander` script already invoked by `make verify`. |
| A3–A7 | ADRs | Class (c) — `ADR_TEMPLATE.md`. |
| P1 | Implementation Plan template | Class (c). |
| P2 | `documentation_standard.md` | Class (c). |
| J6.1 | `verify_references.py` | Class (b) — extend existing check (d). |

**Gates G1.q / G1.t:** `make verify` + pytest; no new skill.

---

## 3. Skills used

| Skill | Why |
| :--- | :--- |
| *(none forged)* | No computational gap |
| `slash-commander` (existing) | G3 extends `verify_commands.py`; already `invoked_by` `make verify` |
| `omni-context-minimizer` (on demand) | If `verify_references.py` edit needs skeleton (>200 lines) |
| Built-in `make verify` | RA-16, README counts, pytest |

## 4. Skills considered and rejected

| Candidate | Why rejected |
| :--- | :--- |
| New "readme-count-writer" skill | One script already owns the counts; a skill would be a second invoker |
| `render_readme.py` at close | Rejected in Design D2 — would overwrite the hand-written nucleus README |
| `autoskills-3rd` | No unresolved tool gap |
| `token-saver-auditor` body | Sprint 030, out of scope |

## 5. Gaps

None.
