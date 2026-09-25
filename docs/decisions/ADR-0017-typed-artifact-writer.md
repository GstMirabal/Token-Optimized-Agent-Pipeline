# 📜 ADR-0017: `config/artifact_registry.json` `writer` is typed — profile, script, or make target

**Status**: `Accepted`
**Date**: 2026-09-25
**Triggers**: 2 (`rules/documentation_standard.md §3.1`) — changes a contract (`config/artifact_registry.json`'s schema) consumed by other containers (`scripts/docs_freshness_check.py`, `scripts/map_workflows.py`, `close_workflow.md` Phase 2.6, `scripts/check_role_artifact.py`, `tests/test_artifact_registry.py`). Trigger #2 does not auto-escalate individually (`§3.2`), so this ADR is Nygard-format.

**Supersedes**: `ADR-0015` (`docs/decisions/ADR-0015-artifact-owner-writer-separation.md`) — restates its full decision below plus the typed-writer extension, so this record stands alone.

---

## 1. Context

### 1.1 What ADR-0015 decided (restated, unchanged)

`config/artifact_registry.json` named **Principal Agent** as `role` for
`IMPLEMENTATION_PLAN.md`, `PHASE_REGISTER.md` and `CHANGELOG.md`, and
`workflows/pipeline_workflow.md` Phase 8 assigned the last two to
`principal_agent` by name. `agents/principal_agent.md` declares
`tools: Read, Glob, Grep, TodoWrite` — no `Write`, no `Edit`.

Reproduced live rather than read (`F-051-R1`,
`docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` ~line 1413): a Sprint 051
session dispatched that profile to author its own Implementation Plan,
received the text in the agent's final message, and had to file it itself. A
host reported the same gap narrower, as the closeout `CHANGELOG` row being
staffed to a profile that cannot write it.

The registry's own `_fields` block called `role` *advisory* — "who usually
writes it". That softened the contract but did not remove the problem: three
required artifacts named a writer that cannot write, so every sprint either
usurped the role or discovered the gap at the keyboard.

ADR-0015's decision: `config/artifact_registry.json` gains a `writer` field
on every artifact entry, alongside the existing `role`. The two fields answer
different questions: `role` names the profile whose ruleset governs the
artifact's **content** (the owner); `writer` names the profile that holds
`Write`/`Edit` and **materializes** the file at its declared path.
`principal_agent` stays owner (`role`) of `IMPLEMENTATION_PLAN.md`,
`PHASE_REGISTER.md` and `CHANGELOG.md` — it debates and authors their
content; it does not touch the filesystem. Recommended writers, chosen from
profiles already holding `Write`/`Edit`:

| Artifact | Phase | `writer` | Why this profile |
| :--- | :--- | :--- | :--- |
| `IMPLEMENTATION_PLAN.md` | Phase 1 (authored), materialized Phase 3 | `orchestrator` | Already writes `SPRINT_LOG.md` at this same phase; filing the plan `principal_agent` negotiated into the sprint hierarchy is a direct extension of that duty |
| `PHASE_REGISTER.md` | Phase 8 (Sprint Closeout) | `doc_orchestrator` | Charter is writing and maintaining project documentation as Markdown; a phase register is a documentation artifact |
| `CHANGELOG.md` | Phase 8 (Sprint Closeout) | `doc_orchestrator` | Same charter fit; Keep a Changelog formatting is markdown documentation work |

Rejected by ADR-0015: granting `principal_agent` `Write`/`Edit` directly — a
tool grant is all-or-nothing for the profile, not scoped to three named
paths, while a `writer` registry field can be asserted per artifact by a
test (the same reasoning `ADR-0009` used to refuse `devops_agent` `Write`
over framework-root `scripts/`).

### 1.2 What implementation found false

Companion unit `U9` (commit `0a55351`) wired `writer` into every entry of
`config/artifact_registry.json` and into `tests/test_artifact_registry.py`.
Doing so for the full artifact set — not only the three Principal-Agent-owned
documents ADR-0015 examined — found artifacts ADR-0015 did not name, whose
files are **mechanically materialized**, not written by any profile's
`Write` tool at all:

- `active_state.json` — written by `scripts/session_state.py`, never by hand
  for the fields it owns (`agents.md §5 state_anchor`).
- `mirror.json` — written by the `hooks/state_mirror.py` Stop hook.
- `graph.json` — written by the `graphify-update` Makefile target
  (`close_workflow.md` Phase 5 `graph_rebuild`).

Each of these artifacts' `role` is **DevOps Agent**, and `agents/devops_agent.md`
holds no `Write`/`Edit` for these paths as a matter of design, not gap:
`agents.md §6 devops_agent` retains `Bash` for environment routines and
explicitly does not hold `Write`/`Edit` over framework-root mechanisms.
Naming a `Write`-holding profile such as `topology_mapper` as `writer` for
these three would record a **false writer** — the file is not, in fact,
materialized by that profile editing it — and would redraw a role boundary
by improvisation rather than by decision, the same defect class ADR-0015 was
written to close.

A fourth artifact, `graph_stats.json`, is hand-persisted at close
(`workflows/close_workflow.md:18`, Phase 1 `docs_freshness_gate`) and names
no acting profile at all — the snapshot is written by hand mid-gate, not by
a dedicated script or make target. It keeps a profile-type `writer`
(`doc_orchestrator`, ADR-0015's own reasoning: the persisting step sits
inside a documentation-freshness gate and that profile's charter is
authoring and maintaining project documentation artifacts), because unlike
the three above, no mechanism name exists to cite in its place.

## 2. Decision

`config/artifact_registry.json`'s `writer` field is **typed**. A declared
`writer` MUST take exactly one of three forms:

| Form | Syntax | Resolution requirement |
| :--- | :--- | :--- |
| Profile | bare snake_case identifier matching an `agents/<writer>.md` filename stem | that profile's `tools:` line MUST contain `Write` (or `Edit`) |
| Script | `script:<repo-relative path>` | the path MUST exist in the repository |
| Make target | `make:<target>` | the target MUST be defined in the nucleus `Makefile` |

`role` is unchanged by this ADR (ADR-0015 §1.1 stands): it names the profile
accountable for the artifact's content, and a `role` without `Write` (e.g.
Principal Agent, DevOps Agent) still owns that content even when `writer`
names a mechanism rather than that same profile.

