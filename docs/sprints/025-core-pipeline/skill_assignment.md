# Skill Assignment — Sprint 025 (`jurisdiction`)

## Used

| Skill / tool | Where |
| :--- | :--- |
| `slash-commander` | `make verify` — command↔workflow links |
| `mass-standardizer` | `make verify` — manifest parity, 34 skills |
| `topology-monitor` | `make verify` — structural audit |

## Not used, deliberately

| Skill | Why not |
| :--- | :--- |
| `env-shielding-auditor` | No `.env` and no infrastructure files touched |
| `graphify` | Two new scripts and three edits; a targeted read costs less than building a graph (`start_workflow.md read_graph`) |

## No skill was forged

Nothing here is a reusable computational tool for a host. Both new scripts are
framework-internal and declare their invokers (`RA-16`), verified by
`scripts/verify_references.py` check (d).
