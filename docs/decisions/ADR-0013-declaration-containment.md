# 📜 ADR-0013: Every field a declaration contributes is contained, and the anchor is verified before what hangs from it

**Status**: `Accepted` — supersedes `ADR-0012`
**Date**: 2026-08-31
**Triggers**: 3 (`rules/documentation_standard.md §3.1`) — the boundary between a data file and execution. Trigger #3 escalates to full MADR individually (`§3.2`).

---

## 1. Context

`ADR-0012` decided that `scripts/check_template_gates.py` renders each versioned
template into a scratch directory and runs the check that consumes it, and that
the declaration in `config/template_gates.json` — a data file that gets executed —
is constrained in code rather than trusted.

It then enumerated the containment as **four** constraints: no shell; `argv[0]` is
`python3`; the script path resolves inside the framework root; `{sprint_dir}` is
the only expandable token. Section 3 called those *"the four constraints above are
the containment, one test per constraint"*.

The implementation matched that enumeration exactly, and it was not containment.
Three rounds of Gate 1 measured what the enumeration had left out:

| Round | Finding | What the enumeration missed |
| :--- | :--- | :--- |
| 1 | `str(script).startswith(str(root))` is a name prefix, not containment. `../.agents-profile/x.py` — the layout `agents.md §3 topological_order` prescribes for host profiles beside the `.agents` submodule — passed and executed | The constraint was named but its implementation was never stated, and «resolves inside» was satisfied by a string test |
| 1 | The `render` map reached `shutil.copyfile` unvalidated: any readable file copied over any writable file, in one case at exit `0` with `[OK]` printed | The enumeration covered the argument vector. The declaration contributes paths through a second channel |
| 2 | `case["id"]` is joined into the scratch anchor unvalidated; `check_render_paths` then measures target containment **against that anchor**, so a declaration-chosen anchor satisfies the predicate by construction. Exit `0`, files written outside the temporary directory, no finding | Adding a guard for one field while its sibling in the same expression stays free |

The sprint was green throughout rounds 1 and 2 — `make verify` exit `0`, full suite
passing, `ruff` clean, the sprint's own abort criterion satisfied. None of those can
see a defect in what the checker *permits*, as opposed to what the shipped
declaration *asks for*.

## 2. Decision

Containment is defined by **which values reach the filesystem or a subprocess**,
not by a list written in advance. Every value the declaration contributes is
traced to a guard, and the guard for a path is anchored to something already
verified:

| Value | Reaches | Guard |
| :--- | :--- | :--- |
| `command[0]` | subprocess argv | literal `python3`, `shell=False` |
| `command[1]` | subprocess argv | `is_relative_to(root.resolve())` and `is_file()` |
| `case["id"]` | path component | the anchor assertion below |
| `scratch_sprint_dir` | path component | one relative component, **and** the anchor assertion |
| `render` keys | `copyfile` source | resolves inside `docs/standards/templates/` |
| `render` values | `copyfile` target | resolves inside the **verified** anchor |
| `exceptions[].reason` | nothing | typed set, mirrored against the declaration so the two cannot drift |

**The anchor is verified before anything is measured against it**, in `run_case`,
between computing `sprint_dir` and validating what hangs from it:

```python
sprint_dir = scratch / case["id"] / case["scratch_sprint_dir"]
if not sprint_dir.resolve().is_relative_to(scratch.resolve()):
    return f"{case['id']}: scratch sprint directory escapes the temporary directory"
```

Asserting the anchor rather than each field is deliberate: it closes the class, so
a fourth component joined onto that expression is contained without anyone
remembering to guard it. `check_render_paths` states the caller's obligation in
its own docstring, at the place a future contributor would otherwise reorder.

**And the enumeration itself is the finding.** A decision record that lists the
controls of a security boundary invites the implementation to match the list and
stop. `ADR-0012` §2.3 was that list. This ADR states the property — every
declaration-derived value is guarded, path guards anchor to verified ground — and
gives the table as evidence of the property, not as its definition.

## 3. Consequences

**Easier.** A reviewer can trace any field of the declaration to its guard in one
table, and the anchor assertion means new fields inherit containment rather than
needing to be remembered.

**Harder.** Nothing measurably. The checks are exact-path comparisons on a handful
of strings per run.

**Known and accepted, recorded rather than discovered later.** `command[2:]` is
unconstrained: a declaration may pass any arguments to any validated in-repository
Python script, including one that writes. The accepted threat model is
reviewed in-repository content — the same trust `make verify` already places in
every script it runs. Separately, `{sprint_dir}` is expanded after `check_command`
validated the unexpanded vector; reaching it would require a file literally named
`{sprint_dir}` in the tree, since `command[1]` must already resolve to an existing
in-root file to survive validation. Both were traced by Gate 1 round 3 and left
open deliberately, not missed.

**Superseded, not corrected in place.** `ADR-0012` remains readable as the record
of the decision as it was accepted, including the enumeration that proved
insufficient. That is the point of the immutability rule in
`rules/documentation_standard.md §3`: deleting the four-item list would delete the
evidence of how a documented control became an undone one.

## 4. Deciders

GstMirabal (Approval Gate, Sprint 042, 2026-08-31). Findings by the Sprint 042
Gate 1 (`qa_agent`) in fresh context across three rounds; remediation authored
under the `implementer_agent` ruleset; this record under `doc_orchestrator`.

## 5. Considered Options

| Option | Pros | Cons |
| :--- | :--- | :--- |
| **Supersede `ADR-0012` with this record (chosen)** | `rules/documentation_standard.md §3` provides exactly this mechanism for a changed decision; keeps the insufficient enumeration visible as evidence | Two ADRs describing one mechanism; a reader must follow the pointer |
| Edit `ADR-0012` §2.3 in place to list seven constraints | One document, immediately correct | Prohibited by `§3`, and it would erase the record of how the four-item list produced the defect — the most useful thing either document contains |
| Leave `ADR-0012` and record the gap only in `SPRINT_LOG.md` | Cheapest | The sprint record is history nobody consults when editing the checker. The ADR is what a future contributor reads, and it would still say four |
| Validate each declaration field individually as findings arrive | Direct, minimal per fix | The pattern that produced the round-2 defect: `scratch_sprint_dir` was guarded while `case["id"]` beside it was not |

---
*Immutable once Accepted — a changed decision gets a new ADR that supersedes this one, never an in-place edit (`rules/documentation_standard.md §3`). File lives at `docs/decisions/ADR-0013-declaration-containment.md`.*
