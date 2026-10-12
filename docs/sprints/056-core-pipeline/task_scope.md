# Task Scope — Sprint 056 (core-pipeline)

Source: `docs/sprints/056-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`, units `A1`-`A22`, `B1`-`B9`) and `docs/sprints/056-core-pipeline/agent_assignment.md` (Phase 4.1, the assignee authority).
Phase 4.3 (Rule Audit), author `rule_validator`. Check: `python3 scripts/check_task_scope.py --sprint-dir docs/sprints/056-core-pipeline`.

Mode: `claude_code`, `delegation_mode: native`. Not a Cursor sprint, so `make cursor-tiers` does not apply.

## Tier transcription

`Model` and `Effort` are transcribed from `config/model_tiers.json` (`tiers.<tier>.claude_code`), keyed by the tier that lists the row's assignee in `profiles`. No `token_economy_agent` verdict exists in the sprint directory at this phase, so no tier is invented and no escalation is declared.

| Assignee | Tier | Model | Effort |
| :--- | :--- | :--- | :--- |
| `implementer_agent`, `rule_validator`, `skill_architect`, `doc_orchestrator` | `author` | sonnet | medium |
| `principal_agent` (measurement half of `B1`, `B4`) | `gate` | opus | high |

Declared escalations: `B2` -> `opus`/`high` (`token_economy_agent` pre-approval audit, 2026-10-12: a security deny-set where a plausible-looking glob was itself the defect in Sprint 055 `RA-19` rounds 1-4). Keep: `B7` stays `sonnet`/`medium` (prose against the stated rule `D14`; Gate 1 reads its diff against `D13`, finding F-8).

## Work

Sequencing rule (`agents.md §2 no_interference`): rows that share a structural subject, or whose companion test shares another row's subject, run one at a time in the order listed in the `Depends on` column of the Locks table below.

