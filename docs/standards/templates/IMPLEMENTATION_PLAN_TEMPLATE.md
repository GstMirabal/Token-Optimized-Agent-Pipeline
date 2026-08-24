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

One row per unit. One unit is one atomic commit (`RA-08`) touching **one physical
file** as its structural subject (`agents.md §2 jurisdictional_lock`).

| # | File | Operation | Risk | Assignee | Status |
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

## Tests

**Reproduce before repairing.** A test that passes against the current tree proves
nothing about a defect claimed to exist in it.

| Check | Fails against the current tree? |
| :--- | :--- |
| {{CHECK}} | **Yes** — this is the defect / **No** — this is a regression to protect |

---

## Verification

The exact commands, and what each must return. Read exit codes with `$?` directly;
**never through a pipe**, which reports the exit code of the last command in it.

| Command | Expected |
| :--- | :--- |
| {{COMMAND}} | {{EXPECTED}} |

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
unattended `/loop` (`workflows/pipeline_workflow.md`, `rules/loop_governance.md`).*
