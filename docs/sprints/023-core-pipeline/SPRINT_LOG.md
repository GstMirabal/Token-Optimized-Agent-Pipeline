# Sprint Log — 023 (`upstream-findings`)

**Branch**: `ai-sprint/023` from `main` at `18696c5` (`v4.7.0`)
**Status**: **SUSPENDED**, sprint open. 1 of 13 units delivered.

## Delivered

### `C9` — branch integration answers in three values, not two (`437493b`)

Ran first because this sprint's own close invokes `branch_sovereignty audit`.
Repairing that gate last would have meant tripping on the defect the sprint
exists to remove.

**The defect.** `merged_pr_exists` returned a bool and mapped every non-zero
exit to `False`, so *"I could not find out"* became *"no merged PR exists"*.
Measured against the live API: **2 of 12 calls returned `rc=1`, `HTTP 503`**.
Because `content_is_integrated` already returns `False` for every squash-merged
branch, one 503 was enough to flip an **integrated** branch to unintegrated.
Reproduced as two triple-runs of `audit` on an unchanged tree exiting `0,2,0`
and `0,0,2` — **accusing a different branch each time**, which is the signature
of a per-call failure rather than a property of any branch.

**Why it mattered despite failing safe.** `prune` never deleted what it could
not prove, so nothing was destroyed. The damage was the remediation the gate
induced: it steered the operator toward a permanent waiver for a healthy
branch — the *"weakening the check"* the module docstring already warned
against. The docstring promised *"reported, not assumed"*; the code assumed.

**The fix.** `YES` / `NO` / `UNKNOWN`, with retry and backoff. `UNKNOWN` still
blocks — a real outage that passed would be a false green, the same defect
inverted — but it is reported as doubt, separately from an accusation, and is
**never offered the waiver**.

**Two traps caught during implementation, both recorded in the code:**

1. **The truthiness inversion.** `classify`'s condition was
   `content_is_integrated(...) or merged_pr_exists(...)`. With a three-valued
   string answer, `NO` and `UNKNOWN` are both non-empty and therefore truthy —
   that chain would have reported **every** branch integrated. A silent
   inversion of the gate is far worse than the flakiness being removed.
2. **`rc=1` means two different things.** Probed rather than recalled:
   `no git remotes found`, `not a git repository` and
   `none of the git remotes …` mean there is no GitHub side to ask, so no pull
   request can exist — a definitive `NO`. Treating them as `UNKNOWN` would
   **refuse the seal forever in every local-only repository**, trading an
   intermittently wrong gate for a permanently closed one.
   `Could not resolve to a Repository` stays `UNKNOWN`: a misconfigured remote
   must surface rather than read as clean.

Also closes an `agents.md §1 exception_handling` violation — the error became a
datum with no log.

**Verification**: `make verify` **168 passed** (161 + 7 new); gate run 5×, exit
measured without a pipe, `0,0,0,0,0`. That does not *prove* determinism — only
that no three consecutive failures occurred. What changed structurally is that
three are now required instead of one, and every path has a direct test.

`RA-14` propagation: `close_workflow.md` steps `branch_audit` and `local_prune`
both described integration as binary; `local_prune` also offered the waiver
without distinguishing doubt from abandonment. Both patched.

## Suspended, not closed

`rules/token_economy.md §3.1` hard threshold: cycle 7 reached **16.5×** its
first turn against a bound of 15×. The rule is binding, the sprint is open, so
the session suspends. **This is the first time that bound has fired** since
Sprint 021 built it — recorded as `forced: true` with unfinished work in
`task_scope.md`, which is the calibration signal `§3.1` asks for rather than
one to infer later.

**Next Phase**: `C0` (`F-021-P0` — the Implementation Plan gets a location and a
gate). Twelve units remain; `task_scope.md` holds per-unit status.
