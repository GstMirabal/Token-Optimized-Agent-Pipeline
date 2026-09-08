# 🏛️ Structural Audit Report: Nucleus Rule Corpus (`agents.md` + `rules/`)

**Audit ID**: #A045-b3f1
**Auditor**: rule_validator
**Sprint**: 045 (nucleus-ruleset-mechanism-audit) · Phase 6 · Unit 1
**Mode**: NUCLEUS · Branch `ai-sprint/045`

---

## 🚦 Executive Summary

Classification of every normative unit in the always-loaded constitution (`agents.md` §0–§8, `RA-01`..`RA-18`) and the 11 on-trigger rule files under `rules/`. This sprint **classifies and drafts** amendments as proposed text inside this report; it applies nothing (`IMPLEMENTATION_PLAN.md` decision D1). No edit to `agents.md` or any `rules/*.md` is made by this unit.

> **Applied in Sprint 046** (`ai-sprint/046`): the mechanical ruleset rows —
> `S045-01` (`RA-04` tombstone), `S045-03` (`install.py` bridge), `S045-04`
> (`legacy_app_auditor.py`), `S045-05` (`§2` paths), `S045-07` (`RA-10` pointer),
> `S045-08` (`§0`/`§3` → pointers), `S045-10` (`RA-15`/`RA-16` order), `S045-11`
> (`frontend_modular_standard.md` retitle), `S045-12` (`project_topology.md`
> nucleus interpreter). `agents.md §7` IDs were **not** renumbered. The `047`
> ruleset rows (`S045-02, 06, 09`) are untouched. Evidence:
> `docs/sprints/046-core-pipeline/`.

| Metric | Score | Status |
| :--- | :--- | :--- |
| Norms classified | 38 (9 sections + 18 amendments + 11 rule files) | ✅ |
| `VIGENTE` | 22 register rows | ✅ |
| `MEJORAR` | 14 register rows (consolidate to 9 distinct cross-cutting findings — ranked below) | ⚠️ |
| `OBSOLETA` | 2 | ⚠️ |
| Corpus integrity (`scripts/verify_references.py`) | GREEN | ✅ |

`verify_references.py` is GREEN ("rules reachable, templates exist, citations resolve, every mechanism has an invoker, living file:line citations in range"): every finding below is a precision / placement / enforcement-gap defect, not a broken reference. Several defects are invisible to that script by design (bare-but-resolvable citations, semantic contradiction, intra-file duplication).

---

## 🔍 Classification Register

One row per section / amendment / rule file. Amendment cell is `—` for `VIGENTE`. Sub-key findings are named in the Evidence cell.

### `agents.md` sections

