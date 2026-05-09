# .agents Global Context & Governance Rules

This is the constitutional matrix of Universal-Agents (`.agents`).
It dictates in an absolute and transversal manner the behavior of subagents, code quality, and topological design.

## 0. Zero Coordinate Protocol (Documentation Matrix)

| Rule | Value / Constraint |
| :--- | :--- |
| **Matrix Entry** | Every session MUST start by reading `docs/0_SYSTEM_OVERVIEW.md`. |
| **Hierarchy** | `arch/` (Law), `roadmaps/` (Future), `walkthroughs/` (Achievements), `sprints/` (History). |
| **Traceability** | Every module MUST have a `[MODULE]_BLUEPRINT.md` in `arch/` before coding. |
| **Execution** | Every task must be recorded in the current Sprint folder. |
| **Certification** | Closing a Sprint requires updating Blueprints, Global Roadmap, and Walkthroughs. |

## 1. Code, Dialect, and Style

| Category | Rule (Key) | Value / Constraint (Value) |
| :--- | :--- | :--- |
| **Python** | `naming_convention` | `snake_case` (vars/funcs), `PascalCase` (classes) |
| **Python** | `linter_command` | `ruff check .` (Reject if exit code > 0) |
| **JS/TS** | `naming_convention` | `camelCase` |
| **JS/TS** | `linter_command` | `npm run lint` (Reject if exit code > 0) |
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
| **Context** | `token_saver` | >200 lines files MUST NOT be fully dumped. Native file-read functions BANNED. |
| **Context** | `ast_skeleton` | For large architectures, exclusively invoke `omni_minimizer.py` to extract classes. |
| **Context** | `anti_amnesia` | Mandate re-reading `agents.md` and `active_state.json` at every execution conclusion. |
| **WIP Safety** | `pre_shielding` | Abort if `git status --porcelain` returns unresolved differences. |
| **WIP Safety** | `destructive_flags` | Reject massive modifications/deletions unless `// turbo` token is in the prompt. |
| **Isolation** | `jurisdictional_lock` | Limit structural editing to `1` single physical file per instantiated subagent task. |
| **Isolation** | `no_interference` | Abort if `task_scope.md` shows the target file listed by another subtask in progress. |

## 3. Architecture and Topology of the Project

| Category | Rule (Key) | Value / Constraint (Value) |
| :--- | :--- | :--- |
| **Matrix** | `federation` | Check `git remote`; isolate `.agents` purely as a *Git Submodule*. |
| **Matrix** | `strict_rule` | Prohibited to alter internal architecture of this submodule from tactical injections. |
| **Environment** | `no_globals` | Cap or reject global injections in the main OS binary. |
| **Environment** | `dependencies` | Force explicit prefix syntax by invoking commands through isolated local dev environment. |
| **Infrastructure**| `trinity_standard` | Skills MUST adhere to: 1. `README.md`, 2. `SKILL.md`, 3. `/scripts/` with `__init__.py`. |
| **Infrastructure**| `topological_order`| Skills flat inside `skills/`. Sub-layers (`core/`, `local/`) PROHIBITED. |
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

## 5. Central Base (Project Master Index)

| Category | Rule (Key) | Value / Constraint (Value) |
| :--- | :--- | :--- |
| **Initialization** | `mandatory_topology` | Reject init if `/docs/` missing. Instantiate `docs/[Sprint_ID]-[Stack]-[Layer]/`. |
| **Initialization** | `legacy_onboarding` | If mature project: Execute **Full Reverse Engineering** and generate Walkthroughs. |
| **Nucleus Guard** | `nucleus_neutrality` | Automatic structural scaffolding PROHIBITED if workspace is `.agents` core. |
| **Traceability** | `state_anchor` | Context MUST be extracted from `docs/active_state.json` (Zero Coordinate). |
| **Traceability** | `state_homologation` | Creating state-tracking files outside `docs/active_state.json` is PROHIBITED. |
| **Traceability** | `historical_log` | Reject pushes without `#02x` suffix. Apply Conventional Commits. |
| **MCP Registry** | `discovery_manifest` | `mcp-config.json` is the single point of discovery for MCP servers. |

