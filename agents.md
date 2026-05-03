# .agents Global Context & Governance Rules

This is the constitutional matrix of Universal-Agents (`.agents`).
It dictates in an absolute and transversal manner the behavior of subagents, code quality, and topological design.

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
| **Language** | `user_chat` | Spanish strictly confined to human-agent textual chat |
| **Language** | `technical_clarity` | Avoid redundant greetings. Prioritize Markdown Tables. Restrict Mermaid/ASCII. |
| **Language** | `restrictions` | Define explicitly what is prohibited. Avoid vague positive actions. |

## 2. Autonomy, Efficiency, and Execution

| Category | Rule (Key) | Value / Constraint (Value) |
| :--- | :--- | :--- |
| **Security** | `triple_lock` | Blockade until: 1. `ACTIVE` Roadmap, 2. `DEPLOYMENT_READY: PASSED`, 3. Explicit user authorization. |
| **Context** | `token_saver` | >200 lines files MUST NOT be fully dumped. Native file-read functions BANNED for massive targets. |
| **Context** | `ast_skeleton` | For large architectures, exclusively invoke `omni_minimizer.py` to extract classes/headers. |
| **Context** | `anti_amnesia` | After 10 interactions or 5,000 tokens, mandate re-reading `agents.md` and `active_state.json`. |
| **WIP Safety** | `pre_shielding` | Abort if `git status --porcelain` returns unresolved differences. |
| **WIP Safety** | `destructive_flags` | Condition/reject massive modifications/deletions unless `// turbo` token is in the prompt. |
| **Isolation** | `jurisdictional_lock` | Limit structural editing to `1` single physical file per instantiated subagent task. |
| **Isolation** | `no_interference` | Abort operation if `task_scope.md` shows the target file listed by another subtask in progress. |

## 3. Architecture and Topology of the Project

| Category | Rule (Key) | Value / Constraint (Value) |
| :--- | :--- | :--- |
| **Matrix** | `federation` | Check `git remote`; isolate `.agents` purely as a *Git Submodule*. |
| **Matrix** | `strict_rule` | Prohibited to alter internal architecture of this submodule from tactical injections. |
| **Environment** | `no_globals` | Cap or reject global injections in the main OS binary. |
| **Environment** | `dependencies` | Force explicit prefix syntax by invoking commands through isolated local dev environment. |
| **Infrastructure**| `trinity_standard` | Skills MUST adhere to: 1. `README.md`, 2. `SKILL.md`, 3. `/scripts/` with `__init__.py`. |
| **Infrastructure**| `topological_order`| Skills flat inside `skills/`. Sub-layers (`core/`, `local/`) PROHIBITED. External skills MUST use `-3rd` suffix. System interfaces & bridges reside at active root. |
| **Infrastructure**| `enforcement` | `mass-standardizer` tool is the official auditor for this standard. |
| **Infrastructure**| `secret_sovereignty`| BANNED from reading `.env` into memory. Use environment export commands. Throw Manual Correction Alert if missing. |
| **QA Framework** | `local_testing` | Overwrite native URLs to instantiate in RAM (`sqlite:///:memory:`). Reject DB connection. |

## 4. Memory Management and Feedback Loop

| Category | Rule (Key) | Value / Constraint (Value) |
| :--- | :--- | :--- |
| **Amnesia** | `ephemeral_memory` | Write `.md` log strictly in the project's *namespace* subdirectory documenting bug resolutions before session wipe. |
| **Amnesia** | `pre_wipe` | Physically check existence of referenced `.md` file before altering status to `CLOSED_SUCCESSFULLY`. |
| **Feedback Loop** | `constitutional_escalation`| Demand `Governance Learner` to audit sprint namespace and propose formal updates to `agents.md` if systemic patterns emerge. |
| **Feedback Loop** | `definitive_amnesia` | Permanently delete temporary logs of audited namespace exactly when rule is inserted into `agents.md`. |
| **Index Routing** | `index_files` | Parse exclusively `memory_index.json` locally. Reject listing directories or mass reading raw `.md`. |
| **Index Routing** | `single_line_breakdown`| Reject JSON insertions that break the 1-sentence limit without a carriage return (`\n`). |

## 5. Central Base (Project Master Index)

