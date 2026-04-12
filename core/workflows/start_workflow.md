---
description: "Session-Start Protocol (Keyword: start)"
version: 3.4.0
---

# 🛡️ Workflow: Start (Inicio)

Master entry protocol optimized to ensure Matrix integrity and secure secret handling.

## 0. Governance and Constitutional Inquiry
Before any operational logic, the Agent **MUST** read the **Constitution of Universal-Agents (`agents.md`)**.
- **Action:** Perform the Federated Reading Protocol focusing on the Matrix Operating Manual (`Section 3: Architecture and Topology of the Project`, `Section 6: Chain of Command`).
- **Halt Condition:** If, upon assimilating `agents.md`, the Agent determines that constitutional dependencies cannot be validated, the gateway remains **LOCKED**.

## 0.3 Constitutional Symlink (Submodule Sovereignty)
When operating as a Git submodule inside a parent project:
- **Requirement:** The project root MUST have a visible reference to the Matrix Constitution.
- **Action:** If the Agent detects it is in a subdirectory (e.g., `.agents/`) and `../AGENTS.md` does not exist:
    - **Execution:** Create a relative symlink: `ln -s .agents/AGENTS.md AGENTS.md` in the parent root.
    - **Certification:** Log the action: "GOVERNANCE: Constitutional symlink instantiated at project root."

## 0.1 Zero Coordinate and Collision Detection
Before any interaction, the Agent **MUST** read the anchor point **`docs/active_state.json`**:
- **Extraction:** Unconditionally extract scope, App, Layer, and Sprint ID (#02x).
- **Nucleus Guard**: Initialization is prohibited if the workspace is the `.agents` nucleus.
- **Task 0.1.1: Nuclear Recovery:** If `docs/active_state.json` is missing or corrupted, search for **`.agent_state/mirror.json`**.
    - **Action**: If the mirror exists, restore the state to `docs/active_state.json` and issue a **Manual Correction Alert** stating "RECOVERY: State restored from Mirror".
- **Action:** If a session collision is detected (`status == "IN_PROGRESS"`), trigger **`extract_workflow.md --forensic`** and abort.

## 0.2 Synchronization Audit (Sentinel Gateway)
Before mapping tools, the Agent **MUST** invoke the **[GitHub Sentinel](../agents/github_sentinel.md)**:
- **Sync Audit**: Compare local vs. remote state via MCP. Block initiation if there is *drift* (local behind remote).
- **Offline Mode**: Permitted during network failures, but with a **strict prohibition** on creating tactical branches. Reconnection triggers a mandatory re-audit.

## 1. UID Signature Validation
Update `task/task.md` with the unique session identifier.

## 2. Hook Protocol (Documentation Mapping)
- Verify the existence of the `/docs/` tree.
- **Action:** If structural support is missing, summon the **[Matrix Mapper](../agents/matrix_mapper.md)** to instantiate the hierarchy.
- **Additional Action**: Summon the **[Doc Orchestrator](../agents/doc_orchestrator.md)** to ensure synchronization of contracts, architecture maps, and sprint logs.

## 3. Skill Efficiency and Manifest Validation
Avoid unnecessary token waste on recursive physical inspections:
- **Fast Validation:** The **[DevOps Sentinel](../agents/devops_sentinel.md)** will verify the integrity and update date of the `manifest_skills.json` file.
- **Trinity Check:** Physical auditing of Trinity Standard compliance (`README`, `SKILL`, `/scripts/`) is perform only on skills that have been recently modified or added.
- **MCP Check:** The **[DevOps Sentinel](../agents/devops_sentinel.md)** will validate the health registry in `mcp-config.json`.

## 4. Environment Health and Secrets (Shielding Protocol)
The **[DevOps Sentinel](../agents/devops_sentinel.md)** will verify the habitability of the sandbox:
- **Action**: Execute environment validation via `Makefile` (`make setup`, `make check-env`).
- **Secrets Protocol**: The Sentinel MUST **export** the `.env` file to the session. It is strictly prohibited for the agent to read or parse the secret's content into its contextual memory.
- **Halt on Absence**: If `.env` does not exist, the Sentinel MUST abort and issue a **Manual Correction Alert** for the user (referencing `.env.template`).

## 5. WIP Safety Freeze (Local)
- **Safety Freeze:** Execute `git status --porcelain`. If there are uncommitted local changes, the session MUST require a commit or abort before proceeding.

## 6. Amnesia Integrity and KI Preloading
- Inspect `docs/sprints/` for orphaned data.
- **Memory Routing:** Exclusively analyze the `memory_index.json` descriptor of the active namespace.

## 7. DevOps Certification (Habitability)
The **[DevOps Sentinel](../agents/devops_sentinel.md)** must certify that the environment is suitable for operation:
- **Certification**: Inject the signature `DEPLOYMENT_READY: PASSED` into the log.
- **Note**: Deep structural auditing of code folders is delegated to the tactical planning phase (Implementation Plan).

## 8. Principal Agent Activation
Command is strictly transferred to the **[Principal Agent](../agents/principal_agent.md)**:
- **8.1 MANDATORY HUMAN AUTHORIZATION (Triple Lock Security):**
- The Principal Agent is **STRICTLY PROHIBITED** from issuing the **`ROADMAP_UNLOCKED`** signal autonomously.
- The Agent MUST present the current roadmap state and explicitly ask: **"Do you authorize the unlocking of this roadmap and the transition to tactical planning?"**

## 9. Git Sovereignty
Checkout/creation of the **`ai-sprint/taskID`** branch and application of Conventional Commits with the Sprint ID (#02x).

## 10. Immunity Seal
The Matrix `.agents/` is recognized as the **Single Source of Truth** for governance and procedures.

---
*Optimized for secret security under Universal-Agents Rules (v3.3.1).*
