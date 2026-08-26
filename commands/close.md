---
description: "Session-Close Protocol (Keyword: close)"
---

Execute the protocol defined in @.agents/workflows/close_workflow.md

After `SESSION LOCKED` and `session_state.py release` on `ai-sprint/[ID]`
(branch still unmerged), continue **this same turn** with
@.agents/workflows/deployment_workflow.md (`/agents:deployment`). Stop before
that handoff only when the human says so, or when status is `SUSPENDED`
(`require-released` already refuses deploy). Do not leave the sprint at
"awaiting `/agents:deployment`".
