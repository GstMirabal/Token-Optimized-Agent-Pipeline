---
description: "Universal Matrix Orchestration Protocol (V 2.0.0)"
version: 2.0.0
---

# 🛡️ Workflow: Matrix (Orchestration V2)

Master operational protocol ensuring rigid task delegation and automated Double-Gate verification.

## 1. Amnestic Anchor (Phase 0 - Cycle 0)
*   **Zero-Memory Initialization:** ALL subagents (Principal, Orchestrator, QA, Tester, etc.) MUST initialize with zero memory.
*   **Constitutional Reading:** Every subagent MUST read `agents.md` as its absolute first operation to prevent role usurpation.
*   **Task Binding:** Behavior and context are strictly bounded by the `task_scope.md` payload.

## 2. Tactical Blueprint (Phase 1)
*   **Blueprint Generation:** The **[Orchestrator](../agents/orchestrator.md)** drafts the initial unassigned `Sprint Roadmap` based strictly on human requests.
*   **Mandatory Context Compression:** When sweeping target repositories to compose the Blueprint, the Orchestrator MUST invoke `skills/omni-context-minimizer/scripts/omni_minimizer.py` across massive files. Native full-file readings of files >200 lines are constitutionally restricted.
*   **Hand-off:** Delivered to the Principal Agent. Terminal execution from the Orchestrator is completely PROHIBITED.

## 3. Master Assembly (Phase 2 - The Council)
The **[Principal Agent](../agents/principal_agent.md)** summons the auxiliary council to harden the drafted implementation plan:
1.  **[Agent Orchestrator](../agents/agent_orchestrator.md)**: Reads the roadmap and assigns specific subagents (by Node ID) to each tactical step.
2.  **[Skill Architect](../agents/skill_architect.md)**: Reviews required logic, evaluates the flat `skills/` layer via `manifest_skills.json`, and synthesizes any missing tools natively.
3.  **[Rule Validator](../agents/rule_validator.md)**: Audits the `/rules` layer and drafts missing topological norms if new terrain is breached.
*   **Assembly Output**: The Principal Agent natively compiles the final `sprint_blueprint.md`.

## 4. The Golden Gate (Phase 3 - Human Lock)
*   **Authorization Shield:** The Principal Agent delivers the `sprint_blueprint.md` to the Human User.
*   **Lock Release:** All matrix operations remain locked. The agent explicitly requests the "OK" human token before proceeding to execution.

## 5. Monitored Execution & Remediation Loop (Phase 4)
*   **Dispatch:** The Principal Agent invokes the assigned executing subagent, delivering the isolated `task_scope.md`.
*   **The Double-Gate Review:** Upon step completion, the artifact undergoes a mandatory double-gate check:
    1.  **Gate 1 (Structural):** The **[QA Agent](../agents/qa_agent.md)** verifies syntax, standard compliance, and constitutional strictness.
    2.  **Gate 2 (Functional):** The **[Tester Agent](../agents/tester_agent.md)** evaluates integration, writes `:memory:` tests, and guarantees zero regressions.
*   **Remediation Loop:** If either gate fails, the Principal Agent bounces the exact trace back to the executor subagent for automatic internal patching. The user is NOT bothered.
*   **Milestone Approval:** Only upon successful, bug-free closure does the Principal Agent request Human authorization to mark the operational step as COMPLETED.

## 6. Liquidation & Context Refresh
*   **Amnesia Extraction:** Run **`extract_workflow.md`**.
*   **Governance Learning (Phase 13):** Executing telemetry distillation via `close_workflow.md`.
*   **Roadmap Liquidation:** Update active Roadmap status to **`COMPLETED (100%)`** and reflect in `task_scope.md` before closure.

---
*Certified under Matrix V2 Topological Constitution*