| Norm | Verdict | Evidence (command/citation) | Proposed amendment (drafted, NOT applied) |
| :--- | :--- | :--- | :--- |
| **§0 Documentation Entry Point** | MEJORAR | `Certification` row (`agents.md:16`) is near-verbatim of `RA-05` (`agents.md:154`): both say "updating Blueprints, Global Roadmap, Walkthroughs, and the Master/… Ledger before closing". Two always-loaded copies of one rule. Separately, `Hierarchy` (`agents.md:11`) and `Traceability` (`agents.md:12`) require `architecture/` + per-module Blueprint; `docs/active_state.json` `acknowledged_gaps.docs` / `.walkthroughs` (dated 2026-08-02 Phase 020, 2026-09-02 Sprint 042) formally accept their absence in the nucleus — that carve-out lives only in the anchor, not in the rule text. | In `Certification` replace the enumeration with: "See `RA-05: SPRINT_CLOSEOUT` for the closeout artifact list." Append to `Hierarchy` and `Traceability`: "Nucleus exception: `docs/active_state.json` `acknowledged_gaps` records that nucleus modules are governance prose that describe themselves; re-evaluate if the nucleus grows code modules." |
| **§1 Code, Dialect, and Style** | MEJORAR | `make verify` (`Makefile:51-92`) runs **no** `ruff check`, `pnpm run lint`, `python-doctor`, `react-doctor`, or any `max_lines_per_func` / `max_indentation` check. `grep -n 'ruff check\|python-doctor\|react-doctor\|pnpm run lint' Makefile` → 0 hits. `memory_index.json:94`: "make verify runs no ruff step". The `linter_command` and `Complexity` rows therefore have no deterministic invoker — enforcement is manual `qa_agent` judgement via the `python-quality-auditor` / `js-standardizer` skills (`config/invocation_exceptions.json:43,48`). `python-doctor` / `react-doctor` binaries are named nowhere in the tree. `path_type`, `ephemeral (TODO/FIXME)`, `code_logic` remain enforced (`scripts/check_absolute_paths.py`, `scripts/scan_workflow_determinism.py` in `verify`). | Add to `linter_command` / `Complexity` rows a `Verified by:` pointer to the QA-gate skill that measures them, and state plainly they are **not** part of `make verify` (a `code_craft.md`-style "enforced" vs "judgment" split). Rename `python-doctor` / `react-doctor` to the actual skill entrypoints or drop the tool names. |
| **§2 Autonomy, Efficiency, and Execution** | MEJORAR | `ast_skeleton` (`agents.md:64`) cites `omni_minimizer.py` bare; real path `skills/omni-context-minimizer/scripts/omni_minimizer.py` (`Glob **/omni_minimizer.py` → single hit under `skills/`). `graph_sovereignty` (`agents.md:66`) cites `graph.json` bare; root `graph.json` does not exist (`Glob graph*.json` → only `graphify-out/graph.json`), and `rules/token_economy.md:26` + `rules/graphify.md` cite the pathed form. `graph_sync` (`agents.md:69`) mandates bare `graphify update`; `rules/graphify.md:9-10` states the bare console-script "fails with `bad interpreter`" and the module form `venv_skillopt/bin/python -m graphify update .` is required. `unambiguous_action` (`agents.md:56`) forbids deictic/abbreviated targets "where a proper name exists". | `ast_skeleton`: "invoke `skills/omni-context-minimizer/scripts/omni_minimizer.py`". `graph_sovereignty`: "Query `graphify-out/graph.json`". `graph_sync`: "running `venv_skillopt/bin/python -m graphify update .` (never the bare `graphify` console-script — `rules/graphify.md`)". |
| **§3 Architecture and Topology** | MEJORAR | `federation` (`agents.md:77`): "the sanctioned bridge … is exclusively `.agents/scripts/install.sh`". `scripts/install.sh` is a 6-line wrapper: `exec python3 "…/install.py" "$@"` (`scripts/install.sh:1-6`). `README.md:60`, `docs/guides/AGENTS_SLASH_COMMANDS_GUIDE.md:16,35,138` name `install.py` the sanctioned bridge and call `install.sh` a "deprecation shim". `enforcement` (`agents.md:85`): "`mass-standardizer` … is the official auditor for this standard" — but `skill_standard_check` runs `skills/topology-monitor/scripts/legacy_app_auditor.py` (`workflows/audit_workflow.md:17`, `Makefile:69`); `mass-standardizer` only runs `generate_manifest.py` (`Makefile:70`, `workflows/skill_forge_workflow.md:21`). `secret_sovereignty` (`agents.md:86`) duplicates `RA-09` (`agents.md:158`). | `federation` / `enforcement`: "the sanctioned bridge is `.agents/scripts/install.py` (`install.sh` is a deprecation shim that forwards to it)"; "the official auditor for adherence is `skills/topology-monitor/scripts/legacy_app_auditor.py`; `mass-standardizer` regenerates `manifest_skills.json`". `secret_sovereignty`: degrade to "See `RA-09: SECRET_SOVEREIGNTY`." |
| **§4 Memory Management and Feedback Loop** | VIGENTE | `feedback_upstream` (`agents.md:99`) carries its own `RA-14` grep-guard and is cross-cited by `§3 jurisdiction` and `workflows/extract_workflow.md`; `remediation_workflow.md:19` implements `negative_ki` injection. No drift found. | — |
| **§5 Central Base (Master Index)** | MEJORAR | `discovery_manifest` (`agents.md:111`): "`install.sh` merges it non-destructively into the host's `.mcp.json`" — same stale-name defect as `§3 federation`; the merge is performed by `install.py` (`scripts/install.sh:6`). `mandatory_topology`, `state_anchor`, `state_homologation`, `historical_log`, `nucleus_neutrality`, `legacy_onboarding` verified against `docs/active_state.json` and `Makefile` — current. | `discovery_manifest`: replace `install.sh` with `install.py` (shim note as in `§3`). |
| **§6 Agent Roles & Execution Pipeline** | VIGENTE | 8 core-role one-liners match `agents/*.md` charters; `Core vs Auxiliary` NOTE and the canonical onboarding-order table (`agents.md:135-140`) resolve to real workflows (`Glob workflows/*_workflow.md`). `rule_validator` row (`agents.md:124`) is a compressed but accurate summary of `agents/rule_validator.md`. | — |
| **§7 Rule Amendments (as a section)** | MEJORAR | Row order breaks monotonic numbering: `RA-16` printed at `agents.md:164`, `RA-15` at `agents.md:165` (`grep -n 'RA-1[56]' agents.md`). `README_TEMPLATE.md:77` still describes §7 as "`RA-01`…`RA-15`". | Swap the two rows so the table reads `… RA-14, RA-15, RA-16, RA-17, RA-18`. Update `docs/standards/templates/README_TEMPLATE.md:77` range to `RA-01…RA-18`. |
| **§8 Supply Chain Security** | VIGENTE | Four rows (`agents.md:173-176`) enforced by `RA-10` scope + `.npmrc` conventions; `onlyBuiltDependencies` row is unique content not present in `RA-10`. This is the complete, canonical statement — see cross-cutting finding CC-1 on `RA-10`. | — |

