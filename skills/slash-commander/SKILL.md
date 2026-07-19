---
name: slash-commander
description: Bridges .agents workflows to real Claude Code slash commands and audits that the link between commands/*.md and workflows/*.md never drifts.
---

# ☄️ Skill: Slash Commander

## 1. How the bridge actually works
Real Claude Code discovers slash commands by scanning `.claude/commands/**/*.md` in the host project root — there is no runtime generation step. The bridge is:

1. **Source of truth**: each `workflows/<name>_workflow.md` has a matching, hand-authored `commands/<name>.md` in this submodule (frontmatter `description` + a body that `@`-references the workflow file).
2. **Installation**: `.agents/scripts/install_claude.sh` symlinks `commands/<name>.md` into the host's `.claude/commands/agents/<name>.md`, which Claude Code then exposes as `/agents:<name>`.
3. **Drift check**: `scripts/verify_commands.py` (this skill) scans `commands/*.md` for `@.agents/workflows/...` references and fails if any points at a workflow file that doesn't exist. Run it after adding/renaming a workflow, or as part of `audit_workflow.md`'s `link_audit` step.

## 2. Command Mapping
| Workflow | Command | Slash invocation |
| :--- | :--- | :--- |
| `start_workflow.md` | `commands/start.md` | `/agents:start` |
| `close_workflow.md` | `commands/close.md` | `/agents:close` |
| `matrix_workflow.md` | `commands/matrix.md` | `/agents:matrix` |
| `extract_workflow.md` | `commands/extract.md` | `/agents:extract` |
| *(new workflow)* | new `commands/<name>.md` | `/agents:<name>` |

## 3. Constitutional Constraints
- **Isolation**: The installer MUST NOT overwrite anything under host `.claude/` that isn't already a symlink back into `.agents/` — it skips and warns on collisions instead.
- **Mirroring**: A change to a workflow file's `description` frontmatter should be reflected by hand in its paired `commands/<name>.md` (no auto-sync exists; `verify_commands.py` only checks the reference resolves, not that the description text matches).

## 4. Error Handling
- **Broken reference**: `verify_commands.py` exits non-zero and lists every command pointing at a missing workflow.
- **Bridge not installed**: if `.agents/.claude_bridge.lock` is missing, `hooks/on_init.py` triggers `install_claude.sh` automatically at session start.

---
*Optimized for Universal-Agents Rule 113.*
