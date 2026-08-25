# 📜 ADR-0006: Session bound before tiering

**Status**: `Accepted`
**Date**: 2026-08-25
**Triggers**: 6 (`rules/documentation_standard.md §3.1`)

**Last Audit Sprint**: 029
**Last Audit Date**: 2026-08-25

---

## 1. Context

Usage reports that opened the 021–030 program attributed roughly **95% of spend**
to sessions active 8+ hours and **90%** to contexts above 150k tokens. A
corrected transcript shape (cache_read drops >50% from above 100K) showed four
context cycles in one session with peak ratios of **38× / 45× / 14× / 28×** against
the first turn of each cycle
(`docs/roadmaps/core/pipeline/021-030-program-queue.md`, Sprint 021).

| Lever (estimated at planning time) | Reduction |
| :--- | ---: |
| Model tiering (Sprint 022) | ~40% on the model dimension (assumes uniform tokens across roles) |
| Splitting the session in two | ~50% |
| Splitting in four | ~75% |

Compaction reset the x-axis without shrinking the area under the sawtooth. Cost
tracked **peak height**, not message count.

## 2. Decision

**Ship the calibrated session bound (Sprint 021) before model tiering
(Sprint 022).** Ordering is a priority inversion relative to "pick cheaper
models first," justified by measurement: session height dominates model mix.

The bound is a ratio against the first turn of the **current context cycle**,
not the session's first turn — otherwise the first compaction collapses the
ratio and the bound never fires again.

## 3. Consequences

**Easier**: later tiering work (022) and portability (026) inherit a pipeline that
already forces session continuity (`suspend` / `resume_pointer`) instead of
pretending one infinite context is free.

**Harder**: Sprint 023-sized work must respect the bound mid-flight; without
`M6` ("session closed, sprint open") the bound would have been an invented
number that lied to `detect_drift.py`.

**Reproduce the ordering claim**: read the Delivered / Next status in
`docs/roadmaps/core/pipeline/021-030-program-queue.md` — `021` precedes `022` in
the sealed program, not by ID accident.

---
*Immutable once Accepted — a changed decision gets a new ADR that supersedes this one, never an in-place edit (`rules/documentation_standard.md §3`). File lives at `docs/decisions/ADR-0006-session-bound-before-tiering.md`.*
