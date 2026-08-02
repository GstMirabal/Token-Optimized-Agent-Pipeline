---
description: "Capabilities — code craft, loop governance, tool-result economics (Phase 20)"
status: "COMPLETED"
version: 1.0.0
---

# Roadmap: Phase 20 - Capabilities

## Status
- **Strategy Lock:** `CLOSED`
- **Completion:** 100% — 4 of 4 tracks resolved (three implemented, one declined on evidence)
- **Sprint ID:** `020` — next sequential number after Phase 19 (`019-protocol-integrity.md`).
- **Branch:** `ai-sprint/020`, branched from `ai-sprint/019` rather than `main`, because `RA-16` had to be in force before any of this phase's mechanisms could declare their invokers. It merges after `019`.

## Objective
Add capability, where Phase `019` repaired defects. The split was deliberate: a failure in something new must not block the repair of something broken.

## Work Breakdown

| PR | Track | Scope | Status |
| :--- | :--- | :--- | :--- |
| 1 | **D + A.3** | Tool-result economics; the Decision Ladder's scope limit | ✅ Merged |
| 2 | **A** | `rules/code_craft.md` + two enforced gates + `commit-msg` hook | ✅ Merged |
| 3 | **B** | `rules/loop_governance.md` + `loop_guard.py` + Filter 6 | ✅ Merged |
| 4 | **C** | Parallel fan-out | ⛔ **Declined on evidence** — `ADR-0001` |

## What each track changed

### D — token economy is about accuracy, not only cost
`§3` forbade re-deriving recorded state; nothing addressed tool-result accumulation. The evidence reframes the rule: on a 50-task benchmark (arXiv 2606.10209), full history completed 71.0% of tasks with 1.48M tokens, pruning to the last 5 tool calls reached 79.0% with 535K, pruning plus summarisation 91.6% with 553K. Retaining everything is not expensive-but-safe; it is expensive **and less accurate**.

Scope was stated rather than overclaimed: Claude Code manages its own context window and this rule cannot prune it. It governs what the agent adds back.

**A.3** closed a latent conflict nobody arbitrated: `token_saver` pushes toward reading less, and nothing said that never applies to the range being edited.

### A — the rules `agents.md §1` could not see
Style, typing and size metrics cannot detect an abstraction built for a requirement nobody has. Five judgment rules plus two enforced gates.

**The calibration run is the part worth keeping.** Both gates were tested against this repository's 156-commit history *before* being wired in, and that run **rejected the first version of the dependency gate**: it flagged 3 of 3, because it fired on any touch of a manifest — version bumps, removals, and `package.json` files vendored under `node_modules/` inside a `-3rd` skill. Rewritten to fire only on a package name added and not removed, it flags 1 of 3: the single commit that genuinely introduces a dependency without saying why. The regression gate flags 4 of 13 `fix(` commits, each real — including PR `#27`, which rewrote 90 lines of the secret scanner with no test at all.

Coverage was then completed rather than left declared: a `commit-msg` hook closes the path `pre-commit` structurally cannot cover, since git has not finalised `COMMIT_EDITMSG` at pre-commit time and reading it there would test the *previous* commit's message.

### B — unattended loops get a stop set
`/loop` had one line of governance. Three binding stops now, one advisory. The token budget is advisory **on purpose**: no agent reads its own spend reliably, and a binding cap would force a field nobody can fill truthfully — the same defect as a gate that cannot fail.

Fail-closed throughout: a missing, incomplete or stale `loop` block exits `2`. Its own tests caught an **off-by-one** — `check` runs at the *start* of an iteration, so its first comparison is against a baseline written before any work could happen, and counting it stopped the loop after one unproductive iteration instead of two.

### C — declined, with the measurement that declined it

| Metric over the 13 work units of Phases 019-020 | Result |
| :--- | :--- |
| Commit pairs with disjoint file sets | 23 of 78 (**29%**) |
| Pairs sharing at least one file | 55 of 78 (**70%**) |
| `CHANGELOG.md` | touched by **10 of 13** units |

The bottleneck is not sequential agent execution; it is contention on shared governance artifacts. Under `jurisdictional_lock` and `no_interference` those units would have serialised on exactly those files anyway, so waves would have been mostly of size one. Full reasoning, options and consequences: `docs/decisions/ADR-0001-no-parallel-fan-out.md`.

Declining is the result, not a gap. The entry condition existed precisely so this could be answered with data.

## Findings recorded

| Finding | Consequence |
| :--- | :--- |
| **A gate must be calibrated against real history before it is wired in.** | The dependency gate's first version would have blocked legitimate work — the PR `#27` failure repeated. 156 commits of history answered in seconds what review would not have. |
| **The previous phase's gates caught this phase's drift.** | `check_readme_counts.py`, built in `019`, failed the build when `code_craft.md` and `loop_governance.md` changed the rule count and the README did not. The mechanism worked on its first unplanned encounter. |
| **A budget is only a constraint if it is honoured when inconvenient.** | `code_craft.md` came in at 61 lines against a 60-line budget. Content was cut, not the limit raised. |
| **Declining on evidence is a deliverable.** | Track C had no defect behind it and an explicit entry condition. Measuring and declining is what the condition was for; implementing it anyway would have been the speculative generality `code_craft.md §1` prohibits. |

## Certification
- [x] `make verify` green end to end (117 tests, installer sandbox, all scanners).
- [x] Every new gate carries tests asserting it **fails** where required.
- [x] Both `on_commit.py` gates calibrated against 156 real commits before wiring.
- [x] `commit-msg` hook verified end to end with real terminal commits in a sandbox repository.
- [x] Size budgets honoured: `code_craft.md` 60 lines, `loop_governance.md` 40.
- [x] Counts verified mechanically: 10 rule contexts, 13 agents, 34 skills, 12 workflows, 13 commands.
- [x] `docs/decisions/` created with `ADR-0001`; the Blueprint gap acknowledged in `acknowledged_gaps` with a reason rather than left to re-fire every session.
- [x] Knowledge graph rebuilt: 3514 nodes, 3703 edges, 422 communities.

---
*Opened and completed 2026-08-02 on `ai-sprint/020`. Not released — ledger entries sit under `[Unreleased]`.*
