# Skill Assignment — Sprint 024 (`close-machinery-verdicts`)

Produced by Phase 4.2. `skill_architect`'s question is whether a computational
tool already exists before a task starts, so the useful answer here is mostly
**which skills were deliberately not used, and why**.

## Used

| Skill / tool | Where | Note |
| :--- | :--- | :--- |
| `slash-commander` | `make verify` | Verifies `commands/` ↔ `workflows/` links; 13 commands checked |
| `mass-standardizer` (`generate_manifest.py`) | `make verify` | Regenerates `skills/manifest_skills.json` and diffs it; 34 skills |
| `topology-monitor` (`legacy_app_auditor.py`) | `make verify` | Structural audit of pipeline core nodes |

## Not used, deliberately

| Skill | Why not |
| :--- | :--- |
| `token-saver-auditor` | Its `scripts/` directory holds only `__init__.py` — the auditor of the token rule has no auditor. Recorded in the program roadmap as Sprint `025` work, not fixed here |
| `graphify` / knowledge graph | `start_workflow.md` `read_graph` skips graph construction under ~25 source files for a targeted grep. This sprint touched 2 scripts and 2 workflows; building a graph would cost more than it saved |
| `env-shielding-auditor` | No `.env`, no infrastructure files touched. `RA-09` was never in play |

## No skill was forged

`skill_architect`'s Three-File Standard was not invoked: nothing in this sprint
is a reusable computational tool. The two scripts changed already exist and
already declare their invokers (`RA-16`), verified intact by
`scripts/verify_references.py` check (d) in `make verify`.
