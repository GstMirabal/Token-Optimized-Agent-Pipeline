# Task Scope — Sprint 060 (core-pipeline)

Source: `docs/sprints/060-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work` 97 rows, `## Design` D1-D17, `## Mechanisms`, `## Abort criterion`), HEAD `1ba05b2`. Row count reproduces with `grep -cE '^\| [A-Z]-[0-9]{2} \|' docs/sprints/060-core-pipeline/IMPLEMENTATION_PLAN.md` = 97, and this file carries the same 97 ids (Z-04 was deleted by plan decision D15; O-12, P-01, M-17, M-18 were added by `241fc29`; O-13, O-14 by `9ae34dd`, which also moved M-18 before M-05 and M-16; Z-07 by `bdecc1a`; Q-01 by `a5131ea`; S-01..S-05 by `9e861b3`).
Staffing authority: `agent_assignment.md` (its Assignee column overrides the plan's `Assignee (proposed)`; the overwrites A-10, A-12, B-02, D-04, H-01 and J-01 are in its "Disagreements with the plan" and are used verbatim here; the O-09 overwrite was adopted by the plan in `241fc29` and is no longer a disagreement; its Wave S table (`1ba05b2`) lists S-01..S-04 for `skill_architect` and S-05 for `implementer_agent`, with no disagreement). `skill_assignment.md` was read: it assigns no skill that adds a Work row; its `## Candidates` decisions are audited below (RV-22, RV-23).
Phase 4.3 of `workflows/pipeline_workflow.md`. Enforced by `scripts/check_task_scope.py`.
Mode: `claude-code`, `delegation_mode: native`. Sprint id 60 >= `MODEL_FROM_SPRINT` (28) and >= `COST_FROM_SPRINT` (60), so Model, Effort, `Est. cost` and `Suspend after` are all required.

## Tier transcription

Model and Effort are transcribed from each assignee's `agents/<role>.md` frontmatter (`model:`, `tier:`) and the `claude_code` column of `config/model_tiers.json` (`tiers.author.claude_code` = `sonnet` / `medium`). No tier is invented and no dated model ID is written. `session_tool` is `claude-code`, so `make cursor-tiers` does not apply. Waves N and O add no assignee: every N and O row is staffed by `doc_orchestrator`, `implementer_agent` or `rule_validator`, all `author` tier, except that O-14 adds `skill_architect` (`agents/skill_architect.md` frontmatter `model: sonnet`, `tier: author`), so the six-row map below covers all 97 rows (new rows: Q-01 `doc_orchestrator`, O-12 `doc_orchestrator`, M-17 `doc_orchestrator`, P-01 `implementer_agent`, M-18 `implementer_agent`, O-13 `agent_orchestrator`, O-14 `skill_architect`, Z-07 `skill_architect`, S-01..S-04 `skill_architect`, S-05 `implementer_agent`).

| Assignee | model | tier | effort |
| :--- | :--- | :--- | :--- |
| `doc_orchestrator` | sonnet | author | medium |
| `implementer_agent` | sonnet | author | medium |
| `rule_validator` | sonnet | author | medium |
| `orchestrator` | sonnet | author | medium |
| `agent_orchestrator` | sonnet | author | medium |
| `skill_architect` | sonnet | author | medium |

Declared escalations: none. No Work row is assigned to a `mechanical` profile (`agent_assignment.md` moved A-10, D-04 and H-01 from `devops_agent`, and B-02, J-01 and O-09 from `token_economy_agent`, to `implementer_agent`), so the mechanical-at-high-risk check does not apply. The high-risk rows (A-03, A-04, A-10, A-15, K-01, N-04, M-01, M-03, M-04, M-16, O-09, F-01, H-01) stay on the `author` tier: the adversarial check on them is the Phase 7 gate (`tier: gate`). No `token_economy_agent` verdict on tiers was produced for this sprint, so none is transcribed.

## Cost basis

`baseline_context` = 60612 (`config/unit_cost_estimates.json`); the segment ceiling is `baseline_context + sum <= 5 * baseline_context`, i.e. an accumulated `Est. cost` of at most 242448 between two `Suspend after: yes`, summed in file row order (`check_task_scope.py` `budget_findings`). Group per row: exact `operation/filetype/risk` group when it exists, else `operation/filetype`, else the `risk` group (config, YAML, `Makefile`, `.txt`, `allowed_signers`). Rename rows use `modify/doc/low`. `rules/*.md` and `agents.md` use `modify/rule`; `workflows/*.md`, `agents/*.md`, ADRs, guides, templates and reports use `doc`. New rows: N-04, M-16, O-09 `create/doc` (115354); A-15 and O-12 `modify/doc` (3753; O-12 is `medium`); M-17 `modify/doc/low` (2798); P-01 and M-18 `modify/script/medium` (10101); M-01, M-03, M-04 `create/script/high` (15109); M-13, M-15, O-08 `create/script/medium` (33574); O-07, N-03 `modify/script/medium` (10101); `claude/` and `Makefile` rows use the `risk` group (4613 low, 10101 medium). Wave S rows: S-01 `modify/doc/low` (2798; a sprint document, low); S-02 `requirements-quality.txt` is a `.txt`, so the `risk medium` group (10101); S-03 `modify/script/medium` (10101; a fix); S-04 `create/doc` (115354); S-05 `create/script/medium` (33574).

| Segment closes at | Accumulated `Est. cost` | Why there |
| :--- | :--- | :--- |
| A-02 | 241012 | O-12, Q-01, S-01, A-01, A-02 (3753 + 3753 + 2798 + 115354 + 115354); margin 1436; A-03 would reach 256121. The S-01 table precedes Wave A in file order (the order the script sums), although A-01 and A-02 landed before S-01 was planned: in time S-01 runs after the A-02 suspension, so the segment executed after it is S-01 plus the A-03..A-08 segment, 183286 (2798 + 180488, margin 59162) (RV-48) |
| A-08 | 180488 | A-03, A-09, A-04, A-05, A-06, A-07, A-08 (A-03, A-05 and A-06 already landed, counted as the script counts every row). The human installs the broker and registers it (guide A-09, installer A-04) before A-10 can measure; A-10 would reach 295842 |
| A-14 | 132570 | A-10..A-14 (115354 + 3753 + 2798 + 7867 + 2798); end of Wave A. Without this suspension A-10..A-14 plus S-02..S-05 would reach 301700 and plus B-01, B-02 would reach 316414, past 242448; S-02 would reach 142671 |
| B-02 | 183844 | S-02..S-05, B-01, B-02 (10101 + 10101 + 115354 + 33574 + 10101 + 4613); margin 58604; end of the model-detector wave; K-01 would reach 238641 |
| N-03 | 190353 | The human applies `install.py` and opens a new session before N-04 measures (D16); N-04 would reach 305707 |
| N-04 | 115354 | M-02 would reach 255043 (N-04, L-04, O-11, M-01, M-02) |
| M-18 | 180008 | L-04, O-11, M-01..M-04, M-18. The human registers the graph MCP server at user scope (D2, D14) after M-18 installs it and before M-16 (RV-35 closed); M-05 would reach 190109 |
| M-17 | 225624 | M-05..M-17 (M-05..M-15, M-16, M-17); O-01 would reach 340978 |
| O-08 | 170221 | O-01..O-08; continuing to L-05 would reach 343104 |
| L-06 | 177496 | O-10, L-01..L-03, L-05, L-06; end of the advisory wave; D-04 would reach 339507 if the segment continued |
| F-02 | 240340 | C-01..F-02 including P-01; margin 2108 to the ceiling; O-02 would reach 248207 |
| I-09 | 165704 | O-02, G-01, G-02, H-01, H-02, I-01..I-09; J-01 would reach 281058 |
| J-02 | 230708 | O-09 would reach 346062 |
| O-09 | 115354 | O-09 alone; O-13, O-14, Z-01 and Z-02 after it would reach 236304 and Z-03 351658, so the segment closes at Z-02 below (Z-07 follows Z-03 in the last segment) |
| Z-02 | 236304 | O-13, O-14, Z-01, Z-02 (2798 + 2798 + 115354 + 115354); Z-03 would reach 351658 |

The last segment (Z-03, Z-07, Z-05, Z-06, A-15) sums to 240057 (115354 + 115354 + 2798 + 2798 + 3753; margin 2391 to the ceiling; Z-07 is `create/doc`). The bound is on estimates (soft). A-10, H-01, N-04, M-16 and O-09 are the largest uncertainty (`create/doc` `max_fresh` 152885); if one measures above 242448 alone the suspension must come earlier. The F-02 segment has the least margin (2108): a single overrun of `modify/script` there moves the suspension to E-01.

## Work

Status values: ⏳ pending, ✅ committed (short SHA). Risk is transcribed from the plan. `Depends on` records order only where one exists in the plan or where this audit found one (see "Same-file ordering"). Rows Z-01, Z-03 and Z-07 already exist on disk (`4cb4570`, `024598e`; Z-07 is `skill_assignment.md`, Phase 4.2) and Z-02 is this file; none is re-run in Phase 6; they are `pending` here because the Phase 4.3 contract sets `pending` on every unit and the closing commit stamps them. Tables follow the plan's execution-order line (plan line 80, `9e861b3`): O-12, Q-01, S-01, A, S-02..S-05, B, K, N, L-04 and O-11, M, O (without O-02, O-09, O-11, O-12), L (without L-04), C, D, E and P-01, F with O-02, G, H, I, J, O-09, O-13, O-14, Z; within Wave M the order is M-01..M-04, M-18, M-05..M-17 (`9ae34dd`, RV-35). A table is a barrier for `check_task_scope.py` and a dependency on a later table is unschedulable (RV-26, closed by `241fc29` plan line 80). O-11 no longer lists O-01 in `Depends on`: the plan runs O-11 before Wave O, so the ADR that records it (O-01) is written after the egress change, as ADR-0026 (L-05) follows L-04. M-14 returns to Wave M after M-13. A-15 is the last table: it runs at the deployment, after Phase 8 (RV-7).

### Wave O-12 — Implementer write scope (first unit)

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| O-12 | `agents/implementer_agent.md` | modify: `write_scope` names the sprint-directory reports, `docs/audits/`, `config/`, `claude/`, `.github/`, `Makefile` and `requirements-core.txt`; `ADR-0009` amended in the same commit (companion, not a second subject); first unit of the sprint, before M-10 (RV-20) | medium | `doc_orchestrator` | sonnet | medium | 3753 | | - | ✅ c83d8b5 |

### Wave Q-01 — Phase 6 parallel batches without worktrees (second unit)

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Q-01 | `workflows/pipeline_workflow.md` | modify: Phase 6 parallel batches without worktrees (batch subagents edit only their unit's files in the shared tree, run only their own tests, do not commit; the orchestrator commits each unit separately in `task_scope.md` order, regenerates generated artifacts and runs `make verify` once per batch); the commit includes the regenerated `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md`; after O-12, before every Wave A unit, M-12 and O-10 (same file) (KI-060-04, RV-42) | medium | `doc_orchestrator` | sonnet | medium | 3753 | | O-12 | ✅ 07be305 |

### Wave S-01 — Skill auditor claim (third unit, before Wave A batch 2)

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| S-01 | `docs/sprints/060-core-pipeline/skill_assignment.md` | modify: the `python-quality-auditor` row stops claiming "the Ruff/Mypy/Bandit gate": it names what is measured (`ruff check` and `scripts/quality_audit.py`) and records A-03 as inconclusive for Mypy, Bandit and Radon (tools absent from `venv_skillopt`); after Q-01, before Wave A batch 2 (KI-060-05) | low | `skill_architect` | sonnet | medium | 2798 | | Q-01 | ✅ f1a0211 |

### Wave A — GitHub App broker

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| A-01 | `docs/decisions/ADR-0025-github-app-broker.md` | create: D1-D6; replaces `ADR-0019` D2 and D6; same commit adds `Superseded by ADR-0025` to the D2 and D6 rows of `ADR-0019` | medium | `doc_orchestrator` | sonnet | medium | 115354 | | - | ✅ 1dac062 |
| A-02 | `docs/architecture/GITHUB_BROKER_BLUEPRINT.md` | create: from `BLUEPRINT_TEMPLATE.md` | low | `doc_orchestrator` | sonnet | medium | 115354 | yes | A-01 | ✅ 800d483 |
| A-03 | `scripts/github_broker.py` | create: stdio MCP server with the D4 operations; companion `tests/test_github_broker.py` in the same commit | high | `implementer_agent` | sonnet | medium | 15109 | | A-01 | ✅ 172c145 |
| A-09 | `docs/guides/GITHUB_BROKER_SETUP_GUIDE.md` | create: human steps (create the App, D4 permissions, install on the nucleus only, keys, `install_broker.py`, `claude mcp add --scope user`; the user-scope registration of the graph server, M-04 and M-18, RV-28) | low | `doc_orchestrator` | sonnet | medium | 115354 | | A-03 | ⏳ pending |
| A-04 | `scripts/install_broker.py` | create: install from a signed tag or a named `main` commit (D5); companion `tests/test_install_broker.py`; its `invoked_by:` is the guide A-09, which exists first | high | `implementer_agent` | sonnet | medium | 15109 | | A-03, A-09 | ⏳ pending |
| A-05 | `claude/settings.hooks.json` | modify: `denyRead` and `permissions.deny` of D3; check `grep -c excludedCommands` = 0 | medium | `implementer_agent` | sonnet | medium | 10101 | | - | ✅ 2f4bfc9 |
| A-06 | `config/allowed_signers` | create: public signing key the human pastes; the agent does not generate it | low | `implementer_agent` | sonnet | medium | 4613 | | - | ✅ 59c2d40 |
| A-07 | `scripts/sync_agents_pin.py` | modify: `git verify-tag` (D6); companion `tests/test_sync_agents_pin.py` | medium | `implementer_agent` | sonnet | medium | 10101 | | A-06 | ⏳ pending |
| A-08 | `scripts/install.py` | modify: `git verify-tag` (D6); companion `tests/test_install.py` | medium | `implementer_agent` | sonnet | medium | 10101 | yes | A-06 | ⏳ pending |
| A-10 | `docs/sprints/060-core-pipeline/BROKER_MEASUREMENT.md` | create: M1 keys unreadable (exit codes only), M2 installed broker not editable, M3 no token in the enumerated set, M4 live D4 rejections | high | `implementer_agent` | sonnet | medium | 115354 | | A-03, A-04, A-05, A-09 | ⏳ pending |
| A-11 | `workflows/deployment_workflow.md` | modify: push, PR, merge, tag and Release through the broker; the commit includes `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` regenerated by `scripts/map_workflows.py` (RV-29) | medium | `doc_orchestrator` | sonnet | medium | 3753 | | A-03 | ⏳ pending |
| A-12 | `agents/devops_agent.md` | modify: GitHub operations run through the broker's MCP tools; keeps `Bash` only, no write authority (`ADR-0009`) | low | `doc_orchestrator` | sonnet | medium | 2798 | | A-11 | ⏳ pending |
| A-13 | `rules/project_topology.md` | modify: `gh`/credential row now names the broker (`KI-059-21`, `-22`, `-24`) | medium | `doc_orchestrator` | sonnet | medium | 7867 | | A-11 | ⏳ pending |
| A-14 | `workflows/repository_hardening_workflow.md` | modify: measured state of `ADR-0019` D7 and the App installation; the commit includes the regenerated `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` (RV-29) | low | `doc_orchestrator` | sonnet | medium | 2798 | yes | - | ⏳ pending |

### Wave S — Skill dependencies declared and fail-closed (KI-060-05)

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| S-02 | `requirements-quality.txt` | modify: pins `mypy`, `bandit`, `radon` and their transitive closure with sha256 hashes for `pip install --require-hashes` (17 packages measured 2026-11-22 with `pip install --dry-run --ignore-installed --report`); regenerates `requirements-core.txt` in the same commit if its closure includes them (companion, not a second subject); after Wave A (KI-060-05) | medium | `skill_architect` | sonnet | medium | 10101 | | A-14 | ⏳ pending |
| S-03 | `skills/python-quality-auditor/scripts/python_quality_auditor.py` | modify (fix): exit other than `0` when a tool is missing or reports findings; accepts file paths; no `shell=True`; runs the current interpreter's tools (`sys.executable -m`); companion `tests/test_python_quality_auditor.py` in the same commit; after S-02 (KI-060-05) | medium | `skill_architect` | sonnet | medium | 10101 | | S-02 | ⏳ pending |
| S-04 | `docs/sprints/060-core-pipeline/SKILL_DEPENDENCY_REPORT.md` | create: for each of the 23 skills with `scripts/`, every dependency (non-stdlib import, executed binary, requirement written in `SKILL.md` or `README.md`) with three measured columns: declared in a `requirements-*.txt`, installed in `venv_skillopt`, script behaviour when it is absent (exit and output); a skill that claims to work without its dependency is a finding; after S-03 (KI-060-05) | medium | `skill_architect` | sonnet | medium | 115354 | | S-03 | ⏳ pending |
| S-05 | `scripts/check_skill_dependencies.py` | create: `make verify` exits `2` when a script of `skills/*/scripts/` imports a module outside the stdlib and its own skill that appears in no `requirements-*.txt`; binaries are outside the claim except what S-04 measures as checkable; companions `tests/test_check_skill_dependencies.py` and `Makefile` in the same commit, and the counted block of `README.md` regenerated by `scripts/check_readme_counts.py --write`; after S-04 (KI-060-05) | medium | `implementer_agent` | sonnet | medium | 33574 | | S-04 | ⏳ pending |

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
| N-01 | `docs/decisions/ADR-0027-session-transcript-read.md` | create: amends the `~/.claude/projects` row of `ADR-0019` (stays in `denyRead`, `allowRead` only for the current project directory); same commit adds `Amended by ADR-0027` to the `~/.claude/projects` row of `ADR-0019` (RV-27) | medium | `doc_orchestrator` | sonnet | medium | 115354 | | A-01 | ⏳ pending |
| N-02 | `claude/settings.hooks.json` | modify: `allowRead` with the `{{PROJECT_TRANSCRIPT_DIR}}` marker (`RA-15`); after A-05 | medium | `implementer_agent` | sonnet | medium | 10101 | | A-05 | ⏳ pending |
| N-03 | `scripts/install.py` | modify: renders the marker with Claude Code's path encoding for nucleus and host; after A-08; companion `tests/test_install.py` | medium | `implementer_agent` | sonnet | medium | 10101 | yes | A-08, N-02 | ⏳ pending |
| N-04 | `docs/sprints/060-core-pipeline/TRANSCRIPT_READ_MEASUREMENT.md` | create: from the sandbox after the human runs `install.py` and opens a new session: `session_cost.py --from-anchor` `measurable: true`, `prompt_count.py` exit `0`; EPERM on the enumerated set (listing of `~/.claude/projects`, one other project's directory, `~/.claude.json`); the claim is limited to that set; exit codes only (D16, `RA-19`, RV-30) | high | `implementer_agent` | sonnet | medium | 115354 | yes | N-03 | ⏳ pending |

### Wave L-04 and O-11 — Sandbox egress before Wave M

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| L-04 | `claude/settings.hooks.json` | modify: `api.osv.dev` in `sandbox.network.allowedDomains` (D13) | low | `implementer_agent` | sonnet | medium | 4613 | | A-05, N-02 | ⏳ pending |
| O-11 | `claude/settings.hooks.json` | modify: `skills.sh` in `sandbox.network.allowedDomains` (human decision 2026-11-22); after L-04, before M-14; recorded afterwards in ADR-0028 (O-01) | low | `implementer_agent` | sonnet | medium | 4613 | | L-04 | ⏳ pending |

### Wave M — Graph as brain (D14)

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| M-01 | `scripts/graph_battery.py` | create: fixed structural query battery against Python AST truth; exit `2` on a differing query or inverted edge; companion `tests/test_graph_battery.py` | high | `implementer_agent` | sonnet | medium | 15109 | | - | ⏳ pending |
| M-02 | `docs/audits/GRAPH_USAGE_AUDIT_REPORT-060.md` | create: baseline with 0.8.30 and after K-01, real consumers, rebuild cost, graph queries versus grep in Phases 1-4 | medium | `implementer_agent` | sonnet | medium | 115354 | | M-01, K-01 | ⏳ pending |
| M-03 | `scripts/graph_query.py` | create: structural queries on `graph.json` with edge-direction correction and transitive closure; companion `tests/test_graph_query.py` | high | `implementer_agent` | sonnet | medium | 15109 | | M-01 | ⏳ pending |
| M-04 | `scripts/graph_mcp.py` | create: read-only stdio MCP server exposing M-03; user-scope install outside writable trees; companion `tests/test_graph_mcp.py` | high | `implementer_agent` | sonnet | medium | 15109 | | M-03, A-04 | ⏳ pending |
| M-18 | `scripts/install_broker.py` | modify: installs `scripts/graph_mcp.py` from a signed tag with the D5 verification; companion `tests/test_install_broker.py`; after A-04 and M-04, before M-05 and M-16: the human's user-scope registration follows M-18 and precedes M-16 (RV-28, RV-35) | medium | `implementer_agent` | sonnet | medium | 10101 | yes | A-04, M-04 | ⏳ pending |
| M-05 | `claude/mcp.json` | modify: removes the project-scope `graphify` entry in favour of the M-04 user registration | medium | `implementer_agent` | sonnet | medium | 10101 | | M-04, M-18 | ⏳ pending |
| M-06 | `rules/graphify.md` | modify: structural-first protocol (symbol or file through M-03/M-04); natural-language CLI mode not used | medium | `doc_orchestrator` | sonnet | medium | 7867 | | K-01, M-03, M-04 | ⏳ pending |
| M-07 | `agents/principal_agent.md` | modify: Phase 1 impact by `impact`/`dependents` before drafting Work | low | `doc_orchestrator` | sonnet | medium | 2798 | | M-06 | ⏳ pending |
| M-08 | `agents/rule_validator.md` | modify: Phase 4.3 dependent files by `dependents` instead of Grep | low | `doc_orchestrator` | sonnet | medium | 2798 | | M-06 | ⏳ pending |
| M-09 | `agents/qa_agent.md` | modify: Gate 1 graph integrity with `graph_battery.py` and the diff's impact radius | low | `doc_orchestrator` | sonnet | medium | 2798 | | M-06 | ⏳ pending |
| M-10 | `agents/implementer_agent.md` | modify: `callers`/`callees` before editing a symbol; cites `rules/qa_and_testing.md` and `rules/code_craft.md`; after O-12 (same file) (RV-31) | low | `doc_orchestrator` | sonnet | medium | 2798 | | M-06, O-12 | ⏳ pending |
| M-11 | `agents/doc_orchestrator.md` | modify: references of a document by `dependents` before editing or renaming; cites `rules/documentation_standard.md` (RV-31) | low | `doc_orchestrator` | sonnet | medium | 2798 | | M-06 | ⏳ pending |
| M-12 | `workflows/pipeline_workflow.md` | modify: graph query steps in Phases 1, 4.3, 6 and 7; the commit includes the regenerated `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` (RV-29) | medium | `doc_orchestrator` | sonnet | medium | 3753 | | M-06, Q-01 | ⏳ pending |
| M-13 | `hooks/graph_usage_log.py` | create: `PostToolUse` hook logging graph queries against `Grep`, `Glob` and search by `Bash`; companion `tests/test_graph_usage_log.py` | medium | `implementer_agent` | sonnet | medium | 33574 | | - | ⏳ pending |
| M-14 | `claude/settings.hooks.json` | modify: registers the M-13 hook; after A-05, N-02, L-04 and O-11 | low | `implementer_agent` | sonnet | medium | 4613 | | M-13, O-11 | ⏳ pending |
| M-15 | `scripts/check_graph_usage.py` | create: exit `2` if a research phase searched by text before querying the graph; named invoker `workflows/close_workflow.md` (finding RV-19); companion `tests/test_check_graph_usage.py` | medium | `implementer_agent` | sonnet | medium | 33574 | | M-13 | ⏳ pending |
| M-16 | `docs/sprints/060-core-pipeline/GRAPH_AB_MEASUREMENT.md` | create: A/B with and without the graph on the same research tasks; `fresh` tokens by `session_cost.py` (finding RV-24 on who runs it); threshold >= 30 %; after M-18 and the human's user-scope registration of the graph server (RV-35) | high | `implementer_agent` | sonnet | medium | 115354 | | M-04, M-18, N-04 | ⏳ pending |
| M-17 | `workflows/close_workflow.md` | modify: step that runs `scripts/check_graph_usage.py`, the invoker of M-15 (RV-19); the commit includes the regenerated `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` (RV-29) | low | `doc_orchestrator` | sonnet | medium | 2798 | yes | M-15 | ⏳ pending |

### Wave O — Forge trigger and capability evaluation (D17)

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| O-01 | `docs/decisions/ADR-0028-forge-trigger.md` | create: D17 candidate criterion, `forge`/`reuse` decision with evidence, A/B threshold; records the `skills.sh` egress (O-11); same commit adds `Amended by ADR-0028` to `ADR-0024` (RV-27) | medium | `doc_orchestrator` | sonnet | medium | 115354 | | - | ⏳ pending |
| O-03 | `agents/agent_orchestrator.md` | modify: `agent_creation` defines "suitable" with the D17 criterion and requires the `Candidates` table | low | `doc_orchestrator` | sonnet | medium | 2798 | | O-01 | ⏳ pending |
| O-04 | `agents/skill_architect.md` | modify: `skill_search` starts from the D17 candidates and records each decision; P3 runs `curl` through Bash against `allowedDomains` and `tools:` drops `WebSearch, WebFetch`, which `permissions.deny` removes (RV-16, KI-060-01) | low | `doc_orchestrator` | sonnet | medium | 2798 | | O-01 | ⏳ pending |
| O-05 | `docs/standards/templates/AGENT_ASSIGNMENT_TEMPLATE.md` | modify: `Candidates` table (candidate, units, criterion a/b, evidence, decision, reason) | low | `doc_orchestrator` | sonnet | medium | 2798 | | O-01 | ⏳ pending |
| O-06 | `docs/standards/templates/SKILL_ASSIGNMENT_TEMPLATE.md` | modify: the same `Candidates` table | low | `doc_orchestrator` | sonnet | medium | 2798 | | O-01 | ⏳ pending |
| O-07 | `scripts/check_forge_ladder.py` | modify: exit `2` without a `Candidates` table or with a candidate lacking evidence or decision (sprint >= 60); companion `tests/test_check_forge_ladder.py::test_missing_candidates_table_fails`; the positive control is a fixture sprint directory in the test, not `docs/sprints/059-core-pipeline` (finding RV-21) | medium | `implementer_agent` | sonnet | medium | 10101 | | O-05, O-06 | ⏳ pending |
| O-08 | `scripts/capability_usage.py` | create: invocations per profile (`Agent` `subagent_type`) and per skill (`Skill`) from project transcripts and prior assignments; after N-04; docstring `invoked_by:` (finding RV-18); companion `tests/test_capability_usage.py` | medium | `implementer_agent` | sonnet | medium | 33574 | yes | N-04 | ⏳ pending |
| O-10 | `workflows/pipeline_workflow.md` | modify: Phases 4.1 and 4.2 done-criterion, `Candidates` table with `capability_usage.py` as evidence; after M-12; the commit includes the regenerated `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` (RV-29) | medium | `doc_orchestrator` | sonnet | medium | 3753 | | M-12, O-08 | ⏳ pending |

### Wave L — Dependency advisories

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| L-01 | `scripts/check_dependency_advisories.py` | create: OSV `/v1/querybatch` (stdlib) per `requirements*.txt` pin, exit `2` on advisory or no network (D13); companion `tests/test_check_dependency_advisories.py` | medium | `implementer_agent` | sonnet | medium | 33574 | | K-01 | ⏳ pending |
| L-02 | `.github/workflows/ci.yml` | modify: L-01 on every PR and a daily cron on `main` | medium | `implementer_agent` | sonnet | medium | 10101 | | L-01 | ⏳ pending |
| L-03 | `scripts/session_start.py` | modify: boot shows L-01 as a warning in nucleus and host (D13); companion `tests/test_session_start.py` | medium | `implementer_agent` | sonnet | medium | 10101 | | L-01, A-07 | ⏳ pending |
| L-05 | `docs/decisions/ADR-0026-dependency-advisory-check.md` | create: D13 and the egress widening; same commit adds `Amended by ADR-0026` to `ADR-0024` | low | `doc_orchestrator` | sonnet | medium | 115354 | | L-01, L-04 | ⏳ pending |
| L-06 | `.github/dependabot.yml` | create: only if the alert #28 message shows the missing `pip` config blocked the PR; otherwise the row closes with the transcribed message (D13) | low | `implementer_agent` | sonnet | medium | 4613 | yes | - | ⏳ pending |

### Wave C — Ledger seal

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| C-01 | `workflows/deployment_workflow.md` | modify: `ledger_seal` on `ai-sprint/[ID]` (D7, `KI-059-35`); the commit includes the regenerated `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` (RV-29) | medium | `doc_orchestrator` | sonnet | medium | 3753 | | A-11 | ⏳ pending |

### Wave D — Host-term scanner

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| D-01 | `scripts/check_host_terms.py` | create: hash scanner (D9); companion `tests/test_check_host_terms.py` | medium | `implementer_agent` | sonnet | medium | 33574 | | - | ⏳ pending |
| D-02 | `config/host_term_hashes.json` | create: hashes the human generates and pastes; the agent does not fabricate them | low | `implementer_agent` | sonnet | medium | 4613 | | - | ⏳ pending |
| D-03 | `tests/test_profile_references.py` | modify: use `check_host_terms.py` (`KI-059-14`) | low | `implementer_agent` | sonnet | medium | 4717 | | D-01 | ⏳ pending |
| D-04 | `docs/sprints/060-core-pipeline/HISTORY_REVIEW_REPORT.md` | create: scan of `origin/main`, SHA, path and line only, never the matched text; rewriting history stays a human decision (`KI-059-12`) | medium | `implementer_agent` | sonnet | medium | 115354 | | D-01, D-02 | ⏳ pending |
| D-05 | `Makefile` | modify: `verify` invokes `scripts/check_host_terms.py` (`RA-16`) | low | `implementer_agent` | sonnet | medium | 4613 | | D-01 | ⏳ pending |

### Wave E and P — Gate log and task_scope check

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| E-01 | `scripts/check_gate_log.py` | modify (fix): one Gate findings row per S0-S2 finding; companion `tests/test_check_gate_log.py::test_s0_s2_finding_without_row_fails` | medium | `implementer_agent` | sonnet | medium | 10101 | | - | ⏳ pending |
| P-01 | `scripts/check_task_scope.py` | modify (fix): from sprint 60 exit `2` when a plan Work id is missing from `task_scope.md` or the reverse; companion `tests/test_check_task_scope.py::test_plan_row_missing_fails` (RV-17, KI-060-02) | medium | `implementer_agent` | sonnet | medium | 10101 | | - | ⏳ pending |

### Wave F — Normative text

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| F-01 | `agents.md` | modify: trim under 20000 bytes; `mass-standardizer` wording (`KI-059-32`); `RA-09` and `§6 devops_agent` name the broker | high | `rule_validator` | sonnet | medium | 49477 | | A-12 | ⏳ pending |
| F-02 | `rules/skills_and_integrations.md` | modify: `mass-standardizer` wording (`KI-059-32`) | low | `rule_validator` | sonnet | medium | 4037 | yes | - | ⏳ pending |
| O-02 | `rules/skills_and_integrations.md` | modify: §1 the ladder opens per D17 candidate, not only for functions outside the stdlib; after F-02 | medium | `rule_validator` | sonnet | medium | 7867 | | F-02, O-01 | ⏳ pending |

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

### Wave O-09 — Capability evaluation report

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| O-09 | `docs/audits/CAPABILITY_EVALUATION_REPORT-060.md` | create: usage (O-08), overlaps and gaps of the 14 profiles and 34 skills; D17 candidates with an A/B by `session_cost.py` on the executed units A-10, N-04, H-01 (A-15 runs at the deployment and is out, RV-25); records evidence only, the `forge`/`reuse` decision is written by `agent_orchestrator` and `skill_architect` (RV-20; but see RV-37); after O-12 and H-01 | high | `implementer_agent` | sonnet | medium | 115354 | yes | O-07, O-08, M-03, O-12, H-01 | ⏳ pending |

### Wave O-13 — Agent candidate decisions

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| O-13 | `docs/sprints/060-core-pipeline/agent_assignment.md` | modify: `forge`/`reuse` decision per agent candidate from the O-09 evidence; a `forge` candidate enters as a re-plan row `O-NN` with its `Destination`; the `claude/settings.hooks.json` decision is reconciled with O-14 (RV-37, RV-39) | low | `agent_orchestrator` | sonnet | medium | 2798 | | O-09 | ⏳ pending |

### Wave O-14 — Skill candidate decisions

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| O-14 | `docs/sprints/060-core-pipeline/skill_assignment.md` | modify: `forge`/`none` decision per skill candidate from the O-09 evidence; a `forge` candidate enters as a re-plan row `O-NN` with its `Destination`; reconciled with O-13 (RV-37, RV-39) | low | `skill_architect` | sonnet | medium | 2798 | | O-09, O-13 | ⏳ pending |

### Wave Z — Pipeline and closeout artifacts

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Z-01 | `docs/sprints/060-core-pipeline/SPRINT_LOG.md` | create: Phase 3 | low | `orchestrator` | sonnet | medium | 115354 | | - | ⏳ pending |
| Z-02 | `docs/sprints/060-core-pipeline/task_scope.md` | create: Phase 4.3; created before Phase 5, not re-run in Phase 6 | low | `rule_validator` | sonnet | medium | 115354 | yes | - | ⏳ pending |
| Z-03 | `docs/sprints/060-core-pipeline/agent_assignment.md` | create: Phase 4.1; created before Phase 5, not re-run in Phase 6; O-13 is its only later modification | low | `agent_orchestrator` | sonnet | medium | 115354 | | - | ⏳ pending |
| Z-07 | `docs/sprints/060-core-pipeline/skill_assignment.md` | create: Phase 4.2; created before Phase 5, not re-run in Phase 6; O-14 is its only later modification | low | `skill_architect` | sonnet | medium | 115354 | | - | ⏳ pending |
| Z-05 | `CHANGELOG.md` | modify: `[Unreleased]` | low | `doc_orchestrator` | sonnet | medium | 2798 | | - | ⏳ pending |
| Z-06 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify: KI routed to closed | low | `orchestrator` | sonnet | medium | 2798 | | - | ⏳ pending |

### Deployment-time unit (after Phase 8)

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| A-15 | `docs/sprints/060-core-pipeline/BROKER_MEASUREMENT.md` | modify: M5 at the 060 deployment (push, PR, merge, signed tag, Release by the agent, each GitHub ID recorded); gates read M1-M4 (RV-7) | high | `implementer_agent` | sonnet | medium | 3753 | | A-10, A-11 | ⏳ pending |

## Same-file ordering (`jurisdictional_lock`, `no_interference`)

97 rows; every `File` cell is distinct except the eleven files below. No two rows are `in progress` at once: the plan executes sequentially (`agent_assignment.md` Mode column), and each chain is ordered by `Depends on`.

| File | Rows in order | Order recorded |
| :--- | :--- | :--- |
| `claude/settings.hooks.json` | A-05, N-02, L-04, O-11, M-14 | N-02 after A-05; L-04 after A-05 and N-02; O-11 after L-04; M-14 after O-11 (plan rows A-05/N-02/M-14/O-11). The plan's execution-order line (`241fc29`) runs L-04 and O-11 before Wave M, then M-14 in Wave M (RV-26 closed); L-04 and O-11 share one table, M-14 sits in Wave M |
| `scripts/install.py` | A-08, N-03 | N-03 `Depends on` A-08, N-02; companion `tests/test_install.py` reached by both in that order |
| `workflows/pipeline_workflow.md` | Q-01, M-12, O-10 | M-12 `Depends on` Q-01; O-10 `Depends on` M-12; Q-01 is the second unit of the sprint, after O-12 (RV-42) |
| `rules/skills_and_integrations.md` | F-02, O-02 | O-02 `Depends on` F-02; the plan's order line puts O-02 after F, so O-02 sits in the Wave F table |
| `agents/implementer_agent.md` | O-12, M-10 | M-10 `Depends on` O-12; O-12 is the first unit of the sprint (RV-20, RV-31); `ADR-0009` is a companion of O-12 |
| `scripts/install_broker.py` | A-04, M-18 | M-18 `Depends on` A-04 and M-04; companion `tests/test_install_broker.py` reached by both in that order (RV-28) |
| `docs/sprints/060-core-pipeline/agent_assignment.md` | O-13, Z-03 | Z-03 is a Phase 4.1 `create` done before Phase 5 (`4cb4570`) and not re-run in Phase 6 (plan line 171); O-13 is its only later modification, so no `Depends on` (the earlier Z-03 `Depends on` O-13 was dropped: it would order a create after the modify; `check_task_scope.py` does not require a dependency between rows sharing a file) (RV-40) |
| `docs/sprints/060-core-pipeline/skill_assignment.md` | Z-07, S-01, O-14 | Z-07 is a Phase 4.2 `create` done before Phase 5, not re-run in Phase 6 (plan line 172); S-01 is its third unit of the sprint (`Depends on` Q-01, table Wave S-01, before Wave A batch 2) and edits one row (`python-quality-auditor`); O-14 edits it last, in a later table, so the order S-01 then O-14 is the table barrier and no `Depends on` is added to O-14 (RV-41) |
| `workflows/deployment_workflow.md` | A-11, C-01 | C-01 `Depends on` A-11; C-01 rewrites the merge/seal sequence A-11 wrote |
| `rules/project_topology.md` | A-13, H-02 | H-02 `Depends on` A-13 and H-01; disjoint rows |
| `docs/sprints/060-core-pipeline/BROKER_MEASUREMENT.md` | A-10, A-15 | A-15 `Depends on` A-10 and is the last table: M5 is written at the deployment |

Companion edits that cross rows (not structural subjects): `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` (generated; regenerated by A-11, A-14, M-12, M-17, C-01, O-10 in that order, RV-29), `docs/decisions/ADR-0024-*` (`Amended by` by O-01, then L-05), `docs/decisions/ADR-0009-implementer-role.md` (O-12), `docs/decisions/ADR-0019-*` (A-01 `Superseded by`, N-01 amendment; A-01 first), `rules/graphify.md` (K-01 figures, then M-06), `tests/test_template_sandbox.py`, `tests/test_install_nucleus_sandbox.py`, `tests/test_merge_json.py` and `tests/test_mcp_template.py` (assert the settings and MCP templates; A-05, N-02, L-04, O-11, M-14, M-05 reach them in chain order), `tests/test_session_start.py` (A-07 new exit `2`, then L-03), `requirements-core.txt` (S-02 only if the closure of the new quality pins is not already carried by `-r requirements-quality.txt` at its line 474; K-01, a later table, is its subject and regenerates it afterwards), `tests/test_python_quality_auditor.py` (S-03, paired test of a `fix(` commit), `tests/test_check_skill_dependencies.py` (S-05), `Makefile` `verify` (S-05 adds the invocation, RA-16; D-05, a later table, is its subject), `README.md` counted block (S-05, `python3 scripts/check_readme_counts.py --write`). `agents/implementer_agent.md` (O-12, M-10) and `agents/doc_orchestrator.md` (M-11) are the profiles of the assignees of other rows: they are edited as subjects only by those rows, one subject each.

## Dependent files (graphify and reference graph)

`graphify-out/graph.json` exists; this dispatch had no shell, so it was queried only with `Grep` (1048 nodes carry a `source_file` of `scripts/check_task_scope.py`, `check_forge_ladder.py`, `install.py` or `install_broker.py`), not by a `python3` traversal or a `scripts/` graph helper. `scripts/graph_query.py` does not exist yet (M-03). Importers and mentions below come from `Grep` over `scripts/ hooks/ tests/ workflows/ rules/ agents/ config/ Makefile`, so they are measured but not a graph traversal.

| Unit | Dependent files the unit will touch or must re-check |
| :--- | :--- |
| A-05, N-02, L-04, O-11, M-14 | `tests/test_template_sandbox.py`, `tests/test_install_nucleus_sandbox.py`, `tests/test_merge_json.py`; consumers `scripts/install.py`, `scripts/merge_json.py`, `scripts/with_env.py`, `scripts/session_end_hook.py`, `hooks/on_init.py`, `hooks/on_commit.py`, `hooks/state_mirror.py`; `permissions.deny` lines 23-24 hold `WebFetch` and `WebSearch` (RV-16) |
| A-07 | `scripts/session_start.py` (calls it at lines 19, 453, 681; must handle exit `2`), `scripts/_root.py:58`, `scripts/_mode.py:37`, `workflows/start_workflow.md:32`, `workflows/close_workflow.md:35` |
| A-08, N-03 | `scripts/install_lock.py`, `scripts/merge_json.py`, `scripts/_mode.py`; `rules/project_topology.md` and `workflows/repository_hardening_workflow.md` cite `ADR-0019` D2/D6 |
| S-01 | `docs/sprints/060-core-pipeline/skill_assignment.md` (the `python-quality-auditor` rows, and the S-05 row that names the same skill); `scripts/check_forge_ladder.py` reads the file (`docs/sprints/*/skill_assignment.md`; O-07 keeps it passing) |
| S-02 | `requirements-core.txt:474` (`-r requirements-quality.txt`), `.github/workflows/ci.yml:33` (`pip install -q --require-hashes -r requirements-test.txt -r requirements-quality.txt`), `scripts/install_lock.py` (hashes the core set and its includes, so hosts re-install on the next boot), `README.md:91`, `Makefile:23` (comment naming the pins), `scripts/quality_audit.py:68,423`, `tests/test_quality_audit.py:897-909`, `rules/code_craft.md:116,127,129` (cite only ruff and tree-sitter pins) |
| S-03 | `config/invocation_exceptions.json:53` (`skills/python-quality-auditor`), `skills/python-quality-auditor/SKILL.md` and `README.md` (state the audit; edited only if the exit contract they describe changes), the callers of `python_quality_auditor.py` in `skill_assignment.md` rows A-03, A-04, A-07, A-08, B-01, M-01, M-03, M-04, M-13, M-15 |
| S-05 | `scripts/check_readme_counts.py` (counts top-level `scripts/*.py`; its `invoked_by:` names the Makefile `verify` target), `Makefile:86`, `scripts/verify_references.py` check `(d)` (the `invoked_by:` line), `skills/skill-creator/scripts/quick_validate.py:7` (`import yaml`, distribution `PyYAML` pinned in `requirements-skillopt.txt:1480`), `tests/test_install_lock.py` |
| Q-01 | `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` (generated; `python3 scripts/map_workflows.py`, checked by `make verify`), `scripts/check_task_scope.py --batches` (the command Phase 6 step 1 names), `scripts/session_cost.py` and `scripts/unit_cost.py` (named by the same Phase 6 row), `scripts/branch_sovereignty.py` (KI-060-04: refuses the seal after a worktree) |
| O-12 | `docs/decisions/ADR-0009-implementer-role.md` (companion), `tests/test_implementer_role.py` (pins the `tools:` line, not `write_scope`; re-run), `agents/implementer_agent.md` read by `config/model_tiers.json` checks and `scripts/check_task_scope.py` tool check (Grep, not a graph traversal) |
| P-01 | `tests/test_check_task_scope.py` (companion), importers by `Grep`: `scripts/loop_guard.py`, `scripts/unit_cost.py`, `scripts/check_sprint_refs.py`, `scripts/check_gate_log.py`, `scripts/_current_sprint.py`, `scripts/_md_table.py`, `scripts/model_ledger.py`, `scripts/audit_cursor_era.py`; invoker `workflows/pipeline_workflow.md` Phase 4.3 and `workflows/close_workflow.md` |
| M-17 | `scripts/check_graph_usage.py` (M-15, the invoker's target), `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` (generated, `scripts/map_workflows.py --check` in `make verify`), `scripts/session_state.py`, `tests/test_session_protocol.py` |
| M-18 | `scripts/install_broker.py` (A-04), `tests/test_install_broker.py`, `scripts/graph_mcp.py` (M-04), `docs/guides/GITHUB_BROKER_SETUP_GUIDE.md` (A-09 registration step) |
| O-13, O-14 | `scripts/check_forge_ladder.py` and `tests/test_check_forge_ladder.py` (O-07: a `Candidates` table without evidence or decision exits `2`; both edits must keep it passing), `docs/standards/templates/AGENT_ASSIGNMENT_TEMPLATE.md`, `SKILL_ASSIGNMENT_TEMPLATE.md` (O-05, O-06), `config/template_gates.json:75`, `scripts/capability_usage.py` (O-08 reads both files) |
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
| RV-10 | A-01 and L-05 rows add the `Superseded by` / `Amended by` line; N-01 and O-01 repeated the defect (RV-27), closed by `241fc29` N-01, O-01 | resolved |
| RV-11 | A-12 row words the broker as MCP tools with `Bash` only and cites `ADR-0009`; F-01's row (`RA-09`/`§6 devops_agent` "con el broker") has no such wording | resolved for A-12, open for F-01 (S3) |
| RV-12 | D15 deletes Z-04; `ls docs/walkthroughs` stays absent | resolved |
| RV-13 | `Work units` was 90 when raised (now 91, `bdecc1a`) and `agent_assignment.md` said 90; the Cost row "Subagents dispatched" = "45 + gates" (plan line 218) contradicts "una dispatch por unidad" with 90 units; `241fc29` edited the Cost row (Work units, Prior session ratio) and left it | open (S3) |
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

### Round 2 — status of RV-16 to RV-31 (diff `62e8089..2aa9a32`)

Each status was read from the plan at `2aa9a32` (rows and Mechanisms/Tests tables) and, for RV-22 and RV-23, from `skill_assignment.md` and `agent_assignment.md`. No shell: statuses come from `Grep` and `Read`, not from running `check_task_scope.py`.

| ID | Status | Evidence |
| :--- | :--- | :--- |
| RV-16 | closed by `241fc29` O-04 | O-04 row: P3 by `curl` through Bash against `allowedDomains`, `tools:` drops `WebSearch, WebFetch`; no widening of `permissions.deny`. Residual `agents/git_sync_agent.md:4` `WebFetch`: RV-38 (S3) |
| RV-17 | closed by `241fc29` P-01 | P-01 row, Tests row 232 and Mechanisms row 203 name the exit `2`, the test and the invoker |
| RV-18 | closed by `241fc29` O-08 | O-08 row: docstring declares `invoked_by:` |
| RV-19 | closed by `241fc29` M-17 | M-17 row and Mechanisms rows 198-202 (graph_battery, graph_query, graph_mcp, hook, check_graph_usage) |
| RV-20 | closed by `241fc29` O-12, O-09 | O-12 widens `write_scope` to every non-`scripts/` path an `implementer_agent` row writes; O-09 records evidence only. The decision step has no unit: RV-37 |
| RV-21 | closed by `241fc29` O-07 | O-07 row and Tests row 231: control is a fixture directory, no 059 expectation |
| RV-22 | closed by `2aa9a32` `skill_assignment.md` C4, C5, C6 | decision `none` with the nearest skill named |
| RV-23 | closed by `2aa9a32` | C6 and the agent candidate both count 5 units (A-05, N-02, L-04, O-11, M-14); decisions differ by candidate class (agent `forge-pending-O-09`, skill `none`), recorded as RV-39 (S3) |
| RV-24 | closed by `241fc29` M-16, G-02, Cost | D16 wording in the three rows; `agent_assignment.md` line 238 and `skill_assignment.md` line 86 say the agent runs `session_cost.py` under the sandbox |
| RV-25 | closed by `241fc29` O-09 | O-09 limited to A-10, N-04, H-01 and depends on H-01; table moved after J |
| RV-26 | closed by `241fc29` plan line 80 | order line `L-04 -> O-11 -> M`, O-02 after F; this file re-tabled to match |
| RV-27 | closed by `241fc29` N-01, O-01 | both rows add `Amended by` |
| RV-28 | closed in part by `241fc29` M-18, A-09 | M-18 and the A-09 registration step exist; their order defeats M-04's installation: RV-35 (S2) |
| RV-29 | closed by `241fc29` A-11, A-14, C-01, M-12, O-10, M-17 | each row states the commit includes the regenerated guide |
| RV-30 | closed by `241fc29` N-04 | enumerated set and its limit stated in the row |
| RV-31 | closed by `241fc29` M-10, M-11 | rows cite `rules/qa_and_testing.md`, `rules/code_craft.md` and `rules/documentation_standard.md` |

RV-32, RV-33 and RV-34 are unchanged by the diff and stay open (S3).

### Round 2 — new findings (RV-35 onward)

| ID | Unit | Rule | Finding and reproducing command | Proposed fix | Severity |
| :--- | :--- | :--- | :--- | :--- | :--- |
| RV-35 | M-04, M-16, M-18 | `RA-14`, `jurisdictional_lock` | M-04 says the user-scope install of `graph_mcp.py` goes through `install_broker.py`, but the code that installs it is M-18, and the plan lists M-18 after M-16 (rows 121-123). The human suspension that installs the server (after M-04) and the A/B of M-16 (needs the registered server) both precede M-18, so neither can run. `grep -nE '^\| M-(04\|16\|18) ' IMPLEMENTATION_PLAN.md` gives lines 109, 121, 123; `grep -c graph_mcp` in A-04's row = 0 | Move M-18 directly after M-04 and put the segment suspension at M-18; add M-18 to the `Depends on` of M-16 | S2 |
| RV-36 | A-09, M-18 | `RA-14` | A-09 (Wave A) already documents the graph registration step "M-04, M-18" before M-04 and M-18 exist, so the guide fixes an installer interface that A-04 and M-18 define later. `grep -n 'M-18' IMPLEMENTATION_PLAN.md` line 87 | M-18 row: the same commit re-reads and amends the guide step | S3 |
| RV-37 | O-09, `agent_assignment.md`, `skill_assignment.md` | memory rule "every decision needs a unit", D17 | O-09 records evidence and says the `forge`/`reuse` decision is written by `agent_orchestrator` and `skill_architect` "afterwards" in both assignment files (`agent_assignment.md` line 217, `skill_assignment.md` C1, C2 `forge-pending-O-09`). No Work row modifies either file after Z-03 creates it, and none forges a skill or agent if the outcome is `forge`. `grep -nE '^\| [A-Z]-[0-9]{2} \|.*(agent_assignment\|skill_assignment)' IMPLEMENTATION_PLAN.md` returns Z-03 only | Add one-line rows for the two decisions (and, if `forge`, for the artifact), or state in O-09 that a `forge` decision becomes a roadmap entry in Z-06 | S2 |
| RV-38 | O-04 | `RA-14` | `agents/git_sync_agent.md:4` declares `WebFetch`, which `permissions.deny` removes; O-04 fixes only `skill_architect`. `grep -n WebFetch agents/git_sync_agent.md claude/settings.hooks.json` | One row dropping `WebFetch` from `git_sync_agent` `tools:` or a stated reason it stays | S3 |
| RV-39 | `agent_assignment.md`, `skill_assignment.md` C6 | `RA-14` | The same subject `claude/settings.hooks.json` is `forge-pending-O-09` as an agent candidate and `none` as a skill candidate; both can be correct but no sentence reconciles them. `grep -n 'settings.hooks.json' agent_assignment.md skill_assignment.md` | One sentence in each file naming the other's decision | S3 |

### Round 3 — status of RV-35, RV-37, RV-39 (diff `225d85d..e8d83a2`)

Statuses read from the plan at `e8d83a2` (rows 123, 121, 136, 137, order line 80) and from `agent_assignment.md` lines 113-116 and `skill_assignment.md` lines 117-118, 173.

| ID | Status | Evidence |
| :--- | :--- | :--- |
| RV-35 | closed by `9ae34dd` M-18, M-16 | Plan row 123 puts M-18 before M-05 and M-16 and the human's registration between M-18 and M-16; M-16 row (121) says it follows both. This file moved M-18 after M-04, suspension from M-04 to M-18 (segment 180008) and added M-18 to `Depends on` of M-05 and M-16; M-17 now carries the second `Suspend after` (225624) |
| RV-37 | closed by `9ae34dd` O-13, O-14 | One row per decision file after O-09, each with the re-plan row rule for `forge` (plan line 175). Residual conflict with `Z-03`: RV-40 (S2) |
| RV-39 | closed by `e8d83a2` | `agent_assignment.md` line 116 and `skill_assignment.md` line 173 each name the other file's decision as reconciled at O-13/O-14 on `claude/settings.hooks.json` |
| RV-34 | open (S3) | Its proposed fix named a row `O-13`, an id now taken by `9ae34dd`; read it as a new unit with a new id |

### Round 3 — new findings (RV-40 onward)

| ID | Unit | Rule | Finding and reproducing command | Proposed fix | Severity |
| :--- | :--- | :--- | :--- | :--- | :--- |
| RV-40 | O-13, Z-03 | `jurisdictional_lock`, `RA-14` | Z-03 claims `agent_assignment.md` as `create`, and it runs after O-13, which modifies the same file; a re-run of `create` discards the O-13 decisions. The file already exists since Phase 4.1. `grep -nE '^\| (O-13\|Z-03) ' IMPLEMENTATION_PLAN.md` gives lines 136 and 171, Z-03 `create`, no dependency | Change Z-03 to `modify: stamp status only` with `Depends on` O-13 (done in this file), and amend the plan row | S2 |
| RV-41 | O-14 | `jurisdictional_lock`, artifact ownership | `skill_assignment.md` is modified by O-14 but no Work row creates it (Phase 4.2 artifact); O-13 and O-14 edit Phase 4.1/4.2 artifacts after the Phase 5 approval, so the staffing the human approved changes. Owners match (`agent_orchestrator`, `skill_architect`), so no ownership conflict. `grep -nE '^\| [A-Z]-[0-9]{2} \|.*skill_assignment' IMPLEMENTATION_PLAN.md` returns O-14 only | State in O-13/O-14 that a changed decision is re-submitted at the Approval Gate; or no finding if the plan's re-plan rule already covers it | S3 |

### Round 4 — closure (diff `bdecc1a~1..613f795`, rows Z-01, Z-02, Z-03, Z-07)

| ID | Status | Evidence |
| :--- | :--- | :--- |
| RV-40 | closed by `bdecc1a` Z-03 | Plan lines 169-171 say Z-01, Z-02, Z-03 were created before Phase 5 and are not re-run in Phase 6; Z-03 names O-13 as its only later modification. `grep -nE '^\| Z-0[123] ' IMPLEMENTATION_PLAN.md` |
| RV-41 | closed by `bdecc1a` Z-07 | Plan line 172 adds Z-07 (`skill_assignment.md`, Phase 4.2, O-14 its only later modification); `grep -cE '^\| [A-Z]-[0-9]{2} \|' IMPLEMENTATION_PLAN.md` = 91 and `Work units` = 91 |

### Round 5 — Q-01 (diff `613f795..b9e5336`)

| ID | Severity | Rule | Row | Finding and reproducing command | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| RV-42 | S3 | `unambiguous_action`, `RA-08`, `RA-14` | Q-01 | Phase 6 step (4) says generated artifacts are regenerated "in the commit of the unit that caused them", but step (3) already committed each unit; the text does not say whether that means amending or a later commit, and an amend rewrites the SHA stamped in `task_scope.md`. Q-01 should state: the regenerating unit's commit is made after step (4), or a separate `chore` commit. `grep -n 'in the commit of the unit that caused them' workflows/pipeline_workflow.md` | closed by the Q-01 commit: step (3) regenerates before each unit commit, amend PROHIBITED (`RA-08`) |

No other finding against Q-01: one structural subject (`jurisdictional_lock`; the guide is a generated companion); no commit on `main` (`RA-12`); atomic per-unit commits (`RA-08`); `make verify` and the commit are separate steps (`RA-13`); the `KI-059-16` base check is superseded by the prohibition of `isolation: "worktree"` (`KI-060-04`). Q-01 is `Depends on` O-12; M-12 now `Depends on` Q-01; Wave A rows follow by table barrier. Q-01 is `modify/doc` 3753; the A-02 segment was 238214 (margin 4234). Counts in this file were 92 at that round.

No new finding against the size of O-12: its `Model`/`Effort` are the `doc_orchestrator` map entry, and no Work row is assigned to a `mechanical` profile.

No finding against `RA-16` for `check_dependency_advisories.py` (invokers rows L-02, L-03), `detect_new_models.py`, `check_gate_log.py`. O-09's change of assignee to `implementer_agent` conflicts with `write_scope` and the decision jurisdiction (RV-20); it does not conflict with `code_unit_assignee` (that rule covers `scripts/`, `hooks/`, `tests/`). No finding against `RA-09` for A-09, nor for F-01, F-02, J-02 (`rule_validator` holds `Write`/`Edit`).

### Round 6 — S-01..S-05 (diff `e2b6c77..1ba05b2`)

Severity follows `RA-17`. Read from the plan at `9e861b3` (rows S-01..S-05, order line 80), `agent_assignment.md` Wave S and `skill_assignment.md` Wave S (`1ba05b2`), `config/unit_cost_estimates.json`, `requirements-core.txt`, `requirements-quality.txt`, `Makefile`, `README.md`, `agents/implementer_agent.md` and `agents/skill_architect.md`. No shell in this dispatch: findings come from `Grep` and `Read`.

| ID | Severity | Rule | Row | Finding and reproducing command | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| RV-43 | S3 | `unambiguous_action`, same class as RV-8 | S-03 | The row names `tests/test_python_quality_auditor.py` but no `::<test>` id, while its three fix criteria (exit other than `0` on a missing tool, on findings, file-path arguments) each need a reproducing test for `scripts/check_fix_reproduces.py --range <base>..HEAD`; B-01, E-01, G-01, G-02, O-07 and P-01 name one. `grep -nE '^\| S-03 ' docs/sprints/060-core-pipeline/IMPLEMENTATION_PLAN.md` shows no `::`; `ls tests/test_python_quality_auditor.py` fails (the file is new) | open; one-line plan edit: name `tests/test_python_quality_auditor.py::test_missing_tool_exits_nonzero` or `Repro: manual` |
| RV-44 | S3 | `unambiguous_action`, `fail_closed_claims` | S-05 | The row states its subset honestly (imports, binaries excluded), but the done-criterion "imports a module that appears in no `requirements-*.txt`" compares an import name with a distribution name and the row gives no mapping: `skills/skill-creator/scripts/quick_validate.py:7` is `import yaml` while the pin is `PyYAML==6.0.3` (`requirements-skillopt.txt:1480`); `tree_sitter` is `tree-sitter`. It also does not say whether a conditional or function-level import and `importlib` use are in scope, nor what happens when no `requirements-*.txt` exists (the claim must exit non-zero then). `grep -nE '^\s*import yaml' skills/skill-creator/scripts/quick_validate.py`; `grep -n '^PyYAML==' requirements-skillopt.txt` | open; S-04 measures the first real mapping cases and precedes S-05, so the script can take the alias table from the report |
| RV-45 | S3 | `unambiguous_action` | S-02 | "regenerates `requirements-core.txt` in the same commit if its closure includes them" is a condition with no test. `requirements-core.txt:474` already carries `-r requirements-quality.txt`, so the new pins reach every host venv without editing core; regeneration matters only if a new pin collides with a graphifyy closure version already pinned in core. Reproduce: `grep -n '^-r requirements-quality.txt' requirements-core.txt`; after S-02, `python3 -m pip install --dry-run --require-hashes -r requirements-core.txt` exits non-zero on a collision | open; the commit records that command's exit |
| RV-46 | S3 | `§8`, `RA-10`, `fail_closed_claims` | S-02 | The hash pinning is stated, but the row omits two constraints the file's own header (lines 7-11) and `K-01` carry: every published file of each version hashed, and a release at least 24 h old. The closure is measured on one interpreter: `requirements-core.txt` line 4 says "Python 3.13" and `README.md:91` says "CI runs 3.12", and `.github/workflows/ci.yml:33` installs `requirements-quality.txt` with `--require-hashes`, so a package gated by an environment marker (for example `tomli` below 3.11 or `colorama` on Windows) is absent from a 3.13 report and its absence is measured nowhere for 3.12. `grep -n 'Python 3.13' requirements-core.txt`; `grep -n 'CI runs' README.md`; `grep -n 'require-hashes' .github/workflows/ci.yml` | open; S-02 states the interpreter versions of the report and runs `pip install --dry-run --require-hashes -r requirements-quality.txt` on each |
| RV-47 | S3 | `RA-14` | S-02 | After the 17 pins the file no longer matches statements nothing else edits: `README.md:91` ("The quality instruments behind `make verify` (`ruff` 0.16.3 and `tree-sitter` ...) are pinned in `requirements-quality.txt`"; mypy, bandit and radon are not behind `make verify`), `Makefile:23` ("`requirements-quality.txt` pins ruff and tree-sitter"), `requirements-quality.txt` lines 1-11 ("no transitive dependencies") and `requirements-core.txt` line 5 ("the 4 pins of requirements-quality.txt"). `grep -n 'requirements-quality' README.md Makefile requirements-core.txt` | open; the file's own header is inside the S-02 subject, the README and Makefile lines need a companion edit named in the row |
| RV-48 | S3 | `RA-14`, `check_task_scope.py` segment sums | S-01 | The Wave S-01 table precedes Wave A in file order (the plan's order, required by the Q-01 precedent), but A-01 and A-02 landed before S-01 existed, so the script's first segment (O-12, Q-01, S-01, A-01, A-02 = 241012, margin 1436) counts a unit that executes after the A-02 suspension. Both sums are within 242448 (executed segment 183286). `grep -c ' | yes | ' docs/sprints/060-core-pipeline/task_scope.md` counts the suspensions | recorded; no edit: the table order is the plan order and the margin is positive; a later rewrite of the A-01 and A-02 rows would break their landed SHAs |
| RV-49 | S3 | `RA-14` | A-04, M-01, M-03, M-04, M-15, L-01, D-01, O-08 | S-05 is the only row that names the `README.md` counted block refresh. `scripts/check_readme_counts.py` counts top-level `scripts/*.py` and `make verify` runs it (`Makefile:86`), so each of the other eight rows that creates a `scripts/*.py` fails `make verify` until the block is regenerated; A-03 was refreshed after the fact (`4139880`). `grep -c 'check_readme_counts' docs/sprints/060-core-pipeline/IMPLEMENTATION_PLAN.md` returns 1 (the S-05 line) | open; add the regeneration to the Phase 6 per-batch step ("regenerate generated artifacts") rather than to each row |

No finding on the following, each checked:

| Check | Rows | Result |
| :--- | :--- | :--- |
| `jurisdictional_lock`: one structural subject per row | S-01..S-05 | Each row's `File` cell is one path, distinct from every other row's, and the only shared file is `skill_assignment.md` (S-01 with Z-07 and O-14, ordered in "Same-file ordering"). Companions: S-02 `requirements-core.txt`; S-03 `tests/test_python_quality_auditor.py`; S-05 `tests/test_check_skill_dependencies.py`, `Makefile`, `README.md` counted block |
| S-03 test under `tests/` with `skill_architect` | S-03 | The subject is `skills/python-quality-auditor/scripts/python_quality_auditor.py`, which `agents/implementer_agent.md` `scope_boundaries` PROHIBITS (it "does NOT own `skills/[name]/scripts/`"); the test is the paired test of a `fix(` commit (`agents.md §2 jurisdictional_lock`), a companion and not a second subject, so the `ADR-0009` rule for units whose subject is under `tests/` does not apply. `skill_architect` frontmatter `tools:` holds `Write, Edit, Bash` and no `write_scope`. Only RV-43 (test id) remains |
| S-02 assignee | S-02 | `grep -o 'requirements-[a-z]*.txt' agents/implementer_agent.md` returns `requirements-core.txt` only, so `requirements-quality.txt` is in no profile's `write_scope`; `skill_architect` has no scope restriction; the `requirements-core.txt` regeneration is a companion of the one subject |
| `unambiguous_action` | S-01, S-04, S-05, S-03 (other criteria) | Operation, named target and done-criterion are stated in every row: S-01 names the row and the two measured instruments, S-04 names 23 skills and three measured columns (`ls skills/*/scripts/__init__.py` returns 23 paths), S-05 names the exit code `2` and the check. Residual wording: RV-43, RV-44, RV-45 |
| `fail_closed_claims` on S-05 | S-05 | The claim states its subset ("imports, not binaries"), so a coverage claim of "any dependency" is not made; the residual gaps (mapping, conditional imports) are RV-44 |
| `RA-16` | S-05 | The invoker is the Makefile `verify` target, which the row names and edits; `scripts/verify_references.py` check `(d)` accepts a Makefile reference (precedent `check_readme_counts.py` `invoked_by: Makefile verify target`); the new script's docstring carries the same `invoked_by:` line (D-05 precedent) |
| `agents/implementer_agent.md` `write_scope` for S-05 | S-05 | `scripts/`, `tests/` and `Makefile` are in scope; `README.md` is regenerated by `scripts/check_readme_counts.py --write`, not hand-edited |
| Cost and segments | S-01..S-05 | 2798 + 10101 + 10101 + 115354 + 33574 = 171928; segments: A-02 241012 (margin 1436), A-08 180488, A-14 132570, B-02 183844, all at most 242448; the A-14 suspension is new, without it the A-10..A-14 plus S-02..S-05 segment would be 301700 |

## Verification record

`python3 scripts/check_task_scope.py --sprint-dir docs/sprints/060-core-pipeline`, `python3 scripts/check_sprint_refs.py --current-sprint` and `python3 skills/token-saver-auditor/scripts/audit_plan.py docs/sprints/060-core-pipeline/IMPLEMENTATION_PLAN.md` could not be run in this dispatch (no shell tool). Segment sums above were computed by hand from `config/unit_cost_estimates.json`; the maximum at that round was 240340 (segment F-02, margin 2108) against a ceiling of 242448 (since Round 6 the maximum is the A-02 segment, 241012); round 3 segments are M-18 180008, M-17 225624 and Z-02 236304. Round 2 changed the table order (O-12 first; L-04 and O-11 before Wave M; M-14 in Wave M; O-09 after J), so `check_task_scope.py --batches` must be re-run by the caller. Round 6 (S-01..S-05) was also written without a shell: segment sums were computed by hand (A-02 241012, A-08 180488, A-14 132570, B-02 183844; maximum 241012, margin 1436) and `check_task_scope.py --current-sprint` with and without `--batches` is to be run by the caller.
