# Task Scope — Sprint 058 (core-pipeline)

Source: `docs/sprints/058-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`, `## Design`, `## Tests`, `## Verification`, `## Abort criterion`).
Staffing authority: `agent_assignment.md` (its only overwrite, D-08, no longer applies: the plan deleted that row). Tools: `skill_assignment.md`.
Phase 4.3 of `workflows/pipeline_workflow.md`. Enforced by `scripts/check_task_scope.py`.
Mode: `claude-code`, `delegation_mode: native`. Sprint id 58 >= `MODEL_FROM_SPRINT` (28), so Model and Effort are required. No template for this artifact exists under `docs/standards/templates/`; the shape comes from `scripts/check_task_scope.py` (`WORK_KEYS`) and the accepted `docs/sprints/057-core-pipeline/task_scope.md` table.

## Tier transcription

Model and Effort are transcribed from each assignee's `agents/<role>.md` frontmatter (`model:`, `tier:`) and the `claude_code` column of `config/model_tiers.json` (`tiers.author.claude_code` = `sonnet` / `medium`). No tier is invented and no dated model ID is written. `session_tool` is `claude-code`, so `make cursor-tiers` does not apply.

| Assignee | `model:` | `tier:` | Effort (`claude_code` column) |
| :--- | :--- | :--- | :--- |
| `doc_orchestrator` | sonnet | author | medium |
| `rule_validator` | sonnet | author | medium |
| `implementer_agent` | sonnet | author | medium |
| `skill_architect` | sonnet | author | medium |
| `agent_orchestrator` | sonnet | author | medium |
| `devops_agent` (runs the D-02 measurements (a)-(c); owns no row) | haiku | mechanical | low |

Declared escalations: none. No row is assigned to a `mechanical` profile, so the mechanical-at-high-risk check does not apply. High-risk rows stay on the `author` tier: the adversarial check on them is the Phase 7 gate (`tier: gate`, opus/high), not the author.

## Work

Status values: ⏳ pending. Risk `high` touches a gate, the CI workflow, the sandbox template, `merge_json.py`, `session_state.py` or `agents.md`. Execution order is the plan's: Wave A, Wave C, Wave B, Wave D (C-01 before B-05). The table holds 48 units (A 17, C 9, B 15, D 7; D-08 was deleted from the plan). Wave D rows D-03..D-07 run only on the "yes" branch of plan D7 (D-02 decides).

### Wave A — upstream channel (D1-D4)

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| A-01 | `docs/standards/templates/UPSTREAM_OUTBOX_TEMPLATE.json` | create (D1 schema, one genericized example entry) | low | `doc_orchestrator` | sonnet | medium | ⏳ |
| A-02 | `scripts/upstream_outbox.py` | create (subcommands `check`, `check-issue`, `export`, `aged`, `deltas`; paired test `tests/test_upstream_outbox.py`) | high | `implementer_agent` | sonnet | medium | ⏳ |
| A-03 | `config/upstream_intake.json` | create (`min_pin`, `aged_after_sprints`, `rate_limit_per_day`, security words) | low | `implementer_agent` | sonnet | medium | ⏳ |
| A-04 | `scripts/upstream_intake.py` | create (channel A reader, structured fields only; paired test `tests/test_upstream_intake.py`) | high | `implementer_agent` | sonnet | medium | ⏳ |
| A-05 | `.gitignore` | modify (ignore `.upstream_hosts.json`) | low | `implementer_agent` | sonnet | medium | ⏳ |
| A-06 | `scripts/session_start.py` | modify (`section_upstream` adds the intake queue; paired test `tests/test_session_start.py`) | medium | `implementer_agent` | sonnet | medium | ⏳ |
| A-07 | `.github/ISSUE_TEMPLATE/host-finding.yml` | create (Issue Form mirroring the schema, channel B) | low | `implementer_agent` | sonnet | medium | ⏳ |
| A-08 | `.github/workflows/host-finding-intake.yml` | create (D3 filter, actions pinned by commit SHA, issue body through an environment variable) | high | `implementer_agent` | sonnet | medium | ⏳ |
| A-09 | `scripts/sync_agents_pin.py` | modify (print `Ships host findings: <ids>`; paired test `tests/test_sync_agents_pin.py`) | medium | `implementer_agent` | sonnet | medium | ⏳ |
| A-10 | `docs/standards/templates/CHANGELOG_TEMPLATE.md` | modify (`host:<id>` citation) | low | `doc_orchestrator` | sonnet | medium | ⏳ |
| A-11 | `agents.md` | modify (`§4 feedback_upstream` and the `§3 jurisdiction` restatement it names) | high | `rule_validator` | sonnet | medium | ⏳ |
| A-12 | `workflows/extract_workflow.md` | modify (`upstream_feedback` writes an outbox entry, runs `upstream_outbox.py check`) | medium | `doc_orchestrator` | sonnet | medium | ⏳ |
| A-13 | `workflows/pipeline_workflow.md` | modify (Phase 1 mandatory intake triage) | medium | `doc_orchestrator` | sonnet | medium | ⏳ |
| A-14 | `workflows/close_workflow.md` | modify (host close runs `upstream_outbox.py aged` and `deltas`, advisory) | medium | `doc_orchestrator` | sonnet | medium | ⏳ |
| A-15 | `docs/guides/SELF_IMPROVEMENT_GUIDE.md` | modify (host guide: outbox, channels, delta discipline) | low | `doc_orchestrator` | sonnet | medium | ⏳ |
| A-16 | `SECURITY.md` | modify (channel C) | low | `doc_orchestrator` | sonnet | medium | ⏳ |
| A-17 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify (record host H1 report, genericized, with 2026-10-22 verdicts) | medium | `doc_orchestrator` | sonnet | medium | ⏳ |

