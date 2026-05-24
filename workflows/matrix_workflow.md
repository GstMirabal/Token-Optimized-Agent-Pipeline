---
description: "Universal Matrix Orchestration Protocol (V 3.5.0)"
version: 3.5.0
---

# 🛡️ Workflow: Matrix (Orchestration V3)

Master operational protocol ensuring rigid task delegation, automated Double-Gate verification, and infrastructural stability.

## 🚀 The Execution Pipeline (Matrix V3)

| Phase | Agent | Action / Constraint |
| :--- | :--- | :--- |
| **1. Strategic Genesis** | Principal | Drafts Implementation Plan (IP) based on User Request. |
| **2. Environment Readiness** | **DevOps** | **MANDATORY**: Activate `venv`, export `.env`, check Docker/DB health. |
| **3. Tactical Blueprint** | Orchestrator | Drafts Initial Roadmap and instantiates `docs/sprints/[ID]-[Stack]-[Layer]/`. |
| **4. Master Assembly** | Concilio | Summon Agent Orch, Skill Arch, and Rule Val to finalize IP and skills. |
| **5. Golden Gate** | Principal | Request explicit Human OK before starting execution. |
| **6. Monitored Execution** | Subagents | Perform atomic tasks with commits referencing the Sprint ID. |
| **7. Quality Gate** | QA & Tester | Gate 1 (Structural Audit & Graph Integrity Check) -> Gate 2 (Functional Verification). |
| **8. Tactical Liquidation**| Principal | Update Blueprints, Global Roadmap, Walkthroughs, and Master Ledger (including final Graph Rebuild via `make graphify-rebuild`). |

## 📐 Standards & Rules
- **Amnestic Anchor**: All subagents start with zero memory; read `active_state.json` and `agents.md` first.
- **Graph Sovereignty**: Query `graph.json` via MCP or CLI before any recursive grep codebase research.
- **Topographic Purity**: Prohibited to leave empty folders. Purge noise before closing.
- **Unique Naming**: All artifacts must follow the `[MODULE]_[TYPE].md` standard (Option B).
- **Context Limit**: Mandatory use of `omni_minimizer.py` for files >200 lines.

---
*Optimized for Matrix V3 Symmetry & Infrastructure Hardening (v3.5.0).*
