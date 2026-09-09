# Skill Assignment — Sprint 047 (nucleus-audit-design-remediation)

Source: `docs/sprints/047-core-pipeline/IMPLEMENTATION_PLAN.md`.
Phase 4.2 of `workflows/pipeline_workflow.md`. Drafted from
`docs/standards/templates/SKILL_ASSIGNMENT_TEMPLATE.md`.

Mode: **claude-code** (nucleus), `delegation_mode: native`.

After writing this file, run:
`python3 scripts/check_forge_ladder.py --sprint-dir docs/sprints/047-core-pipeline`
(exit `2` rejects an empty forge destination or submodule contamination).

---

## 1. Priority ladder (record every rung)

`rules/skills_and_integrations.md §1`:

| Rung | Source | Result | Evidence |
| :--- | :--- | :--- | :--- |
| P1 | `skills/manifest_skills.json` | HIT — existing deterministic tools cover every unit; no new capability required | `Read`/`Edit` for the prose and script edits; `omni-context-minimizer` (`omni_minimizer.py`) for the three script targets over 200 lines; `ruff`, `pytest`, `python3 -m py_compile`, `make verify`, `scripts/verify_references.py`, `scripts/map_workflows.py`, `scripts/check_gate_log.py`, `scripts/scan_workflow_determinism.py`, `scripts/check_template_gates.py`, `skills/token-saver-auditor/scripts/audit_plan.py` for verification |
| P2 | `autoskills-3rd` | not reached | P1 resolved every unit |
| P3 | `https://skills.sh/` (WebSearch/WebFetch) | reached — no applicable published skill | WebSearch on `pytest` test authoring, reference-anchor resolution, workflow step-map generation, gate-log parsing, and git worktree/submodule detection returned only generic `pytest`-pattern house-convention skills (fixtures/parametrize/conftest). None author the nucleus's stdlib suites against internal `scripts/`, and the four framework-internal concerns are the sprint's own edit targets (`scripts/verify_references.py`, `scripts/map_workflows.py`, `scripts/check_gate_log.py`, `scripts/_mode.py`), not tools to import. |
| P4 | Three-File Standard at Destination | not reached | ladder closed at P1; no skill is built this sprint |

This sprint **builds no new skill**. Every unit is a one-file edit — governance
prose (U1–U10), a stdlib-only `scripts/` change (U11–U17), or a `pytest` file
(U18–U23) — verified by tools already present in the tree. No `skills.sh`
negative-result trail is recorded because no build is claimed; per the template's
own guidance the outcome is described, never pasted as a literal trail.

---

## 2. Per-unit tool resolution

