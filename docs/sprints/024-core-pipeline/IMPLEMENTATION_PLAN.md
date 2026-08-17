---
description: "Implementation Plan — Sprint 024 close-machinery verdicts"
status: "APPROVED"
version: 1.0.0
approved_by: human
approved_at: "2026-08-17"
---

# Implementation Plan: Sprint 024 - Close Machinery Verdicts

**Branch:** `ai-sprint/024` · **Base:** `main` at `a3c6f5f`, tag `v4.4.0`

This is the first Implementation Plan the nucleus has kept under version control. Sprint `023`
`C0` makes that a rule; this file establishes the path it will declare, four sprints early,
because the defect that motivates `C0` is the one that blocked this sprint's own start.

**`RA-06` deviation, declared:** named `[NNN]-[slug]-IMPLEMENTATION_PLAN.md` rather than
`[MODULE]_[TYPE].md`, so the plan sorts beside the roadmap it implements. The numeric prefix is
this directory's standing convention since `000-`; `RA-06` compliance would separate a plan from
its own roadmap in the listing. Declared, as `RA-03` declares its own.

**Decision record:** `docs/decisions/ADR-0002-drift-verdict-exit-codes.md` — required by
`rules/documentation_standard.md §3.1` triggers #2 and #6, escalated to MADR by §3.2.

## Context

`workflows/start_workflow.md` Phase 0.4 runs `scripts/detect_drift.py` before anything else. On a
clean tree at `v4.4.0` it exits `2` and states that the ledger records none of the commits it
found. That statement is false: both are described under `## [4.4.0]`.

Reconciliation — the remedy the protocol names — has nothing to do here.
`workflows/reconciliation_workflow.md` Phase 2 `classify` finds every commit covered, Phase 3
`rebuild_ledger` forbids inventing entries, and Phase 8 has nothing to declare unreconstructable.
Running it would update one anchor field and leave the detector lying until the next deployment:
satisfying a gate instead of fixing it, which this repository has already written down as the
failure mode to avoid — *"a gate with no answer gets disabled rather than satisfied"*.

Verifying that defect surfaced two more. All three are in `docs/roadmaps/core/pipeline/024-close-machinery-verdicts.md`.

## Design

### D0 — an orphaned baseline degrades, it does not lie

When `git merge-base --is-ancestor <baseline> HEAD` fails, the recorded baseline is off-branch —
the normal outcome once `deployment_workflow.md` squash-merges the sprint branch whose HEAD the
close recorded. Substitute `git merge-base <baseline> HEAD`, **state the substitution in the
output**, and run the verdict logic from there.

`git cat-file -e` cannot serve here: an orphaned commit still exists as a local object.

**This ships before the close that would need it.** `last_close_commit` entered in `7ccbde6`
(Phase 019) and its only present value was set by hand during that phase's reconciliation, so no
normal close has written one yet. This sprint's close would be the first.

### D1-D3 — five verdicts, and an exit code that follows the required action

A **sealing tag** is a git tag whose version has a `## [X.Y.Z]` section in `CHANGELOG.md`. Derived,
never hardcoded. Verified today: 0 ledger sections lack a local tag; exactly `v3.4.0` and `v3.5.2`
are tags without a section.

```
total    = git rev-list --count HEAD ^baseline
unsealed = git rev-list --count HEAD ^baseline ^<tag1> ^<tag2> …
```

| Verdict | Condition | Exit | Action |
| :--- | :--- | ---: | :--- |
| `S` sealed | `unsealed == 0` | **0** | Name the covering tag and **propose** refreshing the baseline. Require nothing |
| `M` mixed | `0 < unsealed < total`, `[Unreleased]` empty | **2** | Reconcile the unsealed commits, enumerated |
| `U` unrecorded | `unsealed == total`, `[Unreleased]` empty | **2** | Reconcile. This is the Phase 018 case |
| `A` indeterminate | unsealed exist and `[Unreleased]` is **not** empty | **2** | They may be recorded there; reachability cannot prove it per commit. Say so, ask for a human read |
| `R` unverifiable | no sealing tags at all | **0** | State why, as the existing "no baseline" branch already does |

**The exit code follows the required action, not the severity.** An earlier design kept `2` on all
five, reasoning that the drift is real and only the sentence was false. Live execution refuted it:
under `S` there is nothing for reconciliation to do, and a gate demanding recovery of what is not
broken is the gate that gets disabled.

`S` is not silence. It reports the commits, names the sealing tag, and proposes the refresh —
`session_probe.py` doctrine: propose, never execute.

**Declared limit:** reachability proves the *range* is covered by a published section, not that
each commit has its own bullet. PRs `#26`-`#30` ended up ancestors of a tag and were still
unrecorded. The output says this, so `S` is not read as "every commit documented".

**Not touched:** `deployment_workflow.md` still does not write `last_close_commit`. That field
means "the commit where the last close sealed"; letting a deployment advance it would make the
name lie. Staleness is absorbed by the detector understanding tags, not by the deployment
falsifying the field.

`unreleased_is_empty()` is kept: it remains the correct signal separating `U`/`M` from `A`. What
was false was the conclusion drawn from it, not the measurement.

### D7 — the branch being sealed is not an abandoned branch

