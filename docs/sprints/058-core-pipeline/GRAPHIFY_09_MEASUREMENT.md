# Graphify 0.9 Measurement (Sprint 058, D-02)

| Field | Value |
| :--- | :--- |
| Date | 2026-10-31 |
| Session | #65 |
| Candidate version | `graphifyy` 0.9.97, the latest 0.9.x uploaded more than 24 h before the run (0.9.97 2026-10-27T18:16:13Z); 0.9.98 (2026-10-30T22:55:56Z) and 0.9.99 (2026-10-30T23:43:03Z) are excluded by the `agents.md` section 8 release-age floor of 1440 minutes |
| Baseline commit | `f0b11f8` (`docs(roadmap): mark Sprint 057 deployed as v4.40.0 #057`) |
| Runner | `devops_agent` |
| Author | `doc_orchestrator` |
| Source | literal `devops_agent` report; `$S` is the session scratchpad |
| Environment | disposable venv `$S/venv_g097` (`python3 -m venv $S/venv_g097 && $S/venv_g097/bin/python -m pip install -q graphifyy==0.9.97`, output: only a pip upgrade notice; `pip show graphifyy` -> `Version: 0.9.97`); detached worktree `git worktree add --detach $S/wt f0b11f8` (`HEAD is now at f0b11f8 docs(roadmap): mark Sprint 057 deployed as v4.40.0 #057`), `graphify-out/` not copied |
| Plan reference | `IMPLEMENTATION_PLAN.md` section `### D7 — Dependabot`, PR #89: human decision 2026-10-28, measure then decide |

## (a) Re-inclusion option for data JSON

CLI flags read from top-level `--help` (`graphify update --help` and `extract --help` print only "Run 'graphify --help' for full usage." plus a stale-skill warning).

