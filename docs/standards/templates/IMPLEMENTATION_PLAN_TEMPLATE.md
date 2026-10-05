# Implementation Plan: Sprint {{SPRINT_ID}} — {{SPRINT_SLUG}}

**Canonical path**: `docs/sprints/{{SPRINT_ID}}-{{STACK}}-{{LAYER}}/IMPLEMENTATION_PLAN.md`
**Branch**: `ai-sprint/{{SPRINT_ID}}` · **Base**: `{{BASE_BRANCH}}` at `{{BASE_COMMIT}}`
**Status**: `DRAFT` → `APPROVED` → `EXECUTING` → `CLOSED`

> Authored at Phase 1 (Planning) by `principal_agent`, extracted to this path at
> Phase 3, and **committed before Phase 5 approves it**: `agents.md §2 triple_lock`
> names the approved Implementation Plan as its first lock, and a lock cannot close
> over an artifact that does not exist.
>
> Spanish is permitted in this document (`agents.md §1 user_chat`). Every other
> pipeline artifact is English.

---

## Context

Why this sprint exists. State the problem or need, what prompted it, and what is
true when it is done. **Measurements, not adjectives** — a figure carries the
command that reproduces it.

{{CONTEXT}}

---

## Design

The decisions that shape the work, with the reason each was chosen over what it
replaced. Record rejected alternatives here rather than in a session transcript:
this document is the only thing that survives the session.

{{DESIGN}}

---

## Work

One row per unit. One unit is one atomic commit (`RA-08`) with **one physical file as
its structural subject** (`agents.md §2 jurisdictional_lock`) — the file the unit exists
to change, which is the file this row names.

A unit whose commit will be `fix(`-typed names its paired test **in the same row**:
`rules/code_craft.md §6` requires that test in the same commit, and a mandatory
companion file is not a second subject. Plan the pair at Phase 1. Splitting
implementation and test into separate Work rows is what forced Sprint 047 to re-pair 7
units mid-execution.

The Work column `Assignee (proposed)` is a staffing proposal from Phase 1. Phase
4.1 (`agent_orchestrator`) is the authority that records the assignee; it may
overwrite this proposal. A Work row is not closed until `agent_assignment.md`
records it. Do not rename columns on existing `task_scope.md` files to match
this heading.

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| {{ID}} | `{{PATH}}` | create/modify/delete | low/medium/high | `{{ROLE}}` | ⏳ |

---

## Dependencies

`rules/code_craft.md §7` — every dependency is permanent code you do not control.
Before adding one, check the standard library, then what is already present. The
commit that adds it must also carry `Dependency: <name> — <reason>`.

| Package | Version | Why the standard library and the existing dependencies do not suffice |
| :--- | :--- | :--- |
| {{NAME}} | {{VERSION}} | {{JUSTIFICATION}} |

*Write `None` when the sprint adds none. An empty table is indistinguishable from
an unanswered question.*

---

## Mechanisms

Every recurring mechanism this plan proposes (per-sprint or per-commit cadence),
classified before the Approval Gate — `token_economy_agent` `pre_approval_audit`,
Filter 5. A recurring mechanism delegated to agent judgment when a deterministic
alternative exists is rejected, and the alternative must be **named**.

| Mechanism | Deterministic or agent judgment | Invoker (`RA-16`) |
| :--- | :--- | :--- |
| {{MECHANISM}} | script / `make` target / agent | {{INVOKED_BY}} |

`RA-16 INVOCATION_COVERAGE`: no workflow, script, executable skill, hook or gate
merges without a declared, verifiable invoker, or a typed exception in
`config/invocation_exceptions.json` stating why it has none.

---

## Cost

**Required from Sprint 030 onward** (`rules/token_economy.md` §3). Not retroactive
to plans sealed before 030. Enforced by
`skills/token-saver-auditor/scripts/audit_plan.py` (exit `2` if absent).

| Field | Value | Reproduce |
| :--- | :--- | :--- |
| Delegation | `{{native\|sequential}}` | `docs/active_state.json` `delegation_mode` |
| Work units | {{N}} | Count of rows in Work tables |
| Subagents dispatched | {{N}} | `0` under Cursor `sequential` |
| Prior session ratio | {{ratio or "n/a (Cursor / no transcript)"}} | `python3 scripts/session_cost.py --from-anchor --json` |

