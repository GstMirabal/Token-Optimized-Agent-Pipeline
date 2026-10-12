# Skill Assignment — Sprint 056 (sandbox-enumeration-and-instrument-residue)

Source: `docs/sprints/056-core-pipeline/IMPLEMENTATION_PLAN.md`.
Phase 4.2 of `workflows/pipeline_workflow.md`. Drafted from this template.

Mode: **claude-code**, `delegation_mode: native`.

After writing this file, run:
`python3 scripts/check_forge_ladder.py --sprint-dir docs/sprints/056-core-pipeline`
(exit `2` rejects an empty forge destination or submodule contamination).

---

## 1. Priority ladder (record every rung)

`rules/skills_and_integrations.md §1`:

The ladder terminates at P1. Every computational need of the 29 units (`A1`-`A21`,
`B1`-`B8`) is covered by a script or skill that already exists in `skills/`, by a
`scripts/` tool, or by a deliverable the plan itself assigns to `implementer_agent`
(`A13`, `mark-audited`). The remaining rungs are `not reached`.

| Rung | Source | Result | Evidence |
| :--- | :--- | :--- | :--- |
| P1 | `skills/manifest_skills.json` | hit | The manifest lists 34 skills. Used: `omni-context-minimizer`, `python-quality-auditor`, `token-saver-auditor`, `env-shielding-auditor`, `topology-monitor`, `compliance-checker`, `graphify`. Reproduce: `python3 -c "import json;print([s['name'] for s in json.load(open('skills/manifest_skills.json'))['skills']])"` |
| P2 | `autoskills-3rd` | not reached | P1 covered every unit. The directory `skills/autoskills-3rd/` exists locally and was not consulted |
| P3 | `https://skills.sh/` (WebSearch/WebFetch; simulated JSON allowed in tests) | not reached | No unit has an uncovered need, so no query was issued and no trail object was registered. `scripts/check_forge_ladder.py` requires the machine-readable P3 trail only beside a named skill and its `SKILL.md` path; this sprint names none, so registering a trail with no skill would make the check exit `2` (`P3 recorded but no skill name`) |
| P4 | Three-File Standard at Destination | not reached | No destination was chosen because nothing needed building |

`session_state.py mark-audited` (`A13`) is **not** a skill. It is a framework-root
script authored by `implementer_agent` (`ADR-0009`, `agents.md §6 devops_agent` row).
Its invoker is declared in the plan's Mechanisms table (`RA-16`):
`workflows/audit_workflow.md`, last step (`A14`). A skill would add a `SKILL.md` and
a `README.md` around a subcommand of an existing script, which
`agents.md §3 three_file_standard` classes as padding.

The `SANDBOX_ENUMERATION.md` measurement (`B1`, `B4`) has no deterministic tool:
the plan's Mechanisms table classes it as agent judgment, measured with `claude -p`
headless and `jq`, because it needs a sandboxed Claude Code session.

---

## 2. Per-unit tool resolution

Large-file rule (`agents.md §2 token_saver`): files over 200 lines get the
`omni-context-minimizer` skeleton first, then a partial read. Line counts measured
with `wc -l` at base `817ac26`.

