# 📜 ADR-0001: Do not implement parallel subagent fan-out

**Status**: `Accepted`
**Date**: 2026-08-02
**Triggers**: 2, 6 (`rules/documentation_standard.md §3.1`)

**Last Audit Sprint**: 020
**Last Audit Date**: 2026-08-02

---

## 1. Context

Phase 020 carried a proposal to add parallel fan-out ("the Diamond") to the execution pipeline: a `Wave` column in `task_scope.md` derived from the graphify dependency graph, wave-by-wave dispatch in `principal_agent` Phase 4, and `scripts/validate_waves.py` to reject an unsound assignment.

The proposal rested on two observations that are factually correct:

- `rule_validator` already audits the roadmap **using the graphify dependency graph** and already emits `task_scope.md`. Since `jurisdictional_lock` gives each subtask exactly one file, disjointness is trivial and the only thing ordering execution is the dependency edges — which the graph already holds. Waves are its topological levels. The data exists and is discarded.
- `agents.md §6` declares a "rigid sequential process" while `agents.md §2 no_interference` says *"abort if `task_scope.md` shows the target file listed by another subtask **in progress**"* — a rule that only makes sense if two subtasks can coexist. The doctrine is written for concurrency and prohibits it.

It was the only track in Phases 019-020 with **no defect behind it**: every other item repaired something confirmed broken, while this added a capability for a bottleneck nobody had measured. It was therefore admitted with an entry condition: evidence that sequential execution is the real limit.

Measurement over the 13 work units of Phases 019-020:

| Metric | Result |
| :--- | :--- |
| Commit pairs with **disjoint** file sets | 23 of 78 (**29%**) |
| Commit pairs sharing at least one file | 55 of 78 (**70%**) |
| `CHANGELOG.md` | touched by **10 of 13** units |
| `README.md` · phase roadmap | 6 units each |
| `agents.md` · `close_workflow.md` · generated step map | 5 units each |

## 2. Decision

**Parallel fan-out is not implemented.** The entry condition was not met.

The measured bottleneck is not sequential agent execution. It is **contention on shared governance artifacts**: the Master Ledger, the README, the phase roadmap and the constitution are touched by most units of work. Under `jurisdictional_lock` (one file per subagent) and `no_interference` (a file claimed by an in-progress subtask is locked), those units would have serialised on exactly those files anyway. Waves would have been mostly of size one.

The contradiction between `agents.md §6` and `§2 no_interference` is real and stays recorded here, but it is a documentation defect rather than a blocked capability, and correcting it in isolation would license concurrency that nothing yet needs.

## 3. Consequences

**Easier**: the pipeline keeps a single execution model, and `qa_and_testing.md §2`'s `git restore .` kill switch stays globally scoped — its wave-failure semantics were the most dangerous part of the proposal, since a partial wave plus a global restore destroys the work of siblings that succeeded.

**Harder**: a future genuinely parallel workload has to re-derive this analysis. It should not simply reverse this decision: the correct trigger is a measurement where disjoint pairs dominate, not the intuition that parallel is faster.

**Left undone deliberately**: the `§6`/`§2` contradiction. Naming it without acting on it is the honest state — see Considered Options.

**What the measurement actually points at**: if throughput on this repository ever needs improving, the target is contention on shared documentation artifacts, not agent concurrency. That is a different and cheaper problem.

## 4. Deciders

Repository owner, with the measurement produced during Phase 020 execution.

## 5. Considered Options

| Option | Pros | Cons |
| :--- | :--- | :--- |
| **Implement the Diamond now** | Uses data the framework already computes; resolves the doctrinal contradiction | 29% disjointness means waves of ~1; changes `agents.md`, two agent profiles and the kill switch's blast radius for no measured gain |
| **Implement only the `Wave` column, dispatch later** | Low risk; data available when needed | A column nothing reads is an orphan, which `RA-16` exists to prevent |
| **Decline, record the measurement** ← chosen | Honest about the absent evidence; keeps one execution model; leaves the analysis for whoever revisits | The doctrinal contradiction stays on the books |
