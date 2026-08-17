# Task Scope — Sprint 021 (`cost-instrumentation`)

**Branch**: `ai-sprint/021` · **Base**: `main` at `36dd96a` (`v4.5.0`)

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | **high** — corrects a published claim | lead · `doc_orchestrator` ruleset | ✅ M0 |
| 2 | `docs/roadmaps/core/pipeline/021-cost-instrumentation.md` | create | low | lead · `orchestrator` ruleset | ✅ |
| 3 | `docs/sprints/021-core-pipeline/*` | create | low | lead · `orchestrator` / `principal_agent` rulesets | ✅ |
| 4 | `scripts/session_cost.py` | create | medium | lead · `devops_agent` ruleset | ⏳ M1 |
| 5 | `tests/test_session_protocol.py` | modify | medium | lead · `tester_agent` ruleset | ⏳ |
| 6 | `rules/token_economy.md`, `rules/loop_governance.md` | modify | medium | lead · `rule_validator` ruleset | ⏳ M3 |
| 7 | `scripts/session_probe.py` | modify | low | lead · `devops_agent` ruleset | ⏳ M4 |
| 8 | `claude/settings.hooks.json` | modify | low | lead · `devops_agent` ruleset | ⏳ M5 |
| 9 | `scripts/session_state.py`, both workflows | modify | **high** — a gate reads this state | lead · `devops_agent` ruleset | ⏳ M6 |
| 10 | `CHANGELOG.md` | modify | low | lead · `doc_orchestrator` ruleset | ⏳ |

## Declared deviation — delegation

Unchanged from Sprints `024` and `025`: subagent spawning is forbidden by session
configuration, reported before Phase 1 and authorised. `F-021-A2` makes it unavoidable for
`scripts/` regardless — no profile owns that directory.

## Isolation

Single-session, single-branch. `no_interference` has no competing subtask.
