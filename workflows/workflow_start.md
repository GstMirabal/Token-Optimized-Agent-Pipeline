---
description: "Session-Start Protocol (Keyword: start)"
version: 3.1.0
---

# 🛡️ Workflow: Start (Session Gateway)

Master entry protocol to ensure Matrix integrity before any tactical deployment.

## 0. Governance & Constitutional Consultation
Before any operational logic, the Agent MUST read the **Universal-Agents Constitution (`agents.md`)**.
- **Action:** Perform the Federated Reading Protocol focusing on the Matrix Operational Manual (`Section 3: Architecture and Topology of the Project`, `Section 6: Chain of Command`). Align all subsequent decisions with the standard nomenclature, documentation, and efficiency rules defined.

## 0.1 Zero Coordinate & Crash Detection
Before any interaction or topology discovery, the Agent MUST read the anchor point **`docs/active_state.json`**:
- **Zero Coordinate Extraction**: Agents must unconditionally extract their scope, current App, active Layer, and Sprint ID (#02x) from this exact file.
- **Nucleus Guard**: If the workspace is the core `.agents` matrix, automatic structural scaffolding or directory initialization is **PROHIBITED**.
- **Crash Detection:** If `status == "IN_PROGRESS"` or `intelligence_certified != "PASSED"`, a session crash is detected.
- **Action:** The Agent MUST ABORT normal initialization and trigger **`workflow_knowledge_extractor.md --forensic`** to recover or purge orphaned state.
- **Lock:** No new session is permitted until the metadata reports `status: "CLOSED_SUCCESSFULLY"`.

## 1. UID Signature Validation
The Agent MUST update `task/task.md` with the unique session identifier and confirm readiness for role assignment.

## 2. Hook Protocol
- Verify existence of the standardized `/docs/` tree in the host project.
- **Action:** If the `/docs/` tree does not exist (and the project is NOT the `.agents` nucleus), the Agent must summon the **[Matrix Mapper](agents/matrix_mapper.md)** to instantiate the hierarchical directory topology.
- *Note:* The previously utilized `task/topology/` directory is deprecated in v3; the agent relies purely on the state anchor and `/docs/`.

## 3. Skill Infrastructure & Trinity Check
Before execution, the DevOps role function MUST verify physical availability of approved resources:
- Confirm physical presence of tools in `./skills/core/`, `./skills/local/`, or `./skills/3rd/`.
- **Trinity Standard Enforcement:** Ensure any active skill adheres strictly to the structural mandate containing `README.md`, `SKILL.md`, and an executable `/scripts/` folder. Zero-tolerance for root-level tool contamination.
- Validate MCP server connectivity as defined in the implementation plan.

## 4. Environment Health & Sandbox
- Execute environment validation via `Makefile` (`make setup`, `make check-env`).
- Confirm existence of `./venv/`, `./node_modules/`, and version anchoring files (e.g., `.python-version` or `.nvmrc`).
- Validate presence of `.env` secrets.

## 5. WIP Safety Freeze
- **Safety Freeze:** Execute `git status --porcelain`. If uncommitted human changes exist in the root, the session MUST ABORT or require a commit before proceeding.
- **Lock 0:** Changes to governance or workflows require explicit roadmap-level authorization.

## 6. Amnesia Integrity & KI-Preloading
- **Purge Check (Matrix Hygiene):** Inspect `docs/sprints/` for orphaned session data. Destroy unpurged session folders from previous runs.
- **Memory Routing Protocol:** Parse EXCLUSIVELY and dynamically the descriptor nested locally to the active *namespace* (e.g., `memory/[active_layer]/memory_index.json`). Reject listing directories or mass reading raw `.md` content.

## 7. DevOps Certification
- **Structural Audit:** Physical inspection of `/src`, `/tests`, and `/logs` directories to ensure segregation constraints.
- **Certification:** Inject `DEPLOYMENT_READY: PASSED` signature into the session log.
- **Security Lock:** Matrix execution is blocked until this certification is issued.

## 8. Activation of the Principal Agent
Following successful DevOps certification and environment stabilization, command is transferred strictly to the **[Principal Agent](agents/principal_agent.md)**:
- **Strategic Leadership:** The Principal Agent awakens as the Constitutional Guardian.
- **Lock 1 Opening:** The Principal MUST verify the Strategic Roadmap against requested actions.
- **8.1 MANDATORY HUMAN AUTHORIZATION (Triple Lock Security):**
  - The Principal Agent is **STRICTLY PROHIBITED** from issuing the **`ROADMAP_UNLOCKED`** signal or creating tactical branches autonomously.
  - The Agent MUST present the current roadmap status and explicitly ask: **"Do you authorize the unlocking of this roadmap and the transition to tactical planning?"**
  - **Terminal Block:** Execution terminates here until word-for-word human authorization is received. Once received, the Principal Agent authorizes the `ACTIVE` state.

## 9. Git Sovereignty
- **Branch Check:** Once human authorization is granted, checkout/creation of the **`ai-sprint/taskID`** branch occurs.
- **History Linkage:** All subsequent commits MUST aggressively utilize Conventional Commits containing the Sprint ID suffix extracted from the Zero Coordinate (`#02x`).
- **Tracer Masking (PII Shielding):** Configure execution parameters to use **`--tb=short`** by default.

## 10. Immunity Seal and Source of Truth
The Agent MUST recognize this `.agents/` Matrix as the **Single Source of Truth** for governance and operational procedures:
- **Divergence Ban:** Strictly prohibited use of competing rules or workflows outside this Matrix.
- **Conflict Detection:** Any divergence between local state and the constitutional submodule is a **Terminal Session Failure**.

---
*Generated mathematically under Universal-Agents Rules (v3.1.0).*
