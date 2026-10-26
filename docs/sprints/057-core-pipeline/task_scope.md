# Task Scope — Sprint 057 (core-pipeline)

Source: `docs/sprints/057-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`, `## Design`, `## Abort criterion`).
Staffing authority: `agent_assignment.md` (overwrites the plan's proposed assignee on W01). Tools: `skill_assignment.md`.
Phase 4.3 of `workflows/pipeline_workflow.md`. Enforced by `scripts/check_task_scope.py`.
Mode: `claude-code`, `delegation_mode: native`. No template for this artifact exists under `docs/standards/templates/`; the shape comes from `scripts/check_task_scope.py` (`WORK_KEYS`, `MODEL_FROM_SPRINT = 28`).

## Tier transcription

Model and Effort are transcribed from each assignee's `agents/<role>.md` frontmatter (`model:`, `tier:`) and the `claude_code` column of `config/model_tiers.json`. No tier is invented and no dated model ID is written.

| Assignee | `model:` | `tier:` | Effort (`claude_code` column) |
| :--- | :--- | :--- | :--- |
| `doc_orchestrator` | sonnet | author | medium |
| `rule_validator` | sonnet | author | medium |
| `implementer_agent` | sonnet | author | medium |
| `skill_architect` | sonnet | author | medium |
| `governance_learner` | sonnet | author | medium |
| `devops_agent` (runs W01 sessions; owns no row) | haiku | mechanical | low |

Declared escalations: none. No `devops_agent` row exists, so the mechanical-at-high-risk check does not apply.

## Work

Status values: ⏳ pending. Risk `high` touches a gate, the sandbox template or `agents.md`.

### Wave A — criteria and scale

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| W00 | `docs/guides/PROMPT_CRITERIA_GUIDE.md` | create | low | `doc_orchestrator` | sonnet | medium | ✅ `4869bc6` |
| W07 | `rules/qa_and_testing.md` | modify (§4 scale S0-S3 and 5 convergence rules) | medium | `rule_validator` | sonnet | medium | ✅ `b063af1` |
| W08 | `docs/standards/templates/SPRINT_LOG_TEMPLATE.md` | modify (Severity column, escape mark) | low | `doc_orchestrator` | sonnet | medium | ✅ `7d91479` |
| W09 | `scripts/check_gate_log.py` | modify (count escape rows; paired test `tests/test_check_gate_log.py`) | low | `implementer_agent` | sonnet | medium | ✅ `e973077` |

### Wave B — S0 lane (W01 blocks W02-W06)

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| W01 | `docs/sprints/057-core-pipeline/SANDBOX_DB_MEASUREMENT.md` | create (M1-M3 literal output; `devops_agent` runs the at most 6 `claude -p` calls and hands the output over unaltered) | high | `doc_orchestrator` | sonnet | medium | ✅ `7eb188b` |
| W02 | `claude/settings.hooks.json` | modify (allowRead and denyWrite of `./.env.agent`; test `tests/test_template_sandbox.py`) | high | `implementer_agent` | sonnet | medium | ⛔ abort criterion 1 (M1 denied) → KI-057-1 |
| W03 | `scripts/env_agent_check.py` | create (test `tests/test_env_agent_check.py`) | high | `implementer_agent` | sonnet | medium | ⛔ abort criterion 1 → KI-057-1 |
| W04 | `scripts/db_probe.py` | create (test `tests/test_db_probe.py`) | medium | `implementer_agent` | sonnet | medium | ⛔ abort criterion 1 → KI-057-1 |
| W05 | `rules/project_topology.md` | modify (database section) | medium | `rule_validator` | sonnet | medium | ⛔ abort criterion 1 → KI-057-1 |
| W06 | `agents.md` | modify (RA-09 one sentence) | high | `rule_validator` | sonnet | medium | ⛔ abort criterion 1 → KI-057-1 |

### Wave C — block 1 defects

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| W10 | `scripts/session_state.py` | modify (fix: `require-released --hotfix`; test `tests/test_session_state.py`) | high | `implementer_agent` | sonnet | medium | ✅ `8352421` |
| W11 | `workflows/deployment_workflow.md` | modify (Phase 0 hotfix route; C-5 squash body) | high | `doc_orchestrator` | sonnet | medium | ✅ `d0f332d` |
| W12 | `scripts/session_state.py` | modify (fix: B-9 `suspend()`; test `tests/test_session_state.py`) | high | `implementer_agent` | sonnet | medium | ✅ `71a35c3` |
| W13 | `scripts/session_end_hook.py` | modify (fix: E session_id; test `tests/test_session_end_hook.py`) | medium | `implementer_agent` | sonnet | medium | ⛔ not reproducible as specified → KI-057-2 |
| W14 | `scripts/py_compile_tree.py` | modify (fix: C-3 cfile; test `tests/test_verify_py_compile.py`) | medium | `implementer_agent` | sonnet | medium | ✅ `04b8fff` |
| W15 | `scripts/_repro_grammar.py` | create (test `tests/test_repro_grammar.py`) | medium | `implementer_agent` | sonnet | medium | ✅ `20d2013` |
| W16 | `hooks/on_commit.py` | modify (fix: A-4, B-2, B-6; test `tests/test_on_commit.py`) | high | `implementer_agent` | sonnet | medium | ✅ `4785b1d` |
| W17 | `scripts/check_fix_reproduces.py` | modify (fix: A-4, KI-056-2; test `tests/test_check_fix_reproduces.py`) | medium | `implementer_agent` | sonnet | medium | ✅ `70faa66` |
| W18 | `scripts/check_fix_reproduces.py` | modify (reproduce-first B-4, B-5; test `tests/test_check_fix_reproduces.py`) | medium | `implementer_agent` | sonnet | medium | ✅ `a19ab8f` (B-4; B-5 not reproduced, M3) |
| W19 | `scripts/check_task_scope.py` | modify (fix: B-3; test `tests/test_check_task_scope.py`) | low | `implementer_agent` | sonnet | medium | ✅ `a4db5df` |
| W20 | `scripts/model_ledger.py` | modify (fix: B-8; test `tests/test_model_ledger.py`) | medium | `implementer_agent` | sonnet | medium | ✅ `7705611` |
| W21 | `scripts/detect_drift.py` | modify (reproduce-first C-1; test `tests/test_detect_drift.py`) | medium | `implementer_agent` | sonnet | medium | ✅ `5a7ed6c` |
| W22 | `workflows/reconciliation_workflow.md` | modify (reproduce-first C-2) | low | `doc_orchestrator` | sonnet | medium | ✅ `9246d60` |
| W23 | `scripts/session_start.py` | modify (fix: C-4 and KI-056-4; test `tests/test_session_start.py`) | medium | `implementer_agent` | sonnet | medium | ✅ `2ee3ded` |
| W24 | `scripts/check_role_artifact.py` | modify (reproduce-first B-7; test `tests/test_check_role_artifact.py`) | medium | `implementer_agent` | sonnet | medium | ✅ `4da3e2a` |
| W25 | `scripts/session_state.py` | modify (reproduce-first C-9; branch B edits other files, see Audit 5) | low | `implementer_agent` | sonnet | medium | ⛔ RECORD: C-9 not reproduced in the nucleus (no reader, no prescription of the three fields) |
| W26 | `scripts/extract_plan.py` | create (test `tests/test_extract_plan.py`) | medium | `implementer_agent` | sonnet | medium | ✅ `7c6c2be` |
| W27 | `workflows/pipeline_workflow.md` | modify (Phase 3 invokes `extract_plan.py`) | low | `doc_orchestrator` | sonnet | medium | ✅ `2db6c56` |
| W28 | `scripts/session_state.py` | modify (subcommand `block --reason`; test `tests/test_session_state.py`) | medium | `implementer_agent` | sonnet | medium | ✅ `b0cb9d9` |
| W38 | `scripts/session_state.py` | modify (subcommand `unblock`: BLOCKED → OPEN, drops `blocked_reason`; test `tests/test_session_state.py`) — added in execution, human decision 2026-10-24 | medium | `implementer_agent` | sonnet | medium | ✅ `eec0001` |
| W29 | `workflows/remediation_workflow.md` | modify (Phase 2, Phase 3, rule 3 of D6) | medium | `doc_orchestrator` | sonnet | medium | ✅ `61395e5` |
| W30 | `scripts/merge_json.py` | modify (fix: KI-056-3 and H-007 residue; test `tests/test_merge_json.py`) | high | `implementer_agent` | sonnet | medium | ✅ `1474fa6` |
| W31 | `scripts/check_changelog_tags.py` | create (test `tests/test_check_changelog_tags.py`) | medium | `implementer_agent` | sonnet | medium | ✅ `f22a40e` |
| W32 | `Makefile` | modify (`verify` runs `check_changelog_tags.py`) | low | `implementer_agent` | sonnet | medium | ✅ `58a6728` |
| W39 | `.github/workflows/ci.yml` | modify (`fetch-depth: 0` on checkout so `make verify` sees tags for `check_changelog_tags.py` check 1) — added in execution, human decision 2026-10-24 | low | `implementer_agent` | sonnet | medium | ✅ `df50276` |

### Wave D — S3 residues and documentation

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| W33 | `skills/mcp-registry/registry.json` | modify (pinned version in `pnpm dlx` text) | low | `skill_architect` | sonnet | medium | ✅ `4d7c91a` |
| W34 | `tests/test_mcp_template.py` | modify (docstring) | low | `implementer_agent` | sonnet | medium | ✅ `1f84424` |
| W35 | `memory_index.json` | modify (line 169 wording) | low | `governance_learner` | sonnet | medium | ✅ `396754e` |
| W36 | `scripts/install.py` | modify (B5 message names `install.py`) | low | `implementer_agent` | sonnet | medium | ✅ `186ec42` |
| W37 | `skills/env-shielding-auditor/README.md` | modify (badge) | low | `skill_architect` | sonnet | medium | ✅ `9a084b5` |

### Wave E — `install.sh` residue (`KI-057-5`, added in execution by human decision 2026-10-25)

Every row replaces a prescription to run the deprecated shim `install.sh` with `install.py` (`agents.md §3 federation`). Kept unchanged, because they describe the shim correctly: `agents.md:78,112`, `README.md:60,107`, `SECURITY.md:17`, `docs/guides/AGENTS_SLASH_COMMANDS_GUIDE.md:16,35,138`, `docs/guides/SELF_IMPROVEMENT_GUIDE.md:34`, `scripts/install.py:3,5`, `tests/test_installer.sh` (tests the shim itself).

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| W40 | `scripts/session_start.py` | modify (`_run_bridge_install` runs `install.py` with the running interpreter; message names `install.py`; test `tests/test_session_start.py`, incl. `:764` docstring) | medium | `implementer_agent` | sonnet | medium | ✅ `364df20` |
| W41 | `scripts/bridge_state.py` | modify (docstring `:33`, `:226`) | low | `implementer_agent` | sonnet | medium | ✅ `bedf2da` |
| W42 | `scripts/_root.py` | modify (comment `:71`) | low | `implementer_agent` | sonnet | medium | ✅ `027d439` |
| W43 | `tests/test_root_resolution.py` | modify (docstring `:57`) | low | `implementer_agent` | sonnet | medium | ✅ `7245cdc` |
| W44 | `scripts/merge_json.py` | modify (`DEPRECATED_HOOK_COMMANDS` gains the `SessionStart` command string W45 retires; its test `tests/test_merge_json.py::test_pre_install_py_session_start_command_is_replaced` landed with W45 in `3b35681`, because it reads the W45 template) | high | `implementer_agent` | sonnet | medium | ✅ `6296e09` |
| W45 | `claude/settings.hooks.json` | modify (`:78` hook fallback message names `install.py`; carries W44's test `tests/test_merge_json.py::test_pre_install_py_session_start_command_is_replaced`, which pins that the retired command differs from the template's and is pruned on merge; no reviewed-copy test pins the new fallback text) | high | `implementer_agent` | sonnet | medium | ✅ `3b35681` |
| W46 | `config/invocation_exceptions.json` | modify (note `:65`) | low | `implementer_agent` | sonnet | medium | ✅ `cabfa69` |
| W47 | `.gitignore` | modify (comment `:101`) | low | `implementer_agent` | sonnet | medium | ✅ `2486161` |
| W48 | `workflows/start_workflow.md` | modify (`:33` bridge_check) | low | `doc_orchestrator` | sonnet | medium | ✅ `0b110fc` |
| W49 | `workflows/deployment_workflow.md` | modify (`:28` bridge_lock_refresh) | low | `doc_orchestrator` | sonnet | medium | ✅ `136b2e3` |
| W50 | `rules/project_topology.md` | modify (`:34` S-1 row) | medium | `rule_validator` | sonnet | medium | ✅ `e3aef77` |
| W51 | `docs/guides/AUTONOMY_POSTURE_GUIDE.md` | modify (`:12`, `:29`) | low | `doc_orchestrator` | sonnet | medium | ✅ `c04710f` |
| W52 | `docs/guides/SELF_IMPROVEMENT_GUIDE.md` | modify (`:61`, `:92`) | low | `doc_orchestrator` | sonnet | medium | ✅ `379f9da` |
| W53 | `docs/standards/templates/SYSTEM_OVERVIEW_TEMPLATE.md` | modify (`:41`) | low | `doc_orchestrator` | sonnet | medium | ✅ `36a6c7f` |
| W54 | `docs/architecture/global_topology.md` | modify (`:53`) | low | `doc_orchestrator` | sonnet | medium | ✅ `3766aec` |
| W55 | `docs/architecture/topology_map.md` | modify (`:17`, `:20`) | low | `doc_orchestrator` | sonnet | medium | ✅ `ad146ad` |
| W56 | `profiles/example-project/README.md` | modify (`:20`, `:27`, `:29`) | low | `doc_orchestrator` | sonnet | medium | ✅ `0c0349a` |
| W57 | `.github/ISSUE_TEMPLATE/bug_report.yml` | modify (`:26`) | low | `doc_orchestrator` | sonnet | medium | ✅ `231afdf` |
| W58 | `skills/slash-commander/README.md` | modify (`:49`) | low | `skill_architect` | sonnet | medium | ✅ `9d32318` |
| W59 | `skills/slash-commander/SKILL.md` | modify (`:12`, `:30`; own skill, not vendored) | low | `skill_architect` | sonnet | medium | ✅ `e9cc07a` |

### Wave F — Gate 1 round 1 remediation (QA1-1..QA1-10, added by human decision 2026-10-26)

QA Gate 1 round 1 rejected the sprint (`SPRINT_LOG.md` Quality Gate, `a9ae7f9`). Every finding is remediated, S3 included, by human decision. QA1-3 widened during scoping: `hooks/on_commit.py` and `scripts/check_fix_reproduces.py` also disagree on what a test path is (`tests.py`; a staged test file counts as source in the hook). W61, W62 and W64 therefore replace both classifications with one shared definition instead of adding `.json` to the hook's suffix list (`agents.md §1 fail_closed_claims`). Gate 1 round 2 reviews `a9ae7f9..HEAD`.

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| W60 | `scripts/session_state.py` | modify (QA1-1: `_hotfix_refusal` judges the deployed ref: the branch condition reads `--branch` when given and the `HEAD` branch only otherwise; the hotfix record must exist in the tip tree, not the working tree; test `tests/test_session_state.py` reproduces the round 1 case) | high | `implementer_agent` | sonnet | medium | ✅ `1d5313e` |
| W61 | `scripts/_repro_grammar.py` | modify (QA1-3: add `is_test_path` and `is_source_path`, one definition for hook and replayer; `tests.py` is a test; test `tests/test_repro_grammar.py`) | medium | `implementer_agent` | sonnet | medium | ✅ `698cc57` |
| W62 | `scripts/check_fix_reproduces.py` | modify (QA1-3: import the W61 predicates, delete the local `is_test_path` and `NON_SOURCE_SUFFIXES`; existing tests unchanged) | medium | `implementer_agent` | sonnet | medium | ✅ `368f86c` |
| W63 | `scripts/check_fix_reproduces.py` | modify (QA1-6: insert the script directory into `sys.path` before the sibling import, as `check_changelog_tags.py:54`; test `tests/test_check_fix_reproduces.py` runs the script under `python3 -I`) | low | `implementer_agent` | sonnet | medium | ✅ `87b8d84` |
| W64 | `hooks/on_commit.py` | modify (QA1-3 + QA1-2: `audit_regression_test` uses the W61 predicates, deleting `TEST_PATH` and `SOURCE_SUFFIXES`; docstring and rejection text name `Repro: manual` as the route for an untestable fix; test `tests/test_on_commit.py`: a JSON-only `fix(` without trailer is rejected) | high | `implementer_agent` | sonnet | medium | ✅ `f782d37` |
| W65 | `rules/code_craft.md` | modify (QA1-2: `:80` commit-time row states the test-or-`Repro: manual` alternative and the W61 source definition) | low | `rule_validator` | sonnet | medium | ✅ `7a22d85` |
| W66 | `agents.md` | modify (QA1-2: `§2 jurisdictional_lock` companion clause says a paired test or a `Repro: manual` trailer) | medium | `rule_validator` | sonnet | medium | ✅ `e10809c` |
| W67 | `scripts/install_claude.sh` | modify (QA1-4: deprecation message names `scripts/install.py`; `exec` target unchanged; test `tests/test_installer.sh` when it asserts the message) | low | `implementer_agent` | sonnet | medium | ✅ `d5d242f` |
| W68 | `docs/sprints/057-core-pipeline/task_scope.md` | modify (QA1-5: W44/W45 rows state where the test landed and what it covers; QA1-4: drop `scripts/install_claude.sh` from the Wave E keep-list) | low | `orchestrator` | sonnet | medium | ✅ `5e0df70` |
| W69 | `scripts/session_start.py` | modify (QA1-7: the lock permission-denied message names the SessionStart hook only for target `claude`; for any other target it names `install.py`'s `install_command`; test `tests/test_session_start.py`) | low | `implementer_agent` | sonnet | medium | ✅ `4dc9fbf` |
| W70 | `scripts/check_changelog_tags.py` | modify (QA1-8: resolve `--changelog` against the invocation directory before `os.chdir`; test `tests/test_check_changelog_tags.py`) | low | `implementer_agent` | sonnet | medium | ✅ `b5f8d3e` |
| W71 | `scripts/check_changelog_tags.py` | modify (QA1-9: Google-style `Args:`/`Returns:` at `:113`) | low | `implementer_agent` | sonnet | medium | ✅ `9104649` |
| W72 | `scripts/py_compile_tree.py` | modify (QA1-9: Google-style `Args:`/`Returns:` at `:35`, `:45`) | low | `implementer_agent` | sonnet | medium | ✅ `7561d8a` |
| W73 | `scripts/check_role_artifact.py` | modify (QA1-9: Google-style `Args:`/`Returns:` at `:300`, `:315`, `:325`) | low | `implementer_agent` | sonnet | medium | ✅ `2416fee` |
| W74 | `workflows/pipeline_workflow.md` | modify (QA1-10: one path-form note under the title: commands are written in nucleus form, a host prefixes `.agents/`; version bump; regenerated step map as companion) | low | `doc_orchestrator` | sonnet | medium | ✅ `c240c91` |
| W75 | `workflows/remediation_workflow.md` | modify (QA1-10: same note; version bump; regenerated step map as companion) | low | `doc_orchestrator` | sonnet | medium | ✅ `4661026` |
| W76 | `workflows/deployment_workflow.md` | modify (`RA-14` companion of W60: `sprint_seal_gate` hotfix conditions (1) and (2) state the tip-tracked record and the deployed branch) — added in execution | low | `doc_orchestrator` | sonnet | medium | ✅ `493d300` |

Ordering: W61 before W62 and W64 (both import its predicates); W62 before W63 (same subject); W70 before W71 (same subject); W60 claims `scripts/session_state.py` after W38; W60 before W76. `fix(` units with paired test and `Repro:` trailer: W60, W63, W64, W69, W70 (W67 when `tests/test_installer.sh` asserts the message, else `Repro: manual`).


### Wave G — Gate 1 round 2 remediation (QA2-1..QA2-7, added by human decision 2026-10-26)

QA Gate 1 round 2 rejected the remediation (`SPRINT_LOG.md` Quality Gate, `af071d9`). QA2-3 is the second occurrence of the QA1-2 family (an instructing text states the `fix(` paired test unconditionally, omitting the `Repro: manual` route), so `rules/qa_and_testing.md` §4 convergence rule 3 applies: W88 is a deterministic check that fails on every recorded instance. Instances found by `git grep -n -i -E "paired test|untestable|ships its (paired )?test|must stage the test|stage[sd]? (a|the|its) test"` outside `docs/sprints`, `docs/audits`, `CHANGELOG.md` and `tests`: W78-W82 and W83. Gate 1 round 3 reviews `af071d9..HEAD`.

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| W77 | `tests/test_session_state.py` | modify (QA2-1: a test whose tip tracks the record, sits on `ai-sprint/059` with a subject that does not name the hotfix, run with `HEAD` on `hotfix/H-009`; it must fail when `session_state.py` reverts `on_branch` to `git_branch()`, proved by that mutation) | medium | `implementer_agent` | sonnet | medium | ⏳ |
| W78 | `agents/implementer_agent.md` | modify (QA2-3: `:3` and `:20` name the `Repro: manual` route beside the paired test) | low | `agent_orchestrator` | sonnet | medium | ⏳ |
| W79 | `agents/rule_validator.md` | modify (QA1-2 family: `:19` companion clause names the `Repro: manual` route) | low | `agent_orchestrator` | sonnet | medium | ⏳ |
| W80 | `memory_index.json` | modify (QA2-2: `:89` replaces "must be committed as refactor(/build(/chore(" with the `Repro: manual` route) | low | `governance_learner` | sonnet | medium | ⏳ |
| W81 | `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md` | modify (QA1-2 family: `:43` a `fix(` unit names its paired test or its `Repro: manual` record) | low | `doc_orchestrator` | sonnet | medium | ⏳ |
| W82 | `workflows/pipeline_workflow.md` | modify (QA1-2 family: `:24` companion clause names the `Repro: manual` route; regenerated step map as companion) | low | `doc_orchestrator` | sonnet | medium | ⏳ |
| W83 | `hooks/on_commit.py` | modify (QA2-4: the docstring parity claim is narrowed to the files staged when the hook runs; QA2-5: the exemption comment says documentation and configuration suffixes; `:1080` comment names the `Repro: manual` route) | low | `implementer_agent` | sonnet | medium | ⏳ |
| W84 | `scripts/_repro_grammar.py` | modify (QA2-5: module and `is_source_path` docstrings say the denylist holds documentation and `.yml`/`.yaml`/`.toml` configuration suffixes) | low | `implementer_agent` | sonnet | medium | ⏳ |
| W85 | `tests/test_check_changelog_tags.py` | modify (QA2-6: two blank lines around the W70 test) | low | `implementer_agent` | sonnet | medium | ⏳ |
| W86 | `docs/sprints/057-core-pipeline/agent_assignment.md` | modify (QA2-7: every `Ola` heading becomes `Wave`) | low | `orchestrator` | sonnet | medium | ⏳ |
| W87 | `docs/sprints/057-core-pipeline/task_scope.md` | modify (QA2-7: every `Ola` heading and mention becomes `Wave`) | low | `orchestrator` | sonnet | medium | ⏳ |
| W88 | `tests/test_fix_route_wording.py` | create (convergence rule 3 for the QA1-2 family: every line of `agents.md`, `agents/*.md`, `rules/*.md`, `workflows/*.md`, `docs/standards/templates/*.md`, `docs/guides/*.md` and `memory_index.json` matching the W77-row grep pattern above also names `Repro: manual`; the claim covers exactly those files and that pattern; proved failing on each W78-W82 instance at `af071d9`) | medium | `implementer_agent` | sonnet | medium | ⏳ |

Ordering: W78-W82 before W88 (the check is green only once every instance is fixed); W86 and W87 last among the sprint records.

---

## Rule audit

### 1. `jurisdictional_lock` / `no_interference`: shared subjects and ordering

Every unit runs `sequential` (`agent_assignment.md`). A subject is claimed by one in-progress unit; the next unit starts only after the earlier one has landed (committed, status ✅).

| Shared subject | Units, in execution order | Constraint |
| :--- | :--- | :--- |
| `scripts/session_state.py` | W10, W12, W25, W28, W38 | Strictly one at a time, in this order. |
| `scripts/check_fix_reproduces.py` | W17, W18 | W17 lands before W18 starts. |

Cross-subject ordering:

| Before | After | Reason |
| :--- | :--- | :--- |
| W01 | W02, W03, W04, W05, W06 | D1 and Abort criterion 1: W02-W06 do not start until W01 records its result; if M1 or M2 is blocked, W02-W06 are skipped. |
| W03, W04 | W05 | W05 names them as invokers (`RA-16`). |
| W05 | W06 | W06 remits to `rules/project_topology.md`. |
| W15 | W16, W17 | Both import `scripts/_repro_grammar.py`. The paired tests must fail on the parent for the right reason (exit exactly 1, not a collection error: `rules/code_craft.md:80-81`), which holds only when the module already exists at the parent. |
| W26 | W27 | W27 declares an invoker for a script that must already exist (`RA-16`). |
| W31 | W32 | W32 wires a script that must already exist (`RA-16`). |
| W32 | W39 | W39 makes CI fetch the tags the wired check reads. |
| W44 | W45 | The merge must deprecate the old `SessionStart` command before the template stops shipping it, or a re-install leaves both hooks in the host. |
| W28 | W29 | W29 Phase 3 invokes `session_state.py block`. |
| W38 | W29 | W29 names `session_state.py unblock` as the only way to lift the block. |
| W07, W08 | W29 | W29 applies rule 3 of D6 (defined in W07 and W08 artifacts). |
| W12 | W13 | W13 depends on the `suspend()` contract fixed by W12. |
| W10 | W11 | W11 documents the `--hotfix` route W10 implements. |
| W06 | W25 (branch B only) | Branch B edits `agents.md`, which W06 claims. |

### 2. `fix(` units and their paired tests (`rules/code_craft.md:72-81`, §6)

| Unit | Paired test | Repro basis |
| :--- | :--- | :--- |
| W10 | `tests/test_session_state.py` | Test fails at `5851b18`; SHA in `Repro:` trailer. |
| W12 | `tests/test_session_state.py` | Same. |
| W13 | `tests/test_session_end_hook.py` | Same. |
| W14 | `tests/test_verify_py_compile.py` | Same. |
| W16 | `tests/test_on_commit.py` | Same. |
| W17 | `tests/test_check_fix_reproduces.py` | Same. |
| W19 | `tests/test_check_task_scope.py` | Same. |
| W20 | `tests/test_model_ledger.py` | Same. |
| W23 | `tests/test_session_start.py` | Same. |
| W30 | `tests/test_merge_json.py` | Same. |
| W18, W21, W24, W25 | `tests/test_check_fix_reproduces.py`, `tests/test_detect_drift.py`, `tests/test_check_role_artifact.py` (W25 names none) | Conditional `fix(`: only if D8 reproduction succeeds; otherwise the unit closes with a `RECORD` row and no code commit. |

Not `fix(`: W09, W15, W26, W31 (new or extended behaviour, tests listed in the table), W28 (new subcommand), W32, W34, W36. W22 is a workflow edit with no executable subject.

### 3. Applicable rules per wave

| Wave / units | Rules loaded |
| :--- | :--- |
| Source units (W03, W04, W09, W10, W12-W21, W23-W26, W28, W30, W31, W36) | `rules/code_craft.md`; `agents.md §1` (type hints, Google docstrings, `max_lines_per_func` 50, `max_indentation` 3, no `pass` in except, no `TODO`/`FIXME`); `RA-11` for hooks (W16 exits 2 to block); `RA-16` (each new script declares `invoked_by:`) |
| Tests (all `tests/*` named above, W34) | `rules/qa_and_testing.md`; `agents.md §3 local_testing`; a template test that claims coverage uses reviewed-copy equality (`§1 fail_closed_claims`, `agents.md:50`) |
| Docs and rules (W00, W05, W07, W08, W11, W22, W27, W29) | `rules/documentation_standard.md`; `RA-14` patch propagation (grep the sprint artifact set at each patch); W00 and W29 new text follows D7 criteria |
| W01-W06 (S0 lane) | `agents.md RA-09` (`agents.md:159`), `RA-19` (`agents.md:169`), `rules/project_topology.md` §4 sandbox table |
| W30, W31 wording | `agents.md §1 fail_closed_claims`: bare "fail-closed" means exit non-zero on malformed input only. A coverage claim ("every", "any", "complete") requires reviewed-copy equality. W30 prunes a named set of retired keys and subtrees and MUST state that exact set; it MUST NOT claim "all retired entries removed". W31 checks tag-to-header presence and descending order only. |
| W35 | `agents.md §4 single_line_breakdown` (one sentence per entry); R6-2 removes the coverage sense of "fail-closed" |
| W33, W37 | `rules/skills_and_integrations.md §3` (no edit of vendored `SKILL.md`; neither target is a `SKILL.md`, and `skills/mcp-registry` has its own entry in `config/invocation_exceptions.json:63`) |

### 4. W06 against `RA-09` and `RA-19`

| Question | Finding |
| :--- | :--- |
| Does W06 conflict with `RA-09` (`agents.md:159`)? | No, if worded as a scoped exception. `RA-09` bans reading `.env` and printing its values; `./.env.agent` is a different file holding disposable test credentials. The sentence must keep `./.env` and every other `./.env.*` banned and name `./.env.agent` as the single readable file. |
| Must W06 avoid boundary claims (`RA-19`, `agents.md:169`)? | **Yes.** `RA-19` PROHIBITS stating in a rule that the sandboxed agent "cannot reach" a secret or that a write-deny set is a "boundary" without a measured enumeration of every out-of-sandbox entry point. The sentence MUST NOT say the agent "cannot write", "cannot read `.env`", "is isolated from" or "is protected by" anything. Permitted wording: a prescription (the agent MAY read `./.env.agent`; a human creates it; the `SessionStart` hook checks it as hygiene, not as a security control — plan D2) plus `RA-19`'s default form "write-denies REDUCE exposure; they are not a boundary". |
| Must the sentence stay one sentence? | Yes (W06 row, plan line 170). The measurement outcome (M2) is cited by file name `SANDBOX_DB_MEASUREMENT.md`, not restated. |

### 5. Findings against current rules

| # | Severity | Location | Finding | Required action |
| :--- | :--- | :--- | :--- | :--- |
| F1 | S1 | Plan `IMPLEMENTATION_PLAN.md:88-94` (D2), `:224` (Mechanisms); W03 | The prescribed safety procedure runs `scripts/env_agent_check.py` from a `SessionStart` hook outside the sandbox. In nucleus mode the agent can write `scripts/`; in host mode the template's write-deny only REDUCES exposure. `RA-19` (`KI-055-6`, `agents.md:169`) PROHIBITS prescribing a procedure that executes agent-writable content unless the measured enumeration covers that execution. `docs/sprints/056-core-pipeline/SANDBOX_ENUMERATION.md` is the enumeration; it lists hooks as entry points and is per CLI version. | W03 and W05 wording MUST cite the enumeration entry that covers a hook-run validator, or state the exposure instead of the safety claim. If the enumeration does not cover it, W01 extends the measurement or W03/W05 drop the safety wording. |
| F2 | S2 | Plan `:91-92` (D2: "el agente no puede leer `.env`"), `:139` of `skill_assignment.md` | Boundary-style claim in sprint prose. `RA-19` bans it in rules, workflows, docs and CHANGELOG. | Do not carry the sentence into W05, W06, W02's test docstring, the CHANGELOG entry or `SANDBOX_DB_MEASUREMENT.md`. |
| F3 | S2 | W25 (plan line 191) | The row's subject is `scripts/session_state.py`, but branch B deletes prescriptions in `workflows/`, `rules/` and `agents.md`. That is several structural subjects under one row, against `jurisdictional_lock`. | If the grep in branch A finds no reader, the executing session stops and the principal agent adds one `task_scope.md` row per edited file (assignees by ownership: `doc_orchestrator` for `workflows/`, `rule_validator` for `rules/` and `agents.md`) before any edit. |
| F4 | S2 | W02 test (plan line 166) | A template test over `allowRead`/`denyWrite` may be written as an enumeration with a coverage claim. | The test either states the exact keys it checks and claims nothing wider, or compares the whole object to a reviewed copy (`agents.md:50`, `fail_closed_claims`). |
| F5 | S3 | Plan `:182` (W16) | B-2 (`Repro: manual` passes without a staged test) restates behaviour already defined at `rules/code_craft.md:80`. | Before editing, W16 confirms whether the defect is in the hook or in the plan's description; if the hook already matches `code_craft.md:80`, the sub-item closes with a `RECORD` row. |
| F6 | S3 | Plan `:149` | The plan declares legend `Assignee (proposed)`; the authority is `agent_assignment.md`, which overwrites W01. | Resolved in this file (W01 is `doc_orchestrator`). The plan is not edited per Phase 4.3 scope. |

No other rule violation found: contiguous ids W00-W37 (38 rows, matches `Cost`), every `fix(` row names its test, every new mechanism names an invoker (`Mechanisms` table), the plan carries `Out of scope` and `Abort criterion`, and no assignee lacks `Write`/`Edit` for a mutating operation (`check_task_scope.py:211-233`).

### 6. Abort criterion hooks

| Condition | Effect on this scope |
| :--- | :--- |
| W01 measures M1 or M2 blocked | W02-W06 move to ⛔ skipped; row goes to Sprint 059 as `KI-057-n`. |
| Three rejections of one S0/S1 family on `claude/settings.hooks.json` (W02) or `scripts/merge_json.py` (W30) | Revert that unit (`git revert`), open `workflows/remediation_workflow.md` Phase 0; no fourth vector is added to an enumeration. |

## Carry-over recorded during execution

| From | Item | Destination |
| :--- | :--- | :--- |
| W08 | `workflows/pipeline_workflow.md` Phase 7 still names the 5-column gate table `Gate \| Round \| Verdict \| Class \| Notes`; the template now has `Severity` before `Notes` | W27 (same file): update the header string in the same commit |
| W00 | Source guidance conflicts with `agents.md`: §1 `restrictions` vs positive rewrites (PC-11), normative MUST density (PC-01), precedent narratives across §1/§2/§5/§7 (PC-05), tables vs prose (§1 `technical_clarity`) | Sprint 060 prompt audit |
| W07 | Precedence rule added by the lead: the stricter verdict wins when class and severity disagree | Gate 1 reviews it as part of W07 |
| W01 | `KI-057-1`: pytest against a local database cannot run in the sandbox — TCP to 127.0.0.1 measured denied (M1, CLI 2.1.119); `.env.agent` readability (M2) feasible but unused until a DB route exists | Sprint 059 (sandbox regime) |
| W13 | `KI-057-2`: defect E (SessionEnd suspends a session other than the one ending) needs the boot to record the harness `session_id` in the anchor; no comparable field exists (`claim` mints `20261024T112815Z-…`) | A later core-pipeline sprint |
| W19 | Same naive `split("\|")` cell parsing remains in `scripts/check_forge_ladder.py:58`, `scripts/check_gate_log.py:64`, `scripts/detect_new_models.py:142` | `KI-057-3`, a later core-pipeline sprint |
| W01 | M3: `git worktree add` measured allowed in a nucleus-shaped fixture; B-5 does not reproduce there (host `.git/modules/.agents` deny not carried) | W18: B-5 closes as not reproduced unless a host-shaped measurement says otherwise |
| W24 | `KI-057-4` (S2, `instructing`): the `F-107-N1` closure in `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md:88` says `check_role_artifact.py` moved off `SubagentStop`, but `claude/settings.hooks.json:129` still runs it `--from-hook` on every subagent stop | A later core-pipeline sprint; tell host H1 with the B-7 verdict |
| W21 | C-1 fixed for the only prescribed post-seal path outside anchor + CHANGELOG (`.agent_state/mirror.json`); host H1 is asked which file its routine commits touch | Host H1 verdict message |
| W25 | C-9 verdict for host H1: not reproduced in the nucleus; the fields are likely host-side content | Host H1 verdict message |
| W22 | C-2 reproduced from plan line 206 only: the host H1 report text is no longer in the repository; confirm with H1 that the defect matches. Open design question (not C-2): `agents.md §0` places history under `sprints/` and `config/artifact_registry.json` names `PHASE_REGISTER.md` the phase record, yet Phase 4 reconstructs it under `docs/roadmaps/` | Host H1 verdict message; a later core-pipeline sprint |
| W36 | `install.sh` still named as the command in `scripts/bridge_state.py:33`, `scripts/session_start.py:488-490` (`_run_bridge_install` runs the shim and reports "scripts/install.sh missing"), `workflows/deployment_workflow.md:28`, `rules/project_topology.md:34`, `tests/test_session_start.py:764` docstring | `KI-057-5` → Wave E (W40-W59), this sprint, human decision 2026-10-25 |
| W31 | `HISTORICAL_GAPS` = `v3.4.0`, `v3.5.2`: tags released without a ledger section; closed history not rewritten | Recorded; no action |

## Resume point (updated 2026-10-26, session `aeda1d83-cbd8-463b-8f56-25f5958d428e`)

QA Gate 1 round 2 REJECTED (charter, S2; `af071d9`); round 1 findings closed. Next: execute Wave G (W77-W88), then Gate 1 round 3 in fresh context over `af071d9..HEAD`; then Gate 2 (`tester_agent`, fresh context, base `5851b18`); then Phase 8 closeout. A third consecutive REJECTED of the QA1-2 family opens `workflows/remediation_workflow.md`. Before closeout, `SPRINT_LOG.md` Sprint Progression still shows its Phase 3 state and must be brought in line with this file.
