# Rule Context: Documentation Standard

Governs how project documentation is classified, structured, and kept fresh. Consolidates Diátaxis (reader-intent classification), C4 (architecture zoom levels), ADR (decision records), and a deterministic freshness gate that replaces trust-based "an agent will remember to update this" with scripted verification at sprint close. Loaded when creating/updating any document under `docs/`, when authoring an ADR, or when `close_workflow.md` Phase 1 runs `docs-freshness-check`.

## 1. Diátaxis — Reader-Intent Classification

Every document is exactly one of four types. A document that needs content from a second type links to the artifact that owns that type instead of absorbing it inline.

| Type | Owning artifact |
| :--- | :--- |
| **Reference** (current-state facts, no rationale) | `[MODULE]_BLUEPRINT.md` |
| **Explanation** (why, alternatives considered) | ADR log |
| **How-to** (task-oriented steps) | `docs/guides/[MODULE]_[TASK]_GUIDE.md` |
| **Tutorial** (learn by doing) | `README.md` |

- **No absorption, either direction**: a Blueprint that needs to justify a decision links the relevant ADR instead of narrating it; a README that grows into an exhaustive reference (every config option, every field) has drifted into Reference territory and should link out instead.
- **Naming**: How-to files follow Option B (`[MODULE]_[TASK]_GUIDE.md`, English, RA-06). The in-document H1 is phrased as an imperative task ("How to add a new exchange to datafeed"), per Diátaxis's own convention for this type — file name and title serve different audiences (machine-sortable vs. human-scannable).
- **Enforcement**: Vale (prose linter) flags Explanation-register language appearing inside Reference-type documents. Base English vocabulary: `we decided`, `instead of`, `alternative`, `trade-off`, `chose X over Y`, `to avoid`, `to prevent`, `to ensure`, `deferred … to`, `rather than`, `so that`, `so as to`. Style package lives at `styles/Diataxis/Explanation.yml` (`StylesPath: styles` in `.vale.ini`), warning-only. Each host project may extend/localize this vocabulary in its own `.vale.ini` if it documents in a language other than English — the framework ships the default, the host declares its own layer on top.

## 2. C4 — Architecture Zoom Levels

- **Level 1 (Context)** and **Level 2 (Container)**: universal, one diagram each, living in `0_SYSTEM_OVERVIEW.md` / `0_SYSTEM_ARCHITECTURE.md`.
- **Level 4 (Code)**: not required — hand-maintained class diagrams go stale immediately; generate from source if ever needed.
- **Level 3 (Component)**: required per-container only where the formula below says so. Here "container" means a code-topology grouping (a declared directory), not necessarily C4's canonical deployable-unit sense.

### 2.1 Level 3 eligibility formula

1. **Stack** — the density-comparison cohort, typically a language/runtime tier. A stack must hold enough containers for a percentile to be meaningful; declaring many single-container stacks defeats the mechanism.
2. **`code_containers` declaration** — each host project declares its own roots as a sibling root key in `docs/active_state.json` (never nested inside `topology_map`, which holds only flat string paths and is maintained by `topology-mapper`):
   ```json
   "code_containers": [
     {"stack": "backend", "root": "backend/apps/"},
     {"stack": "frontend", "root": "frontend/src/modules/"}
   ]
   ```
   Container identity = the tuple `(stack, first directory segment after the declared root)`. Files sitting directly under a root with no subdirectory of their own are excluded from the container set (they would otherwise register as a phantom zero-density container). Nodes whose `Source` matches no declared root are excluded from the calculation entirely. **A project with no `code_containers` declared runs Level 3 in advisory mode only** — this is the correct default, not a missing feature.
3. **Primitive filter** — a per-language denylist (shipped defaults: Python, JS/TS, Go at minimum, at `scripts/denylists/`) excludes builtin/primitive types from density scoring. No graph-native flag distinguishes primitives from real classes, so this denylist is a maintained artifact, not a computed one. If the detected language has no denylist (shipped or host-declared), that stack stays advisory rather than running the filter empty.
4. **Density** — `Σ(degree of filtered nodes in container) / count(filtered nodes in container)`.
5. **Cutoff** — 75th percentile of density, computed **separately within each stack**, never across stacks. A single cross-stack percentile lets the stack with the naturally higher density band dominate the whole ranking regardless of architectural importance.
6. **Safety floor** — with fewer than 5 containers in a stack the percentile can degenerate; the single highest-density container of that stack always qualifies regardless.
7. **Escape hatch** — a project may declare additional containers as Level-3-required by hand, but the override can only *add* to the computed set, never remove a container the formula already selected. Every manual override must cite a justification: one of the ADR triggers (§3.1) or an existing ADR, recorded in the Blueprint's metadata block: `**C4 Level Override**: 3 (justification: ADR-0007)`.
8. **Bootstrap** — the first run on a new project, or any stack with no denylist/containers declared, is advisory, never blocking.

