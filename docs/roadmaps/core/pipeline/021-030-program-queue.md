---
description: "Program queue — the nucleus sprint backlog, 021 to 030, with the measurements that ordered it"
status: "IN_PROGRESS"
version: 1.0.0
---

# Roadmap: Program Queue 021-030

## Status

- **Strategy Lock:** `OPEN`
- **Delivered:** `024` and `025` (`v4.5.0`), `021` (`v4.6.0`), `022` (`v4.7.0`), `023` (`v4.8.0`), `026` (`v4.9.0`, PR #50), `027` (`v4.10.0`, PR #55), `028` (`v4.11.0`, PR #57)
- **Next:** `029` (`documentation-truth`). `028` (`self-improvement-unblock`) **deployed** `v4.11.0` (PR #57 + seal #58, 2026-08-25). `F-026-A1` / `F-026-A3` closed in 027; `F-021-A2` / `F-026-A2` remain open. **`F-093-G1` opened 2026-08-25** (Double-Gate has no severity class) — carried, not a 029/030 unit; first sprint of the next program (`031` `gate-verdict-classes`)
- **Reconciled 2026-08-25** from `9da899c..84201d2`: the post-release seal record (SPRINT_LOG, this Status block, guide audit SHA after PR #57/#58) landed after tag `v4.11.0` with an empty `[Unreleased]`. Ledger entry under `CHANGELOG.md` `[Unreleased]`.
- **Origin:** drafted in an IDE planning mode across one long session, then migrated
  into this repository. That migration is the point: the same session opened with a
  host having lost an approved plan to ephemeral storage, and this document was
  itself being written outside version control while describing the fix for that.
  It could not land until Sprint `024` removed the `.gitignore` exclusion that made
  the nucleus unable to version its own records.

## What this document is

A **program roadmap**, not an Implementation Plan. `agents.md §0` places multi-sprint
material in `roadmaps/` (Future) and execution in `sprints/` (History), so each sprint
extracts its own `IMPLEMENTATION_PLAN.md` at its Phase 1 — which is when the pipeline
says a plan is written.

**IDs are labels, not positions.** Renumbering was the single largest source of defects
in this document's own audit: 15 of 23, because prose references ("the 022 work") escape
every mechanical replacement pass. So when execution order diverges from numeric order,
the order changes and the IDs do not. `024` ran first; `030` is a reassignment, not a
shift.

**Design here, artifacts just in time.** Seven of these sprints are proposals. Writing
nine sets of sprint artifacts now would document a sequence that measurement will
change — and it has, twice: `021` was created mid-session when transcript data showed
session length dominates cost, and `024` was promoted to first when its defect blocked
the program's own opening command.

## The queue

| Order | Sprint | Title | Why here |
| :--- | :--- | :--- | :--- |
| ✅ | **024** | `close-machinery-verdicts` | Delivered `v4.5.0` (PR #40). Three close-machinery controls returned the wrong verdict; the first blocked this program's opening command |
| ✅ | **025** | `jurisdiction` | Delivered `v4.5.0` (PR #41). The rule that a host session never dirties the submodule became a mechanism instead of a sentence |
| ✅ | **021** | `cost-instrumentation` | Delivered `v4.6.0` (PR #44). **A context cycle climbs to 45× its first turn, and compaction resets the axis without reducing the area.** Bounding the climb yields ~50%, tiering ~40% — and without a meter nothing else is measurable |
| ✅ | **022** | `model-tiering` | Delivered `v4.7.0` (PR #45). **Makes everything after it cheaper.** Doing it last means paying the top tier during the two longest sprints |
| ✅ | **023** | `upstream-findings` | Delivered `v4.8.0` (PR #49). **All fourteen units delivered and gate-approved**; sealed 2026-08-24, deployed the same day. `C8`'s deliverable merged separately as PR #48. Its merge gate found a CodeQL alert on `hooks/on_commit.py` — read, verified a false positive, dismissed with its proof — and three siblings on `main` that no one has read; those are in `CHANGELOG.md` under `[4.8.0]` `Known open`. Seven framework-class findings a host reported and could not patch, plus the Implementation Plan's missing location, plus two gates that answered when they did not know |
| ✅ | **026** | `tool-portability` (Cursor) | Delivered `v4.9.0` (PR #50). Migration Gate `M1`–`M7` passed; A3.r affirmed indistinguishability after A3.1 absorbed the `.mdc` probe receipt. Depends on the artifact registry (`C0.2` of `023`) |
| ✅ | **027** | `autonomy-posture` | Deployed `v4.10.0` (PR #55, seal #56, 2026-08-25). Portable Memory/Drift scripts + Claude template (`auto`/`hard_deny`/sandbox/hooks); `F-026-A1` / `F-026-A3` closed |
| ✅ | **028** | `self-improvement-unblock` | Deployed `v4.11.0` (PR #57 + seal #58, 2026-08-25). Host-side agent destinations, `--profile-path`, `routing_class` |
| **1st** | **029** | `documentation-truth` | **Closes this queue.** The sprints above add scripts and config registries that no verified README figure counts. `F-093-G1` is **not** a unit (carried → `031`) |
| **2nd** | **030** | `token-economy-enforcement` | Reassigned from `025`, which shipped as `jurisdiction`. The auditor with no body, and the consumption-based trigger |

### Carried out of `023` — routed to a hotfix, scheduled after `026`

**`F8` / `F-023-S4` — a literal `.env` holding live credentials passes
`hooks/on_commit.py`, defeating `RA-09 SECRET_SOVEREIGNTY`.** Written here rather
than left in a sprint record because that is precisely how it has been lost
before: it has now survived **four** sessions as *routed, unowned*, which is the
pattern `023`'s own `Context` names as the original loss this program exists to
repair. It is the highest-severity open item this program carries.

**Disposition, decided 2026-08-24: `RA-03 HOTFIX_FLAT`, executed after `026`.**
Not a sprint unit. `026`–`030` are themed and none of them is a secret gate, so
slotting it into `tool-portability` would be the same category error as `C3`
accepting it as a rider — and opening `031` for it contradicts `029`, which
closes this queue. `RA-03` is the route the framework already has for a defect
that fits no sprint, and it is `RA-06`'s sanctioned naming exception.

**Why this was not obvious for four sessions.** It was treated as a sprint unit
throughout, so every session asked *which sprint* and none asked *whether a
sprint*. The question that resolved it took one exchange once it was put.

**Destination**: `docs/hotfixes/[H-ID]-secrets.md`, from
`docs/standards/templates/HOTFIX_TEMPLATE.md`. The measurement, the two
mechanisms, the repair hazard and both fixture traps below transfer verbatim —
this section is the hotfix's source material, not a summary of it.

**Ordering is deliberate and is the human's call, recorded with its cost.**
`RA-03` exists for emergency speed, and scheduling a hotfix *behind* a full sprint
is a departure from that. It is taken knowingly: `026` is already unblocked by
`C0.2`, and interleaving a secret-gate repair into a portability sprint is what
`C3` and this very finding's history argue against. **The cost of the departure**:
the gate stays open across `026`, so any host committing a literal `.env` in that
window is unprotected by `hooks/on_commit.py` and protected only by
`.gitignore`. Whoever opens `026` should read this paragraph before deciding the
order still holds.

| | |
| :--- | :--- |
| **Files** | `hooks/on_commit.py`, `tests/` |
| **Risk** | **High** — a secret gate. Same class as `023`'s `C3`, which took four rounds and a mid-unit remediation halt |
| **Owner** | `devops_agent` ruleset (`hooks/` is its tree per `agents.md §6`, `F-086-A1`) |
| **Reproduces** | Measured on the repaired tree at `023` session #7, after `C3` and `C3.2` landed |

**Two independent mechanisms, and a file need only beat one.** Both were
re-measured rather than carried from the record:

| # | Mechanism | Evidence |
| :--- | :--- | :--- |
| 1 | The forbidden-extension branch never fires | `Path(".env").suffix` is `''`, not `".env"`. `.env.production` is worse — its suffix is `".production"`. `prod.env` **is** blocked, which is the sharpest demonstration: the gate catches the filename nobody uses and misses the three that are used |
| 2 | **Form selection**, not quoting | `secret_forms_for(Path('.env'))` returns `SECRET_ASSIGNMENT`, `QUERY_STRING_SECRET`, `PRIVATE_KEY_BLOCK`. Only `SECRET_ASSIGNMENT` addresses `NAME=value`, and it is the one form of five requiring a quoted value. `YAML_SECRET` and `DOCKERFILE_SECRET` accept unquoted values **only in their own shapes** (`key: value`, `ENV`/`ARG`) and are never selected for a `.env` |

**Do not repair on the obvious diagnosis.** *"The patterns require quotes"* is
**false** — three of the four accept unquoted values. Repairing on it adds
quote-optionality to three patterns that already have it and ships the bug. This
is recorded because the finding's own upstream entry stated it that way for one
round before a gate measured it.

**Scope note that follows from the measurement, not from the report.** The
unquoted `NAME=value` shape is missed in **every** file type, not only `.env` —
`settings.py`, `app.yml` and `Dockerfile` all return no finding against a bare
`API_KEY=<value>`. So the fix is two changes: match `.env` and its variants **by
name** (a suffix test structurally cannot see a filename that begins with its own
dot — `C3` already taught the auditor this for `Dockerfile`), and add a
`NAME=value` form with an end-of-line terminator to the set selected for every
file type.

**Two traps when writing the tests, in opposite directions.** A value that is a
documented placeholder is correctly rejected — AWS's own `…EXAMPLEKEY` returns
nothing quoted *or* unquoted — so a fixture using one produces a false negative
that looks like the finding. And a PEM block or a URL query secret **is** caught
in a `.env`, so a fixture using either produces a blocked commit that looks like
the finding failing to reproduce. A gate reviewing this unit hit the second trap
with a low-entropy PEM fixture and retracted the finding itself; both traps are
recorded because `023` shows this unit's tests are where it will be decided.

**Provenance.** Found end to end by a dispatched `tester_agent` while gating
`023`'s `C3`, and correctly refused as a rider on that unit — `C3`'s declared
scope was the file list and three named alternations, and this is neither. The
refusal was right and is not the reason it was lost; being routed without an
owner is.

---

### Carried — `F-093-G1`, after this queue

**`F-093-G1` — the Double-Gate has no severity class, so a round cap cannot fire.**
Reported by a host 2026-08-25. Full entry: `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md`
under *Reported by a host*. Reproduced against `84201d2` before this line was
written: `rules/qa_and_testing.md` §4 still has no named verdict set;
`rejection_trigger` on both gate profiles is a binary bounce; the Sprint 023 `C6`
sentence (*correct the documents that instruct; annotate the records that testify*)
resolves only in `docs/sprints/023-core-pipeline/task_scope.md` (lines 714 and 817),
not in `agents.md` §7 and not in `rules/qa_and_testing.md`.

**Not a unit of `029` (`documentation-truth`) and not a unit of `030`
(`token-economy-enforcement`).** Folding it into either is the same category
error as carrying `F-023-S4` as a rider on a themed sprint. It is also **not**
`RA-03`: this is a three-verdict design for the gates, not an emergency secret
patch, and remediation's workspace-nuke is the wrong instrument for a stale
comment.

**Do not encode "max N rounds" as the fix.** The reporting host already had N=2
and it did not fire, because every documentary nit was classified as charter.

**Destination.** First sprint of the next program: **`031` (`gate-verdict-classes`)**.
`029` still closes *this* queue (IDs are labels, not a ban on a later program).
The Implementation Plan for `031` is written at that sprint's Phase 1 from this
section and from the findings entry — not now.

| | |
| :--- | :--- |
| **Files (when 031 extracts)** | `rules/qa_and_testing.md` §4, `agents/qa_agent.md`, `agents/tester_agent.md`, `workflows/pipeline_workflow.md` Phase 7 |
| **Risk** | **High** — changes what a gate may reject; every host sprint runs Phase 7 |
| **Owner** | `qa_agent` / `tester_agent` rulesets emit; `governance_learner` authors the rule. No implementer role (`F-021-A2`) |
| **Reproduces** | Commands in the `F-093-G1` findings entry, against `84201d2` |

---

# Sprint 021 — `cost-instrumentation`

Build the cost meter and bound session length, which is the dominant driver.

**Branch:** `ai-sprint/021`

## The measurement that ordered the queue

Claude Code transcripts (`~/.claude/projects/*/*.jsonl`) record `usage` per message
**with the model**. Measured over one real 400-message session in this repository:

| Concept | Tokens | At list price | Share |
| :--- | ---: | ---: | ---: |
| `cache_read` | 108,632,261 | $54.32 | **65%** |
| `output` | 626,524 | $15.66 | 19% |
| `cache_write` | 2,183,787 | $13.65 | 16% |
| uncached `input` | 912 | $0.00 | ~0% |

**And cost grows steeply within a context cycle — but the session is a sawtooth, not a ramp.**

> **Correction, Sprint 021.** An earlier version of this table reported session quartiles of
> 7% / 15% / 23% / 54% and called the growth monotonic. **That measurement was taken over the
> first 400 messages of the drafting session, which fell entirely inside its first context
> cycle**, before any reset. Re-measured over all 1,070 messages the quartiles are *not*
> monotonic — 157K / 681K / 245K / 485K — because the session was compacted four times. The
> quartile figures were real; the scope they came from was not the one declared. Recorded as the
> fifth instance of program risk `J6`, and the most expensive: this figure ordered the queue.

Four context cycles, segmented by `cache_read` drops greater than 50% from above 100K:

| Cycle | Messages | First turn | Peak | Ratio | `cache_read` |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 414 | 22,174 | 849,060 | **38×** | 123,791,322 |
| 2 | 113 | 22,174 | 995,197 | **45×** | 99,489,407 |
| 3 | 267 | 25,833 | 361,337 | 14× | 64,036,103 |
| 4 | 282 | 22,174 | 630,886 | **28×** | 136,030,710 |

**Three findings the corrected shape produces, none available from the quartile view:**

1. **The reset point is 22,174 tokens, identical three times.** That is the fixed session-start
   cost, and it turns the break-even figure from an estimate into an observed constant.
2. **Compaction is not a cost control.** Four resets happened and the session still spent 423M
   `cache_read`. Cycle 2 proves it: **113 messages cost 99.5M**, nearly as much as cycle 1's 414,
   because it climbed to 995K. **Cost tracks peak height, not message count.**
3. **The hard threshold would have fired in 3 of the 4 cycles** — the calibration holds, measured
   per cycle rather than per session. Without that change the ratio collapses after the first
   reset and the bound never fires again.

**The conclusion that reordered the queue still stands, better supported:** the driver is neither
the model nor the cache — the cache performs almost perfectly. It is **how high a context cycle
is allowed to climb**, and total cost is the area under the sawtooth. Compaction resets the x
axis without reducing that area. The two symptoms in the usage report (*95% from sessions active
8+ hours*, *90% above 150k context*) are this one phenomenon measured twice.

| Lever | Estimated reduction |
| :--- | ---: |
| Model tiering (Sprint 022) | ~40% on the model dimension — **estimated**, under an unverified assumption of uniform token distribution across roles |
| Splitting the session in two | **~50%** |
| Splitting in four | **~75%** |

## Work

| # | Action | File |
| :--- | :--- | :--- |
| M1 | **The meter**: aggregate tokens per model from transcripts, broken down by session quartile. Zero network, zero credentials, zero dependencies | `scripts/session_cost.py` (new) |
| M2 | **Report tokens, not dollars.** The per-family price ratio is born with `config/model_tiers.json` in Sprint 022, which is what needs it to compare families. Tokens are complete and useful without any price | — |
| M3 | **A declared, calibrated session bound** | `rules/token_economy.md`, `rules/loop_governance.md` |
| M4 | The start probe reports the previous session's cost and warns when it exceeded the bound | `scripts/session_probe.py` |
| M5 | **`plansDirectory` pointing at the repository** — one configuration line that moves the plan out of `~/.claude/plans/` and into the tree. Advanced from Sprint 027 by the audit: cheapest action in the program, and it solves today the problem that created it. It does not replace `C0`: neither Cursor nor the close gate reads that setting | `.claude/settings.json` (template in `claude/settings.hooks.json`) |
| M6 | **The anchor learns to represent "session closed, sprint open"** — it cannot today, and the bound is exactly what produces that state | `scripts/session_state.py`, `workflows/start_workflow.md`, `workflows/close_workflow.md` |

## Calibrating the bound

**Unit: ratio against the first turn of the current context CYCLE** — not of the session. A session is a sawtooth: after a compaction the reference resets, and measuring against the session's first turn would collapse the ratio and stop the bound firing for the rest of the session. Cycles are segmented from the transcript itself by a `cache_read` drop greater than 50% from above 100K.
Self-calibrating per project: a large repository starts with more base context, but "10×
your first turn" means the same everywhere, and nothing has to be configured per host.

**Calibrated on marginal cost, not cumulative.** Cumulative is sunk: knowing you have
spent $84 says nothing about whether to continue. What decides is the cost of the **next**
turn, and once a turn costs 800K of `cache_read`, every turn after it costs at least that.

| Threshold | Trigger | Action |
| :--- | :--- | :--- |
| **Soft** | turn > **5×** the first | The probe suggests closing at the next commit boundary |
| **Hard** | turn > **15×** the first | No new work starts. If the sprint is complete, close; if not, **suspend** (`M6`) and continue in a fresh session |

**Measured break-even:** restarting costs **at least** ~22K tokens (the first turn of the
measured session). That is a lower bound — it excludes the human reorienting and the agent
re-reading the plan and anchor. Measured cycle peaks reached 849K, 995K, 361K and 631K — **up to 45× above break-even**.
The data says the bound must be more aggressive than intuition suggests. With those
thresholds the soft one would have fired around message ~120 and the hard one around ~250;
the real session reached **37×**.

### Provisional, with a revision mechanism that does not depend on anyone remembering

**Declared provenance: n=1**, and of a specific kind — intensive planning, many reads, no
code execution. A file-editing sprint will have a different curve.

`session_cost.py` records two numbers per sprint and their comparison is the signal:

| Signal | Reading | Correction |
| :--- | :--- | :--- |
| The hard threshold fires **well before** the sprint's natural close, repeatedly | Too tight: it forces artificial cuts | Raise it |
| The sprint closes without the soft threshold ever firing | Too loose: it is measuring nothing | Lower it |

**Correction from the audit — the bound destroyed the data that calibrates it.** If the
hard threshold binds, the sprint **always** closes at the bound and the natural close is
never observed: the comparison cancels itself. Resolved with two changes:

- **The soft threshold is purely observational** during the first sprints: it records the
  ratio and does not act, so the distribution of natural closes accumulates uncontaminated.
- **The hard one records its own intervention**: when it forces a close, `session_cost.py`
  notes `forced: true` and **whether work remained unfinished in `task_scope.md`**. A forced
  close with pending work is the "too tight" signal; a forced close on a complete sprint is not.

The proxy replaces the impossible observation: not *where it would have closed*, but whether
closing there **broke something**. And with `M6`, a sprint that took three sessions is
recorded as such (`session_count`) instead of looking like three sprints.

### The ladder: compact → suspend → close the sprint

Compaction prunes without losing the session and is the cheap rung. **The bound does not
cut mid-task**: it fires at the nearest commit boundary. If that boundary is the end of the
sprint, close; if not, **suspend** — the rung that does not exist today. A threshold that
interrupts a task half-done trades cost for rework, which is the trade this whole program avoids.

## The continuity contract — `M6`

**The anchor cannot represent the state the bound produces.** Verified in
`scripts/session_state.py`: exactly two states, `IN_PROGRESS` and `CLOSED_SUCCESSFULLY`,
and neither means "the session ended, the sprint continues". Two measured consequences:

| Defect | Effect |
| :--- | :--- |
| `release()` **always** writes `last_close_commit` | An intermediate session calling it sets a false baseline, and `detect_drift.py` then treats everything after as conformant |
| `claim()` exits `2` and demands `--takeover` for another UID | Its own comment says a live session and a dead one *"look identical from here"*. Session 2 of a sprint would have to declare itself crash recovery |

**A planned handoff and a crash would be indistinguishable** — the failure mode Phase 019
removed one level down, reappearing one level up the moment the bound exists.

### The missing state

| State | Means | Writes `last_close_commit` |
| :--- | :--- | :--- |
| `IN_PROGRESS` | Session live, sprint open | No |
| **`SUSPENDED`** *(new)* | **Session closed, sprint open** | **No** — the baseline belongs to the sprint close, not the session close |
| `CLOSED_SUCCESSFULLY` | Sprint sealed | Yes |

| # | Action |
| :--- | :--- |
| M6.1 | `session_state.py suspend` — new subcommand: sets `SUSPENDED`, stamps `end_time`, **leaves `last_close_commit` untouched**. Its declared invoker (`RA-16`) is `M3`'s hard threshold. `close_workflow.md` `state_sync` keeps `release` unchanged and **declares the asymmetry**: `release` seals the sprint, `suspend` closes the session |
| M6.2 | `claim()` treats `SUSPENDED` as free: resuming is not a collision and needs no `--takeover`. Increments the sprint's `session_count`, the datum `session_cost.py` needs to know how many sessions a sprint took |
| M6.3 | The anchor gains `resume_pointer`: last completed pipeline phase and next expected artifact, **derived from `config/artifact_registry.json`** (`C0.2` of 023), not hand-maintained. Until then it holds the last commit on `ai-sprint/[ID]` — degraded but real, and declared as such |
| M6.4 | `start_workflow.md` Phase 1: on `SUSPENDED` the session **resumes** — reads plan, `task_scope.md` and `resume_pointer` — instead of aborting. Stated there, beside the collision guard |

### What a cold session reads, in any tool

Eight artifacts, all versioned in git, each answering **one** question. Counts at a declared,
reproducible scope: `grep -rho <name> agents.md rules workflows agents scripts`.

| Artifact | Question it answers | Times named |
| :--- | :--- | ---: |
| `docs/active_state.json` | Which sprint, which layer, which commit sealed the last close, which gaps are accepted | 47 |
| `task_scope.md` | Which files, which operation, which status — and who (`R6`) | 18 |
| `SPRINT_LOG.md` | What each gate rejected and in which round | 1 |
| `ROADMAP.md` | What phases the sprint planned | 1 |
| `IMPLEMENTATION_PLAN.md` | **What was decided and why** | **0** → `C0` |
| `agent_assignment.md` · `skill_assignment.md` | Which role and skill each step carries | **0** → `C0.2` |
| `PHASE_REGISTER.md` | Which phases already ran | **0** → `C0.2` |
| `git log ai-sprint/[ID]` | What was committed, under which concern | n/a — it is git |

**Four of the eight are named zero times and two just once.** The contrast with
`active_state.json` (47) is the diagnosis: the anchor is over-specified and the rest of the
continuity substrate is not. That is why `C0.2` is not only the portability piece — it is
what makes continuity *enforceable* rather than conventional.

**What makes it tool-agnostic** is `C0.2`'s principle: each phase is defined by **the artifact
it leaves**, not by the agent that produces it. A gate asking *"does `task_scope.md` exist with
Phase 4's content?"* runs under Claude Code, under Cursor and from a bare terminal. One asking
*"was `rule_validator` invoked?"* runs only where that primitive exists. The enforcement layer
is already git-native: Conventional Commits, sprint suffix, secret scanner and test gate are
git hooks.

| Where it breaks today | Closed by |
| :--- | :--- |
| The session UID comes from the Claude Code harness | `P8` (026) |
| The plan lives in `~/.claude/plans/`, outside the tree | `M5` (021) + `C0` (023) |
| `docs/0_SYSTEM_OVERVIEW.md` — a mandatory entry point — does not exist in the nucleus | `C6` (023) |

**What does not persist, declared:** the conversation. What survives is the decision and its
reason, not the deliberation that produced it. That is why `C0` requires the plan to say
**why** and not only what — a plan listing only steps forces the next session to re-derive the
reasoning, which is the spend this sprint measures.

### Amendment to `rules/loop_governance.md`

That rule declared its token budget **explicitly advisory**, with this reason written down:
*"no agent reads its own spend reliably, and making it binding would force a field nobody can
fill truthfully"*.

**That reason stops being true with the meter.** Spend is read from the transcript, not
self-declared. The rule is amended to record that the premise changed and that the session
bound **is** binding, precisely because its datum no longer depends on an agent estimating it.
Leaving the old justification standing while the fact changed is the drift `RA-14` pursues.

## Why the meter precedes the bound

Without it, `M3`'s bound would be an invented number and Sprint 022's tier re-evaluation would
have nothing to compare against. **The instrument precedes the rule** — the same reason
`hooks/on_commit.py` was calibrated before being wired in.

## Tests

| Check | Must fail against the current tree |
| :--- | :--- |
| `session_cost.py` over a test transcript returns totals per model and per quartile | **Yes** — it does not exist |
| Over a transcript with no `usage` field, it **says it cannot measure** instead of returning zero | **Yes** — a silent zero reads as "free" |
| The meter reports tokens per model without depending on any price | **Yes** |
| `M3`'s bound is machine-checkable: ratio against the first turn **of the current cycle**, 5×/15× thresholds | **Yes** |
| `session_cost.py` records, per sprint, the ratio at which the bound fired and the ratio at the natural close | **Yes** |
| `rules/loop_governance.md` records that its "advisory budget" premise changed | **Yes** |
| `suspend` sets `SUSPENDED` and **leaves `last_close_commit` intact** — the test compares the field before and after | **Yes** |
| `claim` with another UID over `SUSPENDED` returns `0` without `--takeover`; over `IN_PROGRESS` it still returns `2` | **Yes** on the first half, **No** on the second — the second is the regression to protect |
| After `suspend`, `detect_drift.py` **still sees the drift**: claim→commit→suspend does not launder unrecorded work | **Yes** |
| `release` (sprint close) still writes `last_close_commit` | No — regression to protect |

**Commits:**
1. `feat(scripts): measure session cost from transcripts already on disk #021`
2. `feat(rules): a session length bound the meter can actually enforce #021`
3. `feat(state): a session can end without sealing the sprint it was working on #021`

**Out of scope:** changing how Claude Code manages its context window — not the framework's.
The bound acts on what the protocol does control: **when to close a sprint and open another**.

---

# Sprint 022 — `model-tiering`

Adopt upstream finding `#12`: every profile in `agents/` declares its model tier.

**Branch:** `ai-sprint/022`

## Why

Usage reports attribute **100% of spend to subagent-heavy sessions**. `agents.md §6` mandates
8 roles per pipeline pass, each with its own context, and **0 of 13 profiles declares `model:`**
— so all of them run at the session's top tier, deterministic ones included.
`rules/token_economy.md §2` governs *what a subagent's prompt contains*; nothing governs which
model it runs on.

| Check | Result |
| :--- | :--- |
| Profiles with `model:` | **0 of 13** |
| Frontmatter shape | `name` / `description` / `tools` — `model:` goes after `tools:` |
| Bridge propagation | `.claude/agents/*.md` are **symlinks** to `agents/*.md`. **No bridge reinstall required** |

## Assignment — two dimensions, not one

**Correction to the initial design:** tiering by model alone was half of it. `effort`
(`low`/`medium`/`high`/`xhigh`/`max`) is the second lever, and the reference is explicit about
Opus 5: *"low and medium punch above their weight — high quality at a fraction of the tokens
and latency"*. The Agent tool accepts `effort` per call.

**Prices verified against the authoritative reference** (cached 2026-06-24), not from memory:

| Model | Exact ID | Context | Input $/1M | Output $/1M | Ratio vs Haiku |
| :--- | :--- | :--- | ---: | ---: | ---: |
| Claude Fable 5 | `claude-fable-5` | 1M | $10.00 | $50.00 | 10× |
| Claude Opus 5 | `claude-opus-5` | 1M | $5.00 | $25.00 | 5× |
| Claude Sonnet 5 | `claude-sonnet-5` | 1M | $3.00 | $15.00 | 3× |
| Claude Haiku 4.5 | `claude-haiku-4-5` | **200K** | $1.00 | $5.00 | 1× |

**Tiers are named by role class, not by rank.** "Top/Mid/Low" ages with the catalogue;
"gate/author/mechanical" says what the role does and survives a lineup change.

| Tier | Profiles | Claude Code | Basis |
| :--- | :--- | :--- | :--- |
| **`gate`** | `qa_agent`, `tester_agent`, `principal_agent` | `opus` + effort `high` | Adversarial and planning. They produce findings nothing else produces |
| **`author`** | `orchestrator`, `rule_validator`, `skill_architect`, `doc_orchestrator`, `agent_orchestrator`, `governance_learner`, `token_economy_agent` | `sonnet` + effort `medium` | Structured authorship against a stated rule; downstream gates catch their errors |
| **`mechanical`** | `devops_agent`, `git_sync_agent`, `topology_mapper` | `haiku` + effort `low` | Deterministic, verifiable results. A wrong answer fails at the next command |

**Gates stay at the top, and that is not negotiable** (under Cursor "top" means something
else — see `Sprint 026`). Across four consecutive host sprints, *every* central defect was
found by a gate and nothing else, and several had already survived their author's own
verification. Each was a control reporting clean because of *how it ran*, not what it checked
— the failure a cheaper reviewer is least able to catch, because catching it requires
distrusting a green.

### Three declared constraints

| Constraint | Consequence |
| :--- | :--- |
| **Haiku 4.5 has 200K context**, alone among the four without 1M | The `mechanical` tier inherits that ceiling. Acceptable for deterministic work; a role in that tier handed a large context fails, and that must be known in advance |
| **Fable 5 costs twice Opus** ($10/$50 vs $5/$25) and requires 30-day retention (does not work under ZDR) | **Explicitly excluded.** It is the most capable model, which invites promoting it to the gates; at 2× the cost and with a retention requirement, it does not enter without a human decision of its own |
| **Sonnet 5 carries introductory pricing** $2/$10 through 2026-08-31 | The `author` tier is cheaper today than it will be. Take the cost baseline **after** that date, or compare against list price |

### An alternative the reference opens, and that must be measured

| Option | Input cost | The bet |
| :--- | ---: | :--- |
| `sonnet` + `medium` | $3/1M | Cheaper model at medium effort |
| `opus` + `low` | $5/1M | More capable model at low effort — the reference states `low`/`medium` on Opus 5 punch above their weight |

The plan adopts the first and **declares the second as the first trial** of Sprint 030's
re-evaluation protocol: one authoring sprint on `opus`+`low`, comparing gate rounds. If they
do not rise, that is the correct configuration despite costing more per token — because
rework dominates.

### The artifact

`config/model_tiers.json`, with the `cursor` column **derived automatically** from Cursor's
catalogue (`Sprint 026`):

```json
{
  "_comment": [
    "Tier -> model per tool. Profiles in agents/ declare their tier.",
    "NEVER write a model ID with a date suffix: family aliases absorb version bumps.",
    "The cursor column is derived by audit_cursor_models.py from the on-disk catalogue.",
    "Cursor has no subagents: the tier applies per PHASE (authoring vs gate), not per agent."
  ],
  "tiers": {
    "gate":       { "claude_code": { "model": "opus",   "effort": "high"   }, "cursor": { "model": "<auto>", "family": "<derived>" } },
    "author":     { "claude_code": { "model": "sonnet", "effort": "medium" }, "cursor": { "model": "<auto>", "family": "<derived>" } },
    "mechanical": { "claude_code": { "model": "haiku",  "effort": "low"    }, "cursor": { "model": "<auto>", "family": "<derived>" } }
  },
  "excluded": {
    "claude-fable-5": "2x the cost of Opus ($10/$50) and requires 30-day retention (no ZDR). Enters only by explicit human decision."
  },
  "context_limits": { "haiku": "200K", "sonnet": "1M", "opus": "1M" },
  "verified_at": "2026-08-17",
  "verified_against": "claude-api skill reference (cached 2026-06-24)"
}
```

**Declared uncertainty:** the Agent tool accepts `effort` per call; **whether a profile's
frontmatter accepts it is unverified** and is checked at implementation. If it does not, the
tier is still declared in the profile and `effort` is applied by whoever launches the subagent,
reading the mapping.

## Three layers of indirection

The tier is **stable intent**; the model is **volatile implementation**. Separated from the
first commit, not afterwards.

| Layer | Artifact | Rule |
| :--- | :--- | :--- |
| **Profile** | `agents/*.md` | Declares **two fields**: `model:` with a **family alias** (`opus`/`sonnet`/`haiku`), which the harness applies natively, and `tier:` (`gate`/`author`/`mechanical`) with the intent. **Writing a full model ID is PROHIBITED**: the alias absorbs bumps without touching any file |
| **Mapping** | `config/model_tiers.json` | tier → `{claude_code: <alias>, cursor: <name>}`. A change of landscape edits **one** file, not thirteen profiles |
| **Owner** | `agents/token_economy_agent.md` | Its charter widens to own the tier table and the escalation path. No selector agent is created — see `Sprint 028` |

**Tier-only was rejected**: Claude Code ignores unknown frontmatter keys, so a profile
declaring only `tier:` would silently run on the session default — the most expensive tier.
Both fields are declared, and a `make verify` check asserts they match the mapping.

**Escalation, not an agent.** When a task's difficulty diverges from its role's default — the
`devops_agent` on `haiku` that `C5` asks to author a Dockerfile — the role proposes it in
`task_scope.md`, it is recorded, and the human sees it. Launching a subagent per task to choose
a model would spend the very unit of cost this sprint reduces.

**Declared dependency on 023:** measuring whether a tier was right requires attributing a gate
rejection to the role that produced the work. `task_scope.md` has no assignee column today —
added in 023 (`R6`). **Until then this table is informed judgment, not measurement**, and says so.

## Keeping it current — the framework does NOT maintain a catalogue

**Copying the price table into `config/model_tiers.json` makes it stale the day it is written.**
That is the defect this whole program pursues: a claim nothing recomputes. Same mechanism by
which the README counts drifted three times in one session.

**Measured constraint:** `ant` is not installed, the `anthropic` SDK is not either, and the
`/v1/models` endpoint **returns no prices** — only `max_input_tokens`, `max_tokens` and
`capabilities`. An automatic poller would require admitting a dependency
(`rules/code_craft.md §7`) for a check that runs a few times a year, and still would not cover
the most volatile datum.

| # | Defence | What it absorbs | Maintenance cost |
| :--- | :--- | :--- | :--- |
| **D1** | **Family aliases in the mapping** — `opus`/`sonnet`/`haiku`, never a dated ID | Every version bump within a family | **Zero** |
| **D2** | **The decision record is dated, not live** — prices, context windows and ratios live in this roadmap with their verification date, **never in the config** | A stale datum reading as current | Zero: a fact that declares its date cannot rot silently; a config value that looks live and is not, can |
| **D3** | **Verification is an agent action, not a script** — load the `claude-api` reference, compare the tier table, report | Prices, retirements, new families, context changes | One comparison per declared cadence |
| **D4** | **Two dependency-free checks**: a **detector** diffing Claude Code's bundled catalogue against a baseline, and a **freshness check** verifying `D3` actually ran | New models, retirements, context changes (detector) · `D3` being forgotten (freshness) | Two scripts, zero network, zero credentials |

### New-model detector — `scripts/detect_new_models.py`

**An authoritative on-disk source exists, with no network and no credentials:** the `claude-api`
skill Claude Code bundles ships `shared/models.md` with the full catalogue — alias, full ID,
context window, max output and **status** (`Active` / `Legacy` / `Deprecated` / `Retired`).
Verified on this host: parseable as a Markdown table, at
`bundled-skills/<cli-version>/<hash>/claude-api/shared/models.md`.

**The path encodes the CLI version**, so the catalogue refreshes exactly when Claude Code
updates. Nothing needs polling: the trigger is the tool's own update cycle.

| Aspect | Design |
| :--- | :--- |
| **Source** | The bundled `models.md` of the highest CLI version, located by glob |
| **Baseline** | `catalog_snapshot` in `config/model_tiers.json` — the known alias set with status, and which CLI version produced it. Same pattern as `last_close_commit`: without a baseline there is no "new" |
| **Detects** | New aliases · status transitions (`Active`→`Deprecated`→`Retired`) · context-window changes |
| **Does not detect** | **Prices.** Not on disk, only in the skill's rendered prompt. Covered by `D3` as an agent action — declared rather than faked |

| Finding | Response | Why |
| :--- | :--- | :--- |
| **New alias in the catalogue** | `session_probe` **proposes** it | A candidate for Sprint 030's evidence protocol, not a change. A model is not adopted for existing |
| **A tier's model becomes `Deprecated`** | Proposed **with its retirement date** | There is room, but with a clock: migration is planned before the clock runs out |
| **A tier's model becomes `Retired`** | **`make verify` fails, exit 2** | Not a judgment: a retired model returns 404. Deterministic and catastrophic, so it blocks rather than proposes |

That ladder is the difference between a probe and a gate applied inside one mechanism:
**propose what requires judgment, block what is a guaranteed failure.**

**Bounded freshness, not real time.** The detector sees what the bundled skill knows. If its
cache is from 2026-06-24 and a model ships 2026-08-01, it does not appear until Claude Code
ships an updated skill. A known, bounded delay — not a silent blind spot.

**Under Cursor the detector is different, not absent:** `cursor/seenNewModelBadgeModelNames`
plus the catalogue diff (`Sprint 026`).

**`D4b` — the freshness check.** `config/model_tiers.json` carries `verified_at`.
`scripts/session_probe.py` — which already exists, already has an invoker and already caches by
TTL — adds a check: if `verified_at` exceeds the threshold, propose re-verifying. **It queries
no model: it verifies that someone did.** Exactly the shape of `detect_drift.py`, which does not
judge the work but notices nobody sealed the record.

**Additional mechanical guard, dependency-free.** Inside `make verify`, at grep level: **no file
under `agents/` and not `config/model_tiers.json` contains a dated model ID** (pattern
`claude-[a-z]+-[0-9]+-[0-9]{6,}`). Cheap, deterministic, and it attacks the only way layer 1
can break.

| `D3` trigger | Action |
| :--- | :--- |
| `verified_at` exceeds the threshold (proposed: **90 days**) | The probe proposes it at start |
| Sprint close | `close_workflow.md` already re-runs the platform probe with `--force-platform`; tier re-verification joins that class as an agent step |
| A new model appears in the tool's list | **Candidate**, not change: triggers Sprint 030's evidence protocol |

**Precedent that validates this:** in the session that drafted this plan the tier table was
about to be written from memory; the `claude-api` reference trigger prevented it and the table
changed materially — Fable 5 turned out to cost twice Opus, not to be a cheap top tier. The
mechanism works; what was missing was making it mandatory at the right moment instead of
dependent on someone remembering.

## Interaction with Sprint 023

`C5` of 023 gives `Write`/`Edit` to `devops_agent`. A profile moving from verifying to
**authoring deployment artifacts** may not fit `haiku`. **Decision:** assign `haiku` now, and
have 023 re-evaluate that specific tier when closing `C5` — recorded in 023's plan as a step,
not an option. Pre-assigning a high tier "just in case" would be the speculative generality
`rules/code_craft.md §1` prohibits.

## Tests

| Check | Must fail against the current tree |
| :--- | :--- |
| All 13 profiles declare `model:` (alias) **and** `tier:`, and a `make verify` check asserts they match `config/model_tiers.json` | **Yes** — 0 have them today |
| The three gate profiles resolve to `opus` and effort `high` | **Yes** |
| `config/model_tiers.json` declares `claude-fable-5` in `excluded` with its reason | **Yes** |
| The `mechanical` tier declares Haiku 4.5's 200K ceiling | **Yes** |
| Frontmatter remains valid YAML and `name`/`description`/`tools` are unchanged | No — regression to protect |
| No `agents/*.md` contains a full model ID (pattern `claude-[a-z]+-[0-9]`) | No — regression to protect |

**Commits:**
1. `feat(agents): every profile declares its model tier #022`
2. `feat(config): one tier-to-model map per tool, not thirteen pinned models #022`
3. `feat(scripts): detect a new or retired model from the catalog already on disk #022`
4. `feat(verify): a tier naming a retired model is a build failure, not a warning #022`

**Out of scope:** changing any profile's `tools:` list (that is `C5` of 023); adding tiers to
`profiles/` specialists, which do not exist in the public nucleus; and **building
`audit_cursor_models.py`**, which belongs to Sprint 026.

---

# Sprint 023 — `upstream-findings`

Give the Implementation Plan a location and a gate, repair the seven framework-class findings a
host reported and could not patch, and declare the nature of `requirements-freeze.txt`.

**Branch:** `ai-sprint/023`

## Context

A host (sprints 085-093) accumulated thirteen framework-class findings. `agents.md §4
feedback_upstream` mandates routing them; `§3 strict_rule` forbids it from patching the
submodule. Between the two rules **a nucleus finding had nowhere to live**, and for eight
sprints it lived nowhere: the inventory sat in a session scratchpad and was lost, which is
exactly what `§4 ephemeral_memory` announces.

The host reconstructed it by re-reading the records of 085-093 and routed it to
`origin/contrib/host-findings` (`docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md`, genericized per
`RA-15`). That document is this sprint's input, and its own working rule governs the plan:
**"Reproduce before repairing"**.

### Verified beforehand — 7 of 7 reproduce against `v4.4.0`

| ID | Reproduction |
| :--- | :--- |
| `F-086-A1` | `agents/devops_agent.md:4` → `tools: Read, Glob, Grep, Bash`. No `Write`/`Edit` |
| `F-087-P1` | `scripts/session_probe.py:147-151`. Absent field → `.get(control, {}).get("status")` → `None` → `"disabled"` |
| `F-086-S1` | `skills/env-shielding-auditor/scripts/env_shielding_auditor.py:25`. No `.yml`/`.toml`/`Dockerfile` |
| `F-086-S2` | `hooks/on_commit.py:90-96`. Requires `=` and a quoted value |
| `F-086-S3` | `django-expert-3rd`: a 20-line stub over a 247-line vendor skill |
| `F-093-N1` | `agents.md:10` mandates `docs/0_SYSTEM_OVERVIEW.md`; the nucleus has only the template |
| `F-093-N2` | **Executed live** from a host root: `FileNotFoundError`, exit `1` |

### Three corrections reproduction produced

1. **`F-093-N2` is wider.** All five counters use relative paths **and so does
   `README = Path("README.md")`**. `glob()` over an absent directory returns empty rather than
   raising, so only `skills` blows up and **the exception masks the other four**. Fixing only
   the crash turns the failure into `no declared count found` ×5 → exit `2`: **false drift in
   every host**, worse than the crash because it looks like a verdict.
2. **`F-086-S3` is narrower, and hides a second defect.** Of the 7 `-3rd` skills, **exactly one**
   has a nested `SKILL.md` — the mass re-check the document proposes is unnecessary. But
   `mass_standardizer.py:81` climbs **five** `.parent` levels where four are correct, so
   `manifest_skills.json` resolves outside the repository in nucleus and host alike. **The
   auditor does not generate a bad stub: it cannot run.**
3. **Open decision #5 was mis-framed.** The 26 alerts (19 high) come **entirely** from
   `requirements-freeze.txt`, which **no install path reads**: `start_workflow` installs
   `requirements-core.txt` (1 package) and skillopt installs `requirements-skillopt.txt` (3, on
   demand). `skills/skillopt/SKILL.md:21` documents it as a *record*. It is not debt the nucleus
   carries: it is **documentation being scanned as a lockfile**.

### New findings, not in the inventory

**`F-021-P0` — the Implementation Plan is the only deliverable with no home.** It is
`triple_lock`'s **first lock** (`agents.md §2`), the Phase 1 deliverable, `principal_agent`'s
property, and `rules/code_craft.md §7` requires justifying every new dependency in it. It is
mentioned **seven times** across the governance corpus and **no document says where it is
written**. Measured: 11 templates in `docs/standards/templates/` and none for an Implementation
Plan; a host's real sprint 093 folder contains `ROADMAP.md`, `SPRINT_LOG.md`, `task_scope.md`,
`agent_assignment.md`, `skill_assignment.md` and `PHASE_REGISTER.md` — **no plan**.

`pipeline_workflow.md:15` explicitly acknowledges *"a plan drafted outside this workflow — in an
IDE planning mode"* and routes it as input without requiring persistence. **Measured
consequence:** a host lost an approved plan and nothing detected it.

**Third evidence, found while executing Sprint 024:** the nucleus itself held **two
Implementation Plans from April 2026** in `docs/sprints/core/pipeline/`, **untracked**, because
`.gitignore` excluded that tree and `implementation_plan*` by pattern. They survived four months
on one machine. Sprint 024 removed that exclusion and committed them as the evidence.

**`F-021-A2` — no profile in `agents/` can write code.** The seven profiles with `Write`/`Edit`
are documentation, governance or skill roles; `qa_agent`, `tester_agent`, `principal_agent` and
`devops_agent` do not write. For `scripts/` and `hooks/` **there is no owner**. `F-086-A1` is the
visible case of a structural void.

## Scope: thirteen units, thirteen commits

Ordered by the cost of what goes wrong if nobody decides, not by effort.

| # | Concern | File | Why here |
| :--- | :--- | :--- | :--- |
| C0 | `F-021-P0` — the plan lives in the repository, and plan mode is mandatory | `agents.md`, `pipeline_workflow.md`, new template, new gate | A host lost an approved plan |
| C0.2 | **The artifact registry — the real matrix** | `config/artifact_registry.json` (new) + 3 existing consumers | Defines each phase by the artifact it leaves. Prerequisite of Sprint 026 |
| C0.3 | The framework root is resolved once, not six times | `scripts/_root.py` (new) + 6 consumers | `F-093-N2` is a member of a class. Precedes `C1` and `C4` |
| C1 | `F-093-N2` — anchor paths against the script | `scripts/check_readme_counts.py` | A mandatory close step that **has never passed in any host** |
| C2 | `F-087-P1` — *absent* ≠ *disabled* | `scripts/session_probe.py` | A security control reported off while on destroys trust in the whole probe |
| C3 | `F-086-S1` + `F-086-S2` — the secret gap | `env_shielding_auditor.py:25` + `hooks/on_commit.py:90` | **One PR.** Good patterns with a bad list, and a good list with a bad pattern |
| C4 | `F-086-S3` — `mass-standardizer` returns to service | `mass_standardizer.py` | Two defects: the 5-level `base_dir` and the stub that ignores nested content |
| C5 | `F-086-A1` + `F-021-A2` — the role map | `agents/devops_agent.md:4` | One line closes the finding; the structural void is **declared**, not resolved here |
| C6 | `F-093-N1` — the nucleus entry point | `agents.md:10` + `start_workflow.md:16` | In nucleus mode the mandatory entry resolves to nothing |
| C7 | `requirements-freeze.txt` — declare its nature | `requirements-freeze.txt` | Today it is documentation and lockfile at once |
| C8 | Close the upstream loop | `origin/contrib/host-findings` | Tick the box and **keep the entry** |

### C0 — the plan lives in the repository

| Mode | Path |
| :--- | :--- |
| Host | `docs/sprints/[Sprint_ID]-[Stack]-[Layer]/IMPLEMENTATION_PLAN.md` |
| Nucleus | **The same path.** The asymmetry this concern was going to declare **no longer exists**: Sprint 024 gave the nucleus the canonical sprint hierarchy, and `docs/sprints/024-core-pipeline/IMPLEMENTATION_PLAN.md` is the first instance |

**Binding ordering, `RA-13` shape.** The plan must be **written in the repository before**
Phase 5 (Approval Gate). `triple_lock` names the *"Approved Implementation Plan"* as its first
lock: an artifact that does not exist cannot be approved, nor can an approval whose object
vanished be audited afterwards.

**Mandatory plan mode, stated verifiably.** Written in terms the framework can check, not in
terms of one IDE's feature: *Phase 1 produces a plan written and versioned in the repository
before Phase 5, and where the environment offers a planning mode, Phase 1 runs in it.*

**No new mechanism.** Enforcement reuses what PR `#37` built: the `artifact → producing phase`
map in `scripts/docs_freshness_check.py` gains `IMPLEMENTATION_PLAN.md → "Phase 1 (Planning) —
Principal Agent"`, and `close_workflow.md` Phase 2.6 adds the plan to the artifacts it demands.

**`.gitignore` amendment, carried from Sprint 024's `F-024-D4`:** `C0` must decide how the
nucleus versions its own pipeline state without breaking the exclusion that protects hosts. The
sprint hierarchy was resolved in 024; `docs/active_state.json` remains ignored because it mixes
durable record with live session state, and splitting it by lifetime is a concern of its own
(`F-024-D9`). Also: `scripts/docs_freshness_check.py:418` must stop warning about a directory
`.gitignore` guaranteed absent — resolved for the nucleus in 024, still to be reviewed for hosts.

### C0.2 — the artifact registry

> Promoted from two loose patches to a mechanism, because Sprint 026 consumes it.

**Principle:** *the documentation the pipeline generates is the coordination matrix.* Each phase
is defined by **the artifact it leaves**, not by the agent that produces it nor the tool that
runs it. A framework requiring *"Phase 4 leaves `task_scope.md`"* runs under Claude Code, under
Cursor and from a terminal; one requiring *"invoke `rule_validator`"* runs only where that
primitive exists.

**Artifact:** `config/artifact_registry.json` — one entry per artifact with `filename`, `phase`,
`role` (advisory), `host_path`, `nucleus_path` and `required`. JSON because three consumers read
it; `config/invocation_exceptions.json` and `config/abandoned_branches.json` already establish
`config/*.json` as the home of machine-readable governance configuration.

| Consumer | Today | With the registry |
| :--- | :--- | :--- |
| `scripts/map_workflows.py` | Fixed `ARTIFACTS`: 6 state, 0 documentary | Columns derived from the registry |
| `scripts/docs_freshness_check.py` | Hand-coded `artifact → phase` map | Read from the registry |
| `close_workflow.md` Phase 2.6 | Demands `task_scope.md` and two verdicts | Demands everything `required: true` |

**Why the current instrument could not detect this.** `map_workflows.py` fixes `ARTIFACTS` at six
state artifacts and none documentary, and matches `if artifact in action` — **by literal
filename**. A deliverable named in prose is invisible by construction. Visible symptom since the
guide was generated: `pipeline_workflow` Phase 1, Phase 5 and 4.1 come out as `?`, and
`task_scope.md` appears as `?/verify` under `pipeline_workflow` while `close_workflow` writes it
— **the producer registered as consumer**.

| Step | Action |
| :--- | :--- |
| R1 | Create `config/artifact_registry.json` with the artifacts hosts already produce |
| R2 | Phases 1, 4.1 and 4.2 of `pipeline_workflow.md` name their artifact **by filename** |
| R3 | `map_workflows.py` derives its columns from the registry; regenerate the guide |
| R4 | `docs_freshness_check.py` reads the phase→artifact map from the registry |
| R5 | `close_workflow.md` Phase 2.6 demands everything `required: true` |
| R6 | `task_scope.md` gains an **`Assignee`** column — today it is `# \| File \| Operation \| Risk \| Status` and attribution lives loose in `agent_assignment.md`. Without it a gate rejection cannot be attributed to the role or tier that produced it, and 022's tiering stays informed judgment |

**Limit:** the registry declares artifacts hosts **already produce**. It invents none.

### C0.3 — the framework root resolved once

| How the root is resolved | Scripts |
| :--- | :--- |
| Bare relative paths — **cwd-dependent** | **11** |
| `Path(__file__).resolve().parent.parent` | 3 |
| `Path(__file__).parent.parent` (no `.resolve()`) | 2 |
| `Path(__file__).resolve().parent` | 2 |
| `Path(__file__).parent` × 5 | 1 — `C4`'s defect |

**Correction to the analysis itself: "the eleven" was the wrong reading.** The scripts split into
two classes with **opposite** requirements, and no document distinguishes them:

| Class | Scripts | Being cwd-relative is… |
| :--- | :--- | :--- |
| **Framework-scoped** | `check_readme_counts`, `check_manifest_parity`, `map_workflows`, `scan_workflow_determinism`, `verify_references` | **a defect** |
| **Host-scoped** | `docs_freshness_check`, `loop_guard`, `detect_drift`, `hooks/telemetry`, `hooks/state_mirror` | **correct** — anchoring them to the framework would break them |
| **Mixed** | `branch_sovereignty` — audits the host's git and reads the framework's `config/` | the real defect |

**Action:** `scripts/_root.py` with `agents_root()`, adopted by the five framework-scoped scripts
and `mass_standardizer.py`. Host-scoped scripts are **not touched** — they gain a docstring line
declaring their root is the project. `branch_sovereignty.py` moves only its `config/` path.

**Note:** Sprint 025 created `scripts/_mode.py` with the same anchoring, deliberately, so this
becomes a merge rather than a redesign.

**Explicit limit:** no observable behaviour changes. What passes from the nucleus root today must
pass identically, and additionally pass from any other cwd.

### C1-C8, in brief

> **C9 runs before all of these.** See the `C9-C10` section below: `023`'s own close runs
> `branch_sovereignty audit`, and that gate is intermittently wrong until `C9` lands.

- **C1** — anchor README and the five counters against `agents_root()`. Do **not** wrap
  `iterdir()` in `try/except`: that turns the crash into false drift.
- **C2** — when the key is absent emit `"cannot determine (field not returned)"` instead of
  asserting a state; read `dependabot_security_updates` from
  `GET /repos/{owner}/{repo}/automated-security-fixes` (**verified**: returns
  `{"enabled":true,"paused":false}`).
- **C3** — auditor: extend the suffix tuple with `.yml`, `.yaml`, `.toml`, `.cfg`, `.ini`,
  `.conf`, `.tf`, `.example`, **and** match by full name (`Dockerfile`, `Makefile`,
  `docker-compose.yml`). Hook: three alternations — `ENV|ARG` with optional `=`, `key: value` for
  YAML, and `[?&]\w*(key|token|secret|password)=` for query strings. **Existing false-positive
  exclusions are preserved and applied to all three new forms** — the hook already blocked a host
  once for this.
- **C4** — `base_dir` adopts `agents_root()`; before writing a root `SKILL.md`, detect a nested
  one and link it instead of overwriting. `skills/django-expert-3rd/skills/SKILL.md` is vendored
  and **not touched**.
- **C5** — `agents/devops_agent.md:4` gains `Write, Edit`. `F-021-A2` is **declared**, not
  resolved: splitting an implementer profile is a role-map redesign.
- **C6** — declare the nucleus exception in `agents.md §0`, as `§5` already does for topology.
  `start_workflow.md:16` gets the same carve-out, which it lacks while `close_workflow.md:20`
  has it.
- **C7** — Dependabot alerts **cannot be excluded by path**; `.github/dependabot.yml` governs
  *updates*, not *alerts*. So rename to `docs/audits/SKILLOPT_TRANSITIVE_CLOSURE.md` with the
  content in a code block. **This does NOT claim there is no exposure** — it changes whose debt
  it is.
- **C8** — tick each closed finding's box **keeping the entry** (rule 3 of the document); add
  `F-021-A2` and the three measurement corrections.
  **Scope extended during execution, by human authorization, after the structural gate refused the
  addition as undeclared**: also record **`F-023-S4`** — the literal `.env` that still passes
  `hooks/on_commit.py` after `C3` repaired the secret gate, tracked as `F8` in `023`'s
  `task_scope.md`. The gate was right to refuse it: `C3` had already declined the same finding as a
  rider on a unit whose scope did not name it, and `C8` was taking it on identical terms. It is
  recorded rather than dropped because `agents.md §4 feedback_upstream` mandates routing a
  framework-class finding, and this one had survived **three sessions** as *routed, unowned* — the
  precise pattern this sprint's `Context` identifies as the original loss. Recording it in the
  upstream register is **not** the unit `F8` still needs; that unit remains outstanding.

### C9-C10 — two gates that answer when they do not know

Both were found while **closing Sprint 022**, by running the framework's own close machinery
rather than by reading it. They are one defect class: **a control that treats "I could not
determine" as a determination.** `C9` answers red when it does not know; `C10` answers green.
Neither corrupts data; both make a gate lie, which is what this program exists to pursue.

**`C9` runs FIRST, before every other unit of this sprint** — `023`'s own close runs
`branch_sovereignty audit`, so leaving it flaky means the sprint trips on the defect it came to
repair.

- **C9** — `merged_pr_exists` (`scripts/branch_sovereignty.py:94-107`) collapses a transient
  network failure into a verdict: `if result.returncode != 0: return False`. **Measured, not
  inferred**: twelve consecutive calls to the exact query the script issues returned
  **10 OK and 2 failures**, `rc=1`, `HTTP 503: No server is currently available`. Since
  `content_is_integrated` already returns `False` for any squash-merged branch, one 503 flips an
  **integrated** branch to "unintegrated". Reproduced end to end — three consecutive `audit` runs
  on an unchanged tree exited **`0`, `2`, `0`**, accusing `ai-sprint/025`, whose PR `#41` is
  `MERGED`. **A second triple run minutes later exited `0`, `0`, `2` and accused
  `ai-sprint/024` instead** — the accused branch *varies between runs on an identical tree*, which
  is the signature of a per-call network failure rather than any property of a branch. That is the
  cheapest regression test available: an audit whose accusation is not reproducible is not
  reporting a fact about the repository.
  **Consequence recorded live**: this session declined to run `prune` because its own declared
  precondition (three consecutive `exit 0`) failed, even knowing both PRs were `MERGED`.
  Overriding a red gate on the strength of knowing better is the behaviour this unit exists to
  make unnecessary — so the branches stay until `C9` lands and the gate is worth obeying.
  **The failure direction is safe**: `prune` deletes only what it classified as integrated, so a
  503 leaves the branch untouched — it never destroys. **The real damage is the remediation it
  induces.** On that `exit 2` the script instructs the operator to either re-run
  `/agents:deployment` on an already-merged branch, or record the branch in
  `config/abandoned_branches.json` — which **permanently disables the check for a healthy
  branch**. The script warns about exactly this in its own text: *"an undeclared exception is how
  this check gets disabled instead of answered"*. Its own flakiness manufactures the pressure that
  disables it.
  Fix: three states — *yes*, *no*, *could not determine* — with retry and backoff; the third is
  **reported as indeterminate and never as a verdict**, and the waiver is not offered when the
  cause was a network failure. Also closes an `agents.md §1 exception_handling` violation: the
  error is swallowed with no log.
- **C10** — `workflows/deployment_workflow.md:17` names `gh pr checks [N] --watch` as the `RA-13`
  gate before merging. **It cannot wait for a check that is not registered yet.** Timeline
  measured on PR `#45`: created 16:12:37; `--watch` terminated ~16:13 having seen only `audit`;
  the CodeQL run was **registered at 16:15:14**, two minutes later. Two of the three required
  checks (`Analyze (python)`, `CodeQL`) had not reported when the gate returned. What actually
  blocked the merge was GitHub branch protection — **not the framework's gate** — and
  `/agents:harden` is optional and runs once, so **on a host without it the merge would have gone
  through unverified**.
  `mergeStateStatus` alone is not the fix: it returns `CLEAN` **also when no check is required**,
  so an unprotected repository reads green from the first second — precisely the host case.
  Fix: `scripts/ci_gate.py` reads the **required** checks from branch protection, confirms each
  one reported and passed, and **fails loudly when none is declared**, because an unprotected
  repository is not a verified one. `invoked_by:` declared (`RA-16`), and
  `deployment_workflow.md:17` stops naming `--watch`.

**Amendment candidate for `agents.md §7`, to be decided in this sprint**: *a control that depends
on the network MUST distinguish "could not determine" from a verdict, and never collapse it into
either.* One rule covers both units.

## Execution

**Known conflict, declared rather than silently resolved.** Per `F-021-A2` no profile can write
under `scripts/` or `hooks/`. Writes are emitted by the lead agent **under the ruleset of the
profile governing each artifact**, and the deviation is recorded in `task_scope.md` so the
structural gate **audits** it instead of discovering it.

**Valid until `C5`.** `C5` closed `F-086-A1`, so `devops_agent` now holds `Write`/`Edit` for
the framework-root `scripts/` and `hooks/` trees. The practice above survives unchanged from
`C5` onward, but its **reason** does not: writes stay with the lead session because this
session's configuration forbids dispatching subagents for authoring, **not** because the role
map lacks an owner. `F-021-A2` — the absence of an implementer role — remains open.

One atomic commit per concern (`RA-08`), all on `ai-sprint/023`, one sprint PR.

## Risks and exclusions

| Exclusion / Risk | Posture |
| :--- | :--- |
| The 7 "carried" findings (`G-03`, `REVDOC-G1`, `ADR-0006`, `ADR-0007`, `C5`, `#12`, `#13`) | **Out.** The document requires reproducing before acting, and they are not reproduced |
| Splitting a code-implementer profile (`F-021-A2`) | **Out.** Role-map redesign |
| Editing `skills/django-expert-3rd/skills/SKILL.md` | **Out.** Vendored; `rules/skills_and_integrations.md §3` forbids it |
| **Risk: false positives in C3** | Mitigated and watched. Existing exclusions apply to all three new forms, with their own regression test |
| **Risk: C7 reads as "there is no exposure"** | Declared in the commit and the ledger. What changes is whose debt it is |
| **`C0` and hotfixes** | `RA-03 HOTFIX_FLAT` is a sanctioned exception. The plan obligation is stated over the **sprint pipeline**, not `docs/hotfixes/` |
| **`C0` does not cover the rejected plan** | **Out**, declared. What is persisted is the plan that reaches the Approval Gate |
| **`C0.3` touches 7 files and `jurisdictional_lock` limits one per subtask** | Mitigated by design: the helper is written and tested first, then six one-line subtasks |

---

## Appendix — Sprint 026 (`tool-portability`), proposed

**Agreed objective:** *portability* — the same repository opens with Cursor or Claude Code
interchangeably, with coherent state in both. **Not** concurrency, **not** handoff, **no** calls
to the Anthropic API (human decision: *"for that I use Claude"*).

**Governing principle, given by the human:** *the real matrix is the documentation we generate.*
`C0.2`'s artifact registry **is** that matrix, and this sprint is its first external consumer.

### Already portable today, without knowing it

| Piece | Status |
| :--- | :--- |
| **`AGENTS.md`** | Already exists as a symlink to `agents.md` in a real host. It is the agnostic entry point Cursor reads — **the constitution is already exposed portably** |
| **Commit hooks** | Installed as **git** hooks: Conventional Commits, sprint suffix, secret scanner and test gate run under any tool and from a terminal |
| **Scripts** | Plain Python |
| **State** | `docs/active_state.json` mentions no tool |

### Portability map, measured

| Layer | Claude Code | Cursor | Ports? |
| :--- | :--- | :--- | :--- |
| Constitution | `@import` in `CLAUDE.md` | `AGENTS.md` or `.cursor/rules/*.mdc` with `alwaysApply` | **Yes** |
| Lazy rules | prose trigger table | `.mdc` with `globs:` — **native** lazy loading | **Yes, and better** |
| Protocols | `.claude/commands/agents/*.md` | `.cursor/commands/*.md` | **Yes** |
| Scripts | invoked by workflows | identical | **Yes** |
| **Commit hooks** | installed as **git** hooks | identical | **Already portable** |
| MCP | `.mcp.json` | `.cursor/mcp.json` | **Yes**, different path |
| Session hooks (`RA-11`, `on_init.py`) | `PreToolUse` + session events | different event model | **Partial** |
| Subagent roles (the 8-role pipeline) | `.claude/agents/` with `tools:`/`model:` | no equivalent primitive | **No** |
| Skills | `.claude/skills/` | no equivalent | **No** |

### Obstacle 1 — a live governance contradiction

`workflows/standardization_workflow.md:45` lists `.cursor/rules` among *"other frameworks"*
proposed for archiving at onboarding. Installing under Cursor requires repealing that line, or
the protocol would archive the configuration it just created. **Repealed explicitly, not by
omission.**

### Obstacle 2 — delegation, and the recommendation

`agents.md §6` mandates 8 roles and Cursor cannot spawn them. It is `start_workflow.md` Phase 2's
`delegation_conflict`, but **structural instead of policy**: under Cursor it would fire every
session by construction.

| Role class | Under Cursor | Why |
| :--- | :--- | :--- |
| Authoring | sequential `.cursor/commands/*.md`, single agent | Their artifacts are checked by a downstream gate. Zero new infrastructure |
| **Gate (`qa_agent`, `tester_agent`)** | **Fresh context, mandatory** | Across four host sprints every central defect was found by a gate and nothing else, **and several had survived their author's verification**. The value is not the role: it is the independent context |

**Single-agent-covers-everything is rejected**, despite being safer now than when it failed
(Phase 2.6 exists since PR #37). The precedent: a host used it, Phases 4 and 7 never ran,
`task_scope.md` was not produced, and that silently disabled `jurisdictional_lock` and
`no_interference` across ~30 edits; when the gates finally ran, both rejected the branch over
HIGH defects of exactly the class the sprint existed to remove.

### What stops firing under Cursor — complete list

| Entry | What it does | Portable mitigation |
| :--- | :--- | :--- |
| `permissions.deny` (4 rules) | Blocks `git push --force`, `-f`, `git reset --hard origin`, `rm -rf /` | **`pre-push` git hook** covers the three git ones. `rm -rf /` **is not coverable** by git and is declared a Claude Code-only guardrail, not faked as covered |
| `PreToolUse` → `on_commit.py` | Secret scanner, regression-test gate, dependency gate | **Already covered** — the installer also places it as a git `pre-commit` hook |
| `SessionStart` → `on_init.py` | Verifies bridge integrity, syncs commands | Already written as a protocol step (`start_workflow.md` 1.5). The hook was the automation, not the source |
| `Stop` → `state_mirror.py` | Refreshes the anchor mirror | `session_state.py claim`/`release` already refresh it, so under Cursor it stays fresh **at session edges but not mid-session**. **Declared, not disguised** |

### Day-one blocker not on the map

`session_state.py claim --session-id` is **`required=True`**, and `start_workflow.md` Phase 0.5
invokes it with the UID the Claude Code harness provides. **Cursor exposes no session UID.**
Without resolving this, the protocol's first phase fails and nothing else starts.

**Solution:** `claim` accepts the argument's absence and generates a traceable UID — timestamp
plus PID — also recording the tool in the anchor (`session_tool: claude-code | cursor |
terminal`). The collision guard still works because it compares UIDs, not provenances; and
forensics gains a datum that does not exist today: **which of the two tools left a session open.**

### What is adapted

| # | Change | Form |
| :--- | :--- | :--- |
| P1 | **The pipeline is defined by artifacts**, with roles as a recommended per-tool implementation | Each phase declares artifact, path and done-criterion; the role becomes an advisory column |
| P2 | **Delegation mode declared in state** | `delegation_mode: native \| sequential`. `delegation_conflict` stops being an incident and becomes a configuration read |
| P3 | **Installer with a target** | `scripts/install.py` → `install.py --target claude\|cursor\|both`. The current name stains the `federation` contract and is renamed there |
| P4 | **Cursor adapter** | `.cursor/commands/` from `commands/`, `.cursor/rules/*.mdc` from `rules/`, `.cursor/mcp.json` from `claude/mcp.json`. **Also yields `config/model_tiers.json`'s `cursor` column**, derived by `audit_cursor_models.py` |
| P5 | **The rule trigger table becomes machine-readable** | Today triggers are prose — the same leak `C0.2` describes one level up. Structuring them feeds Cursor's `globs:` **and** makes Claude's lazy loading declarable |
| P6 | **Repeal the line that archives Cursor** | `standardization_workflow.md:45` |
| P7 | **Answer `C5`'s question** | If `AGENTS.md` is the portable entry point, declare whether nucleus content enters the host's gate scope |
| P8 | **`claim` without a harness UID** | `--session-id` stops being required; generates timestamp + PID. New `session_tool` field. **Day-one blocker.** Stacks on Sprint 021's `M6` state machine: `P8` changes *how a session is identified*, `M6` *what states it can hold* — orthogonal, in that order |
| P9 | **`pre-push` git hook** | Covers the three git denials under any tool |
| P10 | **Bridge lock per target** | `.claude_bridge.lock` → `.bridge_claude.lock` / `.bridge_cursor.lock`. One lock cannot represent two installations |
| P11 | **Adapter `.gitignore`** | `.cursor/` entries mirroring `.claude/`'s: generated is ignored, human-edited is tracked |

**Skills stay out of the adapter.** Cursor has no equivalent and their content is readable prose:
they are referenced from the rules, not wrapped in a mechanism the tool does not have.

**The exact `.mdc` format is confirmed at implementation.** There is no `.cursor/` in the local
projects to verify it against, and asserting a frontmatter schema without checking would be
exactly the defect this sprint fixes. P4 is a thin adapter on purpose.

### The `gate` tier under Cursor — automatic selection, no human choosing

**Cursor's catalogue is on disk and auditable.** Verified:
`~/Library/Application Support/Cursor/User/globalStorage/state.vscdb` (SQLite), key
`…persistentStorage.applicationUser` → `availableDefaultModels2`: **36 models from 8 providers**,
each with:

| Field | Use in selection |
| :--- | :--- |
| `name` | Identity; the prefix **derives the family** (`claude-*`→anthropic, `gpt-*`→openai, `gemini-*`→google, `grok-*`→xai…) |
| `supportsAgent` | **Hard filter**: without agent support it serves no role |
| `degradationStatus` | **Hard filter**: Cursor publishes model health; a degraded one excludes itself |
| `parameterDefinitions` | Which levers it accepts: `effort`, `thinking`, `reasoning`, `context`, `fast` |

And two more verified keys:

- **`cursor/seenNewModelBadgeModelNames`** — Cursor's own "new model" signal. **This is the
  detector Cursor was missing**, on disk, no network.
- **`cursor/applicationOpenModelAppliedConfig`** — the selected model **with its parameters**,
  `effort` included.

**Three things this corrects:**

1. Tiering under Cursor is **not "human guidance"**: `effort` is a native parameter, so both
   dimensions apply exactly as in Claude Code.
2. The `family` field **is filled by nobody**: it derives from the name prefix, so the
   provider-diversity rule is automatic and checkable.
3. Auditing *which model ran the gate* **is mechanical**, not human attestation: read from
   `applicationOpenModelAppliedConfig`.

**Hard filters (100% automatic):** `supportsAgent == true`, `degradationStatus == 0`, and for the
`gate` tier `parameterDefinitions` must include a depth lever.

**Ranking by token/quality effectiveness:** the catalogue carries capabilities, **not quality or
price**. Benchmarks were rejected with reason — they measure generic capability, not *"passes
this framework's gates on this code"*. The only valid signal is the one Sprint 021's meter
produces:

```
cost per accepted unit = tokens spent ÷ work that passed the gates
```

A cheap model causing two gate rounds scores worse than an expensive one passing first time.
**That is the token/quality ratio, measured instead of declared.**

**The honest limit: cold start.** A newly discovered model has no history and cannot be ranked.

**What makes the automation safe: the gates.** A model without history **can be tried
automatically in authoring or mechanical work, because the gate catches bad output. It cannot be
tried in the gate, because there nothing catches anything.**

| Promotion step | Who decides |
| :--- | :--- |
| Detected in the catalogue or in `seenNewModelBadgeModelNames` | The script |
| Enters as a candidate for a sprint's `author` tier | The script |
| Its cost per accepted unit is measured | The meter |
| **Eligible for `gate`** only with proven history and a `family` different from `author`'s | The script |

The human chooses no model at any step. What never happens is a model reaching the position
where nothing verifies it without having been measured.

**Artifact:** `scripts/audit_cursor_models.py` — reads the SQLite read-only, applies the filters,
derives families, cross-references the meter's history and **proposes** tier assignments. Zero
network, zero credentials, stdlib `sqlite3` only. It keeps probe doctrine: **proposes and does
not execute**, except the hard filters, which are mechanical because they admit no judgment.

### Done-criterion

The same repository, opened with either tool, produces **the same set of artifacts with the same
names and paths**, and `close_workflow.md` Phase 2.6 seals or rejects it without being able to
tell which generated it. **If the gate can notice the difference, portability has not been
achieved.**

### Acceptance test — a whole sprint run under Cursor

A toy sprint executed end to end in Cursor on a test host. **Not a checklist: an execution.** The
precedent demanding it is in this repository — `F-093-N2` was found by *running* the close
protocol, not reading it, after that step had never once passed in any host.

| # | Step | Criterion |
| :--- | :--- | :--- |
| 1 | `install.py --target cursor` on a clean host | `.cursor/commands/`, `.cursor/rules/`, `.cursor/mcp.json` and `AGENTS.md` present; git hooks installed |
| 2 | Invoke the start protocol from Cursor | Anchor `IN_PROGRESS` with `session_tool: cursor` and a generated UID (`P8`) |
| 3 | Run the authoring phases | Every registry artifact appears at its declared path |
| 4 | Run the gates in fresh context | The sprint record proves both ran |
| 5 | Attempt a commit that violates a gate | The git hook **rejects** it, as under Claude Code |
| 6 | Attempt `git push --force` | The `pre-push` hook **rejects** it (`P9`) |
| 6b | `audit_cursor_models.py` derives families and checks `gate` ≠ `author` | The diversity rule is automatic and verifiable |
| 6c | A model with `degradationStatus != 0` or `supportsAgent: false` is excluded from all tiers | Hard filter, no human judgment |
| 7 | Close the sprint | Phase 2.6 seals. **Compare the resulting tree with an identical sprint run under Claude Code: they must be indistinguishable except `session_tool`** |

Step 7 decides. The first six check pieces; only the last checks the property the sprint is
named for.

**Declared risk:** step 5 must be tested with a **real** violation — an actual secret in a test
`Dockerfile`, not a simulated case. A gate proven only on a healthy tree proves nothing.

---

## Appendix — Sprint 027 (`autonomy-posture`), proposed

**Problem stated by the human:** in a host's recent sprints the session moved to
`bypassPermissions` because authorising every bash command is unworkable. What is wanted is a
configuration managing **effectiveness, memory loss, content drift and security over autonomy** —
four axes, not one.

**Diagnosis:** bypass is a binary instrument. It collapses the four axes into "everything
allowed" and, in doing so, **disables the 4 `deny` rules that are today the only defence** against
`git push --force`, `git reset --hard origin` and `rm -rf /`. The measured host configuration was
already good — 58 `allow` rules, 10 `deny`, with documented precedents — and was abandoned anyway,
which indicates the problem was granularity, not the list.

### What Claude Code's schema already offers and the framework does not use

| Mechanism | What it resolves |
| :--- | :--- |
| `permissions.defaultMode: "auto"` + `autoMode` object | A classifier instead of a prompt per command. Brings `allow`, `soft_deny` (*destructive that intent **can** clear*) and **`hard_deny`** (*security limits intent does **NOT** clear*) |
| `sandbox.enabled` + `autoAllowBashIfSandboxed` | **A contained command does not ask.** Effectiveness and security stop being a trade |
| `sandbox.credentials.files` (`deny` \| `mask`) | `RA-09 secret_sovereignty` moves from rule to OS control |
| `sandbox.network.allowedDomains` | Egress control |
| `plansDirectory` | **The plan lives in the repository by configuration.** Natively resolves the Claude Code half of `C0` |
| `PreCompact` / `PostCompact` hooks | Persist the anchor before losing context and re-read it after: `anti_amnesia` automated |
| `SubagentStop` hook | Verify the artifact a role owed, **the instant it finishes** |
| `SessionEnd` hook | Release the session lock; today only `Stop` refreshes the mirror |
| `fileCheckpointingEnabled` | *Snapshot before editing, restorable with `/rewind`* |
| `disableBypassPermissionsMode: "disable"` | Closes the escape hatch |
| A hook's `if` field | Filters by command pattern. Today `on_commit.py` runs on **every** Bash call |

### Configuration by axis

| Axis | Settings |
| :--- | :--- |
| **Effectiveness** | `defaultMode: auto`; `sandbox.enabled` + `autoAllowBashIfSandboxed`; complete the `allow` list — **`cd` first**, the reason every compound command prompts, plus `jq`, `tee`, `xargs`, `touch`, `chmod`, `which`, `basename`, `dirname`, `tr`, `cut` |
| **Security** | `autoMode.hard_deny`: history rewriting, repository deletion, secret exfiltration. `soft_deny`: `git reset --hard`, `git clean`, `docker compose down -v`. `sandbox.credentials.files` with `.env` in `deny`. `pre-push` hook (`P9`). **`disableBypassPermissionsMode`** |
| **Memory** | `plansDirectory` to the repository; `PreCompact` persists anchor and `task_scope.md`; `PostCompact` re-reads them; `fileCheckpointingEnabled`; **`SessionEnd` → `session_state.py suspend`** (`M6` of 021), **never `release`**: `SessionEnd` marks the end of the *session* and `release` seals the *sprint*, so wiring it to `release` would write a false `last_close_commit` on every session close and blind `detect_drift.py` |
| **Drift** | `SubagentStop` hook against `config/artifact_registry.json`: a role finishing without leaving its artifact is caught instantly, not at close |

### Why `disableBypassPermissionsMode` is not optional

If the framework's security comes to depend on `auto` mode and its `hard_deny`, leaving bypass
available makes the whole design optional — and this host's own precedent shows the option is
taken under friction pressure. Closing it is what makes the posture a posture rather than a
recommendation.

| Risk | Posture |
| :--- | :--- |
| `auto` mode delegates the decision to a classifier | It is a judgment, not a list. That is why `hard_deny` exists: what must not depend on judgment is enumerated |
| The sandbox breaks commands needing network or external paths | `allowedDomains` and `filesystem.allowWrite` are configured from what the host actually uses, measured before enabling — not guessed |
| `classifyAllShell: true` costs on every command | **Not enabled.** `allow` rules must keep short-circuiting the classifier |
| This is host configuration, and the nucleus is public | Configuration lives in the host (`RA-15`); the nucleus ships the **template** and the hooks. No real host value enters here |

### Applicability to Cursor — the gap this sprint created

**Almost none of the above applies to Cursor.** `defaultMode: auto`, the `autoMode` object,
`sandbox`, `plansDirectory`, `fileCheckpointingEnabled` and the
`PreCompact`/`PostCompact`/`SubagentStop`/`SessionEnd` hooks belong to Claude Code's
`settings.json`, which Cursor does not read. `SubagentStop` additionally **has no possible
equivalent**: Cursor has no subagent primitive.

**Consequence if uncorrected:** the same repository opened with Cursor ends up less protected, in
silence, while `agents.md §2 destructive_flags` and `RA-09` remain stated as if they applied. That
is the pattern this program pursues — **a control whose verdict depends on how it was run** —
committed this time by the design itself.

| Axis | Portable layer (git hooks + scripts) | Claude Code only |
| :--- | :--- | :--- |
| Security | `pre-push`, `pre-commit`, `commit-msg`, `submodule_purity` | `hard_deny`, `sandbox`, `sandbox.credentials` |
| Memory | Plan in the repository (`C0`), state anchor, `session_state.py` | `PreCompact`/`PostCompact`, `plansDirectory`, checkpointing |
| Drift | Artifact registry + Phase 2.6 + `make verify` | `SubagentStop` |
| **Effectiveness** | **— none** | `auto` mode, `autoAllowBashIfSandboxed` |

**Effectiveness does not port, and that is not pretended.** It is a property of how the harness
asks, not of the repository. The other three **do** port, and must — precisely so the Cursor
session is not the weak one.

**Binding rule this hardens:** *what must hold under both tools lives in git hooks or in scripts
the protocol invokes, never in `settings.json`.* Every mechanism in the right column is an
**acceleration** of something the left column already guarantees — never the sole instance of a
guarantee.

**Added done-criterion:** for every control in the right column, one exists in the left covering
the same risk with less comfort. A control with no portable counterpart is a rule the framework
applies in only one of its two tools, and is declared as such or not admitted.

---

## Appendix — Sprint 028 (`self-improvement-unblock`), delivered

**The framework cannot improve itself from a host.** Not because of any single rule, but through
the **absence of host-side destinations**: every learning artifact has its destination inside the
submodule, and `agents.md §3 strict_rule` forbids the host from writing there.

| # | Finding | Evidence |
| :--- | :--- | :--- |
| S1 | **Agent creation in hard contradiction** | `agents/agent_orchestrator.md:19` orders *"MUST author a new `.md` profile physically in `agents/`"*; `strict_rule` forbids it from a host. Deadlock |
| S2 | **Skills already solved this; agents did not** | `workflows/skill_forge_workflow.md` Phase 0 `forge_destination` forces a choice between (a) host-only `.claude/skills/` — **default**, (b) profile, (c) framework-wide. No equivalent exists for agents, and Claude Code discovers `.claude/agents/` just as it does `.claude/skills/` |
| S3 | **`RA-16` does NOT block new agents** | `scripts/verify_references.py` `check_invocation_coverage` audits `workflows/` and `scripts/` (requiring `invoked_by:`) and executable skills. **`agents/*.md` is only read to build the corpus**, never audited |
| S4 | **The profile tier is uninstallable** | `scripts/install.py:314` resolves `AGENTS_DIR / "profiles" / <name>` — only inside the submodule. `RA-15` forbids a real profile living there and names no alternative. **The middle tier of three has a destination and no address** |
| S5 | **Memory is a purge pipeline** | Three deletion mandates (`ephemeral_memory`, `definitive_amnesia`, `redundant_ki_purge`) against one manual-judgment preservation path (`constitutional_escalation`) |
| S6 | **The upstream route only fires under human pressure** | `extract_workflow` Phase 2 has the right design. Measured in a host: 13 findings, 8 sprints, 0 routed; sprint 087 recorded *"pending, scheduled after this closeout"* and it never happened |

**Today: creation blocked, promotion unaudited** — which is why learning dies in scratchpads.
**It must be: creation local and free, promotion gated.**

| Artifact | Host-side destination | Status |
| :--- | :--- | :--- |
| New skill | `.claude/skills/` | **Exists** (`forge_destination` option a) |
| New agent | `.claude/agents/` | **Missing** — native discovery available, doctrine absent |
| Family profile | A **named** host path, and `install.py` accepting paths outside the submodule | **Missing** — impossible today |
| Memory | `memory_index.json` already lives in the host | Exists, but is purged without escalating |

| # | Action | File |
| :--- | :--- | :--- |
| U1 | `agent_orchestrator.md` gains `forge_destination`'s equivalent: three destinations, **host-only by default** | `agents/agent_orchestrator.md` |
| U2 | `pipeline_workflow.md` Phase 4.1 names the chosen destination in `agent_assignment.md` | `workflows/pipeline_workflow.md` |
| U3 | `install.py` accepts `--profile <path>` outside the submodule; `RA-15` names the location convention instead of saying *"a private location"* | `scripts/install.py`, `agents.md §7` |
| U4 | **Preservation counterweight**: the close does not purge a memory item without its class being routed (host / profile / nucleus). A deletion with no destination is loss, not hygiene | `close_workflow.md`, `extract_workflow.md` |
| U5 | Promotion gate: a host-side agent or skill promoted to the nucleus passes `RA-16` and `RA-15` **in the PR**, not before | `scripts/verify_references.py` (documented) |

### Recommendation on the model selector — **do not create a new agent**

The human asked for *"an agent specialised in choosing which AI model each agent should use"*. The
recommendation is not to create it, and the argument comes from the framework itself:
`agents/token_economy_agent.md` exists and its charter is deciding **whether a recurring mechanism
should be a deterministic script or an agent judgment**. Applied to itself:

- Model choice is determined by the **role** in most cases → that is Sprint 022's static table,
  deterministic and free.
- Launching a subagent per task to decide the model **spends exactly what it tries to save** — a
  subagent is the unit of cost the usage report attributes 100% to.

**What is missing is the exception, not the agent:** when a task's difficulty diverges from its
role's default (the `devops_agent` on `haiku` that `C5` asks to author a Dockerfile). Resolved with
a **declared escalation** in `task_scope.md` — the role proposes, the record notes it, the human
sees it — owned by `token_economy_agent`, whose charter widens to hold the tier table.

---

## Appendix — Sprint 029 (`documentation-truth`), proposed

**Closes the queue.** Not "update the docs at the end": each sprint updates its own under `RA-05`.
This sprint does what **no individual close can do**: the cross-cutting narrative and widening the
counted set.

The README declares five figures and `check_readme_counts.py` verifies them: **10 rule contexts ·
13 agents · 34 skills · 12 workflows · 13 commands**.

**The sprints in this queue change none of the five.** They add no rules, agents, skills,
workflows or commands — they add **scripts** (`session_cost.py`, `detect_new_models.py`,
`audit_cursor_models.py`, `_root.py`, and 024/025's `_mode.py`, `submodule_purity.py`) and
**configuration registries** (`model_tiers.json`, `artifact_registry.json`), and the "At a Glance"
table has a row for neither.

It is `check_readme_counts.py`'s defect one level above the one Sprint 023 repairs: **the check
faithfully verifies what it counts, and what it counts is incomplete.** An entire surface can grow
without the table turning red. Baseline measured at `v4.5.0`: **17 scripts**, **3 config files**,
neither counted.

| Document | What goes false |
| :--- | :--- |
| `README.md` §At a Glance | No row for `scripts/` or `config/`. Eight sprints of work invisible to the only verified table |
| `README.md` line 60 | Cites `scripts/install.sh`, which Sprint 026 (`P3`) renames to `install.py --target` |
| `README.md` overall | **Does not mention Cursor.** After 026 the framework is a two-tool framework and the README describes one |
| `docs/guides/AGENTS_SLASH_COMMANDS_GUIDE.md` | Already drifted once (documented 11 commands while the README said 13). Nothing in `close` names it |

| # | Action | Why here and not in each sprint |
| :--- | :--- | :--- |
| T1 | **Widen the counted set**: rows for `scripts/` and `config/` in "At a Glance", with their counters in `check_readme_counts.py` | A sprint cannot add the row counting *its own* artifacts without the figure being stale until the next one touches it |
| T2 | **Rewrite the README for two tools**: Cursor stops being an absence and becomes a supported installation | Cross-cutting narrative; no sprint owns it alone |
| T3 | **`AGENTS_SLASH_COMMANDS_GUIDE.md` enters the artifact registry** with its producing phase | Closes the hole that already caused an `RA-14` violation |
| T4 | **ADRs for the decisions this plan made** (below) | `rules/documentation_standard.md §3` defines the triggers; several decisions meet them |
| T5 | **Every sprint declares its documentary impact in its own plan**, as a mandatory row. **And every measured figure carries the command that reproduces it** | Prevents documentation piling up at the end — the antipattern this sprint exists not to repeat |

| Decision | Why it deserves an ADR |
| :--- | :--- |
| Gates never drop tier | A permanent cost constraint with measured evidence behind it |
| No model-selector agent is created | Explicit rejection of a reasonable alternative, with its reason |
| Prices do not enter configuration, only the dated record | A counterintuitive architecture choice someone will try to "fix" |
| The session bound before tiering | A priority inversion based on measurement, not intuition |
| Cursor without API delegation | An evaluated and rejected alternative, reopenable under a declared condition |

**Limit:** does not rewrite documentation the other sprints already left correct. A sweep
rewriting correct documents is cost without signal, and risks breaking prose that already passed
its gate.

---

## Appendix — Sprint 030 (`token-economy-enforcement`), proposed

**Reassigned from `025`**, which shipped as `jurisdiction`. IDs are labels, not positions, so the
reassignment moves nothing else.

Motivated by the usage reports: **100% of spend in subagent-heavy sessions, 95% in sessions of 8+
hours, 90% above 150k of context.**

| Check | Result |
| :--- | :--- |
| `skills/token-saver-auditor/scripts/` | Only `__init__.py`. **The official auditor of the token rule has no auditor**, and the Three-File Standard counts it as an executable skill |
| Profiles with `model:` | **0 of 13** |
| `rules/token_economy.md` trigger | Fires on **intent** (*"auditing a plan's cost"*), never on **consumption** |
| Fixed per-session cost | `agents.md` = 169 lines. **The constitution is not the problem**; tool-result accumulation is |

**Cause by symptom, because they do not share one:**

- **Subagent-heavy** — `agents.md §6` mandates 8 roles per pass. `rules/token_economy.md §2`
  governs *what* a subagent's prompt contains and **nothing governs how many are launched or on
  which model**. Solved by Sprint 022.
- **Long sessions** — `rules/loop_governance.md` bounds `/loop` iterations and nothing bounds
  **sprint size**. Solved by Sprint 021's bound.
- **High context** — `§4` cites the benchmark (pruning to 5 calls: 71% → 91.6% accuracy with
  **−63%** tokens) and then declares it cannot act. Long context is expensive **and less
  accurate**: stale results describe superseded states.

| # | Action | Attacks |
| :--- | :--- | :--- |
| 1 | Give `token-saver-auditor` a body or retire it | The rule with no auditor |
| 2 | **Consumption trigger, not intent**: a context or planned-subagent threshold loads the rule and requires declaring the cost | The 90% |
| 3 | **Re-evaluation by evidence, not announcement**: a new model in the list is a *candidate*; the trial is **one** sprint with authoring roles a tier lower, decided by variation in gate rounds (`SPRINT_LOG.md` already records `Gate N, round R — REJECTED`). Maximum cadence: once per release cycle, never mid-sprint. **First trial already declared**: `author` tier on `opus`+`low` versus `sonnet`+`medium` | Cost drift |

**Explicit limit:** the gates (`qa_agent`, `tester_agent`, `principal_agent`) **stay at the top
tier**. Across four consecutive host sprints every central defect was found by a gate and nothing
else, and several had survived their author's verification. Cheapening the reviewer is the first
thing a budget attacks and the last thing that helps.

---

## Program risks

Six holes no individual sprint owned. Not defects of a sprint: properties of the whole queue.

| # | Risk | Posture |
| :--- | :--- | :--- |
| **J1** | **The plan grows `agents.md` without budgeting it.** Several sprints edit it (`C0`, `C6`, `P1`, `P5`, `P7`, `U3`) and it is the only file loaded in **every session of every subagent**. A program whose thesis is token economy adds lines to the always-loaded file without counting the cost | **Declared ceiling:** `agents.md` does not exceed **200 lines** at the close of 029. Whatever does not fit moves to a lazy `rules/*.md`. `session_cost.py` can measure the effect: it is fixed cost × every subagent × every session |
| **J2** | **No sprint declares an abort criterion.** If `C3`'s regex produces false positives in production, nothing says what reverts it | Every sprint with code names its `workflows/remediation_workflow.md` trigger. For `C3` it is concrete: **a false positive blocking a host reverts the commit**, it is not hot-patched — the hook already blocked a host once for this |
| **J3** | **Sprint 023 has thirteen units and 021 imposes a session bound.** The first drafting of this risk claimed the anchor was already the continuity mechanism — **false, and verified**: `session_state.py` has two states and neither means "session closed, sprint open" | **Resolved in `M6` of 021**, not declared. Without it, `release()` mid-sprint sets a false baseline for `detect_drift`, and the next session must declare itself crash recovery |
| **J4** | **`T5` requires declaring documentary impact per sprint, and the ones already written lack it** | The obligation applies from 029 onward. Retro-applying it is rewriting without signal; each adds it when extracting its Implementation Plan at Phase 1 |
| **J5** | **Counting `scripts/` generates churn.** That directory grows almost every sprint, so the README would need editing each time — the very drift-generating pattern this program fights | The row is added **generated**, not hand-written: same pattern as `manifest_skills.json`, which `generate_manifest.py` produces and `check_manifest_parity.py` verifies. A figure a script writes cannot drift |
| **J6** | **A figure produced by a transformation, cited as if it came from the source.** Four instances in the session that drafted this: (a) *"6 commits outside `main` = squash-merge remnants"* — they were remote branches; (b) *"`task_scope.md` is not in `.gitignore`"* — it was, line 38; (c) *"`#37` at `CHANGELOG.md:44`"* — the 44 was the line number **within the filtered section**, the real one is 51; (d) the first drafting of this very row claimed a line-range gate *"would have caught all three"* — **it would have caught none**, verified | **The mitigation is not a range gate.** That check (resolving `file:line` under `docs/`) is cheap and enters **029** inside `verify_references.py`, but it only catches citations **out of range** — none of the four were. What works, and worked twice in this document, is **every measured claim carrying the command that reproduces it**: that is how `14 → 18` was corrected in `C0.2` and how `44 → 51` was found. Adopted as a drafting requirement in `T5`: *a figure without its command is not evidence, it is memory* |
