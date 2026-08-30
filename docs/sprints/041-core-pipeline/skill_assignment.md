# Skill Assignment — Sprint 041 (bi-harness-bridge-parity)

Source: `docs/sprints/041-core-pipeline/IMPLEMENTATION_PLAN.md`.
Phase 4.2 of `workflows/pipeline_workflow.md`. Drafted from
`docs/standards/templates/SKILL_ASSIGNMENT_TEMPLATE.md`.

Mode: **claude-code**, `delegation_mode: native`.

After writing this file, run:
`python3 scripts/check_forge_ladder.py --sprint-dir docs/sprints/041-core-pipeline`
(exit `2` rejects an empty forge destination or submodule contamination).

---

## 1. Priority ladder (record every rung)

`rules/skills_and_integrations.md §1`. Query terms: `bridge`, `symlink`,
`install`, `harness`.

**The ladder terminates at the first rung.** No rung below it is exercised,
because nothing in this sprint requires a computational tool that does not
already exist.

| Rung | Source | Result | Evidence |
| :--- | :--- | :--- | :--- |
| P1 | `skills/manifest_skills.json` | **resolved here** — 2 of 34 skills match the query; neither performs bridge-integrity work, and none is required | `python3 -c "import json; d=json.load(open('skills/manifest_skills.json')); print([s['name'] for s in d['skills'] if any(t in json.dumps(s).lower() for t in ['bridge','symlink','install','harness'])])"` → `['autoskills', 'slash-commander']` |
| P2 | `autoskills-3rd` | not reached | P1 answered the question the ladder asks |
| P3 | `https://skills.sh/` | not reached | The ladder exists to avoid building a tool that already exists. This sprint builds none — see §5 |
| P4 | Three-File Standard | not reached | Nothing is built at this rung |

---

## 2. Per-unit tool resolution

Every unit edits an existing framework file with the standard library. The tools
are the ones the pipeline already mandates, not new ones.

| Unit | Skill / tool | Destination | P1–P4 trail |
| :--- | :--- | :--- | :--- |
| U1 `scripts/bridge_state.py` | none (stdlib `pathlib`, `hashlib`, `subprocess`) | N/A | P1 hit — no bridge-integrity skill exists and none is needed |
| U2 `scripts/session_start.py` | none | N/A | P1 hit |
| U3 `hooks/on_init.py` | none | N/A | P1 hit |
| U4 `scripts/cursor_adapter.py` | none | N/A | P1 hit |
| U5 `commands/start.md` | `slash-commander` (consulted, not invoked — see §4) | N/A | P1 hit |
| U6 `workflows/start_workflow.md` | none | N/A | P1 hit |
| U7 `workflows/deployment_workflow.md` | none | N/A | P1 hit |
| U8 `tests/test_bridge_state.py` | `pytest` (already a dependency) | N/A | P1 hit |
| U9 `tests/test_session_start.py` | `pytest` | N/A | P1 hit |
| U10 `IMPLEMENTATION_PLAN_TEMPLATE.md` | `token-saver-auditor` | N/A | P1 — `audit_plan.py` is the gate U10 repairs against |
| U11 `SKILL_ASSIGNMENT_TEMPLATE.md` | none (`check_forge_ladder.py` is the gate it repairs against) | N/A | P1 |
| U12 `workflows/pipeline_workflow.md` | none (`check_task_scope.py` is the gate it repairs against) | N/A | P1 |

---

## 3. Skills used

| Skill | Why |
| :--- | :--- |
| `token-saver-auditor` | `skills/token-saver-auditor/scripts/audit_plan.py` is the mandatory Phase 1 gate (`pipeline_workflow.md` Phase 1) and the instrument that U10's defect was found with. Run again at Phase 5 and after U10 lands |
| `graphify` | `graph_rebuild` at close (`close_workflow.md` Phase 5) — this sprint changes source files, so the AST graph must be resynced |

---

## 4. Skills considered and rejected

| Candidate | Why rejected |
| :--- | :--- |
| `slash-commander` | Consulted for U5 (`commands/start.md`). Rejected as an **invocation**: U5 is a one-token edit inside an existing command file, and the correctness constraint lives in `cursor_adapter._rewrite_command_body` (U4), not in slash-command authoring. Invoking a skill to change one flag value is the spend `rules/token_economy.md` prohibits |
| `autoskills` | Matched the P1 query on the word *install*. It discovers and registers third-party skills; this sprint installs a **harness bridge**, an unrelated sense of the word |
| `python-quality-auditor` | `ruff check .` and `make verify` already gate U1–U4 and U8–U9 (`agents.md §1 linter_command`). A second auditor over the same files duplicates a check the Quality Gate already runs |
| `mass-standardizer` | Audits the Three-File Skill Standard. No skill is created or modified, so it has nothing to audit here |

---

## 5. Gaps

**None that block this sprint.** Nothing is built at P4, and that is a deliberate
outcome rather than an unfilled rung: all twelve units are edits to existing
framework files using the standard library, and `rules/code_craft.md §7` treats
a new dependency — or a new skill — as permanent code you do not control.

One observation recorded for `/agents:extract` at Phase 8 rather than acted on
here: **no skill in the manifest covers harness-bridge integrity**, which is
what U1 becomes. If a second host-facing bridge target ever appears, `U1`'s
`scripts/bridge_state.py` is the natural seed for one. Forging it now would be
the speculative generality `rules/code_craft.md §1` prohibits — it would have
exactly one caller.
