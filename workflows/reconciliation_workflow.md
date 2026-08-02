---
description: "Protocol-Failure Reconciliation (Keyword: reconcile)"
version: 1.0.0
invoked_by: human:/agents:reconcile, start_workflow.md#drift_check
---

# 🧭 Workflow: Reconciliation (Protocol-Failure Recovery)

Restore traceability for work that happened **outside** the protocol: commits
made without `start`, without `close`, or without either.

> [!IMPORTANT]
> **This workflow reverts nothing.** The work is good; what is missing is its
> record. Confusing this with `workflows/remediation_workflow.md` — which
> revokes bad work with `git restore .` after three consecutive rejections —
> would destroy exactly the work that needs documenting.

## Why it exists

Five pull requests (`#26`-`#30`) were merged after tag `v4.3.0` with no
`CHANGELOG.md` entry, no roadmap phase record, and `docs/active_state.json`
frozen at sprint `017` dated `2026-07-27` while work continued to `2026-08-02`.
Nothing noticed, because nothing could compare: the anchor recorded no commit.

The procedure below is not a design. It is the transcript of the recovery that
was performed by hand on that exact drift, written down so the next one costs a
command instead of an investigation.

## Precedence

`start_workflow.md` runs `scripts/detect_drift.py` **before** claiming the
session and before handing off to Planning. When it exits `2`, this workflow
runs first. New work stacked on a state that misreports the repository
multiplies the inconsistency rather than resolving it.

## Execution Flow

| Phase | Step | Action / Constraint |
| :--- | :--- | :--- |
| **1** | `delimit` | `git log <last_close_commit>..HEAD`. A closed, enumerated range — never "the recent commits". If no baseline exists, use the last release tag and say so in the record. |
| **2** | `classify` | For each commit in the range, decide whether the Master Ledger already covers it. Output: every commit either covered or listed as orphaned. |
| **3** | `rebuild_ledger` | Write the missing `CHANGELOG.md` `[Unreleased]` entries **from the commit bodies and the diffs**. **Inventing is prohibited**: what a commit does not state is not written. A reconstructed entry that guesses intent is worse than an absent one, because it reads as evidence. |
| **4** | `rebuild_phase` | Reconstruct the roadmap phase record under `docs/roadmaps/`, marked as reconstructed and citing the commit range it was derived from. |
| **5** | `resync_state` | Update `docs/active_state.json` and refresh `.agent_state/mirror.json`. The next `close` writes `last_close_commit`, which restores the baseline drift detection needs. |
| **6** | `rebuild_graph` | `graphify update .` — the graph predates the drifted work by definition. |
| **7** | `regate` | `make verify` green, including the full test suite. Reconciliation that leaves a gate red has traded one inconsistency for another. |
| **8** | `declare_unrecoverable` | State plainly what could **not** be reconstructed. An unreconstructable item that is named is a record; one that is quietly filled in with a plausible guess is a fabrication. |

## What this does not do

- **It does not merge, push, or revert.** Integration is
  `workflows/deployment_workflow.md`'s job (`RA-12`); reverting is
  `workflows/remediation_workflow.md`'s.
- **It does not judge the work.** Whether the drifted commits were a good idea
  is the audit's question. This restores their record.

---
*Written from the recovery performed on the `v4.3.0`-`#30` drift, Phase 019.*
