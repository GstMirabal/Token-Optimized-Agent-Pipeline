# .agents Global Context & Governance Rules

This is the constitutional matrix of Universal-Agents (`.agents`).
It dictates in an absolute and transversal manner the behavior of subagents, code quality, and topological design.

## 1. Code, Dialect, and Style

### Nomenclature and Linters
- **Python**: Validate against PEP 8: `snake_case` for variables/functions, `PascalCase` for classes.
- **JS/TS**: Validate strict use of `camelCase`.
- **Tools**: Execute `ruff check .` (Python) or `npm run lint` (JS/TS). Reject if the *exit code* > 0.

### Typing and Documentation
- **Types**: Demand *type hints* on every argument and return value of added or manipulated functions.
- **Documentation**: Document using *Google Style* (`Args:`, `Returns:`) in Python and *JSDoc* (`@param`, `@returns`) in JS/TS.
- **Ephemeral Markers**: Check regex for `TODO` or `FIXME`. Reject final implementations if matches are found.

### Complexity and Structure
- **Cognitive Limits**: Reject logical blocks with > 3 levels of nested indentation or > 50 total lines per function.
- **Paths**: Reject absolute disk paths; demand the use of relative paths or dynamic libraries.
- **Error Trapping**: Prohibit `except Exception:` block followed by `pass`. Demand explicit logging of the caught exception.

### Language, Communication, and Restrictions
- **Language Isolation**: Prohibit the use of Spanish in variables, code logic, terminal commands, or commit messages. Its rendering is strictly blocked and confined exclusively to the textual chat in the prompt.
- **Technical Clarity**: Avoid redundant greetings. Prioritize Markdown Tables formatting for mapping data and logical variables. Restrict invocations of complex graphics (Mermaid) or flows (ASCII Tree) strictly to what is indicated and enabled by the `.md` regulations of each subagent.
- **Negative Restrictions**: Define explicitly and solely what is prohibited to the LLM. Avoid requesting vague positive actions.
- **Technical Language Sovereignty**: Technical artifacts, workflow protocols, and agent profiles MUST be written in **Technical English** to ensure cross-node interoperability and linguistic precision. Spanish is strictly confined to the human-agent textual chat.

## 2. Autonomy, Efficiency, and Execution

### Triple Lock Security
Total blockade of local operations and deployments until simultaneously validating:
1. Roadmap in `ACTIVE` state.
2. Logging of the `DEPLOYMENT_READY: PASSED` token.
3. Explicit user authorization in the prompt.

### Context Optimization & Compression
- **Token-Saver Mandate**: Files evaluated with a size greater than 200 lines MUST NOT be dumped entirely into active LLM context. Agents are **CONSTITUTIONALLY BANNED** from using native standard file-read functions on massive targets.
- **AST Skeleton Enforcement**: To interpret large architectures, the Agent MUST exclusively invoke `skills/omni-context-minimizer/scripts/omni_minimizer.py` to extract structural classes and headers before any other tactical operation.
- **Anti-Amnesia**: After 10 interactions or surpassing 5,000 processed tokens, execute mandatory re-reading of this base document and the active state anchor.

### WIP Safety Freeze
- **Pre-Shielding**: Abort the editing process early if executing `git status --porcelain` returns unresolved local differences.
- **Destructive Flags**: Condition and reject massive modifications or general deletions unless textual verification of the `// turbo` token is provided in the context request.

### Agent Isolation
- **Jurisdictional Lock**: Limit and strictly cap structural editing to `1` single physical file per instantiated subagent task.
- **No Interference**: Avoid logical access in parallel, aborting the operation if the index (`task_scope.md`) shows the file listed by another subtask in a progress state.

## 3. Architecture and Topology of the Project

### The `.agents` Matrix
- **Federation**: Check `git remote`; isolate `.agents` by managing it purely as a *Git Submodule*.
- **Strict Rule**: Prohibited to alter the internal architecture of this governance submodule from tactical injections of the parent project.

### Isolated Environment
- **No Global Variables**: Cap or reject global injections in the main OS binary.
- **Dependency Containment**: Force explicit prefix syntax by invoking commands through an isolated local development environment.

### Infrastructure
- **Arsenal Sovereignty & Trinity Standard**: Every skill registered in the matrix MUST strictly adhere to the Trinity Standard:
    1. **`README.md`**: Institutional overview.
    2. **`SKILL.md`**: Procedural logic and YAML frontmatter.
    3. **`/scripts/`**: Executable logic with `__init__.py`.
