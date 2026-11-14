# .agents Global Context & Governance Rules

Rows keep the rule and a pointer; history and precedents: `docs/guides/RULE_PRECEDENTS_GUIDE.md`. In a row, `(precedents)` means that file, under the row's key.

## 0. Documentation Entry Point

| Rule | Value / Constraint |
| :--- | :--- |
| **Entry Point** | MUST read `docs/0_SYSTEM_OVERVIEW.md` first (host-only); nucleus: `agents.md` and `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` (generated; never hand-edit). |
| **Hierarchy** | `architecture/` (Law), `roadmaps/` (Future), `walkthroughs/` (Achievements), `sprints/` (History). |
| **Traceability** | Every module MUST have a `[MODULE]_BLUEPRINT.md` in `architecture/` before coding (template: `docs/standards/templates/BLUEPRINT_TEMPLATE.md`). |
| **Execution** | Every task must be recorded in the current Sprint folder. |
| **Implementation Plan** | Sprint MUST leave `IMPLEMENTATION_PLAN.md` in its `§5 mandatory_topology` directory, committed before Phase 5 (`§2 triple_lock`). (precedents) |
| **Master Ledger** | Host `CHANGELOG.md`: closeout appends under `[Unreleased]`, deploy seals `[vX.Y.Z]`; each entry names its commit by short SHA. (precedents) |
| **Certification** | See `RA-05: SPRINT_CLOSEOUT` for the closeout artifact list. |
| **Open upstream findings** | **Nucleus sessions only.** Read `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` before planning; the `--boot` intake queue is triaged in Phase 1. |
| **Command paths** | Declared once here for both forms of a framework command a document names. **Host:** `.agents/` is a git submodule; run from the host root as `python3 .agents/scripts/<name>.py` (likewise `.agents/hooks/`, `make -f .agents/Makefile <target>`). **Nucleus:** this repository is `.agents`; run `python3 scripts/<name>.py` and `make <target>` (`scripts/_mode.py` decides the mode; `.git` is a real directory in the nucleus). A document that writes the bare nucleus form means the host form when run in a host. |

### Rule Contexts (lazy-load index)
Domain rules in `rules/` load **on demand** at these triggers, never preloaded. Mirror: `config/rule_triggers.json` (`verify_references.py` check `(e)`).

| Rule file | Load when… |
| :--- | :--- |
| `rules/code_craft.md` | Writing or modifying source code in any language (not documentation or governance edits). |
| `rules/loop_governance.md` | Before wrapping any phase in `/loop` or `/schedule`, or authoring an unattended routine. |
| `rules/token_economy.md` | Authoring/auditing a plan or `task_scope`, measuring session cost, or changing model tiers / token-economy instruments (not every source edit). |
| `rules/qa_and_testing.md` | Writing/running tests, entering the Quality Gate, or after 3 consecutive failures. |
| `rules/project_topology.md` | Running local commands, choosing interpreters/paths, installing packages, or touching DB containers. |
| `rules/skills_and_integrations.md` | Searching, registering, or forging skills/tools. |
| `rules/frontend_modular_standard.md` | Touching `frontend/src/modules/`. |
| `rules/django_backend_standard.md` | Writing or modifying Django code — models, views, serializers, `signals.py`, app layout, or DRF endpoints. |
| `rules/graphify.md` | Querying or rebuilding the knowledge graph. |
| `rules/documentation_standard.md` | Editing any document under `docs/` or `rules/`, authoring an ADR, or running `docs-freshness-check`. |
| `rules/LEGACY_RULE_CONCORDANCE.md` | Encountering a numbered `Rule NN` citation in any document. |

## 1. Code, Dialect, and Style

