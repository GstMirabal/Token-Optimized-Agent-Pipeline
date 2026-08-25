# Skill Assignment — Sprint 027 (`autonomy-posture`)

Phase 4.2 of `workflows/pipeline_workflow.md`. Implementation Plan committed at
`d874d7a` (`docs/sprints/027-core-pipeline/IMPLEMENTATION_PLAN.md`).

A tool that was considered and rejected is a decision; a tool that was never
seen is a gap. Both halves are recorded below.

---

## 1. Priority-1 search performed first

`rules/skills_and_integrations.md §1`: Priority 1 is `skills/manifest_skills.json`
(read for this sprint). Priority 2 (`skills/autoskills-3rd/`) was **not**
escalated — every unit resolved without a provisioning gap.

---

## 2. Per-unit tool resolution

| Unit(s) | File(s) | Resolution |
| :--- | :--- | :--- |
| A1, A1.1, A1.2 | `agents/*.md` | Class (c) — governance prose. No skill. |
| A3 | `hooks/on_init.py` | Class (b) — `devops_agent` / `F-086-A1`. Pattern: adopt `scripts/_root.agents_root` like other mixed/host scripts. No skill authors hooks. |
| A3.1, P1.1, P2.1, P3.1 | `tests/test_*.py` | Class (b) under tests/ deviation. Existing pytest suite is the runner; no skill generates the tests. |
| P1, P2, P3 | new `scripts/*.py` | Class (b). Sibling patterns: `session_state.py`, `session_probe.py`. `omni-context-minimizer` only if a touched existing file exceeds 200 lines. |
| P2.2 | verify wiring | Class (b). Likely small Makefile or docstring/`invoked_by` + close/verify mention. `slash-commander` / `verify_references` already gate `RA-16` at `make verify`. |
| C1 | `claude/settings.hooks.json` | Class (c) structured JSON. Merge semantics owned by `scripts/install.py` / `merge_json.py` — use those as reference, not a skill. |
| C2 | `docs/guides/AUTONOMY_POSTURE_GUIDE.md` | Class (c). Diátaxis how-to; `documentation_standard` ruleset. |
| C3 | workflow cell | Class (c). `slash-commander` audits commands↔workflows at gate if a command file changes (none planned). |
| D1–D3 | audit / roadmap / CHANGELOG | Class (c). |

**Gates G1.q / G1.t:** `python-quality-auditor` (if present in manifest) + `make verify` instruments; no new skill.

---

## 3. Skills used

| Skill | Why |
| :--- | :--- |
| *(none forged)* | No unit requires a new skill |
| `omni-context-minimizer` (on demand) | Only if editing a file >200 lines (`agents.md §2 ast_skeleton`) |
| Built-in `make verify` stack | `slash-commander`, reference checks, pytest — gate done-criterion |

## 4. Skills considered and rejected

| Candidate | Why rejected |
| :--- | :--- |
| Forging an "autonomy" skill | One-shot template + three scripts; a skill would be padding (`agents.md §3 three_file_standard` — knowledge-only would need justification; executable skill is overkill) |
| `autoskills-3rd` provisioning | No unresolved computational gap after Priority 1 |

## 5. Gaps

None. No unit is blocked on a missing skill.
