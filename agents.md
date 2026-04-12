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

### Context Optimization
- **Limited Reading**: Files evaluated with `wc -l` > 200 lines must not be dumped entirely. Demand reading using AST, `head`, `tail`, or `grep`.
- **Anti-Amnesia**: After 10 interactions or surpassing 5,000 processed tokens, execute mandatory re-reading of this base document and the central index.

### WIP Safety Freeze
- **Pre-Shielding**: Abort the editing process early if executing `git status --porcelain` returns unresolved local differences.
- **Destructive Flags**: Condition and reject massive modifications or general deletions unless textual verification of the `// turbo` token is provided in the context request.

### Agent Isolation
- **Jurisdictional Lock**: Limit and strictly cap structural editing to `1` single physical file per instantiated subagent task.
- **No Interference**: Avoid logical access in parallel, aborting the operation if the index (`task.md`) shows the file listed by another subtask in a progress state.

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
- **Topological Order**: Skills and system interfaces MUST be isolated into exactly four regulated layers: `core/`, `local/`, `3rd/`, and `mcp_servers/` (reserved explicitly for Model Context Protocol bridged architectures). Zero-tolerance for root-layer contamination outside these bounds.
- **Enforcement**: The `mass-standardizer` tool is the official auditor for this standard.
- **Secure Secret Sovereignty**: Agents are strictly prohibited from reading or parsing secret-holding files (e.g., `.env`) into their contextual memory. Their interaction is limited exclusively to invoking **environment export** commands. Any missing secret MUST trigger a **Manual Correction Alert** to the user, prohibiting autonomous deduction or bypass.

### QA Framework
- Overwrite the native URLs of local testing to instantiate in RAM, purifying between tests using `sqlite:///:memory:`. Reject DB connection.

## 4. Memory Management and Feedback Loop

### Amnesia Protocol
- **Ephemeral Memory**: Write a `.md` log strictly in the project's *namespace* subdirectory (e.g., `.agents/core/memory/core/`) documenting bug resolutions, prior to the end-of-session wipe.
- **Pre-Wipe**: Physically check the existence of the referenced `.md` file in said namespace prior to altering metadata to `CLOSED_SUCCESSFULLY`.

### Feedback Loop (Jurisprudence vs Constitution)
- **Constitutional Escalation**: Demand the execution of the [Governance Learner](core/agents/governance_learner.md) to uniquely audit the *namespace* of the Sprint (e.g., `/core/memory/cryptobot/`). Propose formal updates to `agents.md` if systemic patterns emerge.
- **Definitive Amnesia**: Permanently delete the temporary logs of the audited *namespace* at the exact moment its unified rule is successfully inserted into `agents.md`.

### Memory Index Routing
- **INDEX Files**: Parse exclusively and dynamically the `memory_index.json` descriptor nested locally to the active *namespace*. Reject listing directories or mass reading raw `.md` content.
- **Single Line Breakdown**: Reject JSON insertions in the descriptors that break the dictatorial limit of one (1) literal sentence without a carriage return (`\n`).

## 5. Central Base (Project Master Index)

### Hook Protocol (Initialization)
- **Mandatory Topology**: Reject initialization in a project if the standardized `/docs/` tree does not exist. The [Principal Agent](agents/principal_agent.md) will throw a _Halt_ and summon the [Matrix Mapper](agents/matrix_mapper.md) to instantiate its dictatorial `[layer]/[app]/` hierarchy.
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

## 6. Chain of Command

- **[Principal Agent](core/agents/principal_agent.md)**: Strategic authority. Sole entity empowered to sanction the master **Roadmap**.
- **[Orchestrator](core/agents/orchestrator.md)**: Tactical authority. Translates the approved Roadmap into a detailed **Implementation Plan** (which defines and constitutes the active **Sprint**).
- **[Agent Orchestrator](core/agents/agent_orchestrator.md)**: Meta-Governance authority. Responsible for **Staffing** the Implementation Plan by designating existing agents or **creating** new subagent profiles as required.
- **[Skill Architect](core/agents/skill_architect.md)**: Technical researcher and tool synthesizer. Responsible for the **Triangle of Sovereignty** (core/local/3rd) and tool benchmarking.
- **Constitutional Birthright**: Every subagent profile (`.md`) MUST include a **Mandatory Initiation Cycle** (Cycle 0) that forces the reading of `agents.md` before any operational logic is executed. No agent is valid or authorized to act without this constitutional anchor.
- **Workflow Lock**: No secondary or tertiary agent may initialize or execute if the [Principal Agent](agents/principal_agent.md) has not sanctioned the Roadmap, and if the [Orchestrator](agents/orchestrator.md) has not finalized the Implementation Plan. The [Agent Orchestrator](agents/agent_orchestrator.md) must certify the "Agent Ecosystem" readiness before execution begins.
- **Rule 113: Slash Sovereignty**: Every high-integrity operational workflow defined in `core/workflows/` MUST have a corresponding registered slash command alias for friction-less 'Instruction-to-Action' parity. The `slash-commander` skill is the authoritative engine for this synchronization.
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
