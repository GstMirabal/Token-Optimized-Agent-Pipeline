# Skill Assignment — Sprint 057 (s0-lane-and-defect-block)

Source: `docs/sprints/057-core-pipeline/IMPLEMENTATION_PLAN.md`.
Phase 4.2 of `workflows/pipeline_workflow.md`. Drafted from this template.

Mode: **claude-code**, `delegation_mode: native`.

After writing this file, run:
`python3 scripts/check_forge_ladder.py --sprint-dir docs/sprints/057-core-pipeline`
(exit `2` rejects an empty forge destination or submodule contamination).

---

## 1. Priority ladder (record every rung)

`rules/skills_and_integrations.md §1`:

The ladder terminates at the first rung. Every unit W00-W37 is served by a tool
already present in `skills/`, by the Python standard library, or by editing an
existing file. The plan's Dependencies table adds no package. Rungs two to four
are `not reached`.

| Rung | Source | Result | Evidence |
| :--- | :--- | :--- | :--- |
| P1 | `skills/manifest_skills.json` | Hit: all required capabilities are covered | The manifest lists `python-quality-auditor`, `omni-context-minimizer`, `token-saver-auditor`, `env-shielding-auditor`, `compliance-checker`, `topology-monitor`, `mcp-registry`, `readme-standardizer`; sections 2 and 3 map each unit to them or to stdlib |
| P2 | `autoskills-3rd` | not reached | Rung one covers every unit |
| P3 | `https://skills.sh/` (WebSearch/WebFetch; simulated JSON allowed in tests) | not reached | No unit needs a capability absent from `skills/` |
| P4 | Three-File Standard at Destination | not reached | No skill is created; `Destination` is `N/A` in every row of section 2 |

No skill was forged in Sprint 057. No new skill forged means no `Destination`
other than `N/A`, no host skill directory written, and no submodule write.

`claude-api` (W00) is a Claude Code harness skill loaded at session level, not a
directory of `skills/` and not a manifest entry. It is consulted for its
current prompting guidance and nothing is copied into the repository from it.

---

## 2. Per-unit tool resolution

`Skill / tool` names what the unit's assignee runs. `stdlib` means Python
standard library only, run through `python3`. Files above 200 lines are read
through `omni-context-minimizer` first (`agents.md §2 ast_skeleton`), then by
partial `offset`/`limit` reads.

