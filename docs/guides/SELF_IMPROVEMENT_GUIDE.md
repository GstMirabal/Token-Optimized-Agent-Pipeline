# How to create agents and profiles without breaking strict_rule

**Last Audit Sprint**: 028
**Last Audit Date**: 2026-08-25
**Last Audit Commit SHA**: pending close

---

## Goal

Enable a host to improve itself — new agents, family profiles, preserved memory —
without writing into the `.agents` submodule (`agents.md §3 strict_rule`).

## Prerequisites

- Host has `.agents` installed (`scripts/install.py` or `install.sh`).
- You know whether the artifact is **host-only**, **project-family**, or **framework-wide**.

## Steps

### 1. Create a host-only agent (default)

1. Choose destination **(a)** from `agents/agent_orchestrator.md` `agent_forge_destination`.
2. Write `.claude/agents/<name>.md` with valid frontmatter (`name`, `description`, `tools`, `model`, `tier`).
3. Record `Destination: host:.claude/agents/` in the sprint's `agent_assignment.md` (Phase 4.1).
4. Claude Code discovers it natively — no submodule change.

### 2. Create a project-family profile (production)

1. Scaffold a directory **outside** the submodule — convention `<host-root>/.agents-profile/`:

   ```
   .agents-profile/
   ├── agents/
   ├── skills/   (optional)
   ├── rules/    (optional)
   └── mcp/registry.json   (optional)
   ```

2. Install:

   ```bash
   .agents/scripts/install.sh --profile-path .agents-profile
   ```

3. Never commit real profiles to the public nucleus (`RA-15`).

### 3. Promote to the framework (nucleus)

Only via a **separate clone/PR** of the `.agents` repository:

| Check | Requirement |
| :--- | :--- |
| Genericize | `RA-15` — no host names, absolute paths, or business thresholds |
| Invocation | `RA-16` — `invoked_by:` on workflows/scripts; exceptions typed in `config/invocation_exceptions.json` |
| Agents | New nucleus agents land in `agents/` via PR, not from a host session |

### 4. Route memory before close

During `/agents:extract` (`extract_workflow.md`):

1. Assign **`routing_class`** to every candidate KI: `host` | `profile` | `nucleus` | `discard`.
2. Index only `host`-class items into `memory_index.json`.
3. `profile`-class → draft into your profile pack; `nucleus`-class → upstream PR.
4. Close Phase 2.5 confirms the list; Phase 3 purge refuses unclassified loss.

## Verify it worked

```bash
# Host agent exists and is linked
test -f .claude/agents/your_agent.md

# External profile linked
.agents/scripts/install.sh --profile-path .agents-profile
test -L .claude/agents/your_agent.md

# Submodule untouched after host-only work
git -C .agents status --porcelain   # must be empty
```

## If something goes wrong

| Symptom | Remedy |
| :--- | :--- |
| Host wrote into `.agents/` | Revert; use host `.claude/agents/` or upstream PR |
| Profile not found | Pass absolute path or path relative to host root to `--profile-path` |
| Memory purged without routing | Re-run extract; unclassified items block close (Sprint 028) |

## References

- `agents/agent_orchestrator.md` — `agent_forge_destination`
- `workflows/skill_forge_workflow.md` — parallel for skills
- `workflows/extract_workflow.md` — `routing_class`
- `docs/guides/AUTONOMY_POSTURE_GUIDE.md` — harness-specific acceleration
