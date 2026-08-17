# Agent Assignment — Sprint 021 (`cost-instrumentation`)

Eight roles were **not** dispatched: this session cannot spawn subagents. This records which
profile's ruleset governed each write, executed sequentially by the lead agent — the same
honest form used in Sprints `024` and `025`.

| Ruleset applied | Artifacts |
| :--- | :--- |
| `principal_agent` | `IMPLEMENTATION_PLAN.md` |
| `orchestrator` | this sprint directory, `021-cost-instrumentation.md` |
| `doc_orchestrator` | the program-queue correction, `CHANGELOG.md` |
| `rule_validator` | `rules/token_economy.md`, `rules/loop_governance.md` |
| `devops_agent` | `scripts/session_cost.py`, `session_probe.py`, `session_state.py`, `claude/settings.hooks.json` |
| `tester_agent` | `tests/test_session_protocol.py` |
| `qa_agent` | `make verify` — structural verification, not a dispatched role |

`F-021-A2` remains the structural gap: no profile holds `Write` for `scripts/`, so
`devops_agent` is the closest owner rather than the correct one. Sprint `023` `C5` widens it.
