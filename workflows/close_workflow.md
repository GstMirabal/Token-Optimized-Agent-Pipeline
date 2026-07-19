---
description: "Session-Close Protocol (Keyword: close)"
version: 6.1.0
---

# 🛡️ Workflow: Close (Atomic Liquidation V3)

Master closure protocol enforcing the Zero-Tolerance Amnesia rule, Absolute Topographic Purity, and Git state sovereignty.

## Execution Flow

| Phase | Step | Action / Constraint |
| :--- | :--- | :--- |
| **0. Constitutional Invocation** | `read_constitution` | Verify the constitution is in context (auto-imported via the host `CLAUDE.md`); a full re-read is only required after context compaction (`anti_amnesia`) — re-reading an already-loaded document is a token violation, not diligence. Closure actions omitting constitutional compliance are invalid. |
| **1. Topographic Audit** | `noise_purge` | **MANDATORY**: Delete all empty folders (J-07). Validate all new files follow **Option B Naming** (`[MODULE]_[TYPE].md`). |
| **1. Topographic Audit** | `rules_optimization` | Optimize rules via `train_runner.py` if failures or constitutional changes occur (requires explicit authorization). |
| **1. Topographic Audit** | `graph_rebuild` | Run `make -f .agents/Makefile graphify-update` to sync AST changes. Run the semantic rebuild via `make -f .agents/Makefile graphify-rebuild` if documentation has been modified. |
| **2. Tactical Liquidation** | `history_sync` | Update the **Master Ledger** (host root `CHANGELOG.md`: append this sprint's entry under `[Unreleased]`, referencing `#[Sprint_ID]`), the **Global Roadmap**, and **Module Walkthroughs** based on sprint achievements. |
| **2. Tactical Liquidation** | `extract_handoff` | Run `/agents:extract` (see `extract_workflow.md`) to decide what survives into `memory_index.json` before the purge below destroys the raw logs. |
| **3. Zero-Tolerance Purge** | `memory_wipe` | Execute forced physical deletion (`rm`) of all temporary logs within the `/memory/` sprint directory. |
| **4. Roadmap Liquidation** | `state_sync` | Update `docs/active_state.json` with current sprint status, session ID, and `topology_version`. **Applies in nucleus mode too** — the nucleus keeps its own local anchor (git-ignored), and skipping this step leaves it lying to the next session. |
| **5. Git Sovereignty** | `atomic_commit` | Execute atomic `git commit` and `git push origin ai-sprint/[ID]` — **never `main`/upstream directly** (J-12 Branch Discipline). Merging `ai-sprint/[ID]` into `main` is exclusively `deployment_workflow.md`'s job. |
| **5. Git Sovereignty** | `submodule_purity` | Verify `git -C .agents status --porcelain` is **clean**. Host sessions MUST NOT commit into the `.agents` submodule (`agents.md §3 strict_rule`): framework changes go through the nucleus repo's own branch→PR→tag flow, and reach hosts as a deliberate pin update (see `start_workflow.md lightweight_sync`). If dirty, alert the human — do not commit it silently. |
| **6. Golden Gate Lock** | `session_lock` | Output the official seal: **`SESSION LOCKED`**. The Matrix enters suspended animation. |

---
*Optimized for Matrix V3 Topographic Purity & Symmetric Documentation (v6.1.0) — fixes the graphify venv path and anchors the push target to the sprint branch (J-12).*
