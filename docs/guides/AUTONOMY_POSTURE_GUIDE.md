# 🧭 How-to: Apply the autonomy posture
**File**: `docs/guides/AUTONOMY_POSTURE_GUIDE.md` (RA-06 Option B naming)
**Module**: CORE / PIPELINE

---

## 1. Goal
Replace `bypassPermissions` with a four-axis posture — **effectiveness, security, memory, drift** — where Claude Code settings accelerate guarantees that already live in portable scripts and git hooks, and Cursor sessions keep the same guarantees without those settings.

## 2. Prerequisites
- `.agents` installed as a submodule (or this nucleus clone)
- Bridge installed at least once: `.agents/scripts/install.sh --target claude` and/or `--target cursor`
- Sprint 027 scripts present: `persist_session_context.py`, `check_role_artifact.py`, `session_end_hook.py`

## 3. Steps

### 3.1 What is portable vs Claude-only

| Axis | Portable (both tools) | Claude Code only (acceleration) |
| :--- | :--- | :--- |
| Security | `pre-push` / `pre-commit` / `commit-msg` / `submodule_purity` | `autoMode.hard_deny`, sandbox, `permissions.deny` |
| Memory | Plan in sprint dir; `docs/active_state.json`; `session_state.py` | `PreCompact` / `PostCompact`; `plansDirectory`; file checkpointing |
| Drift | `config/artifact_registry.json` + close Phase 2.6 + `make role-artifacts` / `make verify` | `SubagentStop` → `check_role_artifact.py --from-hook` |
| Effectiveness | *(none — harness UX)* | `defaultMode: auto`, `autoAllowBashIfSandboxed` |

Binding rule: a control whose only instance is `settings.json` is not admitted as a framework guarantee.

### 3.2 Apply the template under Claude Code
1. From the **host** root: `.agents/scripts/install.sh --target claude`
2. Confirm merge: host `.claude/settings.json` gained `hooks.PreCompact`, `SubagentStop`, `SessionEnd`, and retained any host-only `permissions.deny` entries (re-install is additive; see `scripts/merge_json.py`).
3. Copy classifier posture to a scope Claude Code actually reads for auto mode:
   - Project `.claude/settings.json` still carries the template (deny floor, hooks, sandbox hints).
   - As of Claude Code ≥2.1.142 / ≥2.1.207, `permissions.defaultMode: "auto"` and the `autoMode` object are **honored from user or managed settings**, not from shared project settings. Promote `autoMode` + `defaultMode` into `~/.claude/settings.json` (or org managed settings) when you need the classifier live.
4. Keep `permissions.disableBypassPermissionsMode: "disable"` so friction cannot reopen bypass.
5. Hosts set their own `sandbox.network.allowedDomains` / write paths — never commit real host values into the public nucleus (`RA-15`).

### 3.3 What Cursor does instead
| Claude hook / key | Cursor counterpart |
| :--- | :--- |
| `PreCompact` | After compaction (or when context feels lost): `python3 .agents/scripts/persist_session_context.py`, then re-read `docs/active_state.json` and the printed `task_scope.md` |
| `SubagentStop` | No subagent primitive — run `make role-artifacts ROLE="<registry role>" SPRINT_DIR=docs/sprints/[ID]-[Stack]-[Layer]` at phase boundaries; close Phase 2.6 still refuses missing required artifacts |
| `SessionEnd` → suspend | `python3 .agents/scripts/session_state.py suspend` (never `release` mid-session) |
| `hard_deny` / sandbox / bypass lock | Git hooks + human `destructive_flags`; no Cursor equivalent for classifier or sandbox — declared gap, not silent omission |
| Effectiveness (`auto`) | Not portable — Cursor keeps its own approval UX |
| IDE Plan mode / `SwitchMode` | **PROHIBITED for Phase 1 (`RA-18`).** Cursor Plan mode cannot write `IMPLEMENTATION_PLAN.md`. Write that file in Agent mode at the canonical sprint path. A `~/.cursor/plans/` draft is input, not the lock |

**If** the session tool is `cursor`: treat Memory/Drift as protocol steps in `/agents:start` and close, not as settings that already ran.

## 4. Verify it worked
```bash
python3 -c "import json; h=json.load(open('.agents/claude/settings.hooks.json')); assert 'SubagentStop' in h['hooks']; assert h['permissions']['disableBypassPermissionsMode']=='disable'"
make role-artifacts ROLE="Orchestrator" SPRINT_DIR=docs/sprints/027-core-pipeline
python3 .agents/scripts/persist_session_context.py
```
Expected: first command exits `0`; `role-artifacts` exits `0` when `SPRINT_LOG.md` exists; persist prints the task_scope pointer and refreshes the mirror without sealing the sprint.

## 5. If something goes wrong
| Symptom | Likely cause | Fix |
| :--- | :--- | :--- |
| Bypass still available | `disableBypassPermissionsMode` missing or overridden in user settings | Set `"disable"` in the winning settings scope |
| Host deny rules vanished after install | Unexpected merge regression | Abort; run `tests/test_merge_json.py::test_merge_preserves_host_deny_and_adds_template_deny`; do not re-install until green |
| `autoMode` ignored | Project-only settings scope | Promote `autoMode` / `defaultMode` to `~/.claude/settings.json` or managed settings |
| `SessionEnd` sealed the sprint | Hook called `release` | Must call `session_end_hook.py` / `suspend` only |
| Cursor session weaker on Memory | Compact without protocol | Run `persist_session_context.py` and re-read the anchor |

---
*See also: `docs/roadmaps/core/pipeline/021-030-program-queue.md` Appendix Sprint 027 · `claude/settings.hooks.json` · `start_workflow.md`.*
