# Hotfix: H-004-cursor
**File**: `docs/hotfixes/H-004-cursor.md` (RA-03 emergency naming — sanctioned exception to RA-06)
**Severity**: `HIGH`
**Detected**: 2026-08-25 · **Resolved**: 2026-08-25

---

## 1. Symptom

Under Cursor, three consecutive Plan mode sessions left Phase 1's deliverable
off the canonical path. The editor stored `~/.cursor/plans/<generated>.plan.md`
and forbade writing `docs/sprints/[ID]-[Stack]-[Layer]/IMPLEMENTATION_PLAN.md`.
`triple_lock` lock 1 could not close. Blast radius: every host session with
`session_tool: cursor` that follows `pipeline_workflow.md` Phase 1.

## 2. Root Cause

`workflows/pipeline_workflow.md` Phase 1 instructed: *Where the environment
offers planning mode, Phase 1 runs in it.* Under Cursor that mode cannot write
the file the same cell names as the deliverable. `plansDirectory` does not
apply (`docs/plans/README.md`: Cursor does not read `settings.json`). The
unqualified sentence is an instructing-document defect (C6 / `F-093-G1` class
`instructing`), not a missing Cursor product feature.

## 3. Fix Applied

| File | Change |
| :--- | :--- |
| `workflows/pipeline_workflow.md` | Phase 1: `SwitchMode` to plan is PROHIBITED when `session_tool: cursor` (`RA-18`) |
| `workflows/start_workflow.md` | `pipeline_invocation` names the same prohibition |
| `agents/principal_agent.md` | `consensus_loop` names `SwitchMode` PROHIBITED under Cursor |
| `agents.md` | `RA-18: CURSOR_PHASE1_NO_PLAN_MODE` |
| `docs/guides/AUTONOMY_POSTURE_GUIDE.md` | Cursor counterpart row for Plan mode |
| `docs/plans/README.md` | Limit: `~/.cursor/plans/` is not the lock |
| `docs/roadmaps/core/pipeline/021-030-program-queue.md` | C0 second clause annotated as Claude-only |
| `tests/test_cursor_phase1.py` | Pins the unqualified sentence stays gone |

Branch/commit: `hotfix/H-004` → SHA recorded by git.

## 4. Verification

```bash
./venv_skillopt/bin/python -m pytest tests/test_cursor_phase1.py
grep -n 'Where the environment offers planning mode, Phase 1 runs in it' workflows/pipeline_workflow.md; echo $?
# expected: no match, grep exit 1
wc -l agents.md
# expected: ≤ 200
```

## 5. Rule Amendment Check

- [x] Systemic → `RA-18: CURSOR_PHASE1_NO_PLAN_MODE` in `agents.md` §7
- [ ] No new ADR: the architectural choice (canonical sprint path vs IDE-generated name) is already `agents.md` §0 / `docs/plans/README.md`. This hotfix stops an instructing document from voiding that choice.
- [x] Master Ledger entry under `[Unreleased]`.
