# Skill Assignment — Sprint 055 (sandbox-restrictions-and-secret-path)

Source: `docs/sprints/055-core-pipeline/IMPLEMENTATION_PLAN.md`.
Phase 4.2 of `workflows/pipeline_workflow.md`. Drafted from this template.

Mode: **claude-code**, `delegation_mode: native`.

After writing this file, run:
`python3 scripts/check_forge_ladder.py --sprint-dir docs/sprints/055-core-pipeline`
(exit `2` rejects an empty forge destination or submodule contamination).

---

## 1. Priority ladder (record every rung)

`rules/skills_and_integrations.md §1`:

The ladder terminates at P1: every computational need of the 19 units is covered
by a script that already exists in `scripts/` or `skills/`, or by a script the
plan itself assigns to `implementer_agent` (`U02`). The remaining rungs are `not reached`.

| Rung | Source | Result | Evidence |
| :--- | :--- | :--- | :--- |
| P1 | `skills/manifest_skills.json` | hit | The manifest lists 34 skills. Used: `omni-context-minimizer` (line 199), `python-quality-auditor`, `token-saver-auditor`, `topology-monitor`, `compliance-checker`, `graphify`. Reproduce: `python3 -c "import json;print([s['name'] for s in json.load(open('skills/manifest_skills.json'))['skills']])"` |
| P2 | `autoskills-3rd` | not reached | P1 covered every unit. `skills/autoskills-3rd/` exists locally (README.md, SKILL.md, scripts/) and was not consulted |
| P3 | `https://skills.sh/` (WebSearch/WebFetch; simulated JSON allowed in tests) | not reached | No unit has an uncovered need, so no external query was issued |
| P4 | Three-File Standard at Destination | not reached | No destination was chosen because nothing needed building |

`scripts/with_env.py` (`U02`) is **not** a skill. It is a framework-root script
authored by `implementer_agent` (`ADR-0009`, `agents.md §6 devops_agent` row). Its invoker is
declared in the plan's Mechanisms table (`RA-16`): `Makefile` `graphify-deep`,
`rules/project_topology.md`, `agents.md RA-09`. A skill would add a `SKILL.md`
and a `README.md` around a single stdlib script with one caller path, which
`agents.md §3 three_file_standard` classes as padding.

---

## 2. Per-unit tool resolution

| Unit | Skill / tool | Destination | P1–P4 trail |
| :--- | :--- | :--- | :--- |
| `U01` | none (human-launched measurement). `jq` and the `claude` CLI only | N/A | P1 hit (no skill applies); P2-P4 not reached |
| `U02` | none (script is the deliverable). Gate: `skills/python-quality-auditor` (`ruff`/`mypy`/`bandit`/`radon` pass/fail lines) plus `make quality-audit` | N/A | P1 hit; P2-P4 not reached |
| `U03` | none (JSON data file). `make verify` JSON-parse step covers it | N/A | P1 hit; P2-P4 not reached |
| `U04` | `skills/python-quality-auditor` on `scripts/merge_json.py` (102 lines, read in full, no skeleton needed) | N/A | P1 hit; P2-P4 not reached |
| `U05` | `skills/omni-context-minimizer` (`scripts/install.py` exceeds 200 lines; extract the skeleton of `merge_into`, then read that function only) plus `skills/python-quality-auditor` | N/A | P1 hit; P2-P4 not reached |
| `U06` | `skills/omni-context-minimizer` (`scripts/session_start.py` exceeds 200 lines; read around line 489 only) plus `skills/python-quality-auditor` | N/A | P1 hit; P2-P4 not reached |
| `U07` | none. `jq -e` checks from the plan's Verification table; `make verify` JSON parse | N/A | P1 hit; P2-P4 not reached |
| `U08` | none for the edit. `graphify` is the tool whose invocation the Makefile target changes; it is exercised, not used, by the unit | N/A | P1 hit; P2-P4 not reached |
| `U09` | none. `skills/token-saver-auditor` `audit_plan.py` is not applicable (it audits plans); the file is read with offset/limit | N/A | P1 hit; P2-P4 not reached |
| `U10` | none. Read with offset/limit | N/A | P1 hit; P2-P4 not reached |
| `U11` | none. Read with offset/limit | N/A | P1 hit; P2-P4 not reached |
| `U12` | `skills/graphify/SKILL.md` is the target, not a tool. Verdict: treated as vendored, unit **omitted** (see §6) | N/A | P1 hit; P2-P4 not reached |
| `U13` | `grep -n 'RA-09\|secret_sovereignty' agents.md` then partial read (177 lines but rows of several thousand characters, so no full dump), plus `skills/compliance-checker` (post-edit scan for rule contradictions between `RA-09`, `§3` and `rules/LEGACY_RULE_CONCORDANCE.md`) | N/A | P1 hit; P2-P4 not reached |
| `U14` | none. Read with offset/limit | N/A | P1 hit; P2-P4 not reached |
| `U15` | none. Read with offset/limit | N/A | P1 hit; P2-P4 not reached |
| `U16` | none. Read with offset/limit | N/A | P1 hit; P2-P4 not reached |
| `U17` | none. `grep -n 'Rule 66'` then partial read (`RA-14` propagation grep) | N/A | P1 hit; P2-P4 not reached |
| `U18` | none. Partial read at `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md:1600` | N/A | P1 hit; P2-P4 not reached |
| `U19` | none. Cites SHAs by hand per `agents.md §0 Master Ledger` | N/A | P1 hit; P2-P4 not reached |
| `U20` | none. Partial read of `agents/devops_agent.md` (under 200 lines) | N/A | P1 hit; P2-P4 not reached |

