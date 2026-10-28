# Skill Assignment — Sprint 058 (upstream-channel-and-reproduce-first)

Source: `docs/sprints/058-core-pipeline/IMPLEMENTATION_PLAN.md`.
Phase 4.2 of `workflows/pipeline_workflow.md`. Drafted from this template.

Mode: **claude-code**, `delegation_mode: native`.

After writing this file, run:
`python3 scripts/check_forge_ladder.py --sprint-dir docs/sprints/058-core-pipeline`
(exit `2` rejects an empty forge destination or submodule contamination).

---

## 1. Priority ladder (record every rung)

`rules/skills_and_integrations.md §1`:

The ladder terminates at the first rung. Every unit A-01..A-17, C-01..C-09,
B-01..B-15 and D-01..D-07 is served by a tool already present in `skills/`, by
the Python standard library, by `git`/`make`/`venv_skillopt/bin/python`, or by
editing an existing file. The plan's Dependencies table adds a version bump
(`claude-agent-sdk`, `graphifyy`) and no new tool. Rungs two to four are
`not reached`.

| Rung | Source | Result | Evidence |
| :--- | :--- | :--- | :--- |
| P1 | `skills/manifest_skills.json` | Hit: all required capabilities are covered | The manifest (`version 1.3.0`) lists `python-quality-auditor`, `omni-context-minimizer`, `token-saver-auditor`, `compliance-checker`, `env-shielding-auditor`, `graphify`, `mcp-registry`; sections 2 and 3 map each unit to them or to plain tool use |
| P2 | `autoskills-3rd` | not reached | Rung one covers every unit |
| P3 | `https://skills.sh/` (WebSearch/WebFetch; simulated JSON allowed in tests) | not reached | No unit needs a capability absent from `skills/`; no web call was made |
| P4 | Three-File Standard at Destination | not reached | No skill is created; `Destination` is `N/A` in every row of section 2 |

No skill was forged in Sprint 058. No new skill forged means no `Destination`
other than `N/A`, no host skill directory written, and no submodule write.
B-08 modifies the existing `audit_plan.py` of `token-saver-auditor`; that is an
edit of an existing script, not a forge, and it is assigned in
`agent_assignment.md` to `skill_architect`.

---

## 2. Per-unit tool resolution

Legend. `OCM` = `omni-context-minimizer` (`skills/omni-context-minimizer/scripts/omni_minimizer.py`), run
before any partial read of a file above 200 lines (`agents.md §2 ast_skeleton`);
the line counts below were measured at Phase 4.2 with `wc -l`. `PQA` =
`python-quality-auditor` (ruff, mypy, bandit, radon print-only; the gating
instruments remain `make verify` and `make quality-audit`). `compliance-checker` is
run on edited governance prose. `stdlib` = Python standard library through
`python3`, tests through the project interpreter (`rules/project_topology.md`).
`plain` = no skill, plain `Read`/`Edit`/`Write` for a file of 200 lines or fewer.

