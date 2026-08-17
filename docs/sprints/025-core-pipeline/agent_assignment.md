# Agent Assignment — Sprint 025 (`jurisdiction`)

Same conflict, same honesty as Sprint `024`: **eight roles were not dispatched**,
because this session cannot spawn subagents. This records which profile's ruleset
governed each write, executed sequentially by the lead agent.

| Ruleset applied | Artifacts |
| :--- | :--- |
| `principal_agent` | `IMPLEMENTATION_PLAN.md` |
| `orchestrator` | this sprint directory and its records |
| `devops_agent` | `scripts/_mode.py`, `scripts/submodule_purity.py`, `scripts/session_probe.py`, `hooks/on_commit.py` |
| `rule_validator` | `agents.md §3 jurisdiction` |
| `doc_orchestrator` | `workflows/close_workflow.md`, `CHANGELOG.md` |
| `tester_agent` | `tests/test_session_protocol.py` |
| `qa_agent` | `make verify` — 137 tests, reference integrity, determinism scan |

`F-021-A2` remains the structural gap: no profile in `agents/` holds `Write` for
`scripts/` or `hooks/`, so `devops_agent` is the closest owner rather than the
correct one. Sprint `023` `C5` widens it; splitting a code-implementer profile is
a redesign of the role map and stays out of scope.
