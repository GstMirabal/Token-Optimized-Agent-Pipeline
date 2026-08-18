# Skill Assignment — Sprint 023 (`upstream-findings`)

**Covers the sprint to date** (units `C9`, `C0`, `C0.2`), appended as the
remaining eleven units land.

## Used

| Skill / tool | Where |
| :--- | :--- |
| `topology-monitor` (`legacy_app_auditor.py`) | Every `make verify` run — structural validity of the pipeline core nodes |
| `mass-standardizer` (`generate_manifest.py`) | Every `make verify` run — manifest parity across 34 skills |
| `graphify` | Session start: the graph was 16 commits stale and was rebuilt to 4213 nodes / 4557 edges before any `C0.2` research |

## Not used, deliberately

| Skill | Why not |
| :--- | :--- |
| `skillopt` (`train_runner.py`) | Rule optimization requires explicit human authorization (`close_workflow.md` Phase 1 `rules_optimization`). Not requested, not run |
| `compliance-checker` | Applies rule amendments to a host. This sprint writes amendments in the nucleus; applying them downstream is a host's pin bump, not this sprint's act |
| `graphify` semantic rebuild | The AST update was sufficient: `C0.2` touches two scripts and four documents, and the semantic pass costs an LLM round-trip for a question already answered by a targeted grep |

## Not used, and that is a finding

| Skill | What it would have caught |
| :--- | :--- |
| `python-quality-auditor` | It declares `ruff check .` as its linting step. `agents.md §1 linter_command` makes that command normative — *"Reject if exit code > 0"* — and **nothing in this framework runs it**: there is no `lint` target in the `Makefile`, `make verify` never invokes it, and `ruff` is not installed in `venv_skillopt/`. Measured 2026-08-18 with `which ruff` (not found) and `grep -rn ruff Makefile scripts/ hooks/` (no hits). A normative linter with no instrument is the same shape as the gates this sprint is repairing, one level up. Recorded in `task_scope.md` as unrouted — no existing unit owns it |
