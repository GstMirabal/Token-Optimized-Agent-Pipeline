---
description: "Execution Pipeline Protocol (Keyword: pipeline)"
version: 3.6.0
invoked_by: human:/agents:pipeline, start_workflow.md#pipeline_invocation
---

# 🛡️ Workflow: Pipeline (Execution Pipeline)

Master operational protocol ensuring rigid task delegation, automated Double-Gate verification, and infrastructural stability.

## 🚀 The Execution Pipeline

| Phase | Role (advisory) | Deliverable / Done-criterion |
| :--- | :--- | :--- |
| **1. Planning** | `principal_agent` | **Deliverable**: `IMPLEMENTATION_PLAN.md` at `docs/sprints/[Sprint_ID]-[Stack]-[Layer]/IMPLEMENTATION_PLAN.md` (`config/artifact_registry.json`, Phase 1). **Done-criterion**: plan drafted from `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md`, filed at Phase 3, and **committed before Phase 5** (`agents.md §2 triple_lock` lock 1). Where the environment offers planning mode, Phase 1 runs in it; what is verifiable is the committed file, not which editor produced it. A plan drafted outside this workflow enters here once approved and does not skip Phases 3–5. `docs/plans/` is a safety net against loss, not the canonical path. |
| **2. Environment Readiness** | `devops_agent` | **Deliverable**: none (precondition). **Done-criterion**: activate `venv`, export `.env` without reading it into context (`RA-09`), and confirm Docker/DB health when the sprint touches them. |
| **3. Roadmap Drafting** | `orchestrator` | **Deliverable**: `SPRINT_LOG.md` at `docs/sprints/[Sprint_ID]-[Stack]-[Layer]/SPRINT_LOG.md` (`config/artifact_registry.json`, Phase 3). **Done-criterion**: instantiate the sprint directory, extract Phase 1's plan into `IMPLEMENTATION_PLAN.md` and commit it, create and check out branch `ai-sprint/[ID]` from base (`RA-12`) before any other commit. |
| **4.1 Agent Assignment** | `agent_orchestrator` | **Deliverable**: `agent_assignment.md` at `docs/sprints/[Sprint_ID]-[Stack]-[Layer]/agent_assignment.md` (`config/artifact_registry.json`, Phase 4.1). **Done-criterion**: every roadmap step names an assignee. When a step **creates** a new agent profile, the table MUST also record **`Destination`**: `host:.claude/agents/` (default), `profile:<path>` (project-family pack outside the submodule), or `nucleus:PR` (framework-wide via nucleus contribution — never from a host write into `.agents/`). Values mirror `agents/agent_orchestrator.md` `agent_forge_destination`. A session that cannot dispatch subagents still writes the file, recording which profile's ruleset governed each write. |
| **4.2 Skill Assignment** | `skill_architect` | **Deliverable**: `skill_assignment.md` at `docs/sprints/[Sprint_ID]-[Stack]-[Layer]/skill_assignment.md` (`config/artifact_registry.json`, Phase 4.2). **Done-criterion**: every step has tools resolved; skills deliberately not used are recorded beside those used. |
| **4.3 Rule Audit** | `rule_validator` | **Deliverable**: `task_scope.md` at `docs/sprints/[Sprint_ID]-[Stack]-[Layer]/task_scope.md` (`config/artifact_registry.json`, Phase 4.3). **Done-criterion**: table shape `# \| File \| Operation \| Risk \| Assignee \| Model \| Effort \| Status` when `session_tool: cursor` (otherwise `# \| File \| Operation \| Risk \| Assignee \| Status`); when `session_tool: cursor`, run `make cursor-tiers` in the same session immediately before writing or revising `Model`/`Effort`, quote the measured block in `task_scope.md`, and transcribe `token_economy_agent` proposals from that catalogue — never copy `claude_code` aliases from `config/model_tiers.json` (`F-20260825-027`); `jurisdictional_lock` and `no_interference` both read this file — skipping Phase 4.3 disables them while they still appear enforced. |
| **5. Approval Gate** | `principal_agent` | **Deliverable**: none (human authorization). **Done-criterion**: verify `IMPLEMENTATION_PLAN.md` exists at the canonical path and is committed; if absent, return to Phase 3 — do not ask for approval first. Then request explicit Human OK. **Must be a single manual invocation — never wrapped inside an unattended `/loop`.** |
| **6. Execution** | Subagents | **Deliverable**: atomic commits on `ai-sprint/[ID]` (never `main`), each referencing the Sprint ID (`RA-12`, `agents.md §5 historical_log`). **Done-criterion**: one physical file per commit where `jurisdictional_lock` applies; rows in `task_scope.md` move to `✅ <sha>` as units land. |
| **7. Quality Gate** | `qa_agent` → `tester_agent` | **Deliverable**: gate verdicts transcribed to `SPRINT_LOG.md` by `orchestrator` (gates emit; they do not write — `config/artifact_registry.json` names Orchestrator as `SPRINT_LOG.md` owner). **Done-criterion**: Gate 1 (structural audit and graph integrity) then Gate 2 (functional verification). On the third consecutive rejection of the same logic block, escalate to `workflows/remediation_workflow.md`. |
| **8. Sprint Closeout** | `principal_agent` | **Deliverables**: `PHASE_REGISTER.md` at `docs/sprints/[Sprint_ID]-[Stack]-[Layer]/PHASE_REGISTER.md` (`config/artifact_registry.json`, Phase 8); host `CHANGELOG.md` `[Unreleased]` entry (`config/artifact_registry.json`, repository scope). **Done-criterion**: update Blueprints, Global Roadmap, Walkthroughs, and the Master Ledger; rebuild graph via `make -f .agents/Makefile graphify-rebuild`; hand off to `workflows/close_workflow.md`. |

> [!NOTE]
> **Role (advisory) governs who drafts, never whether a gate runs in fresh context.** Under Cursor's `delegation_mode: sequential` the same gate phases remain mandatory; only subagent dispatch is unavailable. The precedent that makes this non-negotiable: a host ran the pipeline in a single agent, Phases 4 and 7 never ran, `task_scope.md` was not produced, and that silently disabled `jurisdictional_lock` and `no_interference` across ~30 edits; when the gates finally ran, both rejected the branch over HIGH defects of exactly the class the sprint existed to remove (`docs/roadmaps/core/pipeline/021-030-program-queue.md`, lines 974–978, Obstacle 2). **Fresh-context gate execution is required under both tools** — advisory role assignment is not an exemption.

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
