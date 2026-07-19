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
| **1. Collision Guard** | `lightweight_sync` | Perform a lightweight git check (`git fetch --tags` & `git status`) on both project and submodule. If a **newer `.agents` tag** exists than the one pinned (`git -C .agents describe --tags` vs `git -C .agents tag --sort=-v:refname \| head -1`), **report it to the human with a pointer to `.agents/CHANGELOG.md` and await explicit authorization** — auto-updating the governance submodule is PROHIBITED (same supply-chain doctrine as J-10). |
| **1.5 Bridge Provision** | `bridge_check` | Run `.agents/scripts/install_claude.sh` if `.agents/.claude_bridge.lock` is missing **or** its recorded commit differs from `git -C .agents rev-parse HEAD` (i.e. the submodule was deliberately updated since the last install — new agents/commands/skills need linking). The installer is idempotent; `hooks/on_init.py` performs this same check automatically at session start. |
| **1.5 Bridge Provision** | `first_run_scaffold` | If `docs/active_state.json` is missing, this is the first Matrix session in this host: detect the onboarding scenario and route it (table below) **before** Phase 2 handoff. All scenarios end with: `docs/` tree instantiated, `docs/0_SYSTEM_OVERVIEW.md` materialized from its template, initial `docs/active_state.json`, and the **Master Ledger** (`CHANGELOG.md`) present at the host root (created from `CHANGELOG_TEMPLATE.md` only if absent — an existing changelog is adopted as-is, never reformatted). |

### 🧭 Onboarding Scenario Matrix (`first_run_scaffold` routing)

| Scenario | Detection signals | Route |
| :--- | :--- | :--- |
| **A. Greenfield** | Short/empty git history, no `docs/`, no substantial source code. | Full scaffold from templates + Master Ledger seeded ("Adopted Universal-Agents vX.Y.Z"). Verify default branch is `main` and a baseline `.gitignore` exists. |
| **B. Prior agent interactions** | Pre-existing `CLAUDE.md`/`.claude/`, legacy `.agents` artifacts (`task/`, `implementation_plan*.md`, `knowledge/`, `docs/active_task.md`, `.agent_state/`), or other frameworks' files (`.cursor/rules`, `.windsurfrules`, `copilot-instructions.md`). | Execute the **Legacy Absorption Protocol** (`standardization_workflow.md` Phase 5) — census → secret scan → snapshot gate → reconciliation report → Human OK → migration → integrity audit. If an old `.agents` submodule exists, verify its `git remote` points to the official repo first (a divergent fork HALTS onboarding with an alert). Adopt the existing `CLAUDE.md` (append imports only). Then scaffold whatever is still missing. |
| **C. Mature project, no agents** | Substantial codebase, zero agentic traces. | `agents.md §5 legacy_onboarding`: Full Reverse Engineering (`sprint-architect` Legacy Onboarding Protocol) → Blueprints + Walkthroughs. Adopt an existing `CHANGELOG.md` as the Master Ledger untouched; if none, seed one whose first entry documents the audited inherited state. |
| **2. Pipeline Handoff** | `matrix_invocation` | Explicitly hand command to the **Principal Agent** to initiate Phase 1 (Strategic Genesis) of the Core Workflow. |

---
*Optimized for Matrix V3 Chain of Command & Zero-Memory Initiation (v6.1.0) — adds first-run host bootstrap (bridge install + docs scaffold) and fixes the graphify venv path.*
