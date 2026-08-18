# Task Scope — Sprint 023 (`upstream-findings`)

**Branch**: `ai-sprint/023` · **Base**: `main` at `18696c5` (`v4.7.0`)
**State**: **IN_PROGRESS**, resumed 2026-08-18 (session #2). Sprint open. **`C2` is
delivered and now approved by both gates** — see below. Next: `C3`.

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
| C2 | `scripts/session_probe.py` | modify | high — a security report | lead · `devops_agent` ruleset | ✅ `26367cf` + `ca29010` + `509f525` |
| C3 | `env_shielding_auditor.py`, `hooks/on_commit.py` | modify | **high** — secrets | lead · `devops_agent` ruleset | ⏳ **next** |
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

## `C2` is delivered and APPROVED — closed 2026-08-18, session #2

`26367cf` was the remediation of a **double rejection**. Both gates have now
returned, and `triple_lock`'s third lock is met for this unit.

| Gate | Round 1 | Round 2 | Round 3 |
| :--- | :--- | :--- | :--- |
| `qa_agent` (dispatched subagent) | **REJECTED** — `F-1` `probe_platform` at 93 lines against the 50-line bound; `F-2` closure parameter shadowing `state` with a different type; `F-3` `_from_exit` privacy marker the same commit reached past; `F-4`, `F-6` advisory | **REJECTED** — `G-1` blocking | **APPROVED** against `ca29010` |
| `tester_agent` (dispatched subagent) | **REJECTED** — `D1` critical, plus `D2`-`D7` | **APPROVED** against `ca29010`, `D1`-`D7` each reproduced remediated | — |

**`G-1`, the round-2 rejection, is the same defect class as the sprint's own
thesis.** `collect_security_controls` issued a request to derive the doubt line,
then the state function issued the **same** request internally. Both arguments to
`record()` evaluate eagerly, so the cause came from one response and the state it
annotated came from another: under a failure between the two calls the report
explained an answer it had never received. Measured by counting calls, not by
reading output — **5 invocations for 3 endpoints** — because under a healthy
network both responses agreed and the duplication was invisible in every
rendering. The correct one-call shape already existed twelve lines away, so one
function held two opposite patterns. Fixed in `ca29010`; the two classifiers now
take the fetched response, the shape `state_from_exit` already used.

**The Tester verified `D1` live rather than by unit test**, which is what round 1
had got wrong — that suite asserted the defect instead of catching it. Against
`cli/cli` the round-1 code produced **5 false accusations** and HEAD produces
**0**, with 4 doubt lines each naming its measured cause. `rust-lang/rust` and
`python/cpython` likewise 0. The anti-inversion check holds: on repositories the
token administers, genuinely disabled controls are still accused (3 accusations,
0 doubt on `GstMirabal/.github`), so the tri-state did not become a permanently
closed gate. The one accusation on `torvalds/linux` was checked before being
counted and is a **true positive** — `.protected` is `false` and `rulesets` is
`[]` — not a permission artifact.

**`T-1`, `T-2`, `T-3` — approved with coverage debt, and the debt is paid.**
The Tester approved the unit and named three defects that survived a green suite
when reintroduced by mutation. Closed in `509f525`, each verified to kill its
mutant (baseline `0`, three mutants `1`, restored `0`):

| ID | What passed green while broken |
| :--- | :--- |
| `T-1` | No test asserted **which** URL is asked, so reverting `D2` to the admin-only endpoint kept the count at three and passed. Coverage was *lost*, not missing: the URL used to live inside `branch_protection_state` where its own test saw it, and `ca29010` moved the fetch to the caller |
| `T-2` | Nothing pinned the extraction of `permissions.admin` — the whole of `D1`. Replacing it with `None` passed everything while producing the permanently closed gate the plan names as an abort criterion |
| `T-3` | `D6` was pinned for `dependabot_updates_state` and not its twin. Dropping the guard raises `AttributeError` out of a `main()` with no `try/except`, killing all five probes |

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

## Found at session start, session #2 (2026-08-18)

Three findings from running the start protocol rather than reading it. All three
are measured; none is routed to an existing unit.

| Finding | Where it goes |
| :--- | :--- |
| **`last_platform_probe` is read and written by nothing, so the documented 7-day cache never engages.** `session_probe.py:494` reads it; `grep -rn "last_platform_probe" --include="*.py" --include="*.md" .` returns **one reader, one doc mention in `start_workflow.md:22`, zero writers**, and the key is absent from `docs/active_state.json` after a probe run. Every session therefore makes 3-5 live GitHub API calls that the design says should happen a couple of times a year. Introduced in `7ccbde6` (Phase 019), **not** by `C2` — confirmed independently by the Tester gate as its `O-2` | **Unrouted.** Same class as the `ruff` finding below: a mechanism declared in prose that no code implements. Not `C2` (it repairs the report's *values*, not the cache), not `C6` |
| **`probe_cost` cannot measure the previous session, because it measures the live one.** `session_cost.measure_previous` takes `transcripts[-1]` sorted by mtime, and at session start the newest transcript is the session doing the asking. Reproduced: it returned `3b4625a5` — this session — while the session it should report is `50ce34a7`. That session measured **15.9×** against `§3.1`'s bound of 15×. Both firings of the bound in this sprint (16.5× and 15.9×) were recorded by hand; the probe built to surface them has never once seen one | **Unrouted.** The fix is one line — exclude the live session id — but `probe_cost` is the mechanism `rules/token_economy.md §3.1` leans on, so changing it is a governance-adjacent edit rather than a record |
| **`docs/0_SYSTEM_OVERVIEW.md` does not exist in the nucleus.** `agents.md §0` makes it the mandatory entry point of *every* session, and `start_workflow.md` `read_ruleset` names it. `ls docs/` shows no such file and `find . -name "0_SYSTEM_OVERVIEW.md"` returns nothing. The reading it stands for is satisfied here by `agents.md` plus `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md`, which is what `acknowledged_gaps.docs` already reasons about for Blueprints | **Unrouted.** Either the file is written or `§0` names what the nucleus reads instead. Adjacent to `C6` (the nucleus entry point) but not the same question, so not filed under it |

## Found while scoping the move to Cursor (session #2, for Sprint `026`)

| Finding | Where it goes |
| :--- | :--- |
| **`AGENTS.md` does not exist. It is the same file as `agents.md`, and only macOS hides that.** The Sprint `026` appendix opens its "already portable today" table with *"`AGENTS.md` already exists as a symlink to `agents.md` in a real host — the constitution is already exposed portably"*. In this nucleus it is not a symlink and not a second file: `stat -f "%i %N" agents.md AGENTS.md` returns **inode `105736819` for both**, because APFS is case-insensitive by default, and `git ls-files` tracks **only** `agents.md`. On any case-sensitive filesystem — Linux CI, a case-sensitive volume, a fresh clone on those — Cursor looks for `AGENTS.md` and finds nothing. The portability that reads as free is free only on the developer's own machine | **Sprint `026`, `P4`.** It changes that sprint's premise: the entry point must be *created* (a tracked symlink or a real file), not merely *declared already present*. Recorded here because it was measured here, and because a row in a table asserting a file exists is exactly the class of claim `RA-14` exists to re-verify |

## Found while gating `C2` — no unit owns these

| Finding | Where it goes |
| :--- | :--- |
| **`session_probe.py:493-501` has a bare `except ValueError: pass` and depth-4 nesting**, both prohibited by `agents.md §1`. The QA gate's `G-2` and `G-3`, proven **byte-identical to the parent** of `26367cf`, so `C2` did not author them and `rules/code_craft.md §2` forbids folding the fix in | **Unrouted**, alongside `hooks/state_mirror.py`'s identical `except: pass` recorded under `C0.3`. Three sites of one defect class now — worth one unit rather than three patches |
| **`gh_json:192` is the only function in `session_probe.py` with a rewritten body and no docstring.** The QA gate's `G-4`. `26367cf` rewrote it to delegate to `gh_call` and left it undocumented; the gate declined to block on it in `ca29010` because adjacency is not authorship, and applying a different standard to it than to `G-2`/`G-3` would make the gate inconsistent within one sprint | **Unrouted**, with `G-2`/`G-3` |
| **`HTTP_STATUS_RE` takes the first `(HTTP nnn)` in stderr, and `gh` puts a server-controlled message *before* the status.** The Tester's `N-1`: a message containing a literal `(HTTP 404)` would override the true status — same class as `D3`, narrower. The gate **could not reproduce it against the real API** and explicitly declined to press it; real formats confirmed as `gh: Bad credentials (HTTP 401)`, `gh: Validation Failed (HTTP 422)`. Parsing the last match would close it | **Unrouted, and deliberately not fixed.** This sprint's governing rule is *reproduce before repairing*; an unreproduced finding is exactly what the rule forbids acting on. Recorded so it is not rediscovered as new |
| **The secret-scanning pair's doubt cause is still a hardcoded literal.** The Tester's `O-1`: residual `D7`. `is_admin` is in scope at that call site, yet a non-admin reads `the repository payload did not answer` while the endpoint controls correctly read `admin-only endpoint, and this token does not administer the repository`. Not false — the payload genuinely omits the block — so it is a quality-of-cause note, not a defect. It does misdirect for an **admin** on a private repository, measured on `GstMirabal/CryptoBot` | **Unrouted.** Would be a one-line improvement to `C2`'s own thesis, but `C2` is closed and approved; reopening an approved unit for a non-defect is not warranted |

## Declared deviation — delegation

Unchanged from `022`: the session configuration forbids spawning subagents
unless the human asks. Reported before Phase 1 in session #1 and authorised.

**Session #2 reported the same conflict at the same point and the human lifted
it for both gates**, so `C2`'s remaining rounds were gated by dispatched
`qa_agent` and `tester_agent`, not by their author. The lift is per-session and
per-unit, not standing: `C3` onwards must ask again. Recording it because the
distinction is what `agent_assignment.md` exists to keep honest — five units of
this sprint were written *and* gated by the same session, and `C2` is the one
where that is not true.

`F-021-A2` makes self-execution unavoidable for `scripts/` regardless — no
profile in `agents/` holds `Write` for that tree, which is `C5`'s subject.

## Isolation

Single-session, single-branch. `no_interference` has no competing subtask.
