# 🏛️ Structural Audit Report: `.agents` nucleus (core / pipeline)
**Audit ID**: #A059-RVA
**Auditor**: `rule_validator` coordinating (`agents.md §6 rule_validator`), nucleus mode (`scripts/_mode.py`: `.git` is a real directory)

---

## 🚦 Executive Summary

Structural, topological and legal sweep of the pipeline environment, run at
Sprint 059's close because the `docs_freshness_gate` of `close_workflow.md`
returned `[BLOCK] Structural change since last audit exceeds the p90 delta
threshold — refresh anchors`. The last audited sprint is `057`
(`docs/active_state.json` `current_sprint.last_audit_sprint`). The sweep reads
the tree as it is at `HEAD` (`6070171`) on `ai-sprint/059`.

**Why this audit exists rather than a field being incremented.** Same
reasoning as `PIPELINE_AUDIT_REPORT-057.md`: bumping `last_audit_sprint` from
`57` to `59` without the sweep would assert something that had not happened.
This report is what makes `last_audit_sprint: 59` true.

| Metric | Score | Status |
| :--- | :--- | :--- |
| **Architectural Purity** | 100/100: `legacy_app_auditor.py` and `verify_commands.py` exit `0` (lead-measured, § Sweep results); no file added outside the layer `agents.md §3` and `§5` name was found by this audit | ✅ |
| **Governance Compliance** | 94/100: two false statements in `rules/` (A1, A2), one contradiction between the `enforcement` row and a skill (A3) and one recorded S3 (A4) | ⚠️ |
| **Unit Coverage** | Not measured by this audit. The last count in the sprint record is `make verify` `1924 passed` at QA Gate 1 round 34 (`SPRINT_LOG.md:216`) | n/a |

Score justification: Compliance loses 2 points per S2 finding (A1, A2, A3) and
none for S3 or Info. Coverage is quoted from the sprint log; this audit ran no
test and computes no percentage.

### The measurement that triggered it

`node_delta` (`scripts/docs_freshness_check.py:424`) is
`|Δnodes| + |Δedges| + 100 × max(0, Δcommunities)`. The threshold is
`percentile(deltas, 90)` over the last `GRAPH_STATS_WINDOW` = 10 snapshots with
id below the current sprint (`structural_change_status`, `:545-552`); the
percentile is `sorted[min(n-1, round(0.9 × (n-1)))]` (`:342-347`), here index
`round(0.9 × 8)` = `7`.

Snapshots are read from `docs/sprints/0NN-core-pipeline/graph_stats.json`
(nodes / edges / communities). `051` has no snapshot (carried, A6).

| Window id → id | Nodes | Edges | Communities | `node_delta` |
| :--- | :--- | :--- | :--- | :--- |
| 048 → 049 | 10056 → 10371 | 12840 → 13368 | 862 → 890 | `315 + 528 + 2800` = `3643` |
| 049 → 050 | 10371 → 10586 | 13368 → 13726 | 890 → 903 | `215 + 358 + 1300` = `1873` |
| 050 → 052 | 10586 → 11761 | 13726 → 15788 | 903 → 950 | `1175 + 2062 + 4700` = `7937` |
| 052 → 053 | 11761 → 12375 | 15788 → 16638 | 950 → 994 | `614 + 850 + 4400` = `5864` |
| 053 → 054 | 12375 → 12841 | 16638 → 17475 | 994 → 1037 | `466 + 837 + 4300` = `5603` |
| 054 → 055 | 12841 → 13240 | 17475 → 18156 | 1037 → 1059 | `399 + 681 + 2200` = `3280` |
| 055 → 056 | 13240 → 13677 | 18156 → 18834 | 1059 → 1062 | `437 + 678 + 300` = `1415` |
| 056 → 057 | 13677 → 14521 | 18834 → 20190 | 1062 → 1101 | `844 + 1356 + 3900` = `6100` |
| 057 → 058 | 14521 → 15421 | 20190 → 21921 | 1101 → 1124 | `900 + 1731 + 2300` = `4931` |

Window, sorted: `[1415, 1873, 3280, 3643, 4931, 5603, 5864, 6100, 7937]`.
**p90 threshold = `6100`.**

| Transition (current = 059: `17320 / 25284 / 1210`) | `\|Δnodes\|` | `\|Δedges\|` | `100 × Δcommunities` | `node_delta` | Exceeds `6100`? |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 057 → 059 (what the gate compares: `last_audit_sprint` 57 → current) | `2799` | `5094` | `10900` (109) | `18793` | Yes |
| 058 → 059 (this sprint alone) | `1899` | `3363` | `8600` (86) | `13862` | Yes |

