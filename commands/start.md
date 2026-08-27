---
description: "Session-Start Protocol (Keyword: start)"
---

1. Run `python3 scripts/session_start.py --boot --tool cursor` (or `make session-start` for briefing-only). On exit `2`, run `/agents:reconcile` before Planning.
2. Hand off to the **Principal Agent** for pipeline Phase 1 (Planning). Binding steps are executed by `--boot`; full spec: `@workflows/start_workflow.md`.
