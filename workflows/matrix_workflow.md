---
description: "Universal Matrix Orchestration Protocol (V 3.0.0)"
version: 3.0.0
---

# 🛡️ Workflow: Matrix (Orchestration V2)

Master operational protocol ensuring rigid task delegation and automated Double-Gate verification.

## Execution Flow

| Phase | Step | Action / Constraint |
| :--- | :--- | :--- |
| **0. Amnestic Anchor** | `init_check` | ALL subagents MUST initialize with zero memory and read `agents.md`. Role usurpation is strictly prohibited. |
| **1. Blueprint** | `draft_roadmap`| Orchestrator drafts unassigned `Sprint Roadmap` based strictly on human requests/Implementation Plan. |
| **1. Blueprint** | `context_limit`| Orchestrator MUST invoke `omni_minimizer.py` across massive files. Native full-file readings of files >200 lines are PROHIBITED. |
| **2. Assembly** | `council_summon`| Principal Agent summons Agent Orchestrator, Skill Architect, and Rule Validator to assign roles, verify skills, and audit rules. |
| **3. Golden Gate**| `human_lock` | Principal Agent delivers `sprint_blueprint.md` to user. Execution is LOCKED until explicit "OK" is given. |
| **4. Execution** | `dispatch` | Principal Agent invokes assigned subagent with isolated `task_scope.md`. |
| **4. Double-Gate**| `qa_tester_loop`| Completed logic undergoes strict review: Gate 1 (QA Agent) -> Gate 2 (Tester Agent). Bounces back internally if failed. |
| **5. Closure** | `handover` | Run `close_workflow.md` to execute telemetry distillation, atomic commits, and memory purge. |

---
*Optimized for Matrix V2 Token Savings & Strict Governance (v3.0.0).*
