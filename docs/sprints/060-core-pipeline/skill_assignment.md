# Skill Assignment — Sprint 060 (github-broker-and-059-residue)

Source: `docs/sprints/060-core-pipeline/IMPLEMENTATION_PLAN.md`.
Phase 4.2 of `workflows/pipeline_workflow.md`. Drafted from this template.

Mode: **claude-code**, `delegation_mode: native`.

After writing this file, run:
`python3 scripts/check_forge_ladder.py --sprint-dir docs/sprints/060-core-pipeline`
(exit `2` rejects an empty forge destination or submodule contamination).

---

## 1. Priority ladder (record every rung)

`rules/skills_and_integrations.md §1`:

The ladder terminates at the first rung. Every Work row is served by a tool already
present in `skills/`, by the Python standard library, by `git`/`make`/`openssl`/
`ssh-keygen`/`venv_skillopt/bin/python`, or by editing an existing file. The plan's
Dependencies table adds no package. Rungs two to four are `not reached`.

| Rung | Source | Result | Evidence |
| :--- | :--- | :--- | :--- |
| P1 | `skills/manifest_skills.json` | hit - every unit resolved (section 2) | `skills/manifest_skills.json` lists `python-quality-auditor`, `env-shielding-auditor`, `omni-context-minimizer`, `compliance-checker`, `token-saver-auditor`, `graphify`; the five script-bearing skills have their script on disk (`graphify` is a knowledge skill without `scripts/`) |
| P2 | `autoskills-3rd` | not reached | ladder terminated at P1 |
| P3 | `https://skills.sh/` (WebSearch/WebFetch; simulated JSON allowed in tests) | not reached | ladder terminated at P1 |
| P4 | Three-File Standard at Destination | not reached | ladder terminated at P1; nothing was built |

**When this sprint builds a new skill**, the third rung's outcome MUST be recorded
as a machine-readable trail — a JSON object carrying `source`, `query` and a
boolean `hit`, shaped `{"source": "skills.sh", "query": "<term>", "hit": <bool>}`
with `<bool>` replaced by the real value. No HTTP in `make verify`.
`scripts/check_forge_ladder.py` requires that trail beside a named skill and its
`SKILL.md` path, and exits `2` without it.

> **When this sprint builds nothing, change none of the wording above.** It is
> written the way it is on purpose. `scripts/check_forge_ladder.py` decides whether
> a build is being claimed by pattern-matching this file's prose, so a template
> that *describes* the claim in the claim's own words is read as *making* it —
> and the check then demands a skill name a blank template cannot carry.
>
> Until Sprint 041 this section's header column and its fourth row did exactly
> that, and **the template copied unedited failed the Phase 4.2 gate that consumes
> it** (`exit 2`). Two further attempts to document the repair re-broke it, by
> quoting the offending strings and by pasting a literal example trail. Hence the
> abstractions above: describe the shape, never spell out an instance.
>
> The detector is correct and is not relaxed. What changed is that the template
> stopped announcing work that had not happened.

---

## 2. Per-unit tool resolution

