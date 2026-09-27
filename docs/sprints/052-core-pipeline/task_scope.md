# Task Scope — Sprint 052 (Session defects, the Python quality gate, and the open upstream register)

Phase 4.3 of `workflows/pipeline_workflow.md`. `jurisdictional_lock` and
`no_interference` (`agents.md §2`) are both applied by reading this file;
`scripts/loop_guard.py` measures progress from it; `workflows/close_workflow.md`
Phase 2.6 demands it as phase evidence. Authoritative source for assignees:
`docs/sprints/052-core-pipeline/agent_assignment.md` (Phase 4.1 — it overwrote
`U20` from `implementer_agent` to `rule_validator`). Risk column is transcribed
from `docs/sprints/052-core-pipeline/IMPLEMENTATION_PLAN.md` `## Work`.

Mode: **claude-code** (nucleus), `delegation_mode: native`, `session_tool: claude-code`
(`docs/active_state.json`). Model/Effort columns are required regardless of tool:
`scripts/check_task_scope.py:38` `MODEL_FROM_SPRINT = 28`, `sprint_id_from_dir` reads
`052` from this directory's name, `52 >= 28`.

**Model/Effort source** (`agents.md §6 rule_validator` `tier_transcription`):
`config/model_tiers.json` `tiers.author.claude_code` → `model: sonnet`,
`effort: medium`. `session_tool` is `claude-code`, not `cursor`, so the
`make cursor-tiers` obligation and the `audit_cursor_models.py` catalogue do not
apply to this sprint (`tier_transcription`'s Cursor clause is conditional on
`session_tool: cursor`). The four profiles staffed in this sprint —
`implementer_agent`, `doc_orchestrator`, `rule_validator`, `skill_architect` — are
**all** listed under `tiers.author.profiles` in the committed registry, so every
row's Model/Effort is `sonnet` / `medium` **regardless of Risk**: Risk selects
nothing in `model_tiers.json` (tiers are keyed by profile, not by risk); Risk's only
effect in `scripts/check_task_scope.py` is the mechanical-high escalation check
(`MECHANICAL_PROFILES = {devops_agent, git_sync_agent, topology_mapper}` at
`risk == "high"`), and **no unit in this sprint is staffed to a mechanical-tier
profile**, so that check fires on no row here. This is a read of the committed
registry, not an invented tier (precedent: `docs/sprints/051-core-pipeline/task_scope.md`
used the identical single-tier derivation).

Status `⏳` for every planned unit (none has executed yet — Phase 6 has not opened).
`K1..Kn` (Wave 6) is a **contingency** slot, triggered only if `U21` cannot verify
provenance for every `skills/skill-creator/{scripts,eval-viewer}/*.py` file; its
Status is `contingency`, not `⏳`, and rows are added under it only if triggered
(`IMPLEMENTATION_PLAN.md` `D2`).

---

## Work

### Wave 1 — Records

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U1 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | low | `doc_orchestrator` | sonnet | medium | ✅ `97a34e3` |