| Unit | Skill / tool | Destination | P1–P4 trail |
| :--- | :--- | :--- | :--- |
| A-01 | plain: JSON template written from the D1 schema (stdlib `json` to validate) | N/A | Rung one; others not reached |
| A-02 | PQA; stdlib `json`, `argparse`, `subprocess`; pytest for `tests/test_upstream_outbox.py` | N/A | Rung one; others not reached |
| A-03 | plain: JSON config; stdlib `json` to validate | N/A | Rung one; others not reached |
| A-04 | PQA; `env-shielding-auditor` (the script prints structured fields only, so a secret-handling review applies); stdlib `json`, `re`; pytest | N/A | Rung one; others not reached |
| A-05 | plain: one-line `.gitignore` edit | N/A | Rung one; others not reached |
| A-06 | OCM mandatory (`scripts/session_start.py`, 714 lines); PQA; pytest | N/A | Rung one; others not reached |
| A-07 | plain: YAML Issue Form; no skill covers `.github/` forms | N/A | Rung one; others not reached |
| A-08 | `env-shielding-auditor` (issue body passed by environment variable, actions pinned by SHA); stdlib `pathlib` to confirm no `${{ }}` expression sits inside a `run:` block; no PQA (YAML) | N/A | Rung one; others not reached |
| A-09 | OCM mandatory (`scripts/sync_agents_pin.py`, 303 lines); PQA; stdlib `subprocess`; pytest | N/A | Rung one; others not reached |
| A-10 | plain: 15-line template edit | N/A | Rung one; others not reached |
| A-11 | plain read (`agents.md`, 179 lines, under the 200-line threshold); `compliance-checker` on the amended `§4 feedback_upstream` | N/A | Rung one; others not reached |
| A-12 | `compliance-checker`; plain read (27 lines) | N/A | Rung one; others not reached |
| A-13 | `compliance-checker`; plain read (44 lines) | N/A | Rung one; others not reached |
| A-14 | `compliance-checker`; plain read (38 lines) | N/A | Rung one; others not reached |
| A-15 | `compliance-checker`; plain read (112 lines) | N/A | Rung one; others not reached |
| A-16 | `compliance-checker` and `env-shielding-auditor` review of the secrets/sandbox wording; plain read (19 lines) | N/A | Rung one; others not reached |
| A-17 | OCM mandatory (`docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md`, 2090 lines), then partial `offset`/`limit` reads and an append at the end; `compliance-checker` | N/A | Rung one; others not reached |
| C-01 | PQA; stdlib `re`; pytest for `tests/test_md_table.py` | N/A | Rung one; others not reached |
| C-02 | OCM mandatory (`scripts/check_task_scope.py`, 331 lines); PQA; `tests/test_check_task_scope.py` unchanged and green | N/A | Rung one; others not reached |
| C-03 | OCM mandatory (`scripts/check_gate_log.py`, 224 lines); PQA; pytest | N/A | Rung one; others not reached |
| C-04 | OCM mandatory (`scripts/check_forge_ladder.py`, 368 lines); PQA; pytest | N/A | Rung one; others not reached |
| C-05 | OCM mandatory (`scripts/detect_new_models.py`, 289 lines); PQA; pytest | N/A | Rung one; others not reached |
| C-06 | plain: JSON template (146 lines); stdlib `json`; pytest `tests/test_template_sandbox.py`; `env-shielding-auditor` to confirm the removal leaves the sandbox denies (`./.env`) intact | N/A | Rung one; others not reached |
| C-07 | OCM mandatory (`scripts/merge_json.py`, 410 lines); PQA; stdlib `json`; pytest | N/A | Rung one; others not reached |
| C-08 | OCM mandatory (`docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md`, 2090 lines) then a targeted `F-107-N1` read; `compliance-checker` | N/A | Rung one; others not reached |
| C-09 | OCM mandatory (`scripts/session_state.py`, 1076 lines); PQA; stdlib `subprocess` (`git`); pytest | N/A | Rung one; others not reached |
| B-01 | `compliance-checker` on the amended `§4` (R-4, R-5, A-1); plain read (144 lines) | N/A | Rung one; others not reached |
| B-02 | `compliance-checker`; plain read (85 lines) | N/A | Rung one; others not reached |
| B-03 | plain: 79-line template edit (three tables) | N/A | Rung one; others not reached |
| B-04 | OCM mandatory (`scripts/check_gate_log.py`, 224 lines); PQA; pytest | N/A | Rung one; others not reached |
| B-05 | PQA; stdlib `subprocess` (`git log`), `re`; pytest | N/A | Rung one; others not reached |
| B-06 | OCM mandatory (`hooks/on_commit.py`, 1156 lines); PQA; pytest; `RA-11` exit-code semantics apply (warning path exits `0`) | N/A | Rung one; others not reached |
| B-07 | plain: JSON config; stdlib `json` to validate | N/A | Rung one; others not reached |
| B-08 | OCM mandatory (`skills/token-saver-auditor/scripts/audit_plan.py`, 329 lines); PQA; pytest. `token-saver-auditor` is deliberately not run as an instrument on this unit (section 4) | N/A | Rung one; others not reached |
| B-09 | PQA; stdlib `re`, `pathlib`; pytest | N/A | Rung one; others not reached |
| B-10 | `compliance-checker` (`RA-16` invoker declaration for `check_plan_closure.py`); plain read (38 lines) | N/A | Rung one; others not reached |
| B-11 | `compliance-checker`; plain read (44 lines) | N/A | Rung one; others not reached |
| B-12 | `compliance-checker`; plain read (22 lines) | N/A | Rung one; others not reached |
| B-13 | OCM mandatory (`scripts/check_fix_reproduces.py`, 380 lines); PQA; stdlib `subprocess`; pytest with a simulated runner (no vitest install, no `pnpm`) | N/A | Rung one; others not reached |
| B-14 | OCM mandatory (`scripts/check_fix_reproduces.py`, 380 lines); PQA; stdlib `re`; pytest | N/A | Rung one; others not reached |
| B-15 | `compliance-checker`; plain read of `agents.md` `§0` (179 lines) | N/A | Rung one; others not reached |
| D-01 | plain: one-line version edit of `requirements-skillopt.txt`; commit trailer `Dependency:` | N/A | Rung one; others not reached |
| D-02 | `graphify` skill for the measurement vocabulary only; measurements (a)-(c) run by `devops_agent` through `Bash`, literal output handed to the writer; any secret-needing command is prepared for the human (`RA-09`, `scripts/with_env.py`); `env-shielding-auditor` is not run on `.env` | N/A | Rung one; others not reached |
| D-03 | plain: one-line version edit of `requirements-core.txt`; commit trailer `Dependency:`; decided by the D-02 outcome | N/A | Rung one; others not reached |
| D-04 | plain: `Makefile` edit (169 lines); `make` target dry run | N/A | Rung one; others not reached |
| D-05 | `graphify` skill (`rules/graphify.md` is its governing rule); `compliance-checker`; plain read (32 lines) | N/A | Rung one; others not reached |
| D-06 | `compliance-checker`; plain read (52 lines) | N/A | Rung one; others not reached |
| D-07 | `env-shielding-auditor` (the `reason` field names variables, never values); stdlib `json` to validate | N/A | Rung one; others not reached |