### 2.2 Live-pointer validation

`docs-freshness-check` verifies every `C4 Level Override` justification resolves to an ADR that exists and is not superseded (superseded → `WARN`). Applies to Blueprints (living content) only — a stale pointer inside a historical Walkthrough is an acceptable record of the past, not a defect.

## 3. ADR — Architecture Decision Records

Immutable once accepted; a changed decision gets a new, numbered ADR that supersedes the old one — never an in-place edit. Files live at `docs/decisions/ADR-XXXX-[slug].md` (four-digit zero-padded number, e.g. `docs/decisions/ADR-0007-jwt-signing-key-separation.md`), created from `ADR_TEMPLATE.md`.

### 3.1 Triggers

A decision requires an ADR if it meets any of:

1. Any operation carrying risk of irreversible data loss (schema migration is the common case; also mass deletes, key rotation without escrow, decommissioning a data source with no backup).
2. Changes a contract/interface consumed by another container.
3. Touches a security, authentication, or data-privacy boundary.
4. Adds or removes a hard-to-replace external dependency.
5. The affected node is a god-node (per the knowledge graph).
6. Touches an availability/reliability boundary (removing redundancy, changing failover strategy, introducing a single point of failure).
7. Critical logic that knowingly operates incomplete, simulated, or degraded behind a flag, against real production traffic or data, as the *sole* path for that operation. Does not fire for an intentional, time-boxed canary with a defined rollback path — only when the degraded path is the only path available.

### 3.2 Format scaling

Nygard (Context/Decision/Consequences) by default. Escalates to full MADR (adds Considered Options with pros/cons) if 2+ triggers fire simultaneously, **or if trigger #1, #3, #5, or #7 fires individually** — these four represent severe, immediate-harm risk (data loss, security/privacy breach, god-node blast radius, degraded logic live in production) and warrant full treatment even alone. Triggers #4 and #6 are future-reversal-cost, not immediate-harm, and never auto-escalate individually — they follow the default trigger-count rule.

A host project may redeclare which triggers auto-escalate for its own domain via a root key in `active_state.json`: `"adr_autoescalate_triggers": [1, 3, 5, 7]` (the shown array is the framework default). This is authoring guidance, not a deterministic gate check — nothing in `docs-freshness-check` enforces it.

## 4. Freshness-Gate

Deterministic script (`scripts/docs_freshness_check.py`, invoked as `make docs-freshness-check`), runs in `close_workflow.md` Phase 1, gates `SESSION LOCKED` (Phase 6). Nothing in this section depends on an agent "remembering."

### 4.1 Metadata convention

Fields live in the same bold-key block every real template already uses under its H1 — **not** YAML frontmatter:

```
**Last Audit Sprint**: 083
**Last Audit Date**: 2026-07-21
**Last Audit Commit SHA**: a1b2c3d
```

Parsed via regex over `**Field**: value` lines, anchored to the region between the H1 and the first `---` (where every real template already places its metadata block). A repeated field outside that region doesn't count; a repeated field inside it is `WARN` — same pattern as the duplicate-ADR-ID check below.

### 4.2 Rollout

First cycle a host adopts this gate: `WARN` only. From the second cycle: `BLOCK`.

### 4.3 Structural-change condition

