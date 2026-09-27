# Implementation Plan: Sprint 052 — Session defects, the Python quality gate, and the open upstream register

**Canonical path**: `docs/sprints/052-core-pipeline/IMPLEMENTATION_PLAN.md`
**Branch**: `ai-sprint/052` · **Base**: `main` at `ca70bfa`
**Mode**: nucleus (`.git` is a real directory — `scripts/_mode.py`)
**Status**: `APPROVED`

> Authored at Phase 1 (Planning) by `principal_agent`, extracted to this path at
> Phase 3, and **committed before Phase 5 approves it** (`agents.md §2 triple_lock`).

---

## Context

The human set the objective as *every remaining pending candidate*. Measured at
`ca70bfa` (`v4.34.0`), those are:

| # | Candidate | Measured state | Reproduce |
| :--- | :--- | :--- | :--- |
| 1 | `quality_audit` baseline + `make verify` wiring (`agents.md §1`, `D5` Branch B of Sprint 050) | 87 non-compliant units / 1487 (94.1%) in 53 files; gate exit `2`. 20 units sit in `skills/skill-creator/{scripts,eval-viewer}/`, 67 in 42 first-party files | `python3 scripts/quality_audit.py .; echo $?` and `--report` |
| 2 | `KI-050-6` — JS/TS complexity instrument | Nucleus holds **0** tracked JS/TS files; the instrument serves hosts only | `git ls-files '*.js' '*.ts' '*.tsx' '*.jsx' '*.mjs' '*.cjs' \| wc -l` → `0` |
| 3 | `KI-048-1` — `invoked_by:` coverage for `skills/*/scripts/*.py` and `tests/*.py` | 84 files lack the string (46 `skills/`, 38 `tests/`); `check_invocation_coverage` globs only `workflows/`, `scripts/`, `hooks/` (`scripts/verify_references.py:233-237`) | `for f in $(git ls-files 'skills/*/scripts/*.py' 'tests/*.py'); do grep -q invoked_by "$f" \|\| echo "$f"; done \| wc -l` |
| 4 | 6 open upstream findings (`docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md`) | `REVDOC-G1`, `ADR-0006`, `ADR-0007`, `#13`, `F-051-R1`, `F-051-R3` | `grep -c '^### - \[ \]' docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` → `6` |
| 5 | `ruff` baseline (`§1 linter_command`, recorded for Extract by Sprint 051) | 190 findings at `ruff 0.16.3` (Sprint 051 recorded 56 on another version); **no ruff version is pinned** (`requirements-*.txt`) and no ruff config is tracked, so the figure is not reproducible across machines | `venv_skillopt/bin/ruff check . --statistics \| tail -3` |
| 6 | Session defects found by this session's `/agents:start` | see below | per row |

Session defects (found 2026-09-25, reproduced in this session):

| ID | Defect | Reproduce |
| :--- | :--- | :--- |
| `S052-1` | `session_start.py --boot` passes no `--session-id` to `session_state.py claim` (`scripts/session_start.py:463`), so every boot mints a new UID and a second boot in the **same** session refuses itself (exit `2`). `start_workflow.md:28` says Claude claims with `--session-id <UID>`; the boot never does | run `--boot` twice → second exits `2` |
| `S052-2` | The refusal message says *"re-run with `--takeover`"*; `session_start.py` rejects that flag (`unrecognized arguments`). Only `session_state.py claim` accepts it | `python3 scripts/session_start.py --boot --takeover` → argparse exit `2` |
| `S052-3` | The briefing counts `\| **Still open` **table rows** (`session_start.py:162`), not open entries: it printed `1` against 6 `### - [ ]` entries | `make session-start` vs the `grep -c` above |
| `S052-4` | No instrument writes `current_sprint`; the boot's own advisory asks for it to be opened, and this session had to hand-edit the anchor to record Sprint 051 | `python3 scripts/session_state.py -h` lists no such subcommand |
| `S052-5` | `docs/roadmaps/core/pipeline/021-030-program-queue.md` does not record Sprint 051 (`v4.34.0`) and still calls 050 "deploying" | `grep -c '`051`' docs/roadmaps/core/pipeline/021-030-program-queue.md` |

