# Agent Assignment — Sprint 022 (`model-tiering`)

Eight roles were **not** dispatched: this session cannot spawn subagents. This
records which profile's ruleset governed each write.

| Ruleset applied | Artifacts |
| :--- | :--- |
| `principal_agent` | `IMPLEMENTATION_PLAN.md` |
| `orchestrator` | sprint roadmap and this directory |
| `agent_orchestrator` | the 13 profile frontmatters |
| `token_economy_agent` | `config/model_tiers.json` — **and it now owns it**, per the `tier_ownership` row this sprint added to its charter |
| `devops_agent` | `detect_new_models.py`, `check_model_tiers.py`, `Makefile` |
| `rule_validator` | the charter amendment |
| `tester_agent` | `tests/test_session_protocol.py` |
| `qa_agent` | `make verify` — structural verification, not a dispatched role |

`F-021-A2` remains: no profile holds `Write` for `scripts/`, so `devops_agent` is
the closest owner rather than the correct one. Sprint `023` `C5` widens it.