`tests/test_artifact_registry.py` (`test_every_writer_resolves`) asserts
every declared `writer` resolves per its form: a bare profile id holds
`Write`; `script:`/`make:` name a real script path or Makefile target.

### Mapping table, as shipped (`config/artifact_registry.json`, `version: 1`)

| Artifact | `role` | `writer` | Form |
| :--- | :--- | :--- | :--- |
| `IMPLEMENTATION_PLAN.md` | Principal Agent | `orchestrator` | Profile |
| `SPRINT_LOG.md` | Orchestrator | `orchestrator` | Profile |
| `agent_assignment.md` | Agent Orchestrator | `agent_orchestrator` | Profile |
| `skill_assignment.md` | Skill Architect | `skill_architect` | Profile |
| `task_scope.md` | Rule Validator | `rule_validator` | Profile |
| `graph_stats.json` | DevOps Agent | `doc_orchestrator` | Profile |
| `PHASE_REGISTER.md` | Principal Agent | `doc_orchestrator` | Profile |
| `active_state.json` | DevOps Agent | `script:scripts/session_state.py` | Script |
| `CHANGELOG.md` | Principal Agent | `doc_orchestrator` | Profile |
| `memory_index.json` | Governance Learner | `governance_learner` | Profile |
| `graph.json` | DevOps Agent | `make:graphify-update` | Make target |
| `mirror.json` | DevOps Agent | `script:hooks/state_mirror.py` | Script |
| `AGENTS_SLASH_COMMANDS_GUIDE.md` | Doc Orchestrator | `doc_orchestrator` | Profile |

Rejected: naming a `Write`-holding profile as `writer` for the three
mechanically materialized artifacts (`active_state.json`, `mirror.json`,
`graph.json`) to keep every `writer` value in one shape. Closes the schema
neatly but records a false writer — none of `topology_mapper`,
`devops_agent`, or any other `Write`-holding profile actually materializes
these files by editing them — and none of ADR-0015's reasoning (a profile
whose charter is the closest defensible fit) applies to a file no profile
touches at all. The typed field states what is true instead of what is
uniform.

## 3. Consequences

**Easier**

- A session or test asking "who/what actually writes this file" gets a
  verifiable answer for every artifact, including the ones no profile's
  `Write` tool touches — not only the three ADR-0015 examined.
- `tests/test_artifact_registry.py` fails closed on a `writer` that neither
  resolves to a `Write`-holding profile nor a real script/make target,
  instead of accepting an improvised profile name that happens to hold
  `Write` for unrelated reasons.
- A future artifact backed by a new script or Makefile target has a
  sanctioned way to say so without waiting for that mechanism to be wrapped
  in a profile first.

**Harder / accepted risk**

- Consumers reading `writer` as always a profile identifier (`ADR-0015`'s
  own framing) must branch on three forms instead of one. `scripts/map_workflows.py`
  and `scripts/docs_freshness_check.py` do not read `writer` at all today and
  are unaffected by the type split; a future consumer that starts reading
  `writer` must parse the `script:`/`make:` prefixes.
- The registry now carries two kinds of truth under one field name — "who is
  accountable" stays in `role`, "what materializes the bytes" is `writer`,
  and a `script:`/`make:` value has no `agents/*.md` ruleset to point to for
  further governance, only the file or target itself.

---
*Immutable once Accepted — a changed decision gets a new ADR that supersedes this one, never an in-place edit (`rules/documentation_standard.md §3`). File lives at `docs/decisions/ADR-0017-typed-artifact-writer.md`. Supersedes `ADR-0015` (`docs/decisions/ADR-0015-artifact-owner-writer-separation.md`), which is annotated in place per `rules/documentation_standard.md:145`, never edited beyond that annotation. Cross-references `ADR-0009` (implementer role; the tool-grant-vs-registry-field reasoning ADR-0015 reused and this ADR retains).*
