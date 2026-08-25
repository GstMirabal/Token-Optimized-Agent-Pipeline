# .agents Global Context & Governance Rules

This is the governance ruleset of the Token-Optimized Agent Pipeline (`.agents`).
It dictates in an absolute and transversal manner the behavior of subagents, code quality, and topological design.

## 0. Documentation Entry Point

| Rule | Value / Constraint |
| :--- | :--- |
| **Entry Point** | Every session MUST start by reading `docs/0_SYSTEM_OVERVIEW.md`. **It is host-only by design** and does not exist in the nucleus: `standardization_workflow.md` scaffolds it into a host at onboarding, and `close_workflow.md` already says the same of it and its sibling anchor. **A nucleus session reads `agents.md` plus `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` instead** — stated here rather than left to inference, because five consecutive sessions of Sprint 023 found the absence and each re-derived the same substitute. That guide is **generated** by `scripts/map_workflows.py` and its staleness is gated by `make verify`: regenerate it, never hand-edit it, and never resolve a discrepancy by deleting it. |
| **Hierarchy** | `architecture/` (Law), `roadmaps/` (Future), `walkthroughs/` (Achievements), `sprints/` (History). |
| **Traceability** | Every module MUST have a `[MODULE]_BLUEPRINT.md` in `architecture/` before coding (template: `docs/standards/templates/BLUEPRINT_TEMPLATE.md`). |
| **Execution** | Every task must be recorded in the current Sprint folder. |
| **Implementation Plan** | Every sprint MUST leave `IMPLEMENTATION_PLAN.md` inside the sprint directory named in `§5 mandatory_topology` (template: `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md`). Authored at Phase 1, extracted to that path at Phase 3, **committed before Phase 5 approves it** (`§2 triple_lock`). It is mentioned seven times across this corpus and until Sprint 023 **no document said where it is written**: a host lost an approved plan to ephemeral storage and nothing detected it, and this repository held two Implementation Plans from April 2026 untracked for four months. `plansDirectory` → `docs/plans/` is a safety net against loss, **not the canonical location** — files there carry IDE-generated names, and `close_workflow.md` Phase 2.6 asks whether *this sprint* left its plan, which cannot be asked of a file named by an editor. |
| **Master Ledger** | The host root `CHANGELOG.md` (Keep a Changelog format; template: `docs/standards/templates/CHANGELOG_TEMPLATE.md`). Every Sprint Closeout appends its sprint entry under `[Unreleased]`; every deployment seals it as `[vX.Y.Z]` before tagging. Strictly separate jurisdiction from `.agents/CHANGELOG.md` (framework evolution) — the only crossover allowed is a pin-bump entry (`chore(deps): pin .agents to vX.Y.Z`). |
| **Certification** | Closing a Sprint requires updating Blueprints, Global Roadmap, Walkthroughs, and the Master Ledger. |
| **Open upstream findings** | **Nucleus sessions only.** `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` holds framework-class defects reported by hosts under `§4 feedback_upstream` — the ones `strict_rule` forbade the host from patching. Read it before planning nucleus work, because several are blocking a shipped mechanism rather than proposing a new one. Announced here rather than left to be discovered: in nucleus mode `docs/active_state.json` does not exist (by design, see `§5`) and neither does `docs/0_SYSTEM_OVERVIEW.md` (finding `F-093-N1` in that file), so **this document is the only file a nucleus session is guaranteed to read**. |

### Rule Contexts (lazy-load index)
Domain rules live in `rules/` and are loaded **on demand** at these triggers — never preloaded (token economy). The machine-readable mirror of this table is `config/rule_triggers.json`; check `(e)` in `scripts/verify_references.py` keeps both in sync.

| Rule file | Load when… |
| :--- | :--- |
| `rules/code_craft.md` | Writing or modifying source code in any language (not documentation or governance edits). |
| `rules/loop_governance.md` | Before wrapping any phase in `/loop` or `/schedule`, or authoring an unattended routine. |
| `rules/token_economy.md` | Reading source files, planning subagent context, or auditing a plan's cost. |
| `rules/qa_and_testing.md` | Writing/running tests, entering the Quality Gate, or after 3 consecutive failures. |
| `rules/project_topology.md` | Running local commands, choosing interpreters/paths, or touching DB containers. |
| `rules/skills_and_integrations.md` | Searching, registering, or forging skills/tools. |
| `rules/frontend_modular_standard.md` | Touching `frontend/src/modules/`. |
| `rules/django_backend_standard.md` | Writing or modifying Django code — models, views, serializers, `signals.py`, app layout, or DRF endpoints. |
| `rules/graphify.md` | Querying or rebuilding the knowledge graph. |
| `rules/documentation_standard.md` | Creating/updating any document under `docs/`, authoring an ADR, or running `docs-freshness-check`. |
| `rules/LEGACY_RULE_CONCORDANCE.md` | Encountering a numbered `Rule NN` citation in any document. |