Cross-cutting, not tied to a unit: `venv_skillopt/bin/python -m graphify update .`
after the code units (`agents.md §2 graph_sync`), and `skills/topology-monitor`
at the Phase 7 gate (see §3).

---

## 3. Skills used

| Skill | Why |
| :--- | :--- |
| `omni-context-minimizer` | `agents.md §2 ast_skeleton`. Files above 200 lines in this sprint: `scripts/install.py` (561, `U05`) and `scripts/session_start.py` (625, `U06`). Skeleton first, then offset/limit reads. Reproduce: `wc -l` on the 19 unit files; every other unit file is 177 lines or fewer (`agents.md` 177, `rules/qa_and_testing.md` 91) |
| `python-quality-auditor` | Python units `U02`, `U04`, `U05`, `U06`. Prints a pass/fail line per tool and never exits non-zero, so it is advisory. The gating instruments stay `make verify` (`ruff`) and `make quality-audit` (function length 50, nesting 3) |
| `compliance-checker` | `U13` only. It rewrites a governance rule, the highest-risk edit in the plan, and the scan checks it against the downstream rows that must follow (`U17`) |
| `graphify` | Graph queries before any recursive grep (`agents.md §2 graph_sovereignty`) and the post-change `update` (`graph_sync`). Also the consumer whose key problem motivates `with_env.py` |
| `topology-monitor` | Phase 7 `skill_standard_check` via `skills/topology-monitor/scripts/legacy_app_auditor.py` (`agents.md §3 enforcement`). This sprint adds no skill, so the expected result is no new findings |

## 4. Skills considered and rejected

