# .agents Global Context & Governance Rules

This is the constitutional matrix of Universal-Agents (`.agents`).
It dictates in an absolute and transversal manner the behavior of subagents, code quality, and topological design.

## 0. Zero Coordinate Protocol (Documentation Matrix)

| Rule | Value / Constraint |
| :--- | :--- |
| **Matrix Entry** | Every session MUST start by reading `docs/0_SYSTEM_OVERVIEW.md`. |
| **Hierarchy** | `architecture/` (Law), `roadmaps/` (Future), `walkthroughs/` (Achievements), `sprints/` (History). |
| **Traceability** | Every module MUST have a `[MODULE]_BLUEPRINT.md` in `architecture/` before coding (template: `docs/standards/templates/BLUEPRINT_TEMPLATE.md`). |
| **Execution** | Every task must be recorded in the current Sprint folder. |
| **Master Ledger** | The host root `CHANGELOG.md` (Keep a Changelog format; template: `docs/standards/templates/CHANGELOG_TEMPLATE.md`). Every Tactical Liquidation appends its sprint entry under `[Unreleased]`; every deployment seals it as `[vX.Y.Z]` before tagging. Strictly separate jurisdiction from `.agents/CHANGELOG.md` (framework evolution) — the only crossover allowed is a pin-bump entry (`chore(deps): pin .agents to vX.Y.Z`). |
| **Certification** | Closing a Sprint requires updating Blueprints, Global Roadmap, Walkthroughs, and the Master Ledger. |

### Rule Contexts (lazy-load index)
Domain rules live in `rules/` and are loaded **on demand** at these triggers — never preloaded (token economy):

| Rule file | Load when… |
| :--- | :--- |
| `rules/token_economy.md` | Reading source files, planning subagent context, or auditing a plan's cost. |
| `rules/qa_and_testing.md` | Writing/running tests, entering the Quality Gate, or after 3 consecutive failures. |
| `rules/project_topology.md` | Running local commands, choosing interpreters/paths, or touching DB containers. |
| `rules/skills_and_integrations.md` | Searching, registering, or forging skills/tools. |
| `rules/frontend_modular_standard.md` | Touching `frontend/src/modules/`. |
| `rules/graphify.md` | Querying or rebuilding the knowledge graph. |
| `rules/LEGACY_RULE_CONCORDANCE.md` | Encountering a numbered `Rule NN` citation in any document. |

## 1. Code, Dialect, and Style

| Category | Rule (Key) | Value / Constraint (Value) |
| :--- | :--- | :--- |
| **Python** | `naming_convention` | `snake_case` (vars/funcs), `PascalCase` (classes) |
| **Python** | `linter_command` | `ruff check .` (Reject if exit code > 0) + `python-doctor check --diff` (Warning if score < 95) |
| **JS/TS** | `naming_convention` | `camelCase` |
| **JS/TS** | `linter_command` | `pnpm run lint` (Reject if exit code > 0) + `pnpm run react-doctor` (Warning if score < 95) |
| **Documentation**| `python_style` | Google Style (`Args:`, `Returns:`) |
| **Documentation**| `js_ts_style` | JSDoc (`@param`, `@returns`) |
| **Types** | `requirement` | Mandatory type hints on all args and return values |
| **Complexity** | `max_indentation` | 3 levels |
| **Complexity** | `max_lines_per_func` | 50 lines |
| **Errors** | `exception_handling` | No `pass` in except. Explicit logging required. |
| **Storage** | `path_type` | Relative only. No absolute paths. |
| **Markers** | `ephemeral` | Check regex for `TODO` or `FIXME`. Reject if found. |
| **Language** | `code_logic` | Strictly English (No Spanish in code/logs/commits/artifacts) |
| **Language** | `user_chat` | Spanish strictly confined to human-agent chat and Implementation Plans. |
| **Language** | `technical_clarity` | Avoid redundant greetings. Prioritize Markdown Tables. Restrict Mermaid/ASCII. |
| **Language** | `restrictions` | Define explicitly what is prohibited. Avoid vague positive actions. |

