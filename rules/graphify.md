# Rule Context: Graphify Sovereignty

Consult the graphify knowledge graph at `graphify-out/` for codebase and architecture questions (rung 1 of `rules/token_economy.md`).

## graphify

This project has a graphify knowledge graph at graphify-out/.

**Invocation form — always the module, never the console-script.** Run
`<checkout>/venv_skillopt/bin/python -m graphify <cmd>` (host: `.agents/venv_skillopt/bin/python -m graphify …`). The `venv_skillopt/bin/graphify` console-script carries an absolute shebang to the venv's build path and fails with `bad interpreter` whenever `.agents` sits at a path other than where the venv was created (submodule checkout, copied tree, renamed nucleus). `venv_skillopt/bin/python` is a symlink to the system interpreter and resolves under any path, so the `-m graphify` form works where the bare `graphify` command does not. `scripts/check_venv_relocatable.py` (run by `start_workflow.md` `pip_setup`) exits `2` when the venv itself is stale and must be rebuilt.

Rules:
- For codebase or architecture questions, when `graphify-out/graph.json` exists, first run `venv_skillopt/bin/python -m graphify query "<question>"` (CLI) or `query_graph` (MCP). Use `… -m graphify path "<A>" "<B>"` / `shortest_path` for relationships and `… -m graphify explain "<concept>"` / `get_node` for focused concepts. These return a scoped subgraph, usually much smaller than `GRAPH_REPORT.md` or raw grep output.
- If graphify-out/wiki/index.md exists, navigate it instead of reading raw files
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context
- After modifying code files in this session, run `venv_skillopt/bin/python -m graphify update .` to keep the graph current (AST-only, no API cost). If `graphify update` exits non-zero or the harness sandbox denies it, report `⚠️ graph unavailable (sandbox/venv)` to the human and proceed without graph sovereignty for the session — do not silently fall back to recursive grep as though the graph were current.
- **Known coverage gaps** (observed graphify 0.8.30, AST-only mode): `.yaml`/`.yml` files are never indexed (zero such nodes ever appear — not a bug in the repo, a language the extractor doesn't parse); isolated `.md`/empty-`__init__.py` nodes are normal (no cross-file link extraction for prose/empty files). One anomaly under active watch: `rules/token_economy.md` is silently skipped even after a full cache-less rebuild, while every sibling `rules/*.md` indexes fine — cause not isolated (not encoding, size, or syntax). Treat "absent from the graph" as inconclusive for these cases, not as "doesn't exist" — cross-check with `grep`/`git ls-files` before concluding a file is orphaned.