A delta in `graphify graph_stats` (new community, or node/edge count change) between `last_audit_sprint` and the current sprint, plus a second trigger (a new or newly-promoted god-node). Threshold: 90th percentile of the historical deltas over the last **N=10** sprints (fewer if the project has less history) — self-recalculating, never a fixed number to re-litigate. `BLOCK` does not activate until at least 5 historical deltas exist; before that, the gate stays `WARN` regardless of cycle. A close with no prior `graph_stats.json`/`last_audit_*` (a project's first sprint) is a clean `WARN` pass, never an error.

**Data source**: `close_workflow.md` Phase 1 persists a git-tracked, sprint-tagged snapshot at `graph_stats.json` inside the canonical sprint directory (`agents.md §5 mandatory_topology`) on every close. Deltas are computed exclusively from these records — never from `graphify-out/`, which is gitignored and holds untagged tool-maturation re-runs, not sprint-to-sprint deltas.

### 4.4 Documentation integrity

All `WARN`-level, run every close:

- Every `C4 Level Override → ADR-XXXX` reference resolves to a file that exists (not just "not superseded" — existence itself).
- Every `Superseded by ADR-XXXX` chain resolves to an ADR that exists.
- No duplicate ADR numbers.
- Every `code_containers[].root` exists as a real directory; if not, that container is excluded from the calculation with a warning, never silently.
- Gaps in the `docs/sprints/*/graph_stats.json` series within the N=10 window are skipped but flagged — a gap can indicate corruption (a manually deleted file), not just expected absence.

## 5. Templates

| Template | Diátaxis type | Notes |
| :--- | :--- | :--- |
| `BLUEPRINT_TEMPLATE.md` | Reference | arc42-lite: Introduction & Goals (trimmed) · Context & Scope · Building Block View · Runtime View · Crosscutting Concepts · Glossary. Its own §9-equivalent is a linked list of the module's ADRs, not inline rationale. |
| `ADR_TEMPLATE.md` | Explanation | Nygard/MADR, scaled per §3.2. |
| `GUIDE_TEMPLATE.md` | How-to | Goal · Prerequisites · Steps (may branch into alternatives, unlike a Tutorial) · Verify it worked · If something goes wrong. |
| `README_TEMPLATE.md` | Tutorial | Out of scope for this rule — a host's own branding/identity question, not a governance concern. |
| `SYSTEM_OVERVIEW_TEMPLATE.md` | — (Documentation Entry Point anchor) | Carries the same metadata block (§4.1) plus C4 Level 1-2 diagrams. |
| `WALKTHROUGH_TEMPLATE.md` | — (historical narrative, outside Diátaxis) | Links the ADR behind a decision instead of re-explaining it. |
| `IMPLEMENTATION_PLAN_TEMPLATE.md` | — (pipeline planning) | Mandatory **Documentary impact (T5)** section from Sprint 029 (§6). |

## 6. Documentary impact and measured figures (T5)

**In force from Sprint 029 onward.** Plans sealed before 029 are not rewritten
to add this section (`021-030-program-queue.md` J4).

| Obligation | Where it lives | Done-criterion |
| :--- | :--- | :--- |
| Declare every doc/config/script this sprint creates or changes | `IMPLEMENTATION_PLAN.md` → **Documentary impact (T5)** | Table rows name paths; empty table only when the sprint truly touches none |
| Every measured figure carries the command that reproduces it | Same plan's Context / Design / Verification | A reader can re-run the command and get the figure; adjectives without commands are rejected at Phase 1 |

The cheap `file:line` range check in `scripts/verify_references.py` (living
`docs/guides`, `docs/decisions`, `docs/audits`) is complementary and **does not
replace** T5: it catches citations out of range, not wrong-but-in-range claims.

### T5 extends to status, not only to figures (Sprint 042)

**A status claim in a living document is a measured figure and carries the command
that re-measures it.** `021-030-program-queue.md` called a finding the program's
most severe open item for five sprints after a hotfix closed it; Sprint 042's
Phase 1 read that prose, proposed the closed work as the sprint's scope, and
withdrew only after re-measuring the code. The cost is a planning round, and it is
paid by whoever reads the document next.

| Obligation | Done-criterion |
| :--- | :--- |
| A finding marked closed is marked closed **where the ordering decision is made** — the roadmap that says what is worked on next — not only in the audit register | `grep` the corpus for the identifier before the correction is called complete (`RA-14`) |
| The closing entry names the artifact that closed it, the date, and the command that re-measures | A reader verifies instead of trusting |
| Superseded prose is **annotated in place, never deleted** | The record of what was true when it was written survives beside the correction |

### An enumeration in a decision record becomes the implementation's ceiling

`ADR-0012` listed four constraints and called them *the containment*. The
implementation matched that list exactly and contained nothing — the document is
what made the gap invisible, and a reader treating the list as complete would
re-derive the same defect. **State the property; give the list as evidence of the
property, never as its definition.** When the list proves insufficient, the
correction is a superseding ADR (§3) — deleting the insufficient list would delete
the evidence of how a documented control became an undone one.
