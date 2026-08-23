# Task Scope — Sprint 023 (`upstream-findings`)

**Branch**: `ai-sprint/023` · **Base**: `main` at `18696c5` (`v4.7.0`)
**State**: **IN_PROGRESS**, resumed 2026-08-22 (session #4). Sprint open.
**`C4` and `C4.2` are delivered and APPROVED by both gates** (`5056796`,
`955eb5d`) — seven gate rounds across the two, five rejections, and the
rejections caught a destructive regression `C4` had committed against itself.
**`F-086-S3` is closed.** Delegation was lifted for
those passes only (see *Declared deviation — delegation*). **Next: `C5`**,
which must ask for that lift again.

Fourteen units after `C3.2` was added mid-sprint at the remediation halt. `C9` ran first by design: this sprint's own
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
| C3 | `env_shielding_auditor.py`, `hooks/on_commit.py` | modify | **high** — secrets | lead · `devops_agent` ruleset | ✅ `aa83309`…`5bcbdf6`, gate-approved |
| C3.2 | `hooks/on_commit.py` (`ALLOW_MARKER`), `rules/qa_and_testing.md` | create | **high** — a documented bypass of a secret gate | lead · `devops_agent` ruleset | ✅ `50094c1` + `R5` fixes |
| C4 | `mass_standardizer.py`, `tests/…`, skill `README.md` + `SKILL.md` | modify/create | medium — raised to **high** on execution: the unit deleted authored content | lead · `skill_architect` ruleset | ✅ `5056796`, gate-approved |
| C4.2 | `rules/django_backend_standard.md` (new), `agents.md`, `README.md`, `skills/django-expert-3rd/SKILL.md` | create/modify | **high** — relocating governance content | lead · `rule_validator` ruleset | ✅ `955eb5d`, gate-approved |
| C5 | `agents/devops_agent.md`, `agents.md` §6 role table | modify | medium — role map | lead · `agent_orchestrator` ruleset | ✅ `aa2b11d` + `R1` — both gates APPROVED |
| C6 | `agents.md` §0, `start_workflow.md` (3 rows), `audit_workflow.md` (`federation_audit`), `docs/plans/README.md` (routing discharged), `tests/test_installer.sh` (+1 assertion), `.claude/commands/agents/` (untracked, regenerable) | modify | medium | lead · `rule_validator` ruleset | ✅ `R2` — both gates APPROVED |
| C7 | `requirements-freeze.txt` → `docs/audits/SKILLOPT_TRANSITIVE_CLOSURE.md` (git rename), `skills/skillopt/SKILL.md` (reference) | move | low | lead · `devops_agent` ruleset | ✅ both gates APPROVED, first round |
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
| **The nucleus never gets `plansDirectory`, and the safety net shipped in `v4.6.0` is host-only.** Measured, not inferred: this repository has **no `.claude/settings.json` at all**, and `C0`'s own plan was drafted under `~/.claude/plans/` — the exact ephemeral storage the unit exists to replace. The cause is structural rather than an oversight: `plansDirectory` ships in `claude/settings.hooks.json`, the **bridge template**, and `agents.md §5 nucleus_neutrality` prohibits installing the bridge when the workspace is `.agents` itself. So the framework that wrote the fix cannot receive it. Recorded in `docs/plans/README.md` under Limits | `C6` (the nucleus entry point) — resolving it means deciding whether the nucleus installs its own bridge, which is that unit's subject, not `C0`'s. **✅ Discharged by `C6`, and the finding's stated cause above is corrected there**: `nucleus_neutrality` prohibits *structural scaffolding*, not the bridge — `scripts/install_claude.py` ships `install_nucleus_bridge()` for this exact case, and what it deliberately omits is hooks, skills, MCP and settings. So `plansDirectory` is absent **by omission, not by prohibition**. The finding statement is left as written, per the rule the `C5` gates set: a finding records what was found, and is closed with a marker rather than rewritten |
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

## Found at session start, session #3 (2026-08-22)

One new finding, plus three prior ones re-verified as still true. Re-verification
is recorded because `RA-14`'s lesson is that a finding written once is not a
finding that stays true, and because two of the three now have a second session
of evidence behind them.

| Finding | Where it goes |
| :--- | :--- |
| **`detect_drift.py` has no notion of "these commits belong to the sprint that is open", so verdict `A` fires on every resume of any in-flight sprint.** Measured this session: exit `2`, 24 of 26 commits reported as covered by no released section. All 24 are Sprint 023's own, on `ai-sprint/023`, each carrying the `#023` suffix `agents.md §5 historical_log` requires, with `SPRINT_LOG.md` recording them. `[Unreleased]` holds only the **planning** entry for `C9`/`C10`; the delivery entries are written by `close_workflow.md` Phase 4, which by definition has not run while the sprint is open. The check therefore directs a resuming session to `/agents:reconcile` — a workflow whose own text says it exists for work done **outside** the protocol — for work done inside it. Same defect class the sprint exists to remove: a control reporting a determination it cannot support. Reproduce: `python3 scripts/detect_drift.py; echo $?` on any open sprint branch | **Unrouted.** Not `C10` (that unit is `ci_gate.py`) and not `C9` (`branch_sovereignty.py`). The fix is a fourth verdict or an `A`-suppression when `HEAD` is on `ai-sprint/[ID]` and the anchor's `current_sprint.id` matches — but `detect_drift.py` is the instrument `start_workflow.md` `drift_check` leans on, so changing it is governance-adjacent. Human decision this session: **record and proceed to `C3`**, do not reconcile and do not open a unit for it |

Re-verified, all three still true and all three still unrouted:

| Prior finding | Re-verification this session |
| :--- | :--- |
| The nucleus `.claude/` bridge is partial | `comm -13` still returns `harden`, `reconcile`, `revdoc` as present in `commands/` and absent from `.claude/commands/agents/`; `skeleton.md` is still a dangling symlink. Second session of evidence. Belongs to `C6` |
| `last_platform_probe` has no writer | Key still absent from `docs/active_state.json` after a `session_probe.py` run this session. Unrouted |
| `docs/0_SYSTEM_OVERVIEW.md` does not exist | `ls docs/` still shows no such file. Unrouted |

## Found while executing `C3`

| Finding | Where it goes |
| :--- | :--- |
| **The roadmap's framing of `C3` is half wrong: `env_shielding_auditor.py` does not have "good patterns with a bad list" — the patterns are also bad.** The value character class is `[a-z0-9+/=]{16,}`, which excludes `-` and `_`, so the auditor misses the three commonest real credential shapes **in files it already scanned**: `sk-live-…` (Stripe/OpenAI), `ghp_…` (GitHub PAT), `xoxb-…` (Slack). Measured in isolation — `api_key = "abcdef0123456789abcd"` MATCHES, `api_key = "sk-live-9f2a4c8e1b7d3a5690"` does not. Found because a reproduction case in a `.py` file (already on the scanned list) failed for a reason the file list could not explain | **Unrouted, and deliberately not fixed in `C3`.** The unit's approved scope is the file list and the hook's three alternations; widening the value class changes the false-positive profile of every pattern at once, which is the one thing this unit's abort criterion is written against. `tests/test_env_shielding_auditor.py` uses a value that matches the current class **on purpose**, so its cases isolate the file-list defect and nothing else. Worth a unit of its own — it is a live miss, not a cosmetic one |
| **`agents.md §1` declares `ruff check .` as the linter with "Reject if exit code > 0", and nothing invokes it.** Measured: `grep -n ruff Makefile` returns nothing, `make verify` runs fourteen checks and ruff is not among them, and `ruff check .` exits `1` with **176 errors** across the tree. So the declared gate has never rejected anything. `hooks/on_commit.py` alone carries nine, all predating this sprint — proven by running ruff against the stashed tree and getting a byte-identical rule/site set | **Unrouted.** Exactly the `RA-16 INVOCATION_COVERAGE` class — a mechanism declared in prose that no invoker calls — and the same shape as `last_platform_probe` above. Not `C3`: `rules/code_craft.md §2` forbids folding 176 pre-existing findings into a fix commit, and turning the gate on is a decision with a migration attached, not a patch |

## Found by the `C3` gates — routed, not folded in

The Tester gate rejected `C3` round 1 on two false-positive classes and, in
doing so, produced the most useful finding of the unit: **the measurement that
cleared round 1 could not have detected them.**

| Finding | Where it goes |
| :--- | :--- |
| **A 0-delta false-positive measurement over the nucleus is non-probative for a gate that runs on hosts.** Round 1 measured 455 tracked files, reported 0 new flags, and was honest. The Tester then measured the corpus itself: **6 tracked files are reachable by the YAML form and 0 by the Dockerfile form.** The nucleus contains no Kubernetes manifest, no Helm chart, no Compose file and no Dockerfile, so the corpus could not falsify the claim it was run to test. Round 2 added a host-shaped corpus — stock Ingress, Bitnami `values.yaml`, Compose, `.gitlab-ci.yml`, Terraform — and 16 of 20 legitimate lines were flagged | **Fixed in `C3` round 2**, and the corpus is now a permanent fixture in `tests/test_on_commit.py` rather than a throwaway probe. **The general lesson is unrouted**: every gate in `hooks/` runs in hosts and is measured here, so this repository's own content is the wrong denominator for all of them. Worth a rule amendment — a false-positive measurement must state what fraction of its corpus the changed code path actually reaches |
| **A literal `.env` with live credentials passes the gate.** `Path(".env").suffix` is `''`, not `'.env'`, so the forbidden-extension branch never fires on the file it exists to catch, and the content scan misses it too because `.env` uses unquoted `KEY=value`. Same for `.env.production` and `.env.local`. Reproduced by the Tester end to end: `audit_secret_shielding()` returned `True` (commit allowed) with `API_KEY=…` and `DB_PASSWORD=…` staged | **Unrouted, pre-existing.** Not `C3`: the unit's scope is the file list and three named alternations, and this is the forbidden-extension branch plus an unquoted-assignment form neither half declares. It is the highest-severity item any gate has produced this sprint — `RA-09 SECRET_SOVEREIGNTY` is the rule it defeats — and it deserves its own unit rather than a rider on this one |
| **`get_staged_files()` returns git-quoted names, and the path selector silently drops forms on them.** With the default `core.quotePath=true` a non-ASCII filename comes back as `"caf\303\251.yaml"` **including the literal quotes**, so `Path.suffix` is `.yaml"` and the YAML form is not selected. No signal is emitted | **Unrouted, pre-existing mechanism made load-bearing by `C3`.** Before this unit nothing in the hook read `path`; now the format selector does, so a pre-existing quirk of `get_staged_files` became a correctness dependency. The fix is `git -c core.quotePath=false` in one place |
| **The exclusion filters are trivially abusable.** `PLACEHOLDER_MARKERS` is a substring test, so `ENV API_KEY=fake9f2a…` clears the gate; `_is_test_artifact` skips any path containing a `tests/` component, so production Helm values at `deploy/tests/values.yaml` are never read | **Unrouted, pre-existing.** `C3` extended the reach of these filters without changing them, which is why they are reported here rather than fixed here. They are a deliberate false-positive trade and re-tightening them is the same decision as the abort criterion, taken deliberately rather than as a side effect |

### Round 2 of the Tester gate — the remediation had its own defects

Rejected again, narrowly. Both round-1 classes were confirmed closed and the
host corpus was confirmed the right structural answer to F3, but **the fix
introduced one false positive and one lost detection**, and the second was a
regression against the pre-`C3` gate.

| Finding | Resolution |
| :--- | :--- |
| **`PRIVATE_KEY_BLOCK` returned before the match loop, so it bypassed every exclusion the other forms obey** — `MIN_SECRET_LENGTH`, `PLACEHOLDER_MARKERS`, the `$`/`{`/`[` exemption, `_names_a_reference`. It blocked a setup guide whose key body was literally `YOUR_PRIVATE_KEY_HERE`, and one whose body was `changeme` — **two phrases already in `PLACEHOLDER_MARKERS`**. It was the one form an author had no way to write a legitimate example against | **Fixed.** It is now a form like any other, with `name` and `value` groups, and requires sixteen unbroken base64 characters after the header. That single requirement separates a key from prose quoting the header and from a placeholder body, without needing a closing `-----END` — a key pasted into a diff hunk is still a key |
| **The `://` value exemption dropped credentials that ARE URLs.** `SLACK_WEBHOOK_SECRET = "https://hooks.slack.com/services/…"` was caught by this gate **before `C3` existed** and was not caught after — a regression, not a miss. Same for a MongoDB DSN with inline userinfo. Meanwhile the auditor half of this same unit still matches `Slack Webhook` in its pattern table, so **the two halves contradicted each other for the third round running** | **Fixed by deletion.** The value-side test is gone entirely; the name side already covers every pointer shape measured (`api_key_url`, `private_key_path`, `POSTGRES_PASSWORD_FILE`), because a key that points at a credential is named for what it points with |
| **The justification written for that exemption was factually false.** The comment claimed base64 payloads do not begin with `/`. Measured by the gate: **321 of 20000** random 24-byte base64 values do, which is 1 in 64 as the alphabet predicts. So roughly one base64 secret in 64 was exempt, on the strength of a sentence asserting the opposite | Moot — the rule it justified is deleted. Recorded because the failure mode is worth naming: **a comment that reasons its way to a rule is not evidence for the rule**, and this one read as though it had been measured |
| **The gate was inverted on the pair.** Staged together, `C3` blocked `docs/TLS_SETUP.md` (a placeholder PEM in a setup guide) and passed `config/settings.py` (a live Slack webhook). The pre-`C3` gate did the opposite | Both directions are now pinned by tests, in both polarities |
| **F3 recurred a third time.** Through all of it the 455-file nucleus delta reported 0 new and 0 lost, because this repository contains neither a PEM header nor a webhook URL | The corpus now carries both. It still cannot be assumed sufficient, which is the whole point of the routed F3 finding above |

The Tester also attacked `_names_a_reference`'s bare `endswith` on request and
**could not reproduce a realistic credential-holding name** ending in `id`,
`ref`, `name`, `file`, `path`, `policy`, `dir`, `url`, `uri`, `arn` or
`provider` — the real-world names of that shape (`AWS_ACCESS_KEY_ID`,
`private_key_id`, `token_uri`) are public metadata. Reported as a suspicion and
explicitly not acted on, which is this sprint's rule working as intended.

### Round 3 of the Tester gate — one finding, and it refuted the reasoning

| Finding | Resolution |
| :--- | :--- |
| **`GOOGLE_APPLICATION_CREDENTIALS` is blocked, in stock Compose and stock Dockerfile.** Round 2 deleted the value-side pointer test on the argument that *"a key that points at a credential is named for what it points with"*, so the name side would cover every case. The canonical Google Cloud variable is named for what it points **at**: it ends in `credentials`, which is a `SECRET_WORD` and not a reference word, so `_names_a_reference` structurally cannot see it, and its value is always a path to a mounted key file. Three more of the shape: `privateKey: /etc/ssl/private/tls.key`, `azure_credentials:`, `vault_secret:`. Both formats are `C3`'s own new forms and both were clean before this unit | **Fixed** with a narrow value-side test — `_points_at_a_file`: an absolute path of two or more segments over a charset excluding `+` and `=`, plus a file extension or a third segment. It does **not** reopen the round-2 regression: a Slack webhook, a Mongo DSN and a protocol-relative URL all fail on the leading `/`, and all three stay pinned as detections |
| The base64 exemption rate of that new rule | **Measured, not argued** — 200,000 random values per size: **0.067%** at 24 bytes, 0.107% at 32, 0.140% at 48, against **1.54%** for the deleted `/`-prefix rule. Written in the docstring as those three numbers and explicitly not claimed to be zero. The first draft of that docstring said 0.02%, which was an estimate rather than a measurement, and correcting it before commit is the whole content of the `R2-3` lesson |
| **Elided ASN.1 prefix in documentation.** A README showing `-----BEGIN RSA PRIVATE KEY-----` followed by `MIIEpAIBAAKCAQEA...` is flagged. That prefix is a fixed DER header shared by essentially every RSA key and carries zero entropy | **Open, low severity, not fixed.** The Tester declined to reject on it and so does this record: an author has an escape via `PLACEHOLDER_MARKERS`, and content shaped like a key body arguably should not be committed. Recorded so it is not rediscovered as new |

**The Tester corrected its own round-2 work on the record**: it had also reported a
GKE `Deployment` manifest in that class, then found real Kubernetes uses
`- name: X` / `value: Y` pairs rather than flat mappings, so its single-line
version had not been stock content. The finding survived on Compose and
Dockerfile, which do use flat mappings. Worth keeping because the gate had
rejected round 1 partly on the discipline of testing stock files over invented
lines, and that discipline cut against its own case.

**Strike position.** Three consecutive Tester rejections on one unit.
`workflows/remediation_workflow.md` Phase 0 triggers at **more than** three, so
it has not fired; a fourth rejection fires it. Recorded rather than left to be
counted later. The trend is converging — two blocking findings, then two, then
one — and each round's finding was in the fix for the previous round, which is
the signature of a gate doing its job rather than of a unit out of control.

### Round 4 — `remediation_workflow.md` Phase 0 has fired. `C3` is HALTED pending a human decision

Fourth consecutive Tester rejection. The trigger is *"QA or Tester forcefully
reject the exact same logic block **>3 consecutive times**"*, and `R3-1` and
`R4-1` are the same logic block — the value-side pointer test. **Nothing is
reverted and no further patching is done until the human decides**, because
deciding for them is the failure mode this switch exists to stop.

| Finding | Status |
| :--- | :--- |
| **`_points_at_a_file` blocks relative and home-relative pointers.** `GOOGLE_APPLICATION_CREDENTIALS: ./secrets/gcp-sa.json` and `: ~/.config/gcloud/application_default_credentials.json` are blocked in stock local-development Compose files that were clean before `C3`. The second is the literal path `gcloud auth application-default login` writes. `PATH_VALUE` requires a **leading `/`**, so relative paths — half of the path space — fail it. Five more: bare `secrets/gcp-sa.json`, root-level `/sa-key.json` (one segment), `/etc/azure-creds` (no extension, two segments), `/secret/data/prod/` (trailing slash), `/var/my+app/tls.key` (`+` excluded) | **Open — the rejection.** The aggravator the Tester rested on: **the gate has no suppression affordance at all** — no inline marker, no allowlist, no baseline. In `R3-2` it declined to reject because an author could reach for a `PLACEHOLDER_MARKER`; here the only options are to change the deployment or disable the hook |
| **The exemption rates in the docstring did not reproduce as written.** Independently re-measured: 24 and 48 bytes match, **32 bytes gives exactly 0% padded** and 0.09% only with `=` stripped, because a 32-byte value ends in `=` which is outside the charset. Confirmed here before accepting it | **Fixed.** The docstring now names the unpadded method and says why the clause matters. Errs conservative, so not a security finding — but `R2-3`'s lesson was that a number must carry its method, and this repeated that defect **one round after recording it**. That is the more useful fact than the number |
| **The path rule is applied to `PRIVATE_KEY_BLOCK`, where it can only cost detection.** A PEM body is never a filesystem path, yet the value-side test filters that form too: **0.142% of naturally generated PEM first lines are exempted, about 1 in 706 private keys** | **Open, low severity.** Excluding that one form from the value-side test costs nothing. Held with everything else pending the decision |
| The elided ASN.1 prefix (`R3-2`) | **Open by agreement of both sides.** The Tester was asked whether to close it and said to leave it recorded |

**The structural argument, which is why this is a human decision and not another
patch.** Three value-side rules in three rounds: exempt every URL or path
(dropped real credentials), exempt nothing (blocked real pointers), exempt
absolute multi-segment paths (blocks relative pointers). Each was a reasonable
narrowing of the last and each was wrong in a **new** direction. The Tester's
reading, which this record adopts: value-shape classification cannot separate a
pointer from a credential, because the same string is either one depending on
what reads it. Every production secret scanner ships an allowlist or a baseline
for that reason, and this gate has none.

**`git restore .` would do nothing here** — every round of `C3` is committed, so
the remediation instrument assumes uncommitted work and finds none. Recorded as
a defect of the switch itself, in the sprint that exists to find controls that
cannot do what they claim.

**The Tester's own note on the strike position**, kept because it is the part a
later reader will want: it stated that it checked whether it was applying a
harsher bar than in earlier rounds, judged that it was not, and declined to
reject on three further findings this round that did not meet it. It named the
single question the decision turns on: **whether a relative
`GOOGLE_APPLICATION_CREDENTIALS` path is stock content.**

**F3, a fourth consecutive time**: the 455-file nucleus delta reported 0 new and
0 lost this round too, while `R4-1` was live.

### Round 5 — `APPROVED`. `C3` and `C3.2` clear the Double Gate

Five Tester rounds on one unit: reject, reject, reject, reject, approve. Every
defect raised across the four rejections is fixed and independently verified by
the gate that raised it. The gate stated it checked the approval the same way it
checked round 4's rejection, and reported two findings at full strength rather
than softening them to justify passing.

| Gate finding | Resolution |
| :--- | :--- |
| **`R5-1` — `_suppression_reason` made the scan quadratic.** It does a backwards `rfind` per surviving match and was ordered **before** the cheap `$`/`{`/`[` and `PLACEHOLDER_MARKERS` tests, so every match paid it, and on a single long line each call walks to position 0. Measured by the gate: ×4.00 per doubling where the previous code was linear, and a stock 200 KB single-line JSON export at **259 ms against 0.83 ms — a 313× regression**. No marker needed to trigger it | **Fixed, not routed.** The filter is now last, which makes it strictly cheaper as well as correct. Reproduced here before and after: growth back to ×2 per doubling, and the 200 KB export at **1.8 ms** |
| **`R5-2` — the affordance was undiscoverable at the point of failure.** The block message named only the identifier; `grep -rn "secret-scan" agents.md rules/` returned nothing; the sole document containing the string was this sprint's own `IMPLEMENTATION_PLAN.md`, which no host reads. So for the shapes deliberately left to the marker, a host was **still in the round-4 position in practice** — blocked, with no visible option but to disable the hook | **Fixed, not routed.** The remedy now travels with the refusal, and `rules/qa_and_testing.md §5` documents the marker, its mandatory reason, its line scope and the hard boundary it cannot unlock. It was the unfinished half of `C3.2`'s own argument, so routing it would have left the unit arguing against itself |
| **Found by this session, not by the gate: the waiver announcement counted markers, not suppressions.** `ALLOW_MARKER.finditer(content)` reports a waiver for any line that merely *mentions* the marker — the `IMPLEMENTATION_PLAN.md` row documenting it did exactly that. Nothing was suppressed, so nothing was unsafe; the gate simply **claimed an outcome that had not occurred** | **Fixed.** One filter chain, `_credible_findings`, is now shared by the detector and the announcer, so the two cannot disagree about what a finding is. Recorded because it is the sprint's own defect class appearing in the sprint's own remedy |

The gate's three attack results, kept because negatives are evidence too:
**`ALLOW_MARKER`** is textual rather than syntactic, so it also waives inside a
JSON string or a Markdown heading and one marker covers its whole line —
recorded as characteristics, identical to `# noqa` and `#gitleaks:allow`, since
a committer who could plant a marker in a string could simply write one
properly. A **forbidden file is not waivable**, which is the right hard
boundary. **No credential encoding can take `./`, `../` or `~/` shape** — 0 of
200,000 across base64, base64url and hex — so the zero-risk claim for that
branch is exact rather than approximate. And **`C3.2` was judged a real unit**
rather than the fourth narrowing in disguise, on the grounds that the canonical
case was fixed outright and only marginal shapes left to the marker.

**`F3` held for a fifth consecutive time**: the 455-file nucleus delta reported
0 new and 0 lost this round too, while `R5-1` and `R5-2` were both live. Five
rounds, five clean deltas, five rounds with real findings. That is the whole
case for the routed finding.

### Declared limits of `C3`, so they are not rediscovered as defects

| Limit | Why it is a limit and not a bug |
| :--- | :--- |
| YAML **block and folded scalars** (`api_key: >`), flow mappings (`auth: {api_key: …}`), and values containing spaces are not read as leaks | The value token on the key line is one character, dropped under `MIN_SECRET_LENGTH`. The highest-value case — a PEM private key — is closed by matching `-----BEGIN … PRIVATE KEY-----` directly, which is format-agnostic and covers every scalar style at once. The remainder needs a YAML parser, which is a dependency this unit does not admit (`rules/code_craft.md §4`) |
| `ENV` **continuation lines** (`ENV APP=x \` + newline + `API_KEY=…`) are not read | Multi-pair on a single line is now read. Joining continuations means rewriting the content before matching, which changes what every other form sees — a larger change than the finding warrants |
| The auditor's value character class still excludes `-` and `_` | Recorded above as its own unrouted finding. The Tester confirmed the interaction: the eight new suffixes widen *which files* are read but not *what can be seen in them*, so `sk-live-…` in a newly covered `values.yaml` is still invisible. **The green suite overstates the delivered coverage**, and that is written here rather than left implicit |

## Suspended at the token bound, a third time — session #3

`rules/token_economy.md §3.1`, measured rather than estimated:
`python3 scripts/session_cost.py --session 5990fd61-30e0-4b2a-9c64-b2458eec8ab3`

| Cycle | msgs | first turn | peak | ratio |
| :--- | ---: | ---: | ---: | ---: |
| 1 | 293 | 0 | 296,706 | unusable — no first turn recorded |
| **2** | 50 | 24,272 | 336,603 | **13.9×** |

**The hard bound was NOT crossed.** 13.9× against 15×, and the session suspends
anyway, deliberately: `C3` cost five gate rounds, so opening `C4` would cross
the bound mid-unit. A unit left half-written and un-gated is precisely what the
bound exists to prevent, and the boundary available right now is clean — both
gates approved, every unit committed, `git status --porcelain` empty, graph
rebuilt. `§3.1` prices a restart at ~22K, measured three times, against a
336K peak.

`forced: false`. This is a chosen stop at a clean boundary, not a threshold
firing — the first of the three in this sprint that is.

**Third time the bound has governed this sprint**: 16.5× (session #1, cycle 7),
15.9× (session #2, cycle 1), and 13.9× here with the next unit judged certain
to cross. `§3.1` asks for the "too tight" signal to be recorded rather than
inferred later, so: **three sessions, three stops, seven of fourteen units.**
The provenance note in that section says `n=1` and of one kind — intensive
planning, little code execution. This sprint is the other kind, heavy on code
and on gate rounds, and it stopped at the bound three times out of three. That
is the calibration datum, and it is worth more than any single unit here.

**Cycle 1's `0x` is the measurement artifact already recorded above**, not a
real reading: `session_cost.py` reports no first turn for the cycle that
precedes the first compaction. The usable figure is cycle 2's.

## Found at session start, session #4 (2026-08-22)

Nothing new. Four prior findings re-verified as still true, which is the point of
recording them: `drift_check` and the partial bridge now have three sessions of
evidence each.

| Prior finding | Re-verification this session |
| :--- | :--- |
| `detect_drift.py` fires verdict `A` on an open sprint | Exit `2`, **33 of 35** commits reported as covered by no released section. Verified all 33 are this sprint's own `#023` commits; the 2 covered are `b7f6741` (Sprint 022) and `e5b5fbd` (the `4.7.0` seal). Second firing. Session #3's human decision — record and proceed, do not reconcile — was applied unchanged rather than re-litigated |
| The nucleus `.claude/` bridge is partial | Still 11 symlinks against 13 commands; `harden`, `reconcile`, `revdoc` unlinked, `skeleton.md` still dangling. **Third session of evidence.** It bit again in the same way: `drift_check` directed this session to `/agents:reconcile`, which this repository still cannot invoke. Belongs to `C6` |
| `last_platform_probe` has no writer | Key still absent from `docs/active_state.json` after this session's `session_probe.py` run, which reached the platform section — `gh` is present and authenticated here. Unrouted |
| `docs/0_SYSTEM_OVERVIEW.md` does not exist | `ls docs/` still shows no such file. `read_ruleset` was satisfied by `agents.md` plus `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md`, as in prior sessions. Unrouted |

## Found while executing `C4`

`C4`'s roadmap entry named two defects. Executing it found a third, and the unit
committed a fourth against itself before the gates caught it.

| Finding | Where it goes |
| :--- | :--- |
| **The auditor violated the standard it enforces, and only running it revealed that.** `standardize_skill` called `mkdir()` on `scripts/` for every skill in the manifest, so a skill became executable by the act of being audited. `agents.md §3` says padding a knowledge skill with empty scaffolding is PROHIBITED noise. Measured, not inferred: the first run that reached this library wrote `scripts/__init__.py` into **11** knowledge skills and a template `README.md` into 9, reverted with `git clean`. It was invisible for as long as it was, because defect #1 meant the script could not run at all — `F-086-S3` says "the auditor does not generate a bad stub: it cannot run", and repairing the second half exposed the first | Fixed inside `C4`. The lesson is the sprint's own governing rule read forward rather than backward: *reproduce before repairing* also means **run the thing after repairing**, because a defect that needs the fix in place to appear is invisible to any amount of reading |
| **This unit deleted hand-authored governance content and its own test certified that it could not.** `skills/django-expert-3rd/SKILL.md` was treated as a generated stub because it contained the template's `(Automatic scaffolding)` sentence. It also carried three authored directives, one of them the mandate `RA-02` states (`Clause J-02: LAZY_SIGNAL_PARADIGM`). The QA gate found it with `git log -S`; nothing in the diff, the docstring or the tests recorded the loss. Restored with `git checkout --`, byte-identical to HEAD | Fixed inside `C4`. The substring licence is replaced by **byte-equality with the freshly rendered template** — the only shape that proves nobody has edited the file since this script wrote it. A substring cannot separate *generated* from *generated-then-edited*; on the single production sample it existed to judge, it was wrong 100% of the time |
| **`F-086-S3` is not closed by `C4`, and no unit could close it without a human decision first.** The vendored 247-line Django skill stayed unreachable through `skills/django-expert-3rd/`'s root, because the root file is legitimate authored content rather than a stub. Both ways to close it inside `C4` are forbidden: deleting the authored file is `agents.md §2 destructive_flags`, and copying vendor content into the framework's tree is `rules/skills_and_integrations.md §3`. Both gates ratified that reading independently | **Closed by `C4.2`**, on the human decision `C4` escalated: the three directives were relocated to `rules/django_backend_standard.md` and the root repointed by hand. The wording of this row when first written — *"cannot be closed by any unit"* — was too strong and the QA gate flagged it: what was true is that no unit could close it **unilaterally**. The distinction matters, because the first reading invites a reader to stop looking |
| **`Makefile:74`'s tree-integrity guard watches `config/ hooks/ scripts/` and not `skills/`.** It would have stayed green through the deletion above — the same failure its own comment records about `config/abandoned_branches.json` being destroyed while the suite passed. The strongest advisory either gate produced | **Unrouted.** Not `C4`'s file to edit under `jurisdictional_lock`. Deserves its own unit; the blast radius of the skill library is unwatched |
| **`scripts/verify_references.py:194` check (d) globs only `workflows/*.md` and `scripts/*.py`, so `skills/*/scripts/` is never scanned.** Measured: **25** skill scripts are invisible to the `RA-16` gate and **20** of them declare no `invoked_by`. `verify_references.py` returns exit 0 while asserting "every mechanism has an invoker", over a scan that never read them. `mass_standardizer.py`'s own declaration is therefore honest but unenforced | **Unrouted.** Same class as `RA-16`'s founding precedent, and the same shape as `last_platform_probe`: a mechanism whose declared scope is wider than its implemented scope |

## Found while executing `C4.2`

| Finding | Where it goes |
| :--- | :--- |
| **This is the repository's first tracked symlink.** Measured before claiming it: `git ls-files -s \| awk '$1=="120000"'` returned **zero** entries before `955eb5d`. A git checkout without symlink support — Windows without developer mode, or `core.symlinks=false` — materialises `skills/django-expert-3rd/SKILL.md` as a one-line text file containing `skills/SKILL.md`, and both `generate_manifest.py` and Claude Code's skill discovery would read that line as the skill. `install_claude.py:60-69` already degrades to `shutil.copytree` when symlinks are unavailable, and the QA gate verified that path dereferences correctly — but a **checkout** is not the installer, and nothing degrades there | **Unrouted.** Raised by the Tester gate. It is a new portability surface rather than a continuation of an existing one, which is why it deserves a decision rather than a note: either the framework declares a symlink-capable checkout a prerequisite, or the pointer mechanism changes |
| **The QA gate supplied a better argument for the placement than this session did, and the difference is instructive.** The session argued from `RA-02` — Django governance in `agents.md §7`. The gate identified `rules/frontend_modular_standard.md` as the controlling precedent: a **stack-specific rule context already in core `rules/`**, governing React and TSX down to `View.tsx` suffixes, which is the same class of artifact rather than an analogy. It also found that the prohibition the session had cited (`profiles/example-project/README.md`) rests on `agents.md §3 topological_order`, which governs *skills* topology and does not reach `rules/` — while the objection that **does** bind, `agents.md §4 feedback_upstream`, went unmentioned | Fixed inside `C4.2`. Recorded because the session had argued the case from the weaker precedent *against* the weaker objection, and both halves were improved by a reviewer who had not made the decision |
| **`docs/roadmaps/core/pipeline/021-030-program-queue.md:556` describes `F-086-S3` as "a 20-line stub over a 247-line vendor skill", and it was not a stub.** It was authored content that happened to contain the template's `(Automatic scaffolding)` sentence, which is exactly why `C4` mistook it and deleted it. The row itself is **correct as history** — it sits under *"Verified beforehand — 7 of 7 reproduce against `v4.4.0`"*, a version-pinned reproduction record, so editing it would falsify what was observed rather than update what is true | **Sprint closeout.** Belongs as a fourth entry under that document's own *"Three corrections reproduction produced"* section, where reproduction claims are corrected. Both gates read the table the same way independently |

## Suspended at the token bound, a fourth time — session #4

`rules/token_economy.md §3.1`: cycle 4 reached **14.5×** its first turn against a
bound of 15×. Not yet crossed. The stop is chosen on the same reading session #3
made at 13.9×: the next step is a two-gate round for `C5`, and every gate round
in this session has cost a full dispatch plus a verdict plus at least one
remediation. Peak would cross.

`forced: false`. **Four sessions, four stops, ten of fifteen units.** The
provenance note in `§3.1` says its calibration is `n=1` and of one kind. This
sprint is now four data points of the other kind — heavy on code, heavier on
gate rounds — and it has stopped at the bound every time. That remains the most
valuable thing this sprint has produced about the rule itself.

**Cycle 3's `0x` is the measurement artifact already recorded**, not a reading.

### `C5` is in the working tree, un-gated, and its content is recorded here

`git status --porcelain` will show `agents/devops_agent.md` modified. That is
deliberate and it is **not** a crash artifact. The work is also written out
below, because a working tree is not a durable record and this sprint's own
governing lesson is that an artifact living outside the repository is an
artifact already lost.

**The edit**: `agents/devops_agent.md:4` becomes
`tools: Read, Glob, Grep, Bash, Write, Edit`, plus a `Jurisdiction | write_scope`
row and a section explaining the grant. `agents.md §6`'s `devops_agent` row gains
a clause naming that jurisdiction — **that second edit is not in the tree and is
in no commit**; it was reverted so `C4.2` could commit atomically. Reproduced
verbatim here, because it existed nowhere else and would otherwise have to be
re-invented:

> \| **Subagent Roles** \| `devops_agent` \| Environment Agent. Manages venv, .env export, and Docker health. **Sole holder of `Write`/`Edit` for `scripts/` and `hooks/`** (`F-086-A1`, Sprint 023) — which gives those trees an owner without creating the implementer role the map still lacks (`F-021-A2`, declared in that profile). \|

It replaces the current row, which ends after *"Docker health."*

> [!WARNING]
> **⚠️ SUPERSEDED at `R1`. Do NOT re-apply the row above verbatim.** The QA gate
> rejected it (finding #5): the bare `scripts/` collides with
> `skills/[name]/scripts/`, which `skill_architect` forges, and with
> `token_economy_agent`'s ownership of three named scripts. **The applied,
> gate-corrected row is the `devops_agent` row live in `agents.md` §6** — find it
> by its content, which begins *"Sole holder of `Write`/`Edit` for the
> **framework-root** …"*, not by line number, which drifts on any edit above it.
> Read it there, not here. This paragraph exists because the block above tells a resuming session
> that the row "existed nowhere else and would otherwise have to be re-invented",
> which was true when session #4 wrote it and would now walk a session #6
> straight back into the rejected text. `RA-14` names exactly this: a correction
> applied where a reviewer looked while the same reference drifts uncorrected
> elsewhere in the same artifact. Found by grepping this file for the remediation's
> own terms, not by noticing it.

**What was verified before making it**, which is the part worth not re-deriving:

| Question | Measured answer |
| :--- | :--- |
| Do `Write`/`Edit` grant capability the profile lacked? | **No.** It already holds `Bash`, which writes any file through a shell redirect. `Write`/`Edit` are strictly narrower |
| Does routing writes through `Bash` keep them under a gate? | **No, the reverse.** `claude/settings.hooks.json` registers exactly one `PreToolUse` matcher, on `Bash`, and its deny list is Bash-shaped. What changes is that `Write`/`Edit` name their target, so `jurisdictional_lock`'s one-file limit becomes checkable rather than buried in a shell string |
| Is a `mechanical`/`haiku` tier holding `Write` unprecedented? | **No.** `agents/topology_mapper.md` already does |
| Does the change disturb the tier map? | **No.** `check_model_tiers.py` → exit 0, 13 profiles agree. It changes `tools:`, not `model:`/`tier:` |

**The objection a gate will raise, and the answer prepared for it**: granting
write tools appears to widen the blast radius. It does not — the widening
happened when `Bash` was granted, and this narrows how it is exercised.

**`F-021-A2` is declared, not resolved**, and the profile says so: this gives
`scripts/` and `hooks/` *an* owner without creating the implementer role the map
lacks, and a mechanical tier is not the right author for a governance gate.

## Where session #5 resumes

| | |
| :--- | :--- |
| **Next unit** | **`C5`, already written and awaiting its gates** — the edit is in the working tree and reproduced in full in the section above. Re-apply the `agents.md §6` row, then dispatch `qa_agent` and `tester_agent`. Do **not** re-derive the four verifications; they are recorded |
| **Delegation** | The human lifted it for `C5`'s QA and Tester gates in session #4, before the bound stopped the session. That lift is per-unit and was never spent, so it stands for `C5`. `C6` onwards must ask again |
| **Remaining** | `C5` (written, un-gated), `C6`, `C7`, `C8`, `C10` |
| **Highest-severity open item** | **`F8`** — a literal `.env` holding live credentials passes `hooks/on_commit.py` today. Routed, unowned, and it defeats `RA-09`. It deserves a unit before the sprint closes |

## Found at session start, session #5 (2026-08-23)

| Finding | Routing |
| :--- | :--- |
| **Three mandated commands are not invocable in this workspace.** `commands/` holds 13 files; the installed bridge `.claude/commands/agents/` holds 11 symlinks dated 20–26 July. Missing: `harden.md`, `reconcile.md`, `revdoc.md`. Dangling: `skeleton.md` → `../../../commands/skeleton.md`, which no longer exists in the source. Confirmed against this session's own available-command list, which offers neither `harden`, `reconcile` nor `revdoc` — so `start_workflow.md` `drift_check` mandates running `/agents:reconcile` on exit 2, and that command cannot be typed here. The same holds for the two protocols that open `agents.md §6`'s onboarding order | **`C6`** — this is the nucleus's own `.claude/` bridge, already declared out of scope in the plan and routed to `C6`. This is measured evidence for it. Not fixed at session start: Phase 1.5 is PROHIBITED in nucleus mode (`nucleus_neutrality`). **✅ Discharged by `C6`, and this stated reason was wrong**: `nucleus_neutrality` prohibits *structural scaffolding*, not `bridge_check`. The bridge could have been refreshed at session start; nothing prohibited it. Annotated rather than rewritten because this cell testifies to what a session believed — and that belief, held for a month across four documents, is the substance of what `C6` found |
| **`RA-16`'s guarantee holds on paper while three of its declared invokers are unreachable.** Measured, not inferred: `scripts/verify_references.py:46` puts `.claude/` in the excluded set by design ("linked `.claude` trees"), `:60` builds the corpus from `commands/` — the source — and `:200` asserts only that the string `invoked_by:` is *present* in a file. It never resolves the command that string names to a route. `verify_references.py` exits 0 against the state above | **Unrouted.** Adjacent to `C6` but a distinct question: `C6` is about whether the nucleus installs a bridge, this is about a check that cannot see the bridge either way. A candidate unit — check (d) resolving `human:/agents:x` to `commands/x.md` would have caught all four discrepancies |
| **`drift_check` returned exit 2, verdict `A`, and the verdict is fully explained by the sprint in flight.** Of the 41 commits in the range, the 2 covered are Sprint 022's merge and its `[4.7.0]` seal; the 39 uncovered are exactly the 39 commits carrying `#023`. No commit outside the open sprint is unaccounted for. The verdict cannot distinguish "sprint in flight" from "merged work never recorded" because the script has no notion of an open sprint | **Human decision at session start: proceed to handoff without reconciling**, on the measurement above. Recorded rather than left implicit — `start_workflow.md` mandates `/agents:reconcile` on any exit 2, so a future reader finds a departure from the workflow with its reason attached, not a skipped step. A candidate refinement for the same unit: teach `detect_drift.py` to read `current_sprint.id` and report commits of the open sprint separately from unaccounted ones |
| `docs/0_SYSTEM_OVERVIEW.md` still does not exist | `ls docs/` shows no such file, for the fourth session running. `read_ruleset` satisfied by `agents.md` plus `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md`, as in sessions #2–#4. Unrouted |

## `C5` gate round `R1` — both gates rejected, and they converged

Dispatched `qa_agent` and `tester_agent` under the lift the human granted at
session start. **Both returned `REJECTED`, and independently named the same
primary defect**: `agents/devops_agent.md` asserted *"the seven that hold
`Write`"* while the edit containing that sentence made the count **eight** — and
the eighth is the file making the claim. Neither gate was told the other's
finding. Convergence of two independent gates on a self-falsifying claim is the
clearest evidence this sprint has produced for keeping author and reviewer
distinct: the sentence was written, read and committed to the record by session
#4, and re-read by this session, without either seeing it.

Six blocking findings, all remediated in `R1`:

| # | Gate | Finding | Remedy applied |
| :--- | :--- | :--- | :--- |
| 1 | **both** | *"the seven that hold `Write`"* is falsified by its own edit; the four categories named also exclude the environment role the sentence sits inside | Rewritten to "the **other seven** … and this profile is an environment role — the eighth holder and still not an implementer" |
| 2 | QA | `021-030-program-queue.md:498-503` binds `C5` to a tier re-evaluation *"recorded in 023's plan as a step, not an option"*. `grep` of the plan returned **zero hits** — the step was in no row | Added to `IMPLEMENTATION_PLAN.md` with the verdict (keep `mechanical`/`haiku`) and the trigger for re-asking |
| 3 | QA | `agents.md` was outside `C5`'s declared scope; both the plan row and this file named one file while the tree modified two. `triple_lock` Lock 1 did not cover the second | Both rows now declare `agents/devops_agent.md`, `agents.md` §6 |
| 4 | QA | `RA-14`: two **live** claims contradicted — `agent_assignment.md`'s `## Unresolved` (present tense, governs the remaining units) and `021-030-program-queue.md:807-810` (the operating instruction for `C6`–`C10`) | Both patched. The practice survives; its stated **reason** changes from the role map to the delegation restriction |
| 5 | QA | *"Sole holder"* is an unqualified absolute colliding with `skill_architect` (forges `skills/[name]/scripts/`) and `token_economy_agent` (accountable owner of three named scripts, holding no `Write`) | `agents.md` §6 now says **framework-root** trees and excludes `skills/[name]/scripts/`; a `scope_boundaries` row in the profile records the `token_economy_agent` precedence |
| 6 | QA | Bare `scripts/`/`hooks/` is mode-ambiguous — it resolves to `.agents/` in nucleus mode and the host root in submodule mode, a distinction `agents.md §3 jurisdiction` treats as load-bearing | `write_scope` row now says "resolved against the framework root via `scripts/_root.py`, never the host root" |

**What the gates confirmed rather than found**, and it is worth keeping: the
deletion check the `C4` lesson mandates came back **clean** (`git diff --numstat`
→ `1 1` and `24 1`; exactly two removed lines, each a strict prefix of its
replacement), the re-applied `agents.md` row matched session #4's recorded
reproduction byte-for-byte, and all three factual assertions in the profile's new
table were verified true against `claude/settings.hooks.json`,
`hooks/on_commit.py:766` and `agents/topology_mapper.md`.

### `R1` is APPROVED by both gates — and the re-gate had to be dispatched twice

**Verdict: `C5` clears the Double Gate at `R1`.** `qa_agent` → `APPROVED`,
`tester_agent` → `APPROVED`, both against the committed tree `aa2b11d`.

**The first re-gate produced no verdict at all.** Both agents were dispatched,
worked, and **terminated on an account-level monthly spend limit mid-task** — QA
re-deriving the six-file diff, Tester about to run `docs_freshness_check.py`.
Neither approved and neither rejected. The lead session recorded that state as
un-gated rather than inferring a pass, the human re-authorized, and both were
**resumed with their context intact** rather than respawned — which cost a
fraction of a fresh dispatch and is the reason the second attempt fit inside the
remaining budget. Worth keeping as operational knowledge: a gate that dies is not
a gate that passed, and resuming beats restarting when budget is the binding
constraint.

**What each gate added beyond a verdict:**

| Gate | Contribution |
| :--- | :--- |
| QA | **Answered the tier question it died holding, and strengthened it.** It read the roadmap paragraph to its end, where this session had stopped at its middle: `021-030-program-queue.md:501-503` forbids pre-assigning a high tier as "the speculative generality `rules/code_craft.md §1` prohibits". So keeping `haiku` was not the conservative option — changing it would have **breached** the roadmap. Folded into the plan |
| QA | **Hunted the `RA-14` sibling.** The lead session fixed the verbatim row at `:451`; QA found the **imperative** form of the same trap in the session-#5 "Next unit" row and verified it is neutralized twice (the session-#6 table declares the older one spent by name, plus a dedicated `Do NOT` row). No further sibling |
| Tester | **Proved the freshness check passes for a real reason**, which was the one result it was asked not to take on trust. In a disposable worktree it deleted `IMPLEMENTATION_PLAN.md` and got `[WARN] … Phase 1 (Planning) — Principal Agent left no artifact`. The check is live, reaches this sprint's directory, and asserts existence only (`docs_freshness_check.py:416-480`), so a new section cannot trip it |
| Tester | **Re-derived the consumer set against the enlarged diff instead of reusing its own.** `verify_references.py:45` excludes `docs/roadmaps/` and `docs/sprints/` entirely, so four of the six changed files are invisible to it; nothing in `scripts/` or `hooks/` asserts structure, length or heading shape over them; and `loop_guard.py:42` reads a root-level `task_scope.md`, not the sprint one — so the file that grew by 134 lines has **no consumer at all** |
| Tester | **Argued its own §9 finding should be routed, not blocking**, on its own measurement: the bogus-tools experiment ran in a worktree at `HEAD`, **pre-`C5`**, so the gap exists identically with and without this unit. `C5` neither creates nor widens it, and *"a gate that blocks a fix because an unrelated pre-existing hole was discovered while inspecting it is demanding a feature as the price of a correction"* |

**One distinction the Tester drew and it is kept rather than smoothed over**: on
the tier verdict it records that it *found no factual error*, and says explicitly
that this is weaker than endorsing it. The endorsement is QA's, on the ground
above. Two gates agreeing is not two gates asserting the same thing.

**What the lead session had verified before the second dispatch.** Deterministic
checks only — the mechanical half of a gate and explicitly **not** a substitute
for the independent one, which is the whole point of the author/reviewer split
this sprint has paid for twice (`C2`, `C4`):

| Check | Result, exit code read with `$?` directly |
| :--- | :--- |
| Deletion check across all 6 files | **Clean.** 8 removed lines; 7 are strict prefixes of their replacement. The 8th is a genuine rewrite (`agent_assignment.md`'s `## Unresolved`) and it preserves the historical fact it carried — *"attributed to a profile that could not have performed it"* — while adding the post-`C5` state |
| Arithmetic of the new claim | **True.** 8 holders of `Write`/`Edit` in `agents/` enumerated by exact token with `TodoWrite` excluded, `devops_agent` among them. "Other seven" + "the eighth" holds |
| `check_model_tiers.py` · `verify_references.py` · `check_readme_counts.py` · `map_workflows.py --check` · `check_manifest_parity.py` · `check_absolute_paths.py` · `docs_freshness_check.py` | all **0** |
| `docs_freshness_check.py` output | Only the pre-existing `[WARN] code_containers not declared` advisory — the plan's new section does not trip the `C0` phase-artifact map |
| `make verify` | **0** — 372 passed. Unchanged from the pre-edit count, which the Tester already established means **nothing pins `C5`** |
| `RA-14` over the remediation's own prose | **Found one defect, fixed.** See the `⚠️ SUPERSEDED` warning above `## Where session #5 resumes` — the verbatim row session #4 recorded is the version the QA gate rejected, and the block containing it instructs a resuming session to re-apply it. Fixing the count in `agents.md` while that reproduction drifted is the precise failure `RA-14` describes |

**All of it is now independently confirmed.** The judgment half — whether the new
prose is sound, whether the tier basis holds, and whether the six fixes *answer*
the findings rather than touch the lines they named — was the whole mandate of
the second dispatch, and both gates returned on it. QA ruled all six answered on
substance and three exceeded the ask; Tester verified the three new factual
claims in the `scope_boundaries` row against `agents/token_economy_agent.md:4,19,20`
and `agents/skill_architect.md:3,18`, and re-ran the RA-16 mask check against the
final diff (none of the 23 executable skill names appears in any added line, so no
orphan was masked).

### Found by the `C5` gates — routed, not folded in

| Finding | Routing |
| :--- | :--- |
| **`tools:` frontmatter is entirely unvalidated, proven by experiment.** The Tester replaced the key with `tools: Nonexistent, NotATool, Frobnicate` in a disposable worktree and ran the full suite: **exit 0, 372 passed**. A profile can declare three tools that do not exist and every gate stays green. Consequence for this unit specifically: a typo (`Wrote` for `Write`) would leave the framework-root trees ownerless while `agents.md §6` asserts an owner, and nothing would notice. The same worktree also proved **no test fails if `C5` is reverted** | **Unrouted — a candidate unit.** The cheap fix is an extension of `check_model_tiers.py`, which already parses this exact frontmatter: assert `tools:` names come from a known-tool set, and that a profile declaring a `write_scope` row actually holds `Write`/`Edit`. Not folded into `C5`: it is a new mechanism with its own `RA-16` invoker, not a remediation of this one |
| **`RA-16` cannot see the installed bridge**, so three mandated commands are unreachable while `verify_references.py` exits 0 | Recorded in the session-start findings above. Same candidate unit or its own |
| `021-030-program-queue.md:597-599` states `F-086-A1` and `F-021-A2` as open with no closure marker. The **finding statement** is a record of what was found and must not be rewritten; what it lacks is a closure marker for `F-086-A1` | **`RA-05` closeout obligation**, not a `C5` blocker. Named here so the close does not have to rediscover it |
| `agents/devops_agent.md` uses "here" twice in explanatory prose, which `§1 unambiguous_action` names as prohibited | Non-blocking per the QA gate: `agents.md` itself uses explanatory "here" in `§5` and `RA-16`, so corpus precedent permits it in prose rather than in instructions. Left as-is deliberately |
| **The `token_economy_agent` precedence is recorded one-directionally.** `agents/devops_agent.md`'s new `scope_boundaries` row names it, but `agents/token_economy_agent.md:19-20` still declares it "Owns `scripts/check_model_tiers.py`…" with no reciprocal pointer | **Unrouted, and deliberately not folded into `C5`** — that file is outside this unit's declared scope, and editing it would have re-opened the QA gate's own finding #3. Worth one line when a future unit next opens it. Raised by the gate that specified the precedence rule in the first place |
| The profile's one-file `jurisdictional_lock` limit has **no enforcing mechanism** — `claude/settings.hooks.json` registers a `PreToolUse` matcher on `Bash` only, none on `Write`/`Edit`. The profile text says "check**able**", not "checked", so it is honest | Non-blocking, and not an `RA-16` violation (a profile row is not a workflow, script, skill, hook or gate). Unrouted |

## `C6` gate rounds — and a governance principle worth more than the unit

Both gates rejected at `R1` and **converged for the second time this sprint**,
independently naming the same defect: regenerating
`docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` had flipped `read_ruleset` from `read`
to **`write`**, because the added clause contained *"recorded"* and
`map_workflows.py`'s `WRITE_VERBS` matches `record` by prefix. `C6` promotes that
guide to mandated reading in the same change that put a false claim into it — and
`make verify` **cannot** catch it, because `map_workflows.py --check` compares the
file against its generator: consistency, not correctness. Green and wrong at once.
Replacing one word restored `read` and removed the guide from the diff entirely.

| Round | Gate | Blocking finding | Remedy |
| :--- | :--- | :--- | :--- |
| `R1` | both | The `read` → `write` misclassification | `recorded` → `hit`; guide regenerated and now byte-identical to `HEAD` |
| `R1` | QA | The `bridge_check` row asserted `on_init.py` automation unqualified. **Half a docstring was quoted while its other half falsified the sentence beside it** — the nucleus self-bridge installs *no hooks by design*, which is the real reason this bridge went stale for a month. Had the hook ever run, it could not have | Sentence scoped "in a host", plus a nucleus paragraph naming all three mechanisms |
| `R1` | QA | `docs/plans/README.md:46-51` held the overturned reading and **names `C6` as its owner** | Reason corrected, conclusion kept, routing discharged |
| `R2` | QA | A **fourth** live holder at `task_scope.md:501` — this session's own start-of-session routing cell, justifying an inaction with the exact proposition `C6` overturns, 444 lines from the marker at `:57` | Discharge marker with the corrected cause appended |
| `R2` | Tester | *(routed, folded in by choice)* `audit_workflow.md:18` claims the nucleus *"has no bridge"*. Already false before `C6` — but `C6` turns a **wrong-but-consistent** pair of documents into a contradictory one, and one clause now is cheaper than carrying it to closeout | Row rewritten to skip only the checks that do not apply, and to point at `bridge_check` for the one that does |

**Verdict: `APPROVED` by both gates at `R2`.**

### The classifier defect is systemic, not the one-off `R1` treated it as

Found by the Tester at `R2` while confirming nothing had drifted. It checked
**every** row of `audit_workflow.md` rather than the edited one, and reported that
`federation_audit` publishes as `write` because `release` — a `WRITE_VERB` —
prefix-matches the **noun** in *"pinned to a release tag"*. That is at `HEAD`,
predating this sprint. **A read-only audit step is already published as a
writer**, in the artifact whose own preamble calls that column *"the diagnostic
one"*.

So `R1`'s `recorded`/`record` collision was not an unlucky word choice: prefix
matching against an unanchored verb list mislabels ordinary English, and the
guide has been carrying at least one false label all along. This raises the
priority of the classifier unit already routed out of `C5`/`C6` — and it means
the fix is not "add a word to a denylist" but "stop matching nouns", which is a
behaviour change to a script and therefore its own unit with its own `RA-16`
invoker.

**The rule the QA gate stated for these calls**, which explains every routing
decision this sprint made and is worth reusing: **fold in a correction that this
unit's own change falsifies; route a new mechanism.**

### `C0` gave the plan a home and a gate, but no currency check — measured on `C0`'s own plan

Found while writing `C6`'s row into the Work table. `IMPLEMENTATION_PLAN.md` and
`task_scope.md` carry **the same table** and had drifted apart: the plan showed
`C0` as *"in flight"* and `C0.2`, `C0.3`, `C1`, `C2` as `⏳` — all five committed
and gate-approved — and **omitted `C4.2` entirely**, a unit that exists at
`955eb5d`. Six rows wrong in `triple_lock`'s **first lock**.

`C0`'s own text declares the limit that permits this: the close gate proves the
plan *"exists and is versioned"*, not that it is accurate, and
`docs_freshness_check.py` asserts `(sprint_dir / artifact).is_file()` — existence
only, as the Tester independently established in `C5`. So a plan can be present,
versioned, gated green, and misreport its own sprint.

**Synced under `RA-14` rather than routed**, and the distinction matters against
the QA gate's fold-or-route rule: this session had just patched the `Status`
field of that artifact for `C6`, and `RA-14` requires grepping the artifact in
full for *the same field* before the patch is closed. Five stale rows of the
field just touched are inside that obligation, not outside it. All eight commit
SHAs were verified to exist and their subjects matched their units before being
copied across — the plan is Lock 1, and a synced-but-unverified table would trade
a visible defect for an invisible one.

**What is routed**: that nothing detects the drift. Two artifacts holding one
table with no equality check is a mechanism-shaped gap — a candidate unit
alongside the classifier, not a `C6` fix.

**The principle, supplied by the QA gate while ruling on how `task_scope.md:57`
should be treated.** This session cited the `C5` precedent to justify annotating
rather than rewriting, and the gate accepted the outcome while rejecting the
reasoning — the distinction is worth keeping:

> `021-030-program-queue.md:597-599`, ruled untouchable in `C5`, recorded a
> **measured state of the tree**: true when written, and `C5` changed the world
> rather than the measurement. `task_scope.md:57` records an **interpretation of a
> rule that was wrong when written** — `install_nucleus_bridge()` shipped in July
> and `README.md:193` already documented the carve-out. Nothing changed to falsify
> it; `C6` discovered it had never been true. *"Superseded by events"* and
> *"wrong when written"* are different categories, and the `C5` ruling covers only
> the first.
>
> **The durable rule: correct the documents that instruct; annotate the records
> that testify.** `docs/plans/README.md` instructs, so its reason was corrected in
> place and its conclusion kept. `task_scope.md:57` and `:501` testify, so they
> carry markers — and erasing their wrong reasoning would destroy the evidence
> that the framework held a mistaken reading for a month, which **is** what `C6`
> found. A bare discharge tick would not qualify: the marker must carry the
> correction inline, or a reader can lift the wrong claim without meeting the
> right one.

**Routed to `extract_workflow` / `agents.md §7`, not applied here.** It refines
how `RA-14` is applied and is framework-class under `§4 constitutional_escalation`.
Folding a governance amendment into `C6` would be the scope expansion the QA gate
has already flagged twice in this sprint.

## `C7` gate round — APPROVED by both, and the Tester caught a staging hazard

Both gates approved on the first round. The unit moves `requirements-freeze.txt`
to `docs/audits/SKILLOPT_TRANSITIVE_CLOSURE.md`: Dependabot parses any
`requirements*.txt` as a manifest and its **alerts cannot be excluded by path**
(`.github/dependabot.yml` governs *updates*), so removing the manifest is the only
lever. Alerts were confirmed enabled — `gh api repos/:owner/:repo/vulnerability-alerts`
→ **HTTP 204**, where 404 would mean disabled — so the exposure is real rather
than hypothetical.

**The Tester's blocking precondition, and it is the best catch of the round.**
The index held `D requirements-freeze.txt` staged while the replacement sat
**untracked**. A plain `git commit` would have shipped the removal of 125 pins
with no replacement in the tree, leaving the audit record in the working
directory only — *this sprint's own founding lesson, reproduced by the unit built
to prevent that class of loss.* Staged before committing; git then recorded it as
a **rename** (`R052`) rather than a delete plus a create, which is the correct
history. It was a staging state and not a defect in the authored change, which is
why it was a precondition rather than a rejection — and one keystroke from being
the worst outcome available to the unit.

| Verification | Result |
| :--- | :--- |
| Content fidelity | **125 pins byte-for-byte, order preserved, 0 duplicates, 0 truncation** — measured element-wise against `git show HEAD:` by both gates independently |
| The 4 dropped header comments | Intended. QA traced each to where its content now lives (opening paragraph, the install-path table, `## Regenerating`), and confirmed the regeneration command lost its `> requirements-freeze.txt` redirect — *"the detail that usually drifts, and it did not"* |
| The non-claim | QA ruled it **genuinely prevents** the misreading rather than asserting it does: the callout sits *above* the pins, states a falsifiable invariant, and names what actually changed. A reader cannot reach the list without passing it |
| Is `skills/skillopt/SKILL.md` under the Documentation Veto? | **No.** Verified against the tree, not the claim: seven directories carry the `-3rd` suffix the Nomenclature Mandate requires; `skills/skillopt/` carries none, so it is a native wrapper over a vendored *package* |
| Operational consumers of the removed file | **None.** `ci.yml:30` installs only `pytest`; no Makefile target, test, hook or installer reads it; `grep "\-r requirements-freeze"` empty |
| Consumers enumerating `docs/audits/` | **None.** `check_readme_counts.py` counts five sets, none under `docs/` |
| `make verify` · `docs-freshness-check` | **0** · **0**, 372 passed, one pre-existing advisory |

### Routed out of `C7`

| Finding | Routing |
| :--- | :--- |
| `RA-06` fits the new filename loosely — `TRANSITIVE_CLOSURE` names the subject rather than a corpus document type, where the sibling `TOKEN_ECONOMY_AUDIT-…` uses `AUDIT` | **Left as-is deliberately.** The roadmap prescribes this exact filename at `:740`, so renaming it to satisfy a naming preference would breach Lock 1. The document's own `**Type**: Audit record` header supplies the metadata. Belongs to a naming pass, not here |
| **`docs/audits/THIRD_PARTY_PROVENANCE_TODO.md` carries `TODO` in its filename**, which `agents.md §1 Markers ephemeral` rejects on sight | **Unrouted, pre-existing.** Not `C7`'s defect and outside its scope. Recorded so it is not rediscovered later as a gate failure |
| `docs/roadmaps/…:531,573,617` and `CHANGELOG.md:197` still name the old path | **`RA-05` closeout obligations.** Under the instruct/testify rule these **testify** — they are the finding and its prescribed fix, and rewriting them would erase why `C7` exists |

## Suspended below the bound, a fifth time — session #5, and the first that was not forced

**`forced: false`, and unlike sessions #1-#4 this one did not reach the bound.**
Measured with `scripts/session_cost.py --json`, which `rules/token_economy.md §3.1`
requires — *"a figure without it is memory, not evidence"*:

| Cycle | Messages | First turn | Peak | Ratio |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 94 | 24,272 | 119,653 | 4.9× |
| 2 | 219 | 24,272 | 280,938 | 11.6× |
| 3 | 12 | 24,272 | 292,606 | **12.1×** |

Stopped at **12.1× of 15×**, by choice rather than by the bound: the next unit is
`C10`, a new gate script, and `C5` and `C6` cost two gate rounds each while `C3`
cost four. Starting it here would guarantee cutting it mid-round. The reasoning
sessions #3 and #4 used — price the *next* step, not the consumed budget — with
the difference that this session could stop before the bound instead of at it.

### Two calibration data points `§3.1` asks for by name

`§3.1` declares its provenance as **`n=1` and of one kind** (intensive planning,
many reads, little code execution). This session is of a third kind again — heavy
on **gate rounds**: six dispatches, five rounds, three units closed.

1. **The reset point is a per-project constant, now confirmed in a second
   session.** `§3.1` observed *"22,174 tokens, identical three times"*. This
   session: **24,272, identical three times** across three cycles. Different
   value, same phenomenon — which supports the rule's core design choice of
   measuring against the cycle's first turn rather than the session's, since that
   denominator is stable.
2. **Three units closed at 12.1× where four prior sessions closed ten units
   between them at the bound.** The bound did not bind here, which is the
   observation `§3.1` says its calibration cannot make while the hard threshold
   always fires first. Recorded as evidence the threshold is not set too tight.

## Where session #6 resumes

The table under `## Where session #5 resumes` above is **spent** — its two
instructions ("re-apply the `agents.md §6` row", "dispatch `qa_agent` and
`tester_agent`") were both executed in session #5. Read this table instead.

| | |
| :--- | :--- |
| **Next action** | **`C10`** — a new gate script (`scripts/ci_gate.py`), the last high-risk unit. It wants a fresh cycle with real budget for its rounds: `C5` and `C6` cost two rounds each and `C3` cost four. `C8` (tick closed findings on `origin/contrib/host-findings`) is the cheap alternative if budget is short |
| **Delegation** | Must be asked again. The session-#5 lifts for `C5` and `C6` are **spent** |
| **Blocked on** | Nothing. `make verify` green at 372 |
| **Two mechanism-shaped gaps routed this session**, both candidates for their own unit | (1) `map_workflows.py`'s prefix matching mislabels ordinary English — proven systemic, not a one-off, since `federation_audit` publishes as `write` off the **noun** in "a release tag". (2) `IMPLEMENTATION_PLAN.md` and `task_scope.md` carry the same Work table with **no equality check**; they had drifted by six rows before this session synced them |
| **Do NOT** | Re-apply the `agents.md §6` row reproduced under `### C5 is in the working tree` — it is the version the QA gate **rejected**. The live, corrected row is the `devops_agent` row in `agents.md` §6, identifiable by its opening *"Sole holder of `Write`/`Edit` for the **framework-root** …"* rather than by a line number. That block carries a `⚠️ SUPERSEDED` warning; heed it |
| **Remaining after `C5`** | `C6`, `C7`, `C8`, `C10` |
| **Highest-severity open item** | Unchanged: **`F8`** — a literal `.env` holding live credentials passes `hooks/on_commit.py` today. Routed, unowned, defeats `RA-09`. It deserves a unit before the sprint closes |
| **Newly unrouted, from session #5** | `tools:` frontmatter is unvalidated (three fake tool names keep the suite green, proven by the Tester); `RA-16` cannot see the installed bridge, so `/agents:reconcile`, `/agents:harden` and `/agents:revdoc` are unreachable here while `verify_references.py` exits 0 |

## Declared deviation — delegation

Unchanged from `022`: the session configuration forbids spawning subagents
unless the human asks. Reported before Phase 1 in session #1 and authorised.

**Session #2 reported the same conflict at the same point and the human lifted
it for both gates**, so `C2`'s remaining rounds were gated by dispatched
`qa_agent` and `tester_agent`, not by their author. The lift is per-session and
per-unit, not standing: `C3` onwards must ask again.

**Session #3 asked again, as that sentence requires, and the human lifted it on
the same terms: QA and Tester gates only, for `C3`.** Authoring stays with this
session — `F-021-A2` leaves no choice for `scripts/`, and the human declined the
wider lift so that author and reviewer stay distinct on a unit that handles
secrets. `C4` onwards must ask again. Recording it because the
distinction is what `agent_assignment.md` exists to keep honest — five units of
this sprint were written *and* gated by the same session, and `C2` is the one
where that is not true.

**Session #4 asked again and the human lifted it on the same terms: QA and
Tester gates only, for `C4`.** `C5` onwards must ask again.

**Session #5 asked again and the human lifted it on the same terms: QA and
Tester gates only, for `C5`.** `C6` onwards must ask again.

**That lift is now spent.** Both agents were dispatched under it, both returned
findings, both were resumed for the re-gate, and both died on an account-level
monthly spend limit mid-work. A lift is spent by being used, not by producing a
verdict — so `C5`'s re-gate needs a fresh one, and `C6` onwards needs one
regardless. **The delegation conflict `start_workflow.md` requires reporting is
therefore live again**, and for a new reason: not a session policy this time, but
an external quota. It is reported rather than resolved by the session
substituting itself for the gates, which is the precise failure that workflow
step was written against.

Session #4's handoff note above records that its own lift "was never spent, so
it stands for `C5`". **This session asked anyway**, and the reason belongs here
rather than in a session that will not be read again: a lift is granted to a
session, and session #4 ended. A record asserting that a permission outlives the
session that received it is the record deciding a question reserved to the
human. The answer was the same either way, which is precisely why asking cost
nothing — the case where it would have mattered is the one where it was not.

This is the unit that shows what the distinction is worth, and it is worth
recording in one place rather than being inferred from the round count. `C4`
was rejected **three times**: the Tester found two defects that had no test and
a false measurement recorded in the deliverable's own docstring; the QA gate
found that the unit had **deleted hand-authored governance content** — three
directives including the mandate `RA-02` states — and that the test written to
forbid exactly that deletion passed only because its fixture avoided the case.
Two further rounds were `RA-14` propagation: a claim corrected where a reviewer
had pointed, left standing three lines below and in two other files.

None of it was reachable by its author. The deletion was found with `git log -S`
against a file the author had read and not registered; the false docstring count
was found by re-measuring rather than by re-reading. Six units of this sprint
were written *and* gated by the same session; `C2` and `C4` are the two where
that is not true, and `C4` is the one that would have shipped a destructive
regression without it.

`F-021-A2` makes self-execution unavoidable for `scripts/` regardless — no
profile in `agents/` holds `Write` for that tree, which is `C5`'s subject.

## Isolation

Single-session, single-branch. `no_interference` has no competing subtask.