## 2. Autonomy, Efficiency, and Execution

| Category | Rule (Key) | Value / Constraint (Value) |
| :--- | :--- | :--- |
| **Security** | `triple_lock` | Approved Implementation Plan + Active Sprint + QA/Tester Approval + Human OK. |
| **Context** | `token_saver` | Files >200 lines MUST NOT be fully dumped. Targeted partial reads (offset/limit on the affected function) are the sanctioned mechanism. Decision ladder in `rules/token_economy.md`. |
| **Context** | `ast_skeleton` | For structural discovery on large files, invoke `omni_minimizer.py` to extract the skeleton before any partial read. |
| **Context** | `anti_amnesia` | Re-read `agents.md` and `active_state.json` once per session (at start) and after any context compaction — not after every execution step. |
| **Context** | `graph_sovereignty`| Query `graph.json` via MCP or CLI before any full codebase research or recursive grep operations. |
| **WIP Safety** | `pre_shielding` | Abort if `git status --porcelain` returns unresolved differences. |
| **WIP Safety** | `destructive_flags` | Reject massive modifications/deletions unless the human grants explicit approval (via chat or Claude Code's permission prompt). |
| **WIP Safety** | `graph_sync` | Mandate running `graphify update` post-changes during quality check or commit phase. |
| **Isolation** | `jurisdictional_lock` | Limit structural editing to `1` single physical file per instantiated subagent task. |
| **Isolation** | `no_interference` | Abort if `task_scope.md` shows the target file listed by another subtask in progress. |

## 3. Architecture and Topology of the Project

| Category | Rule (Key) | Value / Constraint (Value) |
| :--- | :--- | :--- |
| **Matrix** | `federation` | Check `git remote`; isolate `.agents` purely as a *Git Submodule*. The sanctioned bridge into the host's `.claude/` is exclusively `.agents/scripts/install_claude.sh` (symlinks + non-destructive JSON merge) — no other mechanism may inject content into the host's Claude Code configuration. |
| **Matrix** | `strict_rule` | Prohibited to alter internal architecture of this submodule from tactical injections. |
| **Environment** | `no_globals` | Cap or reject global injections in the main OS binary. |
| **Environment** | `dependencies` | Force explicit prefix syntax by invoking commands through isolated local dev environment. |
| **Infrastructure**| `trinity_standard` | **Executable skills** (they ship a `/scripts/` folder) MUST adhere to the full Trinity: 1. `README.md`, 2. `SKILL.md`, 3. `/scripts/` with `__init__.py`. **Knowledge skills** (pure guidance, no scripts) only require a `SKILL.md` with valid `name`/`description` frontmatter — padding them with empty scaffolding is PROHIBITED noise. |
| **Infrastructure**| `topological_order`| Skills flat inside `skills/`. Sub-layers (`core/`, `local/`) PROHIBITED. Project-specific packs live under `profiles/[name]/` and are only linked into a host via `install_claude.sh --profile [name]`. |
| **Infrastructure**| `enforcement` | `mass-standardizer` tool is the official auditor for this standard. |
| **Infrastructure**| `secret_sovereignty`| BANNED from reading `.env` into memory. Use environment export commands. |
| **QA Framework** | `local_testing` | Overwrite native URLs to instantiate in RAM (`sqlite:///:memory:`). |

## 4. Memory Management and Feedback Loop

| Category | Rule (Key) | Value / Constraint (Value) |
| :--- | :--- | :--- |
| **Amnesia** | `zero_tolerance` | Zero-Tolerance Accumulation. Bug resolutions MUST be immediately injected. |
| **Amnesia** | `ephemeral_memory` | The `memory` directory is strictly ephemeral. MUST be emptied upon sprint closure. |
| **Feedback Loop** | `constitutional_escalation`| Systemic improvements MUST be formally indexed into `agents.md` before purging logs. |
| **Feedback Loop** | `definitive_amnesia` | Temporary logs are permanently deleted the moment the fix is applied. |
| **Index Routing** | `index_files` | Parse exclusively `memory_index.json` locally. |
| **Index Routing** | `single_line_breakdown`| Reject JSON insertions that break the 1-sentence limit without a carriage return. |
| **Feedback Loop** | `feedback_upstream` | Learning is a LIVING three-tier flow, never a dead end: **host-class** findings stay in the host's `memory_index.json`; **project-family-class** findings route to `profiles/[name]/` (rules/skills/docs); **framework-class** findings (would improve every host) MUST be drafted as a nucleus contribution — a J-amendment proposal or fix PR to the `.agents` repo — during `extract_workflow`. Every host session is a sensor for the shared brain; letting a framework-class lesson die in a local index is a governance violation. |

## 5. Central Base (Project Master Index)

| Category | Rule (Key) | Value / Constraint (Value) |
| :--- | :--- | :--- |
| **Initialization** | `mandatory_topology` | Reject init if `/docs/` missing. Instantiate `docs/sprints/[Sprint_ID]-[Stack]-[Layer]/`. |
| **Initialization** | `legacy_onboarding` | If mature project: Execute **Full Reverse Engineering** and generate Walkthroughs. |
| **Nucleus Guard** | `nucleus_neutrality` | Automatic structural scaffolding PROHIBITED if workspace is `.agents` core. |
| **Traceability** | `state_anchor` | Context MUST be extracted from `docs/active_state.json` (Zero Coordinate). |
| **Traceability** | `state_homologation` | Creating state-tracking files outside `docs/active_state.json` is PROHIBITED. |
| **Traceability** | `historical_log` | Reject pushes without the `#[Sprint_ID]` suffix (e.g. `#073`). Apply Conventional Commits. |
| **MCP Registry** | `discovery_manifest` | `.agents/claude/mcp.json` is the submodule's MCP server template; `install_claude.sh` merges it non-destructively into the host's `.mcp.json`, which is the actual discovery point Claude Code reads. |

## 6. Chain of Command & Core Workflow (Matrix V3)

The Matrix operates under a rigid, highly militarized sequential pipeline. Role usurpation is strictly prohibited.

| Category | Rule (Key) | Value / Constraint (Value) |
| :--- | :--- | :--- |
| **Subagent Roles** | `principal_agent` | Supreme Coordinator. Creates Implementation Plan (informed by graphify), manages Golden Gate. |
| **Subagent Roles** | `devops_agent` | Environment Guardian. Manages venv, .env export, and Docker health. |
| **Subagent Roles** | `orchestrator` | Tactical Architect. Drafts Initial Roadmap and instantiates Sprint Hierarchy. |
| **Subagent Roles** | `agent_orchestrator`| HR/Staffing. Assigns specific subagents to the Initial Roadmap steps. |
| **Subagent Roles** | `skill_architect` | Tool Synthesizer. Prepares/injects skills for the assigned subagents. |
| **Subagent Roles** | `rule_validator` | Governance Sentinel. Audits Roadmap using graphify dependency graph to generate the `task_scope.md`. |
| **Subagent Roles** | `qa_agent` | Structural Verifier. Validates code standards and checks graphify AST graph integrity. |
| **Subagent Roles** | `tester_agent` | Functional Verifier. Ensures logic stability and zero regression. |

> [!NOTE]
> **Core vs. Auxiliary.** The 8 roles above are the *Núcleo del Pipeline V3* (mandatory in every Strategic Genesis → Tactical Liquidation cycle). `governance_learner`, `doc_orchestrator`, `matrix_mapper`, and `github_sentinel` (see `agents/*.md`) are **Agentes Auxiliares** — invoked as needed (knowledge distillation, documentation, topology, upstream sync) but not a mandatory stop on every pipeline pass. **Project-specific specialists** (e.g. `backend_identity_specialist`, `frontend_ux_hardener`) live in `profiles/[name]/agents/` and only join the Matrix when their profile is installed. Their absence from this table is intentional, not an omission.

### 🚀 The Execution Pipeline (Matrix V3)
The normative 8-phase pipeline (Strategic Genesis → Tactical Liquidation) is defined **exclusively** in `workflows/matrix_workflow.md`, loaded on demand via `/agents:matrix`. It is not duplicated here to keep the always-loaded constitution lean and drift-free. Non-negotiables enforced at this level: the Golden Gate (Phase 5) is a single attended human authorization — never wrapped in an unattended `/loop` — and all execution happens on `ai-sprint/[ID]` (J-12).

## 7. Jurisprudence (Heuristic Amendments)

| Category | Rule (Key) | Value / Constraint (Value) |
| :--- | :--- | :--- |
| **Amendment** | `J-01: ENVIRONMENT_VIOLATION`| Agent MUST attempt autonomous remediation EXCEPT if prohibited. |
| **Amendment** | `J-02: LAZY_SIGNAL_PARADIGM` | Prevent circular deps in Django `signals.py`: local imports in receiver. |
| **Amendment** | `J-03: HOTFIX_FLAT` | For critical bugs, use `docs/hotfixes/[H-ID]-[Layer].md` (template: `HOTFIX_TEMPLATE.md`). **Sanctioned exception to J-06 naming** — emergency speed wins over Option B; the deviation is deliberate, not drift. |
| **Amendment** | `J-04: FULL_DEPLOYMENT` | Orchestrator MUST deploy the COMPLETE task hierarchy in a single atomic action. |
| **Amendment** | `J-05: TACTICAL_LIQUIDATION` | Mandatory update of Blueprints, Global Roadmap, Walkthroughs, and Ledger before closing. |
| **Amendment** | `J-06: IDENTITY_NAMING` | Standard Option B: All docs must be named `[MODULE]_[TYPE].md` (e.g. `USERS_BLUEPRINT.md`). |
| **Amendment** | `J-07: ARCHIVE_PURGE` | Prohibited to keep empty `archive/` folders. Purge immediately if found. |
| **Amendment** | `J-08: COMMIT_SQUASH` | Mandatory atomic local commits; mandatory squash & push only during Tactical Liquidation. |
| **Amendment** | `J-09: SECRET_SOVEREIGNTY`| Prohibited from reading `.env` into thought context. Use `Makefile` or `source .env` in a subshell. |
| **Amendment** | `J-10: SUPPLY_CHAIN_SHIELD`| Mandate `pnpm 11+`, `ignore-scripts=true`, and `minimum-release-age=1440`. |
| **Amendment** | `J-11: HOOK_BLOCKING_SEMANTICS`| Claude Code `PreToolUse` hooks only block a tool call on exit code `2` (stderr fed back to the model); exit `1` is a non-blocking warning. Every hook in `hooks/` that must halt execution MUST `sys.exit(2)`, never `1`. |
| **Amendment** | `J-12: BRANCH_DISCIPLINE`| Every sprint lives on `ai-sprint/[ID]`, created in `matrix_workflow.md` Phase 3 before the first commit and pushed (never to `main`) in `close_workflow.md` Phase 5. Only `deployment_workflow.md` Phase 1 may merge a sprint branch into `main`/upstream. Direct commits or pushes to `main` during `Monitored Execution` are PROHIBITED. |

## 8. Supply Chain Security

| Category | Rule (Key) | Value / Constraint (Value) |
| :--- | :--- | :--- |
| **Package Manager** | `requirement` | Mandatory use of `pnpm 11+`. `npm` and `yarn` are prohibited for installation. |
| **Installation** | `ignore_scripts` | `ignore-scripts=true` MUST be active in `.npmrc`. |
| **Release Safety** | `min_release_age` | `minimum-release-age=1440` (24 hours) MUST be enforced to avoid zero-day compromised packages. |
| **Audit** | `only_built_deps` | All dependencies requiring build scripts MUST be explicitly whitelisted in `onlyBuiltDependencies`. |
