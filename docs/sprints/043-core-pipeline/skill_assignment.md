# Skill Assignment — Sprint 043 (submodule-runtime-parity)

Source: `docs/sprints/043-core-pipeline/IMPLEMENTATION_PLAN.md`.
Phase 4.2 of `workflows/pipeline_workflow.md`.

Mode: **claude-code**, `delegation_mode: native`.

Check: `python3 scripts/check_forge_ladder.py --sprint-dir docs/sprints/043-core-pipeline`

---

## 1. Priority ladder (record every rung)

`rules/skills_and_integrations.md §1`. This sprint builds **no skill** — every
unit is prose editing, a rule edit, one framework-root script, or its test, all
within existing agent capability. The ladder terminates at P1.

| Rung | Source | Result | Evidence |
| :--- | :--- | :--- | :--- |
| P1 | `skills/manifest_skills.json` | terminated here — no computational tool needed | D1 (`check_venv_relocatable.py`) is a framework-root gate script owned by `implementer_agent` per `ADR-0009`, not a skill; it parses `pyvenv.cfg` + one shebang with `pathlib`/text ops |
| P2 | `autoskills-3rd` | not reached | — |
| P3 | `https://skills.sh/` | not reached | — |
| P4 | Three-File Standard at Destination | not reached | — |

---

## 2. Per-unit tool resolution

| Unit | Skill / tool | Destination | P1–P4 trail |
| :--- | :--- | :--- | :--- |
| A1 | Edit (workflow prose) | N/A | P1 terminal |
| A2 | Edit (rule prose) | N/A | P1 terminal |
| D1 | Write + Bash (Python stdlib: `pathlib`, text parsing; imports `scripts/_root.py`) | N/A | P1 terminal |
| D2 | Write + Bash (`pytest`, already vendored) | N/A | P1 terminal |
| C1 | Edit (constitutional prose) | N/A | P1 terminal |
| C2 | Edit (guide prose) | N/A | P1 terminal |

---

## 3. Skills used

| Skill | Why |
| :--- | :--- |
| `token-saver-auditor` (`audit_plan.py`) | Phase 1 gate on `IMPLEMENTATION_PLAN.md` — already run, exit 0 |
| `graphify` | Phase 8 `graph_rebuild` (this sprint changes `scripts/`, `tests/`, `agents.md`) |

## 4. Skills considered and rejected

| Candidate | Why rejected |
| :--- | :--- |
| `omni-context-minimizer` | No file >200 lines is edited as a whole; targeted reads suffice |
| `skillopt` | Sprint touches no skill prompt optimization |

## 5. Gaps

None.