## 6. Chain of Command & Core Workflow (Matrix V3)

The Matrix operates under a rigid, highly militarized sequential pipeline. Role usurpation is strictly prohibited.

| Category | Rule (Key) | Value / Constraint (Value) |
| :--- | :--- | :--- |
| **Subagent Roles** | `principal_agent` | Supreme Coordinator. Creates Implementation Plan, manages Golden Gate. |
| **Subagent Roles** | `devops_agent` | Environment Guardian. Manages venv, .env export, and Docker health. |
| **Subagent Roles** | `orchestrator` | Tactical Architect. Drafts Initial Roadmap and instantiates Sprint Hierarchy. |
| **Subagent Roles** | `agent_orchestrator`| HR/Staffing. Assigns specific subagents to the Initial Roadmap steps. |
| **Subagent Roles** | `skill_architect` | Tool Synthesizer. Prepares/injects skills for the assigned subagents. |
| **Subagent Roles** | `rule_validator` | Governance Sentinel. Audits Roadmap and generates the `task_scope.md`. |
| **Subagent Roles** | `qa_agent` | Structural Verifier. Validates code standards (Ruff, ESLint). |
| **Subagent Roles** | `tester_agent` | Functional Verifier. Ensures logic stability and zero regression. |

### 🚀 The Execution Pipeline (Matrix V3)
1.  **Strategic Genesis**: Principal Agent drafts Implementation Plan -> Human Consensus.
2.  **Environment Readiness**: DevOps Agent activates `venv`, exports `.env`, and checks Docker/DB health.
3.  **Tactical Blueprint**: Orchestrator drafts Initial Roadmap and instantiates `docs/sprints/[ID]/`.
4.  **Master Assembly**: Principal Agent summons the Council (Agent Orch, Skill Arch, Rule Val) to finalize the plan.
5.  **Golden Gate**: Principal Agent requests explicit Human OK before execution.
6.  **Monitored Execution**: Subagents perform tasks with atomic LOCAL commits (no remote push) referencing the Sprint ID.
7.  **Quality Gate**: QA Agent and Tester Agent perform structural and functional verification.
8.  **Tactical Liquidation**: Closing process: Squash local commits into logical blocks, PUSH to remote, update Blueprints, Global Roadmap, Walkthroughs, and Master Ledger.

## 7. Jurisprudence (Heuristic Amendments)

| Category | Rule (Key) | Value / Constraint (Value) |
| :--- | :--- | :--- |
| **Amendment** | `J-01: ENVIRONMENT_VIOLATION`| Agent MUST attempt autonomous remediation EXCEPT if prohibited. |
| **Amendment** | `J-02: LAZY_SIGNAL_PARADIGM` | Prevent circular deps in Django `signals.py`: local imports in receiver. |
| **Amendment** | `J-03: HOTFIX_FLAT` | For critical bugs, use `docs/hotfixes/[H-ID]-[Layer].md`. |
| **Amendment** | `J-04: FULL_DEPLOYMENT` | Orchestrator MUST deploy the COMPLETE task hierarchy in a single atomic action. |
| **Amendment** | `J-05: TACTICAL_LIQUIDATION` | Mandatory update of Blueprints, Global Roadmap, Walkthroughs, and Ledger before closing. |
| **Amendment** | `J-06: IDENTITY_NAMING` | Standard Option B: All docs must be named `[MODULE]_[TYPE].md` (e.g. `USERS_BLUEPRINT.md`). |
| **Amendment** | `J-07: ARCHIVE_PURGE` | Prohibited to keep empty `archive/` folders. Purge immediately if found. |
| **Amendment** | `J-08: COMMIT_SQUASH` | Mandatory atomic local commits; mandatory squash & push only during Tactical Liquidation. |
