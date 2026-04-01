# Universal-Agents Global User Rules
Syntax, Quality, and Communication Rules.

## 1. Code and Dialect
- **Standard Nomenclature:** Use PEP 8 for Python (`snake_case` for variables/functions, `PascalCase` for classes, `UPPER_SNAKE_CASE` for constants) and native standards for JS/TS (`camelCase` for functions/variables).
- **Linters:** `ruff` (Python), `eslint/prettier` (JS/TS).
- **Typing:** Mandatory strict typing (`Type Hinting`, TypeScript).
- **Code Documentation:** Mandatory use of *Google Style Docstrings* for Python (`Args:`, `Returns:`) and *JSDoc* for JS/TS (`@param`, `@returns`).
- **Paths:** Prohibited use of absolute paths (hardcoded). Use dynamic `pathlib`.
- **Exception Handling:** Prohibited use of generic captures (`except Exception:`). Forcibly instantiate the specific exception at the source (e.g., `except ValueError:`). Prohibiting silencing errors with `pass`.
- **Output:** Use native `logging` (`INFO`, `ERROR`). Prohibited use of `print()` in production or automated operations.
- **Cognitive Complexity and Refactoring:** The Agent MUST trigger a "Refactoring Alert" in its report if it reviews a module whose code nesting depth is > 3 levels (`if` inside a `for` inside a `while`) or if functions exceed 50 lines.
- **Modularity (DRY):** Extract repetitive code into generic functions/classes.

## 2. Autonomy, Efficiency, and Zero-Trust
- **Imperative Token Saving (Raw Reading Prohibited):** It is **STRICTLY PROHIBITED** to read code files larger than 200 lines directly to understand their content. The agent **MUST** execute the universal `omni-context-minimizer` skill first to extract the structural skeleton, locate the exact line of interest in the terminal output, and only then proceed to isolate its reading to that segment. Ignoring this metric triggers an immediate tactical shutdown.
- **Code and Blackboard Language:** Technical English (variables, commits, `task.md`, `implementation_plan.md`).
- **Chat Language:** Spanish (explanations, debate with the user).
- **Mentor Role and Code Quarantine:** Phase 1 (Debate) is tactical and architectural. The Principal Agent is **prohibited** from injecting resolved code blocks larger than 10 lines into the chat during the discussion phase. Debate the ideas and submit a numbered list of steps to the user for execution.
- **Tactical Delegation:** Destructive operations (file deletion, database purging) or massive mutations are blocked. They require authorization or the explicit use of a *Workflow* with the `// turbo` flag.
- **External Skills Injection (`skills.sh`):** System acceleration is prioritized by integrating tools from the `skills.sh` master repository. **SECURITY LOCK:** Autonomous execution, download, or installation of any Skill by the Orchestrator is terminally prohibited. The AI must present the source link, the proposed content, and wait for the human to verify the source and manually authorize it.
- **Rule 21.1: Search-Before-Build Protocol:** It is MANDATORY for the Orchestrator to search the `skills.sh` master repository before proposing the creation of a new Native Skill. If a similar or superior tool exists in the master repository, the Agent MUST propose its integration instead of a new implementation. Creating a Native Skill is ONLY permitted if no suitable third-party equivalent exists or if specific project requirements justify an ad-hoc native tool.
- **Third-Party vs Native Skill Naming Convention:**
    - **`3rd-` Prefix:** MANDATORY for any Skill downloaded or integrated from a third-party source (e.g., `skills.sh`). This ensures clear auditability of external code origins.
    - **Native Skills (No Prefix):** Any Skill developed natively by the User or the AI within the framework during active sessions MUST NOT carry the `3rd-` prefix. They are considered core framework assets.