| Candidate | Why rejected |
| :--- | :--- |
| `token-saver-auditor` | Already run on the plan itself (`audit_plan.py`, `[OK]`, exit `0`, per the plan's Verification table). It audits plans and `task_scope`, not the 19 source units. `rules/token_economy.md` is loaded only when authoring `task_scope.md`, which belongs to `rule_validator` |
| `env-shielding-auditor` | Scans for hardcoded secrets and `.env` Gitignore status. Sprint 055 changes how a secret is supplied to a process, not where one is stored. Running it would not exercise `with_env.py` and would read `.env` paths, which `RA-09` prohibits |
| `mass-standardizer` | Regenerates `skills/manifest_skills.json`. No skill is added or removed, so the manifest is unchanged |
| `skill-creator`, `skills-samples-3rd`, `autoskills-3rd` | Skill authoring and discovery tools. No skill is built |
| `skillopt` | `agents.md` is rewritten by `U13`, and `skillopt` may score it, but the run needs explicit human authorization per run (`rules/skills_and_integrations.md`) and belongs to `close_workflow.md` `rules_optimization`, not to a unit |
| `js-standardizer`, `vite`, `tailwind-css-patterns`, `typescript-advanced-types`, `nodejs-*`, `vercel-*`, `accessibility`, `seo`, `frontend-design` | No JS/TS or frontend unit in the plan |
| `django-*` (`django-expert-3rd`, `django-patterns-3rd`, `django-security-3rd`, `django-tdd-3rd`, `django-verification-3rd`) | No Django unit in the plan |
| `contract-writer`, `readme-standardizer`, `sprint-architect`, `slash-commander`, `mcp-registry`, `topology-scaffolder` | No contract, README, sprint scaffold, slash command, MCP entry or directory scaffold is touched. `topology-scaffolder` is also prohibited in the nucleus (`agents.md §5 nucleus_neutrality`) |

## 5. Gaps

None. No unit lacks a covering tool, so no skill is built.

Two observations that do not change an assignment:

| Observation | Consequence |
| :--- | :--- |
| `skills/graphify/` has no `-3rd` suffix, no `README.md`, and no entry in `config/invocation_exceptions.json`, although its content is upstream-authored (§6) | Recorded for `governance_learner`. Out of scope for Sprint 055; fixing it would rename a manifest path and touch `U12`'s own target |
| `skills/env-shielding-auditor/README.md:41` names a `scripts/shield_audit.sh` that does not exist (already noted in `config/invocation_exceptions.json`) | Not used by this sprint; no action |

---

## 6. `U12` — is `skills/graphify/SKILL.md` vendored material?

**Verdict: treat as vendored. `U12` is omitted**, and the correction of the key list
(7 names measured against 2 claimed at `skills/graphify/SKILL.md:238`) goes only in `rules/graphify.md`
(`U11`), as plan decision `D9` provides. The plan's own fallback applies, with the omission
recorded in `SPRINT_LOG.md`.

| Evidence | Source | Reproduce |
| :--- | :--- | :--- |
| Authored upstream, not by this repository: line 747 reads `If graphify saved you time, consider supporting it: https://github.com/sponsors/safishamsi` | `skills/graphify/SKILL.md:747` | `sed -n 747p skills/graphify/SKILL.md` |
| Single-commit bulk import of 1114 lines, no history of local edits | `cde6a71` `feat(graphify): register mcp server and add local skill #067` | `git log --format='%h %s' -- skills/graphify/SKILL.md` returns one commit |
| The claim at line 238 describes the upstream package's behaviour, in the first person of the upstream tool (`graphify does **not** read ANTHROPIC_API_KEY...`) | `skills/graphify/SKILL.md:238` | `sed -n 238p skills/graphify/SKILL.md` |
| The skill is a bare `SKILL.md` carrying the upstream `trigger: /graphify` frontmatter key, with no `README.md` and no `scripts/` | `ls skills/graphify` returns `SKILL.md` | `ls skills/graphify` |
| `rules/skills_and_integrations.md §3`, `Skill Documentation Veto`: modifying the technical specifications of an imported external skill is prohibited | `rules/skills_and_integrations.md` §3 | `grep -n 'Skill Documentation Veto' rules/skills_and_integrations.md` |

Counter-evidence, stated so the verdict is not read as certain:

| Counter-evidence | Reproduce |
| :--- | :--- |
| The directory lacks the mandatory `-3rd` suffix (`§3 Nomenclature Mandate`); the seven directories that carry it are `autoskills-3rd`, `django-expert-3rd`, `django-patterns-3rd`, `django-security-3rd`, `django-tdd-3rd`, `django-verification-3rd`, `skills-samples-3rd` | `ls -d skills/*-3rd` |
| `config/invocation_exceptions.json` has no `graphify` entry, so the repository never declared it `vendored-reference` (its `vendored-reference` entries cite `affaan-m/ECC`) | `grep -c -i graphify config/invocation_exceptions.json` returns `0` |
| No `NOTICE.md` or provenance file exists in `skills/graphify/` | `ls skills/graphify` |

Reasoning: the repository never registered the file as vendored, but the immutability rule
protects upstream technical content and the content here is upstream's by its own text.
Editing it would diverge the local copy from upstream with no provenance record to
reconcile against. Omitting `U12` costs nothing, because `rules/graphify.md` is the
file agents load for graphify procedure (`agents.md §0 Rule Contexts`). If the human
rules the file native instead, `U12` reverts to the plan's original wording and
the `-3rd` rename gap in §5 closes with it.
