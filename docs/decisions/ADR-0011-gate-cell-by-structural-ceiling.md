# 📜 ADR-0011: Gate cell by structural ceiling

**Status**: `Accepted`
**Date**: 2026-08-26
**Triggers**: 2 (`rules/documentation_standard.md §3.1`)

**Last Audit Sprint**: 035
**Last Audit Date**: 2026-08-26

**Related**: ADR-0003 · ADR-0005 · ADR-0010
**Supersedes (clause only)**: ADR-0003 §2 sentence that keeps
`cursor.gate.model` `null` until proven history exists.
**Does not supersede**: ADR-0003's rule that gate roles stay at the `gate`
tier and must not be demoted for cost; ADR-0005 (no prices in config).

---

## 1. Context

ADR-0003 keeps `qa_agent`, `tester_agent`, and `principal_agent` at the `gate`
tier. Under Cursor it also said `cursor.gate.model` remains `null` until proven
history exists, with the concern of that clause being **not inventing a cheaper
gate** — not leaving the cell empty forever.

Leaving the cell `null` makes the operational gate equal to whatever model the
human picker happened to choose for the session (ADR-0010: `--resolve gate`
returns `session`). That is an accidental gate, not a governed one.

`propose_tiers` wrongly tied gate proposals to proven history, treating a
**cost** question (when may we cheapen?) as a **fill** question (may we write
a non-null cell at all?). Proven history is the wrong gate for writing the
ceiling cell.

Prices and dollar ratios stay out of config (ADR-0005); this decision does not
reopen a price column.

## 2. Decision

**Fill `tiers.gate.cursor` by structural ceiling**, not by proven history and
not by cost.

| Criterion | Rule |
| :--- | :--- |
| Capability | Candidate must advertise `supportsAgent` |
| Health | `degradationStatus == 0` |
| Depth | Apply the depth lever among eligible candidates |
| Family | Gate family ≠ author family |
| Tie-break | Prefer the family already used for `gate.claude_code`, then larger context |
| Effort | Max effort exposed on the model's `parameterDefinitions` — **not** Claude's literal `high` label |

This fill **does not cheapen** the gate. It supersedes **only** the ADR-0003
clause that keeps `cursor.gate.model` null until proven history. All else in
ADR-0003 remains: roles stay at the `gate` tier; no cost-driven demotion.

## 3. Consequences

| Follow-on | Owner / bound |
| :--- | :--- |
| Write the non-null `gate.cursor` cell into `config/model_tiers.json` | Sprint 035 unit **H2** |
| Propose ceiling candidates via structural rules | Sprint 035 unit **E6** (`propose_tiers`) |
| Cheapening the gate via ledger / proven history | Future work — **out of** program window 034–038 |

**Easier**: Cursor Phase 7 gates resolve a real `(modelId, effort)` pair instead
of inheriting the chat picker; ADR-0010's null→`session` path becomes the
exception, not the default after H2.

**Harder**: catalog probes and ceiling selection must stay accurate; a wrong
ceiling is still a governance defect, even though it is not a cost demotion.

**Unchanged**: ADR-0003 role→`gate` binding; ADR-0005 (no prices in config);
ADR-0010 Task application of the map once the cell exists.

## 4. Deciders

Human owner during Sprint 035 planning; recorded as ADR in Sprint 035
(unit H1).

---
*Immutable once Accepted — a changed decision gets a new ADR that supersedes this one, never an in-place edit (`rules/documentation_standard.md §3`). File lives at `docs/decisions/ADR-0011-gate-cell-by-structural-ceiling.md`.*