### `agents.md` §7 amendments

| Norm | Verdict | Evidence (command/citation) | Proposed amendment (drafted, NOT applied) |
| :--- | :--- | :--- | :--- |
| **RA-01: ENVIRONMENT_VIOLATION** | MEJORAR | `grep -rn 'RA-01' --include='*.md'` → the only substantive definition is `agents.md:150`; every other hit is a range expression (`RA-01..RA-18`, `RA-01…RA-16`, `J-01..J-14 → RA-01..RA-14`). Zero standalone citations in `workflows/`, `rules/`, `docs/guides/AUTONOMY_POSTURE_GUIDE.md` or `workflows/remediation_workflow.md`. Text "Agent MUST attempt autonomous remediation EXCEPT if prohibited" names no prohibiting authority, no operation, no done-criterion — a `§1 unambiguous_action` breach inside the constitution itself. `remediation_workflow.md` covers Double-Gate stalemates, not environment errors, so the principle is not redundant. | Rewrite: "On an environment/tooling failure (missing venv, absent binary, broken lockfile) the agent MUST attempt one scoped autonomous fix through the isolated local environment (`§3 dependencies`) before escalating, UNLESS `rules/project_topology.md` or the Implementation Plan names that remediation as human-only. Procedure: `workflows/remediation_workflow.md` for loop stalls; `RA-03` for CRITICAL/HIGH defects." Give it an `invoked_by`-style pointer. |
| **RA-02: LAZY_SIGNAL_PARADIGM** | MEJORAR | Django-only rule inside the always-loaded constitution. `rules/django_backend_standard.md:55` is the on-trigger home and defers **back** to `agents.md §7` as "the single definition" (`:56`), so neither file is self-contained. `grep -n 'RA-02' rules/django_backend_standard.md` → `:22,:55`. | Move the operative text ("local imports inside the receiver; lazy sender strings") into `rules/django_backend_standard.md §2` as the definition; degrade the `agents.md §7` row to "See `rules/django_backend_standard.md §2 Signal Registration`." Keeps the `RA-02` anchor resolvable for legacy `Clause J-02` citations via `LEGACY_RULE_CONCORDANCE.md`. |
| **RA-03: HOTFIX_FLAT** | VIGENTE | `grep -rn 'RA-03' --include='*.md' \| grep -v agents.md \| wc -l` → 18. Fully specified (branch name, doc path, commit suffix, id successor rule) and enforced by `hooks/on_commit.py`. | — |
| **RA-04: FULL_DEPLOYMENT** | OBSOLETA | `grep -rn 'RA-04' .` → single hit `agents.md:153`. Zero citations anywhere in 44 sprints. "Orchestrator MUST deploy the COMPLETE task hierarchy in a single atomic action" contradicts the `§6` `orchestrator` charter (`agents.md:121`: "Roadmap Author. Drafts Initial Roadmap and instantiates Sprint Hierarchy" — not a deployer). `grep -n 'orchestrator\|hierarchy\|atomic' workflows/deployment_workflow.md` → no matches; deployment/merge is owned by `RA-12` + `deployment_workflow.md` Phase 1. Title "FULL_DEPLOYMENT" vs body "task hierarchy" is itself ambiguous (`§1 unambiguous_action`). | **Retire the row.** If the intent (sprint-hierarchy scaffolding must be one atomic action) is still wanted, fold one sentence into the `§6` `orchestrator` charter and cite `skills/sprint-architect/`. Renumbering of RA-05..RA-18 is NOT proposed (would break 100+ external citations); leave `RA-04` as a tombstone row: "Retired Sprint 045 — superseded by `§6 orchestrator` + `RA-12`." |
| **RA-05: SPRINT_CLOSEOUT** | MEJORAR | Near-verbatim duplicate of `§0 Certification` (`agents.md:16` vs `:154`). `grep -rn 'RA-05' --include='*.md' \| grep -v agents.md \| wc -l` → 5, all pointing at the closeout artifact list. | Keep `RA-05` as the single definition; degrade `§0 Certification` to a pointer (see `§0` row). No change to `RA-05` text itself beyond confirming it is authoritative. |
| **RA-06: IDENTITY_NAMING** | VIGENTE | Cited by `rules/documentation_standard.md:17`, `:50` and the reason `rules/frontend_modular_standard.md` is flagged below. Option B naming is live. | — |
| **RA-07: ARCHIVE_PURGE** | VIGENTE | `grep -rn 'RA-07' --include='*.md' \| grep -v agents.md` → 2 hits; niche but unambiguous and self-enforcing on sight. | — |
| **RA-08: COMMIT_SQUASH** | VIGENTE | Highest external usage: 35 citations. Enforced in `close_workflow.md` Phase 5. | — |
| **RA-09: SECRET_SOVEREIGNTY** | MEJORAR | Duplicates `§3 secret_sovereignty` (`agents.md:86`) and overlaps `RA-15` precedent. `LEGACY_RULE_CONCORDANCE.md:18` maps `Rule 66` to "`§3 secret_sovereignty` + `RA-09`" — two authorities for one rule. `rules/qa_and_testing.md §5` is the operative waiver procedure and cites `RA-09`. | Keep `RA-09` as the single §7 statement (it adds the `Makefile` / subshell mechanism `§3` lacks); degrade `§3 secret_sovereignty` to "See `RA-09`." |
| **RA-10: SUPPLY_CHAIN_SHIELD** | OBSOLETA | `agents.md:159` is a strict **subset** of `§8` (`agents.md:173-176`): `§8` states the same `pnpm 11+` / `ignore-scripts=true` / `minimum-release-age=1440` plus `onlyBuiltDependencies`. Two always-loaded copies, `§8` the superset. `grep -rn 'RA-10' --include='*.md' \| grep -v agents.md \| wc -l` → 3. | Degrade the row to a pointer: "`RA-10: SUPPLY_CHAIN_SHIELD` — see `§8 Supply Chain Security` (canonical)." Keeps the 3 external `RA-10` citations resolvable. |
| **RA-11: HOOK_BLOCKING_SEMANTICS** | VIGENTE | Cited 6×; concrete (`sys.exit(2)` vs `1`), verifiable against `hooks/`. | — |
| **RA-12: BRANCH_DISCIPLINE** | VIGENTE | Cited 6× + `§6` pipeline prose (`agents.md:144`). Enforced by `close_workflow.md` Phase 5. | — |
| **RA-13: SEQUENTIAL_GATES** | VIGENTE | Cited 8× in `workflows/`, restated-with-citation in `rules/loop_governance.md §4` and `rules/code_craft.md §6`. Correct pointer pattern. | — |
| **RA-14: PATCH_PROPAGATION** | VIGENTE | Cited 5×; is the method this audit's cross-cutting table applies. | — |
| **RA-15: HOST_CONTENT_GENERICIZATION** | VIGENTE | Cited 2× + `§3 topological_order` + `§4 feedback_upstream`. Content current (Sprint 028 `--profile-path`). Only defect is print position — see `§7` row. | — |
| **RA-16: INVOCATION_COVERAGE** | MEJORAR | Content is `VIGENTE` and enforced by `scripts/verify_references.py` check (d). Defect is placement only: printed at `agents.md:164`, before `RA-15` at `:165`. | Move the row to follow `RA-15` (numeric order). No text change. |
| **RA-17: GATE_VERDICT_CLASSES** | VIGENTE | Procedure lives in `rules/qa_and_testing.md §4` (operational table verified at `:58-63`); `RA-17` row correctly defers there. | — |
| **RA-18: CURSOR_PHASE1_NO_PLAN_MODE** | VIGENTE | Cited 3×; recent (Sprint 026 era catalogue), tool-specific, procedure in `pipeline_workflow.md` Phase 1. | — |

