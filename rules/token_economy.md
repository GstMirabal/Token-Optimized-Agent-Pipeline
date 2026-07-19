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

## 2. Plan-level Economics (enforced by Token-Saver Auditor)
- **1-Agent : 1-File**: subagent prompts receive the exact filename and line range — never "review the whole system".
- **No raw data dumps**: CSV/JSON datasets are summarized via a throwaway script (`.head()`, `.info()`), never pasted into context.
- **Delegate search to heuristics**: `ripgrep`/graph queries over manual directory crawling; recursive `list_dir` over an indexed tree is rejected (`matrix_topology_map.md` Discovery Lock).

## 3. Session-level Economics
- **Constitution loads once**: `agents.md` auto-loads via the host `CLAUDE.md` import; re-read it only after context compaction (`agents.md §2 anti_amnesia`), not per execution step.
- **State over rediscovery**: `docs/active_state.json` and `graphify-out/graph.json` are the memory — re-deriving what they already record is a violation, not diligence.
- **Workflows are lazy-loaded**: protocols live behind `/agents:*` commands and are only pulled into context when invoked.

## 4. Output Economics
- Markdown tables over prose for data (`agents.md §1 technical_clarity`); no redundant greetings; Mermaid/ASCII restricted to where a diagram genuinely replaces more text than it costs.