### Wave C — Known Issues of Sprint 057 (D6)

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| C-01 | `scripts/_md_table.py` | create (`split_cells()` honouring `\|`; paired test `tests/test_md_table.py`) | low | `implementer_agent` | sonnet | medium | ⏳ |
| C-02 | `scripts/check_task_scope.py` | refactor (`_cells` imports `_md_table.split_cells`; `tests/test_check_task_scope.py` unchanged and green) | low | `implementer_agent` | sonnet | medium | ⏳ |
| C-03 | `scripts/check_gate_log.py` | modify (fix `KI-057-3`; paired test `tests/test_check_gate_log.py`) | low | `implementer_agent` | sonnet | medium | ⏳ |
| C-04 | `scripts/check_forge_ladder.py` | modify (fix `KI-057-3`; paired test `tests/test_check_forge_ladder.py`) | low | `implementer_agent` | sonnet | medium | ⏳ |
| C-05 | `scripts/detect_new_models.py` | modify (fix `KI-057-3`; new paired test `tests/test_detect_new_models.py`) | low | `implementer_agent` | sonnet | medium | ⏳ |
| C-06 | `claude/settings.hooks.json` | modify (`KI-057-4`: remove the `SubagentStop` entry of `check_role_artifact.py --from-hook`; test `tests/test_template_sandbox.py`) | medium | `implementer_agent` | sonnet | medium | ⏳ |
| C-07 | `scripts/merge_json.py` | modify (`KI-057-4`: prune the retired hook entry from hosts; test `tests/test_merge_json.py`) | high | `implementer_agent` | sonnet | medium | ⏳ |
| C-08 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify (`KI-057-4`: `F-107-N1` closing text cites C-06 and C-07) | low | `doc_orchestrator` | sonnet | medium | ⏳ |
| C-09 | `scripts/session_state.py` | modify (fix `KI-057-6`: every commit of `last_close_commit..tip` is hotfix work; paired test `tests/test_session_state.py`) | high | `implementer_agent` | sonnet | medium | ⏳ |