Unlike Sprint 057's breach, the sprint's own transition alone exceeds the
threshold, at 2.3 times its value. Sprint 058 closed without an audit
(`docs/audits/` holds no `-058` report); its transition (`4931`) stayed under
`6100`, so the gate stayed silent until Sprint 059. Communities contribute
`10900` of `18793` (58%) for 057 → 059. The snapshot note
(`docs/sprints/059-core-pipeline/graph_stats.json`) records 834 files at the
snapshot; this audit does not attribute the growth to individual modules.

---

## 🔍 Structural Findings & Rule Amendments

| ID | Step | Severity | File:line | Proof | Disposition |
| :--- | :--- | :--- | :--- | :--- | :--- |
| A1 | `rule_introspection` | S2 | `rules/project_topology.md:81` vs `claude/settings.hooks.json:76-89`; `agents.md` `RA-09` row | Line 81 says "the template today holds only `denyRead` of `./.env` and `./.env.*`" and that the settings files "change in later implementation units". The template's `sandbox.filesystem.denyRead` holds twelve entries (`./.env`, `./.env.*`, `~/.docker/config.json`, `~/.config/gh`, `~/.zsh_history`, `~/.claude/projects`, the keychain path, `~/.ssh`, `~/.aws`, `~/.npmrc`, `~/.bash_history`, `~/**/.env*`), and `permissions.deny` holds `Read(/**/.env*)` (`:22`). The `agents.md` `RA-09` row already lists these denies as present. A rule that tells an agent what the template contains states a false fact (`instructing`) | open, routed to the Sprint 059 close remediation (edit of `rules/project_topology.md:81`, by the role that owns `rules/`; this audit does not edit) |
| A2 | `rule_introspection` | S2 | `rules/project_topology.md:26-27` vs `:41`, `:82`, `:86` | Line 26 names one `Measuring CLI`, `2.1.119`, and line 27 says "Every row is a measurement of that version". Line 41 reports a measurement on CLI `2.1.319`, line 82 cites `2.1.322`, and line 86 states `strictAllowlist` "needs Claude Code 2.1.219 or later", so that row cannot be a `2.1.119` measurement. `ADR-0022` line 41 states the A5 rules were measured on `2.1.119` only. Effect: `scripts/session_start.py:65` compares `claude --version` with the `2.1.119` row, so the advisory fires on every boot under `2.1.322`; the advisory does not block | open, routed to Sprint 060 (amend the `Measuring CLI` and `Re-measure trigger` rows after the matrix re-run their text demands, or state a per-row version) |
| A3 | `rule_introspection` | S2 | `agents.md:86` and `rules/skills_and_integrations.md:44` vs `skills/mass-standardizer/SKILL.md:3,14,28-31`, `skills/mass-standardizer/scripts/mass_standardizer.py:42,63` | The rows say `mass-standardizer` "only regenerates `skills/manifest_skills.json`". The skill's own description says it "detects skills missing the Three-File Skill Standard ... and injects the missing artifacts from templates", and the script defines `SKILL_MD_TEMPLATE` (`:42`) and `README_MD_TEMPLATE` (`:63`). Source of the contradiction: both sides read, the script was not run. Sprint 059 moved the row text to `rules/skills_and_integrations.md §4` (`D18`); this audit did not establish who introduced the claim | open, routed to Sprint 060 (decide which side is true; `enforcement` row or skill text) |
| A4 | `rule_introspection` | S3 | `rules/qa_and_testing.md:68`; same wording at `rules/code_craft.md:80` | Recorded as `R33-4` (`SPRINT_LOG.md:305`, QA Gate 1 round 33, S3 `testifying`, not rediscovered): both rules quote the fix pattern `^fix(\([^)]*\))?!?:\|^fix\(` without saying it is matched case-insensitively. The code is: `scripts/check_remediation_chain.py:36` (`re.IGNORECASE`), `hooks/on_commit.py:160`. The `code_craft.md:80` extension is this audit's: same sentence, same omission | open, routed to the QA record (`R33-4`, round 33), no gate reopened (S3) |
| A5 | `nomenclature` | S3 | see § Nomenclature verdicts, group R | Nine files break `RA-06` Option B | rename candidate, awaiting human |
| A6 | `report` | Info | `docs/active_state.json` (`current_sprint.last_audit_sprint`); `docs/sprints/051-core-pipeline/` | Sprint 058 closed without an audit, so the gate compared against `057` (same pattern as A3 of `-057.md`). `051` has no `graph_stats.json` (carried from `-057.md` A4) | recorded |

