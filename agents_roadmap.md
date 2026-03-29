# 🗺️ Configuration Roadmap for the `.agents` Repository

This roadmap is designed to configure Universal-Agents step-by-step, ensuring it perfectly adapts to your workflow and local development repositories on any OS.

The idea is to verify each phase one by one.

## Phase 1: Global and Behavioral Rules (User Rules)
**Objective:** Establish a hyper-personalized foundation of how you want me to work, communicate, and which architectural and development standards you prefer me to always use. This acts as the "main brain" of our interactions.

### 1.1 Coding and Quality Standards:
- [x] Define naming conventions (Snake case, Camel case, Pascal case) for variables, classes, modules, and constants.
- [x] Select default linters or formatters for each language (e.g., Python: `black`, `ruff`, or `flake8`; JS/TS: `eslint`, `prettier`).
- [x] Define expectations for strict typing (e.g., Do we force the use of `typing` in Python or strict TypeScript?).
- [x] Establish cognitive complexity thresholds: When should I suggest refactoring a large function?
- [x] Preferences on error handling (Aggressive Try/Except, custom exceptions, Option/Result patterns).

### 1.2 Environment and Architecture Rules:
- [x] Define standard paths or conventions where you usually save projects and scripts (e.g., everything in `~/Developer`).
- [x] Regulations for virtual environments: Do we always use `venv`, `poetry`, `pipenv`, or `conda`? Where are they saved (inside the project or centrally)?
- [x] Standards for dependency management (`requirements.txt`, `pyproject.toml`, etc.).
- [x] Base architecture organization: MVC patterns, clean architectures, or sequential scripts? (Especially for your data transformers).

### 1.3 Universal-Agents Behavior and Communication:
- [x] Tactical Delegation and Code Quarantine Rules: Self-approval blocking and strict prohibition of generating extensive blocks during the Mentor role.
- [x] Establish Documentation vs. Code Language (e.g., Code, variables, and commits in **English**, explanations and high-level comments in **Spanish**).
- [x] Level of detail in explanations: Direct technical answers or step-by-step didactic explanations?
- [x] Response format: Extensive use of Mermaid diagrams, comparative tables, or simple Markdown lists?
- [x] Limit the use of third-party libraries (e.g., always prefer the Python standard library before suggesting a new dependency unless there is a good reason).

### 1.4 Testing, Git, and Deployment:
- [x] Commit conventions: (e.g., Use Conventional Commits like `feat:`, `fix:`, `chore:`).
- [x] Testing Standards: Do we use `pytest`, `unittest`? Do we require a minimum % of coverage before closing a module?
- [x] How do we handle sensitive data or passwords in scripts? (e.g., Mandatory use of `.env` files or secret managers).

## Phase 2: Project Mapping and Topology (Physical Structure)
**Objective:** Teach Universal-Agents the exact topology and repository boundaries so it operates without destroying the Mac's native environment.
- [x] Define the Src-Layout isolation structure (`/src`, `/tests`, `/data`), separating code from heavy data (Git LFS).
- [x] Centralize commands with a Shortcut Orchestrator (Makefiles instead of blind bash commands).
- [x] Establish the native Virtual Environment rule (`/venv/`) with strict binary execution (`./venv/bin/python`).
- [x] Container Shielding: Force the use of Docker-Compose for Databases (PostgreSQL) with local retention in `.docker-db-data`.
- [x] Isolate the database from Unit Tests (in-memory Test DB Segregation) so that the AI's QA does not delete your real data.

## Phase 3: Supreme Subagent Architecture (Zero-Trust Framework)
**Objective:** Build a militarized multi-agent AI that operates autonomously over your code using unbreakable physical boundaries, preventing API Loops and collisions.
- [x] Design the 6-Step Operational Flow (Mentor > Orchestrator > Auditor > Human Authorization > Executing Matrix > Rollback).
- [x] Executing Matrix (Ad-Hoc Cached Scanning): Dynamic instantiation of sub-agents based on pre-cached local scanning (`.agent_state/context.md`) and physical segregation (1 file = 1 agent).
- [x] Dual Supervision (Self-Improvement vs. Local): Segregation of the Auditor agent into a master constitutional update profile vs. a read-only project supervisor.
- [x] Token-Saver Audit (Economist): Deployment of an "Efficiency Auditor" in Phase 3, standardized to tear down plans that cause unnecessary waste of tokens and context window.
- [x] Transactional Control: Manual Atomic Commits upon success, combined with Git Branch Isolation (`ai-sprint/task`), or absolute Rollback preserving untracked humans (WIP Safety Freeze).
- [x] RCE and PII Security: LLM prohibition of raw ingestion of sensitive data (`view_file CSV`) or OS libraries (`os.system`). Mandatory masked scripting (Traceback Sanitization).
- [x] Constitutional Supremacy: Session UID isolation of orchestrators (`.agent_state/uid/`) making cross-minds impossible, and unbreakable supremacy of base rules over future *Skills*. AST cognitive limit against massive files.

## Phase 4: Creation of Workflows and Skills (Skills)
**Objective:** After building an unbreakable engine (Phases 1-3), we now build its *Tactical Manuals*. The Director invokes custom commands and the Orchestrator executes under pre-approved rules accelerating weekly tasks.
- [x] Design Workflow 1: Scaffolding (Absolute Scaffolding). Interactive routine or base file to initialize the `src/` base, the `.env`, and the Docker environment all at once under Phase 1 and 2 rules.
- [x] Design Skill 1: *Omni Context Minimizer*. Tactical substitution of the Data Cleaner to prioritize universal extraction of *Abstract Syntax Trees* and save context bloating in massive repositories. The Data Cleaner is postponed on demand.
- [x] Define safe technical triggers (Triggers) to use autonomy delegations instantly (`// turbo`) without destroying governance or Base data.
- [x] Implement MCP Registry: Standardize the indexing of Model Context Protocols (MCP) inside the `.agents/skills/` matrix so the Orchestrator can statically route and assign remote/local server contexts.

## Phase 5: Knowledge Consolidation (Knowledge Items)
**Objective:** Cure the "AI Alzheimer's Syndrome" by providing it with a Long-Term Brain external to your user repos.
- [x] Automate or order the Orchestrator to extract heuristic lessons, discovered workarounds for exotic libraries, or post-sprint bug fixes.
- [x] Dictate format and temporary hosting in `.agents/knowledge/` before the Orchestrator wipes (Total Amnesia) its temporary operational memories at the end of a *Sprint*.
- [x] Implement the Token-Saver KI Index Architecture: Utilize a `ki_index.json` to store 1-line semantic summaries, routing the Orchestrator to atomic, modular `.md` files without polluting the context window.

---
**Mission Accomplished / Maintenance Mode**
With 5/5 phases shielded applying the *Zero-Ambiguity* framework, the tactical arsenal online, and the *Amnesia Protocol* (Knowledge Items) functioning, the Universal-Agents architecture is officially **COMPLETED and PRODUCTION-READY**.

From here, this repository enters Maintenance Mode. Any further enhancements to `.agents/` must strictly pass through the constitutional **Auditor Agent** and be committed via *conventional commits* to ensure all derived local projects (`git submodules`) safely inherit the upgrades without collision.
