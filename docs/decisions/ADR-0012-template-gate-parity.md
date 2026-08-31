# 📜 ADR-0012: A template is proved against the check that consumes it

**Status**: `Accepted`
**Date**: 2026-08-31
**Triggers**: 3 (`rules/documentation_standard.md §3.1`) — the check executes an argument vector declared in a data file, so the boundary between data and execution is the decision's core. Trigger #3 escalates to full MADR individually (`§3.2`).

---

## 1. Context

An author starts a sprint artifact by copying a template out of
`docs/standards/templates/`. A separate script later judges the artifact. Nothing
compared the two.

Sprint 041 hit three divergences inside its own phases, each found by following an
artifact rather than by auditing it:

| Artifact | Gate it failed | Repaired as |
| :--- | :--- | :--- |
| `IMPLEMENTATION_PLAN_TEMPLATE.md` | the Phase 1 plan audit | `041` U10 |
| `SKILL_ASSIGNMENT_TEMPLATE.md` | the Phase 4.2 forge check | `041` U11 |
| `pipeline_workflow.md` Phase 4.3 (prose, not a template) | the Phase 4.3 scope check | `041` U12 |

The first is the one that fixes the severity: **every plan written faithfully from
the official template was rejected by the mandatory Phase 1 gate**, and the only
plans that passed were the ones that had dropped part of the template. The
template taught authors to fail.

All three are repaired. Nothing prevented a fourth.

Measured while planning Sprint 042 (2026-08-30), rendering each template into a
scratch directory and running its consumer: the three repaired pairs exit `0`, and
`check_role_artifact.py` exits `2` against `SPRINT_LOG_TEMPLATE.md` for a reason
that is not a divergence — see Decision, point 4.

## 2. Decision

`scripts/check_template_gates.py`, invoked by `Makefile` target `verify` (and so by
CI, which calls that target rather than listing steps), renders each template
declared in `config/template_gates.json` into a scratch sprint directory and runs
the declared check against the copy. Four properties are decided here:

1. **Rendered copy, never a lint in place.** The consuming checks decide by
   pattern-matching prose. A check pointed at a template in its own directory
   trips over the template's explanatory text — measured twice during Sprint 041
   U11, where documenting the repair in the offending strings' own words re-broke
   it. Sprint 042 hit the same trap a third time: its own correction of a roadmap
   quoted the stale sentence it was retiring and re-tripped the grep written
   against it.
2. **Verbatim copy — `{{PLACEHOLDER}}` is not substituted.** The three shipped
   templates pass their checks with placeholders intact. Substituting would measure
   the fixture that replaced them: a broken template could pass because the
   substitution repaired it.
3. **The declaration is data that gets executed, and is constrained in code.** No
   shell; `argv[0]` must be exactly `python3`; the script path must resolve to an
   existing file inside the framework root; `{sprint_dir}` is the only expandable
   token. These are enforced by the reader, not trusted to whoever edits the JSON.
4. **A template owes the check that consumes it at the phase the template is
   authored** — not every check that ever reads the file. `SPRINT_LOG_TEMPLATE.md`
   is authored at Phase 3; its verdict rows are written at Phase 7 by the gates
   themselves. The `phase-mismatch` exception records this; the alternative is
   fabricated verdict rows in the template, which would teach authors to invent
   verdicts.
5. **Coverage is complete or the build fails.** Every entry of
   `docs/standards/templates/` appears in a case or in a typed exception. This is
   `RA-16`'s shape applied to templates: without it the instrument covers the four
   files it was born with, and the next divergence is born outside it.

The script names no check. Names live in the declaration.

## 3. Consequences

**Easier.** A template edit that would have blocked a future sprint's Phase 1 now
fails at `make verify`, in the session that made it, instead of surfacing in
someone else's planning phase weeks later. Adding a template forces the question
of what judges it.

**Harder.** Every new template costs a decision — a pairing or a written
exception. That is the intended cost.

**Accepted risks.** The declaration widens the set of things `make verify`
executes. The four constraints above are the containment, one test per constraint
in `tests/test_check_template_gates.py`; the failure mode if they are ever relaxed
is arbitrary execution in CI from an edited `.json`, which is why they live in code
rather than in a comment.

**Not covered, deliberately.** A workflow's *prose* instructing an author is not a
renderable template — it produces no artifact a check consumes — so the `041` U12
case is out of this instrument's reach. The inverse divergence (`check_task_scope.py`
enforces a shape for which no template exists) is routed to
`docs/roadmaps/core/pipeline/021-030-program-queue.md` as `T1`/`T2`.

## 4. Deciders

GstMirabal (Approval Gate, Sprint 042, 2026-08-31). Drafted by `principal_agent`;
`implementer_agent` ruleset governed the script, the declaration and the tests.

## 5. Considered Options

| Option | Pros | Cons |
| :--- | :--- | :--- |
| **A new check script (chosen)** | Matches the existing topology, where each sprint gate is its own file; keeps subprocess execution out of the static analyser; one declared invoker satisfies `RA-16` | One more file in a tree that already has 38 scripts |
| Add a check to `scripts/verify_references.py` | It already owns template existence checking, so template *passability* looks adjacent | That file is a pure static corpus analyser: it reads text and executes nothing. Adding subprocesses and scratch directories to it mixes two failure modes in one exit code |
| Render with placeholder substitution from a fixture map | Produces an artifact closer to what an author really writes | Measures the fixture, not the template. A template that cannot pass without help would pass, which inverts the check's purpose |
| Lint each template in place, no copy | Simplest possible implementation | Measured to fail: prose-matching checks trip on the templates' own explanatory text. This is the trap that broke the Sprint 041 repair twice |
| Do nothing; repair divergences as sprints trip over them | Zero build cost | The status quo that produced three divergences in one sprint, one of which had been rejecting every faithfully written plan |

---
*Immutable once Accepted — a changed decision gets a new ADR that supersedes this one, never an in-place edit (`rules/documentation_standard.md §3`). File lives at `docs/decisions/ADR-0012-template-gate-parity.md`.*