- **Topological Order**: The Arsenal (Skills) MUST be mapped directly inside the `skills/` umbrella as a flat hierarchy. Sub-layers mapping origin (like core/ or local/) are strictly **PROHIBITED**. However, maintaining source transparency is legally binding: ANY skill or tool originating from a third-party, vendor, or external fork MUST possess the `-3rd` suffix in its directory name (e.g., `skill-creator-3rd`). System interfaces (`agents/`, `memory/`, `workflows/`, `rules/`) and bridging infrastructure (`mcp_servers/`, `hooks/`, `commands/`, `docs/`) reside directly at the active root.
- **Enforcement**: The `mass-standardizer` tool is the official auditor for this standard.
- **Secure Secret Sovereignty**: Agents are strictly prohibited from reading or parsing secret-holding files (e.g., `.env`) into their contextual memory. Their interaction is limited exclusively to invoking **environment export** commands. Any missing secret MUST trigger a **Manual Correction Alert** to the user, prohibiting autonomous deduction or bypass.

### QA Framework
- Overwrite the native URLs of local testing to instantiate in RAM, purifying between tests using `sqlite:///:memory:`. Reject DB connection.

## 4. Memory Management and Feedback Loop

### Amnesia Protocol
- **Ephemeral Memory**: Write a `.md` log strictly in the project's *namespace* subdirectory (e.g., `.agents/memory/core/`) documenting bug resolutions, prior to the end-of-session wipe.
- **Pre-Wipe**: Physically check the existence of the referenced `.md` file in said namespace prior to altering metadata to `CLOSED_SUCCESSFULLY`.

### Feedback Loop (Jurisprudence vs Constitution)
- **Constitutional Escalation**: Demand the execution of the [Governance Learner](agents/governance_learner.md) to uniquely audit the *namespace* of the Sprint (e.g., `/memory/cryptobot/`). Propose formal updates to `agents.md` if systemic patterns emerge.
- **Definitive Amnesia**: Permanently delete the temporary logs of the audited *namespace* at the exact moment its unified rule is successfully inserted into `agents.md`.

### Memory Index Routing
- **INDEX Files**: Parse exclusively and dynamically the `memory_index.json` descriptor nested locally to the active *namespace*. Reject listing directories or mass reading raw `.md` content.
- **Single Line Breakdown**: Reject JSON insertions in the descriptors that break the dictatorial limit of one (1) literal sentence without a carriage return (`\n`).

## 5. Central Base (Project Master Index)

### Hook Protocol (Initialization)
- **Mandatory Topology**: Reject initialization if the standardized `/docs/` tree does not exist. The [Principal Agent](agents/principal_agent.md) will summon the [Matrix Mapper](agents/matrix_mapper.md) to instantiate its dictatorial `[layer]/[app]/` hierarchy.
    - **Governance Exemption**: Sprints, Roadmaps, and the Active State MUST remain in unified root folders (`/docs/sprints/` and `/docs/roadmaps/`) to preserve project-wide strategic sovereignty, avoiding partitioning by mission (backend/frontend).
- **Sovereignty and Overwrite**: If a host project presents dissident documentary tracking nomenclatures, the [Matrix Mapper](agents/matrix_mapper.md) must exhaustively migrate and homologate the existing information towards the new standard without omissions before eradicating the legacy formats.

### Nucleus Guard
- **Nucleus Neutrality**: Automatic structural scaffolding and Hook Protocol procedures are strictly prohibited if the current workspace is the `.agents` Matrix core.
- **Isolation Constraint**: Agents must verify they are not in the governance nucleus before attempting to instantiate a `/docs/` tree in the parent directory.

### Zero Coordinate and Traceability
- **State Focus (The Anchor)**: Every subagent will unconditionally extract its scope by exclusively reading the `/docs/active_state.json` file **at the workspace root**. Any secondary state files nested within submodules (e.g., `.agents/docs/`) MUST be treated as internal governance metadata and ignored for tactical execution.
- **State Homologation**: The creation of any state-tracking file, directory, or telemetry log outside the constitutional `/docs/active_state.json` anchor is strictly PROHIBITED.
- **Historical Log**: Reject pushes whose commit messages lack the hashtag suffix `#02x` (Sprint ID obtained from the respective active `.json`), rigidly applying *Conventional Commits*. All changes in this submodule MUST be indexed to the active Sprint.

### MCP Configuration Registry
- **Discovery Manifest**: The `mcp-config.json` file in the root acts as the official registry for all Model Context Protocol servers. It is the single point of discovery for AI clients (Claude, Cursor, etc.) to interface with the Matrix's technical skills.
- **Sync Rule**: Any new server added to `mcp_servers/` MUST be reflected in this manifest to maintain operational capability.

## 6. Chain of Command & Core Workflow (Matrix V2)