No finding is "neutralized": none of A1-A4 has a fixing commit.

### Rule cross-reference performed (`rule_introspection`), scoped to this sprint's changes

Method: `git` is not available to this role in this session (no shell), so
`git diff --stat 08c669c..HEAD -- agents.md rules/` was not run. The changed
surface was taken from the lead's list and read directly: `agents.md`,
`rules/project_topology.md` §4-§6, `rules/qa_and_testing.md` §4,
`rules/token_economy.md` §1-§4, `rules/code_craft.md` §6-§8,
`rules/skills_and_integrations.md` §1-§4, plus
`docs/guides/RULE_PRECEDENTS_GUIDE.md`, `claude/settings.hooks.json` and
`config/rule_triggers.json`. The `agents.md` size cap of 20000 bytes was
**not measured**: no instrument in `tests/`, `scripts/`, `hooks/`, `config/` or
`Makefile` checks it, and this role has no `wc`.

| # | Subject | Locations compared | Contradiction? |
| :--- | :--- | :--- | :--- |
| 1 | Pointers from `agents.md` into `rules/` | `agents.md` rows citing `rules/code_craft.md §8`, `rules/project_topology.md §5` and `§6`, `rules/skills_and_integrations.md §4`, `rules/qa_and_testing.md §4` and `§7`, `rules/token_economy.md` against the headings of those files (`code_craft.md:108-157`, `project_topology.md:57,105,117`, `skills_and_integrations.md:30-44`, `qa_and_testing.md:52,149`) | No. Every cited section exists |
| 2 | Rule-context index | `agents.md §0` table (11 rows) vs `config/rule_triggers.json` (11 `path` entries) vs `rules/` (11 files) | No. Same eleven files |
| 3 | `(precedents)` pointers | `agents.md` rows marked `(precedents)` (Implementation Plan, Master Ledger, `triple_lock`, `jurisdictional_lock`, `feedback_upstream`, `RA-11`, `RA-12`) vs headings of `docs/guides/RULE_PRECEDENTS_GUIDE.md` (`:19,23,47,63,199,147,151`) | No. Each key has a heading |
| 4 | Template contents vs sandbox rules | `agents.md` `RA-09`, `rules/project_topology.md:36,54,81-86`, `claude/settings.hooks.json` | Yes: A1 |
| 5 | Measuring CLI version | `rules/project_topology.md:26-27,41,82,86`, `rules/qa_and_testing.md:132`, `docs/decisions/ADR-0022-sandbox-regime-amendment.md:41`, `scripts/session_start.py:65` | Yes: A2 |
| 6 | `gh` under the sandbox | `rules/project_topology.md:41-44` (canonical row) vs `:76` of the same file's §5 `RA-09` and `agents.md` `RA-09` | No. All say the human runs `gh` under the template sandbox; the §5 text points to the §4 row |
| 7 | Egress | `rules/project_topology.md:45,86-87` vs `claude/settings.hooks.json:68-73` | No. The template lists four project-scope domains; the user-scope command lists five (adds `registry.npmjs.org`). Different scopes, and line 86 says the project list does not deny |
| 8 | Skill auditor vs generator | `agents.md:86`, `rules/skills_and_integrations.md:44`, `skills/mass-standardizer/SKILL.md` | Yes: A3 |
| 9 | Severity scale and verdict classes | `rules/qa_and_testing.md:54-99` vs `agents.md` `RA-17` | No. `S0` never `RECORD` (`:85`) and the precedence rule (`:86`) reconcile the `testifying` class with severity |
| 10 | Fix-commit pattern | `rules/qa_and_testing.md:68`, `rules/code_craft.md:80` vs `scripts/check_remediation_chain.py:36`, `hooks/on_commit.py:160` | Wording gap only: A4 (`R33-4`) |
| 11 | `R-4` applicability bound | `rules/qa_and_testing.md:71` ("sprint ids >= 58") vs `scripts/check_gate_log.py:58` (`NOTES_FROM = 58`) | No |
| 12 | `R-5` blast radius | `rules/qa_and_testing.md:72` vs `config/blast_radius.json:9` (`full_suite_command`) | No. The command string matches |
| 13 | Session bound | `rules/token_economy.md:37-40` vs `scripts/session_cost.py:70` (`HARD_CONTEXT = 550_000`, `--bound` at `:428`) and `scripts/session_probe.py:681` (`probe_cost`) | No |
| 14 | Re-read of `agents.md` | `rules/token_economy.md:25` ("re-read it only after context compaction") vs `agents.md §2 anti_amnesia` ("once per session (at start) and after any context compaction") | No contradiction in effect: `token_economy.md:25` is about per-step re-reads and says the constitution loads once through the host import. Not filed |

