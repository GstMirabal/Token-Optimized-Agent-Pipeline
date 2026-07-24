# 📜 ADR-{{NUMBER}}: {{TITLE}}
**Status**: `Proposed | Accepted | Superseded by ADR-{{N}}`
**Date**: {{ISO_DATE}}
**Triggers**: {{TRIGGER_NUMBERS}} (`rules/documentation_standard.md §3.1`)

---

## 1. Context
The forces at play — technical, business, or otherwise. Facts only; make the case for the decision in Section 2, not here.

## 2. Decision
What was decided, stated plainly.

## 3. Consequences
What becomes easier or harder as a result. Include the negative consequences, not only the positive ones.

<!--
Sections 4-5 are MADR-only. Required if 2+ triggers fired simultaneously,
or if trigger #1, #3, #5, or #7 fired individually (severe/immediate-harm
class — rules/documentation_standard.md §3.2). Delete this whole block,
including this comment, for a Nygard-only ADR (a single trigger outside
that set).
-->

## 4. Deciders
Who was involved in making this call.

## 5. Considered Options
| Option | Pros | Cons |
| :--- | :--- | :--- |
| {{OPTION}} | {{PROS}} | {{CONS}} |

---
*Immutable once Accepted — a changed decision gets a new ADR that supersedes this one, never an in-place edit (`rules/documentation_standard.md §3`). File lives at `docs/decisions/ADR-{{NUMBER}}-{{slug}}.md`.*
