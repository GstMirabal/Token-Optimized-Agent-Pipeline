# Task Scope — Sprint 047 (nucleus-audit-design-remediation)

Phase 4.3 of `workflows/pipeline_workflow.md`. Rule audit of the Roadmap against
current `rules/`. `jurisdictional_lock` and `no_interference` are both applied by
reading this file; `scripts/loop_guard.py` measures progress from it; and
`workflows/close_workflow.md` Phase 2.6 demands it as phase evidence.

Mode: **claude-code** (nucleus), `delegation_mode: native`, `session_tool: claude-code`
(NOT cursor). Model/Effort from `config/model_tiers.json` `tiers.author.claude_code`
(`sonnet` / `medium`) for every unit — both assignees (`rule_validator`,
`implementer_agent`) are listed under `tiers.author.profiles`, neither is in
`tiers.gate.profiles`, and no unit is mechanical-tier work. Every unit is a
prose amendment or a stdlib-only script/test edit (no new logic class, no new
dependency). No `tier_escalation`; no `Declared escalations`. This role
transcribes the `token_economy_agent` verdict — the verdict here is the flat
author tier for all 23 rows.

Check: `python3 scripts/check_task_scope.py --sprint-dir docs/sprints/047-core-pipeline`

---

## Work

One row per unit U1–U23. `File` is the single physical file that is the unit's
structural subject (`agents.md §2 jurisdictional_lock`). U12 additionally carries
the regenerated `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` in the same atomic
commit — that file is generator output (`scripts/map_workflows.py`), never
hand-edited, and is not a second structural subject.

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U1 | `agents.md` | modify | high | `rule_validator` | sonnet | medium | ✅ 8ccf8cb |
| U2 | `rules/django_backend_standard.md` | modify | medium | `rule_validator` | sonnet | medium | ✅ 06c076a |
| U3 | `rules/LEGACY_RULE_CONCORDANCE.md` | modify | low | `rule_validator` | sonnet | medium | ✅ 8ffcbd0 |
| U4 | `workflows/audit_workflow.md` | modify | medium | `rule_validator` | sonnet | medium | ✅ feee5a4 |
| U5 | `rules/skills_and_integrations.md` | modify | medium | `rule_validator` | sonnet | medium | ✅ 2524940 |
| U6 | `workflows/close_workflow.md` | modify | medium | `rule_validator` | sonnet | medium | ✅ 87211f1 |
| U7 | `workflows/skill_forge_workflow.md` | modify | low | `rule_validator` | sonnet | medium | ✅ 963b309 |
| U8 | `workflows/reverse_documentation_workflow.md` | modify | low | `rule_validator` | sonnet | medium | ✅ 77e64a7 |
| U9 | `workflows/repository_hardening_workflow.md` | modify | medium | `rule_validator` | sonnet | medium | ✅ 90c0268 |
| U10 | `workflows/standardization_workflow.md` | modify | medium | `rule_validator` | sonnet | medium | ✅ 35e625b |
| U11 | `scripts/verify_references.py` | modify | high | `implementer_agent` | sonnet | medium | ✅ 6125c5f |
| U12 | `scripts/map_workflows.py` | modify | high | `implementer_agent` | sonnet | medium | ✅ fcdbf28 |
| U13 | `scripts/check_gate_log.py` | modify | medium | `implementer_agent` | sonnet | medium | ✅ 3441ac2 |
| U14 | `scripts/session_start.py` | modify | high | `implementer_agent` | sonnet | medium | ✅ 3e9a892 |
| U15 | `scripts/detect_drift.py` | modify | high | `implementer_agent` | sonnet | medium | ✅ d930e4a |
| U16 | `scripts/_mode.py` | modify | high | `implementer_agent` | sonnet | medium | ✅ 61e877c |
| U17 | `scripts/submodule_purity.py` | modify | high | `implementer_agent` | sonnet | medium | ✅ 55014c8 |
| U18 | `tests/test_verify_references.py` | modify/create | medium | `implementer_agent` | sonnet | medium | ✅ 6125c5f |
| U19 | `tests/test_map_workflows.py` | modify/create | medium | `implementer_agent` | sonnet | medium | ✅ fcdbf28 |
| U20 | `tests/test_check_gate_log.py` | modify/create | medium | `implementer_agent` | sonnet | medium | ✅ 3441ac2 |
| U21 | `tests/test_mode.py` | modify/create | medium | `implementer_agent` | sonnet | medium | ✅ 61e877c |
| U22 | `tests/test_session_start.py` | modify/create | medium | `implementer_agent` | sonnet | medium | ✅ 3e9a892 |
| U23 | `tests/test_submodule_purity.py` | modify/create | medium | `implementer_agent` | sonnet | medium | ✅ 55014c8 |
| U24 | `config/invocation_exceptions.json` | modify | low | `rule_validator` | sonnet | medium | ✅ e0b7753 |
| U25 | `workflows/pipeline_workflow.md` | modify | low | `rule_validator` | sonnet | medium | ✅ f3d11cd |
| U26 | `rules/token_economy.md` | modify | low | `rule_validator` | sonnet | medium | ✅ eafc6c3 |
| U27 | `workflows/standardization_workflow.md` | modify | low | `rule_validator` | sonnet | medium | ✅ 5157086 |
| U28 | `scripts/session_start.py` | modify | high | `implementer_agent` | sonnet | medium | ✅ 17db62c |
| U29 | `tests/test_session_start.py` | modify | medium | `implementer_agent` | sonnet | medium | ✅ 17db62c |

