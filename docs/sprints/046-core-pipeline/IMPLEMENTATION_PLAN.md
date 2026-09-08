# Implementation Plan: Sprint 046 — nucleus-audit-mechanical-remediation

**Canonical path**: `docs/sprints/046-core-pipeline/IMPLEMENTATION_PLAN.md`
**Branch**: `ai-sprint/046` · **Base**: `main` at `8265c09c8a12c8a2d79fdc290670fa899f4cb6de`
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

Sprint 045 (`nucleus-ruleset-mechanism-audit`, deployed `v4.28.0`, PR #78) ran a
full obsolescence audit of the framework corpus and **applied nothing** — by
design (`docs/sprints/045-core-pipeline/IMPLEMENTATION_PLAN.md` decision D1). It
left four reports under `docs/audits/` and a consolidated register of 29
actionable rows (`S045-01`..`S045-29`), every one `routing_class: nucleus`,
bucketed into a recommended execution sprint:

| Bucket | Rows | Reproduce |
| :--- | :--- | :--- |
| `046` — mechanical, one-file, stated done-criterion | 18 (`S045-01,03,04,05,07,08,10,11,12,13,15,16,21,23,24,25,26,28`) | `docs/audits/NUCLEUS_AUDIT_SYNTHESIS-045.md §4` ¶1 |
| `047` — needs a design pass | 10 (`S045-02,06,09,14,17,18,19,20,22,27`) | same, ¶2 |
| `defer` — needs a human policy call | 1 (`S045-29`) | same, ¶3 |
| `RECORD` — no action | 1 (`S045-30`) | synthesis register row |

This sprint executes the **046 bucket only** — the 18 mechanical rows — plus one
extract item from the Sprint 045 close, `KI-045-1`
(`docs/roadmaps/core/pipeline/021-030-program-queue.md`, "From the Sprint 045
extract"): `SPRINT_LOG_TEMPLATE.md` ships no Quality Gate table, so every sprint
hand-rolls it and invents a placeholder, and Sprint 045's `_(pending)_`
reddened `make verify` mid-close (Gate 2 T1).

**Scope decision (Planning-phase call, `021-030-program-queue.md` "Queued for
046").** The submodule-mode anchor *read* fix (`session_start.py:56` `load_anchor`,
`detect_drift.py` host-scoping, `_mode.is_nucleus()` in a worktree) and the
`submodule_purity.py --ignored` scan from the Sprint 044 extract were competing
for this slot. They are **out of scope** here (see *Out of scope*): they are a
different theme (submodule-mode field defects) from audit remediation, and the
synthesis recommends 046 stay the coherent mechanical batch.

**True when done:**

- Every one of the 18 `S045-*` rows is applied to its named file with the
  drafted amendment text from the Wave-1 unit reports
  (`NUCLEUS_{RULESET,WORKFLOW,MECHANISM}_AUDIT_REPORT-045.md`), verified against
  the current tree first (`grep` assertion per unit, *Tests* table).
- `SPRINT_LOG_TEMPLATE.md` carries a Quality Gate table stub with the RA-17
  verdict vocabulary named in a comment.
- `make verify` exits `0` on `ai-sprint/046` HEAD.
- `agents.md §7` amendment IDs `RA-01`..`RA-18` are **not renumbered**
  (`NUCLEUS_AUDIT_SYNTHESIS-045.md §4` "DO NOT TOUCH"): `RA-04` and `RA-10`
  become tombstone / pointer rows **in place**.
- The Wave-1 unit reports and the synthesis are updated to mark the 18 rows
  applied (status column), so a later reader is not sent to re-apply them.

---

## Design

### D1 — One unit per physical file (`jurisdictional_lock`, `RA-08`)

`IMPLEMENTATION_PLAN_TEMPLATE.md` Work note: "One unit is one atomic commit
touching **one physical file**." Three `S045-*` rows carry an `RA-14` propagation
to a second (or third) file — the synthesis states this explicitly for `S045-05`
("Same patch fixes `rules/token_economy.md:11` and `workflows/pipeline_workflow.md:37`").
Rather than one multi-file commit (which `no_interference` / `check_task_scope.py`
would flag), each propagation target is its **own unit**, and the units are
grouped below so `rule_validator` (Phase 4.3) serialises them and the reviewer
greps the whole set. `RA-14` is satisfied because every propagation unit lands in
this same sprint / PR.

| `RA-14` propagation group | Primary unit | Propagation units |
| :--- | :--- | :--- |
| Bare tool/graph paths | `U04` (`agents.md §2`) | `U08` (`rules/token_economy.md`), `U09` (`workflows/pipeline_workflow.md`) |
| `§0`/`§3` self-duplication → pointers | `U06` (`agents.md`) | `U10` (`rules/LEGACY_RULE_CONCORDANCE.md`) |
| `RA-16`/`RA-15` print order | `U07` (`agents.md §7`) | `U11` (`docs/standards/templates/README_TEMPLATE.md`) |

### D2 — `agents.md` units serialise; never dispatched in parallel

Seven units (`U01`..`U07`) edit the always-loaded constitution `agents.md`, each a
distinct amendment in a different section. `no_interference` aborts a subagent
whose target file is already claimed by another in-progress subtask, so these
seven run **strictly sequentially** on one `ai-sprint/046` working tree — one
commit each (`RA-08` atomic: a tombstone and a pointer downgrade are two logical
changes, two commits).

### D3 — `RA-04` and `RA-10` are tombstoned in place, not deleted

`NUCLEUS_AUDIT_SYNTHESIS-045.md §4` "DO NOT TOUCH": there are 100+ external
citations of `agents.md §7` amendments **by number** across sprints, hooks,
guides and host records. `U01` replaces the `RA-04` row body with a tombstone
sentence ("Retired Sprint 046 — superseded by `§6 orchestrator` + `RA-12`.");
`U05` degrades `RA-10` to a pointer ("see `§8 Supply Chain Security`
(canonical)"). Neither renumbers `RA-05`..`RA-18`. The tombstone says *Sprint
046* (this sprint), correcting the synthesis draft's "Sprint 045" (nothing was
retired in 045).

### D4 — Drafted text is the source; re-verify against the tree first

Each unit applies the **drafted amendment** already written in the Wave-1 unit
report cell for that row — not a fresh redesign. But `RA-14` precedent (Sprint
045 Gate 1 R1 cited a skill that exists nowhere) means every unit first runs its
*Tests*-table `grep` against the current tree to confirm the defect still
reproduces. If a row's target reference was already corrected (e.g. by Sprint
045's own deployment), that unit is dropped and the drop is recorded in the
sprint log and the roadmap — it does not silently pass.

### D5 — `KI-045-1` stub shape follows the checker, not invention

`SPRINT_LOG_TEMPLATE.md` gains the table `Gate | Round | Verdict | Class | Notes`
(the shape `scripts/check_gate_log.py` and `pipeline_workflow.md` Phase 7 gate
on) with one commented example row and a comment naming the allowed verdict
vocabulary (`APPROVED | REJECTED | RECORD`, classes `charter | instructing |
testifying`, `rules/qa_and_testing.md §4`). If `config/template_gates.json`
requires a declared pairing for this template, `U24` also adds it (checked at
Phase 4.3 / execution; noted so it is not missed).

### D6 — Alternatives rejected

| Alternative | Rejected because |
| :--- | :--- |
| Bundle the 7 `agents.md` amendments into one commit | Violates `RA-08` atomic (7 unrelated logical changes) and makes a bisect useless. |
| Fold `S045-05`/`08`/`10` propagation into single multi-file commits | Violates the template's one-physical-file unit rule and trips `check_task_scope.py`. Split + group (D1) satisfies both `RA-14` and `jurisdictional_lock`. |
| Also take the submodule-mode anchor-read fix (was "competing for 046") | Different theme; the framework prohibits the scope creep of mixing audit remediation with field-defect fixes. Routed to a later sprint. |
| Delete `RA-04` / `RA-10` rows outright | Breaks 100+ external by-number citations (`NUCLEUS_AUDIT_SYNTHESIS-045.md §4`). |

---

## Work

One row per unit. One unit is one atomic commit (`RA-08`) touching **one physical
file**. `Origin` names the `S045-*` synthesis row (drafted amendment text lives in
the Wave-1 unit report for that row).

The Work column `Assignee (proposed)` is a staffing proposal from Phase 1. Phase
4.1 (`agent_orchestrator`) is the authority that records the assignee.

### Group A — `agents.md` (serialise, D2)

| # | File | Origin | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U01 | `agents.md` | `S045-01` | modify — `RA-04: FULL_DEPLOYMENT` row body → tombstone ("Retired Sprint 046 — superseded by `§6 orchestrator` + `RA-12`."); **no renumber** | medium | `rule-validator` | ⏳ |
| U02 | `agents.md` | `S045-03` | modify — `§3 federation` + `§5 discovery_manifest`: `install.sh` → `install.py` as the sanctioned bridge (`install.sh` = deprecation shim) | low | `rule-validator` | ⏳ |
| U03 | `agents.md` | `S045-04` | modify — `§3 enforcement`: `mass-standardizer` → `skills/topology-monitor/scripts/legacy_app_auditor.py` as the auditor; `mass-standardizer` regenerates `skills/manifest_skills.json` | low | `rule-validator` | ⏳ |
| U04 | `agents.md` | `S045-05` | modify — `§2 ast_skeleton` → full `skills/omni-context-minimizer/scripts/omni_minimizer.py` path; `graph_sovereignty` → `graphify-out/graph.json`; `graph_sync` → `venv_skillopt/bin/python -m graphify update .` | low | `rule-validator` | ⏳ |
| U05 | `agents.md` | `S045-07` | modify — `RA-10: SUPPLY_CHAIN_SHIELD` row → pointer ("see `§8 Supply Chain Security` (canonical)"); **no renumber** | medium | `rule-validator` | ⏳ |
| U06 | `agents.md` | `S045-08` | modify — `§0 Certification` → "See `RA-05: SPRINT_CLOSEOUT`"; `§3 secret_sovereignty` → "See `RA-09: SECRET_SOVEREIGNTY`" | low | `rule-validator` | ⏳ |
| U07 | `agents.md` | `S045-10` | modify — `§7` table: swap `RA-15` / `RA-16` rows so order reads `… RA-14, RA-15, RA-16, RA-17, RA-18`; no text change to either amendment | medium | `rule-validator` | ⏳ |

### Group B — `RA-14` propagation (D1)

| # | File | Origin | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U08 | `rules/token_economy.md` | `S045-05` | modify — line ~11 bare `omni_minimizer.py` → full `skills/omni-context-minimizer/scripts/omni_minimizer.py` | low | `rule-validator` | ⏳ |
| U09 | `workflows/pipeline_workflow.md` | `S045-05` | modify — line ~37 "Graph Sovereignty" bare `graph.json` → `graphify-out/graph.json` (align with `graph_sync` phrasing) | low | `doc-orchestrator` | ⏳ |
| U10 | `rules/LEGACY_RULE_CONCORDANCE.md` | `S045-08` | modify — line ~18 `Rule 66` authority → single authority (`RA-09: SECRET_SOVEREIGNTY`), drop the duplicate `§3 secret_sovereignty` citation | low | `rule-validator` | ⏳ |
| U11 | `docs/standards/templates/README_TEMPLATE.md` | `S045-10` | modify — line ~77 `§7` range `RA-01…RA-15` → `RA-01…RA-18` | low | `doc-orchestrator` | ⏳ |

### Group C — `rules/`

| # | File | Origin | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U12 | `rules/frontend_modular_standard.md` | `S045-11` | modify — retitle H1 to `# Rule Context: Frontend Modular Standard`; rename `(Rule 41.x)` subsections to keyed headings; add the intro + trigger line the sibling `rules/` files carry; replace `*Status: ACTIVE*` footer with the `documentation_standard.md §4.1` metadata block. Keep `LEGACY_RULE_CONCORDANCE.md:15` row intact | low | `doc-orchestrator` | ⏳ |
| U13 | `rules/project_topology.md` | `S045-12` | modify — add "Nucleus interpreter is `venv_skillopt/bin/python` (`Makefile`); the `./venv/` form is the host-project convention."; mark the DB / ETL sections `host-only` | low | `rule-validator` | ⏳ |

### Group D — `workflows/`

| # | File | Origin | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U14 | `workflows/remediation_workflow.md` | `S045-13` | modify — frontmatter `invoked_by:` dead `rules/qa_and_testing.md#functional_lock` anchor → `rules/qa_and_testing.md §4` + `pipeline_workflow.md#7-quality-gate` (Unit 2 amendment A1) | low | `doc-orchestrator` | ⏳ |
| U15 | `workflows/standardization_workflow.md` | `S045-15` | modify — Phase 6 end-state list: add `docs/0_SYSTEM_ARCHITECTURE.md` (from its template) beside `docs/0_SYSTEM_OVERVIEW.md` (Unit 2 amendment A4) | low | `doc-orchestrator` | ⏳ |
| U16 | `workflows/skill_forge_workflow.md` | `S045-16` | modify — `skillopt_run` bare `train_runner.py` → full `skills/skillopt/scripts/train_runner.py` + exit-0 done-criterion; `forge_destination` option (b) → add the `scripts/install.py --profile-path <path>` real-project route, keep `profiles/[name]/` for illustrative packs (Unit 2 amendment A5) | low | `doc-orchestrator` | ⏳ |

### Group E — `scripts/` + `hooks/`

| # | File | Origin | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U17 | `hooks/state_mirror.py` | `S045-21` | modify — replace bare `except json.JSONDecodeError: pass` (line ~27) with a `print("[state_mirror] active_state.json is not valid JSON; mirror skipped", file=sys.stderr)` (`agents.md §1 exception_handling`) | low | `implementer-agent` | ⏳ |
| U18 | `scripts/check_gate_log.py` | `S045-23` | modify — docstring line ~17 `2 — …(RA-11)` → `2 — vocabulary or class mismatch (RA-17; exit-code-2 blocking per RA-11 semantics)` | low | `implementer-agent` | ⏳ |
| U19 | `hooks/on_commit.py` | `S045-24` | modify — docstring "Exit codes" block (lines ~12-14) → `2 — rejected (blocks the git commit AND the Claude Code PreToolUse Bash call; RA-11 requires 2, not 1)`; no code change | low | `implementer-agent` | ⏳ |
| U20 | `scripts/merge_json.py` | `S045-25` | modify — add docstring line `invoked_by: scripts/install.py (import; non-destructive settings/mcp merge).` | low | `implementer-agent` | ⏳ |
| U21 | `scripts/cursor_adapter.py` | `S045-25` | modify — add docstring line `invoked_by: scripts/install.py (import; --target cursor\|both).` | low | `implementer-agent` | ⏳ |
| U22 | `scripts/audit_cursor_era.py` | `S045-28` | modify — add docstring line "Scope frozen to sprints 026-033 (Cursor era). Not stale — a bounded historical census, re-runnable but not expected to change." | low | `implementer-agent` | ⏳ |

### Group F — `config/` + templates

| # | File | Origin | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U23 | `config/invocation_exceptions.json` | `S045-26` | modify — add two `exceptions[]` entries (`skills/autoskills-3rd`, `skills/django-expert-3rd`) with `reason: "vendored-reference"` and a `note`, matching the four `django-*-3rd` siblings | low | `implementer-agent` | ⏳ |
| U24 | `docs/standards/templates/SPRINT_LOG_TEMPLATE.md` | `KI-045-1` | modify — add a Quality Gate table stub (`Gate | Round | Verdict | Class | Notes`) + a comment naming the RA-17 verdict vocabulary; add the `config/template_gates.json` pairing if the checker requires one | medium | `rule-validator` | ⏳ |

### Group G — evidence closeout

| # | File | Origin | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U25 | `docs/audits/NUCLEUS_AUDIT_SYNTHESIS-045.md` | — | modify — mark the 18 `046`-bucket rows applied (status / disposition note) with the `ai-sprint/046` reference; leave `047` / `defer` / `RECORD` rows untouched | low | `rule-validator` | ⏳ |
| U26 | `docs/audits/NUCLEUS_RULESET_AUDIT_REPORT-045.md` | — | modify — annotate the applied ruleset rows (`S045-01,03,04,05,07,08,10,11,12`) as executed in Sprint 046 | low | `rule-validator` | ⏳ |
| U27 | `docs/audits/NUCLEUS_WORKFLOW_AUDIT_REPORT-045.md` | — | modify — annotate the applied workflow rows (`S045-13,15,16`) as executed in Sprint 046 | low | `rule-validator` | ⏳ |
| U28 | `docs/audits/NUCLEUS_MECHANISM_AUDIT_REPORT-045.md` | — | modify — annotate the applied mechanism rows (`S045-21,23,24,25,26,28`) as executed in Sprint 046 | low | `rule-validator` | ⏳ |

**Not a Work unit** (Phase 8 / close machinery, listed for completeness): regenerate
`docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` via `scripts/map_workflows.py` if any
Group D edit changes a step table; append the Sprint 046 entry to `CHANGELOG.md`
`[Unreleased]`; mark Sprint 046 in-flight in
`docs/roadmaps/core/pipeline/021-030-program-queue.md`; rebuild the graph.

---

## Dependencies

| Package | Version | Why the standard library and the existing dependencies do not suffice |
| :--- | :--- | :--- |
| None | — | This sprint applies drafted text edits to existing files. It adds no package, no import, no tool. |

---

## Mechanisms

| Mechanism | Deterministic or agent judgment | Invoker (`RA-16`) |
| :--- | :--- | :--- |
| None | — | This sprint proposes no recurring (per-sprint or per-commit) mechanism. Every unit is a one-time edit. Existing gates (`make verify`, `verify_references.py`, `check_template_gates.py`, `check_gate_log.py`, `map_workflows.py` staleness) already cover the changed files and are the verification instrument, not a new mechanism. |

`RA-16 INVOCATION_COVERAGE`: no new workflow, script, executable skill, hook or
gate is introduced, so no new invoker declaration or
`config/invocation_exceptions.json` typed exception is required. `U23` **adds**
two exception entries for already-vendored skills — it does not create a
mechanism.

---

## Cost

| Field | Value | Reproduce |
| :--- | :--- | :--- |
| Delegation | `native` | `docs/active_state.json` `delegation_mode` |
| Work units | 28 (24 amendment + 4 audit-report closeout) | Count of rows in Work tables |
| Subagents dispatched | ~12 (est.: Phase 4 ×3, Phase 6 ×~7 batched by group, Phase 7 ×2) | `0` under Cursor `sequential` — n/a, this is Claude Code `native` |
| Prior session ratio | 3.9× (this session, measurable; soft 5× not reached). Sprint 045 close session is not on this anchor — n/a for a clean prior figure | `python3 scripts/session_cost.py --from-anchor --json` |

Soft (5×) / hard (15×) thresholds force an update to this section before new
work continues — not observational-only, a measurable Claude transcript exists
for this tool.

---

## Tests

**Reproduce before repairing.** Each row's assertion must currently show the
defect; after the unit it flips.

| Check | Fails against the current tree? |
| :--- | :--- |
| `grep -n 'RA-04' agents.md` shows the full `FULL_DEPLOYMENT` directive, not a tombstone | **Yes** — `S045-01` / `U01` |
| `grep -nE 'install\.sh' agents.md` — the `§3 federation` / `§5 discovery_manifest` lines call `install.sh` the exclusive bridge | **Yes** — `S045-03` / `U02` |
| `grep -n 'mass-standardizer' agents.md` — `§3 enforcement` names it "the official auditor for this standard" | **Yes** — `S045-04` / `U03` |
| `grep -nE 'omni_minimizer\.py|graph\.json' agents.md` — `§2` cites bare `omni_minimizer.py` and `graph.json` (root file absent: `ls graph.json` → no such file) | **Yes** — `S045-05` / `U04`, propagated `U08` (`rules/token_economy.md`), `U09` (`workflows/pipeline_workflow.md`) |
| `grep -n 'RA-10' agents.md` shows a full directive duplicating `§8`, not a pointer | **Yes** — `S045-07` / `U05` |
| `agents.md` `§0 Certification` and `§3 secret_sovereignty` carry full directive text (near-verbatim of `RA-05` / `RA-09`) | **Yes** — `S045-08` / `U06`, propagated `U10` |
| `grep -n 'RA-1[56]' agents.md` — `RA-16` prints before `RA-15` | **Yes** — `S045-10` / `U07`, propagated `U11` |
| `head -1 rules/frontend_modular_standard.md` → `# 🛡️ Rule 041: …`; footer is `*Status: ACTIVE*`, not the `§4.1` metadata block | **Yes** — `S045-11` / `U12` |
| `grep -n './venv/bin/python' rules/project_topology.md` with no nucleus-interpreter note | **Yes** — `S045-12` / `U13` |
| `grep -n 'functional_lock' workflows/remediation_workflow.md` → 1 hit in frontmatter; `grep -n 'functional_lock' rules/qa_and_testing.md` → 0 | **Yes** — `S045-13` / `U14` |
| `grep -n '0_SYSTEM_ARCHITECTURE' workflows/standardization_workflow.md` → 0 hits | **Yes** — `S045-15` / `U15` |
| `grep -nE 'train_runner\.py' workflows/skill_forge_workflow.md` → bare name; `grep -n 'profile-path' workflows/skill_forge_workflow.md` → 0 | **Yes** — `S045-16` / `U16` |
| `grep -n 'except json.JSONDecodeError' hooks/state_mirror.py` followed by a bare `pass`, no logging | **Yes** — `S045-21` / `U17` |
| `sed -n '17p' scripts/check_gate_log.py` attributes blocking `exit 2` to `(RA-11)` | **Yes** — `S045-23` / `U18` |
| `sed -n '12,14p' hooks/on_commit.py` says "1 — rejected" | **Yes** — `S045-24` / `U19` |
| `grep -n 'invoked_by' scripts/merge_json.py scripts/cursor_adapter.py` → 0 hits | **Yes** — `S045-25` / `U20`, `U21` |
| `grep -n 'frozen\|026-033\|Cursor era' scripts/audit_cursor_era.py` docstring has no scope-frozen note | **Yes** — `S045-28` / `U22` |
| `python3 -c "import json;e=json.load(open('config/invocation_exceptions.json'));print([x for x in e.get('exceptions',[]) if 'autoskills-3rd' in str(x) or 'django-expert-3rd' in str(x)])"` → `[]` | **Yes** — `S045-26` / `U23` |
| `grep -nE 'Verdict|Gate .*Round' docs/standards/templates/SPRINT_LOG_TEMPLATE.md` → 0 hits (no Quality Gate table) | **Yes** — `KI-045-1` / `U24` |
| `make verify` exits `0` | **No** — regression to protect; must stay `0` after every unit and at HEAD |
| `python3 scripts/verify_references.py` exits `0` | **No** — regression to protect (`U14`, `U20`, `U21`, `U23` touch reference-checked material) |

---

## Verification

| Command | Expected |
| :--- | :--- |
| `make verify; echo $?` | `0` |
| `python3 scripts/verify_references.py; echo $?` | `0` |
| `python3 scripts/map_workflows.py && git diff --exit-code docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md; echo $?` | `0` (regenerated guide committed if Group D changed a step table) |
| `python3 scripts/check_template_gates.py; echo $?` | `0` (covers `U24` / `SPRINT_LOG_TEMPLATE.md`) |
| `python3 -m json.tool config/invocation_exceptions.json >/dev/null; echo $?` | `0` (`U23` well-formed) |
| `python3 -m py_compile hooks/state_mirror.py hooks/on_commit.py scripts/check_gate_log.py scripts/merge_json.py scripts/cursor_adapter.py scripts/audit_cursor_era.py; echo $?` | `0` |
| `grep -cE '^\| RA-(0[1-9]\|1[0-8]) ' agents.md` | `18` — every amendment ID `RA-01`..`RA-18` still present, none renumbered |
| `grep -n 'functional_lock' workflows/remediation_workflow.md; echo $?` | `1` (no match) after `U14` |
| `python3 skills/token-saver-auditor/scripts/audit_plan.py docs/sprints/046-core-pipeline/IMPLEMENTATION_PLAN.md; echo $?` | `0` (Phase 1 / Phase 5 gate on this plan) |

---

## Documentary impact (T5)

| Artefacto | Qué cambia |
| :--- | :--- |
| `agents.md` | 7 amendments: `RA-04` tombstone, `RA-10` pointer, `§3`/`§5` `install.sh`→`install.py`, `§3` `mass-standardizer`→`legacy_app_auditor.py`, `§2` bare-path fixes, `§0`/`§3` duplication→pointers, `RA-15`/`RA-16` order. No amendment ID renumbered. |
| `rules/token_economy.md` | `omni_minimizer.py` reference → full path (`RA-14` propagation of `U04`). |
| `rules/LEGACY_RULE_CONCORDANCE.md` | `Rule 66` authority collapsed to a single citation (`RA-14` propagation of `U06`). |
| `rules/frontend_modular_standard.md` | Retitled to `Rule Context:` form, keyed subsection headings, `§4.1` metadata block, intro + trigger line. |
| `rules/project_topology.md` | Nucleus-interpreter line added; DB / ETL sections marked `host-only`. |
| `workflows/pipeline_workflow.md` | "Graph Sovereignty" bare `graph.json` → `graphify-out/graph.json` (`RA-14` propagation of `U04`). |
| `workflows/remediation_workflow.md` | Frontmatter `invoked_by:` dead anchor repointed to `rules/qa_and_testing.md §4`. |
| `workflows/standardization_workflow.md` | Phase 6 end-state list gains `docs/0_SYSTEM_ARCHITECTURE.md`. |
| `workflows/skill_forge_workflow.md` | `skillopt_run` full `train_runner.py` path + exit criterion; `forge_destination` gains the `--profile-path` real-project route. |
| `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` | Regenerated if `U14`/`U15`/`U16` alter a step table (frontmatter-only edits do not). |
| `hooks/state_mirror.py` | Bare `except: pass` → one stderr line (`§1 exception_handling`). |
| `hooks/on_commit.py` | Docstring "Exit codes" block corrected to RA-11 exit-2 semantics. No code change. |
| `scripts/check_gate_log.py` | Docstring line 17 re-attributed to `RA-17` (blocking per `RA-11`). |
| `scripts/merge_json.py`, `scripts/cursor_adapter.py` | Explicit `invoked_by:` docstring token (import-only invoker made literal). |
| `scripts/audit_cursor_era.py` | Docstring scope-frozen note (026-033, bounded census). |
| `config/invocation_exceptions.json` | Two `vendored-reference` exception entries added. |
| `docs/standards/templates/SPRINT_LOG_TEMPLATE.md` | Quality Gate table stub + verdict-vocabulary comment; `template_gates.json` pairing if required. |
| `docs/standards/templates/README_TEMPLATE.md` | `§7` amendment range `RA-01…RA-15` → `RA-01…RA-18`. |
| `docs/audits/NUCLEUS_AUDIT_SYNTHESIS-045.md` + 3 Wave-1 unit reports | 18 rows marked applied in Sprint 046; `047`/`defer`/`RECORD` rows untouched. |
| `docs/roadmaps/core/pipeline/021-030-program-queue.md` | Sprint 046 marked in-flight / delivered (Phase 8). |
| `CHANGELOG.md` (`[Unreleased]`) | Sprint 046 entry appended (Phase 8). |

**Measured figures.** Every number above carries its reproduce command in the
*Context*, *Tests* or *Verification* tables (`021-030-program-queue.md` J6 / T5).

---

## Out of scope

| Exclusion | Why, and where it goes instead |
| :--- | :--- |
| `S045-02, 06, 09, 14, 17, 18, 19, 20, 22, 27` (10 rows) | Need a design pass (enforcer wiring, cross-file text moves, `RA-14`-bound step-id renumbering, script enhancements). → **Sprint 047** (`NUCLEUS_AUDIT_SYNTHESIS-045.md §4` ¶2). |
| `S045-29` (`last_harden_run` field) | Needs a human policy call: does platform hardening apply to the nucleus itself? → **deferred** (synthesis §4 ¶3). |
| `S045-30` (`on_commit_msg.py` / `on_push.py` `return 1`) | `RECORD` only — native git hooks correctly use `exit 1`, outside `RA-11` scope. → no action, logged in synthesis so it is not re-raised. |
| `KI-045-2` (`RA-14` amendment: headline metrics must be `grep`-reproducible) | `agents.md` / `AUDIT_REPORT_TEMPLATE.md` edits go through a planned sprint unit; its own text queues it. → **Sprint 047**. |
| Submodule-mode anchor *read* (`session_start.py:56` `load_anchor`, `detect_drift.py` host-scoping, `_mode.is_nucleus()` in a worktree) | Different theme (submodule field defects, not audit remediation). Was "competing for 046"; human chose the mechanical batch. → a later sprint (`021-030-program-queue.md` "Queued for 046"). |
| `submodule_purity.py --ignored` scan (Sprint 044 extract) | Same theme as the anchor-read item, same routing. → a later sprint. |
| Sprint 044 `RA-14` amendment proposal (grep the sprint's artifact set, bind to remediation step) | `agents.md` edit → planned sprint unit. → **Sprint 047**. |
| 193 repo-wide `ruff` findings (`021-030-program-queue.md` T3) | Not created or worsened here; unowned. → a dedicated cleanup sprint. |

---

## Abort criterion

Stop and revert `ai-sprint/046` if **either**:

1. Applying a `S045-*` amendment as drafted requires renumbering `agents.md §7`
   `RA-05`..`RA-18` (the synthesis "DO NOT TOUCH" line) — the row is then routed
   to 047 for a redesign, not forced; if three or more of the 18 rows hit this,
   the whole batch is unsafe and the sprint aborts.
2. `make verify` cannot be returned to exit `0` after the batch within the
   Phase 7 round cap (`rules/qa_and_testing.md §4`, 3 consecutive `REJECTED` of
   the same block → `workflows/remediation_workflow.md`).

A single row whose defect no longer reproduces (D4) is **dropped and recorded**,
not an abort.

---

## Approval — `triple_lock` lock 1

| Field | Value |
| :--- | :--- |
| **Approved by** | _(pending Phase 5)_ |
| **Date** | _(pending)_ |
| **Plan commit at approval** | _(pending — filled at Phase 5 after the plan is committed on `ai-sprint/046`)_ |
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
