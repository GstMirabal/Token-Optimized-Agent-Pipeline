---
description: "Execution Pipeline Protocol (Keyword: pipeline)"
version: 3.6.0
invoked_by: human:/agents:pipeline, start_workflow.md#pipeline_invocation
---

# 🛡️ Workflow: Pipeline (Execution Pipeline)

Master operational protocol ensuring rigid task delegation, automated Double-Gate verification, and infrastructural stability.

## 🚀 The Execution Pipeline

| Phase | Agent | Action / Constraint |
| :--- | :--- | :--- |
| **1. Planning** | `principal_agent` | Drafts the Implementation Plan (IP) from the user request, from `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md`. **Deliverable**: `IMPLEMENTATION_PLAN.md`, written and versioned in the repository before Phase 5 — and **where the environment offers a planning mode, Phase 1 runs in it**. That is stated in terms the framework can check rather than in terms of one IDE's feature: what is verifiable is the committed file, not which editor produced it. **A plan drafted outside this workflow — in an IDE planning mode, a document, a conversation — enters HERE as the IP once approved, and does not skip Phases 3-5.** An approved plan is an input to the pipeline, never a substitute for it: skipping ahead discards the roadmap, the agent and skill assignments, and `task_scope.md`, which are produced downstream of planning and not by it. Anything landing in `docs/plans/` via `plansDirectory` is a **safety net against loss, not the artifact** — it carries an IDE-generated name. |
| **2. Environment Readiness** | `devops_agent` | **MANDATORY**: Activate `venv`, export `.env`, check Docker/DB health. |
| **3. Roadmap Drafting** | `orchestrator` | Drafts Initial Roadmap and instantiates `docs/sprints/[ID]-[Stack]-[Layer]/`. **Extracts Phase 1's plan into that directory as `IMPLEMENTATION_PLAN.md` and commits it** — this is the earliest point at which the canonical path exists, which is why Phase 1 authors the plan and Phase 3 files it. **Also creates and checks out branch `ai-sprint/[ID]` from the base branch** (RA-12 Branch Discipline) — no commit may happen before this branch exists. |
| **4.1 Agent Assignment** | `agent_orchestrator` | Assigns the most specialized existing subagent to each roadmap step, or authors a new profile under `agents/` when none fits. **Deliverable**: every step has a named assignee. |
| **4.2 Skill Assignment** | `skill_architect` | Checks whether a computational tool already exists in `skills/` before each task starts; forges one under the Three-File Standard when it does not. **Deliverable**: every step has its tools resolved. |
| **4.3 Rule Audit** | `rule_validator` | Audits the roadmap against current `rules/`, using the graphify dependency graph. **Deliverable**: `task_scope.md` inside the sprint directory named in `agents.md §5 mandatory_topology` — `Subtask \| Target File \| Assignee \| Status`. It said *"at the host root"* and *"git-ignored"* until Sprint 023; Sprint 024 moved it into the sprint directory and made it versioned, and `scripts/docs_freshness_check.py` and `close_workflow.md` Phase 2.6 have read it there ever since. |
| **5. Approval Gate** | `principal_agent` | **Precondition, checked before asking**: `IMPLEMENTATION_PLAN.md` exists at the canonical path and is committed. `agents.md §2 triple_lock` names the approved plan as its first lock — approving one that lives only in a conversation approves nothing auditable. If it is absent, return to Phase 3 and file it; do not ask for approval first. Then request explicit Human OK before starting execution. **Must be a single manual invocation — never wrapped inside an unattended `/loop`.** |
| **6. Execution** | Subagents | Perform atomic tasks with commits referencing the Sprint ID, on branch `ai-sprint/[ID]` (never `main`). |
| **7. Quality Gate** | `qa_agent` → `tester_agent` | Gate 1 (Structural Audit & Graph Integrity Check) → Gate 2 (Functional Verification). On the third consecutive rejection of the same logic block, escalate to `workflows/remediation_workflow.md`. |
| **8. Sprint Closeout**| `principal_agent` | Update Blueprints, Global Roadmap, Walkthroughs, and the Master Ledger (host `CHANGELOG.md` `[Unreleased]` entry), including final Graph Rebuild via `make -f .agents/Makefile graphify-rebuild`. Then hand off to `workflows/close_workflow.md`. |

> [!NOTE]
> Phase 4 was a single row reading *"Summon Agent Orch, Skill Arch, and Rule Val"* until Phase 019. Three agents, three deliverables and no order were compressed into one cell with three abbreviations, so a reader looking for "where are the agents and skills assigned" concluded the step did not exist. `unambiguous_action` prohibits abbreviations where a proper name exists; the deliverables are named here because a phase that produces `task_scope.md` and never says so cannot be checked by anyone.

## 📐 Standards & Rules
- **Zero-Memory Initialization**: All subagents start with zero memory; read `active_state.json` first. The governance ruleset is auto-imported via the host `CLAUDE.md` — verify presence, re-read only after compaction (`anti_amnesia`).
- **Graph Sovereignty**: Query `graph.json` via MCP or CLI before any recursive grep codebase research.
- **Topographic Purity**: Prohibited to leave empty folders. Purge noise before closing.
- **Unique Naming**: All artifacts must follow the `[MODULE]_[TYPE].md` standard (Option B).
- **Context Limit**: Mandatory use of `omni_minimizer.py` for files >200 lines.
- **Branch Discipline (RA-12)**: All work happens on `ai-sprint/[ID]`, created in Phase 3 and pushed in `close_workflow.md` Phase 5. Only `deployment_workflow.md` merges to `main`.
- **`/loop` usage**: Claude Code's `/loop` skill MAY wrap Phases 6-8 (Execution → Quality Gate → Sprint Closeout) to advance a multi-sprint pipeline without manual re-invocation. It MUST NOT wrap Phase 5 (Approval Gate) — human authorization stays a single, attended invocation. **Arm the stop set before the first iteration** (`python3 .agents/scripts/loop_guard.py start --max-iterations N --success "<condition>"`) and run `loop_guard.py check` as the **first action of every iteration**; it fails closed on a missing or stale `loop` block. Full rule: `rules/loop_governance.md`.

---
*Optimized for Pipeline Symmetry & Infrastructure Hardening (v3.6.0) — adds Branch Discipline (RA-12) and `/loop` usage boundary.*
