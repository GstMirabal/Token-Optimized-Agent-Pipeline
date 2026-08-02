# Rule Context: Token Economy

Single reference for context-window economics. Consolidates the token-saving mandates previously scattered across `agents.md §2`, `token-saver-auditor`, `omni-context-minimizer`, and `graphify`. The `Token-Saver Auditor` skill enforces this rule when reviewing plans.

## 1. The Decision Ladder (cheapest first)
Before touching any source file, descend this ladder and stop at the first rung that answers the question:

| Rung | Tool | When | Approx. cost |
| :--- | :--- | :--- | :--- |
| **1. Graph query** | `graphify query "<question>"` / MCP `query_graph` | Architecture, relationships, "where is X used" | Scoped subgraph, smallest |
| **2. AST skeleton** | `omni_minimizer.py <file>` | Structure of one large file (classes, signatures) | ~10% of the file |
| **3. Targeted partial read** | `Read` with offset/limit, or `ripgrep` on the symbol | Inspecting one known function/range | Only the affected lines |
| **4. Full read** | `Read` entire file | Files **<200 lines only** | Full file |

Full-dumping a file >200 lines is PROHIBITED (`agents.md §2 token_saver`). Skipping rungs is only justified when a prior rung already returned the exact line range.

**Scope limit — the ladder governs discovery, never editing.** Rungs 1-3 answer *where* something is. They are not a substitute for reading the range you are about to modify: **the lines being edited are read first, every time**, and a graph query or a symbol grep does not discharge that. Without this limit the rule reads as licence to edit code nobody looked at, which is the most expensive kind of cheap.

## 2. Plan-level Economics (enforced by Token-Saver Auditor)
- **1-Agent : 1-File**: subagent prompts receive the exact filename and line range — never "review the whole system".
- **No raw data dumps**: CSV/JSON datasets are summarized via a throwaway script (`.head()`, `.info()`), never pasted into context.
- **Delegate search to heuristics**: `ripgrep`/graph queries over manual directory crawling; recursive `list_dir` over an indexed tree is rejected (`topology_map.md` Discovery Lock).

## 3. Session-level Economics
- **Constitution loads once**: `agents.md` auto-loads via the host `CLAUDE.md` import; re-read it only after context compaction (`agents.md §2 anti_amnesia`), not per execution step.
- **State over rediscovery**: `docs/active_state.json` and `graphify-out/graph.json` are the memory — re-deriving what they already record is a violation, not diligence.
- **Workflows are lazy-loaded**: protocols live behind `/agents:*` commands and are only pulled into context when invoked.

## 4. Tool-Result Economics

`§3` forbids re-deriving state that is already recorded. This section is about the other accumulation: tool call/response pairs piling up across a long session.

**The finding that reframes this whole rule.** Retaining full history is not expensive-but-safe; it is expensive **and less accurate**. Measured on a 50-task tool-using benchmark (*"Less Context, Better Agents"*, arXiv 2606.10209): full history completed **71.0%** of tasks using 1.48M tokens; pruning to the last 5 tool calls reached **79.0%** with 535K; pruning plus summarisation reached **91.6%** with 553K. Roughly **−63% tokens and +20 points of task completion**. Old tool results describe superseded states, and an agent reading them assigns values to fields that have already changed.

So token economy is not only about cost. It preserves accuracy, and that is the stronger argument for it.

**What is actually controllable here**, stated plainly because the alternative is a rule the framework cannot execute: Claude Code manages its own context window and compaction — this rule cannot prune it. It governs what the agent *adds back*:
- **Do not re-emit a tool result already in the session.** Re-running a command to re-read its output is re-derivation (`§3`).
- **Do not re-read a file already read this session** unless it changed.
- **What crosses a compaction boundary is the state anchor plus `task_scope.md`, never the raw log.** Those two are the summary; reconstructing from transcript is what the anchor exists to prevent.

## 5. Output Economics
- Markdown tables over prose for data (`agents.md §1 technical_clarity`); no redundant greetings; Mermaid/ASCII restricted to where a diagram genuinely replaces more text than it costs.