### Wave B — reproduce-first rules (D5)

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| B-01 | `rules/qa_and_testing.md` | modify (§4: R-4, R-5, A-1) | high | `rule_validator` | sonnet | medium | ⏳ |
| B-02 | `rules/code_craft.md` | modify (§6: R-8 and the vitest runner row) | medium | `rule_validator` | sonnet | medium | ⏳ |
| B-03 | `docs/standards/templates/SPRINT_LOG_TEMPLATE.md` | modify (`Remediation notes`, `Abort criteria`, `Plan results` tables) | low | `doc_orchestrator` | sonnet | medium | ⏳ |
| B-04 | `scripts/check_gate_log.py` | modify (R-4: round >= 2 row without remediation note exits 2; paired test `tests/test_check_gate_log.py`) | medium | `implementer_agent` | sonnet | medium | ⏳ |
| B-05 | `scripts/check_remediation_chain.py` | create (A-1; paired test `tests/test_check_remediation_chain.py`) | medium | `implementer_agent` | sonnet | medium | ⏳ |
| B-06 | `hooks/on_commit.py` | modify (A-1: call `check_remediation_chain.py` on a `fix(` commit, warning, exit 0; paired test `tests/test_on_commit.py`) | medium | `implementer_agent` | sonnet | medium | ⏳ |
| B-07 | `config/blast_radius.json` | create (R-5: shared-module globs and `full_suite_command`) | low | `implementer_agent` | sonnet | medium | ⏳ |
| B-08 | `skills/token-saver-auditor/scripts/audit_plan.py` | modify (C-6: read `config/blast_radius.json` or host override; companion test `tests/test_token_saver_auditor.py`, not a second subject) | medium | `skill_architect` | sonnet | medium | ⏳ |
| B-09 | `scripts/check_plan_closure.py` | create (R-9, R-10; paired test `tests/test_check_plan_closure.py`) | medium | `implementer_agent` | sonnet | medium | ⏳ |
| B-10 | `workflows/close_workflow.md` | modify (Phase 2.6 runs `check_plan_closure.py`) | low | `doc_orchestrator` | sonnet | medium | ⏳ |
| B-11 | `workflows/pipeline_workflow.md` | modify (R-9/A-2 abort-criteria measurement per phase boundary; Phase 7 R-4 and `check_remediation_chain.py` second check) | medium | `doc_orchestrator` | sonnet | medium | ⏳ |
| B-12 | `agents/qa_agent.md` | modify (existing profile; Gate 1 second check `check_remediation_chain.py`) | low | `agent_orchestrator` | sonnet | medium | ⏳ |
| B-13 | `scripts/check_fix_reproduces.py` | modify (R-6 / `KI-054-1`: vitest runner; paired test `tests/test_check_fix_reproduces.py` with a simulated runner) | high | `implementer_agent` | sonnet | medium | ⏳ |
| B-14 | `scripts/check_fix_reproduces.py` | modify (R-8: `SOURCE_TEXT` warning with the five D5 patterns; paired test `tests/test_check_fix_reproduces.py`) | medium | `implementer_agent` | sonnet | medium | ⏳ |
| B-15 | `agents.md` | modify (`§0` row "Command paths", A-3 / `KI-054-2`) | medium | `rule_validator` | sonnet | medium | ⏳ |

### Wave D — Dependabot (D7)

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| D-01 | `requirements-skillopt.txt` | modify (`claude-agent-sdk` to latest; `Dependency:` trailer) | low | `implementer_agent` | sonnet | medium | ⏳ |
| D-02 | `docs/sprints/058-core-pipeline/GRAPHIFY_09_MEASUREMENT.md` | create (measurements (a)-(c), literal output per case; `devops_agent` runs them with `Bash` and hands the output over unaltered) | medium | `doc_orchestrator` | sonnet | medium | ⏳ |
| D-03 | `requirements-core.txt` | modify ("yes" branch: `graphifyy` to latest `0.9.x`; `Dependency:` trailer) | high | `implementer_agent` | sonnet | medium | ⏳ |
| D-04 | `Makefile` | modify ("yes" branch: graphify targets and the comment at `:52`) | medium | `implementer_agent` | sonnet | medium | ⏳ |
| D-05 | `rules/graphify.md` | modify ("yes" branch: version and variables read, `:18`, `:32`) | low | `rule_validator` | sonnet | medium | ⏳ |
| D-06 | `rules/project_topology.md` | modify ("yes" branch: `:37`) | low | `rule_validator` | sonnet | medium | ⏳ |
| D-07 | `config/with_env_allowlist.json` | modify ("yes" branch: `reason` names the measured variables) | medium | `implementer_agent` | sonnet | medium | ⏳ |

## Rule audit