> **U24 — discovered during U1 execution.** U1's `agents.md §1` rewrite dropped
> the `python-doctor` / `react-doctor` names; the RA-14 sprint-artifact-set
> clause U1 itself added then requires the two stale `note` fields in
> `config/invocation_exceptions.json` (`:55`, `:60`) to be reconciled in the same
> sprint. One-file JSON note edit; keys and schema unchanged (`verify_references.py`
> check (d) reads only `path` / `reason`). Same wave/tier as U1–U10.

> **U25/U26 — discovered during U11 execution.** U11 taught `verify_references.py`
> check (d) to resolve `#anchor` fragments in `invoked_by:` and immediately caught
> two pre-existing broken anchors (`S045-13`'s exact defect class): `loop_guard.py`
> → `pipeline_workflow.md#loop_guard` and `session_cost.py` →
> `rules/token_economy.md#session_bound`. Fixed by adding the missing `<a id=…>`
> anchors rather than by touching the two scripts (different files; jurisdictional_lock).
>
> **U27 — discovered during U12 execution.** `standardization_workflow.md` carries
> a *second* non-step reference table (the Scenario Matrix) that U10's single
> skip-marker did not cover; U12's regenerated guide still misparsed its 3 rows.
> A second `<!-- map_workflows:skip-table -->` line closes the S045-27 finding
> completely.
>
> **U28/U29 — discovered during U15 execution.** The roadmap's D8 claim that
> `detect_drift.py` "checks the framework's git history rather than the host's"
> was traced to the actual call sites: `detect_drift.py` itself is correctly
> cwd-scoped (U15, docstring-only), but `session_start.py`'s `section_drift()`
> and `run_boot()` invoked it with `cwd = repo_root()` (the `.agents` checkout)
> unconditionally. The plan's Work table put this fix at U15's file; execution
> found it belongs in `session_start.py` instead — a second, later unit on a file
> U14 already closed (no `no_interference` conflict; U14 was committed).

**Waves (inside the one sprint; `IMPLEMENTATION_PLAN.md` "Commit groups"):**
Wave 1 = U1–U10 governance prose, gate `make verify`; dispatched one atomic
commit each (`RA-08`). Wave 2 = U11–U17 framework-root `scripts/` behaviour.
Wave 3 = U18–U23 pytest suites. Groups are sequential. Every unit is a distinct
physical file, so units inside a wave carry no `no_interference` overlap and may
be dispatched in parallel within the wave (Wave 1 excepted where an `RA-14`
propagation order applies — see below).

---

## Rule audit

### Rules consulted

| Rule file | Bearing on this sprint |
| :--- | :--- |
| `rules/code_craft.md` | U11–U23 touch Python. Changes are branch logic added to existing functions, docstring updates, and new `pytest` cases — type hints on all args/returns, ≤50-line functions, ≤3 indentation levels still apply and must be held by the author; no `TODO`/`FIXME`; English only in code/logs. |
| `rules/token_economy.md` | Plan `## Cost` present; `audit_plan.py` expected exit 0 (`## Verification`). Prior-session ratio 4.8× (`scripts/session_cost.py --from-anchor --json` → `cycles[0].ratio`), under the 5× soft threshold. Model/Effort here transcribe the flat author-tier verdict; no escalation. This is a 23-unit sprint — if the 15× hard threshold fires before U23, `session_state.py suspend` and resume in a fresh session. |
| `rules/documentation_standard.md` | U1–U10 edit `agents.md` / `rules/*.md` / `workflows/*.md`; U12 regenerates `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md`. Regeneration is by `scripts/map_workflows.py` only — never hand-edited; `make verify` gates its staleness. `docs_freshness` handled at close. |
| `rules/skills_and_integrations.md` | U5 adds the canonical SkillOpt `train_runner.py` invocation block to §3 (its natural home per plan D4). U4/U6/U7 reference that block instead of restating it (`RA-14` spirit). No skill forged or vendored `SKILL.md` edited. `RA-16` invoker coverage: no new mechanism — every change hardens a mechanism that already has a declared invoker (plan `## Mechanisms`). |
| `rules/qa_and_testing.md` | `F-026-A1` / plan D10: `tester_agent` executes the suite, does not author test files — U18–U23 are `implementer_agent`. §4 verdict vocabulary (`RA-17`) governs the Phase 7 gate rows. |
| `rules/loop_governance.md` | No `/loop` planned for Execution. Any `/loop` for Phases 6–8 is governed by `scripts/loop_guard.py start` (named in the plan footer alongside `/loop`, satisfying `audit_plan.py` Filter 6). |
| `rules/project_topology.md` | U11–U17 run under the framework root; tests run via `venv_skillopt/bin/python -m pytest`. `graphify update .` via `venv_skillopt/bin/python -m graphify` (never the bare console-script) at the quality/commit phase. |
| `rules/LEGACY_RULE_CONCORDANCE.md` | U3 edits this file (new `Clause J-02` → `rules/django_backend_standard.md §2`, the RA-02 anchor). U1 turns the `RA-02` row into a pointer — the concordance row U3 adds is what keeps legacy `Rule NN` / `Clause` citations resolvable; `verify_references.py` fails on an unmapped citation. U1 must also keep the `RA-04` tombstone and `RA-10` pointer rows resolvable (no renumber of `RA-01`..`RA-18`). |

### `jurisdictional_lock` (one physical file per subtask)

Every unit U1–U23 names exactly one physical file as its structural subject. The
23 targets are pairwise distinct — verified against the plan's Work table and
`agent_assignment.md`:

- `agents.md` appears in **U1 only**.
- `workflows/close_workflow.md` appears in **U6 only**.
- No file is listed by two units. No duplicate found.

U12 also stages the regenerated `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md`. This
does not breach `jurisdictional_lock`: it is deterministic generator output
committed atomically with its generator (`scripts/map_workflows.py`), the same
pattern `close_workflow.md` and `make verify` already assume, not a second
hand-authored file.

### `no_interference` (no target claimed by another active subtask)

`docs/active_state.json` shows exactly one sprint IN_PROGRESS (`current_sprint.id`
= 47). Sprints 021–046 are closed and deployed (HEAD `3dd8537`, Sprint 046 sealed
`v4.29.0`); their `task_scope.md` rows are all terminal. No target file of
U1–U23 is listed by an in-progress subtask in any other `task_scope.md`.

Within Sprint 047: because all 23 targets are disjoint, no file listed by an
in-progress unit is ever the target of another unit. Wave 1 units share no file
with each other; the only ordering constraint is `RA-14` propagation — U2/U3 land
the operative text and concordance row that U1's `RA-02`-row-to-pointer edit
depends on, and U4/U6/U7 reference the block U5 creates — so U1 is committed
after U2/U3 and U4/U6/U7 after U5, but this is a commit-order constraint, not a
shared-file lock.

### Missing rules

None. No new `rules/` file is required. This sprint applies the design-pass
bucket of the Sprint 045 audit (`S045-02, 06, 09, 14, 17, 18, 19, 20, 22, 27`),
`KI-045-2`, `KI-046-3`, and the Sprint 043/044 anchor-read findings against
**existing** rules, workflows and scripts. `rules/skills_and_integrations.md §3`
(U5) gains a canonical invocation block but the file already exists.

---

## Findings for Phase 1 touch-up

Non-blocking. Recorded here per the Phase 4.3 brief; route to `principal_agent`
for a Phase 1 touch-up or carry as Gate-1 notes.

| # | Finding | Location | Suggested resolution |
| :--- | :--- | :--- | :--- |
| F-047-TS1 | `agent_assignment.md` writes assignees as `rule-validator` / `implementer-agent` (hyphen — the `name:` frontmatter value). `scripts/check_task_scope.py` `profile_tools()` resolves the Assignee cell against `agents/<cell>.md` **by filename**, which is underscore (`agents/rule_validator.md`, `agents/implementer_agent.md`). This `task_scope.md` therefore uses the underscore form for all 23 rows, matching every prior passing `task_scope.md` (e.g. Sprint 046) and the `config/model_tiers.json` `profiles` keys. No defect in the assignment itself — the two spellings denote the same profile — but the divergence is a latent trap. | `docs/sprints/047-core-pipeline/agent_assignment.md` Staffing tables; `scripts/check_task_scope.py:147` | Standardise on the underscore profile id in `agent_assignment.md` Assignee cells, or add a hyphen→underscore normalisation in `profile_tools()`. |
| F-047-TS2 | Plan `## Cost` row "Prior session ratio" reads `4.8× (current session at draft time; no distinct prior-session figure in anchor)`. `docs/active_state.json` has no `resume_pointer` cost fields and `session_count` is 40 — consistent with the note, but the figure is a draft-time snapshot and Phase 6+ must refresh it against the real Claude transcript before the soft/hard thresholds are treated as observational-only (plan says as much). | `IMPLEMENTATION_PLAN.md` `## Cost` | Re-run `scripts/session_cost.py --from-anchor --json` at first Execution turn; update the row if `cycles[0].ratio` differs. |
| F-047-TS3 | Plan D7 / U12 and `agent_assignment.md` Wave 2 both state U12's commit "includes the regenerated `WORKFLOWS_STEP_MAP_GUIDE.md`". This is one physical hand-edited file (`scripts/map_workflows.py`) plus one generated file in the same commit. `jurisdictional_lock` is satisfied (generator output is not a structural subject), but the executor MUST regenerate via `scripts/map_workflows.py`, never hand-edit the guide, and `make verify` staleness gate must be green post-commit. Flagged so Gate 1 does not read the two-file commit as a lock breach. | `IMPLEMENTATION_PLAN.md` D7; `agent_assignment.md` Wave 2 | No change needed; note for QA Gate 1. |
| F-047-TS4 | Checked the drift example from the Phase 4.3 brief (`agents.md` ">200 lines"). No such claim exists in `IMPLEMENTATION_PLAN.md` D10. `skill_assignment.md:38` and `:85` already state `agents.md` is **176 lines** and correctly place it **below** the `>200`-line `ast_skeleton` threshold (`agents.md §2`). Verified: `agents.md` ends at line 176. No drift to correct — the artifact set is internally consistent on this point. | `docs/sprints/047-core-pipeline/skill_assignment.md`; `agents.md` | None. Recorded to close the brief's item. |
| F-047-TS5 | U15 (`scripts/detect_drift.py`) is defined as "verify `main()` root resolution matches the docstring claim; repair only if it does not" (plan D8, `## Tests` row: "**No** if the docstring is accurate"). If verification shows the code already correct, U15 becomes a regression-guard-only unit with no production diff — its `task_scope.md` Status will still close, but Gate 1 should expect a test-only change for U15, not a behavioural one. | `IMPLEMENTATION_PLAN.md` D8 / `## Tests`; U15 | No change needed; note for QA Gate 1 acceptance criteria. |
| F-047-TS6 | U16 (`scripts/_mode.py`) carries an explicit abort criterion: if a worktree pointer cannot be distinguished from a submodule pointer without a git call that fails under the sandbox, the unit routes to a hotfix with a git-version matrix. Phase 6 executor must treat that as a live branch, not dead prose. | `IMPLEMENTATION_PLAN.md` `## Abort criterion` | No change needed; carry into Execution checklist. |

---

## Verdict

`task_scope.md` shape: `# | File | Operation | Risk | Assignee | Model | Effort |
Status` — 23 rows, one per U1–U23. `jurisdictional_lock` and `no_interference`
both hold. No missing `rules/` file. Six non-blocking findings routed to Phase 1
/ QA Gate 1. Ready for `scripts/check_task_scope.py` (expected exit 0).
