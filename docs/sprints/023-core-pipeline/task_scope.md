# Task Scope — Sprint 023 (`upstream-findings`)

**Branch**: `ai-sprint/023` · **Base**: `main` at `18696c5` (`v4.7.0`)
**State**: **IN_PROGRESS**, resumed 2026-08-18. Sprint open. **`C2` is delivered but ungated** — see below. Next: re-gate `C2`, then `C3`.

Thirteen units, thirteen commits. `C9` ran first by design: this sprint's own
close invokes `branch_sovereignty audit`, so leaving that gate intermittently
wrong meant the sprint would trip on the defect it came to repair.

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| C9 | `scripts/branch_sovereignty.py`, `tests/…`, `workflows/close_workflow.md` | modify | **high** — a gate | lead · `devops_agent` ruleset | ✅ `437493b` |
| C0 | `agents.md`, both workflows, new template, 3 agent profiles | modify/create | **high** — governance | lead · `rule_validator` ruleset | ✅ `2821953` |
| C0.2 | `config/artifact_registry.json` + 3 consumers | create/modify | high | lead · `rule_validator` ruleset | ✅ `92f42da` |
| C0.3 | `scripts/_root.py` + 6 consumers | create/modify | high | lead · `devops_agent` ruleset | ✅ `359d03c` + `fix` |
| C1 | `scripts/check_readme_counts.py` | modify | high | lead · `devops_agent` ruleset | ✅ `b2d7c2e` |
| C2 | `scripts/session_probe.py` | modify | high — a security report | lead · `devops_agent` ruleset | 🔄 `26367cf` — **gate round 2 owed** |
| C3 | `env_shielding_auditor.py`, `hooks/on_commit.py` | modify | **high** — secrets | lead · `devops_agent` ruleset | ⏳ **next**, after `C2`'s round 2 |
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
| **Opening a sprint does not update the anchor, and nothing notices** | Found on resume: `docs/active_state.json` still read `current_sprint.id: 22` while `ai-sprint/023` and this directory already existed. No script writes that field — `session_state.py claim` takes only a session id — so it is a manual edit with no gate. **The freshness check is one-directional**: `docs_freshness_check.py:418` complains when the anchor names a sprint directory that does not exist, but not when a *newer* sprint directory exists than the anchor names, which is this case and the one that misleads a cold session. Corrected to `23` by hand here. Belongs with `C0.2` (the artifact registry defines each phase by the artifact it leaves) — a sprint directory without a matching anchor is exactly the mismatch that registry exists to catch. **Resolved in `16ed3e9`, and the instrument this row proposed was rejected by measurement**: comparing the anchor against the newest directory under `docs/sprints/` fires on a *correct* state here, because `024` and `025` exist as directories while `023` is legitimately in flight. `session_probe.probe_anchor_sprint` compares the anchor against the checked-out `ai-sprint/[ID]` branch instead (`RA-12` makes the branch the sprint being worked), and a test pins the rejected comparison so the cheaper wrong instrument cannot return |

## Found while executing `C0`

| Finding | Where it goes |
| :--- | :--- |
| **The nucleus never gets `plansDirectory`, and the safety net shipped in `v4.6.0` is host-only.** Measured, not inferred: this repository has **no `.claude/settings.json` at all**, and `C0`'s own plan was drafted under `~/.claude/plans/` — the exact ephemeral storage the unit exists to replace. The cause is structural rather than an oversight: `plansDirectory` ships in `claude/settings.hooks.json`, the **bridge template**, and `agents.md §5 nucleus_neutrality` prohibits installing the bridge when the workspace is `.agents` itself. So the framework that wrote the fix cannot receive it. Recorded in `docs/plans/README.md` under Limits | `C6` (the nucleus entry point) — resolving it means deciding whether the nucleus installs its own bridge, which is that unit's subject, not `C0`'s |
| **`RA-14` found three false paths, not the two the plan predicted.** The worst was `agents/rule_validator.md:19`, calling `task_scope.md` a *"git-ignored session artifact at the host root"* — both halves false since Sprint 024, in the profile of the agent that **produces** the file. `pipeline_workflow.md` Phase 4.3 and `agents/token_economy_agent.md:25` were the other two | Fixed inside `C0`'s commit. The lesson is the one `RA-14` already states and this session re-earned: grep the term, do not patch the sites you happened to look at |

## Found at session start on resume (2026-08-18)