| Category | Rule (Key) | Value / Constraint (Value) |
| :--- | :--- | :--- |
| **Python** | `naming_convention` | `snake_case` (vars/funcs), `PascalCase` (classes) |
| **Python** | `linter_command` | `ruff check .` (Reject if exit code > 0); `make verify` runs it. `rules/code_craft.md §8`. |
| **JS/TS** | `naming_convention` | `camelCase` |
| **JS/TS** | `linter_command` | `pnpm run lint` (Reject if exit code > 0); judged at the QA gate, NOT run by `make verify`. `rules/code_craft.md §8`. |
| **Documentation**| `python_style` | Google Style (`Args:`, `Returns:`) |
| **Documentation**| `js_ts_style` | JSDoc (`@param`, `@returns`) |
| **Types** | `requirement` | Mandatory type hints on all args and return values |
| **Complexity** | `max_indentation` | 3 levels of block-nesting depth (module-level `def` body = level 1; level 4 exceeds). Gate: `make quality-audit`. `rules/code_craft.md §8`. |
| **Complexity** | `max_lines_per_func` | 50 executable lines (blank, comment-only, docstring and decorator lines excluded). Same gate. `rules/code_craft.md §8`. |
| **Errors** | `exception_handling` | No `pass` in except; log. A fault boundary catches every `Exception`; catching only expected types is PROHIBITED. `rules/code_craft.md §8`. |
| **Verification** | `fail_closed_claims` | Fail-closed: non-zero or non-compliant on bad input or missing dependency. A coverage claim ("any"/"every") needs reviewed-copy equality; a subset check MUST state its subset. Same-family repeat: replace the enumeration or narrow the claim. `rules/code_craft.md §8`. |
| **Storage** | `path_type` | Relative only. No absolute paths. |
| **Markers** | `ephemeral` | Check regex for `TODO` or `FIXME`. Reject if found. |
| **Language** | `code_logic` | Strictly English (No Spanish in code/logs/commits/artifacts) |
| **Language** | `user_chat` | Spanish strictly confined to human-agent chat and Implementation Plans. |
| **Language** | `technical_clarity` | Avoid redundant greetings. Prioritize Markdown Tables. Restrict Mermaid/ASCII. |
| **Language** | `restrictions` | Define explicitly what is prohibited. Avoid vague positive actions. |
| **Language** | `unambiguous_action` | EVERY instruction (plan step, task, commit message, rule) MUST state its operation, its target by name and its done-criterion. PROHIBITED: deictics (`here`), verbs hiding the operation (`align`, `review`), unproven adjectives (`clean`), unitless magnitudes, hidden-actor passive. |

## 2. Autonomy, Efficiency, and Execution

