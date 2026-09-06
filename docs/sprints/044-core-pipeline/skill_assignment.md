# Skill Assignment — Sprint 044 (session-start-drift-cigate-host-parity)

Source: `docs/sprints/044-core-pipeline/IMPLEMENTATION_PLAN.md`.
Phase 4.2 of `workflows/pipeline_workflow.md`. Drafted from
`docs/standards/templates/SKILL_ASSIGNMENT_TEMPLATE.md`.

Mode: **claude-code**, `delegation_mode: native`.

After writing this file, run:
`python3 scripts/check_forge_ladder.py --sprint-dir docs/sprints/044-core-pipeline`
(exit `2` rejects an empty forge destination or submodule contamination).

---

## 1. Priority ladder (record every rung)

`rules/skills_and_integrations.md §1`:

| Rung | Source | Result | Evidence |
| :--- | :--- | :--- | :--- |
| P1 | `skills/manifest_skills.json` | Not needed | Every unit edits an existing framework script, its test, the `Makefile`, or an ADR. No computational capability is missing that a skill would supply. |
| P2 | `autoskills-3rd` | Not reached | Ladder terminates at P1 — no capability gap to fill. |
| P3 | `https://skills.sh/` | Not reached | Ladder terminates at P1. No skill is forged this sprint. |
| P4 | Three-File Standard at Destination | Not reached | Ladder terminates at P1. |

This sprint builds no skill. The ladder terminates at the first rung.

---

## 2. Per-unit tool resolution

| Unit | Skill / tool | Destination | P1–P4 trail |
| :--- | :--- | :--- | :--- |
| U1 | Edit — `_bridge_permission_denied` predicate widening | N/A | Ladder → P1 (no skill) |
| U2 | Edit — pytest cases (`unittest.mock` stubs) | N/A | Ladder → P1 |
| U3 | Edit — `_run_script` cwd resolution via `scripts/_root.py` / `scripts/_mode.py` | N/A | Ladder → P1 |
| U4 | Edit — pytest submodule-mode boot fixture | N/A | Ladder → P1 |
| U5 | Edit — `ci_gate.py` 403/404 classification | N/A | Ladder → P1 |
| U6 | Edit — pytest GitHub-client stubs (existing pattern in `test_ci_gate.py`) | N/A | Ladder → P1 |
| U7 | Edit — `detect_drift.py` range filter (`git log`/`git show` already used) | N/A | Ladder → P1 |
| U8 | Create — pytest fixture repo (existing pattern: `git init` in `tmp_path`) | N/A | Ladder → P1 |
| U9 | Edit — `Makefile` recipe line | N/A | Ladder → P1 |
| U10 | Edit — `check_venv_relocatable.py` disjunct removal | N/A | Ladder → P1 |
| U11 | Edit — pytest case | N/A | Ladder → P1 |
| U12 | Write — ADR from `docs/standards/templates/ADR_TEMPLATE.md` | N/A | Ladder → P1 |

---

## 3. Skills used

| Skill | Why |
| :--- | :--- |
| None | No unit needs a computational capability beyond `Read`/`Edit`/`Write`/`Bash` on existing files. |

## 4. Skills considered and rejected

| Candidate | Why rejected |
| :--- | :--- |
| `graphify` | The sprint touches `Makefile graphify-rebuild` config, not the graph itself. No query or rebuild is part of any unit (the Phase 8 `graph_rebuild` is `close_workflow.md`'s, not this sprint's). |
| `omni_minimizer` (skeleton extraction) | Used during Phase 1 investigation only. All target files were read with targeted offset/limit reads; no unit requires a skeleton pass. |

## 5. Gaps

None. Every unit is an edit to an existing tracked file (or a new sibling test /
ADR following an existing pattern) with tools every assignee already holds.
