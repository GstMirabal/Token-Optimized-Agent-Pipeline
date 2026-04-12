---
description: "Universal Matrix Orchestration Protocol (Keyword: matrix)"
version: 1.1.0
---

# 🛡️ Workflow: Matrix (Universal Orchestration)

Master operational protocol ensuring total identity segregation and explicit authorization locks.

## 1. Identity & Memory Audit (Mentor Mode)
*   **Identity & Memory Audit (Rule 57):** Call the **Agente Principal (Mentor)**. Terminal execution is **STRICTLY PROHIBITED** during this phase.
*   **Memory Seal (Rule 57):** **ALL** subagents (Principal, Orchestrator, DevOps, Matrix) **MUST** perform the full Reading Protocol of `.agents/governance/constitution/` and `task/task.md` upon role-switch to ensure total constitutional alignment (Rule 10).
*   **Discovery Block:** Analyze the current strategic roadmap phase.
*   **Gap Analysis (Isolated Question):** Before progressing, ask: *"Is there any additional technical detail or objective that should be integrated into the Roadmap?"*

## 2. Strategic Unlock & Sprint Design (Orchestrator)
*   **Lock 1 (Strategic Unlock):** Once the roadmap is aligned, request: *"Do you authorize the unlocking of Phase [X] for tactical design?"*
*   **Sprint 1:1 Architecture:** Create a dedicated sprint file for each agent/task following **Rule 24 (00x-00y-agent.md)**.
*   **Sprint Artillery (Rules 58/70/81 - Lock 2):** Before generating the implementation plan, the Orchestrator **MUST** present the technical arsenal:
    - **Internal Skills:** List skills from `manifest_skills.json` that will be used and explain WHY.
    - **External Skills:** If tool not in the manifest, escalate to **locally installed `autoskills`** (`skills/3rd/autoskills/`). Final backup: **`skill.sh`**.
    - **MCP/APIs:** Declare remote context dependencies.
    - **Sovereignty Guard:** Use of ephemeral `npx` bridges is strictly **PROHIBITED**.
    - **Mermaid Representation:** The selected tool MUST be explicitly represented in the Implementation Plan architectural diagrams (Rule 70).
    - **Debate -> Select -> Explicit Authorize.**
    - **Debate -> Select -> Explicit Authorize.**
*   **Implementation Plan:** Present `xxx-implementation_plan.md` for signature: **"PLAN_AUTHORIZED"**.

## 3. DevOps Provisioning & Visual Proof (DevOps Agent)
*   **WIP Safety Freeze (Rule 65):** The Agent **MUST** execute `git status --porcelain`. If uncommitted human changes exist in the root, the session **MUST ABORT** or require a commit before any provisioning.
*   **Environment Certification:** Verify task-specific dependencies and environment health.
*   **Visual Proof (Step 3.2):** Present a **Visual Diff or `cat`** of the target file to certify its clean state before handover.
*   **Lock 3 (Deployment Hold):** Emit: **"DEPLOYMENT_READY: [SprintID-AgenteID] PASSED"**.

## 4. Matrix Tactical Execution (The Matrix)
*   **Jurisdictional Isolation (Rule 66):** One subagent per file. Concurrent access requires queuing.
*   **Identity Signature:** Every terminal request must be tagged: `[Agente_ID] requests authorization for [SprintID] on [Path]`.
*   **Subagent Logic:** Execute authorized logic with minimal token waste.

## 5. Audit & QA Architect (The Auditor)
*   **Test Generation:** The **Matrix_QA_Architect** (Rule 80) MUST generate or update a test suite to ensure **100% Coverage (Rule 76)**.
*   **Kill Switch Monitoring (Rule 67):** Activate automated rollback (`git restore .`) after 3 consecutive linter, syntax, or logical errors.
*   **Audit Lock:** Final validation of lints and architectural compliance.

## 6. Liquidation & Context Refresh
*   **Amnesia Extraction:** Run **`extract_workflow.md`**.
*   **Roadmap Liquidation (Rule 31):** Update active Roadmap status to **`COMPLETED (100%)`** and reflect in `task/task.md` before closure.
*   **Full Context Reset:** Call the **Principal (Mentor)** to re-read governance to prevent memory drift before the next mission.

---
*Certified under Roadmap 011 - Universal Orchestration Protocol*
