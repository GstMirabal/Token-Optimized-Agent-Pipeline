# Phase Register — Sprint 023 (`upstream-findings`)

What `close_workflow.md` Phase 2.6 `double_gate_evidence` reads to answer the
one question no other control asks: **did this phase actually happen?**

The precedent is in `CHANGELOG.md [4.4.0]`: a host ran a whole sprint without
Phase 4 and Phase 7, `task_scope.md` was never produced, and nothing raised it
across twelve commits — because every existing control inspected the *content*
of what was written, never whether the phase responsible for it ran.

| Phase | Artifact it must leave | Status |
| :--- | :--- | :--- |
| 1 · Planning | `IMPLEMENTATION_PLAN.md` | ✅ this directory. **This sprint is the reason the artifact has a location at all** — `C0` gave it one, and the plan is versioned here rather than in ephemeral storage |
| 2 · Environment | `venv_skillopt/` present, `installed.lock` read | ✅ verified, `requirements-core.txt` |
| 3 · Roadmap Drafting | `docs/roadmaps/core/pipeline/021-030-program-queue.md` + branch `ai-sprint/023` | ✅ `RA-12`; the sprint's scope lives in the program queue rather than a standalone roadmap file |
| 4.1 · Agent Assignment | `agent_assignment.md` | ✅ this directory |
| 4.2 · Skill Assignment | `skill_assignment.md` | ✅ this directory |
| 4.3 · Rule Audit | `task_scope.md` | ✅ this directory, versioned |
| 5 · Approval Gate | Human authorisation, attended | ✅ granted before execution; **re-granted twice during the sprint** — for `C3.2` at the remediation halt, and for `C8`'s scope extension after the structural gate refused `F-023-S4` as undeclared |
| 6 · Execution | Atomic commits on `ai-sprint/023` (`RA-08`) | ✅ 45 commits, `2821953` → `8dc400d`, plus `C8`'s two on `contrib/host-findings` |
| 7 · Quality Gate | `make verify` green + per-unit Double Gate | ✅ 428 tests, installer sandbox, nucleus self-bridge, reference integrity, determinism scan, manifest parity, step-map regeneration, README counts |
| 8 · Closeout | `CHANGELOG.md` `[Unreleased]`, roadmap updated, anchor synced, `graph_stats.json` persisted | ✅ this close |

## Units and gate rounds

Fourteen units. `C3.2` was added mid-sprint at a remediation halt; `C4.2` was
added because `C4` established `F-086-S3` could not be closed by any unit acting
alone.

Every figure below is quoted from `SPRINT_LOG.md`, not reconstructed. Where the
log records rejections without a round count, the cell says so rather than
inferring one — a first draft of this table inferred four and three of them
contradicted the log.

| Unit | Rounds | Rejections | Gated by |
| :--- | :--- | :--- | :--- |
| `C9`, `C0`, `C0.2`, `C1` | 1 | 0 | lead session |
| `C0.3` | 2 | 1 | lead session |
| `C2` | 3 | **3**, across two gates | **dispatched** `qa_agent` + `tester_agent` |
| `C3` + `C3.2` | 5 | 4 | **dispatched** |
| `C4` | 4 | 3 | **dispatched** |
| `C4.2` | not recorded | 2 | lead session |
| `C5` | not recorded (`R1`) | 1 | **dispatched** |
| `C6` | not recorded | 2 | lead session |
| `C7` | 1 | 0 | lead session |
| `C8` | 5 | 4 | **dispatched** |
| `C10` | 6 | 4 | **dispatched** |

**The two units that would have shipped a defect are both in the dispatched
column.** `C4`'s gate found the unit had deleted hand-authored governance content
— three directives including the mandate `RA-02` states — and that the test
written to forbid exactly that deletion passed only because its fixture avoided
the case. `C8`'s gates found four false claims in a findings register, including
a published reproduction command that returned a different number than its own
entry asserted. Neither was reachable by its author: the deletion was found with
`git log -S` against a file the author had read, and the false count by
re-measuring rather than re-reading.

## Findings recorded against the coordinator

