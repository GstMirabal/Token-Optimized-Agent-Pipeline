---
description: "Hierarchical Modular Scaffolding (Dynamic Generation with Constitutional Hardening)"
version: 2.0.0
---

# 🏗️ Workflow: Modular Scaffolding (Hardened)

This is the **Master Protocol** for initializing any new repository. It ensures that projects are born with **Hierarchical Governance**, **Arsenal Segregation**, and **Tactical Isolation** (Rules 1-78).

The assigned agent MUST follow this sequence in order:

## Phase 1: Ecosystem Interrogation (Mentor Mode)

The Mentor interrogates the Director (the user) to define the technological pillars:
1.  **Base Technology:** Language and Framework choice.
2.  **Dependency Manager:** `pip`, `npm`, `pnpm`, etc.
3.  **Infrastructure:** Docker setup and volumes.
4.  **Metadata Initiation:** Initialize `.agents/task.md` and the initial Sprint `001-base-initialization.md`.

## Phase 2: Cache Shielding & Phase 0 Baseline

- **Action:** Create `project_stack.md` (or inject into session context) detailing the Ecosystem.
- **Phase 0 Definition:** This stage is recorded as **Phase 0: Base Infrastructure & Environment**.
- *Token-Saver Note:* Use the scaffolding logic to prevent a project-wide scan on re-entry.

## Phase 3: Physical Topology Deployment (The Hardened Matrix)

The Orchestrator executes the physical deployment following the **Hierarchy Laws**:

1.  **Framework Link & Constitution Init:**
    - `git submodule add <URL_OR_ROOT_PATH>/.agents .agents`
    - **Modular Relocation (Rule 19):** Immediately execute:
      ```bash
      mkdir -p .agents/governance/constitution
      mv .agents/governance/*.md .agents/governance/constitution/
      ```
2.  **Arsenal Provisioning & Bisection (Rule 70):**
    - **Detection:** Execute `npx -y autoskills@latest`.
    - **Bisection:** Segregate tools into `skills/core/` (Native) and `skills/3rd/` (Domain-specific).
    - **Manifest Sync:** Ensure `skills/manifest.json` reflects the new relative paths.
3.  **Tactical Isolation Shield (Rule 35):**
    - Create a `.gitignore` with the **Mandatory Matrix Seed**:
      ```text
      # Matrix Internal Records
      .agents/task.md
      .agents/task/
      .agents/.agent_state/session_metadata.json
      .agents/.agent_state/
      # Project Dev files
      .env
      venv/
      node_modules/
      ```
4.  **Institutional Identity (Rule 78):**
    - Create the initial `README.md` by **MANDATORY** invoking the `readme-standardizer` skill:
      `Executing [readme-standardizer] skill to ensure Institutional Identity Alignment (Rule 78)`.

## Phase 4: Closing with Audit & Handover

- **Audit:** Verify that the generated tree matches the hierarchical structure (no flat rules in root).
- **Handover:** Declare **Phase 0** as `COMPLETED`. Transition to **Roadmap Alignment (V1.1)** for Phase 1 development.
- **Commit:** `feat(init): bootstrapped hardened modular matrix architecture #001`.

---
*Certified under Roadmap 009 - Matrix Scaffolding & Industrialization*
