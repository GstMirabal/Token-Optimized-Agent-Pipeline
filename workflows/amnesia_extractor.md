---
description: "Post-Sprint Purgatory and Long-Term Memory Extraction Protocol"
version: 1.0.0
---

# 🧠 Workflow: Amnesia and Knowledge Extractor

This is the **Mandatory Closing Protocol** for all Universal-Agents Sprints. Since our architecture dictates that temporary state folders (`.agent_state/session_{UID}/`) must be destroyed to prevent cross-hallucinations and save tokens, this *Workflow* ensures "lessons learned" are distilled and pushed to the system's persistent memory (`/knowledge/`) before executing the physical deletion of the Cache.

## Phase 1: Retrospective Scanning (Brain Drain)
When the Director orders `/save_knowledge` or declares the Sprint as finished, the Orchestrator will read `task.md` and its command history cold, identifying:
1.  **Critical Workarounds:** Creative solutions to rebellious libraries (e.g., "FastAPI crashed with Pydantic V2, fixed by doing X").
2.  **Established Architecture:** (e.g., "Decided to use `envtoml` instead of `dotenv` for X reason").
3.  **Complex Bugs:** Linter or Typing errors that took more than 2 attempts to solve in the session.

## Phase 2: Markdown Distillation
The Orchestrator will create or update a file in the submodule path `.agents/knowledge/<sprint_topic>.md`.
The format demanded by the *Constitutional Agent* is implacable:
- **Title:** Brief and descriptive.
- **Context (1 paragraph):** What were we trying to do?
- **The Blockage:** What failed or what obstacle arose (include traceback error if applicable)?
- **The Solution (Snippets):** The pure code that fixed it.

## Phase 3: Session Purge (Amnesia)
Once validated and files are saved in `/knowledge/`, the Orchestrator will implacably delete temporary files (its own short-term mind):
```bash
rm -rf .agent_state/session_{UID}/
```
**Iron Rule:** It is strictly forbidden to maintain operational session folders from previous days. The project must remain immaculate.

## Phase 4: Central Matrix Update
Since `.agents/` works by distributing through Git Submodules, the Orchestrator will assemble the final command for the Director to consolidate the new knowledge globally so all other repositories inherit it:
```bash
cd .agents
git add knowledge/
git commit -m "docs(knowledge): extract bugs and heuristics from active session"
```

**Note for the Swarm:** This Workflow ensures that Universal-Agents wakes up tomorrow smarter than today, retaining vital knowledge without carrying temporary garbage, dead tokens, or operational hallucinations into the next session.