### 1. `jurisdictional_lock` and `no_interference`

Every row names exactly one structural subject. Paired tests are mandatory companions (`jurisdictional_lock`, Sprint 048 restatement), not second subjects. Rows are staffed `sequential` in `agent_assignment.md`; no two rows run concurrently. Shared subjects and the order that resolves them:

| Subject | Rows, in execution order | Rule |
| :--- | :--- | :--- |
| `agents.md` | A-11 (Wave A) then B-15 (Wave B) | B-15 starts only after A-11 is committed |
| `workflows/pipeline_workflow.md` | A-13 then B-11 | B-11 starts only after A-13 is committed |
| `workflows/close_workflow.md` | A-14 then B-10 | B-10 starts only after A-14 is committed |
| `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | A-17 then C-08 | C-08 starts only after A-17 is committed (Wave A precedes Wave C) |
| `scripts/check_gate_log.py` and `tests/test_check_gate_log.py` | C-03 then B-04 | B-04 starts only after C-03 is committed (Wave C precedes Wave B) |
| `scripts/check_fix_reproduces.py` and `tests/test_check_fix_reproduces.py` | B-13 then B-14 | B-14 starts only after B-13 is committed or closed under abort criterion 3 |
| `scripts/session_state.py`, `scripts/merge_json.py`, `claude/settings.hooks.json` | single rows C-09, C-07, C-06 | no collision; abort criterion 4 applies to the last two |

Dependency order that is not a shared subject: C-01 before C-02 and before B-05; A-02 before A-08, A-12 and A-14; A-04 before A-06; A-01 before A-02 (the `check` target file); B-04 before B-11 and B-12 reference a finished instrument; B-05 before B-06, B-11 and B-12; B-07 before B-08; B-09 before B-10; D-02 before D-03..D-07.

### 2. Unsatisfiable plan rows (`rules/qa_and_testing.md §4`, `F-114-N7`)

Each Tests and Verification row was read against the deliverables that the same plan requires.

| Row | Result |
| :--- | :--- |
| Verification `rg -n 'split\("\x7c"\)' scripts/` expects no output | Satisfiable. C-01's model, `check_task_scope._cells`, uses `re.split(r"(?<!\\)\|", ...)` (`scripts/check_task_scope.py:117`), which the pattern does not match |
| Verification `rg -n -F 'check_role_artifact.py --from-hook' claude/settings.hooks.json` expects no output | Satisfiable. The string sits only at `claude/settings.hooks.json:129`; no deliverable must re-introduce it into that file |
| Verification `rg -n '\$\{\{ *github\.event\.issue' .github/workflows/` expects no output | Satisfiable only if A-08 and `ci.yml` carry no such text, including inside a YAML comment (finding F-2) |
| Verification `make verify` expects exit 0 | Satisfiable only after two generated artifacts are refreshed that no Work row owns (finding F-1) |
| Verification `check_remediation_chain.py --range f0b11f8..HEAD` expects exit 0 | Contingent (finding F-3) |
| Verification `audit_plan.py <plan>` expects exit 0 | Contingent on B-07 (finding F-4) |
| Tests `rg -q -F "pytest replays .py only"` and `split` rows | Mixed polarity (finding F-5); not contradictions |
| Other Tests rows (`test -f`, `rg -q`) | Each deliverable creates exactly the file or text the row checks. No contradiction |

No row is unsatisfiable on its face, so no `instructing` finding blocks Phase 5. F-1 is `instructing` because it leaves two changed files without a unit.

### 3. `fix(` units and `RA-16` invokers

| Unit | Paired test (named in the row) |
| :--- | :--- |
| C-03 | `tests/test_check_gate_log.py` |
| C-04 | `tests/test_check_forge_ladder.py` |
| C-05 | `tests/test_detect_new_models.py` (new) |
| C-09 | `tests/test_session_state.py` |

C-06 and C-07 (`KI-057-4`) also name tests (`tests/test_template_sandbox.py`, `tests/test_merge_json.py`) in case their commit type is `fix(`. `rules/code_craft.md §6` and `hooks/on_commit.py audit_regression_test` apply; the `Repro: manual` route is not used.

| New script | `RA-16` invoker (from plan `## Mechanisms`) |
| :--- | :--- |
| `scripts/upstream_outbox.py` | `workflows/extract_workflow.md` `upstream_feedback` (A-12), `workflows/close_workflow.md` (A-14), the Action (A-08) |
| `scripts/upstream_intake.py` | `scripts/session_start.py --boot` (A-06) |
| `scripts/check_remediation_chain.py` | `hooks/on_commit.py` (B-06) and QA Gate 1 (B-11, B-12) |
| `scripts/check_plan_closure.py` | `workflows/close_workflow.md` Phase 2.6 (B-10) |
| `scripts/_md_table.py` | imported by `scripts/check_task_scope.py` (C-02), then by C-03..C-05; the Mechanisms table does not list it (finding F-6) |
| `config/upstream_intake.json`, `config/blast_radius.json` | read by `upstream_intake.py` / `upstream_outbox.py` and `audit_plan.py`; each script must carry an `invoked_by:` docstring |

### 4. `agents.md §1 fail_closed_claims`

| Design item | Result |
| :--- | :--- |
| D1 genericization scan | Compliant. The plan states "denylist de patrones", names exactly three families (POSIX and Windows absolute paths, email addresses, token prefixes of the repository's secret scanner), says it "no hace afirmacion de cobertura", and assigns the real control to `genericized: true`. Abort criterion 1 matches the rule: after a second same-family rejection the claim is narrowed, no pattern is added |
| D5 R-8 `SOURCE_TEXT` | Compliant. Names exactly five patterns, calls the list a denylist and states it does not claim coverage |
| Obligation on the units | A-02 (docstring), A-11 (`§4` text) and B-02 (`§6` text) must repeat the subset and must not use "complete", "any" or "every". The Phase 7 gate checks this |

### 5. Findings

| ID | Sev | Class | Finding and proof | Disposition |
| :--- | :--- | :--- | :--- | :--- |
| F-1 | S2 | instructing | `make verify` runs `scripts/map_workflows.py --check` and `scripts/check_readme_counts.py` (`Makefile:83-84`). A-12, A-13, A-14, B-10, B-11 change workflows (guide `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` goes stale), and five new `scripts/*.py` plus two new `config/*.json` change the README counts. The plan lists `README.md` under `## Documentary impact` (`check_readme_counts.py --write` at close) but no Work row owns `README.md` or the generated guide. `make verify` is therefore red between those units and close, and two changed files have no declared subject | Plan not patched. Treat both as close-time regenerated artifacts (`python3 scripts/map_workflows.py`, `python3 scripts/check_readme_counts.py --write`), never hand-edited; Phase 5 may add two rows. `make verify` exit 0 is claimable only after both |
| F-2 | S3 | instructing | Verification `rg ... github\.event\.issue ... .github/workflows/` expects no output. A-08 documents the S0 prohibition (plan D3); a comment in the YAML quoting `${{ github.event.issue.body }}` makes the row fail | A-08 must state the prohibition without the literal expression |
| F-3 | S3 | instructing | Verification `check_remediation_chain.py --range f0b11f8..HEAD` expects exit 0, but D5 A-1 exits 2 from the second link. Any gate remediation that is a `fix(` of a line introduced by an earlier `fix(` of the sprint (C-03..C-05, C-09 are `fix(`) makes the row unsatisfiable by design | Not a defect while no chain exists. If one appears, the exit 2 is the instrument working, and the row is read as that |
| F-4 | S3 | instructing | Verification `audit_plan.py <plan>` expects exit 0 on this plan. After B-08, the script exits 2 when a Work row touches a `blast_radius.json` glob and no Verification row contains `full_suite_command`. Verification row 2 is `venv_skillopt/bin/python -m pytest -q -p no:cacheprovider` | B-07 must set `full_suite_command` to exactly that string, and B-08 must be tested on this plan |
| F-5 | S3 | testifying | Tests table polarity is mixed: `test -f` rows are "fails" at exit 1, while the `split`, `--from-hook`, `pytest replays .py only` and `claude-agent-sdk==0.2.88` rows are defect-presence probes that "fail" at exit 0. The `KI-057-6` row is `unverified` | Honest as written. The C-09 test builds the fixture and QA Gate 1 reproduces it |
| F-6 | S3 | instructing | `scripts/_md_table.py` (C-01) has no row in `## Mechanisms` and, between C-01 and C-02, no importer. `verify_references.py` check (d) resolves Python imports (`RA-16`) | Commit C-01 and C-02 consecutively; run `make verify` only after C-02 |
| F-7 | S3 | instructing | `unambiguous_action` (`agents.md §1`): D5 R-8 "`open(` sobre una ruta no-test" and "`Path(__file__)` junto a `read`" do not define "no-test" or "junto a". D1 "los prefijos de token del escaner de secretos ya presente en el repositorio" names no scanner or file | B-14 and A-02 must name the exact predicate and the source file in their tests and docstrings |
| F-8 | S3 | testifying | D-08 is conditional ("yes" branch) while `close_workflow.md` Phase 1 persists `graph_stats.json` in the sprint directory on every close (`rules/documentation_standard.md:94`). On the "no" branch the close writes it; on the "yes" branch D-08 and the close would write the same file | Single writer per branch: on "yes" D-08 writes it and close re-runs at HEAD; on "no" close writes it |
| F-9 | S3 | instructing | `agents.md §4 feedback_upstream` requires that `§3 jurisdiction` and `workflows/extract_workflow.md` be grepped on every patch to the row (`RA-14`). A-11 therefore edits `§3 jurisdiction` in the same file; A-12 covers `extract_workflow.md`. The plan's A-11 row names only `§4` | Treated as part of subject A-11 (same file). The gate greps both restatements |

No S0 or S1 finding. No rule conflict between the plan and `agents.md` or `rules/` was found.

### 6. Resolutions after the plan revision

The principal revised `IMPLEMENTATION_PLAN.md`. Each resolution below was checked against the plan text by partial read (Work preamble, the named rows, Design D1/D5, Cost, Verification).

| ID | Resolution | Plan evidence |
| :--- | :--- | :--- |
| F-1 | Resolved. `README.md` (COUNTED block, `check_readme_counts.py --write`) and `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` (`map_workflows.py`) are generated mandatory companions, regenerated in the same commit as the unit that shifts them; they are not subjects | Work preamble "Companions generados"; Documentary impact rows for both |
| F-2 | Resolved. A-08 forbids `github.event.issue` between `${{ }}` anywhere in the file, comments included | A-08 row |
| F-3 | Resolved. The Verification row reads exit 2 as the A-1 stop, not as a check failure, and counts only in-range commits | Verification `check_remediation_chain.py` row |
| F-4 | Resolved. B-07 pins `full_suite_command` to `venv_skillopt/bin/python -m pytest -q -p no:cacheprovider` | B-07 row |
| F-5 | Accepted as is. Each Tests row already states its polarity | Tests table unchanged |
| F-6 | Resolved. C-01 and C-02 are committed consecutively | Work preamble, line 187-188 |
| F-7 | Resolved. D1 names `SECRET_ASSIGNMENT` and `UNQUOTED_ASSIGNMENT` of `hooks/on_commit.py`, imported and not copied. D5 R-8 is five literal substrings (`readFileSync(`, `?raw`, `.read_text(`, `.read_bytes(`, `open(`) with no path condition | D1 line 79-81; D5 R-8 row |
| F-8 | Resolved. D-08 is deleted; the Phase 8 close writes `graph_stats.json` on both D7 branches, so there is one writer | D7 line 169; Wave D table ends at D-07 |
| F-9 | Resolved. A-11 updates the `§3 jurisdiction` restatement of `§4` in the same commit (`RA-14`) and bans "complete", "any", "every" over the scan | A-11 row |

Counts: Work units 48 (A 17, C 9, B 15, D 7), matching plan `## Cost`. Remaining defect outside this file: `agent_assignment.md` still lists D-08 in the Wave D table and in "Disagreements with the plan", and `skill_assignment.md` may cite it; they are Phase 4.1/4.2 artifacts and were not edited here.

## Evidence

Run after writing this file: `python3 scripts/check_task_scope.py --sprint-dir docs/sprints/058-core-pipeline` (exit code read with `$?` in the Phase 4.3 report).