| Category | Rule (Key) | Value / Constraint (Value) |
| :--- | :--- | :--- |
| **Security** | `triple_lock` | Approved Implementation Plan + Active Sprint + QA/Tester Approval + Human OK; the plan is committed **before** Phase 5. (precedents) |
| **Context** | `token_saver` | Files >200 lines MUST NOT be fully dumped; use targeted partial reads (offset/limit). Ladder: `rules/token_economy.md`. |
| **Context** | `ast_skeleton` | For structural discovery on large files, run `skills/omni-context-minimizer/scripts/omni_minimizer.py` before any partial read. |
| **Context** | `anti_amnesia` | Re-read `agents.md` and `active_state.json` once per session (at start) and after any context compaction — not after every step. |
| **Context** | `graph_sovereignty`| Query `graphify-out/graph.json` via MCP or CLI before any full codebase research or recursive grep operations. |
| **WIP Safety** | `pre_shielding` | Abort if `git status --porcelain` returns unresolved differences. |
| **WIP Safety** | `destructive_flags` | Reject massive modifications/deletions unless the human grants explicit approval (via chat or Claude Code's permission prompt). |
| **WIP Safety** | `graph_sync` | Run `venv_skillopt/bin/python -I scripts/graph_update.py` at quality check or commit, never the bare `graphify` (`rules/graphify.md`). |
| **Isolation** | `jurisdictional_lock` | A task claims **exactly one file as its structural subject** in `task_scope.md`; no concurrent task may claim it. A commit also stages files the subject's rules require, e.g. a `fix(`'s paired test unless `Repro: manual`. (precedents) |
| **Isolation** | `no_interference` | Abort if `task_scope.md` shows the target file listed by another subtask in progress. |

## 3. Architecture and Topology of the Project

| Category | Rule (Key) | Value / Constraint (Value) |
| :--- | :--- | :--- |
| **Framework** | `federation` | Check `git remote`; isolate `.agents` as a *Git Submodule*. Only `.agents/scripts/install.py` may inject content into the host's `.claude/`. |
| **Framework** | `strict_rule` | Prohibited to alter internal architecture of this submodule from tactical injections. |
| **Framework** | `symlink_gate_exclusion` | A host-root `AGENTS.md` symlink into `.agents/agents.md` is **out of host gate scope**; the host excludes its path. |
| **Framework** | `jurisdiction` | **Jurisdiction is where the anchor is.** Nucleus: records in `.agents/docs/sprints/`. Host: records at host root, `git -C .agents status --porcelain` MUST stay empty, framework fixes via `§4 feedback_upstream`. `rules/project_topology.md §5`. |
| **Environment** | `no_globals` | Cap or reject global injections in the main OS binary. |
| **Environment** | `dependencies` | Force explicit prefix syntax by invoking commands through isolated local dev environment. |
| **Infrastructure**| `three_file_standard` | Skills with `scripts/` MUST have `README.md`, `SKILL.md`, `scripts/__init__.py`; others only `SKILL.md`; padding PROHIBITED. `rules/skills_and_integrations.md §4`. |
| **Infrastructure**| `topological_order`| Skills flat in `skills/` (sub-layers PROHIBITED). Production profiles never enter the nucleus (`RA-15`): `install.py --profile-path`. `rules/skills_and_integrations.md §4`. |
| **Infrastructure**| `enforcement` | Auditor: `skills/topology-monitor/scripts/legacy_app_auditor.py`; `mass-standardizer` only regenerates `skills/manifest_skills.json`. |
| **Infrastructure**| `secret_sovereignty`| See `RA-09: SECRET_SOVEREIGNTY` (canonical). BANNED from reading `.env` into memory or printing a value from it. |
| **QA Framework** | `local_testing` | Isolate the test DB, default `sqlite:///:memory:`; another engine MUST have a host ADR (`ADR-0016`); shared or persistent DBs PROHIBITED. `rules/qa_and_testing.md §7`. |

## 4. Memory Management and Feedback Loop

| Category | Rule (Key) | Value / Constraint (Value) |
| :--- | :--- | :--- |
| **Amnesia** | `zero_tolerance` | Zero-Tolerance Accumulation. Bug resolutions MUST be immediately injected. |
| **Amnesia** | `ephemeral_memory` | The `memory` directory is strictly ephemeral. MUST be emptied upon sprint closure. |
| **Feedback Loop** | `constitutional_escalation`| Systemic improvements: routed by `governance_learner`, audited before purging logs. |
| **Feedback Loop** | `definitive_amnesia` | Temporary logs are permanently deleted the moment the fix is applied. |
| **Index Routing** | `index_files` | Parse exclusively `memory_index.json` locally. |
| **Index Routing** | `single_line_breakdown`| Reject JSON insertions that break the 1-sentence limit without a carriage return. |
| **Feedback Loop** | `feedback_upstream` | `routing_class`: `host` \| `profile` \| `nucleus` \| `discard`. host-class: local; **project-family-class** findings route to `profiles/[name]/` (rules/skills/docs), a real project's at `--profile-path`, never in the nucleus (`RA-15`); framework-class MUST become a nucleus contribution. `docs/guides/SELF_IMPROVEMENT_GUIDE.md`; (precedents) |

## 5. Central Base (Project Master Index)

| Category | Rule (Key) | Value / Constraint (Value) |
| :--- | :--- | :--- |
| **Initialization** | `mandatory_topology` | Reject init if `/docs/` missing. Canonical sprint path: `docs/sprints/[Sprint_ID]-[Stack]-[Layer]/`. |
| **Initialization** | `legacy_onboarding` | If mature project: Execute **Full Reverse Engineering** and generate Walkthroughs. |
| **Nucleus Guard** | `nucleus_neutrality` | Automatic structural scaffolding PROHIBITED if workspace is `.agents` core. |
| **Traceability** | `state_anchor` | Context MUST be extracted from `docs/active_state.json` (Zero Coordinate). |
| **Traceability** | `state_homologation` | Creating state-tracking files outside `docs/active_state.json` is PROHIBITED. |
| **Traceability** | `historical_log` | Reject pushes without the `#[Sprint_ID]` suffix (e.g. `#073`). Apply Conventional Commits. |
| **MCP Registry** | `discovery_manifest` | `.agents/claude/mcp.json` is the MCP template; `install.py` merges it non-destructively into the host's `.mcp.json`. |

## 6. Agent Roles & Execution Pipeline

The pipeline operates under a rigid sequential process. Role usurpation is strictly prohibited.

| Category | Rule (Key) | Value / Constraint (Value) |
| :--- | :--- | :--- |
| **Subagent Roles** | `principal_agent` | Lead Agent. Creates Implementation Plan (informed by graphify), manages the Approval Gate. |
| **Subagent Roles** | `devops_agent` | Environment Agent: venv, Docker; `.env` commands prepared for the human (`RA-09`). No `Write`/`Edit` on `scripts/hooks/tests` (`ADR-0009`). |
| **Subagent Roles** | `orchestrator` | Roadmap Author. Drafts Initial Roadmap and instantiates Sprint Hierarchy. |
| **Subagent Roles** | `agent_orchestrator`| Agent Assignment. Assigns specific subagents to the Initial Roadmap steps. |
| **Subagent Roles** | `skill_architect` | Skill Builder. Prepares/injects skills for the assigned subagents. |
| **Subagent Roles** | `rule_validator` | Rule Auditor. Audits Roadmap using graphify dependency graph to generate the `task_scope.md`. |
| **Subagent Roles** | `qa_agent` | Structural Verifier. Validates code standards and checks graphify AST graph integrity. |
| **Subagent Roles** | `tester_agent` | Test Verifier. Ensures logic stability and zero regression. |

> [!NOTE]
> The 8 roles above are the *Core Pipeline Roles* (mandatory in every Planning → Sprint Closeout cycle). `governance_learner`, `doc_orchestrator`, `topology_mapper`, `git_sync_agent`, `token_economy_agent` and `implementer_agent` are **Auxiliary Agents**, invoked as needed.

### 🚀 The Execution Pipeline

**Onboarding order (canonical, declared once).** Three protocols run before the pipeline on a new repository. Other documents **reference this list, never restate it** (`RA-14`):

| # | Protocol | Owns | Why here |
| :--- | :--- | :--- | :--- |
| 1 | `workflows/repository_hardening_workflow.md` (`/agents:harden`) | **Platform controls**: secret and vulnerability scanning, Dependabot, branch protection | Risk-free |
| 2 | `workflows/standardization_workflow.md` (`/agents:standardization`) | **Artifacts and topology**: census, secret scan, snapshot branch, migration | Order first |
| 3 | `workflows/reverse_documentation_workflow.md` (`/agents:revdoc`) | **Documentation of the code**: graph first, paths verified, contracts, C4, ADR | Fix against the system |
| 4 | `workflows/pipeline_workflow.md` (`/agents:pipeline`) | Change | Only now is there a verified account of what is being changed |

The normative 8-phase pipeline is defined **exclusively** in `workflows/pipeline_workflow.md`. The Approval Gate (Phase 5) is a single attended human authorization, never wrapped in an unattended `/loop`, and all execution happens on `ai-sprint/[ID]` (RA-12).

## 7. Rule Amendments

| Category | Rule (Key) | Value / Constraint (Value) |
| :--- | :--- | :--- |
| **Amendment** | `RA-01: ENVIRONMENT_VIOLATION`| On a tooling failure, MUST try one scoped fix in the isolated environment (`§3 dependencies`) before escalating, unless human-only. |
| **Amendment** | `RA-02: LAZY_SIGNAL_PARADIGM` | See `rules/django_backend_standard.md §2 Signal Registration`. |
| **Amendment** | `RA-03: HOTFIX_FLAT` | For CRITICAL/HIGH defects outside the sprint pipeline: branch MUST be `hotfix/[H-ID]`, never `fix/`, `feat/`, `chore/` or an IDE prefix (rename before the first substantive commit); `docs/hotfixes/[H-ID]-[Layer].md` before that commit; suffix `#[H-ID]`, no hyphen; next id follows the highest `docs/hotfixes/H-*.md`. Sanctioned exception to `RA-06`. |
| **Amendment** | `RA-04: FULL_DEPLOYMENT` | **Retired Sprint 046** (superseded by `RA-12`). Tombstone: `RA-05`..`RA-19` are **never renumbered**. |
| **Amendment** | `RA-05: SPRINT_CLOSEOUT` | Mandatory update of Blueprints, Global Roadmap, Walkthroughs, and Ledger before closing. |
| **Amendment** | `RA-06: IDENTITY_NAMING` | Standard Option B: All docs must be named `[MODULE]_[TYPE].md` (e.g. `USERS_BLUEPRINT.md`). |
| **Amendment** | `RA-07: ARCHIVE_PURGE` | Prohibited to keep empty `archive/` folders. Purge immediately if found. |
| **Amendment** | `RA-08: COMMIT_SQUASH` | Mandatory atomic local commits; mandatory squash & push only during Sprint Closeout. |
| **Amendment** | `RA-09: SECRET_SOVEREIGNTY`| Never read `.env` into context or print a value from it; the agent prepares secret commands, and `gh` under the sandbox, for the human to run. Exposure reduction, no boundary claim: `denyRead` list, `Read(/**/.env*)`, out-of-project `.env*` denies; keychain service and git credential helper stay open (`KI-059-21`). **No `sandbox.excludedCommands` entry may exist.** Write-denies are not a boundary (`RA-19`). `ADR-0019`; `rules/project_topology.md §5`. |
| **Amendment** | `RA-10: SUPPLY_CHAIN_SHIELD`| See `§8 Supply Chain Security` (canonical). |
| **Amendment** | `RA-11: HOOK_BLOCKING_SEMANTICS`| `PreToolUse` hooks block only on exit `2`; exit `1` only warns. A hook in `hooks/` that must halt MUST `sys.exit(2)`, never `1`. (precedents) |
| **Amendment** | `RA-12: BRANCH_DISCIPLINE`| Sprint branch `ai-sprint/[ID]`; direct commits or pushes to `main` PROHIBITED; only `deployment_workflow.md` Phase 1 merges; an IDE prefix is not valid: rename before the first substantive commit. (precedents) |
| **Amendment** | `RA-13: SEQUENTIAL_GATES`| A gate and its irreversible action MUST be separate invocations, result OBSERVED first; chaining (`sleep && merge`) voids it. |
| **Amendment** | `RA-14: PATCH_PROPAGATION`| A patch MUST be followed by a grep of its term across the sprint artifact set; headline metrics MUST be `grep`-reproducible. |
| **Amendment** | `RA-15: HOST_CONTENT_GENERICIZATION`| MUST genericize host-identifying strings (name, paths, logic) in any `feedback_upstream` contribution. |
| **Amendment** | `RA-16: INVOCATION_COVERAGE`| No mechanism merges without `invoked_by:` or an entry in `config/invocation_exceptions.json` (`verify_references.py` (d)). |
| **Amendment** | `RA-17: GATE_VERDICT_CLASSES` | Phase 7 emits `APPROVED` \| `REJECTED` \| `RECORD` with class `charter` / `instructing` / `testifying`, and a severity `S0`-`S3` per finding (the row's `Severity` cell holds the highest, or `none`). `RECORD` does not count toward remediation. Procedure: `rules/qa_and_testing.md` §4. |
| **Amendment** | `RA-18: CURSOR_PHASE1_NO_PLAN_MODE` | Under `session_tool: cursor`, Phase 1 MUST NOT invoke `SwitchMode` to plan. Write `IMPLEMENTATION_PLAN.md` at the canonical sprint path in the current session. A file under `~/.cursor/plans/` is not the `triple_lock` plan. Procedure: `pipeline_workflow.md` Phase 1. |
| **Amendment** | `RA-19: SANDBOX_BOUNDARY_CLAIMS` | **PROHIBITED**: (1) any `sandbox.excludedCommands` entry or boundary claim without a measured enumeration of EVERY out-of-sandbox entry point; (2) closing only the measured vector; (3) a safety procedure running agent-writable content. `rules/project_topology.md §5`. |

## 8. Supply Chain Security

Detail: `rules/project_topology.md §6`.

| Category | Rule (Key) | Value / Constraint (Value) |
| :--- | :--- | :--- |
| **Package Manager** | `requirement` | Mandatory use of `pnpm 11+`. `npm` and `yarn` are prohibited for installation. |
| **Installation** | `ignore_scripts` | `ignoreScripts: true` MUST be set in `pnpm-workspace.yaml` at the project root. Verified by: `pnpm config get ignoreScripts` → `true`. |
| **Release Safety** | `min_release_age` | `minimumReleaseAge: 1440` (minutes) MUST be set in `pnpm-workspace.yaml`. Verified by: `pnpm config get minimumReleaseAge` → `1440`. |
| **Audit** | `only_built_deps` | Build deps MUST be whitelisted in `pnpm-workspace.yaml` `onlyBuiltDependencies`. Verified: `pnpm config get onlyBuiltDependencies`. |
| **Location** | `config_file` | **`.npmrc` does NOT carry these settings** (`pnpm config get` returns `undefined`); a host MUST move them to `pnpm-workspace.yaml`. |