### `rules/` files

| Norm | Verdict | Evidence (command/citation) | Proposed amendment (drafted, NOT applied) |
| :--- | :--- | :--- | :--- |
| **`rules/code_craft.md`** | VIGENTE | §§1-5 exempt from Filter 5 (recorded `:7`), §§6-7 enforced by `hooks/on_commit.py` (`:76`, `:80`). Cross-refs to `RA-13`, `qa_and_testing.md §2`, `agents.md §8` all resolve. | — |
| **`rules/loop_governance.md`** | VIGENTE | Stop-set enforced by `scripts/loop_guard.py` (`:20,:29`); §3 correctly defers verify to `qa_and_testing.md §4` and state to `active_state.json`. `§2` self-corrects an obsolete justification per `RA-14`. | — |
| **`rules/token_economy.md`** | MEJORAR | §1 rung 2 cites `omni_minimizer.py <file>` bare (`:11`) — same buried-`skills/` path as `agents.md §2` (cross-cutting CC-4). `rules/graphify.md:17` records this file is "silently skipped" by the graph extractor (coverage anomaly under watch — not a rule defect, but worth a one-line note so a future auditor does not read "absent from graph" as "orphaned"). Rule content itself (Decision Ladder, session bound §3.1, tool-result economics §4) is current and evidence-backed. | §1 rung 2: `skills/omni-context-minimizer/scripts/omni_minimizer.py <file>`. Optional: footnote the graphify skip with a pointer to `rules/graphify.md:17`. |
| **`rules/qa_and_testing.md`** | VIGENTE | Citation convention (`:5`), Coverage Mandate, Three-Strikes, Double-Gate table (`:58-63` = `RA-17` procedure), secret-scan waiver (`:68-88` = `RA-09` procedure) all current and enforced by `hooks/on_commit.py` / `remediation_workflow.md`. | — |
| **`rules/project_topology.md`** | MEJORAR | §1 mandates `./venv/bin/python` and `./node_modules/.bin/npx` as the interpreter examples; the framework's own interpreter is `venv_skillopt/bin/python` (`Makefile:23`, `rules/graphify.md:10`) — the rule's examples do not match the nucleus topology, and a nucleus session applying `§1` literally looks for a non-existent `./venv/`. `./.docker-db-data`, `./data/output/` are host conventions with no nucleus referent. Low blast radius (host-facing rule, `frontend/`/DB triggers never fire in the nucleus). | Add a line: "Nucleus interpreter is `venv_skillopt/bin/python` (`Makefile`); the `./venv/` form is the host-project convention." Mark the DB/ETL sections `host-only`. |
| **`rules/skills_and_integrations.md`** | VIGENTE | `skills/manifest_skills.json` (`Makefile:70-71`), `skills/autoskills-3rd/`, `-3rd` suffix mandate, Priority 4 → `skill_forge_workflow.md forge_destination` all resolve. Skill Documentation Veto (§3) is the reason `RA-16` routes skills through `config/invocation_exceptions.json`. | — |
| **`rules/frontend_modular_standard.md`** | MEJORAR | H1 is `# 🛡️ Rule 041: Frontend Modular Standard` (`:1`); subsections `(Rule 41.1)` / `(Rule 41.2)` / `(Rule 41.3)` (`:3,:12,:16`). `LEGACY_RULE_CONCORDANCE.md:27`: "numbered citations are legacy-only and frozen to this table"; `RA-06` mandates keyed naming. Sibling `rules/django_backend_standard.md:1` uses `# Rule Context: Django Backend Standard` and `:17-22` explicitly says this file is the frontend counterpart "named to match" — but the titles do not match. Footer `*Status: ACTIVE*` / `*Effective since: 2026-05-07*` (`:20-22`) is not the `documentation_standard.md §4.1` bold-key metadata block. | Retitle to `# Rule Context: Frontend Modular Standard`; rename subsections to `## 1. Directory Anatomy` etc. (drop `(Rule 41.x)`); add the intro sentence + trigger line the other `rules/` files carry; replace the footer with the `§4.1` metadata block. Keep the `Rule 41 / 041 / 41.x` row in `LEGACY_RULE_CONCORDANCE.md:15` so historical citations still resolve. |
| **`rules/django_backend_standard.md`** | VIGENTE | Placement rationale recorded in-file (`:5-46`) with the measurement that the vendored 247-line skill has zero signal-registration guidance. §2 defers to `RA-02` (see `RA-02` row for the circular-definition fix, which lands here). | — |
| **`rules/graphify.md`** | VIGENTE | Invocation form (`-m graphify`, not the console-script) is correct and matches `Makefile:40`; documents the `bad interpreter` failure mode and known coverage gaps. This file is the correct pathed-citation model that `agents.md §2` should follow. | — |
| **`rules/documentation_standard.md`** | VIGENTE | Diátaxis / C4 / ADR / Freshness-Gate all map to real instruments: `scripts/docs_freshness_check.py` (`Makefile:100-101`), `styles/Diataxis/Explanation.yml`, `graph_stats.json` snapshots (`Glob` → 21 files under `docs/sprints/*/`). `§6` T5 obligations enforced at Phase 1. | — |
| **`rules/LEGACY_RULE_CONCORDANCE.md`** | VIGENTE | Every legacy number maps to a live keyed authority; CI (`scripts/verify_references.py`) fails on any unmapped `Rule NN`. `Rule 40 / 40.x` correctly recorded as removed (`RA-15`). | — |