The Matrix operates under a rigid, highly militarized sequential pipeline. Role usurpation is strictly prohibited. Subagents cannot bypass the Principal Agent.

### 6.1. Subagent Roles (The Council)
- **[Principal Agent](agents/principal_agent.md)**: Supreme Coordinator. Does NOT code or execute. Reviews and validates macro-states, manages the Golden Gate (Human Authorization), and orchestrates the handoffs.
- **[Orchestrator](agents/orchestrator.md)**: Tactical Architect. Responsible exclusively for analyzing the workspace and drafting the initial **Sprint Roadmap**.
- **[Agent Orchestrator](agents/agent_orchestrator.md)**: Human Resources/Staffing. Assigns specific specialized subagents to the steps inside the Sprint Roadmap.
- **[Skill Architect](agents/skill_architect.md)**: Tool Synthesizer. Prepares and injects the executable skills/scripts needed for the sprint.
- **[Rule Validator](agents/rule_validator.md)**: Governance Sentinel. Audits `/rules`; creates and indexes missing topological or structural norms.
- **[QA Agent](agents/qa_agent.md)**: Structural Verifier. Validates code standards, syntax, and constitutional adherence post-execution.
- **[Tester Agent](agents/tester_agent.md)**: Functional Verifier. Writes and runs tests, ensuring logic stability and regression absence post-execution.

### 6.2. The Standard Execution Pipeline
**Phase 0: Amnestic Anchor (Cycle 0)**:
- Subagents MUST initialize with **Zero-Memory**. They will read `agents.md` as their absolute first operation.
- They operate inside a strict **Context Package** (`task_scope.md`) delivered by the Principal Agent.

**Phase 1: Tactical Blueprint**:
- The **Orchestrator** drafts the initial unassigned `Sprint Roadmap` and delivers it to the Principal Agent.

**Phase 2: Master Assembly**:
- The **Principal Agent** summons the auxiliary council (in isolated sessions) to harden the plan:
  1. `Agent Orchestrator` assigns the subagents contextually.
  2. `Skill Architect` defines/creates the tools required.
  3. `Rule Validator` creates any missing rules in `/rules`.
- The Principal Agent compiles these into a physical, unified `sprint_blueprint.md`.

**Phase 3: The Golden Gate**:
- The **Principal Agent** delivers the `sprint_blueprint.md` to the Human User and holds operations until explicit OK is granted.

**Phase 4: Monitored Execution & Remediation Loop**:
- The **Principal Agent** calls the executing subagent, delivering the isolated `task_scope.md`.
- Upon task completion, the artifact undergoes the **Double-Gate Review**: `QA Agent` checks standards, `Tester Agent` evaluates functionality.
- *Remediation Loop*: If rejected, the Principal Agent bounces the code back to the executing subagent for patching without bothering the Human.
- *Approval*: Only upon successful, bug-free closure does the Principal Agent request Human authorization to mark the step as completed.

### 6.3. System Bridges (Hooks & Commands)
- **Rule 113: Slash Sovereignty**: Every high-integrity operational workflow defined in `workflows/` MUST have a corresponding registered slash command alias for friction-less 'Instruction-to-Action' parity. The `slash-commander` skill is the authoritative engine for this synchronization.
- **Rule 114: Hook Sovereignty**: Critical automation via Claude Hooks MUST be registered in the `hooks/` layer. It defines Hooks as the "Enforcement Arm" of the Matrix during session initiation and commit phases.

## 7. Jurisprudence (Heuristic Amendments)

This section contains rules automatically promoted from the Heuristic Governance Loop. These rules have been vetted by operational frequency and are binding for all agents until formally integrated into the core constitution.

### 7.1 Historical Amendments
> [!NOTE]
> No amendments have been promoted yet. The Matrix is currently in a state of constitutional purity.

#### Clause J-01: ENVIRONMENT_VIOLATION
- **Heuristic Rule**: The agent MUST attempt autonomous remediation before reporting failure.
- **Manual Override**: The user HAS PROHIBITED autonomous remediation for this violation. Remediation MUST be a **Manual Correction Alert**.
- **Original Source**: `on_init`
- **Vetted Date**: 1775991625.0121827

#### Clause J-02: LAZY_SIGNAL_PARADIGM
- **Heuristic Rule**: To prevent circular dependencies in Django `signals.py`, model imports MUST be performed locally inside the receiver functions. Signal decorators MUST use lazy string references for the `sender` argument (e.g., `@receiver(post_save, sender='users.User')`).
- **Original Source**: `Sprint 028: Identity Hardening`
- **Vetted Date**: 1713091200.0 (2026-04-14)