| Unit | Skill / tool | Destination | P1–P4 trail |
| :--- | :--- | :--- | :--- |
| A-01 | none | N/A | P1: no skill authors ADRs; written from the ADR template |
| A-02 | none | N/A | P1: written from `BLUEPRINT_TEMPLATE.md` |
| A-03 | `python-quality-auditor`, `env-shielding-auditor` | N/A | P1 hit: `python_quality_auditor.py` on the new script; `env_shielding_auditor.py` confirms no key material lands in the repo |
| A-04 | `python-quality-auditor`, `env-shielding-auditor` | N/A | P1 hit: same pair as A-03 |
| A-05 | `env-shielding-auditor` | N/A | P1 hit: `env_shielding_auditor.py` after the `denyRead` and `permissions.deny` edit |
| A-06 | none | N/A | P1: public key supplied by the human; no tool needed |
| A-07 | `omni-context-minimizer`, `python-quality-auditor` | N/A | P1 hit: skeleton before any partial read of the existing script (>200 lines rule); quality audit after |
| A-08 | `omni-context-minimizer`, `python-quality-auditor` | N/A | P1 hit: same pair as A-07 |
| A-09 | none | N/A | P1: guide prose; no skill authors guides |
| A-10 | none | N/A | P1: Bash measurements M1-M5 written into the report; `devops_agent` is not the assignee (agent_assignment.md) |
| A-11 | none | N/A | P1: workflow prose edit |
| A-12 | none | N/A | P1: agent profile prose edit |
| A-13 | none | N/A | P1: rule prose edit |
| A-14 | none | N/A | P1: workflow prose edit |
| A-15 | none | N/A | P1: measurement M5 is recorded by hand from the GitHub IDs of each deploy operation; no skill applies |
| B-01 | `omni-context-minimizer`, `python-quality-auditor` | N/A | P1 hit: skeleton before partial read; quality audit on the fix |
| B-02 | none | N/A | P1: JSON edit with values from `token_economy_agent` |
| K-01 | `graphify` | N/A | P1 hit: `rules/graphify.md` method to confirm the `graph_update.py` workaround still holds on 0.9.x; the pin itself is `pip` under `--require-hashes`, no skill |
| M-01 | `python-quality-auditor`, `graphify` | N/A | P1 hit: quality audit on the battery and its test; `rules/graphify.md` for the `graph.json` edge schema the battery compares with the stdlib `ast` ground truth |
| M-02 | `graphify` | N/A | P1 hit: `rules/graphify.md` rebuild method for the 0.8.30 and post-K-01 baselines; counts by `wc -c`, timing by `time`, battery from M-01 |
| M-03 | `python-quality-auditor`, `graphify` | N/A | P1 hit: quality audit on the query script and its test; `rules/graphify.md` for the node and edge schema |
| M-04 | `python-quality-auditor`, `env-shielding-auditor`, `graphify` | N/A | P1 hit: quality audit on the stdio server; `env_shielding_auditor.py` confirms no credential or host term lands in the repo and the user-scope install stays outside writable trees (D2); `rules/graphify.md` for the tool surface |
| M-05 | `env-shielding-auditor` | N/A | P1 hit: `env_shielding_auditor.py` after the project-scope MCP entry is removed; JSON edit otherwise |
| M-06 | `graphify`, `compliance-checker` | N/A | P1 hit: `rules/graphify.md` is the file edited, so its own method is the content source; `compliance-checker` scans the normative text |
| M-07 | none | N/A | P1: agent profile prose edit; protocol text comes from M-06 |
| M-08 | none | N/A | P1: agent profile prose edit |
| M-09 | none | N/A | P1: agent profile prose edit |
| M-10 | none | N/A | P1: agent profile prose edit |
| M-11 | none | N/A | P1: agent profile prose edit |
| M-12 | `compliance-checker` | N/A | P1 hit: scan of the edited normative workflow |
| M-13 | `python-quality-auditor`, `env-shielding-auditor` | N/A | P1 hit: quality audit on the hook and its test; `env_shielding_auditor.py` confirms the usage log stores no tool input that can carry secrets; `RA-11` exit semantics checked by hand |
| M-14 | `env-shielding-auditor` | N/A | P1 hit: same check as A-05 after the hook registration edit |
| M-15 | `python-quality-auditor` | N/A | P1 hit: quality audit on the checker and its test |
| M-16 | none | N/A | P1: the A/B is run by the human with `scripts/session_cost.py` outside the sandbox; `token-saver-auditor` classifies prompts, it does not measure sessions |
| L-01 | `python-quality-auditor`, `env-shielding-auditor` | N/A | P1 hit: new stdlib script with network I/O and a paired test |
| L-02 | none | N/A | YAML job edit; no skill applies |
| L-03 | `python-quality-auditor`, `omni-context-minimizer` | N/A | P1 hit: modify a large script (`session_start.py`) with a paired test |
| L-04 | `env-shielding-auditor` | N/A | P1 hit: sandbox egress change |
| L-05 | none | N/A | ADR prose from `ADR_TEMPLATE.md` |
| L-06 | none | N/A | conditional config file or transcription of the alert message |
| C-01 | none | N/A | P1: workflow prose edit |
| D-01 | `python-quality-auditor`, `env-shielding-auditor` | N/A | P1 hit: quality audit; the scanner handles only hashes, `env_shielding_auditor.py` confirms no plaintext term enters the repo |
| D-02 | none | N/A | P1: JSON supplied by the human (hashes) |
| D-03 | `python-quality-auditor` | N/A | P1 hit: quality audit on the modified test |
| D-04 | none | N/A | P1: runs `scripts/check_host_terms.py` (D-01) over `origin/main`; no skill |
| D-05 | none | N/A | P1: Makefile edit; `make verify` is the check, no skill applies |
| E-01 | `omni-context-minimizer`, `python-quality-auditor` | N/A | P1 hit: skeleton before partial read; quality audit on the change |
| F-01 | `compliance-checker` | N/A | P1 hit: `compliance-checker` scans the trimmed `agents.md` for rule violations; byte count by `wc -c` |
| F-02 | `compliance-checker` | N/A | P1 hit: same scan on `rules/skills_and_integrations.md` |
| G-01 | `python-quality-auditor` | N/A | P1 hit: quality audit on the fix |
| G-02 | `python-quality-auditor` | N/A | P1 hit: quality audit on the fix |
| H-01 | none | N/A | P1: Bash matrices of 055 and 056 written into the report |
| H-02 | none | N/A | P1: rule prose edit |
| I-01 | none | N/A | P1: `git mv` to `GLOBAL_TOPOLOGY_MAP.md` plus a grep of the old path (RA-14); no skill renames files |
| I-02 | none | N/A | P1: `git mv` to `TOPOLOGY_MAP.md` plus a grep of the old path (RA-14); no skill renames files |
| I-03 | none | N/A | P1: `git mv` to `DOC_ORCHESTRATOR_CONTRACT.md` plus a grep of the old path (RA-14); no skill renames files |
| I-04 | none | N/A | P1: `git mv` to `TOPOLOGY_MAPPER_CONTRACT.md` plus a grep of the old path (RA-14); no skill renames files |
| I-05 | none | N/A | P1: `git mv` to `TOPOLOGY_SCAFFOLDER_CONTRACT.md` plus a grep of the old path (RA-14); no skill renames files |
| I-06 | none | N/A | P1: `git mv` to `TOKEN_ECONOMY_DOCUMENTATION_STANDARD_AUDIT.md` plus a grep of the old path (RA-14); no skill renames files |
| I-07 | none | N/A | P1: `git mv` to `SKILLOPT_TRANSITIVE_CLOSURE_AUDIT.md` plus a grep of the old path (RA-14); no skill renames files |
| I-08 | none | N/A | P1: `git mv` to `THIRD_PARTY_PROVENANCE_REGISTER.md` plus a grep of the old path (RA-14); no skill renames files |
| I-09 | none | N/A | P1: `git mv` to `AUTONOMY_POSTURE_PLAN.md` plus a grep of the old path (RA-14); no skill renames files |
| J-01 | `token-saver-auditor` | N/A | P1 hit: its rejection filters classify the measured findings; byte and token counts by `wc -c` and `scripts/` measurement tools |
| J-02 | `compliance-checker` | N/A | P1 hit: `compliance-checker` as the scan base for prose motives in normative documents |
| Z-01 | none | N/A | P1: written from `SPRINT_LOG` template |
| Z-02 | `graphify` | N/A | P1 hit: dependency graph query for the jurisdictional scope (`graph_sovereignty`) |
| Z-03 | none | N/A | P1: already written (commit `024598e`) |
| Z-05 | none | N/A | P1: ledger edit |
| Z-06 | none | N/A | P1: roadmap edit |