- **Mandatory Skill Utilization:** If a specialized Skill (e.g., `3rd-django-security`, `3rd-django-patterns`) is present in the repository, the Agent is **FORBIDDEN** from proposing or implementing code changes without first executing said Skill to audit the existing state or validate the proposed pattern. Skipping this step constitutes a major failure of the orchestration protocol.
- **Phase Auditing:** Before closing any task phase (e.g., "Phase 1"), the Agent MUST execute all pertinent auditor Skills (like `token-saver-auditor` or `3rd-django-verification`) to verify the implementation.
- **Domain Audit (Global vs Local):** Every proposed new Skill MUST pass the *3-Variable Amnesia Test*: If the tool survives functionally to the total destruction of the current project, it will be saved in the universal matrix (`.agents/skills/`). If its code is heavily coupled to the business logic or native client databases, it will be isolated outside the submodule in a local project directory (e.g., `/.local_skills/`) to never contaminate the global matrix.
- **Dependencies and Secrets (Global Governance):** Mandatory use of the native Standard Library as the first option. Any third-party dependency must be justified. **MANDATORY:** Export the `.env` file for all automated operations. **MANDATORY:** After any dependency update/install, execute the appropriate sync command for the chosen manager (e.g., `pip freeze > requirements.txt`, `uv pip compile`, `npm shrinkwrap`, `pnpm-lock.yaml` update) to maintain environment consistency across agents.
- **Implementation Artifacts:** All `implementation_plan.md` and `task.md` MUST be written in professional Technical English. They are stored in the `.agents/sprints/` directory following the naming convention `XXX-sprint-name.md`.
- **Master Task Index:** The root `.agents/task.md` MUST remain a clean Table of Contents (TOC) pointing to the active sprint.
- **Sprint Initialization Audit (Arsenal Check):** Every time a new sprint is initialized, after creating the mandatory root `.agents/task.md` entry and the corresponding `.agents/sprints/XXX-sprint-name.md` file, the Agent **MUST** perform a "Pre-Flight Arsenal Audit":
    1. **Skills Analysis:** Scan the `/skills/` directory and analyze if current tools are sufficient for the task.
    2. **Missing Skills Identification:** Identify if any specialized skill from the master repository or third-party is required to optimize performance.
    3. **Skill Assignment:** Formally assign the corresponding skills to the subagents in the `implementation_plan.md`.
    4. **MCP Provisioning:** Determine if a Model Context Protocol (MCP) server must be downloaded, started, or connected to provide extended context (DB schema, specialized APIs).

## 3. Governance and Directory Structure (Submodule Separation)
- **Persistent Global Metadata (`.agents/governance/`):** All persistent files related to agent behavior, roadmaps, project context, and long-term rules MUST be stored here. This is the **Shared Framework** (Read-Only for local projects).
- **Audit Exclusion:** The `.agents/governance/` directory is **EXCLUDED** from automated code audits.
- **Local Project-Specific Records (Ignored by Git):** To prevent polluting the global submodule repository, all project-specific task tracking and data MUST be stored in the following list of locations (strictly ignored by Git):
    - **`task.md`**: Master Task TOC (Local Index).
    - **`.agent_state/`**: Mandatory ephemeral session cache (AST, context, trace).
    - **`task/sprints/`**: Detailed tactical plans (`XXX-sprint-name.md`).
    - **`task/roadmaps/`**: Strategic roadmap history (Discovery & Ultimate Phases).
    - **`task/logs/`**: Ephemeral trace and debug logs.
- **Sprint Naming Convention:** Use `XXX-sprint-name.md` (e.g., `001-retrofitting-and-alignment.md`).
- **High-Value Deliverables (`docs/roadmaps/`):** While strategic roadmaps are kept in the local `roadmaps/` folder for AI tracking, the final architecturally-relevant documents MUST be mirrored or moved to the project's root `docs/` folder (outside the submodule) for permanent versioning in the main repository.

## 4. Roadmap Maturity and Execution Control
- **Roadmap Maturity Protocol (Safety Lock):** It is **FORBIDDEN** for the Agent to initialize a new Sprint (creating files in `task/sprints/` or entries in `task.md`) if the roadmap of the current Phase (within `task/roadmaps/`) is not finalized or is marked with a `safety_lock: LOCKED`.
- **Discovery First:** Before moving to execution, the Agent MUST ensure that all Milestones (M0, M1, etc.) of the current phase are fully defined, including their specific deliverables and technical constraints.
- **Lock Override:** The `safety_lock` can only be changed to `READY_FOR_EXECUTION` after a full Discovery Audit and explicit user agreement on the tactical scope.