---

## 3. Skills used

| Skill | Why |
| :--- | :--- |
| `omni-context-minimizer` | Mandatory before partial reads of the 12 edited files above 200 lines: `scripts/session_start.py` (714), `scripts/session_state.py` (1076), `scripts/check_fix_reproduces.py` (380), `scripts/sync_agents_pin.py` (303), `hooks/on_commit.py` (1156), `scripts/check_gate_log.py` (224), `scripts/check_forge_ladder.py` (368), `scripts/detect_new_models.py` (289), `scripts/merge_json.py` (410), `scripts/check_task_scope.py` (331), `skills/token-saver-auditor/scripts/audit_plan.py` (329), `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` (2090) |
| `python-quality-auditor` | Print-only ruff/mypy/bandit/radon pass on every Python file created or modified; it is not a gate, so `make verify` and `make quality-audit` remain the acceptance checks |
| `compliance-checker` | Governance prose edits: `agents.md`, `rules/*.md`, `workflows/*.md`, the guide and `SECURITY.md` (A-11..A-16, B-01, B-02, B-10..B-12, B-15, D-05, D-06) |
| `env-shielding-auditor` | Units that touch secret or sandbox surfaces without reading `.env`: A-04, A-08, A-16, C-06, D-02 (not run on `.env`), D-07 |
| `graphify` | D-05 (rule); D-02 uses it for vocabulary. The graph query `graph_sovereignty` applies before any recursive grep across `scripts/` for the shared-module blast radius |

## 4. Skills considered and rejected

| Candidate | Why rejected |
| :--- | :--- |
| `token-saver-auditor` | B-08 edits its own `audit_plan.py`; running the instrument that the unit is changing, before and after the change, would measure the plan with two different versions of the rule and prove nothing. It is also not needed to author the other 47 units: the plan's token audit belongs to Phase 1. Run it once on the finished plan only if a later gate asks, with the post-B-08 script |
| `js-standardizer` | Not applicable: no JavaScript or TypeScript is written. A-08 and A-07 are YAML; `claude/settings.hooks.json` is JSON. B-13 adds a vitest runner invocation to a Python script and installs no JS tooling |
| `mcp-registry` | No unit adds, edits or binds an MCP server; `claude/mcp.json` is untouched |
| `sprint-architect` | The Implementation Plan already exists (Phase 1); this phase does not redraft it |
| `topology-monitor` | Its `legacy_app_auditor.py` audits Three-File adherence; no skill directory is created, so there is nothing to audit |
| `mass-standardizer` | It regenerates `skills/manifest_skills.json`; no skill is added or renamed |
| `skill-creator`, `skillopt` | No forge and no instruction optimisation run is planned; `skillopt` needs separate explicit human authorization per run |
| `readme-standardizer`, `contract-writer`, `topology-scaffolder`, `slash-commander` | The documents edited are governance prose and templates, not READMEs, contracts, scaffolds or slash commands |
| `autoskills-3rd` and the `*-3rd`, `django-*`, `vercel-*`, `tailwind-*`, `typescript-*`, `vite`, `seo`, `accessibility`, `frontend-design`, `nodejs-*` families | Stack-specific to Django or frontend work; the sprint touches neither |
| Web search of `https://skills.sh/` | Not used: the instruction was to search `skills/` first and every need is covered locally |

## 5. Gaps

None. No unit lacks a tool, and no forge is required. One item for the
Principal Agent, not a gap: the line counts in section 3 were taken at Phase 4.2
and `hooks/on_commit.py` measures 1156 lines against 1144 in the Sprint 057
record, so each unit re-measures with `wc -l` before relying on a count.
