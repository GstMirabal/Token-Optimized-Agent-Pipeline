# 🏁 Walkthrough: {{MODULE}}
**File**: `docs/walkthroughs/{{MODULE}}_WALKTHROUGH.md` (RA-06 Option B naming)
**Last updated**: Sprint #{{SPRINT_ID}}

---

## 1. What was achieved
| Sprint | Milestone | Outcome |
| :--- | :--- | :--- |
| #{{ID}} | {{MILESTONE}} | {{ONE_LINE_RESULT}} |

## 2. Current state
One short paragraph: what works today, verified how (tests, manual run). Link the Blueprint it implements: `docs/architecture/{{MODULE}}_BLUEPRINT.md`.

## 3. Known limitations / tech debt
| Item | Marked as | Tracked where |
| :--- | :--- | :--- |
| {{LIMITATION}} | `:tech-debt:` | {{SPRINT_OR_HOTFIX_DOC}} |

If a limitation exists *because* of a deliberate decision (not just unfinished work), link the ADR that made that call instead of re-explaining it here: `docs/decisions/ADR-{{NUMBER}}-{{slug}}.md` (`rules/documentation_standard.md §1`).

## 4. How to operate it
Minimum commands to run/verify the module (deterministic, prefixed paths per agents.md §3):

```bash
{{RUN_COMMAND}}
{{VERIFY_COMMAND}}
```

---
*Updated at every Sprint Closeout touching this module (RA-05).*