| Finding | Where it goes |
| :--- | :--- |
| **The nucleus has a *partial* `.claude/` bridge, which is worse than none because it reads as installed.** Measured: `.claude/commands/agents/` holds 11 symlinks dated 2026-07-20/26, while `commands/` holds 13. The three added since — `harden.md`, `reconcile.md`, `revdoc.md` — are **not linked and therefore not invocable in the nucleus**, and `skeleton.md` is a dangling link to a deleted target. Reproduce with `comm -13 <(ls .claude/commands/agents/ \| sed 's/\.md//' \| sort) <(ls commands/ \| sed 's/\.md//' \| sort)`. This bit immediately: `start_workflow.md` `drift_check` exited `2` and directed to `/agents:reconcile`, a command this repository cannot run. It also sharpens the precedent `RA-16` was written from — `/agents:harden` shipped and was never run here, and one reason is that it was never linked | `C6`, which already owns whether the nucleus installs its own bridge (routed there by `C0`'s findings). The measurement changes that unit's question from *whether to install a bridge* to *what to do with a stale one already present* |

## Found while executing `C0.2`

| Finding | Where it goes |
| :--- | :--- |
| **Sprint 023 had skipped Phases 4.1 and 4.2 and nothing could see it.** The registry's first act was to report `agent_assignment.md` and `skill_assignment.md` missing from this directory — both produced by sprints `021`, `022`, `024` and `025`, both invisible to the three-filename map `docs_freshness_check.py` held before `C0.2`. Reproduce: `python3 scripts/docs_freshness_check.py . 23` | Fixed in the same session: both files are now in this directory, covering the sprint to date. The gap is recorded rather than quietly closed, because it is `C0.2` catching a real defect on the sprint that built it |
| **The declared tier and the model that actually ran are not the same fact, and only one of them is recorded.** `config/model_tiers.json` and the 13 profile frontmatters declare a model per role — `gate` → opus, `author` → sonnet, `mechanical` → haiku — and `check_model_tiers.py` verifies that map on every `make verify`. What it verifies is **coherence between two declarations**, never what executed: in a session that cannot dispatch subagents, every unit runs on the session model regardless of its assignee's tier. Sprint 022 called its own tiering *"informed judgment"* and `R6` of `C0.2` named the `Assignee` column as the fix, but attribution through the profile only holds when the profile's model is the one that ran. Measured on this sprint: `C9`, `C0` and `C0.2` are attributed to `devops_agent` and `rule_validator` (tier `author`, sonnet) and all three executed on the session model, Opus 5 | **Unrouted.** The durable fix is one clause in `pipeline_workflow.md` Phase 4.1 requiring `agent_assignment.md` to state the model that ran whenever it differs from the assignee's declared tier — proposed, not applied, because it changes what every sprint owes and that is a governance edit rather than a record. Recorded for `023` in `agent_assignment.md` in the meantime |
| **`ruff check .` is normative and no mechanism runs it.** `agents.md §1 linter_command` says *"Reject if exit code > 0"*. Measured 2026-08-18: `which ruff` → not found; no `lint` target in the `Makefile`; `grep -rn ruff Makefile scripts/ hooks/` → no hits. `skills/python-quality-auditor` declares the command and is wired into nothing. So every Python change in this repository, including this sprint's, has been merged unlinted against a rule that reads as enforced | **Unrouted — no existing unit owns it.** Not `C1`-`C3` (each repairs one named script), not `C0.3` (path resolution). Named here rather than attached to the nearest unit, because a finding filed under a unit that does not cover it is how a finding disappears |

## Found while executing `C0.3`

| Finding | Where it goes |
| :--- | :--- |
| **A test destroyed the repository's real waiver list and the suite stayed green.** Anchoring `branch_sovereignty.WAIVERS` to the framework root is correct, and it silently converted `test_waived_branch_does_not_block` from a test writing into its own `tmp_path` into one overwriting `config/abandoned_branches.json` with fixture data, destroying the three keys that document why the valve exists. **Found by reading the commit's diff, not by any assertion** | Fixed in the commit after `359d03c`: file restored, the test patches `WAIVERS` instead of writing through it, and `make verify` gains `git diff --exit-code config/ hooks/ scripts/` after the suite — the same regenerate-and-compare shape the manifest check already used. The general lesson is `C0.3`'s own, inverted: **anchoring a constant is not a local change**, because every test that wrote through it now writes into the real repository |
| **`DENYLIST_DIR` pointed at `.agents/scripts/denylists`** — correct inside a host, a directory that does not exist in the nucleus. The three denylists that ship in `scripts/denylists/` were therefore never loaded here and the density filter ran empty, degrading silently because `load_denylist` returns an empty set on a missing file | Fixed inside `C0.3`'s commit as a mixed-scope path, the same treatment the plan specified for `branch_sovereignty`'s `config/` |
| **`hooks/state_mirror.py` swallows a corrupt anchor with a bare `except: pass`**, and closes with `else: pass`. `agents.md §1 exception_handling` prohibits both — *"No `pass` in except. Explicit logging required."* A mirror that silently declines to update when the anchor is unparseable leaves the backup stale exactly when it is the one thing that matters | **Unrouted.** Not `C0.3` — that unit only added the file's module docstring, and folding a behaviour change into it would break the atomicity `RA-08` requires. Named here rather than fixed in passing |

## `C2` is delivered and NOT approved — read this before resuming

`26367cf` is the remediation of a **double rejection**, and no round-2 verdict
exists. Until both gates pass, `C2` has no approved gate and `triple_lock`'s
third lock is unmet for it.

| Gate | Round 1 | Round 2 |
| :--- | :--- | :--- |
| `qa_agent` (dispatched subagent) | **REJECTED** — `F-1` `probe_platform` at 93 lines against the 50-line bound; `F-2` closure parameter shadowing `state` with a different type; `F-3` `_from_exit` privacy marker the same commit reached past; `F-4`, `F-6` advisory | **owed** |
| `tester_agent` (dispatched subagent) | **REJECTED** — `D1` critical, plus `D2`-`D7` | **owed** |

**`D1`, and why it matters more than the fix.** GitHub answers `404` on an
admin-only endpoint to any caller without administrative access, whether the
feature is on or off. Reproduced live against `cli/cli` and `torvalds/linux`,
both demonstrably hardened: three false accusations each, with a remedy
proposing to patch a repository the caller cannot administer. **The unit
rebuilt this sprint's own defect inside the function written to remove it**,
and the first test suite asserted the defect instead of catching it. The author
had measured only against this repository, where the token is an admin, and
recorded that blind spot in the session without acting on it.

`F-5` was rejected back at Gate 1 with a measurement rather than an argument:
the report joiner renders at exactly the indent `main()` gives every top-level
finding.

## Suspended at the token bound, a second time

`rules/token_economy.md §3.1`: cycle 1 of session `50ce34a7` reached **15.1×**
its first turn (335,285 tokens) against a bound of 15×. Reproduce:
`python3 scripts/session_cost.py --session 50ce34a7-24bc-4431-9294-11c1c9c5fcbc`.

The rule is binding and the sprint is open, so the session suspends rather than
closing or pushing on. **Re-gating `C2` was deliberately NOT done on the way
out**: a verification performed on exhausted context is the low-quality check
the bound exists to prevent, and an approval produced that way would be worse
than the missing one it replaces.

**Second firing in this sprint** — the first was cycle 7 at 16.5×. Two firings
across two sessions of one sprint is the calibration signal `§3.1` asks to be
recorded rather than inferred.

## Found while suspending

| Finding | Where it goes |
| :--- | :--- |
| **`resume_pointer.derived_from` reads `"git (registry pending C0.2)"`, and `C0.2` landed.** The substance is still true — the pointer is derived from git — but the parenthetical now names a delivered unit, so a cold session reads it as work outstanding that is not. The cause is that `C0.2` shipped `config/artifact_registry.json` with the three consumers the roadmap named, and `scripts/session_state.py` was never one of them: deriving the pointer from the registry is roadmap item `M6.3`, correctly outside this unit. Reproduce: `python3 -c "import json;print(json.load(open('docs/active_state.json'))['resume_pointer'])"` | **Unrouted, and deliberately not fixed on the way out.** Editing the anchor by hand is the exact class of change `session_probe.probe_anchor_sprint` was built this session to detect. The label should be corrected when `session_state.py` becomes a registry consumer under `M6.3`, so the text and the mechanism change together rather than the text alone drifting into a second false claim |

## Declared deviation — delegation

Unchanged from `022`: this session cannot spawn subagents, reported before
Phase 1 and authorised. `F-021-A2` makes it unavoidable for `scripts/`
regardless — no profile in `agents/` holds `Write` for that tree, which is
`C5`'s subject.

## Isolation

Single-session, single-branch. `no_interference` has no competing subtask.
