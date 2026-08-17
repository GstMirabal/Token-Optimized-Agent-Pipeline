---
description: "Cost instrumentation — the meter, the per-cycle bound, and the suspended state (Sprint 021)"
status: "COMPLETED"
version: 1.0.0
---

# Roadmap: Sprint 021 - Cost Instrumentation

## Status
- **Strategy Lock:** `CLOSED`
- **Sprint ID:** `021` — first in execution order after `024` and `025`, which were promoted
  when their defects blocked the program. IDs are labels, not positions.
- **Branch:** `ai-sprint/021`, from `main` at `36dd96a` (`v4.5.0`).
- **`RA-06` deviation, declared:** `[NNN]-[slug].md`, the standing convention of this directory
  since `000-`, because a roadmap sorts by phase and `[MODULE]_[TYPE]` does not sort at all.

## Objective

Build the instrument before the rule. The bound this sprint declares is only as good as the
measurement behind it, and that measurement was wrong until this sprint re-took it.

## Work Breakdown

| Commit | Track | Scope | Status |
| :--- | :--- | :--- | :--- |
| 0 | **Correction + documentation** | The refuted claim in the program roadmap, plus this sprint's records | ✅ `6276a50` |
| 1 | **The meter** | `session_cost.py`, segmenting by context cycle | ✅ `a01f9e6` |
| 2 | **The bound** | `token_economy.md`, `loop_governance.md`, `session_probe.py` | ✅ `de3b7f6` |
| 3 | **Continuity** | `SUSPENDED` state and the resume path | ✅ `09d8b37` |
| 4 | **`plansDirectory`** | A plan drafted in an IDE lands in the repository | ✅ `862d6b7` |
| 5 | **Ledger + records** | `CHANGELOG.md`, sprint log, phase register | ✅ this commit |

## The correction that opens the sprint

The program queue was ordered by a claim that cost grows monotonically with message position.
Re-measuring before building refuted the **shape**: the session is a sawtooth of four context
cycles, each reset to ~22K. The original quartiles came from the first 400 messages, entirely
inside cycle 1, at a scope never declared.

The conclusion survives and strengthens — cost is the area under the sawtooth, and compaction
resets the axis without reducing the area. Full measurement and its three consequences are in
`IMPLEMENTATION_PLAN.md` in this directory.

**Recorded as the fifth instance of program risk `J6`**, and the most expensive: this figure
ordered the queue. The mitigation `J6` names — every measured claim carrying the command that
reproduces it — is what made the re-measurement possible at all.

## Delegation

Sequential. The session configuration forbids spawning subagents while `agents.md §6` requires
eight roles; reported before Phase 1 per `start_workflow.md` `delegation_conflict` and
authorised. Writes are emitted under the ruleset of the profile governing each artifact.

## Outcome

| Check | Result |
| :--- | :--- |
| `make verify` | green — 151 tests, installer sandbox, nucleus self-bridge |
| Live acceptance, the meter | reproduces 38.3x / 44.9x / 14.0x / 30.0x on the drafting session |
| Abort criterion, the segmenter | **did not fire** |
| Abort criterion, `suspend` laundering drift | **did not fire** — hermetic test |
| Freshness gate on `021` | clean, only the pre-existing `code_containers` advisory |

**`M5` was missing from this sprint's own commit table** — present in the work
breakdown, absent from the commit list. Found while closing, and split into its
own commit rather than folded into the ledger (`RA-08`). Recorded because a plan
that silently drops one of its own items is the class of defect this program
exists to remove.
