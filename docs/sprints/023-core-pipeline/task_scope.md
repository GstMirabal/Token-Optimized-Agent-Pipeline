# Task Scope — Sprint 023 (`upstream-findings`)

**Branch**: `ai-sprint/023` · **Base**: `main` at `18696c5` (`v4.7.0`)
**State**: **SUSPENDED** at the session bound, sprint open. Resume at `C0`.

Thirteen units, thirteen commits. `C9` ran first by design: this sprint's own
close invokes `branch_sovereignty audit`, so leaving that gate intermittently
wrong meant the sprint would trip on the defect it came to repair.

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| C9 | `scripts/branch_sovereignty.py`, `tests/…`, `workflows/close_workflow.md` | modify | **high** — a gate | lead · `devops_agent` ruleset | ✅ `437493b` |
| C0 | `agents.md`, `pipeline_workflow.md`, new template, new gate | modify/create | **high** — governance | lead · `rule_validator` ruleset | ⏳ **next** |
| C0.2 | `config/artifact_registry.json` + 3 consumers | create/modify | high | lead · `rule_validator` ruleset | ⏳ |
| C0.3 | `scripts/_root.py` + 6 consumers | create/modify | high | lead · `devops_agent` ruleset | ⏳ |
| C1 | `scripts/check_readme_counts.py` | modify | high | lead · `devops_agent` ruleset | ⏳ |
| C2 | `scripts/session_probe.py` | modify | high — a security report | lead · `devops_agent` ruleset | ⏳ |
| C3 | `env_shielding_auditor.py`, `hooks/on_commit.py` | modify | **high** — secrets | lead · `devops_agent` ruleset | ⏳ |
| C4 | `mass_standardizer.py` | modify | medium | lead · `skill_architect` ruleset | ⏳ |
| C5 | `agents/devops_agent.md` | modify | medium — role map | lead · `agent_orchestrator` ruleset | ⏳ |
| C6 | `agents.md`, `start_workflow.md` | modify | medium | lead · `rule_validator` ruleset | ⏳ |
| C7 | `requirements-freeze.txt` | modify | low | lead · `devops_agent` ruleset | ⏳ |
| C8 | `origin/contrib/host-findings` | modify | low | lead · `doc_orchestrator` ruleset | ⏳ |
| C10 | `scripts/ci_gate.py` (new), `workflows/deployment_workflow.md:17` | create/modify | **high** — a gate | lead · `devops_agent` ruleset | ⏳ |

## Why this session stopped here

`rules/token_economy.md §3.1` hard threshold: cycle 7 reached **16.5×** its
first turn (bound: 15×). The rule is binding and the sprint is open, so the
session **suspends** rather than closing or pushing on. **This is the first
time that bound has actually fired** since Sprint 021 built it.

`forced: true`. Unfinished work remains in `task_scope.md` — which is the
"too tight" signal the calibration section asks to be recorded, not a silent
one. Recorded here rather than inferred later.

## Two findings deferred out of `C9`, deliberately

| Finding | Where it goes |
| :--- | :--- |
| `WAIVERS = Path("config/abandoned_branches.json")` is a **relative path** — run from another directory it finds no waiver and does not say so | `C0.3`, which resolves the framework root once. Same defect class as `F-093-N2`. Kept out of `C9` to keep the commit atomic (`RA-08`) |
| `ai-sprint/024` and `ai-sprint/025` are integrated but unpruned | Prune **after** `C9` is merged, when the gate authorising it is trustworthy. This session declined to prune while that gate was still intermittent, rather than overriding a red verdict |

## Declared deviation — delegation

Unchanged from `022`: this session cannot spawn subagents, reported before
Phase 1 and authorised. `F-021-A2` makes it unavoidable for `scripts/`
regardless — no profile in `agents/` holds `Write` for that tree, which is
`C5`'s subject.

## Isolation

Single-session, single-branch. `no_interference` has no competing subtask.
