---
description: "Close-machinery verdicts — drift, orphaned baselines, branch sovereignty (Sprint 024)"
status: "IN_PROGRESS"
version: 1.0.0
---

# Roadmap: Sprint 024 - Close Machinery Verdicts

## Status
- **Strategy Lock:** `OPEN`
- **Completion:** 0% — 4 commits planned
- **Sprint ID:** `024` — **not sequential after `020`, deliberately.** This sprint was queued
  fourth in a nine-sprint program and promoted to first when its defect blocked the program's
  own start. IDs are labels, not positions; renumbering was rejected because it was the single
  largest source of defects in that program's own audit. This directory therefore reads
  `018, 019, 020, 024, 021, …`. **That gap is a decision, not lost files.**
- **Branch:** `ai-sprint/024`, from `main` at `a3c6f5f` (tag `v4.4.0`).
- **`RA-06` deviation, declared:** this file is named `[NNN]-[slug].md`, not `[MODULE]_[TYPE].md`.
  The deviation is the standing convention of this directory — every file from `000-` onward uses
  it, because a roadmap sorts by phase and `[MODULE]_[TYPE]` does not sort at all. Renaming this
  one file to comply would make it unfindable beside its own series. Declared here rather than
  left as drift, the way `RA-03` declares its own sanctioned deviation.

## Objective

Make three close-machinery controls return the verdict they claim to return.

All three were found by *running* the protocol, not by reading it — the same way `F-093-N2` was
found, and the reason `RA-16`'s precedent exists. The first blocked this program's opening
command; verifying it surfaced the second; siting this file surfaced the third.

## Work Breakdown

| Commit | Track | Scope | Status |
| :--- | :--- | :--- | :--- |
| 0 | **Documentation** | This roadmap and the Implementation Plan, written before any code | ⏳ |
| 1 | **A — drift verdicts** | `detect_drift.py`: orphaned baseline, five verdicts, exit code follows required action | ⏳ |
| 2 | **B — branch sovereignty** | `branch_sovereignty.py`: the checked-out branch is not an abandoned branch | ⏳ |
| 3 | **C — protocol text** | `start_workflow.md` Phase 0.4 states the verdicts | ⏳ |

## The three defects

### A.1 — a sealed commit was reported as drift

`scripts/detect_drift.py` computes `baseline..HEAD` and calls everything it finds "outside the
protocol". That range mixes two populations: commits genuinely unrecorded, and commits sealed
into a **published** ledger section. It then prints *"the [Unreleased] section is empty, so none
of it is recorded"* — but emptying that section is the post-condition of
`workflows/deployment_workflow.md` Phase 4 `ledger_seal`.

Because `deployment_workflow.md` never touches `last_close_commit`, the first `/agents:start`
after every deployment emits that sentence **by construction**.

Measured against `v4.4.0` on a clean tree:

| Check | Result |
| :--- | :--- |
| `git status --porcelain` | empty |
| `python3 scripts/detect_drift.py` | exit `2` |
| `#37` in the ledger | `CHANGELOG.md:51`, described in full |
| `a3c6f5f` | is the commit that *sealed* `[Unreleased]` as `[4.4.0]` |
| `git tag --points-at a3c6f5f` | `v4.4.0` |
| Both ancestors of `v4.4.0` | yes (`git merge-base --is-ancestor`) |

### A.2 — the baseline is orphaned by every deployment

`workflows/close_workflow.md` Phase 4 `state_sync` records `git rev-parse HEAD`, while Phase 5
`atomic_commit` has pushed `ai-sprint/[ID]` and **never `main`**. Deployment then integrates with
`gh pr merge --squash`, so that commit never becomes an ancestor of `main`.

`git cat-file -e` does not catch it: an orphaned commit still exists as a local object.

**It has never fired.** `last_close_commit` was introduced in `7ccbde6` (Phase 019), and its only
present value was set by hand during that phase's reconciliation. The first normal close to write
it would be this one — which is why the fix ships before the close that would need it.

### B — the close gate refuses the sprint's own branch

Phase 5.5 `branch_audit` refuses the seal while any local branch holds work outside `main`.
Phase 6 `deployment_handoff` of the same workflow states the sprint branch is pushed and
**unmerged**. The two contradict each other.

