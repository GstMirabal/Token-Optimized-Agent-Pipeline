---
description: "Retrofitting Scaffolding (Context Re-entry and Token-Saver Optimization)"
version: 1.5.0
---

# 🏗️ Workflow: Retrofitting & Roadmap Alignment (V1.5)

This workflow is optimized for maximum token economy. It mandates a "Context Re-entry Audit" before any code scanning to ensure the agent understands the current project state from existing local metadata.

## Phase 1: Context Re-entry & Phase Discovery (Mentor Mode) 🧠
*   **Action:** The Mentor debates with the Director (in Spanish).
*   **Local Metadata Audit (MANDATORY):** Before any code scanning, the Mentor MUST read `.agents/task.md` and scan the `.agents/roadmaps/` folder.
    *   **Goal:** To establish the "Last Known State" without consuming tokens on source code analysis.
*   **Physical Alignment (Token-Saver):** ONLY if the local metadata is missing or outdated, execute `omni-context-minimizer` to map the current repository topology.
*   **Phase Discovery:** Identify already completed phases (e.g., `PHASE1_FOUNDATION`) and current progress.
*   **Ultimate Phase Definition:** Define the final destination and intermediate steps.

## Phase 2: Governance & Roadmap Documentation (Orchestrator) 📋
1.  **Storage Policy (High-Value Deliverables):** All Roadmap definitions and Phase historical records MUST be stored in the local **`.agents/roadmaps/`** folder (Ignored by Git).
    *   **Final Handover:** Mirror architecturally-relevant summaries to the project's root `docs/` folder for permanent versioning.
2.  **Task Index:** Update `.agents/task.md` as the local Master TOC. It MUST clearly state the **Discovery Status** (e.g., `Status: Continuing from PHASE 2`).
3.  **Strategic Sprint:** Create/Update `.agents/sprints/XXX-sprint-name.md`.
4.  **Context Mapping:** Update `.agent_state/context.md` static cache.

## Phase 3: Arsenal, MCP Audit & WIP Safety Freeze 🛠️
The Orchestrator audits tools with the **Safety Freeze** active:
1.  **WIP Safety Freeze:** Abort if uncommitted human changes exist.
2.  **Local Skills:** Scan `.agents/skills/` for sufficiency.
3.  **External Search (`skills.sh`):** Search the master repository for specialized tools.
4.  **SECURITY LOCK:** No autonomous installation. Human authorization required.
5.  **Skill & MCP Assignment:** Formally assign connections in the `implementation_plan.md`.

## Phase 4: Matrix Activation (Execution & Audit) ⚡
1.  **Authorization:** Present the `implementation_plan.md` and wait for human approval.
2.  **Step Zero (DevOps):** Dependency synchronization and MCP provisioning.
3.  **Coding Matrix:** Deployment of specialized subagents (1 file = 1 agent).
4.  **Dual Audit (Normative & Efficiency):** Validation of rules and context usage.

## Phase 5: Roadmap Closing & Amnesia Extraction 📑
*   Perform a **Final Documentation and Consistency Audit** at the end of each phase.
*   Commit Final Roadmaps to local **`.agents/roadmaps/`**.
*   **Amnesia Protocol (Knowledge Items):** Extract tactical heuristics to **`.agents/knowledge/`**.
*   **Closing Report:** Summarize current progress and the next phase trigger.
