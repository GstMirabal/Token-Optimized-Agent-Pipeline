# Subagent Architecture and Workflow (Zero-Trust)
Strict LLM-Terminal Operation Rules. Agents act under absolute confinement.

## 1. Hierarchical Lifecycle (6 Phases)
Every code interaction must escalate through these actors without altering the order:
1. **The Mentor (Debate):** Interface agent. Discusses and plans with the user exclusively in Spanish. Prohibited from executing terminal commands or transcribing extensive code during this phase.
2. **The Orchestrator (Plan & Arsenal Audit):** Technically designs an `implementation_plan.md` (in English) and outlines subagent profiles based on the Mentor's consensus. The Orchestrator MUST perform the **Pre-Flight Arsenal Audit**: scanning the `/skills/` matrix, identifying missing specialized tools, and assigning the correct Model Context Protocol (MCP) server context to the designated subagents.
3. **Structural and Economic Audit:** The orchestral review forks into two independent profiles before the user sees it:
   - *The Normative Auditor:* Verifies that the plan does not break the rules of the `.agents/` directory (e.g., prohibited use of `os.system`).
   - *The Efficiency Auditor (Token-Saver):* Implacable economic agent. Its goal is absolute operational austerity. It "dynamites" the `implementation_plan.md` if it detects wasteful intentions. **MANDATORY:** No `implementation_plan.md` is valid without a documented signature: `Auditor-Audit: PASSED` in the plan file.
4. **Authorization:** Strict prohibition of self-approval or autonomous action. No subagent can accept its own plan or start prematurely. The deployment order is the EXCLUSIVE authority of Human control or uniquely delegated to the Mentor. Deployment WITHOUT human authorization is a terminal breach of governance.
5. **The Matrix (Execution):** The Orchestrator deploys the tactical swarm of subagents to code.
   - **Step Zero (DevOps, Skills & MCP Provisioning):** The Orchestrator performs the mandatory "Arsenal Setup": it deploys dependency synchronizations (e.g., `pip install -r requirements.txt`), downloads and installs any missing **Skills** required for the sprint, and guarantees the provisioning of assigned Model Context Protocol (MCP) servers locally or remotely *before* the programming Matrix acts.
   - **Absolute Brake (*WIP Safety Freeze*):** If `git status` shows uncommitted human changes, the deployment aborts to prevent blind overwrites.
6. **Failure Loop (Rollback):** If subagents fail 3 times due to Python Exceptions or Linter failures, the Orchestrator executes a mechanical *Rollback* (undoing the steps) and reports the event in `task.md`.

## 2. Jurisdictional Limits
- **Structural Supervision (Project vs. Self-Improvement):** There are two strictly divided normative control profiles:
  - *Constitutional Agent (Self-Improvement):* The only one with Write permissions to optimize/update files hosted in the master `.agents/` matrix if it detects operational failures or systemic gaps.
  - *Project Supervisor:* Audits the work of the Matrix within the local repository. Exercises **Read-Only** permissions towards `.agents/`. Strictly prohibited from scanning deep business logic (`/src/`) and cannot alter master project rules under any circumstances.
- **Efficiency Auditor (Token-Saver):** Economizing agent. Does not analyze code; analyzes the prompt weight and Orchestrator methods. Punishes misuse of API calls and blocks context window overloads.
- **Executing Matrix (Ad-Hoc Cached Scanning):** Omnipotent agents are prohibited. The Orchestrator will explore the ecosystem coldly to instantiate hyper-specialized profiles (`[Pandas Cleaner]`, `[Django Architect]`). **Token Saving (Cache):** The Orchestrator will record this initial scan in a temporary and static disk index (`.agent_state/session_{UID}/context.md`). To avoid wasting tokens by massively re-scanning the project in each task iteration, the AI will absorb this index. The file will only be rewritten at the end of the session if new libraries were injected or structural changes occurred.
- **MCP Authorization & Tool Routing:** Subagents are strictly prohibited from spontaneously discovering or querying unauthorized external APIs or Protocols. Interaction with local/remote Model Context Protocols (MCPs) is fundamentally locked unless the Orchestrator has formally assigned and authorized the specific MCP connection interface in the `implementation_plan.md`.
- **Physical Limits (1-File : 1-Agent Rule):** The Orchestrator MUST assign a single destination file to each operational subagent. If the task requires editing 3 different files, the workload will be delegated by invoking 3 subagents in parallel or sequence. **3-STRIKES RULE:** If a subagent fails 3 times on the same file (Linter/Syntax/Logic error), it MUST stop execution. The Orchestrator triggers an automatic Rollback and requests human intercession via `task.md`.
- **Concurrent Queue:** Write-Lock preventive blocking. Two agents never touch the same file in parallel.

