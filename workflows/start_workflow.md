---
description: "Session-Start Protocol (Keyword: start)"
version: 6.0.0
---

# 🛡️ Workflow: Start (Matrix Initiation V3)

Master entry protocol optimized to minimize token consumption and strictly invoke the Matrix V3 execution pipeline.

## Execution Flow

| Phase | Step | Action / Constraint |
| :--- | :--- | :--- |
| **0. Amnestic Anchor** | `read_anchor` | Subagents MUST initialize with **Zero-Memory**. The absolute first operation is to extract the topology map from `docs/active_state.json`. |
| **0. Amnestic Anchor** | `read_constitution` | Immediately after the anchor, read `agents.md` to adopt current governance. |
| **0. Amnestic Anchor** | `pip_setup` | Check if `.agents/installed.lock` exists. If not, create virtual environment `.agents/venv_skillopt/`, install dependencies with `.agents/venv_skillopt/bin/pip install -r .agents/requirements.txt`, and create `.agents/installed.lock`. If it exists, skip setup. |
| **0. Amnestic Anchor** | `read_graph` | If `graphify-out/graph.json` is missing, build it by running `venv/bin/graphify update .`. If present, query the graph via MCP/CLI to align on boundaries. |
| **1. Collision Guard** | `habitability_check` | Abort if `IN_PROGRESS` exists with a different session UID. Initialization is PROHIBITED if the workspace is the `.agents` nucleus. |
| **1. Collision Guard** | `lightweight_sync` | Perform a lightweight git check (`git fetch` & `git status`) on both project and submodule to ensure no remote drift. |
| **2. Pipeline Handoff** | `matrix_invocation` | Explicitly hand command to the **Principal Agent** to initiate Phase 1 (Strategic Genesis) of the Core Workflow. |

---
*Optimized for Matrix V3 Chain of Command & Zero-Memory Initiation (v6.0.0).*
