---
description: "Session-Start Protocol (Keyword: start)"
---

1. Run `python3 scripts/session_start.py --boot --tool claude-code` (or `make session-start` for briefing-only). On exit `2`, run `/agents:reconcile` before Planning.

   The `--tool` value above is **rendered per harness** and must not be edited to match the session you happen to be in: Claude reads this file through a symlink and gets `claude-code`; Cursor reads a copy that `scripts/cursor_adapter.py` rewrites to `cursor`. It claims the anchor's `session_tool`, which decides whether `session_cost.py` measures at all and whether `RA-18` and the Cursor dispatch rules apply — so a wrong value silently misconfigures the whole sprint (Sprint 041).
2. Hand off to the **Principal Agent** for pipeline Phase 1 (Planning). Binding steps are executed by `--boot`; full spec: `@workflows/start_workflow.md`.
