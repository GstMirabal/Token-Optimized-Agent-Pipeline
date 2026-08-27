---
description: "Session-Start Protocol (Keyword: start)"
version: 6.6.0
invoked_by: human:/agents:start
---

# Workflow: Start (Pipeline Initiation)

## Operator path (token-cheap)

| # | Action |
| :--- | :--- |
| 1 | Run `python3 scripts/session_start.py --boot --tool cursor` (Claude: `--tool claude-code`; terminal: `--tool terminal`). Executes **drift → claim → probe → sync → bridge**, then prints a ≤80-line briefing. Drift exit `2` propagates (no claim). No network. No `.env`. No full UPSTREAM dump. Briefing-only (compat): omit `--boot` or `make session-start`. |
| 2 | Read that briefing. On exit `2`, run `/agents:reconcile` before handoff. |
| 3 | Hand to **Principal Agent** for pipeline Phase 1. Binding table below is the spec; `--boot` is the measurable invoker (`RA-16`). |

Host paths below use `.agents/…`; **nucleus** resolves the same scripts at repo root (`scripts/…`, `./venv_skillopt/`).

## Binding steps

| Phase | Step | Action / Constraint |
| :--- | :--- | :--- |
| **0. Zero-Memory** | `read_anchor` | First: load `docs/active_state.json`. If `.agent_state/mirror.json` disagrees, **anchor wins** — resync (`python3 .agents/hooks/state_mirror.py`) and continue. Mirror is authoritative only when the anchor is missing/corrupt. |
| **0. Zero-Memory** | `read_ruleset` | Then read `agents.md` + `docs/0_SYSTEM_OVERVIEW.md`. **Nucleus:** overview is host-only — read `agents.md` + `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` (`agents.md §0`). |
| **0. Zero-Memory** | `pip_setup` | If `.agents/installed.lock` missing: create `.agents/venv_skillopt/`, `pip install -r .agents/requirements-core.txt`, write the lock (ISO timestamp + requirement set). Skillopt stack installs on demand. |
| **0. Zero-Memory** | `read_graph` | Skip graph on tiny hosts (<~25 sources). Else build/query `graphify-out/graph.json` via `.agents/venv_skillopt/bin/graphify update .` or MCP/CLI. |
| **0.4 Drift** | `drift_check` | **Before `state_claim`.** `python3 .agents/scripts/detect_drift.py` — verdict, not boolean (ADR-0002). Against sealing tags (`## [X.Y.Z]`): **`S`** covered → `0`; **`M`/`U`/`A`/`R`** → `2` → `/agents:reconcile` before Phase 2. Orphaned baseline (squash-merge) falls back to merge-base and says so. No baseline yet → reports and passes. Under `--boot`, exit `2` stops the boot (no claim). |
| **0.5 Claim** | `state_claim` | `python3 .agents/scripts/session_state.py claim` — sets `IN_PROGRESS`, `session_id`, `session_tool`, `start_time`, mirror. `--session-id` optional (default mint `UTC-PID`); `--tool` `claude-code\|cursor\|terminal` (default `terminal`); `--delegation-mode` optional `native\|sequential` (else derived: `cursor`→`sequential`, else `native`). **Named:** Claude → `--session-id <UID> --tool claude-code`; Cursor → `--tool cursor` (no UID); terminal → `--tool terminal`. Exit `2` if another session holds the lock; `--takeover` is manual. |
| **0.6 Probe** | `readiness_probe` | `python3 .agents/scripts/session_probe.py` — **advisory only**. Flags stale graph, missing docs, **anchor sprint ≠ checked-out `ai-sprint/[ID]`** (branch, not newest `docs/sprints/` dir), and (Sprint 039) `IN_PROGRESS` with `current_sprint.status=CLOSED` or `resume_pointer.branch` ≠ `HEAD`. Gaps accepted by humans live in `acknowledged_gaps`. May propose `/agents:revdoc` (needs `triple_lock`). |
| **0.7 Probe** | `platform_probe` | Same script. Secret scanning, Dependabot, branch protection, community files (tree, never `community/profile`). Cached 7d via `last_platform_probe`. Skip if no `gh` / non-GitHub. May propose `/agents:harden`. |
| **1. Guard** | `session_lock_check` | Abort if `IN_PROGRESS` under a **different** `session_id`. **`SUSPENDED` = resume** (read plan, `task_scope.md`, `resume_pointer`). **Nucleus:** Phase 0 + `lightweight_sync` run; `.agents/`-prefixed paths → repo root. Of Phase 1.5, **only `first_run_scaffold` is PROHIBITED** (`nucleus_neutrality`). `bridge_check` **runs** in nucleus (not scaffolding — `install_nucleus_bridge()`). |
| **1. Sync** | `lightweight_sync` | `python3 .agents/scripts/sync_agents_pin.py` (nucleus: `python3 scripts/sync_agents_pin.py`). Ping `git fetch --tags` (20s, `GIT_TERMINAL_PROMPT=0`); unreachable → keep pin, continue. Newer **version tag** (`vX.Y.Z`) than `describe --tags --abbrev=0` → **auto-checkout that tag** (tags only, never `main`). Dirty `.agents` while behind → exit `2`, do not overwrite. Nucleus: no-op when `describe` ahead of latest tag. After bump, `bridge_check` re-links. Host gitlink stays dirty until host commits the pin. Prints `.agents/CHANGELOG.md`. Exit `2` → stop Phase 2 until clean. |
| **1.5 Bridge** | `bridge_check` | Cursor / Claude: when **this target's** lock is missing, lock commit ≠ framework `HEAD`, linked artifacts under `.claude/` / `.cursor/` are gone, or (Cursor) `commands_stale()` — digests diverge (Sprint 039). **Sprint 040 triage:** (a) lock stale and commands **fresh** → refresh `.bridge_<target>.lock` only (no install); (b) commands stale or mirror missing → `install.sh --target …` **incremental** (no happy-path `rmtree` of `.cursor/`); (c) install `PermissionError` on `.cursor` → **advisory** in briefing, boot exit `0` (run install outside the agent sandbox). Other install failures still exit `2`. Locks are independent per target. Host: `hooks/on_init.py` often covers this. **Nucleus:** `--boot` runs this triage. |
| **1.5 Bridge** | `first_run_scaffold` | If `docs/active_state.json` missing: load Onboarding Scenario Matrix (`standardization_workflow.md` Phase 6) before Phase 2. **Nucleus: PROHIBITED.** |
| **1.6 Cursor** | `cursor_memory_drift` | When `session_tool` is `cursor`: after compaction (or resume without sprint path), run `persist_session_context.py`, re-read anchor + `task_scope.md`; use `make role-artifacts` as Drift check. No Cursor counterpart to Claude `defaultMode: auto`. See `docs/guides/AUTONOMY_POSTURE_GUIDE.md`. |
| **2. Handoff** | `pipeline_invocation` | Hand to **Principal Agent** for pipeline Phase 1 (Planning). **Under `session_tool: cursor`, do not `SwitchMode` to plan (`RA-18`); write `IMPLEMENTATION_PLAN.md` at the canonical sprint path in this session.** |
| **2. Handoff** | `delegation_conflict` | Read `delegation_mode` from the anchor. Recorded `sequential` under Cursor is **configuration, not an incident** (Cursor cannot spawn the 8 roles). **Report only when declared mode and capability diverge:** if `native` but this agent cannot delegate, report to the human before Phase 1 and await a decision. Silent self-substitution for the pipeline is PROHIBITED. |

---
*Start v6.6.0 — operator path = `session_start.py --boot`; bridge triage = lock-only / incremental install / PermissionError advisory (Sprint 040).*