---

## 🔀 Cross-Cutting Findings

Overlaps where the same normative content is stated in two always-loaded places, and internal contradictions.

| # | Type | Locations | Detail | Resolution class |
| :--- | :--- | :--- | :--- | :--- |
| **CC-1** | Constitution duplicates itself | `RA-10` (`agents.md:159`) ⊂ `§8` (`:173-176`) | `§8` is a strict superset (adds `onlyBuiltDependencies`). Two always-loaded statements of `pnpm 11+` / `ignore-scripts` / `minimum-release-age`. | `RA-10` → pointer to `§8`. |
| **CC-2** | Constitution duplicates itself | `RA-05` (`agents.md:154`) ≡ `§0 Certification` (`:16`) | Same closeout artifact list, verbatim. | `§0 Certification` → pointer to `RA-05`. |
| **CC-3** | Constitution duplicates itself | `RA-09` (`agents.md:158`) ≡ `§3 secret_sovereignty` (`:86`); `LEGACY_RULE_CONCORDANCE.md:18` names both as authority for `Rule 66` | Same `.env`-not-in-memory rule; `RA-09` uniquely adds the `Makefile`/subshell mechanism. | `§3 secret_sovereignty` → pointer to `RA-09`. |
| **CC-4** | Stale tool name across files | `federation` `agents.md:77`, `discovery_manifest` `agents.md:111` say "exclusively `install.sh`"; `scripts/install.sh:1-6` is `exec python3 install.py`; `README.md:60`, `AGENTS_SLASH_COMMANDS_GUIDE.md:16,35,138` say `install.py` is sanctioned, `install.sh` is a "deprecation shim" | The always-loaded constitution names a deprecated shim as the sole sanctioned mechanism. | Both `agents.md` rows → `install.py` (shim note). |
| **CC-5** | Wrong enforcement tool named | `§3 enforcement` (`agents.md:85`) names `mass-standardizer`; `audit_workflow.md:17` + `Makefile:69` run `skills/topology-monitor/scripts/legacy_app_auditor.py` for `skill_standard_check`; `mass-standardizer` runs only `generate_manifest.py` (`Makefile:70`) | Three-File-Standard adherence is audited by `topology-monitor`, not `mass-standardizer`. | `§3 enforcement` → name `legacy_app_auditor.py`; keep `mass-standardizer` as the manifest generator. |
| **CC-6** | Bare citation of buried script | `omni_minimizer.py` bare in `agents.md:64`, `rules/token_economy.md:11`, `workflows/pipeline_workflow.md:37`; real path `skills/omni-context-minimizer/scripts/omni_minimizer.py` | `rules/qa_and_testing.md:5` permits bare citation only for `workflows/ rules/ agents/ commands/` or repo root — not `skills/`. `verify_references.py` does not catch it (filename resolves). | Path all three call sites. |
| **CC-7** | Bare citation, target absent | `graph_sovereignty` `agents.md:66` cites `graph.json`; root file does not exist (`Glob graph*.json` → only `graphify-out/graph.json`); `rules/token_economy.md:26`, `rules/graphify.md` use the pathed form | `agents.md` is the one place the path is wrong. | `agents.md:66` → `graphify-out/graph.json`. |
| **CC-8** | Circular definition | `RA-02` (`agents.md:151`) ↔ `rules/django_backend_standard.md:55-56` | The rule file calls `agents.md §7` "the single definition"; `agents.md §7` is a one-line summary. Neither is self-contained; a reader loading only one gets a stub. | Move operative text into `rules/django_backend_standard.md §2`; `RA-02` → pointer. |
| **CC-9** | Contradiction | `RA-04` (`agents.md:153`) vs `§6 orchestrator` (`agents.md:121`) vs `RA-12` / `deployment_workflow.md` Phase 1 | `orchestrator` is a roadmap author, not a deployer; merge/deploy authority is `RA-12` + `deployment_workflow.md`. `RA-04` has 0 citations and no implementing workflow (`grep -n atomic workflows/deployment_workflow.md` → none). | Retire `RA-04` (tombstone row, no renumber). |
| **CC-10** | Enforcement gap | `§1 linter_command` + `§1 Complexity` vs `Makefile:51-92` | `make verify` runs no `ruff` / `pnpm lint` / `*-doctor` / line-length / indent check (`memory_index.json:94` confirms). Rules rely entirely on manual `qa_agent` judgement; `python-doctor`/`react-doctor` tool names resolve to nothing on disk. | Add `Verified by:` skill pointers; state the split between `make verify` (deterministic) and QA-gate judgement. |
| **CC-11** | Numbering / print-order | `RA-16` at `agents.md:164` precedes `RA-15` at `:165`; `README_TEMPLATE.md:77` still says "`RA-01`…`RA-15`" | Cosmetic but violates the monotonic-numbering expectation the corpus relies on for `RA-NN` lookup. | Swap rows; bump template range to `RA-18`. |

