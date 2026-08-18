# Plans written by the IDE

`plansDirectory` in the bridge template points here, so a plan drafted in an IDE
planning mode is written **inside the repository** instead of under
`~/.claude/plans/`.

## Why this directory exists

A host lost an approved Implementation Plan because it lived in ephemeral
storage, which is what `agents.md §4 ephemeral_memory` says will happen to
anything left there. The program roadmap that designed the fix was itself being
drafted outside version control while describing it, and the nucleus held two
Implementation Plans from April 2026 that survived four months on one machine and
existed in no clone.

## What this is NOT

**Not the canonical location, and the distinction is load-bearing.** Files here
carry IDE-generated names. The Implementation Plan that `agents.md §2 triple_lock`
names as its first lock is authored deliberately at Phase 1, to:

```
docs/sprints/[Sprint_ID]-[Stack]-[Layer]/IMPLEMENTATION_PLAN.md
```

Treating a generated name as that artifact would make the lock unverifiable —
`close_workflow.md` Phase 2.6 asks whether *this sprint* left its plan, and it
cannot ask that of a file named by an editor.

So: this directory is a **safety net against loss**. The canonical plan is
extracted from whatever lands here, deliberately, before Phase 5 approves it.

## Limits

- **Cursor does not read this setting** (`settings.json` is Claude Code's).
  Sprint `026` `P4` covers the other tool.
- **The close gate now reads the canonical path** — Sprint `023` `C0` declared it in
  `agents.md §0`, shipped `IMPLEMENTATION_PLAN_TEMPLATE.md`, and added
  `IMPLEMENTATION_PLAN.md` to the phase-artifact map in
  `scripts/docs_freshness_check.py`, which `close_workflow.md` Phase 2.6 demands.
  **It still does not read *this* directory, and it should not**: a file named by an
  editor cannot answer "did *this sprint* leave its plan".
- **What the gate proves is existence, not ordering.** It cannot show the plan was
  written before it was approved; that is held by the Phase 5 precondition in
  `pipeline_workflow.md`, an attended human step.
- **In nucleus mode `plansDirectory` never applies.** It ships in the bridge template,
  and `agents.md §5 nucleus_neutrality` prohibits installing the bridge when the
  workspace is `.agents` itself — measured: this repository has no
  `.claude/settings.json`, and `C0`'s own plan was drafted under `~/.claude/plans/`.
  Routed to Sprint `023` `C6`.
