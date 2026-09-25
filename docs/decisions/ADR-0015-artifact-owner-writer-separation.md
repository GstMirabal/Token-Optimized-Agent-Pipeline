# 📜 ADR-0015: `config/artifact_registry.json` separates artifact owner from writer

**Status**: `Superseded by ADR-0017` — implementation (companion unit `U9`, `config/artifact_registry.json`) found the `role`/`writer` split true for the three Principal-Agent-owned artifacts this ADR examined, and false for `active_state.json`, `mirror.json` and `graph.json`, whose owner (DevOps Agent) holds no `Write` and whose files are materialized by a script or Makefile target, not by any profile editing them. `ADR-0017` carries the full decision, typed to admit a script/make-target writer alongside a profile one; this record is kept intact as the reasoning it restates and the gap it did not yet cover.
**Date**: 2026-09-25
**Triggers**: 2 (`rules/documentation_standard.md §3.1`) — changes a contract (`config/artifact_registry.json`'s schema) consumed by other containers (`scripts/docs_freshness_check.py`, `scripts/map_workflows.py`, `close_workflow.md` Phase 2.6, `scripts/check_role_artifact.py`). Trigger #2 does not auto-escalate individually (`§3.2`), so this ADR is Nygard-format.

---

## 1. Context

`config/artifact_registry.json` names **Principal Agent** as `role` for
`IMPLEMENTATION_PLAN.md` (`:37`), `PHASE_REGISTER.md` (`:96`) and
`CHANGELOG.md` (`:116`), and `workflows/pipeline_workflow.md` Phase 8 assigns
the last two to `principal_agent` by name. `agents/principal_agent.md:4`
declares `tools: Read, Glob, Grep, TodoWrite` — no `Write`, no `Edit`.

Reproduced live rather than read (`F-051-R1`,
`docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` ~line 1413): a Sprint 051
session dispatched that profile to author its own Implementation Plan,
received the text in the agent's final message, and had to file it itself. A
host reported the same gap narrower, as the closeout `CHANGELOG` row being
staffed to a profile that cannot write it.

The registry's own `_fields` block calls `role` *advisory* — "who usually
writes it" (`:13`). That softens the contract but does not remove the
problem: three required artifacts name a writer that cannot write, so every
sprint either usurps the role or discovers the gap at the keyboard.

The finding names two available fixes that redraw the role boundary in
opposite directions: give `principal_agent` `Write` for its own declared
documents, or have the registry name a writer separately from the owner.
`ADR-0009` used the *second* reasoning to refuse `devops_agent` `Write` over
framework-root `scripts/`: a tool grant cannot be scoped to a set of paths, a
registry field can be tested.

## 2. Decision

`config/artifact_registry.json` gains a `writer` field on every artifact
entry, alongside the existing `role`. The two fields answer different
questions from now on: `role` names the profile whose ruleset governs the
artifact's **content** (the owner — unchanged for the three artifacts below);
`writer` names the profile that holds `Write`/`Edit` and **materializes** the
file at its declared path. `principal_agent` stays owner (`role`) of
`IMPLEMENTATION_PLAN.md`, `PHASE_REGISTER.md` and `CHANGELOG.md` — it debates
and authors their content; it does not touch the filesystem.

Recommended `writer` per artifact, chosen from the profiles that already hold
`Write`/`Edit` (`agents/*.md` `tools:`), justified from each profile's own
charter:

| Artifact | Phase | Recommended `writer` | Why this profile |
| :--- | :--- | :--- | :--- |
| `IMPLEMENTATION_PLAN.md` | Phase 1 (authored), materialized Phase 3 | `orchestrator` | `agents/orchestrator.md` already writes `SPRINT_LOG.md` at this same phase and its charter is to "instantiate the `docs/sprints/[ID]` hierarchy" — filing the plan `principal_agent` negotiated into that same hierarchy is a direct extension of that duty, not a new one |
| `PHASE_REGISTER.md` | Phase 8 (Sprint Closeout) | `doc_orchestrator` | `agents/doc_orchestrator.md` charter is writing and maintaining project documentation as Markdown; a phase register is a documentation artifact, not a roadmap or code artifact |
| `CHANGELOG.md` | Phase 8 (Sprint Closeout) | `doc_orchestrator` | Same charter fit as above; Keep a Changelog formatting is markdown documentation work, matching `doc_orchestrator`'s `tabular_standard` rule (prioritize Markdown over prose) |

Rejected: granting `principal_agent` `Write`/`Edit` directly. Same reasoning
`ADR-0009` used to refuse `devops_agent` `Write` over `scripts/`: a tool
grant is all-or-nothing for the profile, not scoped to the three named
paths, while a `writer` registry field can be asserted per artifact by a
test.

`tests/test_artifact_registry.py` (companion unit `U9`) asserts that every
declared `writer` names a profile whose `agents/<writer>.md` `tools:` line
contains `Write`.

## 3. Consequences

**Easier**

- A session dispatching subagents for Phase 1, 3 or 8 artifact writes has a
  machine-checkable `writer` to dispatch instead of usurping the role or
  hand-writing the file itself — the exact failure `F-051-R1` reproduced.
- A future profile losing `Write` (a tool-grant edit that forgets this
  dependency) fails `tests/test_artifact_registry.py` instead of silently
  reintroducing the gap.

**Harder / accepted risk**

- Two names now describe one artifact (`role` for content ownership,
  `writer` for the filesystem act). Every consumer of the registry that
  currently reads `role` as "who writes this" — the field's own docstring
  says exactly that today (`:13`) — must be corrected to read `writer`
  instead; `scripts/map_workflows.py` and `scripts/docs_freshness_check.py`
  do not yet read a `writer` field and need the schema change wired in
  alongside it (companion unit `U9`).
- `orchestrator` and `doc_orchestrator` gain a duty — materializing content
  `principal_agent` authors or negotiates — that is not yet stated in their
  own profile-rule tables. `workflows/pipeline_workflow.md` Phases 1 and 8
  must name it explicitly (companion unit `U10`) so the handoff is not left
  to inference.

---
*Immutable once Accepted — a changed decision gets a new ADR that supersedes this one, never an in-place edit (`rules/documentation_standard.md §3`). File lives at `docs/decisions/ADR-0015-artifact-owner-writer-separation.md`. Closes upstream `F-051-R1`. Cross-references `ADR-0009` (implementer role; the tool-grant-vs-registry-field reasoning this ADR reuses).*