Soft (5×) / hard (15×) thresholds force an update to this section before new
work continues — they are not observational-only once a measurable Claude
transcript exists for this tool.

---

## Tests

**Reproduce before repairing.** A test that passes against the current tree proves
nothing about a defect claimed to exist in it (`KI-053-4`).

For every `**Yes**` row, `Observed at base` records the command run at the base
commit and its exit code, read directly with `$?` and never through a pipe — or the
literal word `unverified` followed by the reason it could not be run. A `**No**` row
records the passing run instead. An empty `Observed at base` cell is not an answer.

| Check | Fails against the current tree? | Observed at base |
| :--- | :--- | :--- |
| {{CHECK}} | **Yes** — this is the defect / **No** — this is a regression to protect | {{OBSERVED_AT_BASE}} |

---

## Verification

The exact commands, and what each must return. Read exit codes with `$?` directly;
**never through a pipe**, which reports the exit code of the last command in it.

**Dry-run rule.** Before Phase 5 approves the plan, the author runs every read-only
command in this table against the current tree and records the exit code and the
observed result in `Dry run`. A row that is destructive or slow says `run at close`
and gives the reason. Every row whose `Expected` is "no output" or `0` hits names in
`Positive control` a command, or a one-line variation of the row's own command, that
produces output when the guarded defect is present, and records that it did
(`F-114-N7` a, b). A guard that was never seen firing proves nothing by staying silent.

**Alternation in a backticked command.** Do not write it as an escaped `\|`: ripgrep
reads that literally and matches the characters `\|`, not either side. Inside a
Markdown table cell an unescaped `|` splits the row. Use `-e a -e b` instead.

| Command | Expected | Dry run | Positive control |
| :--- | :--- | :--- | :--- |
| {{COMMAND}} | {{EXPECTED}} | {{DRY_RUN}} | {{POSITIVE_CONTROL}} |

---

## Documentary impact (T5)

**Applies from Sprint 029 onward** (`rules/documentation_standard.md` §6). Not
retroactive to plans already sealed.

Every artifact this sprint creates or changes, and what changes about it. A
sprint that claims "docs updated" without this table has no documentary gate.

| Artefacto | Qué cambia |
| :--- | :--- |
| {{PATH}} | {{CHANGE}} |

**Measured figures.** Every number in Context / Design / Verification carries
the command that reproduces it. A figure without its command is memory, not
evidence (`021-030-program-queue.md` J6 / T5).

---

## Out of scope

Named exclusions with their destination. A finding with no destination is a finding
that dies in this document.

| Exclusion | Why, and where it goes instead |
| :--- | :--- |
| {{EXCLUSION}} | {{DESTINATION}} |

---

## Abort criterion

The observation that stops this sprint and reverts it, decided **before** execution
starts. Written in advance so it is not renegotiated once the work is sunk cost.

{{ABORT_CRITERION}}

---

## Approval — `triple_lock` lock 1

| Field | Value |
| :--- | :--- |
| **Approved by** | {{HUMAN}} |
| **Date** | {{ISO_DATE}} |
| **Plan commit at approval** | `{{COMMIT_SHA}}` |
| **Remaining locks** | Active Sprint · QA + Tester verdicts · Human OK at close |

*Phase 5 is a single attended human authorization. It MUST NOT be wrapped inside an
unattended `/loop` (`workflows/pipeline_workflow.md`, `rules/loop_governance.md`).
Any `/loop` this sprint does run — Phases 6-8 only — is governed by
`scripts/loop_guard.py start`, which fails closed.*

> **Do not delete the sentence above.** `audit_plan.py` Filter 6 rejects any plan
> that names `/loop` without also naming `loop_guard.py`, and this footer names
> both. Until Sprint 041 it named only `/loop`, so **every plan written faithfully
> from this template was rejected by the mandatory Phase 1 gate** — the template
> failed the check that consumes it, and the only passing plans were the ones that
> had dropped this footer. Replace `{{…}}` placeholders; leave this pairing intact.
