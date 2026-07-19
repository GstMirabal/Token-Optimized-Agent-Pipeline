---
description: "Session-Start Protocol (Keyword: start)"
version: 6.1.0
---

# 🛡️ Workflow: Start (Matrix Initiation V3)

Master entry protocol optimized to minimize token consumption and strictly invoke the Matrix V3 execution pipeline.

## Execution Flow

| Phase | Step | Action / Constraint |
| :--- | :--- | :--- |
| **0. Amnestic Anchor** | `read_anchor` | Subagents MUST initialize with **Zero-Memory**. The absolute first operation is to extract the topology map from `docs/active_state.json` (if it doesn't exist yet, see `first_run_scaffold` below). |
| **0. Amnestic Anchor** | `read_constitution` | Immediately after the anchor, read `agents.md` and `docs/0_SYSTEM_OVERVIEW.md` to adopt current governance. |
| **0. Amnestic Anchor** | `pip_setup` | Check if `.agents/installed.lock` exists. If not, create virtual environment `.agents/venv_skillopt/`, install the lean core with `.agents/venv_skillopt/bin/pip install -r .agents/requirements-core.txt`, and create `.agents/installed.lock`. The heavy skillopt stack (`requirements-skillopt.txt`) installs on demand only when that skill first runs. |
| **0. Amnestic Anchor** | `read_graph` | Skip graph construction on tiny hosts (fewer than ~25 source files — a targeted grep is cheaper than building and loading a graph). Otherwise, if `graphify-out/graph.json` is missing, build it with `.agents/venv_skillopt/bin/graphify update .`; if present, query it via MCP/CLI to align on boundaries. |
| **1. Collision Guard** | `habitability_check` | Abort if `IN_PROGRESS` exists with a different session UID. **All steps below are PROHIBITED if the workspace is the `.agents` nucleus itself** (i.e. `.agents/.git` is a real repo directory, not a submodule pointer — same check `scripts/install_claude.sh` uses). |
| **1. Collision Guard** | `lightweight_sync` | Perform a lightweight git check (`git fetch` & `git status`) on both project and submodule to ensure no remote drift. |
| **1.5 Bridge Provision** | `bridge_check` | If `.agents/.claude_bridge.lock` is missing, run `.agents/scripts/install_claude.sh` before continuing — this is the first time the Claude Code bridge (`.claude/agents`, `.claude/commands/agents`, `.claude/skills`, hooks, MCP) is being wired into this host. Idempotent on later sessions. |
| **1.5 Bridge Provision** | `first_run_scaffold` | If `docs/active_state.json` is missing, this is the first Matrix session in this host project: apply `agents.md §5 mandatory_topology`/`legacy_onboarding` — instantiate the `docs/` tree, materialize `docs/0_SYSTEM_OVERVIEW.md` from `.agents/docs/standards/templates/SYSTEM_OVERVIEW_TEMPLATE.md`, and create an initial `docs/active_state.json` — all **before** Phase 2 handoff. On a mature/legacy codebase, this triggers Full Reverse Engineering (`sprint-architect`'s Legacy Onboarding Protocol) instead of a blank scaffold. |
| **2. Pipeline Handoff** | `matrix_invocation` | Explicitly hand command to the **Principal Agent** to initiate Phase 1 (Strategic Genesis) of the Core Workflow. |

---
*Optimized for Matrix V3 Chain of Command & Zero-Memory Initiation (v6.1.0) — adds first-run host bootstrap (bridge install + docs scaffold) and fixes the graphify venv path.*