`local_branches()` additionally excludes the currently checked-out branch. The gate's stated
purpose — its docstring and its `CHANGELOG` entry — is catching *"branches from earlier sprints"*
left behind. The branch whose close is executing is not a forgotten branch; it is the subject of
the close. Excluding it does not weaken the gate, it returns it to what it says it does.

`config/abandoned_branches.json` is not the answer: it requires a reason, and its own rule states
that an unexplained "abandoned" is indistinguishable from work someone forgot.

## Work

| # | Action | File |
| :--- | :--- | :--- |
| D0 | Orphaned baseline → `merge-base` substitution, declared in output. **First: without it the sprint breaks at its own close** | `scripts/detect_drift.py` |
| D1 | Derive sealing tags by crossing `git tag` with `## [X.Y.Z]` ledger sections | `scripts/detect_drift.py` |
| D2 | The five verdicts and their exit codes | `scripts/detect_drift.py` |
| D3 | Output naming the verdict, its evidence, and the reachability limit | `scripts/detect_drift.py` |
| D4 | Tests: anti-whitewash calibration, the five verdicts, the four existing regressions | `tests/test_session_protocol.py` |
| D5 | Phase 0.4 states the verdicts and what each requires | `workflows/start_workflow.md` |
| D6 | `invoked_by: start_workflow.md#drift_check` left intact (`RA-16`, `verify_references.py` check (d)) | `scripts/detect_drift.py` |
| D7 | The checked-out branch is excluded from the sovereignty audit | `scripts/branch_sovereignty.py`, `workflows/close_workflow.md` 5.5 |
| D8 | Sprint documentation, written before the code | `docs/roadmaps/core/pipeline/024-*.md` |

## Tests

| Check | Must fail against the current tree |
| :--- | :--- |
| **Anti-whitewash calibration**: synthetic repo, baseline at a sealing tag, 2 commits after, no new tag, `[Unreleased]` empty → **`U`, exit 2** | No — this is the guarantee the fix does not whitewash genuine drift. **If this yields `S`, the sprint is reverted** |
| **Live acceptance**: this repository, untouched → **`S`, exit 0**, naming `v4.4.0` | **Yes** — today exit 2 with the false sentence |
| Mixed: 2 commits, sealing tag on the first, 1 more after → **`M`, exit 2**, listing only the unsealed one | **Yes** |
| `[Unreleased]` non-empty with unsealed commits → **`A`, exit 2**, stating it cannot prove per commit | **Yes** |
| No sealing tags at all → **`R`, exit 0** stating why | **Yes** |
| A tag **without** a ledger section (`v3.4.0`, `v3.5.2`) does not count as sealing | **Yes** |
| `S` output declares reachability ≠ per-commit bullet | **Yes** |
| **D0**: repo with a squash-merged branch, baseline at the dead branch commit → substitutes `merge-base`, **declares it**, does not list the whole range | **Yes** — today `cat-file -e` passes and the range is meaningless |
| D0: a baseline that **is** an ancestor of HEAD is not substituted | No — regression to protect |
| **D7**: sprint branch checked out with its own commits → `audit` exits **0**; the same branch not checked out and unintegrated still exits **2** | **Yes** on the first half, **No** on the second — the second is what the gate exists to catch |
| The 4 existing drift tests (`tests/test_session_protocol.py:123`-158) stay green unedited | No — regression to protect |
| The 4 existing sovereignty tests (`tests/test_session_protocol.py:79`-118) stay green unedited | No — regression to protect |
| `make verify` green, `invoked_by` intact | No |

## Execution

Sequential; the delegation conflict and the per-artifact ruleset are declared in the sprint
roadmap's §Delegation and §Task scope.

**Gates every commit must pass:** `hooks/on_commit_msg.py` (Conventional Commits + `#024` suffix);
`hooks/on_commit.py` `audit_regression_test` — a `fix(` touching `scripts/` must carry its test in
the same stage, which is why D0-D4 ship as one commit.

| Order | Commit |
| :--- | :--- |
| 0 | `docs(roadmap): the sprint plan lives in the repository before the first line of code #024` |
| 1 | `fix(scripts): a sealed commit is not drift, and the ledger already said so #024` |
| 2 | `fix(scripts): the branch a close is sealing is not an abandoned branch #024` |
| 3 | `docs(workflows): the drift check reports a verdict, not a boolean #024` |

Commit `0` goes first and is not ceremony: if the session dies mid-`D1`, the plan survives. That is
precisely what did not happen to the two April 2026 plans this sprint found untracked.

## Out of scope

| Exclusion | Reason |
| :--- | :--- |
| `deployment_workflow.md` writing `last_close_commit` | Would make the field's name lie. The detector absorbs staleness |
| Verifying each commit has its own ledger bullet | Would require parsing prose and attributing it to commits. The detector **declares** the limit instead of pretending to cover it |
| Reconciling `.gitignore` with the nucleus's own-project role | Recorded as `F-024-D4`, routed to Sprint `023` `C0` |
| `M6` of Sprint `021` (the `SUSPENDED` state) | Belongs to `021`. This sprint fixes the **reader** of `last_close_commit`; `021` adds the writer |

## Abort criterion

`workflows/remediation_workflow.md` triggers if the anti-whitewash calibration yields `S` for the
Phase 018 scenario. A drift detector that certifies genuine drift as sealed is worse than one that
cries wolf, because the false verdict reads as evidence.
