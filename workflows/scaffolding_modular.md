---
description: "Multiple Modular Scaffolding (Dynamic Generation and Configuration of Projects)"
version: 1.0.0
---

# 🏗️ Workflow: Modular Scaffolding (Dynamic Scaffolding)

This is the **Master Protocol** for initializing any new repository. It ensures that project requirements are permanently recorded in cache, complying with the [Token-Saver] savings requirement, and installs the physical topology under the laws of the Constitution [Phases 1 and 2].

The assigned agent MUST follow this sequence in order:

## Phase 1: Ecosystem Interrogation (Mentor Mode)

The Mentor interrogates the Director (the user) to define 4 technological pillars:
1.  **Base Technology:** Python (Data/Backend) or Node/JS (Frontend/Fullstack)? Which exact framework (e.g., Django, FastAPI, React, NextJS)?
2.  **Dependency Manager:** For Python (`venv` + `requirements.txt`, `poetry`, or `uv`)? For JS (`npm`, `yarn`, `pnpm`)?
3.  **Persistence / Docker:** Will a database be set up in `docker-compose.yml` (e.g., PostgreSQL, Redis)?
4.  **Formatters/Linters:** (e.g., `ruff`, `black`, `eslint`).

## Phase 2: Cache Shielding (Token Saving)

Any project born from this Workflow MUST shield its immediate dependencies so that future tactical agents do not blindly scan the project wasting hundreds of thousands of tokens:
- **Action:** The Orchestrator creates a `project_stack.md` file (or injects it directly into the mandatory cache `.agent_state/session_{UID}/context.md`) detailing the Ecosystem, the Root Path, the installed DB, and the Testing Commands chosen in Phase 1.
- *Token-Saver Note:* No one reads this repository from scratch anymore. The cache is consulted.

## Phase 3: Physical Topology Deployment

Based on Phase 1 and the `project_mapping_and_context.md` file, the Orchestrator executes sequentially (*using atomic terminal commands in bash separated by SafeToAutoRun* if applicable):

1.  **Directory and Propagation:**
    - Perform `mkdir` for the project subfolder and `cd` into it.
    - **ABSOLUTE LAW (Git Submodules):** Execute initial `git init`, followed immediately by `git submodule add <URL_OR_ROOT_SYSTEM_PATH>/.agents .agents` to link the constitutional framework without breaking the chain of global updates.
2.  **Topology (Src Layout):**
    - Create `/src`, `/tests`, `/data/output`.
    - Create `/logs` (Pure traces) and `.gitignore` (mandatory blocking of `.DS_Store`, `.agent_state/`, `/venv/`, `.env`, and `/data/`).
3.  **Sandbox (Virtual Sandbox):**
    - Python: Instantiate `./venv/` and shield it. Configure the `.python-version` file.
    - Node: Execute `npm init -y` or the shielded equivalent, leaving the `node_modules` directory.
4.  **The Human Orchestrator (Makefile):**
    - Draft a `Makefile` (or `Taskfile`) instantiating common dependencies (`test`, `lint`, `db-up`) and **mandatory** add the `make sync-ai` alias that asynchronously invokes `git submodule update --remote` so the human can update the AI's logical framework with one click.
5.  **Data Shielding (Docker):**
    - If a DB was chosen, inject the `docker-compose.yml` file with the volume mapping forced to `./.docker-db-data`.

## Phase 4: Closing with Audit

- The Orchestrator asks the 3 Auditors (Dual Constitutional + Project, and Token-Saver) to verify the generated tree without consuming context, only reviewing `project_stack.md`.
- Present the final Git instantiation command (`git init && git add . && git commit -m "chore: init modular scaffolding"`) for the human to press the Final Approval Button.