| Step | Evidence |
| :--- | :--- |
| `local_branches()` | returns `refs/heads/` minus `base` — the active sprint branch is included |
| `content_is_integrated()` | `git cherry main ai-sprint/024` returns `+<sha>` once a commit exists → `False` |
| `merged_pr_exists()` | `gh` is present, but no merged PR for this branch → `False` |
| `classify()` | neither → `unintegrated` → `audit()` exits `2` → the seal is refused |

Verified by construction. `audit` passes today only because the branch has no commits yet; it
prints `✅ ai-sprint/024 — work is in main`, which stops being true at the first commit.

**The waiver is not the answer.** `config/abandoned_branches.json` requires a reason, and its own
rule states that an unexplained "abandoned" is indistinguishable from work someone forgot.
Declaring the active branch abandoned would be lying to the gate to pass it.

## Scope limit

A fourth finding surfaced while siting this file and is **recorded, not fixed here**: the nucleus
excludes its own pipeline state from version control — the anchor (`.gitignore:16`), the sprint
hierarchy (`:18`), the state mirror (`:19`), `implementation_plan*` in eight extensions
(`:21-28`) and `task_scope.md` (`:38`).

That exclusion is **correct** for the role its header names — *"Ignored by Global Submodule"* — it
is `RA-15` in `.gitignore` form, keeping a host's records out of the shared nucleus. The defect is
the collision with the repository's *other* role: the nucleus also runs the pipeline on itself, and
for its own sprints those are exactly the artifacts the close depends on.

Two consequences recorded for Sprint `023` (`C0`):

- `docs/sprints/core/pipeline/` holds two Implementation Plans from April 2026 (sprints `031` and
  `032`, from the numbering that preceded the phase renumbering) that are **untracked**. They
  survived four months on one machine; a clean clone does not have them.
- `scripts/docs_freshness_check.py:418` warns when `docs/sprints/{NNN}*` is missing — a directory
  `.gitignore` guarantees absent in any clean clone. A control firing on a correct state.

This sprint writes nothing under `docs/sprints/`, so it does not deepen the problem.

## Delegation

Executed **sequentially**. The session configuration forbids spawning subagents while
`agents.md §6` requires eight roles per pipeline pass. The conflict is reported here rather than
resolved silently, per `workflows/start_workflow.md` Phase 2 `delegation_conflict`, whose own
precedent is a sprint that ran alone without saying so and had Phases 4 and 7 never execute.

Writes are emitted under the ruleset of the profile that governs each artifact, because
`F-021-A2` leaves `scripts/` and `hooks/` with no owning profile. The deviation is recorded here
so the structural gate audits it rather than discovers it.

## Task scope

Recorded in this file rather than in a root `task_scope.md`: `.gitignore:38` excludes that name,
so the artifact would be lost exactly as the two April plans were.

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `docs/roadmaps/core/pipeline/024-close-machinery-verdicts.md` | create | low | lead (doc_orchestrator ruleset) | ⏳ |
| 2 | `docs/roadmaps/core/pipeline/024-close-machinery-verdicts-IMPLEMENTATION_PLAN.md` | create | low | lead (principal_agent ruleset) | ⏳ |
| 3 | `scripts/detect_drift.py` | modify | **high** — a gate | lead (devops_agent ruleset) | ⏳ |
| 4 | `tests/test_session_protocol.py` | modify | medium | lead (tester_agent ruleset) | ⏳ |
| 5 | `scripts/branch_sovereignty.py` | modify | **high** — a gate | lead (devops_agent ruleset) | ⏳ |
| 6 | `workflows/start_workflow.md` | modify | low | lead (doc_orchestrator ruleset) | ⏳ |
| 7 | `CHANGELOG.md` | modify | low | lead (doc_orchestrator ruleset) | ⏳ |

**`loop_guard` limitation, declared:** `scripts/loop_guard.py:38` reads `Path("task_scope.md")` at
the repository root and will not find this table. It does not affect this sprint — that guard only
acts under `/loop`, which is not used here — but it is `G-03` reproducing, and it is noted rather
than left to be rediscovered.

## Findings recorded

| ID | Finding | Disposition |
| :--- | :--- | :--- |
| `F-024-D1` | A sealed commit reported as drift | Fixed, commit 1 |
| `F-024-D2` | The baseline is orphaned by every squash-merge deployment | Fixed, commit 1 |
| `F-024-D3` | The close gate refuses the sprint's own branch | Fixed, commit 2 |
| `F-024-D4` | The nucleus gitignores its own pipeline state | **Recorded**, routed to Sprint `023` `C0` |