---

## 🏆 Impact Ranking (OBSOLETA + MEJORAR)

Ranked: always-loaded constitution defects outrank on-trigger `rules/` defects; within each, breadth of reader impact.

### OBSOLETA (2)

| Rank | Norm | Why it outranks | Action |
| :--- | :--- | :--- | :--- |
| 1 | **RA-04: FULL_DEPLOYMENT** | Always-loaded; actively **contradicts** the `§6 orchestrator` charter, so a reader can be misled, not merely under-informed. 0 citations, 0 implementing workflow. | Retire to a tombstone row (no renumber of RA-05..RA-18). |
| 2 | **RA-10: SUPPLY_CHAIN_SHIELD** | Always-loaded; harmless but redundant — a strict subset of `§8` two rows below it. | Degrade to a one-line pointer to `§8`. |

### MEJORAR — top 5 (of 9 distinct findings; 14 register rows)

| Rank | Norm | Core defect | Fix |
| :--- | :--- | :--- | :--- |
| 1 | **§1 (linter_command + Complexity)** / CC-10 | Always-loaded rules with **no deterministic enforcer**; two named tools (`python-doctor`, `react-doctor`) exist nowhere on disk. Every code sprint's "standards" gate is unscripted judgement. | Add `Verified by:` skill pointers; declare the `make verify` vs QA-judgement split explicitly. |
| 2 | **§3 federation / §5 discovery_manifest** (CC-4) | Always-loaded; name the **deprecated** `install.sh` shim as the *exclusive* sanctioned bridge, diverging from `README.md` + all guides which name `install.py`. | Replace `install.sh` → `install.py` in both rows, note the shim. |
| 3 | **§3 enforcement** (CC-5) | Always-loaded; names the wrong tool (`mass-standardizer`) as the Three-File-Standard auditor; the real auditor is `skills/topology-monitor/scripts/legacy_app_auditor.py`. | Correct the tool name; keep `mass-standardizer` scoped to manifest generation. |
| 4 | **§2 (ast_skeleton / graph_sovereignty / graph_sync)** (CC-6, CC-7) | Always-loaded; three deictic/bare or wrong paths (`omni_minimizer.py`, `graph.json`, bare `graphify update`), one pointing at a file that does not exist — a `§1 unambiguous_action` breach in the constitution. | Path all three; use the `-m graphify` module form. |
| 5 | **§0 Certification ≡ RA-05, §3 secret_sovereignty ≡ RA-09, RA-02 circular** (CC-2, CC-3, CC-8) | Always-loaded self-duplication: three rules each stated twice, one pair (`RA-02`) circular so neither copy is complete. | Pick the canonical statement in each pair; degrade the other to a pointer. |