## 1. Code, Dialect, and Style

| Category | Rule (Key) | Value / Constraint (Value) |
| :--- | :--- | :--- |
| **Python** | `naming_convention` | `snake_case` (vars/funcs), `PascalCase` (classes) |
| **Python** | `linter_command` | `ruff check .` (Reject if exit code > 0) + `python-doctor check --diff` (Warning if score < 95) |
| **JS/TS** | `naming_convention` | `camelCase` |
| **JS/TS** | `linter_command` | `pnpm run lint` (Reject if exit code > 0) + `pnpm run react-doctor` (Warning if score < 95) |
| **Documentation**| `python_style` | Google Style (`Args:`, `Returns:`) |
| **Documentation**| `js_ts_style` | JSDoc (`@param`, `@returns`) |
| **Types** | `requirement` | Mandatory type hints on all args and return values |
| **Complexity** | `max_indentation` | 3 levels |
| **Complexity** | `max_lines_per_func` | 50 lines |
| **Errors** | `exception_handling` | No `pass` in except. Explicit logging required. |
| **Storage** | `path_type` | Relative only. No absolute paths. |
| **Markers** | `ephemeral` | Check regex for `TODO` or `FIXME`. Reject if found. |
| **Language** | `code_logic` | Strictly English (No Spanish in code/logs/commits/artifacts) |
| **Language** | `user_chat` | Spanish strictly confined to human-agent chat and Implementation Plans. |
| **Language** | `technical_clarity` | Avoid redundant greetings. Prioritize Markdown Tables. Restrict Mermaid/ASCII. |
| **Language** | `restrictions` | Define explicitly what is prohibited. Avoid vague positive actions. |
| **Language** | `unambiguous_action` | EVERY instruction — plan step, task, commit message, rule — MUST be executable without interpretation. PROHIBITED: deictics (`here`, `there`, `this repo`) and abbreviations where a proper name exists; action verbs that do not state the operation (`align`, `adopt`, `review`, `evaluate`, `handle`); adjectives used as acceptance criteria (`perfect`, `correct`, `clean`, `complete`) without the check that proves them; magnitudes without a unit; and passive voice that hides who decides. Every step MUST state its operation, its target by name, and its done-criterion. Precedent: in one plan `here` resolved to two different repositories in the same document, and `leave it perfect` was the exit criterion of its largest phase — both would have executed wrongly with no visible error. |

## 2. Autonomy, Efficiency, and Execution