| Unit | Skill / tool | Destination | P1–P4 trail |
| :--- | :--- | :--- | :--- |
| W00 | `claude-api` (harness skill, prompting guidance for Opus 5.5); `token-saver-auditor` on the finished guide | N/A | Rung one; others not reached |
| W07 | `omni-context-minimizer` for `rules/qa_and_testing.md` if above 200 lines; `compliance-checker` on the amended §4 | N/A | Rung one; others not reached |
| W08 | none (single-table edit of a template) | N/A | Rung one; others not reached |
| W09 | `python-quality-auditor` (ruff, mypy, bandit on `scripts/check_gate_log.py`); stdlib `pytest` | N/A | Rung one; others not reached |
| W01 | none; headless `claude -p` per `docs/sprints/056-core-pipeline/SANDBOX_ENUMERATION.md`; `env-shielding-auditor` is NOT run on `.env` (`RA-09`) | N/A | Rung one; others not reached |
| W02 | `env-shielding-auditor` (confirms `./.env` stays denied after the `./.env.agent` rule is added); stdlib `json` for the template test | N/A | Rung one; others not reached |
| W03 | `env-shielding-auditor` (secret-handling review of a script that compares credential files; prints names only); `python-quality-auditor`; stdlib `re`, `pathlib` | N/A | Rung one; others not reached |
| W04 | `python-quality-auditor`; stdlib `socket`, `urllib.parse` | N/A | Rung one; others not reached |
| W05 | `compliance-checker` on the amended database section; `omni-context-minimizer` if the file is above 200 lines | N/A | Rung one; others not reached |
| W06 | `compliance-checker` (one-sentence edit to `RA-09`); `omni-context-minimizer` mandatory (`agents.md` is above 200 lines) | N/A | Rung one; others not reached |
| W10 | `omni-context-minimizer` mandatory (`scripts/session_state.py`, 872 lines); `python-quality-auditor` | N/A | Rung one; others not reached |
| W11 | `omni-context-minimizer` if `workflows/deployment_workflow.md` is above 200 lines; `compliance-checker` | N/A | Rung one; others not reached |
| W12 | `omni-context-minimizer` mandatory (`scripts/session_state.py`); `python-quality-auditor` | N/A | Rung one; others not reached |
| W13 | `python-quality-auditor`; stdlib `json`, `sys.stdin` | N/A | Rung one; others not reached |
| W14 | `python-quality-auditor`; stdlib `tempfile`, `py_compile` | N/A | Rung one; others not reached |
| W15 | `python-quality-auditor`; stdlib `re` | N/A | Rung one; others not reached |
| W16 | `omni-context-minimizer` mandatory (`hooks/on_commit.py`, 1144 lines); `python-quality-auditor` | N/A | Rung one; others not reached |
| W17 | `omni-context-minimizer` mandatory (`scripts/check_fix_reproduces.py`, 384 lines); `python-quality-auditor` | N/A | Rung one; others not reached |
| W18 | `omni-context-minimizer` mandatory (`scripts/check_fix_reproduces.py`); `python-quality-auditor`; stdlib `subprocess`, `git` | N/A | Rung one; others not reached |
| W19 | `omni-context-minimizer` mandatory (`scripts/check_task_scope.py`, 323 lines); `python-quality-auditor` | N/A | Rung one; others not reached |
| W20 | `omni-context-minimizer` mandatory (`scripts/model_ledger.py`, 254 lines); `python-quality-auditor` | N/A | Rung one; others not reached |
| W21 | `omni-context-minimizer` mandatory (`scripts/detect_drift.py`, 595 lines); `python-quality-auditor`; stdlib `git` | N/A | Rung one; others not reached |
| W22 | `omni-context-minimizer` if `workflows/reconciliation_workflow.md` is above 200 lines; `compliance-checker` | N/A | Rung one; others not reached |
| W23 | `omni-context-minimizer` mandatory (`scripts/session_start.py`, 718 lines); `python-quality-auditor` | N/A | Rung one; others not reached |
| W24 | `omni-context-minimizer` if `scripts/check_role_artifact.py` is above 200 lines; `python-quality-auditor` | N/A | Rung one; others not reached |
| W25 | `omni-context-minimizer` mandatory (`scripts/session_state.py`); `python-quality-auditor`; stdlib `grep` over `workflows/ rules/ agents.md` | N/A | Rung one; others not reached |
| W26 | `python-quality-auditor`; stdlib `shutil`, `pathlib`, `filecmp` | N/A | Rung one; others not reached |
| W27 | `compliance-checker` (invoker declaration, `RA-16`) | N/A | Rung one; others not reached |
| W28 | `omni-context-minimizer` mandatory (`scripts/session_state.py`); `python-quality-auditor` | N/A | Rung one; others not reached |
| W29 | `compliance-checker`; `token-saver-auditor` (Phase 2 rewrite must not add always-loaded narrative) | N/A | Rung one; others not reached |
| W30 | `omni-context-minimizer` mandatory (`scripts/merge_json.py`, 290 lines); `python-quality-auditor`; stdlib `json` | N/A | Rung one; others not reached |
| W31 | `python-quality-auditor`; stdlib `subprocess` (`git tag`), `re` | N/A | Rung one; others not reached |
| W32 | none (one-line Makefile edit); `topology-monitor` is not needed | N/A | Rung one; others not reached |
| W33 | `mcp-registry` (the file under edit is that skill's `registry.json`; its SKILL.md defines the registry protocol); stdlib `json` | N/A | Rung one; others not reached |
| W34 | `python-quality-auditor` (docstring-only edit) | N/A | Rung one; others not reached |
| W35 | none; stdlib `json` to confirm `memory_index.json` still parses | N/A | Rung one; others not reached |
| W36 | `omni-context-minimizer` mandatory (`scripts/install.py`, 756 lines); `python-quality-auditor` | N/A | Rung one; others not reached |
| W37 | `readme-standardizer` (its README rule governs the badge); `env-shielding-auditor` is the edited skill, not a tool for the edit | N/A | Rung one; others not reached |

`Destination` for a forged skill: none this sprint. Every row is `N/A`.
Writing under the submodule skills tree from a host session is PROHIBITED
(`strict_rule`); this sprint runs in nucleus mode and writes none.

Whole-sprint tools, not tied to one unit:

| Tool | Where it applies |
| :--- | :--- |
| `token-saver-auditor` | Phase 1/4 audit of `task_scope.md` and of the plan; also run on W00 and W29 |
| `python-quality-auditor` | Quality gate over every new or modified `.py` file (W03, W04, W09, W10, W12-W21, W23-W26, W28, W30, W31, W34, W36) |
| `make verify` | Final gate: ruff, `make quality-audit`, `scripts/check_forge_ladder.py` |

---

## 3. Skills used

| Skill | Why |
| :--- | :--- |
| `omni-context-minimizer` | Required before reading any file above 200 lines: `hooks/on_commit.py` (1144, W16), `scripts/session_state.py` (872; W10, W12, W25, W28), `scripts/session_start.py` (718; W23), `scripts/install.py` (756; W36), `scripts/detect_drift.py` (595; W21), `scripts/check_fix_reproduces.py` (384; W17, W18), `scripts/check_task_scope.py` (323; W19), `scripts/merge_json.py` (290; W30), `scripts/model_ledger.py` (254; W20) |
| `python-quality-auditor` | Runs ruff, mypy and bandit on each Python unit; ruff `0.16.3` is the pinned gate. It prints pass/fail per tool and computes no score |
| `env-shielding-auditor` | W02, W03: the `.env.agent` units touch the secret prohibition of `RA-09`; the audit confirms no value reaches output and `./.env` stays denied. It runs against source files, never against `.env` |
| `token-saver-auditor` | W00 and W29 add text that is loaded on later sessions; the audit checks plan and scope cost. Also the Phase 1/4 audit of the sprint artifacts |
| `compliance-checker` | W05, W06, W07, W11, W22, W27, W29: governance-text edits are scanned for rule violations before QA |
| `mcp-registry` | W33: the edited file is the skill's registry; its SKILL.md is the protocol the edit must keep |
| `readme-standardizer` | W37: governs README structure for the badge correction |
| `claude-api` (harness skill) | W00: source of the current Opus 5.5 prompting guidance for `docs/guides/PROMPT_CRITERIA_GUIDE.md` (D7); consulted, not copied in |

## 4. Skills considered and rejected

| Candidate | Why rejected |
| :--- | :--- |
| `skill-creator` | No skill is created; the plan adds no dependency and no unit lacks a tool |
| `skillopt` | No instruction file is trained; training overwrites its target and needs separate human authorization (`rules/skills_and_integrations.md`) |
| `autoskills-3rd` | Rung one resolved every unit |
| `mass-standardizer` | No skill directory changes shape, so `skills/manifest_skills.json` is not regenerated. W33 and W37 edit content, not structure |
| `topology-monitor` | Its skill-standard auditor is run by `make verify`; no unit needs it directly. W32 is a one-line Makefile edit |
| `topology-scaffolder` | `docs/` exists; scaffolding is PROHIBITED in the nucleus (`nucleus_neutrality`) |
| `graphify` | Used by the process at post-change sync (`graph_sync`), not by any unit |
| `sprint-architect` | The work breakdown exists in the approved plan |
| `contract-writer` | No API contract is written |
| `slash-commander` | No workflow gains a slash command; W27 and W29 edit existing workflows |
| `js-standardizer`, `typescript-advanced-types`, `vite`, `tailwind-css-patterns`, `vercel-*`, `nodejs-*`, `frontend-design`, `accessibility`, `seo` | No unit touches JS/TS or frontend files |
| `django-*-3rd` | No unit touches Django code |
| `skills-samples-3rd` | Reference examples only |

## 5. Gaps

None. No unit lacks a tool, and no skill is forged.

Notes for the executing agents, not gaps:

- W01 is a measurement unit run by `devops_agent` with headless `claude -p`; no skill wraps that method.
- W03 handles credentials: output is variable names only, never values (`RA-09`). Run the script only through the hook or by the human; the agent does not read `.env`.
- W16 and W10/W12/W25/W28 each touch a large file that several units share. `jurisdictional_lock` applies: no two in-progress units claim the same file. The ordering is a matter for `task_scope.md`, not for this file.
