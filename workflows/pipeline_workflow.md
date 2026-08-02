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
| **1. Planning** | Principal | Drafts Implementation Plan (IP) based on User Request. |
| **2. Environment Readiness** | **DevOps** | **MANDATORY**: Activate `venv`, export `.env`, check Docker/DB health. |
| **3. Roadmap Drafting** | Orchestrator | Drafts Initial Roadmap and instantiates `docs/sprints/[ID]-[Stack]-[Layer]/`. **Also creates and checks out branch `ai-sprint/[ID]` from the base branch** (RA-12 Branch Discipline) — no commit may happen before this branch exists. |
| **4. Roadmap Review** | Review Group | Summon Agent Orch, Skill Arch, and Rule Val to finalize IP and skills. |
| **5. Approval Gate** | Principal | Request explicit Human OK before starting execution. **Must be a single manual invocation — never wrapped inside an unattended `/loop`.** |
| **6. Execution** | Subagents | Perform atomic tasks with commits referencing the Sprint ID, on branch `ai-sprint/[ID]` (never `main`). |
| **7. Quality Gate** | QA & Tester | Gate 1 (Structural Audit & Graph Integrity Check) -> Gate 2 (Functional Verification). |
| **8. Sprint Closeout**| Principal | Update Blueprints, Global Roadmap, Walkthroughs, and the Master Ledger (host `CHANGELOG.md` `[Unreleased]` entry), including final Graph Rebuild via `make -f .agents/Makefile graphify-rebuild`. |

## 📐 Standards & Rules
- **Zero-Memory Initialization**: All subagents start with zero memory; read `active_state.json` first. The governance ruleset is auto-imported via the host `CLAUDE.md` — verify presence, re-read only after compaction (`anti_amnesia`).
- **Graph Sovereignty**: Query `graph.json` via MCP or CLI before any recursive grep codebase research.
- **Topographic Purity**: Prohibited to leave empty folders. Purge noise before closing.
- **Unique Naming**: All artifacts must follow the `[MODULE]_[TYPE].md` standard (Option B).
- **Context Limit**: Mandatory use of `omni_minimizer.py` for files >200 lines.
- **Branch Discipline (RA-12)**: All work happens on `ai-sprint/[ID]`, created in Phase 3 and pushed in `close_workflow.md` Phase 5. Only `deployment_workflow.md` merges to `main`.
- **`/loop` usage**: Claude Code's `/loop` skill MAY wrap Phases 6-8 (Execution → Quality Gate → Sprint Closeout) to advance a multi-sprint pipeline without manual re-invocation. It MUST NOT wrap Phase 5 (Approval Gate) — human authorization stays a single, attended invocation.

---
*Optimized for Pipeline Symmetry & Infrastructure Hardening (v3.6.0) — adds Branch Discipline (RA-12) and `/loop` usage boundary.*