| Unit | Skill / tool | Destination | P1–P4 trail |
| :--- | :--- | :--- | :--- |
| `A1` | `skills/omni-context-minimizer` on `scripts/docs_freshness_check.py` (644 lines; skeleton, then read `is_adr_superseded` and `ADR_STATUS_SUPERSEDED_RE` only) plus `skills/python-quality-auditor` | N/A | P1 hit; P2-P4 not reached |
| `A2` | `skills/omni-context-minimizer` on `scripts/verify_references.py` (1038 lines; read `:547`, `:659`, `:698` and `_invoked_by_line` only) plus `skills/python-quality-auditor` | N/A | P1 hit; P2-P4 not reached |
| `A3` | `skills/omni-context-minimizer` on `scripts/verify_references.py` (read `_token_present`, `_skill_doc_names_script`, around `:411`-`:435`) plus `skills/python-quality-auditor` | N/A | P1 hit; P2-P4 not reached |
| `A4` | none for the edit (`tests/test_root_resolution.py` is 120 lines, read in full). Gate: `skills/python-quality-auditor` | N/A | P1 hit; P2-P4 not reached |
| `A5` | none (one-line README edit, 42 lines). Evidence for the fix is `skills/env-shielding-auditor/scripts/env_shielding_auditor.py`, which exists and is read, not run | N/A | P1 hit; P2-P4 not reached |
| `A6` | `skills/omni-context-minimizer` on `scripts/quality_audit.py` (871 lines; skeleton, then the JS/TS unit-measurement functions) plus `skills/python-quality-auditor`. Gate: `make quality-audit` (the instrument under change measures the change) | N/A | P1 hit; P2-P4 not reached |
| `A7` | `skills/omni-context-minimizer` on `scripts/quality_audit.py` (Python and JS/TS counting functions only) plus `skills/python-quality-auditor`. Gate: `make quality-audit` | N/A | P1 hit; P2-P4 not reached |
| `A8` | none. Edit of two `agents.md` table rows (long lines, so partial read by row); `skills/compliance-checker` is not applicable (see §4) | N/A | P1 hit; P2-P4 not reached |
| `A9` | `skills/omni-context-minimizer` on `scripts/install.py` (669 lines; read `RENDER_OWNED_RE` and the `prune_rendered_exclusions` docstring, `:60` and `:176-181`) plus `skills/python-quality-auditor` | N/A | P1 hit; P2-P4 not reached |
| `A10` | `skills/omni-context-minimizer` on `scripts/install.py` (`prune_rendered_exclusions` only) plus `skills/python-quality-auditor` | N/A | P1 hit; P2-P4 not reached |
| `A11` | none for the edit (`tests/test_template_sandbox.py`, 120 lines, read in full). Gate: `skills/python-quality-auditor` | N/A | P1 hit; P2-P4 not reached |
| `A12` | none for the edit (`tests/test_install_with_env_render.py`, 95 lines, read in full). Gate: `skills/python-quality-auditor` (return-type check via `mypy` line) | N/A | P1 hit; P2-P4 not reached |
| `A13` | `skills/omni-context-minimizer` on `scripts/session_state.py` (799 lines; skeleton to find the subcommand registration and the anchor-write helpers) plus `skills/python-quality-auditor`. The test file `tests/test_session_state.py` (673 lines) is read through the same skeleton | N/A | P1 hit; P2-P4 not reached |
| `A14` | none (25-line workflow edit). `scripts/map_workflows.py` regenerates `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` afterwards; the guide is never hand-edited | N/A | P1 hit; P2-P4 not reached |
| `A15` | none (49-line rule file, read in full). `skills/compliance-checker` is not applicable (see §4) | N/A | P1 hit; P2-P4 not reached |
| `A16` | none. Partial read of the `RA-09` row of `agents.md` only (`§2 token_saver`) | N/A | P1 hit; P2-P4 not reached |
| `A17` | none (34-line workflow, read in full). `scripts/map_workflows.py` regenerates the step-map guide afterwards | N/A | P1 hit; P2-P4 not reached |
| `A18` | none (117-line rule file; read `§5` only) | N/A | P1 hit; P2-P4 not reached |
| `A19` | none (42-line workflow, read in full). `scripts/map_workflows.py` regenerates the step-map guide afterwards | N/A | P1 hit; P2-P4 not reached |
| `A20` | none (134-line template; read around line 91). `skills/readme-standardizer` is not applicable (see §4) | N/A | P1 hit; P2-P4 not reached |
| `A21` | none (37-line agent file, read in full) | N/A | P1 hit; P2-P4 not reached |
| `B1` | none for the measurement: `claude -p` headless (CLI 2.1.119) and `jq`, agent judgment per the plan's Mechanisms table. `skills/env-shielding-auditor` is not run against the fixture host (see §4). Skeleton reads of `claude/settings.hooks.json` and the seven hook scripts use `skills/omni-context-minimizer` where a hook exceeds 200 lines | N/A | P1 hit; P2-P4 not reached |
| `B2` | none for the edit (`claude/settings.hooks.json`, 158 lines, read in full). Gate: `venv_skillopt/bin/python -m pytest -q tests/test_template_sandbox.py` plus `jq -e` parse checks from the plan's Verification table | N/A | P1 hit; P2-P4 not reached |
| `B3` | none (`claude/mcp.json`, 21 lines). `jq -e` parse check plus the MCP template test | N/A | P1 hit; P2-P4 not reached |
| `B4` | none: same `claude -p` measurement as `B1`, repeated after `B2`/`B3` | N/A | P1 hit; P2-P4 not reached |
| `B5` | `skills/omni-context-minimizer` on `scripts/install.py` (read the `excludedCommands` handling near `:197` only) plus `skills/python-quality-auditor` | N/A | P1 hit; P2-P4 not reached |
| `B6` | none (`rules/project_topology.md`, 49 lines, read in full) | N/A | P1 hit; P2-P4 not reached |
| `B7` | none. Partial read of the `RA-09` and `RA-19` rows of `agents.md` only (`§2 token_saver`) | N/A | P1 hit; P2-P4 not reached |
| `B8` | `skills/omni-context-minimizer` is not applicable to Markdown prose; read `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` (2036 lines) with offset/limit at lines `1990-2020` for `F-055-N1` | N/A | P1 hit; P2-P4 not reached |

