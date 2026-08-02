---
description: "Session-Close Protocol (Keyword: close)"
version: 6.2.0
invoked_by: human:/agents:close
---

# 🛡️ Workflow: Close (Session Close)

Master closure protocol enforcing the Zero-Tolerance Memory Purge rule, Absolute Topographic Purity, and Git state sovereignty.

## Execution Flow

| Phase | Step | Action / Constraint |
| :--- | :--- | :--- |
| **0. Ruleset Invocation** | `read_ruleset` | Verify the governance ruleset is in context (auto-imported via the host `CLAUDE.md`); a full re-read is only required after context compaction (`anti_amnesia`) — re-reading an already-loaded document is a token violation, not diligence. Closure actions omitting governance compliance are invalid. |
| **1. Topographic Audit** | `noise_purge` | **MANDATORY**: Delete all empty folders (RA-07). Validate all new files follow **Option B Naming** (`[MODULE]_[TYPE].md`). |
| **1. Topographic Audit** | `rules_optimization` | Optimize rules via `train_runner.py` if failures or governance rule changes occur (requires explicit authorization). |
| **1. Topographic Audit** | `graph_rebuild` | Run `make -f .agents/Makefile graphify-update` to sync AST changes. Run the semantic rebuild via `make -f .agents/Makefile graphify-rebuild` if documentation has been modified. |
| **1. Topographic Audit** | `docs_freshness_gate` | Persist `docs/sprints/[ID]/graph_stats.json` (git-tracked snapshot of node/edge/community counts — the only source `docs-freshness-check` trusts, never `graphify-out/`, which is gitignored). Run `make -f .agents/Makefile docs-freshness-check SPRINT_ID=[ID]` (`rules/documentation_standard.md §4`). First cycle a host adopts this gate: findings are `WARN` only. From the second cycle: a `BLOCK` finding halts Phase 6 (`SESSION LOCKED`) until resolved. |
| **2. Sprint Closeout** | `history_sync` | Update the **Master Ledger** (host root `CHANGELOG.md`: append this sprint's entry under `[Unreleased]`, referencing `#[Sprint_ID]`), the **Global Roadmap**, **Module Walkthroughs**, and — **explicitly, not by inference** (a prior host let these go stale for 34 sprints because this list never named them) — the **Documentation Entry Point anchors** (`0_SYSTEM_OVERVIEW.md`, `0_SYSTEM_ARCHITECTURE.md`) whenever this sprint touched structure, stamping their `**Last Audit Sprint**`/`**Last Audit Date**`/`**Last Audit Commit SHA**` fields (`rules/documentation_standard.md §4.1`). |
| **2. Sprint Closeout** | `extract_handoff` | Run `/agents:extract` (see `extract_workflow.md`) to decide what survives into `memory_index.json` before the purge below destroys the raw logs. |
| **2.5 Heuristic Pulse Gate** | `heuristic_pulse_gate` | Present the human with the exact list of candidate KIs `extract_handoff` decided survive into `memory_index.json`, and wait for explicit confirmation before Phase 3 executes — the same `RA-13 SEQUENTIAL_GATES` principle (a verification and the irreversible action it guards must be observed separately) applied to `memory_wipe` instead of a merge. **Exception**: when this session is running under Claude Code's `/loop` (Phases 6-8 unattended, per `pipeline_workflow.md`), this gate does not block — log the candidate KI list and proceed, so multi-sprint automation isn't stalled waiting on a human who isn't watching. Outside `/loop`, this is a hard stop. |
| **3. Zero-Tolerance Purge** | `memory_wipe` | Execute forced physical deletion (`rm`) of all temporary logs within the `/memory/` sprint directory. |
| **4. State Sync** | `state_sync` | Update `docs/active_state.json` with current sprint status, session ID, and `topology_version`, **then refresh the mirror** (`python3 .agents/hooks/state_mirror.py` — in the nucleus: `python3 hooks/state_mirror.py`; hosts also get it automatically via the Stop hook). **Applies in nucleus mode too** — the nucleus keeps its own local anchor, and a stale anchor or mirror lies to the next session. |
| **5. Git Sovereignty** | `atomic_commit` | Execute atomic `git commit` and `git push origin ai-sprint/[ID]` — **never `main`/upstream directly** (RA-12 Branch Discipline). Merging `ai-sprint/[ID]` into `main` is exclusively `deployment_workflow.md`'s job. |
| **5. Git Sovereignty** | `submodule_purity` | Verify `git -C .agents status --porcelain` is **clean**. Host sessions MUST NOT commit into the `.agents` submodule (`agents.md §3 strict_rule`): framework changes go through the nucleus repo's own branch→PR→tag flow, and reach hosts as a deliberate pin update (see `start_workflow.md lightweight_sync`). If dirty, alert the human — do not commit it silently. |
| **6. Session Lock** | `deployment_handoff` | **Name the next protocol, do not merely name the jurisdiction.** The sprint branch is pushed and unmerged; integrating it is `workflows/deployment_workflow.md` (`/agents:deployment`), which is where the Tester signature and the observed-green CI gate live (`RA-13`). Until Phase 019 this workflow said only that merging was "exclusively deployment's job" — a statement about ownership, not a transition — and the branch therefore survived every close by design. That is how sprint branches accumulate. |
| **6. Session Lock** | `session_lock` | Output the official seal: **`SESSION LOCKED`**. The pipeline enters suspended animation. |

---
*Optimized for Pipeline Topographic Purity & Symmetric Documentation (v6.2.0) — fixes the graphify venv path and anchors the push target to the sprint branch (RA-12); adds the Heuristic Pulse Gate (Phase 013) with a `/loop`-aware exception.*
