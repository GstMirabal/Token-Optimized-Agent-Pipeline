# 🚑 Hotfix: {{H-ID}}-{{LAYER}}
**File**: `docs/hotfixes/{{H-ID}}-{{LAYER}}.md` (RA-03 emergency naming — sanctioned exception to RA-06)
**Severity**: `CRITICAL | HIGH`
**Detected**: {{ISO_DATE}} · **Resolved**: {{ISO_DATE}}

---

## 1. Symptom
What broke, observed where, and blast radius. One paragraph, facts only.

## 2. Root Cause
The actual defect (not the symptom). Reference exact files/lines.

## 3. Fix Applied
| File | Change |
| :--- | :--- |
| {{PATH}} | {{ONE_LINE_CHANGE}} |

Branch/commit: `hotfix/{{H-ID}}` → `{{COMMIT}}` (hotfixes may merge outside the sprint cycle, but never unreviewed).

## 4. Verification
Exact commands/tests proving the fix, and the regression test added (mandatory — a hotfix without a pinning test WILL recur).

## 5. Rule Amendment Check
- [ ] Is this failure class systemic (a process pattern, not a one-off)? If yes → draft a `RA-XX` amendment via `constitutional_escalation` and link it here: {{RA_REF_OR_N/A}}
- [ ] Does the root cause reveal a design decision worth recording (not a process pattern — a specific architectural choice)? If yes → draft an ADR (`rules/documentation_standard.md §3.1`, trigger criteria apply) and link it here: {{ADR_REF_OR_N/A}}
- [ ] Master Ledger entry added under `[Unreleased]`.
