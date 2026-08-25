# 🚑 Hotfix: H-005-pipeline
**File**: `docs/hotfixes/H-005-pipeline.md` (RA-03 emergency naming — sanctioned exception to RA-06)
**Severity**: `HIGH`
**Detected**: 2026-08-25 · **Resolved**: 2026-08-25

---

## 1. Symptom

Sprint task scopes assigned file-mutating work to agent profiles that declare no
`Write` and no `Edit` tool, and the sprint records marked those units executed
successfully. Measured over the sprints whose tables carry `Model`/`Effort`
columns, this is **32 rows across five consecutive sprints, 028 through 032**.
Whatever produced those files, it was not the profile the record names — so for
32 units the record of who did the work is wrong, and `jurisdictional_lock`,
which is enforced per assignee, was enforced against a name that could not act.

| Sprint | Rows | Profiles named |
| :--- | :--- | :--- |
| 028 | 3 | `devops_agent` ×2, `principal_agent` ×1 |
| 029 | 8 | `devops_agent` ×6, `principal_agent` ×2 |
| 030 | 13 | `devops_agent` ×9, `token_economy_agent` ×3, `principal_agent` ×1 |
| 031 | 5 | `devops_agent` ×3, `qa_agent` ×1, `tester_agent` ×1 |
| 032 | 3 | `devops_agent` ×2, `token_economy_agent` ×1 |
| **033** | **0** | — the sprint `ADR-0009` created `implementer_agent` |

Two of these are role usurpation on their face: `qa_agent` and `tester_agent`
(031 `R2`, `R3`) were assigned to modify files, when `ADR-0008` gives a gate a
verdict to emit and no file to write. `principal_agent` was assigned four
mutations across 028–030, and `agents.md §6` gives it the Approval Gate, not an
editor.

The same shape exists earlier and is **deliberately not counted here**: 026 has
44 such rows and 027 has 20, but both predate the `Model`/`Effort` columns and
`scripts/check_task_scope.py` skips sprints before 028 by design. Sprints 021
through 025 name their assignee `lead`, a vocabulary that predates the profile
tree, and are not comparable at all.

## 2. Root Cause

Two independent gaps, either of which alone would have caught this.

**No capability check existed.** `scripts/check_task_scope.py` read the
`Assignee` column only to decide whether a *mechanical* profile at *high* risk
carried an escalation note (`_mechanical_high_findings`). Nothing compared the
assignee against the `tools:` frontmatter of `agents/[profile].md`, so an
assignment that no runtime could execute was indistinguishable from a valid one.

**No implementer role existed until 033.** Before `ADR-0009` there was no
profile owning framework-root `scripts/`, `hooks/` and `tests/` with `Write`
and `Edit`. Authors reached for `devops_agent` because it was the closest thing
to "the one that touches infrastructure" — it holds `Bash` and nothing else.
That 033 measures clean is the corroboration: the defect stopped the sprint the
role appeared, three sprints before anything detected the previous five.

## 3. Fix Applied

| File | Change |
| :--- | :--- |
| `scripts/check_task_scope.py` | `_capability_findings` refuses a mutating row whose assignee declares no `Write`/`Edit`, and one naming a profile with no file at all |
| `scripts/check_task_scope.py` | `profile_tools` resolves `agents/[name].md` and `profiles/*/agents/[name].md` |
| `tests/test_check_task_scope.py` | Three pinning tests, plus two fixtures corrected — they assigned `devops_agent` a `modify`, the exact defect |

Branch/commit: `ai-sprint/034` → `3dc95db`. **Deviation from RA-03, stated
rather than hidden**: there is no `hotfix/H-005` branch. This is a retrospective
record of a defect found while auditing, not an emergency interrupting a sprint,
and the fix is unit `I4` of the 034 plan. RA-03 exists to let emergency speed
bypass Option B naming; borrowing its document shape for a planned fix keeps the
finding discoverable, and inventing an emergency branch for it would be theatre.

## 4. Verification

```bash
# The five sprints, before the fix: exit 0. After: exit 2 with the rows named.
for s in 028 029 030 031 032 033; do
  python3 scripts/check_task_scope.py --sprint-dir docs/sprints/$s-core-pipeline
done
# 028..032 exit 2 (3, 8, 13, 5, 3 findings). 033 exits 0.

.agents/venv_skillopt/bin/python3 -m pytest tests/test_check_task_scope.py -q
# 10 passed. The three new tests fail against the previous implementation.
```

Regression pinning: `test_assignee_without_write_tool_fails` (a mutating row
assigned to `devops_agent` must exit 2) and `test_assignee_with_no_profile_file_fails`
(an assignee with no profile must exit 2, not be treated as unconstrained).

## 5. Rule Amendment Check

- [x] Is this failure class systemic? Yes, and it is already recorded as design
  section `D17` of `docs/sprints/034-core-pipeline/IMPLEMENTATION_PLAN.md`
  ("absence approves"): three separate checks treated a condition they could not
  evaluate as a condition that passed. No new `RA-XX` is drafted here because
  `D17` and unit `I4` fix the mechanism; a rule restating what the check now
  enforces would be a rule nothing reads. Revisit at sprint close if the same
  shape appears in a fourth check.
- [x] Does the root cause reveal a design decision worth recording? Already
  recorded: `ADR-0009` (implementer role) is the decision whose absence caused
  the misassignment, and `D14` of the 034 plan fixes who assigns agents.
- [ ] Master Ledger entry added under `[Unreleased]` — pending sprint close.