### Sweep results, each with the command that produced it

Measured by the lead before this report; recorded literally.

| Step | Command | Result |
| :--- | :--- | :--- |
| `skill_standard_check` | `python3 skills/topology-monitor/scripts/legacy_app_auditor.py` | exit `0`, `✨ [AUDIT PASSED]: Pipeline Structure is Valid.` |
| `link_audit` | `python3 skills/slash-commander/scripts/verify_commands.py` | exit `0`, `All command references resolve (13 commands checked)`; the guide names every command stem (13) |
| `federation_audit` | Not run: nucleus mode skips the tag, lock and submodule checks (`audit_workflow.md` row; the bridge check belongs to `start_workflow` `bridge_check`) | n/a |
| `precision_audit` | `venv_skillopt` has no `skillopt` module (`ModuleNotFoundError: No module named 'skillopt'`) | `precision_audit skipped: skillopt stack absent` |

### Nomenclature verdicts

Scope: files under `docs/` outside `docs/sprints/` (Glob over `docs/**`). Names
are judged against `RA-06` Option B (`[MODULE]_[TYPE].md`). Listing only; no
file was renamed.

**Group R: rename candidates (awaiting human approval).**

| # | Current path | Why it breaks Option B | Proposed name |
| :--- | :--- | :--- | :--- |
| R1 | `docs/architecture/global_topology.md` | lowercase; no `[TYPE]` suffix | `GLOBAL_TOPOLOGY_MAP.md` |
| R2 | `docs/architecture/topology_map.md` | lowercase; the body is the `topology-mapper` product | `TOPOLOGY_MAP.md` |
| R3 | `docs/contracts/core/doc_orchestrator_contract.md` | lowercase | `DOC_ORCHESTRATOR_CONTRACT.md` |
| R4 | `docs/contracts/core/topology_mapper_contract.md` | lowercase | `TOPOLOGY_MAPPER_CONTRACT.md` |
| R5 | `docs/contracts/core/topology_scaffolder_contract.md` | lowercase | `TOPOLOGY_SCAFFOLDER_CONTRACT.md` |
| R6 | `docs/audits/TOKEN_ECONOMY_AUDIT-documentation-standard.md` | hyphen-joined lowercase slug after the `[TYPE]` | `TOKEN_ECONOMY_DOCUMENTATION_STANDARD_AUDIT.md` |
| R7 | `docs/audits/SKILLOPT_TRANSITIVE_CLOSURE.md` | `[TYPE]` slot holds no document type | `SKILLOPT_TRANSITIVE_CLOSURE_AUDIT.md` |
| R8 | `docs/audits/THIRD_PARTY_PROVENANCE_TODO.md` | `[TYPE]` slot is `TODO`, a work-state, not a document type | `THIRD_PARTY_PROVENANCE_REGISTER.md` (proposal; the human picks the type) |
| R9 | `docs/plans/027-autonomy-posture-DRAFT.md` | numeric prefix, lowercase slug, `DRAFT` as type; `docs/plans/README.md` states no naming convention for the directory | `AUTONOMY_POSTURE_PLAN.md` (proposal) |

Propagation cost for R1-R5: the strings `topology_map`, `global_topology` and
`_contract.md` occur in 9 files outside `docs/` among `agents.md`, `rules/`,
`workflows/`, `agents/`, `scripts/`, `hooks/`, `config/` and `skills/`
(`agents/topology_mapper.md`, `rules/token_economy.md:22`,
`scripts/check_task_scope.py`, `config/model_tiers.json` and others). A rename
needs the `RA-14` grep of each term before it merges. `docs/active_state.json`
keeps a `topology_map` key (a JSON key, not a file name).

**Exempt groups, each with the convention it follows.**

