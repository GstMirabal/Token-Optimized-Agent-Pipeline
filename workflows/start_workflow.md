---
description: "Session-Start Protocol (Keyword: start)"
version: 6.1.0
---

# 🛡️ Workflow: Start (Matrix Initiation V3)

Master entry protocol optimized to minimize token consumption and strictly invoke the Matrix V3 execution pipeline.

## Execution Flow

| Phase | Step | Action / Constraint |
| :--- | :--- | :--- |
| **0. Amnestic Anchor** | `read_anchor` | Subagents MUST initialize with **Zero-Memory**. The absolute first operation is to extract the topology map from `docs/active_state.json` (if it doesn't exist yet, see `first_run_scaffold` below). **Mirror reconciliation**: if `.agent_state/mirror.json` disagrees with the anchor, this is NOT a collision — the anchor wins (the mirror is the backup; staleness only means a previous session ended without the Stop hook firing). Resync it (`python3 .agents/hooks/state_mirror.py`) and continue. The mirror is only authoritative when the anchor itself is missing or corrupt (crash recovery). |
| **0. Amnestic Anchor** | `read_constitution` | Immediately after the anchor, read `agents.md` and `docs/0_SYSTEM_OVERVIEW.md` to adopt current governance. |
| **0. Amnestic Anchor** | `pip_setup` | Check if `.agents/installed.lock` exists. If not, create virtual environment `.agents/venv_skillopt/`, install the lean core with `.agents/venv_skillopt/bin/pip install -r .agents/requirements-core.txt`, and write `.agents/installed.lock` recording the ISO timestamp and the requirement set installed (so a later reader knows *what* this environment contains). The heavy skillopt stack (`requirements-skillopt.txt`) installs on demand only when that skill first runs. |
| **0. Amnestic Anchor** | `read_graph` | Skip graph construction on tiny hosts (fewer than ~25 source files — a targeted grep is cheaper than building and loading a graph). Otherwise, if `graphify-out/graph.json` is missing, build it with `.agents/venv_skillopt/bin/graphify update .`; if present, query it via MCP/CLI to align on boundaries. |
| **1. Collision Guard** | `habitability_check` | Abort if `IN_PROGRESS` exists with a different session UID (crash forensics). **Nucleus mode** (`.git` is a real repo directory, not a submodule pointer — same check the installer uses): only Phase 1.5 (bridge/scaffold) is PROHIBITED (`nucleus_neutrality`); Phase 0 and `lightweight_sync` still run, with `.agents/`-prefixed paths resolving to the repo root (e.g. `./venv_skillopt/`). |
| **1. Collision Guard** | `lightweight_sync` | Perform a lightweight git check (`git fetch --tags` & `git status`) on both project and submodule. If a **newer `.agents` tag** exists than the one pinned (`git -C .agents describe --tags` vs `git -C .agents tag --sort=-v:refname \| head -1`), **report it to the human with a pointer to `.agents/CHANGELOG.md` and await explicit authorization** — auto-updating the governance submodule is PROHIBITED (same supply-chain doctrine as J-10). *Nucleus mode: `git describe` naturally runs ahead of the latest tag on `main` — commit offset alone is NOT drift.* |
| **1.5 Bridge Provision** | `bridge_check` | Run `.agents/scripts/install_claude.sh` if `.agents/.claude_bridge.lock` is missing, its recorded commit differs from `git -C .agents rev-parse HEAD` (i.e. the submodule was deliberately updated since the last install — new agents/commands/skills need linking), **or** the linked artifacts themselves are gone from `.claude/` despite a matching lock (a `git clean -fd`/manual deletion wipes the host's untracked bridge without touching the lock, which lives inside the submodule). The installer is idempotent; `hooks/on_init.py` performs this same check (`sync_commands` + `bridge_intact` sentinel) automatically at session start. |
| **1.5 Bridge Provision** | `first_run_scaffold` | If `docs/active_state.json` is missing, this is the first Matrix session in this host: load the **Onboarding Scenario Matrix** (`standardization_workflow.md` Phase 6) and route the detected scenario (greenfield / prior agents / mature) **before** Phase 2 handoff. The matrix lives there — not here — because first-run routing is a one-time cost while this workflow loads on EVERY session (`rules/token_economy.md §3`). |
| **2. Pipeline Handoff** | `matrix_invocation` | Explicitly hand command to the **Principal Agent** to initiate Phase 1 (Strategic Genesis) of the Core Workflow. |

---
*Optimized for Matrix V3 Chain of Command & Zero-Memory Initiation (v6.1.0) — adds first-run host bootstrap (bridge install + docs scaffold) and fixes the graphify venv path.*
