# 📜 ADR-0002: A drift verdict's exit code follows the required action, not the severity

**Status**: `Accepted`
**Date**: 2026-08-17
**Triggers**: 2, 6 (`rules/documentation_standard.md §3.1`)

---

## 1. Context

`scripts/detect_drift.py` compares `last_close_commit` against `HEAD` and exits `2` whenever the
range is non-empty. `workflows/start_workflow.md` Phase 0.4 consumes that exit code and, on `2`,
requires `/agents:reconcile` before any handoff to Planning.

Run against `main` at `a3c6f5f` (tag `v4.4.0`) on a clean tree, it exits `2` and prints:

> *"The Master Ledger's [Unreleased] section is empty, so none of it is recorded."*

The measurements say otherwise:

| Check | Result |
| :--- | :--- |
| `git status --porcelain` | empty |
| `#37` in the ledger | `CHANGELOG.md:51`, described in full |
| `a3c6f5f` | is the commit that sealed `[Unreleased]` as `[4.4.0]` |
| `git tag --points-at a3c6f5f` | `v4.4.0` |
| Both commits ancestors of `v4.4.0` | yes (`git merge-base --is-ancestor`) |

`[Unreleased]` is empty because emptying it is the post-condition of
`workflows/deployment_workflow.md` Phase 4 `ledger_seal`. Because that workflow never writes
`last_close_commit`, the first `/agents:start` after every deployment emits the false sentence by
construction.

The remedy the protocol names does not apply. `workflows/reconciliation_workflow.md` Phase 2
`classify` finds every commit already covered; Phase 3 `rebuild_ledger` forbids inventing entries;
Phase 8 `declare_unrecoverable` has nothing to declare.

Two adjacent facts constrain the decision:

- **The baseline is orphaned by every deployment.** `close_workflow.md` Phase 4 records
  `git rev-parse HEAD` while Phase 5 has pushed `ai-sprint/[ID]` and never `main`; deployment then
  squash-merges (0 merge commits since `v4.3.0`, over 10 commits). `git cat-file -e` cannot detect
  this — an orphaned commit still exists as a local object. It has never fired: `last_close_commit`
  entered in `7ccbde6` (Phase 019) and its only present value was set by hand during that phase's
  reconciliation.
- **`scripts/branch_sovereignty.py` refuses the sprint's own branch.** `local_branches()` excludes
  only the base, so `close_workflow.md` Phase 5.5 rejects the seal for the very branch Phase 6 of
  the same workflow declares will be unmerged.

## 2. Decision

The exit code of a drift check follows **the action required of the operator**, not the severity of
what was observed.

Five verdicts, derived from **sealing tags** — git tags whose version has a `## [X.Y.Z]` section in
`CHANGELOG.md`:

| Verdict | Condition | Exit |
| :--- | :--- | ---: |
| `S` sealed | no unsealed commits in range | **0** — report, name the tag, propose refreshing the baseline |
| `M` mixed | some unsealed, `[Unreleased]` empty | **2** — reconcile the enumerated commits |
| `U` unrecorded | all unsealed, `[Unreleased]` empty | **2** — reconcile |
| `A` indeterminate | unsealed exist, `[Unreleased]` non-empty | **2** — reachability cannot prove per-commit coverage; human read |
| `R` unverifiable | no sealing tags exist | **0** — state why |

An orphaned baseline is replaced by `git merge-base <baseline> HEAD` and **the substitution is
stated in the output**. `branch_sovereignty.py` additionally excludes the checked-out branch.

`S` and `R` are not silence: both report what they found and why they are not blocking.

## 3. Consequences

**Easier.** The check stops crying wolf after every deployment, so a `2` regains meaning. The
nucleus can close a sprint at all, which it could not before. An orphaned baseline degrades to a
narrower comparison instead of listing an entire branch history.

**Harder.** Verdict logic is more code than a boolean, and it depends on ledger sections and git
tags agreeing — a repository that tags without sealing gets `R` and no protection. The tag↔section
mapping becomes a maintained coupling.

**Accepted and declared, not hidden.** Reachability proves the *range* is covered by a published
section, never that each commit carries its own bullet — PRs `#26`-`#30` were ancestors of a tag
and still unrecorded. The tool states this in its `S` output so the verdict is not read as "every
commit documented."

**Narrowed on purpose.** Excluding the checked-out branch means a sovereignty audit run mid-sprint
no longer reports that sprint's own work. That is the gate's stated purpose — catching *branches
from earlier sprints* — and the anti-whitewash calibration test guards the rest.

**The reverting condition is explicit.** If the calibration test yields `S` for the Phase 018
scenario (baseline at a sealing tag, commits after it under no tag, `[Unreleased]` empty), the
change is reverted via `workflows/remediation_workflow.md`. A detector that certifies genuine
drift as sealed is worse than one that cries wolf, because a false clean verdict reads as evidence.

## 4. Deciders

Human operator and the lead agent, Sprint `024`. The reordering that put this sprint first — ahead
of the cost instrumentation it was queued behind — was a human decision taken after the defect
blocked the program's opening command.

## 5. Considered Options

| Option | Pros | Cons |
| :--- | :--- | :--- |
| **Verdict-dependent exit codes** (chosen) | A `2` means an action is required, so it stays credible. `S` still reports. Handles the orphaned baseline in the same pass | More logic than a boolean; couples the check to the tag↔ledger-section mapping |
| **Keep exit `2` on all five verdicts** — the original design | Simplest change; never under-reports | Refuted by execution: under `S` reconciliation has no precondition to satisfy. A gate demanding recovery of what is not broken is the gate that gets disabled — a failure this repository has already recorded in `CHANGELOG.md [4.4.0]`: *"a gate with no answer gets disabled rather than satisfied"* |
| **Reconcile now, leave the detector alone** | Zero code; follows Phase 0.4 literally | Reconciliation's own preconditions are unmet — nothing to classify, nothing to rebuild. Updates one anchor field and the false sentence returns at the next deployment. Sprint `021` `M6` would then design new `last_close_commit` semantics on top of a reader that misreads it |
| **Hotfix under `RA-03`** | Fastest path to an unblocked pipeline | The first act of a program about traceability would bypass traceability. The design here — five verdicts, tag↔section mapping, calibration — is too substantial for `docs/hotfixes/` |

---
*Immutable once Accepted — a changed decision gets a new ADR that supersedes this one, never an in-place edit (`rules/documentation_standard.md §3`). File lives at `docs/decisions/ADR-0002-drift-verdict-exit-codes.md`.*
