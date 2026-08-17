---
description: "Implementation Plan — Sprint 021 cost instrumentation"
status: "APPROVED"
version: 1.0.0
approved_by: human
approved_at: "2026-08-17"
---

# Implementation Plan: Sprint 021 - Cost Instrumentation

**Branch:** `ai-sprint/021`, from `main` at `36dd96a` (`v4.5.0`)

## Context

The program queue was ordered by a measurement of session cost. Re-measuring it before
building the meter **refuted its shape**, and the correction is the first commit of this
sprint rather than a footnote: leaving a disproven claim standing in a published document
is the drift `RA-14` exists to catch.

| What the roadmap said | What the full data shows |
| :--- | :--- |
| Cost grows monotonically with message position | The session is a **sawtooth**: four context cycles, each reset to ~22K |
| Quartiles 7 / 15 / 23 / 54% | 157K / 681K / 245K / 485K — **not monotonic** |

The original figures were real. They came from the first 400 messages, which fell **entirely
inside the first context cycle**, before any reset — a scope never declared. Fifth instance of
program risk `J6`, and the most expensive, because this figure ordered the queue.

| Cycle | Messages | First turn | Peak | Ratio | `cache_read` |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 414 | 22,174 | 849,060 | 38× | 123,791,322 |
| 2 | 113 | 22,174 | 995,197 | 45× | 99,489,407 |
| 3 | 267 | 25,833 | 361,337 | 14× | 64,036,103 |
| 4 | 282 | 22,174 | 630,886 | 28× | 136,030,710 |

**The corrected thesis is stronger than the original.** Cost is the area under the sawtooth.
Compaction resets the x axis and does not reduce the area — four resets happened and the
session still spent 423M `cache_read`. Cycle 2 is the proof: **113 messages cost 99.5M**,
nearly as much as cycle 1's 414, because it climbed to 995K. **Cost tracks peak height, not
message count.**

Two things this buys that the quartile view could not:

- **The reset point is 22,174 tokens, identical three times.** The break-even figure stops
  being an estimate and becomes an observed constant.
- **The hard threshold would have fired in 3 of 4 cycles** — calibration validated, provided
  the ratio is measured per cycle. Against the session's first turn it would collapse after
  the first reset and never fire again.

## Work

| # | Action | File |
| :--- | :--- | :--- |
| M0 | Correct the refuted claim and its four propagation sites in the program roadmap | `docs/roadmaps/core/pipeline/021-030-program-queue.md` |
| M1 | **The meter**, segmenting by context cycle, discarding `model == "<synthetic>"` | `scripts/session_cost.py` (new) |
| M2 | Tokens, not dollars — the price ratio is born with `config/model_tiers.json` in 022 | — |
| M3 | The bound, **per cycle**: soft 5× observational, hard 15× recording `forced` and unfinished scope | `rules/token_economy.md`, `rules/loop_governance.md` |
| M4 | The start probe reports the previous session's cost per cycle | `scripts/session_probe.py` |
| M5 | `plansDirectory` pointing at the repository | `claude/settings.hooks.json` |
| M6 | `SUSPENDED` state, `suspend` subcommand, `resume_pointer`, `session_count` | `scripts/session_state.py`, both workflows |

## Tests

| Check | Must fail against the current tree |
| :--- | :--- |
| Totals per model **and per cycle** over a test transcript | **Yes** — it does not exist |
| A synthetic transcript with two resets produces three cycles | **Yes** |
| `<synthetic>` entries are discarded | **Yes** |
| No `usage` field → **says it cannot measure** rather than returning zero | **Yes** |
| **Live acceptance**: over the drafting session it reproduces 4 cycles and ratios 38/45/14/28 | **Yes** |
| The bound is machine-checkable against the **cycle's** first turn | **Yes** |
| `suspend` sets `SUSPENDED` and leaves `last_close_commit` intact | **Yes** |
| `claim` over `SUSPENDED` returns 0 without `--takeover`; over `IN_PROGRESS` still returns 2 | **Yes** / **No** — the second half is the regression to protect |
| `release` still writes `last_close_commit` | No — regression to protect |
| `make verify` green, `invoked_by` declared (`RA-16`) | No |

## Abort criterion

If live acceptance does not reproduce the four cycles, the segmenter is wrong and everything
above it rests on it. Revert via `remediation_workflow.md` before building the bound on top.

## Out of scope

| Exclusion | Reason |
| :--- | :--- |
| Changing how Claude Code manages its context window | Not the framework's. The bound acts on what the protocol controls: when to close a sprint |
| Treating compaction as a cost control | **Measured: it is not.** Four resets, 423M spent anyway |
| Dollar prices | Born with `config/model_tiers.json` in Sprint 022 |