Recorded here rather than only in `task_scope.md` because a phase register that
lists only the work's defects, and never the process's, is measuring itself less
carefully than it measures the work.

| Finding | Rule | Disposition |
| :--- | :--- | :--- |
| The `C8` artifact was patched **while the Tester gate was auditing it**; the gate detected the mutation itself and pinned a hash before continuing | `RA-13` | The edits were judged safe on the grounds that they touched no measurement. The QA gate then showed that is a test which *cannot* work — the next patch under the same justification corrected a claim at one site and left its twin standing, and both sites passed it. Halt-patch-redispatch applied twice afterwards, against committed objects |
| Two of `C8`'s five rounds were **one `RA-14` omission repeated** | `RA-14` | The rule asks for the *term* to be grepped across the whole artifact; the author re-read the patched region instead, twice. Four `RA-14` instances in this sprint total |
| `C8` was classified **low-risk** and cost 5 rounds and 4 rejections, against `C10`'s 6 and 4 | — | Risk was assessed on the operation — ticking checkboxes — and not on what the artifact asserts. Recorded as `F-20260824-UF03` |

Both rule-shaped findings are routed as governance amendments for a later sprint
rather than double-recorded as Knowledge Items (`extract_workflow.md`
`rule_vs_ki`). Neither `RA-13` nor `RA-14` currently has a mechanical check:
`RA-13` does not say the gate's object must be frozen for the gate's duration,
and nothing in `make verify` or the hooks greps a patched term across its
artifact.

## Deviation — delegation

Delegation was forbidden by session configuration throughout, reported before
Phase 1 in session #1 and authorised. **The lift is per-session and per-unit, not
standing**, and was re-requested at every session boundary: sessions #2 through
#7 each asked again and each received it for that session's unit only. Session
#5's lift was spent when both dispatched agents died mid-round on an
account-level monthly spend limit — a lift is spent by being used, not by
producing a verdict.

Six of fourteen units were therefore written *and* gated by the same context.
`F-021-A2` is why and is declared in `agents/devops_agent.md`: no profile in
`agents/` is an implementer, so there is nobody to dispatch authoring to.

## Sessions

Seven working sessions plus this close. Every one before this suspended **below**
the `rules/token_economy.md §3.1` bound rather than at it: 12.1×, 12.9× and 12.3×
at the last three, against 15×. The per-project reset constant was observed at
**24,272 across three sessions and seven cycles**, which is the stability the
rule's denominator was designed around.

### This close crossed the bound, and that is the datum

**Measured at 16.0×** (`scripts/session_cost.py`, cycle 2, peak 388,617 against a
first turn of 24,272). The bound is 15× and it is binding. Recorded here rather
than in a session note because it is the first time this framework has *crossed*
it rather than stopped short.

**What happened, in order.** The session measured 12.3× with every unit closed
and priced the remaining close as not fitting in 2.7× of headroom. The human
overruled that on correct grounds — `close_workflow.md` is atomic and a close
split across sessions is worse than either doing it or deferring it whole. The
close then cost **≈3.7×**, so the estimate was right about the fit and the
decision was still the better of the two available.

**The reserve nothing states.** `§3.1` bounds a session's climb and says nothing
about the close, so a session plans by units-remaining and meets the close with
whatever is left. Measured here: **a nucleus sprint close costs about 3.7× on top
of the session that reaches it** — fourteen protocol steps, six unit narratives, a
ledger entry, a graph rebuild and a phase register. A session intending to close
must reserve for it at roughly 11× rather than discover the cost at 12.3×.

**Why finishing was the lower-risk branch once past the bound.** Abandoning at
16.0× would have left the ledger entry, six narratives, this register, the memory
index and the graph snapshot uncommitted, with the sprint neither cleanly open
nor sealed — a state no resume block can describe and no gate can check. The
remaining phases were deterministic scripts and one commit. **Stopping was more
expensive than finishing**, which is a property of *where* in the protocol the
bound is crossed, and `§3.1` has no concept of that either.

Routed with the `RA-13` and `RA-14` findings above: three token-economy gaps for
one later unit, all of them cases where the rule measures a thing but not the
thing a session actually needs to decide.
