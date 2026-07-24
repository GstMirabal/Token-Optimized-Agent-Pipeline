# 🧭 System Overview: {{PROJECT_NAME}}
**Last Audit Sprint**: #{{SPRINT_ID}}
**Last Audit Date**: {{ISO_DATE}}
**Last Audit Commit SHA**: {{COMMIT_SHA}}

This is the **Zero Coordinate entry point**. `agents.md §0 (Matrix Entry)` requires every session to read this file before anything else. It is intentionally short — for the full component inventory, see `.agents/docs/architecture/matrix_topology_map.md`.

---

## 1. What this is
This project uses the **Universal-Agents (`.agents`)** framework as a git submodule: a constitutional layer that governs how AI subagents plan, execute, and hand off work here.

## 2. Architecture at a glance (C4 Level 1-2)

**Level 1 — Context**: this system and who/what it talks to outside its own boundary.

```
{{C4_CONTEXT_DIAGRAM}}
```

**Level 2 — Container**: the deployable pieces this system is built from (backend, frontend, datastores, workers).

```
{{C4_CONTAINER_DIAGRAM}}
```

Component-level (Level 3) detail, where required, lives per-module in the relevant `[MODULE]_BLUEPRINT.md` — see `rules/documentation_standard.md §2.1` for which modules require it.

## 3. The constitutional hierarchy
| Layer | Location | Role |
| :--- | :--- | :--- |
| **Constitution** | `.agents/agents.md` | The absolute, transversal rules. Nothing overrides this. |
| **Rules** | `.agents/rules/*.md` | Domain-specific standards (QA, topology, skills, security, documentation). |
| **Workflows** | `.agents/workflows/*.md` | Step-by-step protocols, invoked as `/agents:<name>` slash commands. |
| **Subagents** | `.agents/agents/*.md` | The roles that execute workflow steps (Principal, Orchestrator, QA, Tester, etc.). |
| **Skills** | `.agents/skills/*/` | Concrete tools subagents call into (linters, scaffolders, auditors). |

## 4. How a session starts
Run `/agents:start`. It will:
1. Read `agents.md` and this file (Zero-Memory anchor).
2. Install/verify the Claude Code bridge (`.agents/scripts/install_claude.sh`) if not already done.
3. On a brand-new project, scaffold `docs/active_state.json` and the rest of the `docs/` tree — see `.agents/workflows/start_workflow.md`.
4. Hand off to the Principal Agent for Strategic Genesis (drafting the Implementation Plan with you).

## 5. Where state lives
- `docs/active_state.json` — this project's own session anchor (git-ignored, host-specific, never committed to `.agents`).
- `CHANGELOG.md` (root) — the **Master Ledger**: sprint entries at close, version seals at deployment.
- `docs/roadmaps/`, `docs/sprints/` — this project's own tactical history.
- `.agents/docs/` — the framework's own (separate) self-documentation; not this project's (its changelog is `.agents/CHANGELOG.md`, a different jurisdiction).

## 6. Full inventory
For the detailed component-by-component map (what lives where inside `.agents/`, current status of each piece), read `.agents/docs/architecture/matrix_topology_map.md`.