| Category | Rule (Key) | Value / Constraint (Value) |
| :--- | :--- | :--- |
| **Security** | `triple_lock` | Approved Implementation Plan + Active Sprint + QA/Tester Approval + Human OK. **Lock 1 has a path and an ordering**: the plan is at `IMPLEMENTATION_PLAN.md` inside the canonical sprint directory (`§0`, `§5 mandatory_topology`) and is committed **before** Phase 5 runs. A lock cannot close over an artifact that does not exist, and an approval whose object vanished cannot be audited afterwards — which is the failure this rule was written against. |
| **Context** | `token_saver` | Files >200 lines MUST NOT be fully dumped. Targeted partial reads (offset/limit on the affected function) are the sanctioned mechanism. Decision ladder in `rules/token_economy.md`. |
| **Context** | `ast_skeleton` | For structural discovery on large files, invoke `omni_minimizer.py` to extract the skeleton before any partial read. |
| **Context** | `anti_amnesia` | Re-read `agents.md` and `active_state.json` once per session (at start) and after any context compaction — not after every execution step. |
| **Context** | `graph_sovereignty`| Query `graph.json` via MCP or CLI before any full codebase research or recursive grep operations. |
| **WIP Safety** | `pre_shielding` | Abort if `git status --porcelain` returns unresolved differences. |
| **WIP Safety** | `destructive_flags` | Reject massive modifications/deletions unless the human grants explicit approval (via chat or Claude Code's permission prompt). |
| **WIP Safety** | `graph_sync` | Mandate running `graphify update` post-changes during quality check or commit phase. |
| **Isolation** | `jurisdictional_lock` | Limit structural editing to `1` single physical file per instantiated subagent task. |
| **Isolation** | `no_interference` | Abort if `task_scope.md` shows the target file listed by another subtask in progress. |

## 3. Architecture and Topology of the Project

| Category | Rule (Key) | Value / Constraint (Value) |
| :--- | :--- | :--- |
| **Framework** | `federation` | Check `git remote`; isolate `.agents` purely as a *Git Submodule*. The sanctioned bridge into the host's `.claude/` is exclusively `.agents/scripts/install.sh` (symlinks + non-destructive JSON merge) — no other mechanism may inject content into the host's Claude Code configuration. |
| **Framework** | `strict_rule` | Prohibited to alter internal architecture of this submodule from tactical injections. |
| **Framework** | `symlink_gate_exclusion` | Host-root `AGENTS.md` that is a tracked symlink into `.agents/agents.md` is **out of host documentary-gate scope**. The host **excludes the symlink path** in its own gate configuration. Reason: `strict_rule` forbids the host from modifying that content, so a gate that demands fixing what the host must not touch is an unsalvageable red (`C5`). |
| **Framework** | `jurisdiction` | **A session's jurisdiction is where its anchor is.** In nucleus mode (`.git` is a real directory — `scripts/_mode.py`) the framework is the work and its sprint records belong in `.agents/docs/sprints/`. In submodule mode the host is the work, and **a host session MUST leave `git -C .agents status --porcelain` empty**: its sprint records belong at the host root (`§5`), and a framework improvement goes through `§4 feedback_upstream` — a branch and pull request against the nucleus repository, worked in a **separate clone** — which is a distinct act from the host's sprint, never a write into the submodule's tree. Enforced by `scripts/submodule_purity.py` at commit time (`hooks/on_commit.py`) and at close (`close_workflow.md` Phase 5), not by recollection: until Sprint 025 this rule existed only as prose and the command that would have checked it was blind, because `.gitignore` hid the very paths a host contaminates. |
| **Environment** | `no_globals` | Cap or reject global injections in the main OS binary. |
| **Environment** | `dependencies` | Force explicit prefix syntax by invoking commands through isolated local dev environment. |
| **Infrastructure**| `three_file_standard` | **Executable skills** (they ship a `/scripts/` folder) MUST adhere to the full Three-File Standard: 1. `README.md`, 2. `SKILL.md`, 3. `/scripts/` with `__init__.py`. **Knowledge skills** (pure guidance, no scripts) only require a `SKILL.md` with valid `name`/`description` frontmatter — padding them with empty scaffolding is PROHIBITED noise. |
| **Infrastructure**| `topological_order`| Skills flat inside `skills/`. Sub-layers (`core/`, `local/`) PROHIBITED. Project-specific packs live under `profiles/[name]/` and are only linked into a host via `install.sh --profile [name]`. **Real production profiles are never committed to the public nucleus** (`RA-15`) — only illustrative examples like `profiles/example-project/` live here; a host's real profile stays in a private location it controls. |
| **Infrastructure**| `enforcement` | `mass-standardizer` tool is the official auditor for this standard. |
| **Infrastructure**| `secret_sovereignty`| BANNED from reading `.env` into memory. Use environment export commands. |
| **QA Framework** | `local_testing` | Overwrite native URLs to instantiate in RAM (`sqlite:///:memory:`). |

## 4. Memory Management and Feedback Loop

| Category | Rule (Key) | Value / Constraint (Value) |
| :--- | :--- | :--- |
| **Amnesia** | `zero_tolerance` | Zero-Tolerance Accumulation. Bug resolutions MUST be immediately injected. |
| **Amnesia** | `ephemeral_memory` | The `memory` directory is strictly ephemeral. MUST be emptied upon sprint closure. |
| **Feedback Loop** | `constitutional_escalation`| Systemic improvements MUST be formally indexed into `agents.md` before purging logs. |
| **Feedback Loop** | `definitive_amnesia` | Temporary logs are permanently deleted the moment the fix is applied. |
| **Index Routing** | `index_files` | Parse exclusively `memory_index.json` locally. |
| **Index Routing** | `single_line_breakdown`| Reject JSON insertions that break the 1-sentence limit without a carriage return. |
| **Feedback Loop** | `feedback_upstream` | Learning is a LIVING three-tier flow, never a dead end: **host-class** findings stay in the host's `memory_index.json`; **project-family-class** findings route to `profiles/[name]/` (rules/skills/docs); **framework-class** findings (would improve every host) MUST be drafted as a nucleus contribution — a J-amendment proposal or fix PR to the `.agents` repo — during `extract_workflow`. Every host session is a sensor for the shared brain; letting a framework-class lesson die in a local index is a governance violation. |

## 5. Central Base (Project Master Index)

| Category | Rule (Key) | Value / Constraint (Value) |
| :--- | :--- | :--- |
| **Initialization** | `mandatory_topology` | Reject init if `/docs/` missing. **Canonical sprint path, declared here and referenced (never restated) elsewhere**: `docs/sprints/[Sprint_ID]-[Stack]-[Layer]/`. Four different forms of it were in circulation until Phase 019 — `docs/sprints/[ID]/`, this one, `docs/sprints/[ID]-[Stack]-[Layer]/`, and the nucleus's own `docs/sprints/core/pipeline/` — so `graph_stats.json` was being persisted to a path no other document recognised. **The nucleus uses this same path** (`docs/sprints/024-core-pipeline/` was the first). It previously did not, and could not: `.gitignore` excluded `docs/sprints/`, `task_scope.md`, `implementation_plan*` and the anchor itself, to keep a host's records out of the shared submodule. That intent is `RA-15` and is right; the instrument was inverted. `close_workflow.md` `submodule_purity` guards the submodule with `git -C .agents status --porcelain`, **which does not list ignored files** — verified: a file created under `docs/sprints/` left that command completely empty, so the exclusion hid host contamination from the only check built to catch it, while making `rules/documentation_standard.md:94` (a **git-tracked** `graph_stats.json` inside this directory) impossible to satisfy. Host protection is now stated where it can be enforced rather than assumed: a host session MUST NOT write inside `.agents` (`§3 strict_rule`), and `submodule_purity` refuses the close when it does. |
| **Initialization** | `legacy_onboarding` | If mature project: Execute **Full Reverse Engineering** and generate Walkthroughs. |
| **Nucleus Guard** | `nucleus_neutrality` | Automatic structural scaffolding PROHIBITED if workspace is `.agents` core. |
| **Traceability** | `state_anchor` | Context MUST be extracted from `docs/active_state.json` (Zero Coordinate). |
| **Traceability** | `state_homologation` | Creating state-tracking files outside `docs/active_state.json` is PROHIBITED. |
| **Traceability** | `historical_log` | Reject pushes without the `#[Sprint_ID]` suffix (e.g. `#073`). Apply Conventional Commits. |
| **MCP Registry** | `discovery_manifest` | `.agents/claude/mcp.json` is the submodule's MCP server template; `install.sh` merges it non-destructively into the host's `.mcp.json`, which is the actual discovery point Claude Code reads. |

## 6. Agent Roles & Execution Pipeline

The pipeline operates under a rigid sequential process. Role usurpation is strictly prohibited.

| Category | Rule (Key) | Value / Constraint (Value) |
| :--- | :--- | :--- |
| **Subagent Roles** | `principal_agent` | Lead Agent. Creates Implementation Plan (informed by graphify), manages the Approval Gate. |
| **Subagent Roles** | `devops_agent` | Environment Agent. Manages venv, .env export, and Docker health. **Sole holder of `Write`/`Edit` for the framework-root `scripts/` and `hooks/` trees** (`F-086-A1`, Sprint 023) — not `skills/[name]/scripts/`, which `skill_architect` forges. It gives those trees an owner without creating the implementer role the map still lacks (`F-021-A2`, declared in that profile). |
| **Subagent Roles** | `orchestrator` | Roadmap Author. Drafts Initial Roadmap and instantiates Sprint Hierarchy. |
| **Subagent Roles** | `agent_orchestrator`| Agent Assignment. Assigns specific subagents to the Initial Roadmap steps. |
| **Subagent Roles** | `skill_architect` | Skill Builder. Prepares/injects skills for the assigned subagents. |
| **Subagent Roles** | `rule_validator` | Rule Auditor. Audits Roadmap using graphify dependency graph to generate the `task_scope.md`. |
| **Subagent Roles** | `qa_agent` | Structural Verifier. Validates code standards and checks graphify AST graph integrity. |
| **Subagent Roles** | `tester_agent` | Test Verifier. Ensures logic stability and zero regression. |

> [!NOTE]
> **Core vs. Auxiliary.** The 8 roles above are the *Core Pipeline Roles* (mandatory in every Planning → Sprint Closeout cycle). `governance_learner`, `doc_orchestrator`, `topology_mapper`, `git_sync_agent`, and `token_economy_agent` (see `agents/*.md`) are **Auxiliary Agents** — invoked as needed (knowledge distillation, documentation, topology, upstream sync) but not a mandatory stop on every pipeline pass. **Project-specific specialists** (e.g. `backend_identity_specialist`, `frontend_ux_hardener`) live in `profiles/[name]/agents/` and only join the pipeline when their profile is installed. Their absence from this table is intentional, not an omission.

### 🚀 The Execution Pipeline

**Onboarding order (canonical, declared once).** On a repository the framework has not handled before, three protocols run before the pipeline, in this order. Every other document that mentions onboarding **references this list and never restates it** (`RA-14`):

| # | Protocol | Owns | Why here |
| :--- | :--- | :--- | :--- |
| 1 | `workflows/repository_hardening_workflow.md` (`/agents:harden`) | **Platform controls**: secret scanning, private vulnerability reporting, Dependabot, code scanning, branch protection | Changes no code and reduces risk immediately, so it costs nothing to do first |
| 2 | `workflows/standardization_workflow.md` (`/agents:standardization`) | **Artifacts and topology**: census of legacy material, secret scan, snapshot branch, migration under human approval | Ordering the house before documenting it; otherwise the documentation describes a layout about to change |
| 3 | `workflows/reverse_documentation_workflow.md` (`/agents:revdoc`) | **Documentation of the code**: graph first, every declared path verified, contracts, C4, ADR | Fixing before documenting means fixing against a model of the system rather than the system |
| 4 | `workflows/pipeline_workflow.md` (`/agents:pipeline`) | Change | Only now is there a verified account of what is being changed |

Steps 2 and 3 are frequently confused because they are adjacent: `standardization` migrates *artifacts*, `revdoc` documents *code*. Different objects, and until Phase 019 no document declared which ran first.

The normative 8-phase pipeline (Planning → Sprint Closeout) is defined **exclusively** in `workflows/pipeline_workflow.md`, loaded on demand via `/agents:pipeline`. It is not duplicated here to keep the always-loaded governance ruleset lean and drift-free. Non-negotiables enforced at this level: the Approval Gate (Phase 5) is a single attended human authorization — never wrapped in an unattended `/loop` — and all execution happens on `ai-sprint/[ID]` (RA-12).

## 7. Rule Amendments

| Category | Rule (Key) | Value / Constraint (Value) |
| :--- | :--- | :--- |
| **Amendment** | `RA-01: ENVIRONMENT_VIOLATION`| Agent MUST attempt autonomous remediation EXCEPT if prohibited. |
| **Amendment** | `RA-02: LAZY_SIGNAL_PARADIGM` | Prevent circular deps in Django `signals.py`: local imports in receiver. |
| **Amendment** | `RA-03: HOTFIX_FLAT` | For CRITICAL/HIGH defects outside the sprint pipeline (including protocol gaps found during or after `/agents:deployment`): (1) branch MUST be `hotfix/[H-ID]` — **never** `fix/`, `feat/`, or `chore/` as the branch name (Conventional Commits *type* `fix(...)` on that branch is fine); (2) record `docs/hotfixes/[H-ID]-[Layer].md` from `HOTFIX_TEMPLATE.md` **before** the first substantive commit; (3) commit suffix `#[H-ID]` with no hyphen (`#H003`, not `#H-003` — `hooks/on_commit.py` requires `#\w+`). Next free id is the successor of the highest existing `docs/hotfixes/H-*.md`. **Sanctioned exception to RA-06 naming** — emergency speed wins over Option B; the deviation is deliberate, not drift. Precedent: Hotfix H-003 was first opened as `fix/github-release-in-deploy` because this row named only the doc path, not the branch — corrected here. |
| **Amendment** | `RA-04: FULL_DEPLOYMENT` | Orchestrator MUST deploy the COMPLETE task hierarchy in a single atomic action. |
| **Amendment** | `RA-05: SPRINT_CLOSEOUT` | Mandatory update of Blueprints, Global Roadmap, Walkthroughs, and Ledger before closing. |
| **Amendment** | `RA-06: IDENTITY_NAMING` | Standard Option B: All docs must be named `[MODULE]_[TYPE].md` (e.g. `USERS_BLUEPRINT.md`). |
| **Amendment** | `RA-07: ARCHIVE_PURGE` | Prohibited to keep empty `archive/` folders. Purge immediately if found. |
| **Amendment** | `RA-08: COMMIT_SQUASH` | Mandatory atomic local commits; mandatory squash & push only during Sprint Closeout. |
| **Amendment** | `RA-09: SECRET_SOVEREIGNTY`| Prohibited from reading `.env` into thought context. Use `Makefile` or `source .env` in a subshell. |
| **Amendment** | `RA-10: SUPPLY_CHAIN_SHIELD`| Mandate `pnpm 11+`, `ignore-scripts=true`, and `minimum-release-age=1440`. |
| **Amendment** | `RA-11: HOOK_BLOCKING_SEMANTICS`| Claude Code `PreToolUse` hooks only block a tool call on exit code `2` (stderr fed back to the model); exit `1` is a non-blocking warning. Every hook in `hooks/` that must halt execution MUST `sys.exit(2)`, never `1`. |
| **Amendment** | `RA-12: BRANCH_DISCIPLINE`| Every sprint lives on `ai-sprint/[ID]`, created in `pipeline_workflow.md` Phase 3 before the first commit and pushed (never to `main`) in `close_workflow.md` Phase 5. Only `deployment_workflow.md` Phase 1 may merge a sprint branch into `main`/upstream. Direct commits or pushes to `main` during `Execution` are PROHIBITED. |
| **Amendment** | `RA-13: SEQUENTIAL_GATES`| A verification gate and the irreversible action it guards MUST be separate invocations: the gate's result is OBSERVED before the action is issued. Chaining them in one script/command (e.g. `sleep && merge`) voids the gate — that is how a red CI reached `main` in Sprint #081. |
| **Amendment** | `RA-14: PATCH_PROPAGATION`| A long-lived planning/design document revised across multiple sessions or review rounds MUST, at each patch, be grepped in full for other mentions of the same term/field before the patch is considered closed. A fix applied only where a reviewer looked, while the same reference drifts uncorrected elsewhere in the same artifact, is not a correction — it is a new inconsistency. |
| **Amendment** | `RA-16: INVOCATION_COVERAGE`| No mechanism — workflow, script, executable skill, hook or gate — merges without a **declared, verifiable invoker**, or a typed exception stating why it has none. Workflows and scripts declare `invoked_by:` (frontmatter or module docstring); skills and vendored material are declared in `config/invocation_exceptions.json`, since `rules/skills_and_integrations.md §3` forbids editing vendored `SKILL.md` files. Enforced by `scripts/verify_references.py` check (d), which also rejects an exception pointing at a path that no longer exists. A mechanism nothing calls is a regression, not a pending feature. Precedent: `/agents:harden` shipped in PR #29 and was never run against this repository — five platform controls sat disabled for weeks — while `contract-writer` was built for `revdoc` Phase 6 and that phase never named it. The check must resolve Python **imports**, not just filename mentions: `merge_json.py` looked orphaned to a filename-only scan while `install.py` depends on it, and deleting it would have broken the bridge installer. |
| **Amendment** | `RA-15: HOST_CONTENT_GENERICIZATION`| Any `feedback_upstream` (`agents.md §4`) contribution to the nucleus — a framework-class fix, skill, or test fixture discovered while working inside a real host project — MUST have every host-identifying string (real project name, real absolute filesystem paths, real business logic/thresholds) genericized before the PR. Real project profiles (`profiles/[name]/`) are never committed to the public nucleus at all — they live in a private location the host controls, referenced locally. Precedent: a real host's absolute path leaked into `skills/skillopt/data/scenarios.json`, and a real host project name was hardcoded into `skills/compliance-checker/scripts/kill_switch.sh`, both found only during a pre-publication audit rather than caught at contribution time. |

## 8. Supply Chain Security

| Category | Rule (Key) | Value / Constraint (Value) |
| :--- | :--- | :--- |
| **Package Manager** | `requirement` | Mandatory use of `pnpm 11+`. `npm` and `yarn` are prohibited for installation. |
| **Installation** | `ignore_scripts` | `ignore-scripts=true` MUST be active in `.npmrc`. |
| **Release Safety** | `min_release_age` | `minimum-release-age=1440` (24 hours) MUST be enforced to avoid zero-day compromised packages. |
| **Audit** | `only_built_deps` | All dependencies requiring build scripts MUST be explicitly whitelisted in `onlyBuiltDependencies`. |