Plan-level and close-level tools, outside the unit rows:

| Gate | Tool |
| :--- | :--- |
| Phase 1/4 plan audit | `skills/token-saver-auditor` `scripts/audit_plan.py` on `IMPLEMENTATION_PLAN.md` |
| Phase 4 topology | `skills/topology-monitor` `scripts/legacy_app_auditor.py` (Three-File Standard adherence; no skill directory is added or changed by this sprint) |
| Phase 7 gates | `make verify`, `scripts/check_fix_reproduces.py`, `skills/python-quality-auditor` |
| Close | `venv_skillopt/bin/python -m graphify update .` (`§2 graph_sync`), `scripts/map_workflows.py` |

`Destination` is `N/A` for every unit: nothing is built under a skill destination.
Writing under the submodule skills tree from a host session is PROHIBITED
(`strict_rule`); this sprint runs in nucleus mode and touches only the unit files in
the plan's Work tables.

---

## 3. Skills used

| Skill | Why |
| :--- | :--- |
| `omni-context-minimizer` | Skeleton before partial read of every file over 200 lines that a unit edits: `scripts/docs_freshness_check.py`, `scripts/verify_references.py`, `scripts/quality_audit.py`, `scripts/install.py`, `scripts/session_state.py` (`A1`-`A3`, `A6`, `A7`, `A9`, `A10`, `A13`, `B5`) |
| `python-quality-auditor` | Pass/fail `ruff`/`mypy`/`bandit`/`radon` lines on every Python file a unit touches, including test files (`A1`-`A4`, `A6`, `A7`, `A9`-`A13`, `B5`). It computes no score and never exits non-zero, so `make verify` stays the authoritative gate |
| `token-saver-auditor` | `audit_plan.py` on `IMPLEMENTATION_PLAN.md` (Verification table, already recorded exit `0`) and on any revision of it |
| `topology-monitor` | `legacy_app_auditor.py` is the official Three-File Standard auditor (`agents.md §3 enforcement`); run at the QA gate to show the sprint left the skills tree conformant |
| `graphify` | `graph_sync` after changes, and graph queries before any recursive grep for callers of `_invoked_by_line`, `RENDER_OWNED_RE` and `prune_rendered_exclusions` |

## 4. Skills considered and rejected

| Candidate | Why rejected |
| :--- | :--- |
| `env-shielding-auditor` | Scans for hardcoded secrets and validates `.env` protection. `B1`/`B4` measure which paths a sandboxed agent can write, using a fixture `.env`; this skill neither enumerates entry points nor writes fixtures. `A5` only corrects its README. `RA-09` also keeps the agent from running secret-reading commands |
| `compliance-checker` | Scans plans and code for rule violations. `A8`, `A15`, `A16`, `A18`, `B6`, `B7` amend the rules themselves, so the checker would compare the amended text against the text it replaces. The amendments are judged by Gate 1 instead |
| `readme-standardizer` | `A20` edits one line of the README template and `A5` one line of a skill README. The skill regenerates whole READMEs, which would rewrite far more than the unit's single line |
| `skill-creator` | Nothing is forged (§1) |
| `mass-standardizer` | Regenerates `skills/manifest_skills.json`; no skill is added, renamed or removed, so the manifest does not change |
| `sprint-architect` | The Work Breakdown Structure already exists in `IMPLEMENTATION_PLAN.md` |
| `slash-commander` | No workflow gains or loses a slash command; `A14`, `A17`, `A19` edit step text only |
| `autoskills-3rd` | P2 not reached (§1) |

## 5. Gaps

None. Every unit `A1`-`A21` and `B1`-`B8` has its tools resolved above. Four rows
(`B1`, `B4`, and the measurement half of `B2`) rely on a human-attended sandboxed
Claude Code session, with no skill behind them, as the plan's Mechanisms table
already states.
