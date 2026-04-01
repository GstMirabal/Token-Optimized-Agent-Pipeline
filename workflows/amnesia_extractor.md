---
description: "Post-Sprint Purgatory and Long-Term Memory Extraction Protocol"
version: 1.1.0
---

# 🧠 Workflow: Amnesia and Knowledge Extractor (V1.1)

This is the **Mandatory Closing Protocol** for all Universal-Agents sessions. To prevent cross-session hallucinations and save tokens, temporary state folders (`.agent_state/session_{UID}/`) must be destroyed. ## Phase 0: Transactional Integrity Cycle (Master Protocol)
Before concluding any session, the Orchestrator MUST execute the following atomic sequence to ensure data integrity and knowledge preservation:
1.  **Amnesia Extraction:** Run this workflow (Phases 1-4) to distill learning heuristics into persistent memory.
2.  **Indexing:** Update both global and local knowledge indexes to enable semantic search for future agents.
3.  **Final Atomic Commit:** Consolidate all changes (governance, roadmaps, and knowledge) into a single transactional commit in both the parent repository and the submodule.

This workflow ensures that "lessons learned" are distilled into the system's persistent memory before the session terminates.

## Phase 1: Retrospective Scanning (Brain Drain)
When the session is declared finished or `/save_knowledge` is triggered, the Orchestrator reads the local `task.md` and `task/sprints/` (Local Context) to identify:
1.  **Critical Workarounds:** Creative solutions to rebellious libraries or exotic environments.
2.  **Architectural Decisions:** Rationale for choosing specific patterns or tools (e.g., `uv` vs `pip`).
3.  **Resolved Complex Bugs:** Linter, Typing, or Logic errors that required multiple attempts to solve.

## Phase 2: Domain Audit (Global vs Project-Local)
Before saving, the Orchestrator MUST apply the **3-Variable Amnesia Test**:
*   **Global Knowledge:** If the lesson is universal (e.g., "FastAPI Pydantic V2 fix"), it is destined for `.agents/knowledge/`.
*   **Local Knowledge:** If the lesson is coupled to business logic or a specific project database, it is saved in the local **`.agents/roadmaps/`** folder (Ignored by Git).

## Phase 3: Markdown Distillation & Semantic Indexing
1.  **Distillation:** Create or update `.md` files in the chosen domain path.
    *   **Format:** Title, Context, The Blockage (Traceback), and The Solution (Snippets).
2.  **Semantic Indexing (Token-Saver):** Update the **`knowledge/ki_index.json`** (for global) or local index.
    *   **Action:** Add a 1-line summary and the file path. This allows future agents to search for keywords without reading dozens of Markdown files.

## Phase 4: Session Purge (Amnesia)
Once knowledge is indexed, the Orchestrator permanently deletes temporary session files:
```bash
rm -rf .agent_state/session_{UID}/
```
**Iron Rule:** It is strictly forbidden to maintain operational session folders from previous sessions.

## Phase 5: Central Matrix Update (Optional)
If the knowledge was marked as **Global**, the Orchestrator prepares the command for the human to commit the framework upgrade:
```bash
cd .agents
git add knowledge/
git commit -m "docs(knowledge): extract bugs and heuristics via amnesia protocol"
```

**Note:** Local `task.md` and `sprints/` are strictly ignored by Git and will remain in the local repository for future session re-entry.