### Wave A

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `A1` | `scripts/docs_freshness_check.py` (companion: `tests/test_docs_freshness_check.py`, `fix(`) | modify: `ADR_STATUS_SUPERSEDED_RE` accepts ``**Status**: `Superseded`` (`D2`, `KI-052-1`) | low | `implementer_agent` | sonnet | medium | ✅ `7f0f926` |
| `A2` | `scripts/verify_references.py` (companion: `tests/test_verify_references.py`, `fix(`) | modify: the three `invoked_by:` substring checks use `_invoked_by_line` (`D3`, `NF-2`) | medium | `implementer_agent` | sonnet | medium | ✅ `a740f88` |
| `A3` | `scripts/verify_references.py` (companion: `tests/test_verify_references.py`, `fix(`) | modify: token boundary between paths in `_skill_doc_names_script` (`D3`, `NF-1`) | medium | `implementer_agent` | sonnet | medium | ✅ `b083715` |
| `A4` | `tests/test_root_resolution.py` | modify: assertion by checkout shape, valid in linked worktrees (`D4`, `KI-052-4`); commit `test(` | low | `implementer_agent` | sonnet | medium | ✅ `eccb6ea` |
| `A5` | `skills/env-shielding-auditor/README.md` | modify: name `scripts/env_shielding_auditor.py` (`D5`, `KI-052-7`) | low | `skill_architect` | sonnet | medium | ✅ `77eb3c4` |
| `A6` | `scripts/quality_audit.py` (companion: `tests/test_quality_audit.py`, `fix(`) | modify: nested-function boundary in JS/TS (`D6` a) | medium | `implementer_agent` | sonnet | medium | ✅ `2e4487c` |
| `A7` | `scripts/quality_audit.py` (companion: `tests/test_quality_audit.py`, `fix(`) | modify: exclude blank and comment-only rows inside multi-row statements, Python and JS/TS (`D6` b) | medium | `implementer_agent` | sonnet | medium | ✅ `9f02419` |
| `A8` | `agents.md` | modify: `§1` `max_lines_per_func` and the JS/TS `linter_command` row declare the two `D6` rules | low | `rule_validator` | sonnet | medium | ✅ `d40f3da` |
| `A9` | `scripts/install.py` (companion: `tests/test_install_with_env_render.py`, `fix(`) | modify: `RENDER_OWNED_RE` accepts paths with spaces; docstring aligned with `T2-1` (`D7`, `Q9`) | low | `implementer_agent` | sonnet | medium | ✅ `b2bf703` |
| `A10` | `scripts/install.py` (companion: `tests/test_install_with_env_render.py`, `fix(`) | modify: no crash when the JSON root is not a dict (`D7`, `Q10`) | low | `implementer_agent` | sonnet | medium | ✅ `8dba69b` |
| `A11` | `tests/test_template_sandbox.py` | modify: pin `Edit(/.agents/venv_skillopt/**)` (`Q10`); commit `test(` | low | `implementer_agent` | sonnet | medium | ✅ `40b2ffc` |
| `A12` | `tests/test_install_with_env_render.py` | modify: return types and docstrings (`Q10`); commit `test(` | low | `implementer_agent` | sonnet | medium | ✅ `2016dad` |
| `A13` | `scripts/session_state.py` (companion: `tests/test_session_state.py`) | modify: subcommand `mark-audited` (`D9`, `KI-055-7`); commit `feat(` | medium | `implementer_agent` | sonnet | medium | ✅ `46059d8, 076145c` |
| `A14` | `workflows/audit_workflow.md` | modify: last step invokes `session_state.py mark-audited` (`D9`, `RA-16`) | low | `doc_orchestrator` | sonnet | medium | ✅ `8035aea` |
| `A15` | `rules/project_topology.md` | modify: `gh` row of §4 with the "under the sandbox" condition (`D10`, `KI-055-8`) | medium | `rule_validator` | sonnet | medium | ✅ `45743dd, c025350` |
| `A16` | `agents.md` | modify: `RA-09` references the `A15` condition (`D10`) | medium | `rule_validator` | sonnet | medium | ✅ `d40f3da` |
| `A17` | `workflows/deployment_workflow.md` | modify: `pr_flow`, `github_release` and the line-31 note carry the condition (`D10`) | medium | `doc_orchestrator` | sonnet | medium | ✅ `d2c3aa4` |
| `A18` | `rules/qa_and_testing.md` | modify: `§5` `with_env.py` sentence names the actor and points to `S-3` (`D16`, `F1`) | low | `rule_validator` | sonnet | medium | ✅ `a86570f` |
| `A19` | `workflows/pipeline_workflow.md` | modify: Phase 2 points to `S-3` and names the human (`D16`, `R7-4`) | low | `doc_orchestrator` | sonnet | medium | ✅ `29781aa` |
| `A20` | `docs/standards/templates/README_TEMPLATE.md` | modify: line 91 (`D16`, `R7-4`) | low | `doc_orchestrator` | sonnet | medium | ✅ `6f1cc0c` |
| `A21` | `agents/devops_agent.md` | modify: line 16 cites the residual-risk row (`D16`, `R7-5`) | low | `doc_orchestrator` | sonnet | medium | ✅ `be7c041` |
| `A22` | `workflows/repository_hardening_workflow.md` | modify: `gh` note (line 44) points at the §4 `gh` row with the sandbox condition (`D10`); discovered in Phase 6 by the `RA-14` propagation grep | low | `doc_orchestrator` | sonnet | medium | ✅ `3d8fe3f` |

### Wave B

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `B1` | `docs/sprints/056-core-pipeline/SANDBOX_ENUMERATION.md` | create: measured enumeration at base (`D11`, `KI-055-1`, `F4`); measurement handed over by `principal_agent`, which writes nothing | high | `doc_orchestrator` | sonnet | medium | ✅ `c7c0701` |
| `B2` | `claude/settings.hooks.json` (companion: `tests/test_template_sandbox.py`, `fix(`) | modify: write-deny of all `./.agents` and `Edit(/.agents/**)`; `.git` denies only if `B1` justifies them (`D12`) | high | `implementer_agent` | opus | high | ✅ `d70d00c` |
| `B3` | `claude/mcp.json` (companion: `tests/test_mcp_template.py` (new), `fix(`; named in the plan after finding F-4) | modify: `-I` on the `graphify` launcher (`D12`, `Q3`) | medium | `implementer_agent` | sonnet | medium | ✅ `05c74a6` |
| `B4` | `docs/sprints/056-core-pipeline/SANDBOX_ENUMERATION.md` | modify: re-measurement of each vector after `B2`/`B3`, handed over by `principal_agent` (`D12`, `D13`) | high | `doc_orchestrator` | sonnet | medium | ✅ `6fd75ec` |
| `B5` | `scripts/install.py` (companion: `tests/test_install_with_env_render.py`, `fix(`) | modify: exit `2` refusal of a host `excludedCommands` entry (`D8`, `KI-055-2`) | medium | `implementer_agent` | sonnet | medium | ✅ `3bfa1d9` |
| `B6` | `rules/project_topology.md` | modify: `N3` and residual-risk rows per the enumeration; three `gh` script rows (`D13`, `D15`, `KI-055-4`) | medium | `rule_validator` | sonnet | medium | ✅ `9171740` |
| `B7` | `agents.md` | modify: `RA-19` extends the prohibition to prescribed procedures (`D14`, `KI-055-6`); `RA-09` tree list per `B2` | high | `rule_validator` | sonnet | medium | ✅ `5083e70` |
| `B8` | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify: `F-055-N1` status per `D13` and `Q` correspondence (`D16`, `F2`) | low | `doc_orchestrator` | sonnet | medium | ✅ `50b5281` |
| `B9` | `scripts/session_start.py` (companion: `tests/test_session_start.py`) | modify: advisory readiness finding when `claude --version` differs from the `Measuring CLI` row of `rules/project_topology.md` §4 (`D17`); `feat(` | medium | `implementer_agent` | sonnet | medium | ✅ `8bb0d1a` |

## Locks (`jurisdictional_lock` / `no_interference`)

A subject is claimed by one in-progress row at a time. A row starts only after every row in `Depends on` has landed (`Status` = `✅ <sha>`).

| Subject | Rows in order | Depends on (cross-subject) |
| :--- | :--- | :--- |
| `agents.md` | `A8` -> `A16` -> `B7` | `A16` after `A15`; `B7` after `B2`, `B4` |
| `scripts/verify_references.py` | `A2` -> `A3` | none |
| `scripts/quality_audit.py` | `A6` -> `A7` | none |
| `scripts/install.py` | `A9` -> `A10` -> `B5` | none |
| `tests/test_install_with_env_render.py` (subject of `A12`; companion of `A9`, `A10`, `B5`) | `A9` -> `A10` -> `A12` -> `B5` | none |
| `tests/test_template_sandbox.py` (subject of `A11`; companion of `B2`) | `A11` -> `B2` | none |
| `rules/project_topology.md` | `A15` -> `B6` | `B6` after `B4` |
| `docs/sprints/056-core-pipeline/SANDBOX_ENUMERATION.md` | `B1` -> `B4` | `B4` after `B2`, `B3` |
| `workflows/audit_workflow.md` | `A14` | after `A13` |
| `workflows/deployment_workflow.md` | `A17` | after `A15` |
| `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | `B8` | after `B4` |
| `claude/settings.hooks.json` | `B2` | after `B1` (`B1` supplies the justification for the `.git` denies) |

Every other row has a subject no other row claims (`A1`, `A4`, `A5`, `A18`, `A19`, `A20`, `A21`, `B3`).

## Findings (rule conflicts and gaps in the plan; the plan is not edited)

| ID | Unit(s) | Finding | Rule cited | Disposition in this file |
| :--- | :--- | :--- | :--- | :--- |
| F-1 | `B1`, `B4` | The plan and `agent_assignment.md` list `principal_agent` first. `agents/principal_agent.md` declares `tools: Read, Glob, Grep, TodoWrite`: no `Write`/`Edit` and no `Bash`. `scripts/check_task_scope.py` (`_capability_findings`) reads the first token of the Assignee cell and rejects a `create`/`modify` for a profile without `Write`/`Edit` (exit 2). The measurement (`claude -p` headless) also needs `Bash`, which `principal_agent` does not hold, so the parent session must run it. | `agents.md §6 principal_agent` and `ADR-0017` (owner vs writer); `scripts/check_task_scope.py` | Assignee cell is `doc_orchestrator` (writer). The measurement hand-off by `principal_agent` is recorded in the Operation cell. `agent_assignment.md` B1/B4 should be re-ordered to match; this role does not edit it. |
| F-2 | `B5` | `agent_assignment.md` orders `B5` only after `A9`, `A10`. Its companion test lives in `tests/test_install_with_env_render.py`, which is the structural subject of `A12`. Without `A12 -> B5` two tasks could claim that file at once. | `agents.md §2 no_interference` | Locks table orders `A9 -> A10 -> A12 -> B5`. |
| F-3 | `B2` | Its companion test file `tests/test_template_sandbox.py` is the subject of `A11`. `agent_assignment.md` does not order `B2` after `A11`. | `agents.md §2 no_interference` | Locks table orders `A11 -> B2`. |
| F-4 | `B3` | The plan names its companion only as "test de plantilla MCP". No existing test file covers the `graphify` launcher (`grep mcp.json tests/` hits `test_session_start.py`, `test_merge_json.py`, `test_installer.sh`, `test_bridge_state.py`; none asserts the launcher args). A `fix(` commit must carry a paired test that fails on the parent. | `rules/code_craft.md §6`; `agents.md §1 unambiguous_action` (target by name); `hooks/on_commit.py audit_regression_test` | Companion recorded as "new MCP-template test file under `tests/`". `implementer_agent` must name it in the commit; Gate 1 verifies it with `check_fix_reproduces.py`. |
| F-5 | `A14`, `A17`, `A19` | Three workflow files change, and `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` is generated from them. `make verify` gates its staleness. The plan lists regeneration only under "Documentary impact" and gives it no Work row, so no task owns it and no row records it. | `agents.md §0 Entry Point` (regenerate with `scripts/map_workflows.py`, never hand-edit); `agents.md §0 Execution` (every task recorded in the sprint) | Not added as a row (this file holds exactly the 29 plan units). Recommendation: regenerate in the same commit as the last of `A14`/`A17`/`A19`, or as a close-phase step; the guide is a generated companion, not a second subject. |
| F-6 | `A15`-`A17`, `A19`-`A21`, `B6` | `D10` changes a rule stated in several places (`RA-09`, `deployment_workflow.md:31`, `project_topology.md:39`, plus `A18`-`A21`). The plan does not require the full-corpus grep after the patch. | `agents.md §7 RA-14` (patch propagation, sprint-artifact-set clause) | Recommendation: acceptance for `A17` and the last `D10`/`D16` unit includes a grep of `agents.md rules workflows agents docs/standards` for the old unconditional phrasing, result 0 hits. |
| F-7 | `A8`, `A16`, `B7` | Three units edit `agents.md`, which `agents.md §4 constitutional_escalation` also reserves for sprint-close indexing. Close-time edits to `agents.md` must wait until `B7` lands. | `agents.md §2 no_interference`; `§4 constitutional_escalation` | Recorded in Locks; the close phase is outside this file. |
| F-8 | `B2`, `B7` | `B2` replaces six subtree denies with one whole-submodule deny and `B7` rewrites the `RA-09` tree list and `RA-19`. `RA-19` forbids stating a boundary without a measured enumeration of every entry point. `D13` already keeps the "reduces exposure, not a boundary" wording; `B7` must not weaken it. | `agents.md §7 RA-19`, `RA-09` | No change to rows. Gate 1 checks the `B7` diff against `RA-19`. |
| F-9 | `A9`, `A10`, `B5`, `A13` | `fix(` commits (`A1`-`A3`, `A6`, `A7`, `A9`, `A10`, `B2`, `B3`, `B5`) each need a `Repro:` test that fails on the parent (exit exactly 1). `A13` is `feat(` and `A4`, `A11`, `A12` are `test(`, so they are exempt. `A12` changes only types and docstrings and cannot fail on the parent; it must stay `test(` and must not be relabelled `fix(`. | `workflows/pipeline_workflow.md` Phase 7 Gate 1 first check; `rules/code_craft.md §6` | Commit type is recorded in the Operation cell of each affected row. |

No row violates `jurisdictional_lock`: each of the 31 rows has one structural subject, and every paired test is a companion. No row requires a Cursor model, so the `haiku`/`sonnet`/`opus` prohibition for Cursor sprints does not apply.