| Group | Files | Convention followed |
| :--- | :--- | :--- |
| ADRs | `docs/decisions/ADR-0001-*.md` to `ADR-0024-*.md` | `ADR-NNNN-slug.md` (`docs/standards/templates/ADR_TEMPLATE.md`) |
| Roadmaps | `docs/roadmaps/core/pipeline/NNN-slug.md` | Numbered roadmap files by phase id (`000-master-blueprint.md` to `024-close-machinery-verdicts.md`, `021-030-program-queue.md`) |
| Pipeline audit reports | `docs/audits/PIPELINE_AUDIT_REPORT-NNN.md` and the `NUCLEUS_*_REPORT-045.md` / `NUCLEUS_AUDIT_SYNTHESIS-045.md` set | `[SUBJECT]_AUDIT_REPORT-NNN.md`, one report per sprint number, as `audit_workflow.md` Phase 3 names them |
| Hotfix records | `docs/hotfixes/H-NNN-[Layer].md` | `RA-03 HOTFIX_FLAT`: `docs/hotfixes/[H-ID]-[Layer].md` |
| State anchor | `docs/active_state.json` | `agents.md §5 state_anchor` (fixed path) |
| Standing names | `docs/plans/README.md`, `docs/guides/*_GUIDE.md`, `docs/standards/templates/*_TEMPLATE.{md,json}`, `docs/audits/MODEL_LEDGER.md`, `CURSOR_ERA_EXECUTION_AUDIT.md`, `UPSTREAM_FINDINGS_FROM_HOSTS.md` | Conform to `[MODULE]_[TYPE].md` (the `README.md` is the repository-wide standard name) |
| Host-only entry | `docs/0_SYSTEM_OVERVIEW.md` | `0_SYSTEM_*` documented convention (`agents.md §0`); absent from the nucleus by design |
| Sprint records | `docs/sprints/**` | Out of scope of this step |

`docs/.DS_Store` is an OS artifact, listed in `.gitignore:2`; not a document.

---

## 🛠️ Three-File Skill Standard Verification
Sprint 059 forged no skill (`skill_assignment.md`: P1 hit, every unit resolved).
The skill documents it touched (`skills/mass-standardizer/scripts/generate_manifest.py`
for unit `B-04`, `skills/token-saver-auditor/scripts/audit_plan.py`) belong to
the framework's own skills. A3 is a contradiction in how the standard's
enforcement is described, not a standard violation.

- [x] **README.md**: certified by `legacy_app_auditor.py` (`AUDIT PASSED`, exit `0`).
- [x] **SKILL.md**: procedural logic and YAML manifest verified by the same instrument; A3 flags one description that disagrees with `agents.md:86`.
- [x] **scripts/**: executable logic and `__init__.py` present where the standard requires them (executable skills only, `agents.md §3 three_file_standard`).

---

## 🛡️ Certification

### Does anything block the close?

**No finding blocks the Sprint 059 close.** Severity cutoff per
`rules/qa_and_testing.md` §4: `S0` blocks merge and deploy and `S1` is
`REJECTED`. This audit found no `S0` and no `S1`. A1, A2 and A3 are `S2`
`instructing`-class defects in text that tells an agent what a template
contains, which CLI a table was measured on, and what a skill does; by the
severity table an in-scope `S2` is "fixed in the sprint" and an out-of-scope
one takes a `KI` entry naming its destination. Both routes stay open to the
human at the close:

| Finding | In-sprint route | Out-of-sprint route |
| :--- | :--- | :--- |
| A1 | One-line edit of `rules/project_topology.md:81` | n/a, the template already holds the entries |
| A2 | Amend the two rows after a matrix re-run | `KI` entry, destination Sprint 060 |
| A3 | Decide which side is true | `KI` entry, destination Sprint 060 |

Neither route is taken by this audit. `A4` is `S3` and `RECORD`; the rename
candidates (`A5`) need the human's approval and do not gate the close.

### What makes `last_audit_sprint: 59` true

This report is the artifact `workflows/audit_workflow.md` Phase 3 `report`
requires. It records that `rule_introspection` and `nomenclature` ran against
the Sprint 059 tree at `HEAD` `6070171`, with the lead-measured instrument
results above, and that each finding carries a disposition.
`python3 scripts/session_state.py mark-audited --report docs/audits/PIPELINE_AUDIT_REPORT-059.md`
then writes `current_sprint.last_audit_sprint: 59` (Phase 3 `record_audit`).
Sprint 058 has no report of its own; `59` supersedes `57` for both.

### Limits of this audit

| Limit | Effect |
| :--- | :--- |
| No shell for this role | `git diff --stat 08c669c..HEAD` and `git cat-file -e` were not run. Every commit SHA in this report is quoted from a repository file: `6070171` from the session's git context; none is cited as a fix |
| `agents.md` size not measured | The 20000-byte cap has no instrument and was not counted here |
| `skillopt` stack absent | `precision_audit` skipped, as recorded |
| Cross-reference is by reading | The 14 subjects above are the ones the sprint changed; a coverage claim over "every rule pair" is not made (`agents.md §1 fail_closed_claims`) |

**Certified under Pipeline Methodology, nucleus mode.**
*Timestamp: 2026-11-21*
*Sealed at: `ai-sprint/059`*
