# Rule Context: Graphify Sovereignty

Consult the graphify knowledge graph at `graphify-out/` for codebase and architecture questions (rung 1 of `rules/token_economy.md`).

## graphify

This project has a graphify knowledge graph at graphify-out/.

Rules:
- For codebase or architecture questions, when `graphify-out/graph.json` exists, first run `graphify query "<question>"` (CLI) or `query_graph` (MCP). Use `graphify path "<A>" "<B>"` / `shortest_path` for relationships and `graphify explain "<concept>"` / `get_node` for focused concepts. These return a scoped subgraph, usually much smaller than `GRAPH_REPORT.md` or raw grep output.
- If graphify-out/wiki/index.md exists, navigate it instead of reading raw files
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context
- After modifying code files in this session, run `graphify update .` to keep the graph current (AST-only, no API cost)
- **Known coverage gaps** (observed graphify 0.8.30, AST-only mode): `.yaml`/`.yml` files are never indexed (zero such nodes ever appear — not a bug in the repo, a language the extractor doesn't parse); isolated `.md`/empty-`__init__.py` nodes are normal (no cross-file link extraction for prose/empty files). One anomaly under active watch: `rules/token_economy.md` is silently skipped even after a full cache-less rebuild, while every sibling `rules/*.md` indexes fine — cause not isolated (not encoding, size, or syntax). Treat "absent from the graph" as inconclusive for these cases, not as "doesn't exist" — cross-check with `grep`/`git ls-files` before concluding a file is orphaned.