Remaining MEJORAR (findings 6-9): **RA-16 print-order** (CC-11, cosmetic), **rules/frontend_modular_standard.md** legacy `Rule 041` nomenclature (on-trigger, `frontend/` only), **rules/token_economy.md** bare `omni_minimizer.py` (on-trigger), **rules/project_topology.md** `./venv/` example mismatch (on-trigger, host-facing).

*Register-row vs distinct-finding count: the 14 register rows verdicted `MEJORAR` collapse to these 9 cross-cutting findings — the self-duplication finding (CC-2/CC-3/CC-8) marks both halves of each pair (§0 + RA-05, §3 + RA-09, RA-02 + its rule row), and the §2 path finding (CC-6/CC-7) marks three rows. `NUCLEUS_AUDIT_SYNTHESIS-045.md` §3 carries the same reconciliation.*

---

## 🛠️ Three-File Skill Standard Verification

Not applicable — this audit unit produces one Markdown report and ships no `scripts/` folder.

- [n/a] **README.md**
- [n/a] **SKILL.md**
- [n/a] **scripts/**

---

## 🛡️ Certification

**Certified by the Rule Validator under Pipeline Methodology v4.0 (Sprint 045, Phase 6, Unit 1).**
Scope: `agents.md` §0–§8 + `RA-01`..`RA-18` + all 11 `rules/*.md`. Classification and drafted amendments only — **nothing applied** (`IMPLEMENTATION_PLAN.md` D1).
*Timestamp: 2026-09-07*
*Signature ID: A045-b3f1-rule_validator*