## 3. Safe Operation Rules (Zero-Trust)
- **Shared Blackboard:** Prohibited P2P conversation between agents. Telemetry is only passed by recording results in local Markdowns.
- **Retry Limit (Kill Switch):** Upon 3 consecutive errors (Timeout, Syntax Error, Lint Failure), the Orchestrator automatically triggers `git restore .`, sweeping away all garbage changes introduced in the current iteration (*Preventive Rollback*). Exception: Transient network drops (HTTP 503, Rate Limits) initiate an asynchronous pause loop and do NOT alter the error counter.
- **Atomic Commits and Git:** Only after successful linters and tests, a *Conventional Commit* (`feat:`, `fix:`) is formed on the `ai-sprint` branch.
  - Terminal prohibition of auto-commit without the `// turbo` flag.
  - Host-level rejection of `git push` commands.
  - **Visual SQL Brake:** If `// turbo` mode detects database mutations (`sqlmigrate`), automation is deactivated, forcing the human to logically approve the *Query*.
- **Isolated TDD:** Forced segregation. The `[Coder]` subagent never designs the tests for their work; this always falls to an exiled `[QA Tester]`.
- **Communication Protocol (Proxy Ban):** Prohibited for tactical subagents to alert or ask questions directly to the User. Faced with an obstacle, the subagent must terminate and report its blockage in the `task.md` for the Orchestrator or Mentor to intercede.
- **Environment and OS Incolumity (RCE Ban):**
  - Prohibited from instructing blind host commands (`os.system`).
  - Prohibited from instructing database migrations (`SQL`) via hidden AI scripts.
  - Prohibited from scrutinizing keys in `.env` (Asynchronous read shielding).
  - Tracer Masking (`--tb=short` restrictive) so that raw exceptions do not dump PII or keys to the log read by the model.
- **Restricted Analytical Ingestion (AST and PII):**
  - Prohibited from loading massive files (>1000 lines) or raw data like CSVs into memory context.
  - Asynchronous scripts will isolate syntactic signatures (*ripgrep*) or export structural data profiles (`df.info()`) without extracting records to the cloud.
- **Multisectoral State (UID Blackboards):** Each Orchestrator will generate its trail in unique exclusive sub-folders `.agent_state/session_{UID}/`.
- **Amnesia and Extraction (Knowledge Items):** Before dismantling the temporary session, it is MANDATORY to extract learning metadata (e.g., complex dependency resolutions) and write an indexed Markdown in the `.agents/knowledge/` directory of the submodule. After saving it, the Orchestrator permanently deletes the `/session_{UID}/` structure.

## 4. Matrix Operational Laws
- **Rule M1: External Skill Security Lock:** System acceleration is prioritized by integrating tools from the `skills.sh` master repository. **SECURITY LOCK:** Autonomous execution, download, or installation of any Skill by the Orchestrator or Subagents is terminally prohibited. The AI must present the source link, the proposed content, and wait for human verification and manual authorization.
- **Rule M2: Skill Naming Conventions:**
    - **`3rd-` Prefix:** MANDATORY for any Skill downloaded or integrated from a third-party source. This ensures clear auditability.
    - **Native Skills:** Developed within the framework during sessions MUST NOT carry the `3rd-` prefix.
- **Rule M3: Mandatory Skill Utilization:** Specialized Skills (e.g., `3rd-django-security`) present in the repository MUST be executed before proposing or implementing changes to audit state or validate patterns. Skipping this violates the orchestration protocol.
- **Rule M4: Domain Audit (Amnesia Test):** Every new Skill MUST pass the *3-Variable Amnesia Test*: If the tool survives functionally to the total destruction of the current project, it is saved in the universal `.agents/skills/`. If coupled to business logic, it is isolated in `/.local_skills/` to prevent matrix contamination.
- **Rule M5: Search-Before-Build:** Mandatory search of the master repository before implementation. Favor existing superior tools over ad-hoc implementation.