`Destination` for a forged skill: `host:.claude/skills/<name>/` (default),
`profile:<path>`, or `nucleus:PR`. Writing under `.agents/skills/` from a
host session is PROHIBITED (`strict_rule`). Every Destination here is `N/A`: no skill is created.

---

## 3. Skills used

| Skill | Why |
| :--- | :--- |
| `python-quality-auditor` | A-03, A-04, A-07, A-08, B-01, L-01, L-03, D-01, D-03, E-01, G-01, G-02, M-01, M-03, M-04, M-13, M-15: every Python unit meets the Ruff/Mypy/Bandit gate before QA (`agents.md §1 linter_command`). |
| `env-shielding-auditor` | A-03, A-04, A-05, L-01, L-04, D-01, M-04, M-05, M-13, M-14: the broker, its installer, the deny settings, the hash scanner, the graph MCP server and the usage hook handle credentials, host names or tool input; the scan proves nothing sensitive is committed (`RA-09`, `RA-15`). |
| `omni-context-minimizer` | A-07, A-08, B-01, L-03, E-01: existing scripts above 200 lines get a skeleton before any partial read (`agents.md §2 ast_skeleton`). |
| `compliance-checker` | F-01, F-02, J-02, M-06, M-12: normative text edits and the prose-motive audit need a rule-violation scan. |
| `token-saver-auditor` | J-01: its rejection filters are the classification basis for prompt-audit findings. The plan itself was already audited at Phase 3. |
| `graphify` | K-01, Z-02, M-01, M-02, M-03, M-04, M-06: graph workaround check on the new `graphifyy`, the dependency graph behind `task_scope.md`, and the `rules/graphify.md` schema and method that Wave M (D14) turns into the battery, the query interface, the MCP server and the structural-first protocol. |

