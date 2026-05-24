---
description: "Session-Close Protocol (Keyword: close)"
version: 6.0.0
---

# 🛡️ Workflow: Close (Atomic Liquidation V3)

Master closure protocol enforcing the Zero-Tolerance Amnesia rule, Absolute Topographic Purity, and Git state sovereignty.

## Execution Flow

| Phase | Step | Action / Constraint |
| :--- | :--- | :--- |
| **0. Constitutional Invocation** | `read_constitution` | Subagents MUST zero memory and read `agents.md`. Closure actions omitting explicit constitutional compliance are invalid. |
| **1. Topographic Audit** | `noise_purge` | **MANDATORY**: Delete all empty folders (J-07). Validate all new files follow **Option B Naming** (`[MODULE]_[TYPE].md`). |
| **1. Topographic Audit** | `graph_rebuild` | Run `venv/bin/graphify update .` to sync AST changes. Run semantic rebuild (Opción C) if documentation has been modified. |
| **2. Tactical Liquidation** | `history_sync` | Update **Master Ledger**, **Global Roadmap**, and **Module Walkthroughs** based on sprint achievements. |
| **3. Zero-Tolerance Purge** | `memory_wipe` | Execute forced physical deletion (`rm`) of all temporary logs within the `/memory/` sprint directory. |
| **4. Roadmap Liquidation** | `state_sync` | Update `docs/active_state.json` with current sprint status and session ID. |
| **5. Git Sovereignty** | `atomic_commit` | Execute atomic `git commit` and `push` on BOTH the main project repository and the `.agents` submodule sequentially. |
| **6. Golden Gate Lock** | `session_lock` | Output the official seal: **`SESSION LOCKED`**. The Matrix enters suspended animation. |

---
*Optimized for Matrix V3 Topographic Purity & Symmetric Documentation (v6.0.0).*