| Unit | Skill / tool | Destination | P1–P4 trail |
| :--- | :--- | :--- | :--- |
| U1 (`agents.md`, 176 lines) | `Read` with `offset`/`limit` on `§1`, `RA-01`, `RA-02`, `RA-14`; `grep -nE '^\| ' agents.md` to locate rows; `Edit`. Verify: `make verify`, `scripts/verify_references.py`, `grep -c 'python-doctor\|react-doctor' agents.md` == `0`, `grep -n 'RA-04\|RA-10' agents.md` (no renumber) | N/A | P1 HIT; P3 checked, no applicable skill |
| U2 (`rules/django_backend_standard.md`, 62) | `Read`/`Edit`. Verify: `scripts/verify_references.py`, `make verify` | N/A | P1 HIT |
| U3 (`rules/LEGACY_RULE_CONCORDANCE.md`, 27) | `Read`/`Edit`. Verify: `scripts/verify_references.py` (unmapped `Clause`/`Rule NN` → fail), `make verify` | N/A | P1 HIT |
| U4 (`workflows/audit_workflow.md`, 25) | `Read`/`Edit`. Verify: `scripts/verify_references.py`, `scripts/scan_workflow_determinism.py`, `scripts/check_template_gates.py`, `make verify` | N/A | P1 HIT |
| U5 (`rules/skills_and_integrations.md`, 18) | `Read`/`Edit`. Verify: `scripts/verify_references.py`, `make verify` | N/A | P1 HIT |
| U6 (`workflows/close_workflow.md`, 38) | `Read`/`Edit`. Verify: `scripts/verify_references.py`, `scripts/scan_workflow_determinism.py`, `make verify` | N/A | P1 HIT |
| U7 (`workflows/skill_forge_workflow.md`, 25) | `Read`/`Edit`. Verify: `scripts/verify_references.py`, `make verify` | N/A | P1 HIT |
| U8 (`workflows/reverse_documentation_workflow.md`, 145) | `Read` with `offset`/`limit` on phases 2–10 and 9.5; `Edit`. Verify: `scripts/map_workflows.py --check` (parenthetical step ids, frozen numbering), `scripts/verify_references.py` (`#findings-handoff` anchor), `make verify` | N/A | P1 HIT |
| U9 (`workflows/repository_hardening_workflow.md`, 154) | `Read` with `offset`/`limit` on the Execution-Flow list; `Edit`. Verify: `scripts/map_workflows.py --check`, `scripts/scan_workflow_determinism.py`, `make verify` | N/A | P1 HIT |
| U10 (`workflows/standardization_workflow.md`, 59) | `Read`/`Edit`. Verify: `scripts/map_workflows.py --check` (Legacy Routing Table skip-marker excluded), `scripts/verify_references.py`, `make verify` | N/A | P1 HIT |
| U11 (`scripts/verify_references.py`, 409 — over 200) | `skills/omni-context-minimizer/scripts/omni_minimizer.py` for the skeleton (`agents.md §2 ast_skeleton`), then targeted `Read` of check (d); `Edit`. Verify: `ruff check scripts/verify_references.py`, `venv_skillopt/bin/python -m pytest tests/test_verify_references.py -q`, `make verify` | N/A | P1 HIT; P3 checked, no applicable skill |
| U12 (`scripts/map_workflows.py`, 193) | `Read`/`Edit`; regenerate and stage `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` via `python3 scripts/map_workflows.py`. Verify: `python3 scripts/map_workflows.py --check` (exit `0`, guide not stale), `ruff check scripts/map_workflows.py`, `venv_skillopt/bin/python -m pytest tests/test_map_workflows.py -q` | N/A | P1 HIT |
| U13 (`scripts/check_gate_log.py`, 146) | `Read`/`Edit`. Verify: `ruff check scripts/check_gate_log.py`, `venv_skillopt/bin/python -m pytest tests/test_check_gate_log.py -q`, `python3 scripts/check_gate_log.py` self-run, `make verify` | N/A | P1 HIT |
| U14 (`scripts/session_start.py`, 481 — over 200) | `skills/omni-context-minimizer/scripts/omni_minimizer.py` for the skeleton (`agents.md §2 ast_skeleton`), then targeted `Read` of `load_anchor`; `Edit`. Verify: `ruff check scripts/session_start.py`, `venv_skillopt/bin/python -m pytest tests/test_session_start.py -q` | N/A | P1 HIT; P3 checked, no applicable skill |
| U15 (`scripts/detect_drift.py`, 359 — over 200) | `skills/omni-context-minimizer/scripts/omni_minimizer.py` for the skeleton (`agents.md §2 ast_skeleton`), then targeted `Read` of `main()`; `Edit`. Verify: `ruff check scripts/detect_drift.py`, `venv_skillopt/bin/python -m pytest tests/ -q -k drift` | N/A | P1 HIT; P3 checked, no applicable skill |
| U16 (`scripts/_mode.py`, 46) | `Read`/`Edit`. Verify: `ruff check scripts/_mode.py`, `venv_skillopt/bin/python -m pytest tests/test_mode.py -q` | N/A | P1 HIT |
| U17 (`scripts/submodule_purity.py`, 144) | `Read`/`Edit`. Verify: `ruff check scripts/submodule_purity.py`, `venv_skillopt/bin/python -m pytest tests/test_submodule_purity.py -q`, `python3 scripts/submodule_purity.py` self-run, `make verify` | N/A | P1 HIT |
| U18 (`tests/test_verify_references.py`) | `Read`/`Edit`/`Write`; `tmp_path` fixtures. Verify: `venv_skillopt/bin/python -m pytest tests/test_verify_references.py -q`, `ruff check tests/` | N/A | P1 HIT; `django-tdd-3rd` rejected (§4) |
| U19 (`tests/test_map_workflows.py`) | `Read`/`Edit`/`Write`; `tmp_path` fixtures. Verify: `venv_skillopt/bin/python -m pytest tests/test_map_workflows.py -q`, `ruff check tests/` | N/A | P1 HIT; `django-tdd-3rd` rejected (§4) |
| U20 (`tests/test_check_gate_log.py`) | `Read`/`Edit`/`Write`; `tmp_path` fixtures. Verify: `venv_skillopt/bin/python -m pytest tests/test_check_gate_log.py -q`, `ruff check tests/` | N/A | P1 HIT; `django-tdd-3rd` rejected (§4) |
| U21 (`tests/test_mode.py`) | `Read`/`Edit`/`Write`; `monkeypatch` + `tmp_path` for a simulated worktree/submodule `.git` file. Verify: `venv_skillopt/bin/python -m pytest tests/test_mode.py -q`, `ruff check tests/` | N/A | P1 HIT; `django-tdd-3rd` rejected (§4) |
| U22 (`tests/test_session_start.py`) | `Read`/`Edit`/`Write`; `monkeypatch` + `tmp_path` for a simulated submodule layout. Verify: `venv_skillopt/bin/python -m pytest tests/test_session_start.py -q`, `ruff check tests/` | N/A | P1 HIT; `django-tdd-3rd` rejected (§4) |
| U23 (`tests/test_submodule_purity.py`) | `Read`/`Edit`/`Write`; `tmp_path` for a gitignored stray anchor. Verify: `venv_skillopt/bin/python -m pytest tests/test_submodule_purity.py -q`, `ruff check tests/` | N/A | P1 HIT; `django-tdd-3rd` rejected (§4) |