## 4. Skills considered and rejected

| Candidate | Why rejected |
| :--- | :--- |
| `mcp-registry` | A-03 and M-04 are MCP servers, but D2 forbids registering it in `claude/mcp.json` or `.mcp.json`; the registry protocol would route it into agent-writable files. Registration is the human's `claude mcp add --scope user` step; M-05 removes the project-scope `graphify` entry rather than adding one. |
| `autoskills-3rd` | P1 already resolved every unit; running it needs `pnpm install` provisioning and writes a discovery file for no gain. |
| `skillopt` | F-01, F-02, M-06, M-12: it rewrites rule files and needs explicit human authorization per run; no authorization exists and the edits are specified by the plan. |
| `contract-writer` | A-03 has no HTTP API of its own; the operation list is in D4 and ADR-0025. M-04 is a stdio tool surface specified by D14, not an HTTP contract. |
| `token-saver-auditor` for M-16 | It classifies prompt findings; the A/B needs per-session `fresh` token counts, which only `scripts/session_cost.py` run by the human produces. |
| Any new graph skill for Wave M | `graphify` plus M-01, M-03 and M-04 (scripts in `scripts/`, not skills) cover the need; D14 asks for a query interface, not a skill. |
| `topology-scaffolder`, `topology-monitor` | Nucleus mode forbids scaffolding (`nucleus_neutrality`); I-01..I-09 are renames of existing files, not new topology. |
| `mass-standardizer`, `readme-standardizer`, `skill-creator` | No skill is added or changed this sprint, so the manifest is not regenerated and no README is written. |
| `sprint-architect` | The plan exists and was approved for drafting at Phase 3; Z-01 and Z-03 are already templated. |
| `django-*`, `nodejs-*`, `typescript-advanced-types`, `vercel-*`, `vite`, `tailwind-css-patterns`, `frontend-design`, `accessibility`, `seo`, `js-standardizer`, `slash-commander`, `skills-samples-3rd` | No Django, Node, frontend or slash-command surface in any Work row. |

## 5. Gaps

None. No skill was forged and nothing was written under `skills/`. The plan's Dependencies table adds no package, so no external discovery was needed.
