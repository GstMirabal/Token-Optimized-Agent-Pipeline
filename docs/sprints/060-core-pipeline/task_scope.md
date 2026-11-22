# Task Scope — Sprint 060 (core-pipeline)

Source: `docs/sprints/060-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work` 84 rows, `## Design` D1-D17, `## Mechanisms`, `## Abort criterion`), HEAD `d9a1198`. Row count reproduces with `grep -cE '^\| [A-Z]-[0-9]{2} \|' docs/sprints/060-core-pipeline/IMPLEMENTATION_PLAN.md` = 84, and this file carries the same 84 ids (Z-04 was deleted by plan decision D15).
Staffing authority: `agent_assignment.md` (its Assignee column overrides the plan's `Assignee (proposed)`; the overwrites A-10, A-12, B-02, D-04, H-01, J-01 and O-09 are in its "Disagreements with the plan" and are used verbatim here). `skill_assignment.md` was read: it assigns no skill that adds a Work row; its `## Candidates` decisions are audited below (RV-22, RV-23).
Phase 4.3 of `workflows/pipeline_workflow.md`. Enforced by `scripts/check_task_scope.py`.
Mode: `claude-code`, `delegation_mode: native`. Sprint id 60 >= `MODEL_FROM_SPRINT` (28) and >= `COST_FROM_SPRINT` (60), so Model, Effort, `Est. cost` and `Suspend after` are all required.

## Tier transcription

Model and Effort are transcribed from each assignee's `agents/<role>.md` frontmatter (`model:`, `tier:`) and the `claude_code` column of `config/model_tiers.json` (`tiers.author.claude_code` = `sonnet` / `medium`). No tier is invented and no dated model ID is written. `session_tool` is `claude-code`, so `make cursor-tiers` does not apply. Waves N and O add no assignee: every N and O row is staffed by `doc_orchestrator`, `implementer_agent` or `rule_validator`, all `author` tier, so the five-row map below covers all 84 rows.

| Assignee | model | tier | effort |
| :--- | :--- | :--- | :--- |
| `doc_orchestrator` | sonnet | author | medium |
| `implementer_agent` | sonnet | author | medium |
| `rule_validator` | sonnet | author | medium |
| `orchestrator` | sonnet | author | medium |
| `agent_orchestrator` | sonnet | author | medium |

Declared escalations: none. No Work row is assigned to a `mechanical` profile (`agent_assignment.md` moved A-10, D-04 and H-01 from `devops_agent`, and B-02, J-01 and O-09 from `token_economy_agent`, to `implementer_agent`), so the mechanical-at-high-risk check does not apply. The high-risk rows (A-03, A-04, A-10, A-15, K-01, N-04, M-01, M-03, M-04, M-16, O-09, F-01, H-01) stay on the `author` tier: the adversarial check on them is the Phase 7 gate (`tier: gate`). No `token_economy_agent` verdict on tiers was produced for this sprint, so none is transcribed.

## Cost basis

`baseline_context` = 60612 (`config/unit_cost_estimates.json`); the segment ceiling is `baseline_context + sum <= 5 * baseline_context`, i.e. an accumulated `Est. cost` of at most 242448 between two `Suspend after: yes`, summed in file row order (`check_task_scope.py` `budget_findings`). Group per row: exact `operation/filetype/risk` group when it exists, else `operation/filetype`, else the `risk` group (config, YAML, `Makefile`, `.txt`, `allowed_signers`). Rename rows use `modify/doc/low`. `rules/*.md` and `agents.md` use `modify/rule`; `workflows/*.md`, `agents/*.md`, ADRs, guides, templates and reports use `doc`. New rows: N-04, M-16, O-09 `create/doc` (115354); A-15 `modify/doc` (3753); M-01, M-03, M-04 `create/script/high` (15109); M-13, M-15, O-08 `create/script/medium` (33574); O-07, N-03 `modify/script/medium` (10101); `claude/` and `Makefile` rows use the `risk` group (4613 low, 10101 medium).

| Segment closes at | Accumulated `Est. cost` | Why there |
| :--- | :--- | :--- |
| A-02 | 230708 | A-03 would reach 245817 |
| A-08 | 180488 | The human installs the broker and registers it (guide A-09, installer A-04) before A-10 can measure; A-10 would reach 295842 |
| B-02 | 147284 | End of the model-detector wave |
| N-03 | 190353 | The human applies `install.py` and opens a new session before N-04 measures (D16); N-04 would reach 305707 |
| N-04 | 115354 | M-02 would reach 245817 |
| M-04 | 160681 | The human installs and registers the graph MCP server at user scope (D2, D14) before consumers use it |
| M-16 | 218213 | O-01 would reach 333567 |
| O-08 | 170221 | O-09 would reach 285575 |
| M-14 | 186722 | End of the settings chain; L-05 would reach 302076 |
| L-06 | 119967 | End of the advisory wave |
| O-02 | 238106 | G-01 would reach 242823 |
| I-09 | 157837 | J-01 would reach 273191 |
| J-02 | 230708 | Z-01 would reach 346062 |
| Z-02 | 230708 | Z-03 would reach 346062 |

The last segment (Z-03, Z-05, Z-06, A-15) sums to 124703. The bound is on estimates (soft). A-10, H-01, N-04, M-16 and O-09 are the largest uncertainty (`create/doc` `max_fresh` 152885); if one measures above 242448 alone the suspension must come earlier.

## Work

Status values: ⏳ pending, ✅ committed (short SHA). Risk is transcribed from the plan. `Depends on` records order only where one exists in the plan or where this audit found one (see "Same-file ordering"). Rows Z-01 and Z-03 already exist on disk (`4cb4570`, `024598e`) and Z-02 is this file; they are `pending` here because the Phase 4.3 contract sets `pending` on every unit and the closing commit stamps them. Tables follow the plan's execution order (A, B, K, N, M, O, L, C, D, E, F, G, H, I, J, Z) with three rows relocated into the table of their predecessor (O-11 and M-14 into Wave L after L-04; O-02 into Wave F after F-02) because `check_task_scope.py` treats a table as a barrier and a dependency on a later table is unschedulable (finding RV-26). A-15 is the last table: it runs at the deployment, after Phase 8 (RV-7).

### Wave A — GitHub App broker

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| A-01 | `docs/decisions/ADR-0025-github-app-broker.md` | create: D1-D6; replaces `ADR-0019` D2 and D6; same commit adds `Superseded by ADR-0025` to the D2 and D6 rows of `ADR-0019` | medium | `doc_orchestrator` | sonnet | medium | 115354 | | - | ⏳ pending |
| A-02 | `docs/architecture/GITHUB_BROKER_BLUEPRINT.md` | create: from `BLUEPRINT_TEMPLATE.md` | low | `doc_orchestrator` | sonnet | medium | 115354 | yes | A-01 | ⏳ pending |
| A-03 | `scripts/github_broker.py` | create: stdio MCP server with the D4 operations; companion `tests/test_github_broker.py` in the same commit | high | `implementer_agent` | sonnet | medium | 15109 | | A-01 | ⏳ pending |
| A-09 | `docs/guides/GITHUB_BROKER_SETUP_GUIDE.md` | create: human steps (create the App, D4 permissions, install on the nucleus only, keys, `install_broker.py`, `claude mcp add --scope user`) | low | `doc_orchestrator` | sonnet | medium | 115354 | | A-03 | ⏳ pending |
| A-04 | `scripts/install_broker.py` | create: install from a signed tag or a named `main` commit (D5); companion `tests/test_install_broker.py`; its `invoked_by:` is the guide A-09, which exists first | high | `implementer_agent` | sonnet | medium | 15109 | | A-03, A-09 | ⏳ pending |
| A-05 | `claude/settings.hooks.json` | modify: `denyRead` and `permissions.deny` of D3; check `grep -c excludedCommands` = 0 | medium | `implementer_agent` | sonnet | medium | 10101 | | - | ⏳ pending |
| A-06 | `config/allowed_signers` | create: public signing key the human pastes; the agent does not generate it | low | `implementer_agent` | sonnet | medium | 4613 | | - | ⏳ pending |
| A-07 | `scripts/sync_agents_pin.py` | modify: `git verify-tag` (D6); companion `tests/test_sync_agents_pin.py` | medium | `implementer_agent` | sonnet | medium | 10101 | | A-06 | ⏳ pending |
| A-08 | `scripts/install.py` | modify: `git verify-tag` (D6); companion `tests/test_install.py` | medium | `implementer_agent` | sonnet | medium | 10101 | yes | A-06 | ⏳ pending |
| A-10 | `docs/sprints/060-core-pipeline/BROKER_MEASUREMENT.md` | create: M1 keys unreadable (exit codes only), M2 installed broker not editable, M3 no token in the enumerated set, M4 live D4 rejections | high | `implementer_agent` | sonnet | medium | 115354 | | A-03, A-04, A-05, A-09 | ⏳ pending |
| A-11 | `workflows/deployment_workflow.md` | modify: push, PR, merge, tag and Release through the broker | medium | `doc_orchestrator` | sonnet | medium | 3753 | | A-03 | ⏳ pending |
| A-12 | `agents/devops_agent.md` | modify: GitHub operations run through the broker's MCP tools; keeps `Bash` only, no write authority (`ADR-0009`) | low | `doc_orchestrator` | sonnet | medium | 2798 | | A-11 | ⏳ pending |
| A-13 | `rules/project_topology.md` | modify: `gh`/credential row now names the broker (`KI-059-21`, `-22`, `-24`) | medium | `doc_orchestrator` | sonnet | medium | 7867 | | A-11 | ⏳ pending |
| A-14 | `workflows/repository_hardening_workflow.md` | modify: measured state of `ADR-0019` D7 and the App installation | low | `doc_orchestrator` | sonnet | medium | 2798 | | - | ⏳ pending |

### Wave B — Model detector

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| B-01 | `scripts/detect_new_models.py` | modify (fix): fail closed and new catalogue source (D8); companion `tests/test_detect_new_models.py::test_check_fails_closed_without_catalogue` | medium | `implementer_agent` | sonnet | medium | 10101 | | - | ⏳ pending |
| B-02 | `config/model_tiers.json` | modify: `catalog_snapshot`, `context_limits.haiku`, `excluded` (`claude-fable-5-2`), `verified_at`; values come from `token_economy_agent` | low | `implementer_agent` | sonnet | medium | 4613 | yes | B-01 | ⏳ pending |

### Wave K — `graphifyy` pin

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| K-01 | `requirements-core.txt` | modify: `graphifyy` 0.8.30 to the newest version >= 0.9.70 published >= 24 h ago, closure and hashes regenerated; same commit reviews the `scripts/graph_update.py` workaround and edits the version figures in `rules/graphify.md` (D12, RV-9) | high | `implementer_agent` | sonnet | medium | 54797 | | - | ⏳ pending |

### Wave N — Session transcript read (D16)

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| N-01 | `docs/decisions/ADR-0027-session-transcript-read.md` | create: amends the `~/.claude/projects` row of `ADR-0019` (stays in `denyRead`, `allowRead` only for the current project directory) | medium | `doc_orchestrator` | sonnet | medium | 115354 | | A-01 | ⏳ pending |
| N-02 | `claude/settings.hooks.json` | modify: `allowRead` with the `{{PROJECT_TRANSCRIPT_DIR}}` marker (`RA-15`); after A-05 | medium | `implementer_agent` | sonnet | medium | 10101 | | A-05 | ⏳ pending |
| N-03 | `scripts/install.py` | modify: renders the marker with Claude Code's path encoding for nucleus and host; after A-08; companion `tests/test_install.py` | medium | `implementer_agent` | sonnet | medium | 10101 | yes | A-08, N-02 | ⏳ pending |
| N-04 | `docs/sprints/060-core-pipeline/TRANSCRIPT_READ_MEASUREMENT.md` | create: from the sandbox after the human runs `install.py` and opens a new session: `session_cost.py --from-anchor` `measurable: true`, `prompt_count.py` exit `0`; another project EPERM; exit codes only | high | `implementer_agent` | sonnet | medium | 115354 | yes | N-03 | ⏳ pending |

### Wave M — Graph as brain (D14)

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| M-01 | `scripts/graph_battery.py` | create: fixed structural query battery against Python AST truth; exit `2` on a differing query or inverted edge; companion `tests/test_graph_battery.py` | high | `implementer_agent` | sonnet | medium | 15109 | | - | ⏳ pending |
| M-02 | `docs/audits/GRAPH_USAGE_AUDIT_REPORT-060.md` | create: baseline with 0.8.30 and after K-01, real consumers, rebuild cost, graph queries versus grep in Phases 1-4 | medium | `implementer_agent` | sonnet | medium | 115354 | | M-01, K-01 | ⏳ pending |
| M-03 | `scripts/graph_query.py` | create: structural queries on `graph.json` with edge-direction correction and transitive closure; companion `tests/test_graph_query.py` | high | `implementer_agent` | sonnet | medium | 15109 | | M-01 | ⏳ pending |
| M-04 | `scripts/graph_mcp.py` | create: read-only stdio MCP server exposing M-03; user-scope install outside writable trees; companion `tests/test_graph_mcp.py` | high | `implementer_agent` | sonnet | medium | 15109 | yes | M-03, A-04 | ⏳ pending |
| M-05 | `claude/mcp.json` | modify: removes the project-scope `graphify` entry in favour of the M-04 user registration | medium | `implementer_agent` | sonnet | medium | 10101 | | M-04 | ⏳ pending |
| M-06 | `rules/graphify.md` | modify: structural-first protocol (symbol or file through M-03/M-04); natural-language CLI mode not used | medium | `doc_orchestrator` | sonnet | medium | 7867 | | K-01, M-03, M-04 | ⏳ pending |
| M-07 | `agents/principal_agent.md` | modify: Phase 1 impact by `impact`/`dependents` before drafting Work | low | `doc_orchestrator` | sonnet | medium | 2798 | | M-06 | ⏳ pending |
| M-08 | `agents/rule_validator.md` | modify: Phase 4.3 dependent files by `dependents` instead of Grep | low | `doc_orchestrator` | sonnet | medium | 2798 | | M-06 | ⏳ pending |
| M-09 | `agents/qa_agent.md` | modify: Gate 1 graph integrity with `graph_battery.py` and the diff's impact radius | low | `doc_orchestrator` | sonnet | medium | 2798 | | M-06 | ⏳ pending |
| M-10 | `agents/implementer_agent.md` | modify: `callers`/`callees` before editing a symbol | low | `doc_orchestrator` | sonnet | medium | 2798 | | M-06 | ⏳ pending |
| M-11 | `agents/doc_orchestrator.md` | modify: references of a document by `dependents` before editing or renaming | low | `doc_orchestrator` | sonnet | medium | 2798 | | M-06 | ⏳ pending |
| M-12 | `workflows/pipeline_workflow.md` | modify: graph query steps in Phases 1, 4.3, 6 and 7 | medium | `doc_orchestrator` | sonnet | medium | 3753 | | M-06 | ⏳ pending |
| M-13 | `hooks/graph_usage_log.py` | create: `PostToolUse` hook logging graph queries against `Grep`, `Glob` and search by `Bash`; companion `tests/test_graph_usage_log.py` | medium | `implementer_agent` | sonnet | medium | 33574 | | - | ⏳ pending |
| M-15 | `scripts/check_graph_usage.py` | create: exit `2` if a research phase searched by text before querying the graph; named invoker `workflows/close_workflow.md` (finding RV-19); companion `tests/test_check_graph_usage.py` | medium | `implementer_agent` | sonnet | medium | 33574 | | M-13 | ⏳ pending |
| M-16 | `docs/sprints/060-core-pipeline/GRAPH_AB_MEASUREMENT.md` | create: A/B with and without the graph on the same research tasks; `fresh` tokens by `session_cost.py` (finding RV-24 on who runs it); threshold >= 30 % | high | `implementer_agent` | sonnet | medium | 115354 | yes | M-04, N-04 | ⏳ pending |

### Wave O — Forge trigger and capability evaluation (D17)

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| O-01 | `docs/decisions/ADR-0028-forge-trigger.md` | create: D17 candidate criterion, `forge`/`reuse` decision with evidence, A/B threshold; records the `skills.sh` egress (O-11) | medium | `doc_orchestrator` | sonnet | medium | 115354 | | - | ⏳ pending |
| O-03 | `agents/agent_orchestrator.md` | modify: `agent_creation` defines "suitable" with the D17 criterion and requires the `Candidates` table | low | `doc_orchestrator` | sonnet | medium | 2798 | | O-01 | ⏳ pending |
| O-04 | `agents/skill_architect.md` | modify: `skill_search` starts from the D17 candidates and records each decision | low | `doc_orchestrator` | sonnet | medium | 2798 | | O-01 | ⏳ pending |
| O-05 | `docs/standards/templates/AGENT_ASSIGNMENT_TEMPLATE.md` | modify: `Candidates` table (candidate, units, criterion a/b, evidence, decision, reason) | low | `doc_orchestrator` | sonnet | medium | 2798 | | O-01 | ⏳ pending |
| O-06 | `docs/standards/templates/SKILL_ASSIGNMENT_TEMPLATE.md` | modify: the same `Candidates` table | low | `doc_orchestrator` | sonnet | medium | 2798 | | O-01 | ⏳ pending |
| O-07 | `scripts/check_forge_ladder.py` | modify: exit `2` without a `Candidates` table or with a candidate lacking evidence or decision (sprint >= 60); companion `tests/test_check_forge_ladder.py::test_missing_candidates_table_fails` (finding RV-21) | medium | `implementer_agent` | sonnet | medium | 10101 | | O-05, O-06 | ⏳ pending |
| O-08 | `scripts/capability_usage.py` | create: invocations per profile (`Agent` `subagent_type`) and per skill (`Skill`) from project transcripts and prior assignments; after N-04; docstring `invoked_by:` (finding RV-18); companion `tests/test_capability_usage.py` | medium | `implementer_agent` | sonnet | medium | 33574 | yes | N-04 | ⏳ pending |

### Wave L — Dependency advisories (and the tail of the settings chain)

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| O-09 | `docs/audits/CAPABILITY_EVALUATION_REPORT-060.md` | create: usage (O-08), overlaps and gaps of the 14 profiles and 34 skills; D17 candidates decided with an A/B by `session_cost.py` (findings RV-20, RV-25) | high | `implementer_agent` | sonnet | medium | 115354 | | O-07, O-08, M-03 | ⏳ pending |
| O-10 | `workflows/pipeline_workflow.md` | modify: Phases 4.1 and 4.2 done-criterion, `Candidates` table with `capability_usage.py` as evidence; after M-12 | medium | `doc_orchestrator` | sonnet | medium | 3753 | | M-12, O-08 | ⏳ pending |
| L-01 | `scripts/check_dependency_advisories.py` | create: OSV `/v1/querybatch` (stdlib) per `requirements*.txt` pin, exit `2` on advisory or no network (D13); companion `tests/test_check_dependency_advisories.py` | medium | `implementer_agent` | sonnet | medium | 33574 | | K-01 | ⏳ pending |
| L-02 | `.github/workflows/ci.yml` | modify: L-01 on every PR and a daily cron on `main` | medium | `implementer_agent` | sonnet | medium | 10101 | | L-01 | ⏳ pending |
| L-03 | `scripts/session_start.py` | modify: boot shows L-01 as a warning in nucleus and host (D13); companion `tests/test_session_start.py` | medium | `implementer_agent` | sonnet | medium | 10101 | | L-01, A-07 | ⏳ pending |
| L-04 | `claude/settings.hooks.json` | modify: `api.osv.dev` in `sandbox.network.allowedDomains` (D13) | low | `implementer_agent` | sonnet | medium | 4613 | | A-05, N-02 | ⏳ pending |
| O-11 | `claude/settings.hooks.json` | modify: `skills.sh` in `sandbox.network.allowedDomains` (human decision 2026-11-22); after L-04, before M-14; recorded in ADR-0028 | low | `implementer_agent` | sonnet | medium | 4613 | | L-04, O-01 | ⏳ pending |
| M-14 | `claude/settings.hooks.json` | modify: registers the M-13 hook; after A-05, N-02, L-04 and O-11 | low | `implementer_agent` | sonnet | medium | 4613 | yes | M-13, O-11 | ⏳ pending |
| L-05 | `docs/decisions/ADR-0026-dependency-advisory-check.md` | create: D13 and the egress widening; same commit adds `Amended by ADR-0026` to `ADR-0024` | low | `doc_orchestrator` | sonnet | medium | 115354 | | L-01, L-04 | ⏳ pending |
| L-06 | `.github/dependabot.yml` | create: only if the alert #28 message shows the missing `pip` config blocked the PR; otherwise the row closes with the transcribed message (D13) | low | `implementer_agent` | sonnet | medium | 4613 | yes | - | ⏳ pending |

### Wave C — Ledger seal

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| C-01 | `workflows/deployment_workflow.md` | modify: `ledger_seal` on `ai-sprint/[ID]` (D7, `KI-059-35`) | medium | `doc_orchestrator` | sonnet | medium | 3753 | | A-11 | ⏳ pending |

### Wave D — Host-term scanner

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| D-01 | `scripts/check_host_terms.py` | create: hash scanner (D9); companion `tests/test_check_host_terms.py` | medium | `implementer_agent` | sonnet | medium | 33574 | | - | ⏳ pending |
| D-02 | `config/host_term_hashes.json` | create: hashes the human generates and pastes; the agent does not fabricate them | low | `implementer_agent` | sonnet | medium | 4613 | | - | ⏳ pending |
| D-03 | `tests/test_profile_references.py` | modify: use `check_host_terms.py` (`KI-059-14`) | low | `implementer_agent` | sonnet | medium | 4717 | | D-01 | ⏳ pending |
| D-04 | `docs/sprints/060-core-pipeline/HISTORY_REVIEW_REPORT.md` | create: scan of `origin/main`, SHA, path and line only, never the matched text; rewriting history stays a human decision (`KI-059-12`) | medium | `implementer_agent` | sonnet | medium | 115354 | | D-01, D-02 | ⏳ pending |
| D-05 | `Makefile` | modify: `verify` invokes `scripts/check_host_terms.py` (`RA-16`) | low | `implementer_agent` | sonnet | medium | 4613 | | D-01 | ⏳ pending |

### Wave E — Gate log

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| E-01 | `scripts/check_gate_log.py` | modify (fix): one Gate findings row per S0-S2 finding; companion `tests/test_check_gate_log.py::test_s0_s2_finding_without_row_fails` | medium | `implementer_agent` | sonnet | medium | 10101 | | - | ⏳ pending |

### Wave F — Normative text

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| F-01 | `agents.md` | modify: trim under 20000 bytes; `mass-standardizer` wording (`KI-059-32`); `RA-09` and `§6 devops_agent` name the broker | high | `rule_validator` | sonnet | medium | 49477 | | A-12 | ⏳ pending |
| F-02 | `rules/skills_and_integrations.md` | modify: `mass-standardizer` wording (`KI-059-32`) | low | `rule_validator` | sonnet | medium | 4037 | | - | ⏳ pending |
| O-02 | `rules/skills_and_integrations.md` | modify: §1 the ladder opens per D17 candidate, not only for functions outside the stdlib; after F-02 | medium | `rule_validator` | sonnet | medium | 7867 | yes | F-02, O-01 | ⏳ pending |

### Wave G — Measurement scripts

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| G-01 | `scripts/unit_cost.py` | modify (fix): only backticked SHAs that resolve as a commit (`KI-059-34`); companion `tests/test_unit_cost.py::test_non_commit_hex_in_status_is_ignored` | low | `implementer_agent` | sonnet | medium | 4717 | | - | ⏳ pending |
| G-02 | `scripts/prompt_count.py` | modify (fix): `EPERM` on the transcript prints the human command and a documented exit `2` (`KI-059-34`); companion `tests/test_prompt_count.py::test_eperm_prints_human_command` | low | `implementer_agent` | sonnet | medium | 4717 | | - | ⏳ pending |

### Wave H — Sandbox re-measurement

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| H-01 | `docs/sprints/060-core-pipeline/SANDBOX_REMEASUREMENT.md` | create: 055 and 056 matrices on one fixed CLI (`KI-059-31`) | high | `implementer_agent` | sonnet | medium | 115354 | | - | ⏳ pending |
| H-02 | `rules/project_topology.md` | modify: `Measuring CLI` row and the rows H-01 changes | medium | `doc_orchestrator` | sonnet | medium | 7867 | | A-13, H-01 | ⏳ pending |

### Wave I — `RA-06` renames (D10, audit 059 R1-R9)

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| I-01 | `docs/architecture/global_topology.md` | modify: rename to `GLOBAL_TOPOLOGY_MAP.md` (R1) with `git mv`; reference edits are companions of the same commit; grep of the old path returns 0 outside sealed records | low | `doc_orchestrator` | sonnet | medium | 2798 | | - | ⏳ pending |
| I-02 | `docs/architecture/topology_map.md` | modify: rename to `TOPOLOGY_MAP.md` (R2) with `git mv`; same grep | low | `doc_orchestrator` | sonnet | medium | 2798 | | - | ⏳ pending |
| I-03 | `docs/contracts/core/doc_orchestrator_contract.md` | modify: rename to `DOC_ORCHESTRATOR_CONTRACT.md` (R3) with `git mv`; same grep | low | `doc_orchestrator` | sonnet | medium | 2798 | | - | ⏳ pending |
| I-04 | `docs/contracts/core/topology_mapper_contract.md` | modify: rename to `TOPOLOGY_MAPPER_CONTRACT.md` (R4) with `git mv`; same grep | low | `doc_orchestrator` | sonnet | medium | 2798 | | - | ⏳ pending |
| I-05 | `docs/contracts/core/topology_scaffolder_contract.md` | modify: rename to `TOPOLOGY_SCAFFOLDER_CONTRACT.md` (R5) with `git mv`; same grep | low | `doc_orchestrator` | sonnet | medium | 2798 | | - | ⏳ pending |
| I-06 | `docs/audits/TOKEN_ECONOMY_AUDIT-documentation-standard.md` | modify: rename to `TOKEN_ECONOMY_DOCUMENTATION_STANDARD_AUDIT.md` (R6) with `git mv`; same grep | low | `doc_orchestrator` | sonnet | medium | 2798 | | - | ⏳ pending |
| I-07 | `docs/audits/SKILLOPT_TRANSITIVE_CLOSURE.md` | modify: rename to `SKILLOPT_TRANSITIVE_CLOSURE_AUDIT.md` (R7) with `git mv`; same grep | low | `doc_orchestrator` | sonnet | medium | 2798 | | - | ⏳ pending |
| I-08 | `docs/audits/THIRD_PARTY_PROVENANCE_TODO.md` | modify: rename to `THIRD_PARTY_PROVENANCE_REGISTER.md` (R8) with `git mv`; same grep | low | `doc_orchestrator` | sonnet | medium | 2798 | | - | ⏳ pending |
| I-09 | `docs/plans/027-autonomy-posture-DRAFT.md` | modify: rename to `AUTONOMY_POSTURE_PLAN.md` (R9) with `git mv`; same grep | low | `doc_orchestrator` | sonnet | medium | 2798 | yes | - | ⏳ pending |

### Wave J — Audits

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| J-01 | `docs/audits/PROMPT_AUDIT_REPORT-060.md` | create: measurement and findings (D11) | medium | `implementer_agent` | sonnet | medium | 115354 | | - | ⏳ pending |
| J-02 | `docs/audits/PROSE_MOTIVES_AUDIT_REPORT-060.md` | create: prose motives in normative documents (D11) | medium | `rule_validator` | sonnet | medium | 115354 | yes | - | ⏳ pending |

### Wave Z — Pipeline and closeout artifacts

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Z-01 | `docs/sprints/060-core-pipeline/SPRINT_LOG.md` | create: Phase 3 | low | `orchestrator` | sonnet | medium | 115354 | | - | ⏳ pending |
| Z-02 | `docs/sprints/060-core-pipeline/task_scope.md` | create: Phase 4.3 | low | `rule_validator` | sonnet | medium | 115354 | yes | - | ⏳ pending |
| Z-03 | `docs/sprints/060-core-pipeline/agent_assignment.md` | create: Phase 4.1 | low | `agent_orchestrator` | sonnet | medium | 115354 | | - | ⏳ pending |
| Z-05 | `CHANGELOG.md` | modify: `[Unreleased]` | low | `doc_orchestrator` | sonnet | medium | 2798 | | - | ⏳ pending |
| Z-06 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify: KI routed to closed | low | `orchestrator` | sonnet | medium | 2798 | | - | ⏳ pending |

### Deployment-time unit (after Phase 8)

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| A-15 | `docs/sprints/060-core-pipeline/BROKER_MEASUREMENT.md` | modify: M5 at the 060 deployment (push, PR, merge, signed tag, Release by the agent, each GitHub ID recorded); gates read M1-M4 (RV-7) | high | `implementer_agent` | sonnet | medium | 3753 | | A-10, A-11 | ⏳ pending |

## Same-file ordering (`jurisdictional_lock`, `no_interference`)

Eighty-four rows; every `File` cell is distinct except the seven files below. No two rows are `in progress` at once: the plan executes sequentially (`agent_assignment.md` Mode column), and each chain is ordered by `Depends on`.

| File | Rows in order | Order recorded |
| :--- | :--- | :--- |
| `claude/settings.hooks.json` | A-05, N-02, L-04, O-11, M-14 | N-02 after A-05; L-04 after A-05 and N-02; O-11 after L-04; M-14 after O-11 (plan rows A-05/N-02/M-14/O-11). The plan's execution-order line runs M and O before L, which contradicts M-14 and O-11 "after L-04" (RV-26); O-11 and M-14 sit in the Wave L table |
| `scripts/install.py` | A-08, N-03 | N-03 `Depends on` A-08, N-02; companion `tests/test_install.py` reached by both in that order |
| `workflows/pipeline_workflow.md` | M-12, O-10 | O-10 `Depends on` M-12 |
| `rules/skills_and_integrations.md` | F-02, O-02 | O-02 `Depends on` F-02; the plan's wave order has O before F (RV-26), so O-02 sits in the Wave F table |
| `workflows/deployment_workflow.md` | A-11, C-01 | C-01 `Depends on` A-11; C-01 rewrites the merge/seal sequence A-11 wrote |
| `rules/project_topology.md` | A-13, H-02 | H-02 `Depends on` A-13 and H-01; disjoint rows |
| `docs/sprints/060-core-pipeline/BROKER_MEASUREMENT.md` | A-10, A-15 | A-15 `Depends on` A-10 and is the last table: M5 is written at the deployment |

Companion edits that cross rows (not structural subjects): `docs/decisions/ADR-0019-*` (A-01 `Superseded by`, N-01 amendment; A-01 first), `rules/graphify.md` (K-01 figures, then M-06), `tests/test_template_sandbox.py`, `tests/test_install_nucleus_sandbox.py`, `tests/test_merge_json.py` and `tests/test_mcp_template.py` (assert the settings and MCP templates; A-05, N-02, L-04, O-11, M-14, M-05 reach them in chain order), `tests/test_session_start.py` (A-07 new exit `2`, then L-03). `agents/implementer_agent.md` (M-10) and `agents/doc_orchestrator.md` (M-11) are the profiles of the assignees of other rows: they are edited as subjects only by M-10 and M-11, one subject each.

## Dependent files (graphify and reference graph)

`graphify-out/graph.json` exists; this dispatch had no shell, so it was queried only with `Grep` (1048 nodes carry a `source_file` of `scripts/check_task_scope.py`, `check_forge_ladder.py`, `install.py` or `install_broker.py`), not by a `python3` traversal or a `scripts/` graph helper. `scripts/graph_query.py` does not exist yet (M-03). Importers and mentions below come from `Grep` over `scripts/ hooks/ tests/ workflows/ rules/ agents/ config/ Makefile`, so they are measured but not a graph traversal.

| Unit | Dependent files the unit will touch or must re-check |
| :--- | :--- |
| A-05, N-02, L-04, O-11, M-14 | `tests/test_template_sandbox.py`, `tests/test_install_nucleus_sandbox.py`, `tests/test_merge_json.py`; consumers `scripts/install.py`, `scripts/merge_json.py`, `scripts/with_env.py`, `scripts/session_end_hook.py`, `hooks/on_init.py`, `hooks/on_commit.py`, `hooks/state_mirror.py`; `permissions.deny` lines 23-24 hold `WebFetch` and `WebSearch` (RV-16) |
| A-07 | `scripts/session_start.py` (calls it at lines 19, 453, 681; must handle exit `2`), `scripts/_root.py:58`, `scripts/_mode.py:37`, `workflows/start_workflow.md:32`, `workflows/close_workflow.md:35` |
| A-08, N-03 | `scripts/install_lock.py`, `scripts/merge_json.py`, `scripts/_mode.py`; `rules/project_topology.md` and `workflows/repository_hardening_workflow.md` cite `ADR-0019` D2/D6 |
| A-11, C-01, M-12, O-10, A-14 | `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` (generated; `make verify` runs `scripts/map_workflows.py --check`, Makefile:85); `scripts/session_state.py`, `scripts/check_role_artifact.py`, `tests/test_session_state.py`, `tests/test_session_protocol.py`, `workflows/close_workflow.md` |
| B-01, B-02 | `scripts/_root.py:55`, `scripts/_md_table.py:14`, `Makefile:84`, `tests/test_detect_new_models.py`; `config/model_tiers.json` is read by `scripts/audit_cursor_models.py` and the profile/tier check in `make verify` |
| K-01 | `scripts/graph_update.py`, `rules/graphify.md:18` ("graphifyy 0.8.30"), `rules/project_topology.md:38,40`, `tests/test_mcp_template.py`, `Makefile:32-44` |
| M-01 .. M-05 | `scripts/graph_update.py`, `scripts/graph_reconcile.py` (`Makefile:34,44`), `claude/mcp.json`, `tests/test_mcp_template.py`, `scripts/install_broker.py` (A-04; M-04 install, RV-28) |
| M-07 .. M-11 | `agents/*.md` profile checks in `make verify` (`scripts/check_model_tiers.py`, profile reference tests) |
| O-05 .. O-07, O-10 | `scripts/check_forge_ladder.py` invoked by `workflows/pipeline_workflow.md` Phases 4.1 and 4.2 (line 10 of the script), `config/template_gates.json:75`, `tests/test_check_forge_ladder.py` |
| O-08 | `scripts/session_cost.py`, `scripts/prompt_count.py` (transcript readers), `docs/sprints/*/agent_assignment.md`, `skill_assignment.md` |
| L-01 .. L-03 | `scripts/session_start.py` (L-03 subject), `.github/workflows/ci.yml` (L-02 subject), `config/invocation_exceptions.json` only if the invoker is not a file |
| D-01, D-05 | `Makefile` `verify` (D-05 subject), `tests/test_profile_references.py` (D-03 subject) |
| E-01 | `scripts/check_plan_closure.py`, `scripts/check_role_artifact.py:360`, `scripts/model_ledger.py`, `scripts/audit_cursor_era.py`, `scripts/_current_sprint.py`, `scripts/_md_table.py`, `rules/qa_and_testing.md` (lines 71 and 99), `tests/test_check_gate_log.py`, `tests/test_gate_row_wording.py` |
| G-01, G-02 | `workflows/close_workflow.md:25,29`, `workflows/pipeline_workflow.md:22,24`, `scripts/check_task_scope.py` (cost columns), `tests/test_unit_cost.py`, `tests/test_prompt_count.py` |
| F-01 | `tests/test_cursor_phase1.py` (pins `RA-18`), `tests/test_gate_row_wording.py`, the `Command paths` row; `config/rule_triggers.json` mirrors the `Rule Contexts` table |
| I-01 .. I-09 | Reference counts outside sealed sprint records, by old name: `THIRD_PARTY_PROVENANCE_TODO` in `SECURITY.md`, `NOTICE.md`, `README.md` (line 214 twice), `CONTRIBUTING.md`, `profiles/example-project/README.md`; `topology_map.md` in `rules/token_economy.md:22`, `workflows/extract_workflow.md:27`, `docs/standards/templates/SYSTEM_OVERVIEW_TEMPLATE.md` (lines 6 and 52), `docs/hotfixes/H-007-mcp.md:38`, the two topology contracts; `global_topology.md` in `docs/contracts/core/doc_orchestrator_contract.md:9`, `skills/contract-writer/SKILL.md:30`; `SKILLOPT_TRANSITIVE_CLOSURE.md` in `skills/skillopt/SKILL.md:21`, `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md:680`, `docs/roadmaps/core/pipeline/021-030-program-queue.md:1321`; roadmap entries `007`, `014`..`018` and `docs/audits/PIPELINE_AUDIT_REPORT-059.md` also name old paths |

## RV-1 to RV-15 — status against the current plan

| ID | How the plan now resolves it | Status |
| :--- | :--- | :--- |
| RV-1 | D10: references edited in the `git mv` commit; third-party `skills/*/SKILL.md` exempt and listed; each I-row states the grep | resolved |
| RV-2 | D-05 modifies `Makefile` so `verify` invokes `check_host_terms.py` | resolved |
| RV-3 | A-09 is listed before A-04 and A-04 depends on it; A-03's invoker `workflows/deployment_workflow.md` is an existing file and `verify_references.py` (d) inspects only `#fragment` tokens | resolved |
| RV-4 | D-04 row: SHA, path and line only, never the matched text | resolved |
| RV-5 | A-10 row: M1 measured by exit codes only, no content printed | resolved |
| RV-6 | A-10 row: M3 limited to the enumerated set (`RA-19`) | resolved |
| RV-7 | A-15 split off (M5 at the deployment); Abort criterion cites M1-M4 in A-10 and M5 in A-15 | resolved |
| RV-8 | B-01, E-01, G-01, G-02, O-07 name `tests/<file>::<test>` | resolved |
| RV-9 | K-01 row adds `rules/graphify.md` figures; `rules/project_topology.md:38,40` cite the pin and neither A-13 nor H-02 lists it | partly open (project_topology) |
| RV-10 | A-01 and L-05 rows add the `Superseded by` / `Amended by` line; N-01 and O-01 repeat the defect (RV-27) | resolved for A-01, L-05 |
| RV-11 | A-12 row words the broker as MCP tools with `Bash` only and cites `ADR-0009`; F-01's row (`RA-09`/`§6 devops_agent` "con el broker") has no such wording | resolved for A-12, open for F-01 (S3) |
| RV-12 | D15 deletes Z-04; `ls docs/walkthroughs` stays absent | resolved |
| RV-13 | `Work units` 84 reproduces and `agent_assignment.md` says 84; the Cost row "Subagents dispatched" = "45 + gates" (plan line 206) contradicts "una dispatch por unidad" with 84 units | open (S3) |
| RV-14 | Verification table carries `grep -c excludedCommands claude/settings.hooks.json` -> 0 with a positive control; rows A-05 and L-04 cite no check (the table does) | resolved |
| RV-15 | A-06 and D-02 rows: the agent writes only what the human pastes | resolved |

## Rule audit findings (RV-16 onward)

Severity follows `RA-17` (S0-S3, `rules/qa_and_testing.md §4`). This audit did not edit the plan, `agent_assignment.md` or `skill_assignment.md`. Proposed fixes are one-line plan rows or row edits.

| ID | Unit | Rule | Finding and reproducing command | Proposed fix | Severity |
| :--- | :--- | :--- | :--- | :--- | :--- |
| RV-16 | O-11, O-04 (KI-060-01) | `agents/skill_architect.md` `skill_search`; `RA-19` | The profile's `tools:` line declares `WebSearch, WebFetch` and P3 is "via WebSearch/WebFetch", but `claude/settings.hooks.json:23-24` puts both in `permissions.deny`, which removes them from every agent whatever the profile says; `skills.sh` is also absent from `sandbox.network.allowedDomains` (lines 68-73). O-11 opens only the Bash egress, so after O-11 P3 through the declared tools still fails. `grep -n '"WebFetch"\|"WebSearch"' claude/settings.hooks.json`; `grep -c 'skills.sh' claude/settings.hooks.json` -> 0; `agents/git_sync_agent.md:4` declares `WebFetch` and is denied too | Add to O-04: P3 runs `curl` through Bash against `allowedDomains` and the profile drops `WebSearch, WebFetch` from `tools:` (no widening of `permissions.deny`) | S2 |
| RV-17 | Work table vs plan (KI-060-02) | `agents.md §1 fail_closed_claims` | `check_task_scope.py` `collect_findings` (lines 423-446) validates the rows present (shape, cost, dependencies) and never compares them with the plan, so a file lacking N-0x/O-0x rows passes. Not run before the edit (no shell in this dispatch); confirmed by reading the source. A unit is needed | `P-01 scripts/check_task_scope.py modify (fix): from sprint 60 exit 2 when a plan Work id is missing from task_scope.md or the reverse; test tests/test_check_task_scope.py::test_plan_row_missing_fails` | S2 |
| RV-18 | O-08 | `RA-16` | `capability_usage.py` is covered without an exception entry: the form `invoked_by: workflows/pipeline_workflow.md Phases 4.1 and 4.2` is the precedent of `scripts/check_forge_ladder.py:10`, and `verify_references.py` (d) (lines 749-755) needs only an `invoked_by:` line; the anchor check (884-899) inspects `#fragment` tokens only. The O-08 row does not say the docstring carries it, and the workflow names the script only after O-10 | Add to O-08: the docstring declares `invoked_by:` | S3 |
| RV-19 | M-01, M-03, M-04, M-15 | `RA-16` | `## Mechanisms` lists none of the Wave M scripts. M-15 names `workflows/close_workflow.md` as invoker (plan line 120) but no row edits that workflow (`grep -n close_workflow IMPLEMENTATION_PLAN.md` -> lines 120 only). `graph_battery.py` is invoked only by M-09/M-12 prose | `M-17 workflows/close_workflow.md modify: step that runs check_graph_usage.py; Mechanisms rows for graph_battery, graph_query, graph_mcp (user-scope registration, like github_broker)` | S2 |
| RV-20 | O-09 (and A-10, A-15, H-01, M-02, M-16, N-04, J-01, D-04, config/`claude/`/`.github/`/Makefile rows) | `agents.md §6` role usurpation; `agents/implementer_agent.md` `write_scope`, `agents/agent_orchestrator.md` `restriction` | `implementer_agent` holds `Write`/`Edit` for framework-root `scripts/`, `hooks/`, `tests/` only (`grep -n write_scope agents/implementer_agent.md`), yet O-09 and the reports are `docs/` files. O-09 also records the D17 `forge`/`reuse` decision that `## Mechanisms` (plan line 196) assigns to `agent_orchestrator` and `skill_architect`; `token_economy_agent` is only "accountable at the Phase 5 plan audit", which precedes Phase 6 where O-09 runs. `agent_assignment.md` says the A/B stays human-run, contradicting D16 (RV-24). The tool check of `check_task_scope.py` passes because it tests tool presence, not scope | `O-12 agents/implementer_agent.md modify: write_scope names sprint-directory reports, docs/audits/, config/, claude/, .github/, Makefile and requirements-core.txt; ADR-0009 amended in the same commit`; O-09 records evidence and `agent_orchestrator`/`skill_architect` record the decision | S2 |
| RV-21 | O-07, D17 Check, Verification | `agents.md §1 fail_closed_claims` | D17 Check (plan line 73) and Verification (line 240) expect `check_forge_ladder.py --sprint-dir docs/sprints/059-core-pipeline` -> `2` after O-07, but O-07 limits the new exit to "sprint >= 60", so 059 stays `0` and the positive control cannot hold. `grep -n 'sprint ≥ 60\|059-core-pipeline' IMPLEMENTATION_PLAN.md` | Change the control to a fixture sprint directory in `tests/test_check_forge_ladder.py`, or drop the 059 expectation | S2 |
| RV-22 | skill_assignment C4, C5, C6 | D17 (decision without a packaging skill is `none`, never `reuse` of the nearest skill) | C4 `reuse:python-quality-auditor`, C5 `reuse:python-quality-auditor`, C6 `reuse:env-shielding-auditor` are the nearest audit skills, not packages of OSV checking, script-plus-test authoring or settings editing; C3, C7, C8 with the same argument are `none`. `grep -n '^| C[0-9]' skill_assignment.md` | Re-decide C4, C5, C6 as `none` with the nearest skill named in Reason | S2 |
| RV-23 | skill_assignment C6, agent_assignment `claude/settings.hooks.json` candidate | `RA-14` | C6 counts 4 units (omits O-11): `grep -E '^\| [A-Z]-[0-9]{2} \|.*settings\.hooks\.json' IMPLEMENTATION_PLAN.md` returns 5 rows (A-05, N-02, M-14, O-11, L-04). For the same subject the agent file decides `forge-pending-O-09` and the skill file `reuse` | One count and one decision in both files | S2 |
| RV-24 | M-16, G-02, plan Cost row, `agent_assignment.md`/O-09 | `RA-14`, D16 | D16 (line 72) says "M-16 lo ejecuta el agente" and G-02 is verified in the sandbox, but M-16 (line 121) still says the human runs `session_cost.py` outside the sandbox, G-02 (line 149) prints a human command, Cost (line 207) says no prior ratio because of `denyRead`, and both assignment notes keep the A/B human-run. `grep -n 'fuera del sandbox\|humano ejecuta' IMPLEMENTATION_PLAN.md` | Patch M-16, Cost and both assignment notes to the D16 wording | S2 |
| RV-25 | O-09 | D17 (A/B on the candidate's units) | The A/B of C2 names A-10, A-15, H-01, N-04; H-01 (Wave H) and A-15 (deployment) run after O-09, so no per-unit `fresh` tokens exist when O-09 decides | `O-09` Depends on `H-01` for C2, or the A/B covers only the executed units A-10 and N-04 | S2 |
| RV-26 | Execution-order line, M-14, O-02, O-11 | `RA-14` | Line 80 orders N, M, O, L, C..F, but N-02 says "antes de M-14 y L-04", O-11 "después de L-04 y antes de M-14", M-14 "después de A-05 y L-04" and O-02 "después de F-02". Kept as written, `check_task_scope.py --batches` cannot schedule M-14, O-11 or O-02 (a table is a barrier). `grep -n 'después de' IMPLEMENTATION_PLAN.md` | Order line: `K -> N -> L-04 -> O-11 -> M -> O -> L -> ...`; O-02 moves into Wave F after F-02 | S2 |
| RV-27 | N-01, O-01 | `agents.md §4` / `RA-14` (same class as RV-10) | N-01 amends `ADR-0019` and O-01 records the `skills.sh` egress (an egress change `ADR-0024` governs) with no row text adding `Amended by` to the old ADR; A-01 and L-05 have it. `grep -n 'Amended by\|Superseded by' IMPLEMENTATION_PLAN.md` -> A-01 and L-05 only | Add the line to N-01 (`ADR-0019`) and O-01 (`ADR-0024`) | S2 |
| RV-28 | M-04, A-04, A-09 | `jurisdictional_lock`, `RA-14` | M-04 installs the graph server with `install_broker.py` (plan line 109), but A-04 specifies a broker-only installer and A-09 a broker-only guide; the change is a second structural subject with no row | `M-18 scripts/install_broker.py modify: install graph_mcp.py from a signed tag; companion test; A-09 guide gains the registration step` after M-04 | S2 |
| RV-29 | A-11, A-14, C-01, M-12, O-10 | `agents.md §0` (generated map), `RA-14` | `make verify` runs `python3 scripts/map_workflows.py --check` (Makefile:85); an edit of a workflow step table makes `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` stale and no row claims it | State in each row that the commit includes the regenerated guide | S2 |
| RV-30 | N-02, N-04, D16 | `RA-19` (1), `RA-09` | D16 "se mantiene la barrera entre proyectos" is a boundary claim, and N-04 measures one other project. `allowRead` on the project directory also exposes every earlier session of this project, which may hold pasted material (RA-09) | N-04 states "the enumerated set" (parent listing, one other project, `~/.claude.json`) with its criterion | S2 |
| RV-31 | agent_assignment candidates (documentation author, test-bearing script author) | D17 (b), memory rule "every decision needs a unit" | Both are `reuse` because "the gap is profile text" (a missing `rules/documentation_standard.md` or `rules/qa_and_testing.md` citation), but no row edits `agents/doc_orchestrator.md` or `agents/implementer_agent.md` for it (M-10, M-11 are graph steps). `grep -c 'rules/' agents/doc_orchestrator.md` | Extend M-10 and M-11 with the missing rule citations | S2 |
| RV-32 | M-13, M-15 | `rules/token_economy.md` Filter 5, `agents.md §5 state_homologation` | A new hook writes a per-session usage log, a new state-like file with no declared location, while D16 makes transcripts readable and O-08 already parses them for tool use; M-15 could read the same source | Delete M-13 and M-14, M-15 reads transcripts | S3 |
| RV-33 | M-02 | `rules/project_topology.md` (installs) | M-02 measures with 0.8.30 after K-01 replaced it; that needs a second environment no row names | State a scratch venv `pip install graphifyy==0.8.30` in M-02 | S3 |
| RV-34 | O-09/D17 | `agents/token_economy_agent.md` `burden_of_proof` | Candidate detection by criteria (a) and (b) is counting and path matching, classified as judgment in `## Mechanisms`; only the decision is judgment | `O-13 scripts/forge_candidates.py create` computing (a) and (b) | S3 |

No finding against `RA-16` for `check_dependency_advisories.py` (invokers rows L-02, L-03), `detect_new_models.py`, `check_gate_log.py`. O-09's change of assignee to `implementer_agent` conflicts with `write_scope` and the decision jurisdiction (RV-20); it does not conflict with `code_unit_assignee` (that rule covers `scripts/`, `hooks/`, `tests/`). No finding against `RA-09` for A-09, nor for F-01, F-02, J-02 (`rule_validator` holds `Write`/`Edit`).

## Verification record

`python3 scripts/check_task_scope.py --sprint-dir docs/sprints/060-core-pipeline`, `python3 scripts/check_sprint_refs.py --current-sprint` and `python3 skills/token-saver-auditor/scripts/audit_plan.py docs/sprints/060-core-pipeline/IMPLEMENTATION_PLAN.md` could not be run in this dispatch (no shell tool). Segment sums above were computed by hand from `config/unit_cost_estimates.json`; the maximum is 238106 against a ceiling of 242448.
