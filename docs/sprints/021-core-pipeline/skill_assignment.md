# Skill Assignment — Sprint 021 (`cost-instrumentation`)

## Used

| Skill / tool | Where |
| :--- | :--- |
| `slash-commander`, `mass-standardizer`, `topology-monitor` | `make verify` |

## Not used, deliberately

| Skill | Why not |
| :--- | :--- |
| `token-saver-auditor` | Its `scripts/` holds only `__init__.py` — the auditor of the token rule has no auditor. Sprint `030` work, not fixed here |
| `graphify` | One new script and a handful of edits; a targeted read costs less than building a graph |

## No skill was forged

`session_cost.py` is framework-internal and declares its invoker (`RA-16`). Nothing here is a
reusable computational tool for a host.