**Programme decision (human, 2026-09-25).** The roadmap itself sizes `KI-050-6` and
`KI-048-1` as a sprint each, and Sprint 050 aborted precisely on JS/TS. The candidates
are therefore split into a programme. The Approval Gate authorises **one**
`Sprint_ID` (`pipeline_workflow.md` Phase 5), so 053 and 054 each pass their own
Phase 1–5:

| Sprint | Scope |
| :--- | :--- |
| **052 (this plan)** | Candidates 1, 3, 4, 6 |
| 053 | Candidate 2 — JS/TS instrument on `tree-sitter` (human decision) |
| 054 | Candidate 5 — pin ruff, track its config, reach exit `0`, wire into `verify` |

Done when: `make verify` exits `0` **and runs `quality-audit`**; the 6 upstream
entries are `[x]` with a closing SHA each (or re-routed with a destination);
`check_invocation_coverage` covers the two new trees; `S052-1`..`5` are closed with
paired tests where the fix is code.

---

## Design

| ID | Decision | Chosen over | Why |
| :--- | :--- | :--- | :--- |
| `D1` | **Typed exclusion file** `config/quality_audit_exclusions.json` (`path`, `reason`, `provenance`); `quality_audit.py` skips listed paths and **exits `2` on an entry whose path no longer exists** (same shape as `RA-16`'s stale-exception check) | Refactoring vendored code to 0 violations | Human decision. Rewriting upstream code forks it on every future sync. The stale-entry check stops the list becoming a silent allowlist |
| `D2` | `skills/skill-creator/scripts/` and `skills/skill-creator/eval-viewer/` enter the exclusion file **only after provenance is verified** against Anthropic's `skill-creator` (Apache-2.0, `skills/skill-creator/LICENSE.txt`). If it cannot be verified file by file, the unverified files join the refactor wave as contingency units `K1..Kn` | Excluding the whole skill | Commit `1457237` (#16) established that `SKILL.md` is first-party. Excluding by directory would exclude first-party code on an unverified claim |
| `D3` | **`artifact_registry.json` separates `owner` from `writer`** (`F-051-R1`). `principal_agent` stays owner of `IMPLEMENTATION_PLAN.md`, `PHASE_REGISTER.md` and `CHANGELOG.md`; the writer is a profile that holds `Write`. A test asserts that every `writer` declares `Write` in `agents/<writer>.md` `tools:` | Granting `principal_agent` `Write` | Human decision; same reasoning `ADR-0009` used to refuse `devops_agent` `Write` over `scripts/`. A tool grant cannot be path-scoped, a registry field can be tested. Recorded as `ADR-0015` |
| `D4` | `F-051-R3`: `check_role_artifact.py` resolves the sprint directory against the **anchor of the repository the gate audits** (`git rev-parse --show-toplevel` of the audited path, falling back to cwd only when no path is given), never the session cwd alone | Suppressing the hook in nucleus clones | Suppression would hide a real missing row; resolving by anchor is `§3 jurisdiction`'s own definition |
| `D5` | `REVDOC-G1`: new `scripts/graph_reconcile.py` compares `git ls-files` against the `source_file` set of `graphify-out/graph.json`, writes `graphify-out/unmapped_files.json`, prints the count, **exit `0` (advisory)**. Invoked by `Makefile` `graphify-update` and `graphify-rebuild` after the graph write | Patching `graphify` | Third-party cause (Sprint 051 verdict). The risk is the nucleus's (`§2 graph_sovereignty`), so the nucleus owns the reconciliation. Measured today: 730 tracked, 698 mapped, 32 unmapped (7 `.md`, 1 `.py`). Advisory, not blocking: `.txt`/`.svg`/`.yml` are legitimately unmapped |
| `D6` | `ADR-0006`: `agents.md §3 local_testing` restated as *isolate the test database*; in-memory SQLite is the default, and a declared deviation (host ADR naming the fidelity requirement) is the sanctioned path. Recorded as `ADR-0016` | Leaving the rule and letting hosts deviate | Hosts already build the deviation path; the rule should name it rather than be broken silently |
| `D7` | `ADR-0007`: `hooks/on_commit.py` refuses a `#[ID]` commit on `ai-sprint/[ID]` that stages any path **outside** `docs/sprints/[ID]-*/` while `docs/sprints/[ID]-*/task_scope.md` is absent. Sprint-directory-only commits (plan, log, the scope itself) pass | Prose reminder in `pipeline_workflow.md` | Sprint 051 produced `task_scope.md` only at Closeout, inside the repository that owns the rule. A reminder already existed and did not prevent it |
| `D8` | `#13`: close by measurement. Sprint 050 defined executable lines and `ast`-ancestor nesting in `agents.md §1`. The residual question — decorators — is answered by the instrument (units are counted over `FunctionDef.body`; `decorator_list` is outside it). `§1` states it, and a test pins it | Reopening the definition | The definition exists. Only the decorator clause is unstated, and the instrument already answers it |
| `D9` | `KI-048-1`: `check_invocation_coverage` gains the two trees with **typed tree rules**, not blanket exceptions: `tests/test_*.py` and `tests/conftest.py` resolve to invoker `make verify` (pytest collection, by filename pattern); `skills/<s>/scripts/*.py` resolves when named in `skills/<s>/SKILL.md` or `README.md`, or imported by a resolved module. The residue is declared in `config/invocation_exceptions.json` with a typed reason | Per-file `invoked_by:` in 84 files; one blanket exception per tree | Per-file declaration puts boilerplate in ordinary pytest suites. A blanket exception would pass a helper nothing calls, which `RA-16` forbids. A tree rule is a deterministic proof of invocation  **Amended at QA Gate 1 (`F-1`/`F-2`, `ef2b0bc`)**: "named" means a whole-token filename, skill-relative path or dotted module (`scripts.X`); "imported by a resolved module" is a fixpoint seeded only from directly resolved files, with imports resolved to real paths and `tests/` importers excluded; a Makefile recipe or an own `invoked_by:` also resolves (U19) |
| `D10` | `S052-1`/`S052-2`: `session_start.py --boot` accepts `--session-id` and `--takeover` and forwards both to `claim`. The refusal message names the invocation valid for the **entry point that issued it** | Documenting a workaround | The flag the message recommends must exist where the user is told to use it |
| `D11` | `S052-4`: `session_state.py open-sprint --id <N>` writes `current_sprint.{id,status: OPEN}` and keeps `layer`, `app` and `last_audit_sprint`. It refuses (exit `2`) while `status` is `IN_PROGRESS` for another sprint | Hand-editing the anchor | `§5 state_homologation`: the anchor has writers; this field had none  **Amended at QA Gate 1 (`F-3`, `dc38968`)**: the refusal was unreachable, because nothing writes `IN_PROGRESS` to `current_sprint.status`, and the top-level `status` is the session lock that `claim()` resets. `release()` now writes `current_sprint.status = CLOSED_SUCCESSFULLY`, and `open-sprint` refuses a different sprint unless that seal is present |
| `D12` | Gate-agent final-message loss (`F-051-R3` related note): `agents/qa_agent.md` and `agents/tester_agent.md` require the **final message** to carry the full verdict register (Gate, Round, Verdict, Class, findings table) | Leaving it as a note | Six runs across three sprints delivered a one-line final message. A profile rule is the only lever on the agent's output. Whether the hook causes it stays unestablished; this makes the loss detectable |
| `D13` | Order inside the sprint: behaviour changes before refactors; `Makefile` `verify` wiring (`U66`) **last**, so the gate measures the final tree | Refactor first | A refactor done before a feature lands in the same file is measured against code that is about to change |

---

## Work

One unit is one atomic commit with one structural subject. A `fix(` unit carries its
paired test in the same commit. `R` = `refactor(`, behaviour-preserving, the only
acceptance being `quality_audit` compliance of the named functions plus an unchanged
full suite.

### Wave 1 — Records

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| U1 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify — record 050 deployed `v4.33.0`, 051 deployed `v4.34.0`, programme 052–054; `KI-048-1`/`KI-050-6` routed to 052/053; ruff baseline routed to 054 (`S052-5`) | low | `doc_orchestrator` | ⏳ |

### Wave 2 — Session and anchor defects

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| U2 | `scripts/session_start.py` + `tests/test_session_start.py` | `fix(` — `--boot` accepts and forwards `--session-id`, `--takeover` (`S052-1`, `D10`) | medium | `implementer_agent` | ⏳ |
| U3 | `scripts/session_state.py` + `tests/test_session_state.py` | `fix(` — refusal message names the valid invocation per entry point (`S052-2`) | low | `implementer_agent` | ⏳ |
| U4 | `scripts/session_state.py` + `tests/test_session_state.py` | `feat(` — `open-sprint --id` subcommand (`S052-4`, `D11`) | medium | `implementer_agent` | ⏳ |
| U5 | `scripts/session_start.py` + `tests/test_session_start.py` | `fix(` — upstream section counts `### - [ ]` entries (`S052-3`) | low | `implementer_agent` | ⏳ |
| U6 | `workflows/start_workflow.md` | modify — Phase 0.5 names `open-sprint` and boot forwarding; `RA-14` grep for `--takeover` across `workflows/` | low | `doc_orchestrator` | ⏳ |
| U7 | `commands/start.md` | modify — boot step passes `--session-id` where the harness exposes one | low | `doc_orchestrator` | ⏳ |

### Wave 3 — Upstream findings

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| U8 | `docs/decisions/ADR-0015-artifact-owner-writer-separation.md` | create (`F-051-R1`, `D3`) | low | `doc_orchestrator` | ⏳ |
| U9 | `config/artifact_registry.json` + `tests/test_artifact_registry.py` | `feat(` — `writer` field on every artifact; test: each writer's profile declares `Write` | medium | `implementer_agent` | ⏳ |
| U10 | `workflows/pipeline_workflow.md` | modify — Phases 1 and 8 name owner and writer (`RA-14` grep over `principal_agent` authorship claims) | low | `doc_orchestrator` | ⏳ |
| U11 | `scripts/check_role_artifact.py` + `tests/test_check_role_artifact.py` | `fix(` — resolve by audited repository's anchor (`F-051-R3`, `D4`) | high | `implementer_agent` | ⏳ |
| U12 | `scripts/graph_reconcile.py` + `tests/test_graph_reconcile.py` | create — `invoked_by:` `Makefile` graphify targets (`REVDOC-G1`, `D5`) | medium | `implementer_agent` | ⏳ |
| U13 | `Makefile` | modify — `graphify-update`/`graphify-rebuild` run `graph_reconcile.py` | low | `implementer_agent` | ⏳ |
| U14 | `docs/decisions/ADR-0016-test-database-isolation.md` | create (`ADR-0006`, `D6`) | low | `doc_orchestrator` | ⏳ |
| U15 | `agents.md` | modify — `§3 local_testing` restated (`D6`) | medium | `rule_validator` | ⏳ |
| U16 | `hooks/on_commit.py` + `tests/test_on_commit.py` | `feat(` — task-scope precondition on sprint commits (`ADR-0007`, `D7`) | high | `implementer_agent` | ⏳ |
| U17 | `agents/qa_agent.md` | modify — final message carries the full register (`D12`) | low | `rule_validator` | ⏳ |
| U18 | `agents/tester_agent.md` | modify — same (`D12`) | low | `rule_validator` | ⏳ |

### Wave 4 — Invocation coverage (`KI-048-1`)

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| U19 | `scripts/verify_references.py` + `tests/test_verify_references.py` | `feat(` — two new trees with typed tree rules (`D9`); tests prove an uninvoked helper is still flagged | high | `implementer_agent` | ⏳ |
| U20 | `config/invocation_exceptions.json` | modify — typed entries for the residue U19 reports | low | `implementer_agent` | ⏳ |

### Wave 5 — Quality-audit scope

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| U21 | `config/quality_audit_exclusions.json` | create — only provenance-verified vendored paths (`D1`, `D2`); verification evidence per entry | medium | `implementer_agent` | ⏳ |
| U22 | `scripts/quality_audit.py` + `tests/test_quality_audit.py` | `feat(` — read exclusions; exit `2` on stale entry; test pins decorators outside the line count (`D8`) | medium | `implementer_agent` | ⏳ |

### Wave 6 — Refactor to zero (`R`, one file per unit)

Functions named are those `quality_audit.py --report` flags at `ca70bfa`, with (lines, depth).

| # | File | Functions | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| U23 | `hooks/on_commit.py` | `audit_three_file_standard`(31,4) `audit_secret_shielding`(31,4) `main`(40,4) | high | `implementer_agent` | ⏳ |
| U24 | `hooks/on_init.py` | `sync_commands`(24,4) | medium | `implementer_agent` | ⏳ |
| U25 | `hooks/state_mirror.py` | `mirror_active_state`(11,4) | medium | `implementer_agent` | ⏳ |
| U26 | `scripts/audit_cursor_era.py` | `ce4_count`(14,4) | low | `implementer_agent` | ⏳ |
| U27 | `scripts/branch_sovereignty.py` | `merged_pr_exists`(24,4) `classify`(15,4) | medium | `implementer_agent` | ⏳ |
| U28 | `scripts/check_absolute_paths.py` | `main`(16,4) | low | `implementer_agent` | ⏳ |
| U29 | `scripts/check_forge_ladder.py` | `_tables`(19,5) `check_agent_assignment`(20,4) | medium | `implementer_agent` | ⏳ |
| U30 | `scripts/check_gate_log.py` | `gate_tables`(20,6) `collect_findings`(9,4) | medium | `implementer_agent` | ⏳ |
| U31 | `scripts/check_model_tiers.py` | `check_agreement`(22,4) | low | `implementer_agent` | ⏳ |
| U32 | `scripts/check_task_scope.py` | `work_tables`(20,6) `_capability_findings`(18,4) | medium | `implementer_agent` | ⏳ |
| U33 | `scripts/check_template_gates.py` | `check`(22,4) | medium | `implementer_agent` | ⏳ |
| U34 | `scripts/ci_gate.py` | `gh_json`(16,4) | low | `implementer_agent` | ⏳ |
| U35 | `scripts/cursor_adapter.py` | `_write_commands`(14,4) `_write_profile_rules`(38,4) | medium | `implementer_agent` | ⏳ |
| U36 | `scripts/detect_drift.py` | `covering_tags`(8,4) | medium | `implementer_agent` | ⏳ |
| U37 | `scripts/detect_new_models.py` | `tier_status`(13,4) | low | `implementer_agent` | ⏳ |
| U38 | `scripts/docs_freshness_check.py` | `check_c4_override_pointers`(9,5) `check_superseded_chains`(7,4) `run`(31,4) | medium | `implementer_agent` | ⏳ |
| U39 | `scripts/install.py` | `link_one`(19,4) `install_profile_from_dir`(23,4) | high | `implementer_agent` | ⏳ |
| U40 | `scripts/merge_json.py` | `prune_deprecated_hooks`(13,4) `merge`(10,7) | high | `implementer_agent` | ⏳ |
| U41 | `scripts/model_ledger.py` | `gate_round_counts`(18,5) `work_summary`(20,4) | low | `implementer_agent` | ⏳ |
| U42 | `scripts/quality_audit.py` | `scan`(12,5) `_discover_python_units`(19,5) `iter_source_files`(17,4) | medium | `implementer_agent` | ⏳ |
| U43 | `scripts/session_cost.py` | `main`(40,4) | low | `implementer_agent` | ⏳ |
| U44 | `scripts/session_probe.py` | `probe_anchor_hygiene`(31,4) `record`(6,5) `probe_platform`(27,5) | medium | `implementer_agent` | ⏳ |
| U45 | `scripts/session_start.py` | `section_chat_vs_map`(22,4) | low | `implementer_agent` | ⏳ |
| U46 | `scripts/session_state.py` | `main`(57,2) — grows in U4; re-measured before the refactor | medium | `implementer_agent` | ⏳ |
| U47 | `scripts/sync_agents_pin.py` | `parse_version`(10,4) | low | `implementer_agent` | ⏳ |
| U48 | `scripts/verify_references.py` | `scan_files`(6,4) `check_rule_citations`(10,4) `imported_modules`(11,5) `check_file_line_citations`(21,5) | medium | `implementer_agent` | ⏳ |
| U49 | `skills/compliance-checker/scripts/distill.py` | `generate_proposal`(33,4) | low | `skill_architect` | ⏳ |
| U50 | `skills/env-shielding-auditor/scripts/env_shielding_auditor.py` | `scan_files`(15,9) `check_gitignore`(10,4) | medium | `skill_architect` | ⏳ |
| U51 | `skills/js-standardizer/scripts/js_standardizer.py` | `check_jsdoc`(16,7) | low | `skill_architect` | ⏳ |
| U52 | `skills/mass-standardizer/scripts/generate_manifest.py` | `parse_frontmatter`(16,5) | medium | `skill_architect` | ⏳ |
| U53 | `skills/mass-standardizer/scripts/mass_standardizer.py` | `point_at_vendored`(13,4) | low | `skill_architect` | ⏳ |
| U54 | `skills/omni-context-minimizer/scripts/omni_minimizer.py` | `parse_python_ast`(23,6) `parse_heuristic`(37,5) | medium | `skill_architect` | ⏳ |
| U55 | `skills/skillopt/scripts/dataloader.py` | `load_split_items`(13,4) | low | `skill_architect` | ⏳ |
| U56 | `skills/skillopt/scripts/env.py` | `_grade_prediction`(42,4) `rollout`(32,5) `get_task_types`(11,4) | medium | `skill_architect` | ⏳ |
| U57 | `skills/skillopt/scripts/gemini_backend.py` | `_call_gemini`(37,4) | low | `skill_architect` | ⏳ |
| U58 | `skills/skillopt/scripts/train_runner.py` | `custom_load_prompt`(79,3) `main`(24,4) | medium | `skill_architect` | ⏳ |
| U59 | `skills/topology-monitor/scripts/coverage_auditor.py` | `audit_code_coverage`(11,4) `audit_doc_coverage`(24,4) | low | `skill_architect` | ⏳ |
| U60 | `skills/topology-monitor/scripts/legacy_app_auditor.py` | `audit_repo_nodes`(34,4) | medium | `skill_architect` | ⏳ |
| U61 | `skills/topology-monitor/scripts/task_auditor.py` | `audit`(28,4) | low | `skill_architect` | ⏳ |
| U62 | `tests/test_artifact_registry.py` | `test_a_path_ends_with_the_filename_it_declares`(5,4) | low | `implementer_agent` | ⏳ |
| U63 | `tests/test_ci_gate.py` | `_call`(12,4) | low | `implementer_agent` | ⏳ |
| U64 | `tests/test_session_protocol.py` | `run`(6,4) | low | `implementer_agent` | ⏳ |
| K1..Kn | `skills/skill-creator/{scripts,eval-viewer}/*.py` whose provenance U21 cannot verify | `R` — up to 20 units in 11 files (`D2`); rows added to `task_scope.md` only if triggered | medium | `skill_architect` | contingency |

### Wave 7 — Wiring and records

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| U65 | `agents.md` | modify — `§1 max_indentation`/`max_lines_per_func`: `verify` now runs `quality-audit`, exclusion file named, decorator clause (`#13`, `D8`); `RA-14` grep over "does NOT run `make quality-audit`" corpus-wide | medium | `rule_validator` | ⏳ |
| U66 | `Makefile` | modify — `verify` runs `quality-audit` (`D13`: last code unit) | medium | `implementer_agent` | ⏳ |
| U67 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify — six entries `[x]` with closing SHA; status table row for 052 | low | `doc_orchestrator` | ⏳ |

**Units: 67 planned + up to 11 contingency files (`K*`).**

---

## Dependencies

| Package | Version | Why the standard library and the existing dependencies do not suffice |
| :--- | :--- | :--- |
| None | — | `tree-sitter` is Sprint 053's dependency, not this sprint's. `graph_reconcile.py` reads JSON and `git ls-files` with the stdlib |

---

## Mechanisms

| Mechanism | Deterministic or agent judgment | Invoker (`RA-16`) |
| :--- | :--- | :--- |
| `quality-audit` inside `verify` (per commit/PR) | `make` target | `Makefile` `verify` |
| Quality-audit stale-exclusion check | script (exit `2`) | `scripts/quality_audit.py`, via `verify` |
| Unmapped-file manifest | script (advisory, exit `0`) | `Makefile` `graphify-update` / `graphify-rebuild` |
| Task-scope precondition on sprint commits | hook (exit `2`, `RA-11`) | `hooks/on_commit.py` |
| Registry writer holds `Write` | test | `tests/test_artifact_registry.py`, via `verify` |
| Invocation coverage over `tests/`, `skills/*/scripts/` | script (exit `2`) | `scripts/verify_references.py` check (d), via `verify` |
| `open-sprint` anchor writer | script | `workflows/start_workflow.md` Phase 0.5 / `pipeline_workflow.md` Phase 3 |
| Gate final-message register | agent judgment — no deterministic alternative exists for the content of an agent's own reply; `check_role_artifact.py` remains the deterministic check on the transcribed row | `agents/qa_agent.md`, `agents/tester_agent.md` |

---

## Cost

| Field | Value | Reproduce |
| :--- | :--- | :--- |
| Delegation | `native` | `docs/active_state.json` `delegation_mode` |
| Work units | 67 (+ up to 11 contingency) | Count of rows in Work tables |
| Subagents dispatched | ~70: one `implementer_agent`/`skill_architect`/`doc_orchestrator`/`rule_validator` per unit, 2 fresh gates per round (`always-fresh-gate-agents`) | Work table Assignee column |
| Prior session ratio | **5.8×** in this planning cycle (first turn 22,863, peak 133,029) — **soft threshold breached** | `python3 scripts/session_cost.py --from-anchor --json` |

Soft breach declared: 67 units remain, all to be executed. **Execution starts in a
fresh session** after Phase 5 (break-even ~22K, `rules/token_economy.md §3.1`). The
hard threshold (15×) suspends the session with `session_state.py suspend`. It does
not abort the sprint. Wave 6 is 42 independent units and is the natural suspension
boundary.

---

## Tests

| Check | Fails against the current tree? |
| :--- | :--- |
| Second `--boot` with the same `--session-id` exits `0` | **Yes** — `S052-1` (flag does not exist) |
| `session_start.py --boot --takeover` parses | **Yes** — `S052-2` |
| Briefing reports `6` open upstream entries on the current file | **Yes** — `S052-3` (prints `1`) |
| `session_state.py open-sprint --id 52` writes `current_sprint` | **Yes** — `S052-4` |
| Every registry `writer` declares `Write` in its profile | **Yes** — `F-051-R1` (field absent; `principal_agent` holds no `Write`) |
| Role-artifact check invoked from a host cwd against a nucleus sprint dir reads the nucleus log | **Yes** — `F-051-R3` |
| `graph_reconcile.py` reports ≥ 1 unmapped tracked file on a fixture graph missing one | **Yes** — script absent (`REVDOC-G1`) |
| Sprint commit touching `scripts/` before `task_scope.md` exists is refused | **Yes** — `ADR-0007` |
| An uninvoked `skills/x/scripts/helper.py` is flagged by check (d) | **Yes** — tree not scanned (`KI-048-1`) |
| A `tests/test_*.py` file needs no `invoked_by:` | **No** — regression to protect under the new tree rule |
| A stale exclusion entry exits `2` | **Yes** — exclusions absent |
| A decorated function's line count excludes the decorator lines | **No** — regression to protect (`#13`) |
| Full suite count ≥ 813 and all pass after every `R` unit | **No** — regression to protect |

---

## Verification

| Command | Expected |
| :--- | :--- |
| `make verify; echo $?` | `0`, and its output contains the `quality-audit` step |
| `python3 scripts/quality_audit.py .; echo $?` | `0` |
| `python3 scripts/graph_reconcile.py; echo $?` | `0`, prints the unmapped count |
| `grep -c '^### - \[ \]' docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | `0` |
| `make session-start` | `Still open` line equals the command above |
| `python3 scripts/verify_references.py; echo $?` | `0` with `tests/` and `skills/*/scripts/` in check (d) |
| `python3 skills/token-saver-auditor/scripts/audit_plan.py docs/sprints/052-core-pipeline/IMPLEMENTATION_PLAN.md; echo $?` | `0` |
| `git -C . status --porcelain` at close | empty |

---

## Documentary impact (T5)

| Artefacto | Qué cambia |
| :--- | :--- |
| `agents.md` | `§1` complexity rows (verify wiring, exclusions, decorators); `§3 local_testing` |
| `docs/decisions/ADR-0015-*.md`, `ADR-0016-*.md` | New |
| `config/artifact_registry.json` | `writer` field |
| `config/quality_audit_exclusions.json` | New |
| `config/invocation_exceptions.json` | Residue entries |
| `workflows/start_workflow.md`, `workflows/pipeline_workflow.md`, `commands/start.md` | Boot forwarding, `open-sprint`, owner/writer |
| `agents/qa_agent.md`, `agents/tester_agent.md` | Final-message contract |
| `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | Six entries closed |
| `docs/roadmaps/core/pipeline/021-030-program-queue.md` | 050/051 deployed; programme 052–054 |
| `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` | Regenerated by `scripts/map_workflows.py` if workflow steps change |
| `CHANGELOG.md` | `[Unreleased]` entry at Closeout, citing SHAs |

---

## Out of scope

| Exclusion | Why, and where it goes instead |
| :--- | :--- |
| JS/TS complexity instrument (`KI-050-6`) | Sprint 053, on `tree-sitter` (human decision 2026-09-25); acceptance corpus = the five failure families of Sprint 050 |
| `ruff` pin, tracked config, 190-finding baseline, `verify` wiring — including the two latent bugs `F821` (`skills/skillopt/scripts/env.py`) and `E722` (`skills/js-standardizer/scripts/js_standardizer.py`) | Sprint 054. U56 and U51 refactor those files for **complexity only**; a refactor that touches the `F821`/`E722` lines keeps their behaviour and names them in the commit body |
| Syncing `skill-creator` vendored files with upstream | Not a defect; the exclusion file records provenance for a future sync |
| Fixing `graphify`'s drop behaviour | Third-party; `D5` makes it observable |

---

## Abort criterion

Decided before execution:

1. **Refactor residue.** If after Wave 6 more than **5** first-party files cannot
   reach compliance without a behaviour change (a test that must change to pass),
   U66 (`verify` wiring) is **withheld**, the residue is recorded as a `KI-052-*`
   row in the program queue, and the rest of the sprint ships. A partial gate is not
   wired.
2. **Invocation coverage.** If U19's tree rules would mark as covered a file that
   nothing invokes (the fixture test fails and cannot be fixed within one remediation
   round), U19–U20 are reverted and `KI-048-1` returns to the queue with the measured
   residue.
3. **Hook precondition.** If U16 refuses any commit that Phases 3–4 legitimately
   need before `task_scope.md` exists, U16 is reverted. The prose rule does not
   replace it.
4. **Gate cap.** Three consecutive `REJECTED` on one logic block →
   `workflows/remediation_workflow.md` (`RA-17`; `RECORD` does not count).

---

## Approval — `triple_lock` lock 1

| Field | Value |
| :--- | :--- |
| **Approved by** | GstMirabal (chat: "aprobado, continua") |
| **Date** | 2026-09-25 |
| **Plan commit at approval** | `979af67` (Phase 4 records `06d6b36`) |
| **Remaining locks** | Active Sprint · QA + Tester verdicts · Human OK at close |

*Phase 5 is a single attended human authorization. It MUST NOT be wrapped inside an
unattended `/loop` (`workflows/pipeline_workflow.md`, `rules/loop_governance.md`).
Any `/loop` this sprint does run — Phases 6-8 only — is governed by
`scripts/loop_guard.py start`, which fails closed.*
