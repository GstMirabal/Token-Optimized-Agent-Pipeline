# 📜 ADR-0003: Gates never drop tier

**Status**: `Accepted`
**Date**: 2026-08-25
**Triggers**: 2, 6 (`rules/documentation_standard.md §3.1`)

**Last Audit Sprint**: 029
**Last Audit Date**: 2026-08-25

---

## 1. Context

Sprint 022 introduced three intent tiers (`gate` / `author` / `mechanical`) so
authoring roles stop running on the most expensive model by default. The first
budget cut a cost-driven program invites is to move reviewers down a tier.

Measurement cited when the program ordered the queue
(`docs/roadmaps/core/pipeline/021-030-program-queue.md`, Sprint 022 section):

| Claim | How to reproduce |
| :--- | :--- |
| Gate profiles are the `gate` tier in `config/model_tiers.json` | `python3 -c "import json; t=json.load(open('config/model_tiers.json'))['tiers']; print(t['gate'])"` |
| Author / mechanical sit below gate | Same command for `author` and `mechanical` |

Across four consecutive host sprints, every central defect that survived the
author's own verification was found by a gate and nothing else. Cheapening the
reviewer attacks the only role class that produced those findings.

## 2. Decision

**`qa_agent`, `tester_agent`, and `principal_agent` stay at the `gate` tier.**
No sprint, hotfix, or token-economy trial may reassign them to `author` or
`mechanical` without a new ADR that supersedes this one.

Under Cursor, "top tier" means the applied model logged from disk at gate time
while `cursor.gate.model` remains `null` until proven history exists (Design §D7
of Sprint 026) — not inventing a cheaper gate cell.

## 3. Consequences

**Easier**: budget pressure cannot silently erode the Double-Gate; Sprint 030's
re-evaluation protocol may trial cheaper **author** configurations only.

**Harder**: gate spend stays the fixed premium of the pipeline; hosts that want
cheaper reviews must change process (fewer units, smaller sprints), not tier.

## 4. Deciders

Program authors of `021-030-program-queue.md`; recorded as ADR in Sprint 029.

## 5. Considered Options

| Option | Pros | Cons |
| :--- | :--- | :--- |
| **Drop gates to `author`** | Immediate model-cost cut | Removes the independent context that caught every central defect in the four-sprint sample |
| **Trial gates one tier lower for one sprint** | Empirical | A single false green that merges is irreversible relative to the cost saved |
| **Keep gates at top (this ADR)** | Preserves the measured control | Gate spend remains high |

---
*Immutable once Accepted — a changed decision gets a new ADR that supersedes this one, never an in-place edit (`rules/documentation_standard.md §3`). File lives at `docs/decisions/ADR-0003-gates-never-drop-tier.md`.*
