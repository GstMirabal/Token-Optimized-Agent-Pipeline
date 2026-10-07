---
description: "Session-Start Protocol (Keyword: start)"
---

1. Run the boot from the repository root, in the form that matches where this framework sits:

   | Workspace | Command | Briefing only |
   | :--- | :--- | :--- |
   | **Host** (`.agents/` is a submodule) | `python3 .agents/scripts/session_start.py --boot --tool claude-code` | `make -f .agents/Makefile session-start` |
   | **Nucleus** (this repository is `.agents` itself) | `python3 scripts/session_start.py --boot --tool claude-code` | `make session-start` |

   Append `--session-id <UID>` when the harness exposes one — Claude does; Cursor's rendered copy omits it, since Cursor exposes no session id. On exit `2`, run `/agents:reconcile` before Planning. A host has no `scripts/session_start.py` at its own root, so the nucleus form fails there with `can't open file` (`F-115-N3`, Sprint 054).

   The `--tool` value above is **rendered per harness** and must not be edited to match the session you happen to be in: Claude reads this file through a symlink and gets `claude-code`; Cursor reads a copy that `scripts/cursor_adapter.py` rewrites to `cursor`. It claims the anchor's `session_tool`, which decides whether `session_cost.py` measures at all and whether `RA-18` and the Cursor dispatch rules apply — so a wrong value silently misconfigures the whole sprint (Sprint 041).
2. Hand off to the **Principal Agent** for pipeline Phase 1 (Planning). Binding steps are executed by `--boot`; full spec: `@workflows/start_workflow.md`.
