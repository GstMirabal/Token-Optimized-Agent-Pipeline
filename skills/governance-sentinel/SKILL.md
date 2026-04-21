# 🛠️ Local Skill: Governance Sentinel (v1.0.0)

## Domain
- **Category:** Governance / Quality Assurance / Compliance
- **Origin:** Custom synthesis for automated constitutional auditing.
- **Status:** `ACTIVE_LOCAL`
- **Sovereignty:** `local` (Project-Specific)

## Technical Logic
This skill provides the **Compliance Engine** for the framework. It enables a subagent to proactively scan workspace artifacts (plans, roadmaps, code) to detect and block constitutional violations before they reach the execution phase.

## Procedures

### 1. Compliance Scanning (Pre-Execution Audit)
- **Restricted Pattern Detection**: Scan for "Negative Restrictions" defined in `agents.md` (e.g., absolute paths, Spanish in code, global variable injections).
- **Halt Trigger**: If a violation is found in an `implementation_plan.md`, the agent must throw a **HALT** state and provide a specific logic-violation report.

### 2. Pattern Synthesis (Jurisprudence)
- **Friction Extraction**: Analyze `/memory/` logs to identify recurring technical friction or workflow bottlenecks.
- **Amendment Draft**: Propose formal amendments to `agents.md` formulated as technical clauses that provide a definitive solution to the identified friction.

### 3. State Integrity Verification
- **Coordinate Audit**: Verify that `active_state.json` is healthy and that its `current_sprint_id` matches the task headers.

## Governance Audit
- **Sovereignty Policy:** This skill is the "Supreme Court" of code; its dictates are final and must be respected by all Dev and Orchestration nodes.
- **Language Guard:** All audit reports and amendment proposals MUST be in Technical English.
