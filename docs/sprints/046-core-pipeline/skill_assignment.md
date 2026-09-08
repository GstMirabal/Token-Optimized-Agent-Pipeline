# Skill Assignment — Sprint 046 (nucleus-audit-mechanical-remediation)

Source: `docs/sprints/046-core-pipeline/IMPLEMENTATION_PLAN.md`.
Phase 4.2 of `workflows/pipeline_workflow.md`. Drafted from this template.

Mode: **claude-code**, `delegation_mode: native`.

After writing this file, run:
`python3 scripts/check_forge_ladder.py --sprint-dir docs/sprints/046-core-pipeline`
(exit `2` rejects an empty forge destination or submodule contamination).

---

## 1. Priority ladder (record every rung)

`rules/skills_and_integrations.md §1`:

| Rung | Source | Result | Evidence |
| :--- | :--- | :--- | :--- |
| P1 | `skills/manifest_skills.json` | HIT — existing deterministic tools cover every verification need; no new capability required | `Edit`/`Read`/`grep` for the text edits; `make verify`, `scripts/verify_references.py`, `scripts/map_workflows.py`, `scripts/check_template_gates.py`, `scripts/check_gate_log.py`, `skills/token-saver-auditor/scripts/audit_plan.py` for verification |
| P2 | `autoskills-3rd` | not reached | P1 satisfied the need |
| P3 | `https://skills.sh/` | not reached | P1 satisfied the need |
| P4 | Three-File Standard at Destination | not reached | no skill is forged this sprint |

This sprint **builds no new skill**. Every unit is a drafted-text edit to an
existing file, verified by tools already present in the tree. No machine-readable
`skills.sh` trail is required because no build is claimed.

---

## 2. Per-unit tool resolution

| Unit | Skill / tool | Destination | P1–P4 trail |
| :--- | :--- | :--- | :--- |
| U01–U07 | `Edit`, `Read`, `grep`; `grep -cE '^\| RA-' agents.md` to confirm no renumber | N/A | P1 HIT |
| U08, U10, U13 | `Edit`, `Read`, `grep` | N/A | P1 HIT |
| U09, U14, U15, U16 | `Edit`, `Read`, `grep`; `scripts/map_workflows.py` to regenerate the step map if a step table changed | N/A | P1 HIT |
| U11, U12 | `Edit`, `Read`; `rules/documentation_standard.md §4.1` metadata block reference | N/A | P1 HIT |
| U17, U19 | `Edit`, `Read`; `python3 -m py_compile` on the touched file | N/A | P1 HIT |
| U18, U20, U21, U22 | `Edit`, `Read`; `python3 -m py_compile` on the touched file | N/A | P1 HIT |
| U23 | `Edit`, `Read`; `python3 -m json.tool config/invocation_exceptions.json`; `scripts/verify_references.py` check (d) | N/A | P1 HIT |
| U24 | `Edit`, `Read`; `scripts/check_template_gates.py`, `scripts/check_gate_log.py` | N/A | P1 HIT |
| U25–U28 | `Edit`, `Read` | N/A | P1 HIT |

---

## 3. Skills used

| Skill | Why |
| :--- | :--- |
| `token-saver-auditor` (`audit_plan.py`) | Phase 1 / Phase 5 gate on `IMPLEMENTATION_PLAN.md` — already run at Phase 1 (exit 0). |
| `slash-commander` (`verify_commands.py`) | Invoked transitively by `make verify`; confirms `commands/` ↔ `workflows/` links survive the `workflows/` edits (U09, U14, U15, U16). |
| `topology-monitor` (`legacy_app_auditor.py`) | Invoked transitively by `make verify` (`skill_standard_check`); no skill topology changes this sprint but the gate still runs. |

## 4. Skills considered and rejected

| Candidate | Why rejected |
| :--- | :--- |
| `omni-context-minimizer` (`omni_minimizer.py`) | For AST skeletons of files >200 lines. `agents.md` (~180 lines of table) and every other target are read with targeted `grep`/offset reads; no full-file structural discovery needed. |
| A new "audit-row applicator" skill | Rejected as over-engineering: 18 one-file text edits with drafted amendment text do not warrant a forged tool. `rules/skills_and_integrations.md §1` — build only when the ladder finds no existing capability. |

## 5. Gaps

None. Every unit resolves to `Edit`/`Read`/`grep` plus an existing verification
tool. No capability is missing; no skill is forged.