| Mechanism | Location | Effect on data JSON |
| :--- | :--- | :--- |
| `update <path>` flags `--force` (or `GRAPHIFY_FORCE=1`), `--no-cluster` | CLI top-level `--help` | None; no mention of JSON or data files |
| `extract <path>` flags `--backend`, `--model`, `--mode deep`, `--force`, `--max-workers`, `--token-budget`, `--max-concurrency`, `--api-timeout`, `--out/--output`, `--google-workspace`, `--no-gitignore`, `--no-cluster`, `--code-only`, `--postgres`, `--cargo`, `--global`, `--as` | CLI top-level `--help` | None mentions JSON or data files |
| `.json` in `CODE_EXTENSIONS` | `detect.py:48` | Detection still collects the files |
| Exclusion site: `if not _is_config_json(path, doc, source): return {"nodes": [], "edges": [], "skipped": "data json (not a config/manifest)"}` | `extractors/json_config.py:293-294` | Skips data JSON at extraction, no nodes |
| `_is_config_json` accepts only: names in `_CONFIG_JSON_NAMES` (lines 10-16: package.json, tsconfig.json, manifest.json, app.json, vercel.json, ...); suffixes `.eslintrc.json`, `.prettierrc.json`, `.babelrc.json`, `tsconfig.json`, `jsconfig.json`; or a root key in `_CONFIG_JSON_KEYS` (lines 18-22: dependencies, devDependencies, extends, $schema, compilerOptions, ...) unless `$schema` plus `$defs`/`definitions`/`$id` | `extractors/json_config.py:34-` | Admits config/manifest files only |
| Array or scalar root skipped ("data json (non-object root)") | `extractors/json_config.py:302-303` | Skips |
| Files over 1 MiB skipped (`_JSON_MAX_BYTES = 1_048_576`) | `extractors/json_config.py:~110` | Skips |
| Skipped files recorded in `_skipped_sources`, no nodes | `extract.py:9751-9758` | No nodes |
| Comment states data JSON is "left to the LLM semantic pass" (#1224) | `extract.py:8855-8859` | Not indexed by the extractor |
| `.graphifyinclude` removed (#2112); now triggers a warning | `detect.py:2097-2101` | None |
| `.graphifyignore` / `.gitignore` | `detect.py:1628-1650` | Exclude only; `!` re-inclusion acts at detection, which already detects the file, so it does not reach the extractor skip |
| `language.<ext>=<name>` | `rcfile.py:72` | Maps suffixes only; does not touch `_is_config_json` |
| `GRAPHIFY_OUT`, `GRAPHIFY_OUT_NAME`, `GRAPHIFY_INSTALLED_FILES`, `GRAPHIFY_GOOGLE_WORKSPACE` | `detect.py`, `rcfile.py` | None concerns JSON |

Result: no flag, environment variable or config key re-includes data JSON. A file is indexed only if its name or root keys match the config rules, or through the LLM semantic pass. Override run not executed (no override exists).

## (b) Graph size on f0b11f8

Fresh copy per run.

| Run | Command | Exit | Last line |
| :--- | :--- | :--- | :--- |
| 0.8.30 | `<repo>/venv_skillopt/bin/python -I -m graphify update . --force` | 0 | `[graphify watch] Rebuilt: 9996 nodes, 13367 edges, 924 communities` |
| 0.9.97 default | `$S/venv_g097/bin/python -I -m graphify update . --force` | 0 | `[graphify watch] Rebuilt: 9538 nodes, 14262 edges, 802 communities` |
| 0.9.97 override | not run, no override exists | | |

0.9.97 also printed `warning: 17 code file(s) yielded no symbols ... CLAUDE.md, commands/audit.md (+12 more)` and wrote graph.html in aggregated form; 0.8.30 skipped graph.html (graph over the 5000-node limit).

Comparison: `python3 -I $S/cmp.py run_a/graphify-out/graph.json run_b/graphify-out/graph.json` (top-level keys `built_at_commit, directed, graph, hyperedges, links, multigraph, nodes`; edges under `links`):

```
0.8.30 nodes 9996 edges 13367 (key links) distinct source files 775 json sources 57
0.9.97 nodes 9538 edges 14262 (key links) distinct source files 731 json sources 2
json in 0.8.30 absent in 0.9.97: 55
claude/settings.hooks.json
config/abandoned_branches.json
config/artifact_registry.json
config/framework_identity.json
config/invocation_exceptions.json
config/model_tiers.json
config/quality_audit_exclusions.json
config/rule_triggers.json
config/template_gates.json
config/with_env_allowlist.json
json only in 0.9.97: 0
0.9.97 json sources: ['claude/mcp.json', 'skills/autoskills-3rd/package.json']
```

The list of 55 is cut at 10 by the runner.

| Metric | Delta (0.9.97 vs 0.8.30) |
| :--- | :--- |
| Nodes | 458 fewer |
| Edges | 895 more |

## (c) Provider variables and .env loader

Command: `grep -rhoE '[A-Z_]+_API_KEY' <site-packages>/graphify | sort -u`.

| Version | Variables | Count |
| :--- | :--- | :--- |
| 0.9.97 | ANTHROPIC_API_KEY, AZURE_OPENAI_API_KEY, DEEPSEEK_API_KEY, GEMINI_API_KEY, GOOGLE_API_KEY, GRAPHIFY_API_KEY, MOONSHOT_API_KEY, OLLAMA_API_KEY, OPENAI_API_KEY | 9 |
| 0.8.30 | ANTHROPIC_API_KEY, DEEPSEEK_API_KEY, GEMINI_API_KEY, GOOGLE_API_KEY, MOONSHOT_API_KEY, OLLAMA_API_KEY, OPENAI_API_KEY | 7 |

New in 0.9.97: AZURE_OPENAI_API_KEY, GRAPHIFY_API_KEY.

`.env` search: `grep -rnE "dotenv|load_dotenv|\.env\b" --include='*.py'`.

| Version | Hits | Locations |
| :--- | :--- | :--- |
| 0.8.30 | 1 | `detect.py:600` (directory skip list) |
| 0.9.97 | 13 | all comments/docstrings/extension or skip lists: `build.py:1576`, `paths.py:35`, `export.py:704`, `detect.py:150, 151, 156, 160, 206, 304, 315, 976, 1156, 1227` |

No `read_text`/`open(` line mentions `.env` or `envrc`. Only `os.environ[...] =` assignments: `cli.py:3918` (GRAPHIFY_API_TIMEOUT), `cli.py:3920` (GRAPHIFY_MAX_WORKERS). By grep: no .env loader, no dotenv import. Stated limit: this is a text search, not an execution trace.

## Cleanup

- `git worktree remove --force $S/wt`; `git worktree prune`.
- `git worktree list` -> only the main checkout at 42355f7 [ai-sprint/058].
- `git status --porcelain` -> empty.
- No .env read or stat; nothing written in the repository.

## Branch

Plan D7 criterion: the yes branch requires an option from (a). Measured: none exists.

| Item | Value |
| :--- | :--- |
| **Decision** | **No branch**, chosen by the human in chat on 2026-10-31 (session #65). |
| **Pin** | `graphifyy==0.8.30` stays in `requirements-core.txt`; D-03..D-07 are not executed. |
| **Dependabot #89** | Closed citing this document; the human runs the `gh pr close` command. |
| **Upstream report** | An issue to graphify asks for an option that indexes data JSON in AST mode, with the figures in (a) and (b). The human files it. |
| **Known issue** | `KI-058-2`, entered in the program queue at the Sprint 058 close extract. Exit condition: graphify ships an option that re-includes data JSON; each later Dependabot bump of `graphifyy` checks for it against this document. |
| **Alternatives rejected** | Adding `"$schema"` to the 55 files to pass `_is_config_json` (edits vendored skills and fixtures, and depends on a heuristic that can change in any release). A local extractor that adds config JSON nodes to `graph.json` after `graphify update` (a new mechanism with no measured benefit of 0.9.x to pay for it). |
| **Consumer affected by a future bump** | `scripts/graph_reconcile.py` reads `graphify-out/graph.json` and lists tracked files without a node, so a bump without the option adds the 55 files to `graphify-out/unmapped_files.json`. |
