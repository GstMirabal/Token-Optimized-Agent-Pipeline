# Sprint Log — 023 (`upstream-findings`)

**Branch**: `ai-sprint/023` from `main` at `18696c5` (`v4.7.0`)
**Status**: open. 2 of 13 units delivered.

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

### `C0` — the Implementation Plan gets a location and a gate (`2821953`)

**The defect.** The plan was the only pipeline deliverable with no home. It is
`triple_lock`'s first lock, the Phase 1 deliverable, and `rules/code_craft.md`
requires justifying every dependency in it — mentioned **seven times** across the
governance corpus, and **no document said where it is written**. Measured: 11
templates in `docs/standards/templates/` and none for a plan; a host's sprint 093
folder left six artifacts and none was the plan. The consequence was measured too
— a host lost an approved plan, and this repository held two Implementation Plans
from April 2026 untracked for four months.

**The sequencing contradiction, which no document had resolved.** The plan is
*authored* at Phase 1; the sprint directory is *instantiated* at Phase 3. The
canonical path does not exist when the plan is written. Resolved explicitly:
Phase 1 authors, Phase 3 extracts and commits, Phase 5 checks existence as a
precondition, close verifies retrospectively. Without that, the rule would have
been unexecutable while reading as complete.

**What the gate proves, written into the workflow.** It proves the plan exists and
is versioned — the loss it was built against. It does **not** prove the plan
existed before approval; that ordering rests on the Phase 5 precondition, an
attended human step. Stated rather than implied, because a gate suggesting a
guarantee it does not give is this program's subject.

**No new mechanism** (`RA-16`): `PHASE_ARTIFACTS` in `docs_freshness_check.py`
gains one entry and the dict is reordered by phase, so a sprint that skipped
several steps reads in the order they should have run.

**`RA-14` found three false paths, not two.** The full grep — the rule's actual
requirement, as opposed to patching where one happened to look — turned up
`agents/rule_validator.md:19` calling `task_scope.md` a *"git-ignored session
artifact at the host root"*, both halves false since Sprint 024, **in the profile
of the agent that produces the file**. `pipeline_workflow.md` Phase 4.3 and
`agents/token_economy_agent.md:25` were the other two.

**Verification**: the gate measured **red then green** on this tree — naming
`IMPLEMENTATION_PLAN.md` and Phase 1 while absent, silent once written — with the
exit read from `$?` directly and never through a pipe. `check_phase_artifacts`
shipped in PR `#37` with **no test at all**; it now has six, and three of them
could not have passed before this change. `make verify`: **174 passed**.

This sprint's own plan is filed with the commit, from the new template, and says
in its header that it was filed retroactively.

## Suspended, not closed

`rules/token_economy.md §3.1` hard threshold: cycle 7 reached **16.5×** its
first turn against a bound of 15×. The rule is binding, the sprint is open, so
the session suspends. **This is the first time that bound has fired** since
Sprint 021 built it — recorded as `forced: true` with unfinished work in
`task_scope.md`, which is the calibration signal `§3.1` asks for rather than
one to infer later.

**The session resumed after compaction** and delivered `C0`. That does not erase
the record above: the bound fired, and the calibration `§3.1` asks for needs the
event kept, not tidied away once the work continued.

**Next Phase**: `C0.2` (the artifact registry — `config/artifact_registry.json`
and its three consumers). Eleven units remain; `task_scope.md` holds per-unit
status and the findings routed out of `C0`.