| Category | Rule (Key) | Value / Constraint (Value) |
| :--- | :--- | :--- |
| **Initialization** | `mandatory_topology` | Reject init if `/docs/` tree missing. Summon `Matrix Mapper` for `[layer]/[app]/` hierarchy. Sprints/Roadmaps/Active State MUST remain in root folders. |
| **Initialization** | `sovereignty_overwrite` | `Matrix Mapper` MUST exhaustively migrate/homologate legacy dissident nomenclatures before eradicating them. |
| **Nucleus Guard** | `nucleus_neutrality` | Automatic structural scaffolding / Hook Protocol PROHIBITED if workspace is `.agents` core. |
| **Nucleus Guard** | `isolation_constraint` | Verify not in governance nucleus before instantiating `/docs/` tree in parent dir. |
| **Traceability** | `state_anchor` | Scope MUST be extracted exclusively from `/docs/active_state.json` at workspace root. Secondary `.agents/docs/` files are ignored tactically. |
| **Traceability** | `state_homologation` | Creating state-tracking files/dirs/logs outside `/docs/active_state.json` is PROHIBITED. |
| **Traceability** | `historical_log` | Reject pushes without `#02x` suffix (Sprint ID) in commits. Apply Conventional Commits. |
| **MCP Registry** | `discovery_manifest` | `mcp-config.json` is the single point of discovery for MCP servers. |
| **MCP Registry** | `sync_rule` | Any new server in `mcp_servers/` MUST be reflected in `mcp-config.json`. |

## 6. Chain of Command & Core Workflow (Matrix V2)

The Matrix operates under a rigid, highly militarized sequential pipeline. Role usurpation is strictly prohibited. Subagents cannot bypass the Principal Agent.

| Category | Rule (Key) | Value / Constraint (Value) |
| :--- | :--- | :--- |
| **Subagent Roles** | `principal_agent` | Supreme Coordinator. Does NOT code. Manages Golden Gate, orchestrates handoffs. |
| **Subagent Roles** | `orchestrator` | Tactical Architect. Analyzes workspace, drafts initial Sprint Roadmap. |
| **Subagent Roles** | `agent_orchestrator`| HR/Staffing. Assigns specific subagents to Sprint Roadmap steps. |
| **Subagent Roles** | `skill_architect` | Tool Synthesizer. Prepares/injects executable skills/scripts needed for sprint. |
| **Subagent Roles** | `rule_validator` | Governance Sentinel. Audits `/rules`, creates/indexes structural norms. |
| **Subagent Roles** | `qa_agent` | Structural Verifier. Validates code standards, syntax, constitutional adherence. |
| **Subagent Roles** | `tester_agent` | Functional Verifier. Writes/runs tests, ensures logic stability/zero regression. |
| **Execution Phase**| `0_amnestic_anchor` | Subagents MUST initialize Zero-Memory, read `agents.md` first, operate inside `task_scope.md`. |
| **Execution Phase**| `1_tactical_blueprint` | Orchestrator drafts unassigned Sprint Roadmap -> delivers to Principal Agent. |
| **Execution Phase**| `2_master_assembly` | Principal Agent summons council to harden plan, compiles physical `sprint_blueprint.md`. |
| **Execution Phase**| `3_golden_gate` | Principal Agent requests explicit Human OK before execution. |
| **Execution Phase**| `4_monitored_execution`| Execution undergoes Double-Gate Review (QA + Tester). Remediation loop internal. Marks completed after success. |
| **System Bridges** | `slash_sovereignty` | Workflows in `workflows/` MUST have slash command alias via `slash-commander`. |
| **System Bridges** | `hook_sovereignty` | Critical automation via Claude Hooks MUST be registered in `hooks/` layer. |

## 7. Jurisprudence (Heuristic Amendments)

This section contains rules automatically promoted from the Heuristic Governance Loop. These rules have been vetted by operational frequency and are binding for all agents until formally integrated into the core constitution.

> [!NOTE]
> No amendments have been promoted yet. The Matrix is currently in a state of constitutional purity.

| Category | Rule (Key) | Value / Constraint (Value) |
| :--- | :--- | :--- |
| **Amendment** | `J-01: ENVIRONMENT_VIOLATION`| Agent MUST attempt autonomous remediation EXCEPT if prohibited (Manual Correction Alert). Source: `on_init`. |
| **Amendment** | `J-02: LAZY_SIGNAL_PARADIGM` | Prevent circular deps in Django `signals.py`: local imports in receiver, lazy sender string. Source: Sprint 028. |
