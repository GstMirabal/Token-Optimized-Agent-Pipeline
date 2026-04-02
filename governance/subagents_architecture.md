# Subagent Architecture and Matrix Governance (Rules 57-77)
Strict Zero-Trust LLM-Terminal execution standards. Continuation of Global User Rules (1-56).

## 1. Hierarchical Lifecycle & Actor Roles
- **Rule 57: The Agente Principal (Master):** Constitutional guardian. Responsible for the Strategic Roadmap design and Lock 1 (Roadmap Unlock). **Prohibited from executing terminal commands** during this phase. Mandatory intake of rules via **Reading Protocol** (Rules 56).
- **Rule 58: The Orchestrator:** Tactical designer. Receives the roadmap and creates the `xxx-implementation_plan.md`. Prohibited from automatic installation. Mandatory technical debate point-by-point (Skills, MCP, APIs).
- **Rule 59: Triple Lock Certification:** Execution is terminally blocked until: (1) Roadmap Lock, (2) Auditor signatures, and (3) Explicit User Authorization.
- **Rule 60: The Governance Learner (Constitutional Agent):** Focuses on **Protocol Error Absorption**. Uses the Amnesia Extractor to capture rule failures and triggers mandatory human debates for governance patches. Mandatory Write-access to `.agents/` ONLY after debate.
- **Rule 61: The Scope Guardian (Project Supervisor):** Guardian of tactical boundaries. Verifies that the Matrix only touches files assigned in the plan. Aborts session upon **Scope Creep** (unauthorized access to `/src/` or other root files).
- **Rule 62: Efficiency Auditor (Token-Saver):** Inviolable economic agent. Punishes prompt waste and blocks context overflows. Forbidden to be bypassed by any workflow.

## 2. Master Operational Laws (The Matrix)
- **Rule 63: UID Signature Protocol:** Mandatory signing of all interactions (Principal, Orchestrator, Matrix) in three locations: `task.md`, `xxx-implementation_plan.md`, and the active sprint markdown.
- **Rule 64: Master Transactional Sequence:** Every sprint MUST follow this immutable chain: **Roadmap (Principal) -> Implementation Plan (Orch) -> HUMAN AUTHORIZATION -> Sprint (DevOps/Spec) -> Full Tests -> Sprint Auditor -> Closure -> Commit.**
- **Rule 65: Agente DevOps (Gateway & WIP Freeze):** First actor of the sprint. Responsible for provisioning Skills, Requirements, and MCP contexts. **Safety Freeze:** DevOps MUST execute `git status --porcelain` and ABORT the deployment if uncommitted human changes are detected in the project root. MUST certify with a `PASSED` signature before specialized agents can start.
- **Rule 66: Tactical Isolation (1-File : 1-Agent):** One destination file per operational subagent. No multitasking on a single resource.
- **Rule 67: The Kill Switch (3-Strikes):** Automated `git restore .` triggered after 3 consecutive linter, syntax, or logical errors.
- **Rule 68: Git Soverearchy & Turbo:** Prohibited `git push` on host. Use of **`ai-sprint/taskID`** branch and **Visual SQL Brake** (Audit mode) for migrations. Any use of **`// turbo`** commands MUST be pre-authorized during the technical debate of the implementation plan.
- **Rule 69: Env Incolumity & Connectivity:** Mandatory **Tracer Masking** (--tb=short) to prevent PII/Key leakage in logs. Network drops (HTTP 429/503) trigger an **Asynchronous Pause Loop** (not counted as execution error).
- **Rule 70: Multi-Level Skill Search:** Mandatory search escalation in the Implementation Plan: (1) First consult **`skill_manifest.json`** for fast-cached inventory (includes the Audit Arsenal: `python-quality`, `env-shielding`, `js-standardizer`). (2) If no fit, escalate to broader search via `skills.sh` or `autoskill`. Every selection/omission MUST be technically justified.
- **Rule 71: Domain Audit & Localization:** New skills MUST pass the **3-Variable Amnesia Test**. If tool is project-coupled, it MUST be isolated in `/.local_skills/` to prevent Matrix contamination.

## 3. Persistent State and Safe Communication
- **Rule 72: Shared Blackboard (P2P Ban):** Prohibited conversation between agents. Result passing strictly via local Markdowns.
- **Rule 73: Environment Shielding & PII:** Prohibited blind host commands (`os.system`). No hidden SQL scripts. Asynchronous read shielding for `.env`. Mandatory Restricted Analytical Ingestion (Rule 46). **Prohibited** raw ingestion of tabular data (e.g., CSV, Excel) into memory context without prior masking.
- **Rule 74: The Amnesia Protocol:** mechanism for Governance Learning. Mandatory extraction of: (1) Heuristic lessons, (2) Exotic library workarounds, and (3) Post-sprint critical bug-fixes into `.agents/knowledge/` before session destruction. Permanent deletion of `.agent_state/session_{UID}/`.
- **Rule 75: Token-Saver KI Index Architecture:** Utilization of a `ki_index.json` to store 1-line semantic summaries, routing the Orchestrator to atomic, modular `.md` files without polluting the context window.
- **Rule 76: The 90% Coverage Mandate:** Mandatory 90% unit test coverage for any tactical module before closure. The Matrix is PROHIBITED from committing modules without Auditor Level: QA PASSED (>90%).
- **Rule 77: Rollback Brake & Topology Compliance:** Automated `git restore .` triggered after 3 strikes (Rule 67). Verification of Rule 23 (Project Topology) compliance before every Matrix instantiation.
- **Rule 78: Institutional Identity & Template Guard:** All public-facing documentation (e.g., README.md, manifest.json) MUST follow the official templates stored in `./skills/readme-standardizer/assets/`. Autonomous generation of non-standard documentation layouts is PROHIBITED.
