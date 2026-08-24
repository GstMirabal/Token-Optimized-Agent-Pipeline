# ♟️ Implementation Plan: Sprint 032 - Topological Flattening (Core Eradication)

## 🎯 Goal
Execute a massive topological refactor triggered by a user override to eradicate the `.agents/core/` namespace. The internal subsystems (`agents/`, `memory/`, `rules/`, `workflows/`) will be promoted directly to the root layer of the Matrix. This requires a systemic path refactoring across all governance manuals, scripts, and commands.

## 🧱 Components (Work Breakdown Structure)

### Component 1: Physical File System Migration
- **Target**: `.agents/core/`
- **Dependencies**: None.
- **Verification Gate**: The `core/` root directory must cease to exist, and its 4 native subdirectories (`agents`, `memory`, `rules`, `workflows`) must successfully reside at `.agents/`.

### Component 2: Constitutional & Topological Sync
- **Target**: `agents.md`, `docs/architecture/matrix_topology_map.md`
- **Dependencies**: Component 1.
- **Verification Gate**: `matrix_topology_map.md` must be updated to explicitly register `agents/`, `memory/`, `rules/`, and `workflows/` as root elements, dropping references to `core/...`. The Constitution (`AGENTS.md`) must reflect new paths for profile constraints (`[Principal Agent](agents/principal_agent.md)` vs `agents/...`).

### Component 3: Hook & Telemetry Redirection
- **Target**: `hooks/*.py`, `memory/memory_index.json`
- **Dependencies**: Component 1.
- **Verification Gate**: Telemetry nodes and git hooks must route correctly to `memory/telemetry/raw_errors.json` instead of `memory/telemetry/raw_errors.json`.

### Component 4: Command & Toolkit Arsenal Refactor ("Slash Commander")
- **Target**: `skills/...` (specifically `slash-commander` and `governance-sentinel`), `commands/*.ts`
- **Dependencies**: Component 1.
- **Verification Gate**: `generate_commands.py` must point to `Path("workflows")` directly. All generated `.ts` artifacts in `commands/` must replace `.agents/workflows/` with `.agents/workflows/`.

## 📋 Task Breakdown

| Task ID | Component | Description | Assignee Role | Status |
| :--- | :--- | :--- | :--- | :--- |
| `032-1` | File System Migration | Execute mechanical folder displacement (`mv core/* .` y `rm -rd core`). | DevOps Sentinel | COMPLETED |
| `032-2` | Constitutional Sync | Find & Replace all textual references of `core/agents/`, `core/memory/`, etc., in `agents.md` & `/docs/`. | Doc Orchestrator | COMPLETED |
| `032-3` | Python Hooks Refactor | Update `Path()` declarations across `hooks/telemetry.py` and other internal scripts to point to root elements. | Orchestrator | COMPLETED |
| `032-4` | Skill Engine Hardening | Update hardcoded paths in `governance-sentinel` (distill.py) and `slash-commander` (generate_commands.py). | Skill Architect | COMPLETED |
| `032-5` | Commands Re-generation | Trigger `python3 skills/core/slash-commander/scripts/generate_commands.py --sync` to refresh `.ts` endpoints. | Orchestrator | COMPLETED |

## 🧪 Verification Plan
- `git status` must confirm the massive namespace shift sin perder archivos.
- Un barrido general buscando `"workflows"` debe resultar en cero (0) hits dentro del código o los docs.
- Lanzar `/start` mecánicamente para certificar la habitabilidad de las nuevas rutas.