Full-suite regression after Wave 3: `venv_skillopt/bin/python -m pytest tests/ -q`
(expected exit `0`, `IMPLEMENTATION_PLAN.md` Verification table).

`Destination` is `N/A` on every row: no skill is built, so there is no forge
destination to validate. Writing under `.agents/skills/` from any session is
prohibited (`agents.md §3 strict_rule`); it is not attempted here.

---

## 3. Skills used

| Skill | Why |
| :--- | :--- |
| `token-saver-auditor` (`audit_plan.py`) | Phase 1 / Phase 5 gate on `IMPLEMENTATION_PLAN.md` — already run at Phase 1 (`IMPLEMENTATION_PLAN.md` Verification table, exit `0`). |
| `omni-context-minimizer` (`omni_minimizer.py`) | `agents.md §2 ast_skeleton`: skeleton extraction before any partial read of the three script targets over 200 lines — `scripts/verify_references.py` (409, U11), `scripts/session_start.py` (481, U14), `scripts/detect_drift.py` (359, U15). |
| `slash-commander` (`verify_commands.py`) | Invoked transitively by `make verify`; confirms `commands/` ↔ `workflows/` links survive the `workflows/*.md` edits (U4, U6, U7, U8, U9, U10). |
| `topology-monitor` (`legacy_app_auditor.py`) | Invoked transitively by `make verify` (`skill_standard_check`); no skill topology changes this sprint but the gate still runs. |
| `graphify` | Phase 8 `venv_skillopt/bin/python -m graphify update . --force` post-change (`agents.md §2 graph_sync`; `IMPLEMENTATION_PLAN.md` Verification table). |

## 4. Skills considered and rejected

| Candidate | Why rejected |
| :--- | :--- |
| `omni-context-minimizer` for U1 (`agents.md`) | `agents.md` is 176 lines — below the >200-line `ast_skeleton` threshold (`agents.md §2`). Targeted `grep -nE '^\| '` plus `offset`/`limit` `Read` on the four affected `§` blocks suffice; the skeleton tool is still used for U11/U14/U15, which are over 200 lines. |
| `django-tdd-3rd` (pytest authoring, U18–U23) | Django/`pytest-django` specific — `factory_boy`, migrations, DRF client, coverage gates. The nucleus suites are plain stdlib `pytest` with `tmp_path`/`monkeypatch` against framework `scripts/`. No Django in the nucleus. |
| `sprint-architect` | The Work Breakdown (U1–U23) was produced at Phase 1 and is fixed in `IMPLEMENTATION_PLAN.md`. Phase 4.2 does not re-derive it. |
| `skill-creator` / `skill-forge_workflow` | No new skill is built: every unit maps to `Read`/`Edit` (or `Write` for a test file) plus an existing deterministic gate. `rules/skills_and_integrations.md §1` — build only when the ladder finds no existing capability. |
| A new "anchor-resolver" / "audit-row applicator" skill | Over-engineering. U11 extends an existing check (d) in `scripts/verify_references.py`; the other 22 units are one-file prose, stdlib-script, or `pytest` edits. A forged tool for a one-time set of internal edits is disproportionate (`rules/skills_and_integrations.md §1`). |
| `autoskills-3rd` (P2 rung) | Not reached — P1 resolved every unit. |

## 5. Gaps

None. Every unit U1–U23 resolves to `Read`/`Edit`/`Write` plus an existing
verification tool (`ruff`, `pytest`, `py_compile`, `make verify`, and the
`scripts/*.py` gates). No capability is missing; no skill is built.
