# Rule Context: Graphify Sovereignty

Consult the graphify knowledge graph at `graphify-out/` for codebase and architecture questions (rung 1 of `rules/token_economy.md`).

## graphify

This project has a graphify knowledge graph at graphify-out/.

**Invocation form — always the module, never the console-script.** Run
`<checkout>/venv_skillopt/bin/python -m graphify <cmd>` (host: `.agents/venv_skillopt/bin/python -m graphify …`). The `venv_skillopt/bin/graphify` console-script carries an absolute shebang to the venv's build path and fails with `bad interpreter` whenever `.agents` sits at a path other than where the venv was created (submodule checkout, copied tree, renamed nucleus). `venv_skillopt/bin/python` is a symlink to the system interpreter and resolves under any path, so the `-m graphify` form works where the bare `graphify` command does not. `scripts/check_venv_relocatable.py` (run by `start_workflow.md` `pip_setup`) exits `2` when the venv itself is stale and must be rebuilt.

## Deep mode and the provider key (Sprint 055)

`graphify update .` is AST-only and needs no key. `graphify extract . --mode deep` calls an LLM provider and needs a key in the process environment. Sandbox behaviour for every command below is in the single table `rules/project_topology.md` section 4; this section does not restate it.

| Item | Fact |
| :--- | :--- |
| **Variables read** | graphifyy 0.8.30 reads 7 provider variables, from the environment only: `ANTHROPIC_API_KEY`, `DEEPSEEK_API_KEY`, `GEMINI_API_KEY`, `GOOGLE_API_KEY`, `MOONSHOT_API_KEY`, `OLLAMA_API_KEY`, `OPENAI_API_KEY`. |
| **Reproduce the list** | `grep -rhoE '[A-Z_]+_API_KEY' <venv site-packages>/graphify` |
| **`.env` loader** | None. graphify never opens `.env`; a key that lives only in `.env` is invisible to it (`GKEY` = 0 variables visible). |
| **Vendored claim superseded** | `skills/graphify/SKILL.md:238` states that only `GEMINI_API_KEY` / `GOOGLE_API_KEY` are read. The measured list above supersedes it. That file is vendored and is not edited (`rules/skills_and_integrations.md` section 3). |
| **Agent form (inside the sandbox)** | Host only: the `graphify-extract-deep` line that `scripts/install.py` renders into `.claude/settings.local.json`, shaped `<absolute python3> -I <absolute host path>/.agents/scripts/with_env.py graphify-extract-deep`, copied from that file and run verbatim; the other names are `graphify-extract` and `graphify-label`. The cwd-relative spelling `python3 -I .agents/scripts/with_env.py graphify-extract-deep` is not excluded and fails on the `.env` deny by design. The wrapper loads `.env` outside the sandbox and exports the value to the child. Masking of exact `.env` values of length >= 4 in the child's output is NOT a security boundary (encoded or split values, files the child writes and shorter values pass unmasked); the boundary is that only the rendered absolute lines are excluded and what they execute is write-denied (`rules/project_topology.md` section 4). The nucleus has no rendered line: see the human form. |
| **Human form (unsandboxed shell)** | Nucleus: `make graphify-deep` (the only form there). Host: `make -f .agents/Makefile graphify-deep`. An agent does not use this target: a `make` target that calls the wrapper is not matched by `sandbox.excludedCommands`. |
| **Allowlist** | `config/with_env_allowlist.json` lists `graphify-extract`, `graphify-extract-deep` and `graphify-label`. It is nucleus-only: a host does not extend it (`rules/project_topology.md` section 4). The wrapper, the allowlist and the interpreter tree (`.agents/venv_skillopt`) are write-denied. |
| **`.env` stat (`S-4`)** | The sandbox `.env` deny also refuses `stat()`. `graphify update .` succeeded in the nucleus because graphify skips names equal to `.env`; a host with other `.env*` names, or any full-tree walker, can fail. Sanctioned form: run the walker unsandboxed (human) or scope it. |

Rules:
- For codebase or architecture questions, when `graphify-out/graph.json` exists, first run `venv_skillopt/bin/python -m graphify query "<question>"` (CLI) or `query_graph` (MCP). Use `… -m graphify path "<A>" "<B>"` / `shortest_path` for relationships and `… -m graphify explain "<concept>"` / `get_node` for focused concepts. These return a scoped subgraph, usually much smaller than `GRAPH_REPORT.md` or raw grep output.
- If graphify-out/wiki/index.md exists, navigate it instead of reading raw files
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context
- After modifying code files in this session, run `venv_skillopt/bin/python -m graphify update .` to keep the graph current (AST-only, no API cost). If `graphify update` exits non-zero or the harness sandbox denies it, report `⚠️ graph unavailable (sandbox/venv)` to the human and proceed without graph sovereignty for the session — do not silently fall back to recursive grep as though the graph were current.
- **Known coverage gaps** (observed graphify 0.8.30, AST-only mode): `.yaml`/`.yml` files are never indexed (zero such nodes ever appear — not a bug in the repo, a language the extractor doesn't parse); isolated `.md`/empty-`__init__.py` nodes are normal (no cross-file link extraction for prose/empty files). One anomaly under active watch: `rules/token_economy.md` is silently skipped even after a full cache-less rebuild, while every sibling `rules/*.md` indexes fine — cause not isolated (not encoding, size, or syntax). Treat "absent from the graph" as inconclusive for these cases, not as "doesn't exist" — cross-check with `grep`/`git ls-files` before concluding a file is orphaned.