### Wave 2 — Session and anchor defects

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U2 | `scripts/session_start.py` (subject) + paired `tests/test_session_start.py` | fix( | medium | `implementer_agent` | sonnet | medium | ✅ `0622cb5` |
| U3 | `scripts/session_state.py` (subject) + paired `tests/test_session_state.py` | fix( | low | `implementer_agent` | sonnet | medium | ✅ `7382890` |
| U4 | `scripts/session_state.py` (subject) + paired `tests/test_session_state.py` | feat( | medium | `implementer_agent` | sonnet | medium | ✅ `3937194` |
| U5 | `scripts/session_start.py` (subject) + paired `tests/test_session_start.py` | fix( | low | `implementer_agent` | sonnet | medium | ✅ `fb820f1` |
| U6 | `workflows/start_workflow.md` | modify | low | `doc_orchestrator` | sonnet | medium | ✅ `aa03002` |
| U7 | `commands/start.md` | modify | low | `doc_orchestrator` | sonnet | medium | ✅ `980fb3f` |

`U6` carries an `RA-14` propagation obligation (grep `--takeover` across
`workflows/` — `IMPLEMENTATION_PLAN.md` U6), owed at the unit's own commit, not
restated here.

### Wave 3 — Upstream findings

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U8 | `docs/decisions/ADR-0015-artifact-owner-writer-separation.md` | create | low | `doc_orchestrator` | sonnet | medium | ✅ `b2eba19` |
| U8a | `docs/decisions/ADR-0017-typed-artifact-writer.md` (subject) + `Superseded by` annotation in ADR-0015 | create | low | `doc_orchestrator` | sonnet | medium | ✅ `b0cc724` |
| U9 | `config/artifact_registry.json` (subject) + paired `tests/test_artifact_registry.py` | feat( | medium | `implementer_agent` | sonnet | medium | ✅ `0a55351` |
| U10 | `workflows/pipeline_workflow.md` | modify | low | `doc_orchestrator` | sonnet | medium | ✅ `c35c634` |
| U11 | `scripts/check_role_artifact.py` (subject) + paired `tests/test_check_role_artifact.py` | fix( | high | `implementer_agent` | sonnet | medium | ✅ `11933ce` |
| U12 | `scripts/graph_reconcile.py` (subject) + paired `tests/test_graph_reconcile.py` | create | medium | `implementer_agent` | sonnet | medium | ✅ `a830894` |
| U13 | `Makefile` | modify | low | `implementer_agent` | sonnet | medium | ✅ `e59795a` |
| U14 | `docs/decisions/ADR-0016-test-database-isolation.md` | create | low | `doc_orchestrator` | sonnet | medium | ✅ `30a14db` |
| U15 | `agents.md` | modify | medium | `rule_validator` | sonnet | medium | ✅ `bbd8d0c` |
| U16 | `hooks/on_commit.py` (subject) + paired `tests/test_on_commit.py` | feat( | high | `implementer_agent` | sonnet | medium | ✅ `3c217ed` |
| U17 | `agents/qa_agent.md` | modify | low | `rule_validator` | sonnet | medium | ✅ `56d11c8` |
| U18 | `agents/tester_agent.md` | modify | low | `rule_validator` | sonnet | medium | ✅ `700913a` |

`U8a` was **added during Phase 6**, not planned. `U9` found that ADR-0015's "`writer` is always a Write-holding profile" is false for artifacts a script or Makefile target materializes (`active_state.json`, `mirror.json`, `graph.json`), and shipped a typed `writer` (`0a55351`). `rules/documentation_standard.md:50` makes an accepted ADR immutable, so the changed decision gets a superseding ADR.

`U10` carries an `RA-14` obligation (grep `principal_agent` authorship claims
across `pipeline_workflow.md`), owed at its own commit.

### Wave 4 — Invocation coverage (`KI-048-1`)

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U19 | `scripts/verify_references.py` (subject) + paired `tests/test_verify_references.py` | feat( | high | `implementer_agent` | sonnet | medium | ✅ `6a7fe27` |
| U20 | `config/invocation_exceptions.json` | modify | low | `rule_validator` | sonnet | medium | ✅ `3a11230` |

`U20`: reassigned from the plan's proposed `implementer_agent` to `rule_validator`
by `agent_assignment.md`'s recorded disagreement (`config/invocation_exceptions.json`
is an existing `RA-16` registry, outside `implementer_agent`'s `scripts/`/`hooks/`/`tests/`
write scope) — transcribed here, not re-litigated.

### Wave 5 — Quality-audit scope

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U21 | `config/quality_audit_exclusions.json` | create | medium | `implementer_agent` | sonnet | medium | ✅ `e0922dd` |
| U22 | `scripts/quality_audit.py` (subject) + paired `tests/test_quality_audit.py` | feat( | medium | `implementer_agent` | sonnet | medium | ✅ `6bc75b9` |

### Wave 6 — Refactor to zero (`R`, one file per unit, 42 independent units)

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U23 | `hooks/on_commit.py` | R | high | `implementer_agent` | sonnet | medium | ✅ `bdb3b40` |
| U24 | `hooks/on_init.py` | R | medium | `implementer_agent` | sonnet | medium | ✅ `18235fb` |
| U25 | `hooks/state_mirror.py` | R | medium | `implementer_agent` | sonnet | medium | ✅ `4e8e297` |
| U26 | `scripts/audit_cursor_era.py` | R | low | `implementer_agent` | sonnet | medium | ✅ `c542959` |
| U27 | `scripts/branch_sovereignty.py` | R | medium | `implementer_agent` | sonnet | medium | ✅ `67c406f` |
| U28 | `scripts/check_absolute_paths.py` | R | low | `implementer_agent` | sonnet | medium | ✅ `dd70ac2` |
| U29 | `scripts/check_forge_ladder.py` | R | medium | `implementer_agent` | sonnet | medium | ✅ `2185d74` |
| U30 | `scripts/check_gate_log.py` | R | medium | `implementer_agent` | sonnet | medium | ✅ `4945d43` |
| U31 | `scripts/check_model_tiers.py` | R | low | `implementer_agent` | sonnet | medium | ✅ `a41bac5` |
| U32 | `scripts/check_task_scope.py` | R | medium | `implementer_agent` | sonnet | medium | ✅ `ba0a244` |
| U33 | `scripts/check_template_gates.py` | R | medium | `implementer_agent` | sonnet | medium | ✅ `254d8f0` |
| U34 | `scripts/ci_gate.py` | R | low | `implementer_agent` | sonnet | medium | ✅ `c2bb934` |
| U35 | `scripts/cursor_adapter.py` | R | medium | `implementer_agent` | sonnet | medium | ✅ `c17be99` |
| U36 | `scripts/detect_drift.py` | R | medium | `implementer_agent` | sonnet | medium | ✅ `a2fc516` |
| U37 | `scripts/detect_new_models.py` | R | low | `implementer_agent` | sonnet | medium | ✅ `aa31333` |
| U38 | `scripts/docs_freshness_check.py` | R | medium | `implementer_agent` | sonnet | medium | ✅ `6ff17bf` |
| U39 | `scripts/install.py` | R | high | `implementer_agent` | sonnet | medium | ✅ `f2e4822` |
| U40 | `scripts/merge_json.py` | R | high | `implementer_agent` | sonnet | medium | ✅ `244f70c` |
| U41 | `scripts/model_ledger.py` | R | low | `implementer_agent` | sonnet | medium | ✅ `c08d3ef` |
| U42 | `scripts/quality_audit.py` | R | medium | `implementer_agent` | sonnet | medium | ✅ `1de54b5` |
| U43 | `scripts/session_cost.py` | R | low | `implementer_agent` | sonnet | medium | ✅ `e62f648` |
| U44 | `scripts/session_probe.py` | R | medium | `implementer_agent` | sonnet | medium | ✅ `119b8df` |
| U45 | `scripts/session_start.py` | R | low | `implementer_agent` | sonnet | medium | ✅ `e1c8557` |
| U46 | `scripts/session_state.py` | R | medium | `implementer_agent` | sonnet | medium | ✅ `3c77a4b` |
| U47 | `scripts/sync_agents_pin.py` | R | low | `implementer_agent` | sonnet | medium | ✅ `aa06616` |
| U48 | `scripts/verify_references.py` | R | medium | `implementer_agent` | sonnet | medium | ✅ `aefb4ca` |
| U49 | `skills/compliance-checker/scripts/distill.py` | R | low | `skill_architect` | sonnet | medium | ✅ `23d17a5` |
| U50 | `skills/env-shielding-auditor/scripts/env_shielding_auditor.py` | R | medium | `skill_architect` | sonnet | medium | ✅ `8afb5ea` |
| U51 | `skills/js-standardizer/scripts/js_standardizer.py` | R | low | `skill_architect` | sonnet | medium | ✅ `a3c3b10` |
| U52 | `skills/mass-standardizer/scripts/generate_manifest.py` | R | medium | `skill_architect` | sonnet | medium | ✅ `d3277fe` |
| U53 | `skills/mass-standardizer/scripts/mass_standardizer.py` | R | low | `skill_architect` | sonnet | medium | ✅ `613c376` |
| U54 | `skills/omni-context-minimizer/scripts/omni_minimizer.py` | R | medium | `skill_architect` | sonnet | medium | ✅ `5c84a61` |
| U55 | `skills/skillopt/scripts/dataloader.py` | R | low | `skill_architect` | sonnet | medium | ✅ `b586cf2` |
| U56 | `skills/skillopt/scripts/env.py` | R | medium | `skill_architect` | sonnet | medium | ✅ `147b276` |
| U57 | `skills/skillopt/scripts/gemini_backend.py` | R | low | `skill_architect` | sonnet | medium | ✅ `3931024` |
| U58 | `skills/skillopt/scripts/train_runner.py` | R | medium | `skill_architect` | sonnet | medium | ✅ `4334548` |
| U59 | `skills/topology-monitor/scripts/coverage_auditor.py` | R | low | `skill_architect` | sonnet | medium | obsolete — file deleted `3d65f37` |
| U60 | `skills/topology-monitor/scripts/legacy_app_auditor.py` | R | medium | `skill_architect` | sonnet | medium | ✅ `0add610` |
| U61 | `skills/topology-monitor/scripts/task_auditor.py` | R | low | `skill_architect` | sonnet | medium | obsolete — file deleted `3d65f37` |
| U62 | `tests/test_artifact_registry.py` | R | low | `implementer_agent` | sonnet | medium | ✅ `2fef0de` |
| U63 | `tests/test_ci_gate.py` | R | low | `implementer_agent` | sonnet | medium | ✅ `7dbf116` |
| U64 | `tests/test_session_protocol.py` | R | low | `implementer_agent` | sonnet | medium | ✅ `c3d2aef` |
| K1..Kn | `skills/skill-creator/{scripts,eval-viewer}/*.py` whose provenance `U21` cannot verify (up to 20 units in 11 files, `D2`) | R | medium | `skill_architect` | sonnet | medium | not triggered — `e0922dd` |

`U56` and `U51` refactor `env.py` and `js_standardizer.py` for **complexity only**
(latent `F821`/`E722` findings stay for Sprint 054 — `IMPLEMENTATION_PLAN.md`
"Out of scope").

### Wave 7 — Wiring and records

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U65 | `agents.md` | modify | medium | `rule_validator` | sonnet | medium | ✅ `ac33d04` |
| U66 | `Makefile` | modify | medium | `implementer_agent` | sonnet | medium | ✅ `1449e65` |
| U67 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify | low | `doc_orchestrator` | sonnet | medium | ✅ `8f65dcf` |

`U65` carries an `RA-14` obligation (grep "does NOT run `make quality-audit`"
corpus-wide). `U66` is deliberately **last** in execution order (`D13`: refactors
land before the gate is wired, so `verify` measures the final tree) — see the
sequencing table below.

**Units: 67 planned + up to 11 contingency files (`K*`). Breakdown**:
`implementer_agent` 42 (`U2–U5, U9, U11–U13, U16, U19, U21–U48, U62–U64, U66`),
`doc_orchestrator` 7 (`U1, U6–U8, U10, U14, U67`), `rule_validator` 5
(`U15, U17, U18, U20, U65`), `skill_architect` 13 (`U49–U61`) + `K1..Kn`.
Matches `agent_assignment.md`'s breakdown exactly.

---

## Rule audit — findings against current `rules/` and `agents.md`

| # | Finding | Disposition |
| :--- | :--- | :--- |
| 1 | **Same-file collisions across non-adjacent waves.** Eight files are claimed as a subject (or touched as a mandatory companion) by more than one unit. `jurisdictional_lock` caps *concurrent* claims, not lifetime touches, and permits sequential re-claim once the predecessor has landed (`agents.md §2`, Phase 014 `T21`/`T22` precedent). Every pair below is separated by wave order already declared in the Plan, so no reordering is required — but the order was not previously consolidated in one place, and this file is what `no_interference` is read from. Recorded strictly sequential: `session_start.py` — `U2` → `U5` → `U45`; `session_state.py` — `U3` → `U4` → `U46` (`U46`'s own note: "grows in `U4`; re-measured before the refactor" confirms the direction); `Makefile` — `U13` → `U66` (`D13` states `U66` last explicitly); `agents.md` — `U15` → `U65`; `hooks/on_commit.py` — `U16` → `U23`; `scripts/verify_references.py` — `U19` → `U48`; `scripts/quality_audit.py` — `U22` → `U42`. | **Not a violation — sequential ordering matches the Plan's wave structure and `D13`.** No two units in this list may ever be in-progress at the same time; a runner processing Wave 6 concurrently with Wave 2/3/4/5 units on the same file would violate `no_interference`. |
| 2 | **`U9`/`U62` on `tests/test_artifact_registry.py` — companion vs. subject.** `U9`'s structural subject is `config/artifact_registry.json`; `tests/test_artifact_registry.py` is its mandatory companion (feat( unit, coverage required by `rules/qa_and_testing.md §1`), not a second claimable subject under `jurisdictional_lock`. `U62` later claims that same file as its **own** structural subject (Wave 6 refactor). `jurisdictional_lock`'s text ("a mandatory companion... is not an independently claimable subject and cannot collide with another task") is stated for the `fix(` case (`code_craft.md §6`) and generalizes to any "further file the subject's own rules require" — but it does not say a companion-touched file is thereby exempt from **future** subject-claims by another unit. It is not: `U62` must still land strictly after `U9`, both because `U62` cannot refactor content `U9` has not yet written, and because a companion write and a later subject-claim on the identical file are a real filesystem collision if ever concurrent, regardless of which one is "the subject." Recorded order: `U9` → `U62`. | **Governance clarification recorded, not a violation.** The rule's "cannot collide with another task" clause protects the *companion's own unit* from being miscounted as two subjects; it does not retroactively license concurrency with an unrelated later unit that claims the same file as its subject. Flagging this distinction because it is not spelled out in `agents.md §2` and could be misread as a blanket exemption. |
| 3 | **`code_craft.md §6` fix( pairing.** Every `fix(` unit in this sprint (`U2`, `U3`, `U5`, `U11`) declares a paired test file in the same File cell, satisfying `hooks/on_commit.py audit_regression_test`'s requirement that a `fix(` commit stage at least one test file. `feat(`/`create` units (`U4`, `U9`, `U12`, `U16`, `U19`, `U22`) also declare paired tests although the hook does not gate on those prefixes — required instead by `rules/qa_and_testing.md §1`'s coverage mandate. No unit lacks its required companion. | **Compliant.** No finding. |
| 4 | **`RA-16` invoker for every new mechanism.** Cross-checked against the Plan's `Mechanisms` table: `quality-audit` inside `verify` → `Makefile` `verify` (wired at `U66`, deliberately last per `D13`, but `make quality-audit` already exists as a standalone invoker from Sprint 050 — not an orphan mechanism in the interim); stale-exclusion check → `scripts/quality_audit.py` via `verify`; unmapped-file manifest → `Makefile` `graphify-update`/`graphify-rebuild` (`U13`); task-scope precondition → `hooks/on_commit.py` (git commit hook, self-invoking); registry-writer test → `tests/test_artifact_registry.py` via `verify`; invocation-coverage tree rules → `scripts/verify_references.py` via `verify`; `open-sprint` → `workflows/start_workflow.md` Phase 0.5 / `pipeline_workflow.md` Phase 3; gate final-message register → agent judgment, explicitly typed as having no deterministic alternative (`D12`). Every row names an invoker. | **Compliant.** No finding. |
| 5 | **`RA-14` propagation obligations.** The Plan itself assigns three explicit corpus-wide greps to their owning units: `U6` (`--takeover` across `workflows/`), `U10` (`principal_agent` authorship claims across `pipeline_workflow.md`), `U65` ("does NOT run `make quality-audit`" corpus-wide). These are the unit's own obligation, restated here only as pointers (finding 1/2 table notes) to avoid duplicating text that would itself drift under `RA-14` if this file and the Plan disagreed later. | **Compliant as designed.** No finding; flagged as a pointer, not restated in full. |
| 6 | **Abort criterion 1 interaction with this file.** If Wave 6 residue exceeds 5 files (`IMPLEMENTATION_PLAN.md` "Abort criterion" #1), `U66` is withheld and the residue becomes a `KI-052-*` roadmap row rather than a task-scope unit. This file's Status column will need a targeted amendment at that point (`U66` → withdrawn, not silently left `⏳`); not an issue at Phase 4.3 since no unit has executed. | **Procedural note, not a current violation.** Recorded for Phase 6/Closeout attention. |
| 7 | **Table shape.** `# | File | Operation | Risk | Assignee | Model | Effort | Status` on every Work table (sprint `52 ≥ 28`, `MODEL_FROM_SPRINT`), matching the long form mandated by `agents.md §6 rule_validator` `task_scope` — the short five-column shape is historical-only (pre-28) and not used here. | **Compliant.** No finding. |

No blocking defect was found in `IMPLEMENTATION_PLAN.md` or `agent_assignment.md`
during this audit. Findings 1 and 2 are governance clarifications recorded for
execution-time discipline, not plan defects requiring a plan edit.

---

## Checker trace (`scripts/check_task_scope.py`)

1. `main()` → `--sprint-dir docs/sprints/052-core-pipeline` → `check(path)`.
2. `path = docs/sprints/052-core-pipeline/task_scope.md` — exists (this file). `sprint_id_from_dir` reads `"052-core-pipeline"[:3] = "052"`, digit-checks pass → `sprint_id = 52`.
3. `collect_findings(text, 52, root)`: `work_tables(text)` scans every `|`-prefixed non-separator line; a header row qualifies when it contains all of `File`, `Operation`, `Risk`, `Assignee`. Every Wave table above (1–7, including the Wave 6 contingency row inside the Wave 6 table) has header `# | File | Operation | Risk | Assignee | Model | Effort | Status` — all four keys present, so each of the 7 tables is collected.
4. `requires_model_columns(52, text)`: `sprint_id is not None and 52 >= 28` → `True` immediately (text-content branches never evaluated).
5. For each of the 7 tables: `_capability_findings` — for every row whose `Operation` (lowercased) contains one of `create/modify/delete/move/regenerate/append/transcribe` as a substring (this fires on the literal `modify` and `create` rows: `U1, U6, U7, U8, U10, U13, U14, U15, U17, U18, U20, U21, U65, U66, U67`; it does **not** match `fix(`, `feat(`, or `R` as substrings of those keywords, so those rows are not mutation-checked — not a failure mode, just an unchecked row), `profile_tools(assignee, root)` is read from `agents/<profile>.md` `tools:` frontmatter. All four profiles used (`implementer_agent`, `doc_orchestrator`, `rule_validator`, `skill_architect`) declare `Write` and `Edit` (confirmed in `agent_assignment.md`'s own Tool-sufficiency table and independently by the `tools:` line convention used across `agents/*.md`) → `tools & WRITE_TOOLS` is non-empty for every checked row → **zero capability findings**.
6. `"Model" in header and "Effort" in header` — both present in every table's header → no missing-column finding.
7. `_mechanical_high_findings`: iterates rows checking `profile in MECHANICAL_PROFILES` (`devops_agent`, `git_sync_agent`, `topology_mapper`) — no row in this file assigns any of those three profiles (all rows are `implementer_agent`, `doc_orchestrator`, `rule_validator`, or `skill_architect`) → the `continue` fires on every row → **zero mechanical-high findings**, independent of any row's `Risk` value (including the several `high`-risk rows: `U11`, `U16`, `U19`, `U23`, `U39`, `U40`).
8. `findings` list is empty after all 7 tables → `check()` prints `[OK] check_task_scope: <path>` and returns `0`.

**Conclusion: `python3 scripts/check_task_scope.py --sprint-dir docs/sprints/052-core-pipeline` traces to exit `0`.**
