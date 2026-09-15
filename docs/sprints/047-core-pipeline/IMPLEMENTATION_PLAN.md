# Implementation Plan: Sprint 047 — nucleus-audit-design-remediation

**Canonical path**: `docs/sprints/047-core-pipeline/IMPLEMENTATION_PLAN.md`
**Branch**: `ai-sprint/047` · **Base**: `main` at `3dd8537`
**Status**: ~~`DRAFT`~~ → `APPROVED` → `EXECUTING` → `CLOSED`

> Authored at Phase 1 (Planning) by `principal_agent`, extracted to this path at
> Phase 3, and **committed before Phase 5 approves it**: `agents.md §2 triple_lock`
> names the approved Implementation Plan as its first lock, and a lock cannot close
> over an artifact that does not exist.
>
> Spanish is permitted in this document (`agents.md §1 user_chat`). Every other
> pipeline artifact is English.

---

## Context

Sprint 045 (`nucleus-ruleset-mechanism-audit`, `v4.28.0`, PR #78) ran a full
obsolescence audit of the framework corpus and produced 29 actionable `S045-*`
rows plus `KI-045-1`/`KI-045-2`, all `routing_class: nucleus`, analysis-only —
it applied nothing (`strict_rule`: `agents.md` changes go through a planned
sprint unit).

Sprint 046 (`nucleus-audit-mechanical-remediation`, `v4.29.0`, PR #79) applied
the **18-row mechanical bucket** (`S045-01, 03, 04, 05, 07, 08, 10, 11, 12, 13,
15, 16, 21, 23, 24, 25, 26, 28`) + `KI-045-1`. It deliberately did **not** take
the rows whose fix is a design decision rather than a transcription.

**This sprint is the declared design-pass bucket.** Scope fixed by the human at
Planning to the complete bucket, exactly as recorded in
`docs/roadmaps/core/pipeline/021-030-program-queue.md:13` and the *Queued for 047*
sections of that file:

| Source | Rows |
| :--- | :--- |
| Sprint 045 design-pass `S045-*` | `S045-02, 06, 09, 14, 17, 18, 19, 20, 22, 27` |
| Sprint 045 extract | `KI-045-2` (RA-14 headline-metrics extension) |
| Sprint 046 Gate 2 (`testifying`) | `KI-046-3` (`check_gate_log.py` HTML-comment blindness) |
| Sprint 043/044 Gate-2 findings, re-routed 045 → 046 → 047 | submodule-mode anchor *read* (`session_start.py`, `detect_drift.py`, `_mode.is_nucleus()` in a worktree) |
| Sprint 044 extract | `submodule_purity.py --ignored` anchor scan |
| Sprint 044 extract | RA-14 extension for `rule_validator` (grep the sprint's **artifact set**, bound to the remediation step) |

**True when done**: every row above is either applied or explicitly routed out
with a destination; `make verify` green; `agents.md §7` IDs `RA-01`..`RA-18` **not**
renumbered (`RA-04` tombstone / `RA-10` pointer stay rows in place — same
constraint as Sprint 046); the drafted Sprint 045 amendment texts (`A2`, `A3`,
`A6`, `A7` and the Unit 1 rewrites) are applied *after* being re-verified against
the current tree, not transcribed blind — Sprint 046 `F-046-QA1` is the precedent
for a faithfully transcribed but defective drafted amendment.

Prior-session cost at draft time: cycle ratio **4.8×** first turn
(`python3 scripts/session_cost.py --from-anchor --json` → `cycles[0].ratio`),
well under the 5× soft threshold.

---

## Design

### D1 — Grouping: one physical file per unit, drafted text re-verified before apply

`agents.md §2 jurisdictional_lock` + `RA-08`: one unit = one atomic commit whose
structural subject is one physical file. Where Sprint 045 produced drafted
amendment text (`NUCLEUS_{RULESET,WORKFLOW}_AUDIT_REPORT-045.md`), the executor
**re-runs the evidence command in that row against the current tree** before
applying, and treats a drafted text that no longer matches reality as a Phase 1
regression to route back — not something to transcribe (Sprint 046 `F-046-QA1`).

### D2 — `agents.md` is one unit carrying four `§`-level edits (U1)

`S045-02` (§1), `S045-06` (RA-01), `S045-09` (RA-02 row → pointer), and the
consolidated RA-14 extension (`KI-045-2` + the Sprint 044 proposal) all land in
`agents.md` as **one commit**. Rationale: this mirrors Sprint 046's "`agents.md`
×7" single-commit precedent, and `RA-14 PATCH_PROPAGATION` is best satisfied by
editing every `agents.md` reference to a term in one pass rather than across
commits. `RA-01`..`RA-18` row order and IDs are **not** touched.

### D3 — `KI-045-2` and the Sprint 044 RA-14 proposal are consolidated

Both extend `RA-14`. `KI-045-2`: a deliverable's **headline metrics** (verdict
counts, cross-reference targets) must be a `grep`-reproducible figure derived
from the body register, not carried from author prose. Sprint 044 proposal:
extend the mandatory patch-propagation grep from "the same artifact" to "the
sprint's **artifact set**", and bind it to the **remediation step**, not only
the reviewer's spot-check. These are one amendment to `RA-14` with two clauses —
applied together in U1, not as two rows.

### D4 — `S045-17` canonical SkillOpt block lives in `rules/skills_and_integrations.md` (U5)

The `train_runner.py` mechanism is cited three ways in three workflows
(`audit_workflow.md precision_audit`, `close_workflow.md rules_optimization`,
`skill_forge_workflow.md skillopt_run`), each with its own authorization clause.
One canonical invocation block (full path, args, config, done-criterion,
authorization gate) is written **once** in `rules/skills_and_integrations.md §3`
(the skills/integrations rule, its natural home); the three workflow steps
reference it (`RA-14` spirit). Chosen over `rules/token_economy.md` because the
block is about *how to invoke a skill*, not *what a prompt costs*.

### D5 — `S045-14` applies the drafted `A2`/`A3` texts verbatim-after-verification

`workflows/audit_workflow.md`: `precision_audit` gets the real `train_runner.py`
invocation (`--skill agents.md --config <path> --eval-only`), a skip-if-absent
clause, and a written-diff done-criterion (drafted `A2`). `nomenclature` gets the
canonical `docs/sprints/[Sprint_ID]-[Stack]-[Layer]/` path and the
non-destructive verb "lists … as a rename candidate for human approval"
(`agents.md §2 destructive_flags`); `report` names
`docs/audits/PIPELINE_AUDIT_REPORT-[Sprint_ID].md` (`RA-06` Option B); with D4
in place, `precision_audit` **references** the U5 block instead of restating the
invocation. `skill_standard_check` drops the `.agents/skills/…` host prefix for
bare `skills/…` (parity with sibling `link_audit`).

### D6 — `S045-18`/`S045-19` are `RA-14`-frozen-numbering-safe

`reverse_documentation_workflow.md` fractional numbering is deliberately frozen
(`RA-14`, in-file line 51). U8 adds a **parenthetical step id** per row
(`Phase 5 (correct_false)` …) without changing any phase number, and an
`<a id="findings-handoff"></a>` at Phase 9.5 so the `audit_workflow.md`
frontmatter `invoked_by` anchor resolves mechanically. U9 reshapes
`repository_hardening_workflow.md`'s prose Execution-Flow list into a
`Phase | Step id | Operation | Verify` table, lifting the `gh api` verify calls
out of the prose, and adds a **Mode** line stating nucleus applicability. The
`last_harden_run` anchor field (workflow-audit meta-finding 3) is **out of
scope** — it is not an `S045-*` row and adds a new mechanism.

### D7 — `S045-22` + `S045-27` are coupled script enhancements with test surface

`verify_references.py` check (d) currently confirms a workflow *has* an invoker
and that filename mentions resolve, but does not resolve `#anchor` fragments in
`invoked_by:` (which is how `remediation_workflow.md#functional_lock` passed
before Sprint 046 repointed it). U11 extends check (d) to resolve
`file.md#anchor` against the target file's headings / step ids and fail on an
unresolvable fragment. U12 gives `map_workflows.py` a skip-marker (or second
column) so non-step table rows are excluded from step parsing, and distinguishes
"ambiguous verb" from "prose step" from "not a step" in the generated guide.
U12's commit **includes the regenerated `WORKFLOWS_STEP_MAP_GUIDE.md`** — it is
generator output, never hand-edited, and `make verify` gates its staleness.

### D8 — submodule-mode anchor *read* (`S`-rider): read follows write

`F-BOOT-2` (Sprint 044) host-scoped the anchor *write* (claim/probe run with
`cwd = agents_root().parent` in submodule mode). The *read* is still
framework-anchored: `session_start.py` `load_anchor(root)` is called with
`root = repo_root()` (parent of `scripts/`) unconditionally, so `/agents:start`
in a host prints "docs/active_state.json: absent or unreadable" over a live host
anchor. U15 makes `load_anchor`'s root host-scoped when `not is_nucleus()`.
`detect_drift.py` already documents itself host-scoped (docstring: "MUST NOT
adopt `scripts/_root.py`") — U16 **verifies** `main()`'s root resolution matches
that claim and repairs only if it does not; if it is already correct, U16's test
becomes a regression guard, not a fix. `_mode.is_nucleus()` returns `False`
inside a linked git worktree of the nucleus (a worktree's `.git` is a file):
U17 distinguishes a worktree pointer (`gitdir:` into the nucleus's own
`.git/worktrees/…`) from a submodule pointer (`gitdir:` into a superproject).

### D9 — `submodule_purity.py --ignored` (E)

`git -C .agents status --porcelain -uall` does not list ignored files, so a
stray gitignored `.agents/docs/active_state.json` written by a buggy
submodule-mode session is invisible to the one check built to catch host
contamination (`agents.md §5 mandatory_topology` documents the same blindness for
`docs/sprints/`). U18 adds a `--ignored` scan of the anchor paths
(`docs/active_state.json`, `.agent_state/`) to `submodule_purity.py`; U6 updates
the `close_workflow.md` Phase 5 `submodule_purity` prose to name it.

### D10 — Tests: `implementer-agent`, not `tester_agent`

`tester_agent` executes the suite; it does not write test files (`F-026-A1`).
The pytest units (U19–U23) are authored by `implementer-agent`. Pure-prose units
(U1–U10) have no pytest surface — their gate is `make verify` (`verify_references.py`,
`map_workflows.py` staleness, `scan_workflow_determinism.py`,
`check_template_gates.py`).

### Rejected alternatives

| Rejected | Why |
| :--- | :--- |
| Split the bucket into 047 (rules/workflows) + 048 (scripts) | Human scoped 047 to the complete bucket; the roadmap declares it as one. A natural commit-group boundary (U1–U13 prose vs U14–U23 behaviour) is kept **inside** the sprint. |
| Renumber `RA-*` to close the `RA-04`/`RA-10` gaps | 100+ external by-number citations; Sprint 045/046 both explicitly forbid it. Tombstone + pointer rows stay. |
| Transcribe drafted `A2`/`A3`/`A6`/`A7` verbatim without re-verification | Sprint 046 `F-046-QA1`: a faithfully transcribed drafted amendment (`A4`) asserted a template that does not exist and was rejected at Gate 1. Every drafted text is re-checked against the tree first (D1). |
| Put the canonical SkillOpt block in `rules/token_economy.md` | The block is invocation mechanics, not prompt cost. `rules/skills_and_integrations.md` is its home (D4). |
| Add `last_harden_run` to the anchor as part of U9 | Workflow-audit meta-finding 3, not an `S045-*` row; new mechanism. Routed to *Out of scope*. |

---

## Work

One row per unit. One unit is one atomic commit (`RA-08`) touching **one physical
file** as its structural subject (`agents.md §2 jurisdictional_lock`).

The Work column `Assignee (proposed)` is a staffing proposal from Phase 1. Phase
4.1 (`agent_orchestrator`) is the authority that records the assignee.

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| U1 | `agents.md` | modify — `S045-02` (§1 `linter_command`+`Complexity`: `Verified by:` pointer to `python-quality-auditor`/`js-standardizer`, state "not in `make verify`", repoint/drop `python-doctor`/`react-doctor` names); `S045-06` (RA-01 → executable directive + `invoked_by`-style pointer); `S045-09` (RA-02 row → "See `rules/django_backend_standard.md §2 Signal Registration`"); RA-14 extension (`KI-045-2` headline-metrics clause + Sprint 044 sprint-artifact-set / remediation-step clause) | high | `rule_validator` | ⏳ |
| U2 | `rules/django_backend_standard.md` | modify — `S045-09`: move RA-02 operative text ("local imports inside the receiver; lazy sender strings") into §2 as the definition; drop the circular "single definition in `agents.md §7`" deferral | medium | `rule_validator` | ⏳ |
| U3 | `rules/LEGACY_RULE_CONCORDANCE.md` | modify — `S045-09`: add `Clause J-02` → `rules/django_backend_standard.md §2` (RA-02 anchor) row so legacy citations resolve; `verify_references.py` fails on an unmapped `Clause`/`Rule NN` | low | `rule_validator` | ⏳ |
| U4 | `workflows/audit_workflow.md` | modify — `S045-14`: apply `A2` (`precision_audit` real `train_runner.py` invocation via U5 ref, skip-if-absent, written-diff done-criterion), `A3` (`nomenclature` canonical sprint path + non-destructive verb; `report` → `PIPELINE_AUDIT_REPORT-[Sprint_ID].md`), `skill_standard_check` bare `skills/…` path parity | medium | `rule_validator` | ⏳ |
| U5 | `rules/skills_and_integrations.md` | modify — `S045-17`: add one canonical SkillOpt `train_runner.py` invocation block (full path, `--skill`/`--config`, done-criterion `exit 0`, explicit-authorization gate) in §3 | medium | `rule_validator` | ⏳ |
| U6 | `workflows/close_workflow.md` | modify — `S045-17`: `rules_optimization` references the U5 block instead of restating; `D9`: Phase 5 `submodule_purity` prose names the `--ignored` anchor scan | medium | `rule_validator` | ⏳ |
| U7 | `workflows/skill_forge_workflow.md` | modify — `S045-17`: `skillopt_run` references the U5 block; keep the `--profile-path` route added in Sprint 046 | low | `rule_validator` | ⏳ |
| U8 | `workflows/reverse_documentation_workflow.md` | modify — `S045-18` (`A7`): parenthetical step id per phase 2–10 (no phase renumber, `RA-14` frozen numbering); `<a id="findings-handoff"></a>` at Phase 9.5 | low | `rule_validator` | ⏳ |
| U9 | `workflows/repository_hardening_workflow.md` | modify — `S045-19` (`A6`): reshape Execution-Flow prose list → `Phase \| Step id \| Operation \| Verify` table, lift `gh api` verify calls from prose; add "Mode" line (nucleus applicability) | medium | `rule_validator` | ⏳ |
| U10 | `workflows/standardization_workflow.md` | modify — `S045-20`: `condition_check` names the actor + `legacy_app_auditor.py`/`noise_purge`; mark `/backend/` host-only; tag the Legacy Routing Table with a skip-marker so `map_workflows.py` (U12) excludes it | medium | `rule_validator` | ⏳ |
| U11 | `scripts/verify_references.py` | modify — `S045-22`: check (d) resolves `file.md#anchor` in `invoked_by:` against the target file's headings / step ids; unresolvable fragment → exit `2` (same as unresolvable filename) | high | `implementer-agent` | ⏳ |
| U12 | `scripts/map_workflows.py` | modify — `S045-27`: skip-marker / column so non-step table rows are excluded from step parsing; label "ambiguous verb" vs "prose step" vs "not a step". Commit includes regenerated `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` | high | `implementer-agent` | ⏳ |
| U13 | `scripts/check_gate_log.py` | modify — `KI-046-3`: `gate_tables()` skips `<!-- … -->` regions so a commented example row below a real header is not parsed as data | medium | `implementer-agent` | ⏳ |
| U14 | `scripts/session_start.py` | modify — `D8`: `load_anchor` root is host-scoped (`agents_root().parent`) when `not is_nucleus()`; nucleus mode unchanged | high | `implementer-agent` | ⏳ |
| U15 | `scripts/detect_drift.py` | modify — `D8`: verify `main()` root resolution is host-scoped in submodule mode (docstring claims it); repair only if it is not | high | `implementer-agent` | ⏳ |
| U16 | `scripts/_mode.py` | modify — `D8`: `is_nucleus()` returns `True` inside a linked git worktree of the nucleus (distinguish worktree `gitdir:` → nucleus `.git/worktrees/…` from submodule `gitdir:` → superproject) | high | `implementer-agent` | ⏳ |
| U17 | `scripts/submodule_purity.py` | modify — `D9` / E: add a `--ignored` scan of the anchor paths (`docs/active_state.json`, `.agent_state/`) to catch a stray gitignored anchor | high | `implementer-agent` | ⏳ |
| U18 | `tests/test_verify_references.py` | modify/create — `S045-22`: assert check (d) exits `2` on an unresolvable `#anchor` in `invoked_by:` and `0` on a resolvable one | medium | `implementer-agent` | ⏳ |
| U19 | `tests/test_map_workflows.py` | modify/create — `S045-27`: assert a non-step table row is not emitted as a step; ambiguous-verb vs prose-step labels are distinct | medium | `implementer-agent` | ⏳ |
| U20 | `tests/test_check_gate_log.py` | modify/create — `KI-046-3`: assert an example row inside `<!-- … -->` placed below a real header is not parsed as gate data | medium | `implementer-agent` | ⏳ |
| U21 | `tests/test_mode.py` | modify/create — `D8`: `is_nucleus()` `True` for a simulated worktree `.git` file, `False` for a submodule-style pointer | medium | `implementer-agent` | ⏳ |
| U22 | `tests/test_session_start.py` | modify/create — `D8`: `load_anchor` reads the host anchor (`agents_root().parent/docs/active_state.json`) in a simulated submodule layout | medium | `implementer-agent` | ⏳ |
| U23 | `tests/test_submodule_purity.py` | modify/create — E: a gitignored stray `docs/active_state.json` in the framework tree is reported by the `--ignored` scan | medium | `implementer-agent` | ⏳ |

**Commit groups (inside the one sprint):** U1–U10 prose/governance (gate: `make
verify`); U11–U17 script behaviour; U18–U23 tests. Groups are sequential; no
`no_interference` overlap (each unit is a distinct physical file).

---

## Dependencies

| Package | Version | Why the standard library and the existing dependencies do not suffice |
| :--- | :--- | :--- |
| None | — | Every change is to existing `agents.md` / `rules/` / `workflows/` prose or to existing stdlib-only scripts and their `pytest` suites. |

---

## Mechanisms

| Mechanism | Deterministic or agent judgment | Invoker (`RA-16`) |
| :--- | :--- | :--- |
| `verify_references.py` check (d) `#anchor` resolution (U11) | deterministic — extends an existing `make verify` check | `Makefile#verify` (unchanged) |
| `map_workflows.py` non-step skip-marker (U12) | deterministic — extends an existing generator + its staleness gate | `Makefile#verify` (unchanged) |
| `check_gate_log.py` HTML-comment skip (U13) | deterministic — extends an existing gate | `Makefile#verify` + `close_workflow.md` Phase 2.6 (unchanged) |
| `submodule_purity.py --ignored` scan (U17) | deterministic — extends an existing check | `hooks/on_commit.py` + `close_workflow.md` Phase 5 (unchanged) |

No **new** recurring mechanism is proposed. Every change hardens a mechanism that
already has a declared invoker; no invoker is added or removed.

---

## Cost

| Field | Value | Reproduce |
| :--- | :--- | :--- |
| Delegation | `native` | `docs/active_state.json` `delegation_mode` |
| Work units | 23 | Count of rows in the Work table |
| Subagents dispatched | ≤ 8 per pipeline pass (`agents.md §6`); Execution fans out `rule_validator` (U1–U10) and `implementer-agent` (U11–U23) per unit | `docs/active_state.json` `delegation_mode: native` |
| Prior session ratio | 4.8× (current session at draft time; no distinct prior-session figure in anchor) | `python3 scripts/session_cost.py --from-anchor --json` → `cycles[0].ratio` |

Soft (5×) / hard (15×) thresholds force an update to this section before new
work continues — they are not observational-only once a measurable Claude
transcript exists for this tool. This is a large sprint (23 units); if the hard
threshold fires before U23, `session_state.py suspend` and resume in a fresh
session (`resume_pointer` from `config/artifact_registry.json`).

---

## Tests

**Reproduce before repairing.** A test that passes against the current tree proves
nothing about a defect claimed to exist in it.

| Check | Fails against the current tree? |
| :--- | :--- |
| `verify_references.py` check (d) rejects a workflow whose `invoked_by:` names `file.md#nonexistent-anchor` | **Yes** — the defect (`S045-22`; this is why `#functional_lock` passed) |
| `map_workflows.py` output distinguishes a non-step table row from an ambiguous-verb step | **Yes** — the defect (`S045-27`; both render as `?`) |
| `check_gate_log.py` ignores an example gate row inside `<!-- … -->` placed below a real header | **Yes** — the defect (`KI-046-3`; `gate_tables()` scans raw lines) |
| `_mode.is_nucleus()` returns `True` inside a linked git worktree of the nucleus | **Yes** — the defect (`D8`; a worktree `.git` is a file) |
| `session_start.load_anchor` reads the host anchor in submodule mode | **Yes** — the defect (`D8`; `root = repo_root()` unconditionally) |
| `detect_drift.py` resolves its root against the host tree in submodule mode | **No** if the docstring is accurate — then U15 adds a regression guard; **Yes** if `main()` contradicts the docstring |
| `submodule_purity.py` reports a gitignored stray `.agents/docs/active_state.json` | **Yes** — the defect (E; `--porcelain -uall` does not list ignored files) |
| `make verify` green after U1–U10 (`verify_references.py`, `map_workflows.py` staleness, `scan_workflow_determinism.py`, `check_template_gates.py`) | **No** — regression to protect; it is green now and must stay green |
| `agents.md §7` still reads `RA-01 … RA-18` with `RA-04` tombstone / `RA-10` pointer as rows | **No** — regression to protect (no renumber) |

---

## Verification

| Command | Expected |
| :--- | :--- |
| `python3 skills/token-saver-auditor/scripts/audit_plan.py docs/sprints/047-core-pipeline/IMPLEMENTATION_PLAN.md; echo $?` | `0` |
| `make verify; echo $?` | `0` (after every commit group) |
| `venv_skillopt/bin/python -m pytest tests/ -q; echo $?` | `0` |
| `python3 scripts/verify_references.py; echo $?` | `0` |
| `grep -n 'RA-04\|RA-10' agents.md` | `RA-04` tombstone row + `RA-10` pointer row present; no renumber |
| `grep -c 'python-doctor\|react-doctor' agents.md` | `0` (names dropped/repointed — `S045-02`) |
| `python3 scripts/map_workflows.py --check; echo $?` | `0` (guide not stale after U12 regen) |
| `venv_skillopt/bin/python -m graphify update . --force; echo $?` | `0` (Phase 8) |

---

## Documentary impact (T5)

| Artefacto | Qué cambia |
| :--- | :--- |
| `agents.md` | §1 `linter_command`/`Complexity` gain `Verified by:` + "not in `make verify`" note; `RA-01` becomes an executable directive; `RA-02` row → pointer; `RA-14` gains the headline-metrics + sprint-artifact-set clauses |
| `rules/django_backend_standard.md` | §2 gains the RA-02 operative text as its own definition |
| `rules/LEGACY_RULE_CONCORDANCE.md` | new `Clause J-02` → `django_backend_standard.md §2` row |
| `rules/skills_and_integrations.md` | §3 gains the canonical SkillOpt `train_runner.py` invocation block |
| `workflows/audit_workflow.md` | `precision_audit` / `nomenclature` / `report` / `skill_standard_check` rewritten (`A2`/`A3`, path parity) |
| `workflows/close_workflow.md` | `rules_optimization` references the canonical block; Phase 5 prose names `submodule_purity --ignored` |
| `workflows/skill_forge_workflow.md` | `skillopt_run` references the canonical block |
| `workflows/reverse_documentation_workflow.md` | parenthetical step ids (phases 2–10); `#findings-handoff` anchor |
| `workflows/repository_hardening_workflow.md` | Execution-Flow prose → `Phase \| Step id \| Operation \| Verify` table; "Mode" line |
| `workflows/standardization_workflow.md` | `condition_check` names actor + tool; `/backend/` host-only; routing table skip-marker |
| `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` | regenerated by `map_workflows.py` (U12) — non-step rows no longer render as `?` steps |
| `scripts/{verify_references,map_workflows,check_gate_log,session_start,detect_drift,_mode,submodule_purity}.py` | behaviour changes per the Work table; docstrings updated |
| `tests/test_{verify_references,map_workflows,check_gate_log,mode,session_start,submodule_purity}.py` | new/extended cases (U18–U23) |
| `CHANGELOG.md` `[Unreleased]` | Sprint 047 closeout entry |
| `docs/roadmaps/core/pipeline/021-030-program-queue.md` | 047 line + *Queued for 047* sections marked delivered |

**Measured figures.** Prior-session ratio 4.8× —
`python3 scripts/session_cost.py --from-anchor --json`. Bucket row list —
`docs/roadmaps/core/pipeline/021-030-program-queue.md:13` and
`docs/audits/NUCLEUS_AUDIT_SYNTHESIS-045.md:15`.

---

## Out of scope

| Exclusion | Why, and where it goes instead |
| :--- | :--- |
| `last_harden_run` anchor field + `platform_probe` surfacing | Workflow-audit meta-finding 3, not an `S045-*` row; adds a new mechanism. → new roadmap line under *Still open for a later program*. |
| `S045-29` | Deferred by the Sprint 045 synthesis itself (`:15`). → stays deferred. |
| Renumbering `RA-04` / `RA-10` to close the ID gap | 100+ external by-number citations. → permanent: tombstone + pointer rows. |
| The 193 repo-wide `ruff` findings (`S045-02` / T3) | Not this bucket; no sprint has owned them. → `021-030-program-queue.md` *Still open for a later program* T3. |
| Full sandbox auto-retry for `graphify` (`C-4`, Sprint 043) | Claude Code owns the sandbox; explicitly not taken in 043. → unchanged. |
| Zero-Memory Initialization boilerplate consolidation (workflow-audit duplication finding 2) | Each workflow is loaded independently; "arguably acceptable". → not pursued. |

---

## Abort criterion

Stop and revert the branch if, **after re-verifying a drafted Sprint 045
amendment against the current tree (D1)**, applying it makes `make verify` or
`verify_references.py` red in a way that cannot be resolved without redesigning
the amendment text itself (i.e. the drafted `A2`/`A3`/`A6`/`A7` or a Unit 1
rewrite is structurally defective, as `A4` was in Sprint 046 `F-046-QA1`). In
that case the affected row returns to a design pass on the roadmap and the
sprint proceeds with the remaining units — a full revert only if more than half
the prose units (U1–U10) are so affected.

Also abort if U16 (`_mode.is_nucleus()` worktree fix) cannot distinguish a
worktree pointer from a submodule pointer reliably across git versions without a
git call that fails under the sandbox — route that unit to a hotfix with a
git-version matrix instead.

---

## Approval — `triple_lock` lock 1

| Field | Value |
| :--- | :--- |
| **Approved by** | GstMirabal (`gst.mirabal@gmail.com`) — Phase 5, attended, not in a `/loop` |
| **Date** | 2026-09-09 |
| **Plan commit at approval** | `a995d6f` (`docs/sprints/047-core-pipeline/IMPLEMENTATION_PLAN.md` on `ai-sprint/047`) |
| **Remaining locks** | Active Sprint ✅ (id 47, `IN_PROGRESS`) · QA + Tester verdicts (pending Phase 7) · Human OK at close (pending Phase 8) |

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
