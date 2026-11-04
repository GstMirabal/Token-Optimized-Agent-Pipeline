# How to find the history and precedents of a rule in agents.md

**Last Audit Sprint**: 059
**Last Audit Date**: 2026-11-04
**Last Audit Commit SHA**: 21e248e

---

## Goal

`agents.md` keeps each rule and a pointer; this guide holds the history, measurement and precedents of the rows moved in Sprint 059. It is loaded on demand, never preloaded. The detail of `linter_command`, `max_indentation`, `max_lines_per_func`, `exception_handling` and `fail_closed_claims` is in `rules/code_craft.md §8`, the detail of `jurisdiction`, `RA-09` and `RA-19` is in `rules/project_topology.md §5`, and the detail of `feedback_upstream` is in `docs/guides/SELF_IMPROVEMENT_GUIDE.md`.

## §0 Documentation Entry Point

### Entry Point

Every session MUST start by reading `docs/0_SYSTEM_OVERVIEW.md`. **It is host-only by design** and does not exist in the nucleus: `standardization_workflow.md` scaffolds it into a host at onboarding, and `close_workflow.md` already says the same of it and its sibling anchor. **A nucleus session reads `agents.md` plus `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` instead** — stated here rather than left to inference, because five consecutive sessions of Sprint 023 found the absence and each re-derived the same substitute. That guide is **generated** by `scripts/map_workflows.py` and its staleness is gated by `make verify`: regenerate it, never hand-edit it, and never resolve a discrepancy by deleting it.

### Implementation Plan

Every sprint MUST leave `IMPLEMENTATION_PLAN.md` inside the sprint directory named in `§5 mandatory_topology` (template: `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md`). Authored at Phase 1, extracted to that path at Phase 3, **committed before Phase 5 approves it** (`§2 triple_lock`). It is mentioned seven times across this corpus and until Sprint 023 **no document said where it is written**: a host lost an approved plan to ephemeral storage and nothing detected it, and this repository held two Implementation Plans from April 2026 untracked for four months. `plansDirectory` → `docs/plans/` is a safety net against loss, **not the canonical location** — files there carry IDE-generated names, and `close_workflow.md` Phase 2.6 asks whether *this sprint* left its plan, which cannot be asked of a file named by an editor.

### Master Ledger

The host root `CHANGELOG.md` (Keep a Changelog format; template: `docs/standards/templates/CHANGELOG_TEMPLATE.md`). Every Sprint Closeout appends its sprint entry under `[Unreleased]`; every deployment seals it as `[vX.Y.Z]` before tagging. Strictly separate jurisdiction from `.agents/CHANGELOG.md` (framework evolution) — the only crossover allowed is a pin-bump entry (`chore(deps): pin .agents to vX.Y.Z`). **An entry under `[Unreleased]` names the commit it describes**, by short SHA in backticks. Not decoration: `scripts/detect_drift.py` reads that citation as per-commit proof of coverage, and it is the only such proof available before a deployment seals the section — reachability can show a *range* is covered and never a commit, which is how `PRs #26-#30` sat inside a tag's ancestry and stayed unrecorded. An entry naming no commit leaves its work on verdict `A`, which asks a human to re-read the same section every session until the next tag; the sixth such reading is the one that gets skipped. Sprint 051.

### Certification

See `RA-05: SPRINT_CLOSEOUT` for the closeout artifact list (Blueprints, Global Roadmap, Walkthroughs, Master Ledger). Single definition kept in `§7` to avoid an always-loaded duplicate.

### Open upstream findings

**Nucleus sessions only.** `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` holds framework-class defects reported by hosts under `§4 feedback_upstream` — the ones `strict_rule` forbade the host from patching. Read it before planning nucleus work, because several are blocking a shipped mechanism rather than proposing a new one. Announced here rather than left to be discovered: a nucleus session has no `docs/0_SYSTEM_OVERVIEW.md` (`F-093-N1`; host-only, Entry Point above) and **does** keep `docs/active_state.json` (`§5 state_anchor`; `close_workflow.md` Phase 4 applies in nucleus mode too). Start from this document and that anchor. The channel A intake queue that `--boot` lists (`§4 feedback_upstream`) is triaged in Phase 1 of the same sprint.

### Command paths

Declared once here for both forms of a framework command that a document names (`F-115-N3`, Sprint 054; `KI-054-2`). **Host:** `.agents/` is a git submodule and commands run from the host root as `python3 .agents/scripts/<name>.py` (likewise `.agents/hooks/`, `make -f .agents/Makefile <target>`). **Nucleus:** this repository is `.agents`, so the form is `python3 scripts/<name>.py` and `make <target>`; `scripts/_mode.py` decides the mode (`.git` is a real directory in the nucleus). A document that writes the bare nucleus form means the host form when run in a host: a host session that ran it got `can't open file`. Kept here because this file is always loaded, gate subagents included, which replaces per-file notes.

## §1 Code, Dialect, and Style

### unambiguous_action

EVERY instruction — plan step, task, commit message, rule — MUST be executable without interpretation. PROHIBITED: deictics (`here`, `there`, `this repo`) and abbreviations where a proper name exists; action verbs that do not state the operation (`align`, `adopt`, `review`, `evaluate`, `handle`); adjectives used as acceptance criteria (`perfect`, `correct`, `clean`, `complete`) without the check that proves them; magnitudes without a unit; and passive voice that hides who decides. Every step MUST state its operation, its target by name, and its done-criterion. Precedent: in one plan `here` resolved to two different repositories in the same document, and `leave it perfect` was the exit criterion of its largest phase — both would have executed wrongly with no visible error.

## §2 Autonomy, Efficiency, and Execution

### triple_lock

Approved Implementation Plan + Active Sprint + QA/Tester Approval + Human OK. **Lock 1 has a path and an ordering**: the plan is at `IMPLEMENTATION_PLAN.md` inside the canonical sprint directory (`§0`, `§5 mandatory_topology`) and is committed **before** Phase 5 runs. A lock cannot close over an artifact that does not exist, and an approval whose object vanished cannot be audited afterwards — which is the failure this rule was written against.

### token_saver

Files >200 lines MUST NOT be fully dumped. Targeted partial reads (offset/limit on the affected function) are the sanctioned mechanism. Decision ladder in `rules/token_economy.md`.

### ast_skeleton

For structural discovery on large files, invoke `skills/omni-context-minimizer/scripts/omni_minimizer.py` (skill: `omni-context-minimizer`) to extract the skeleton before any partial read.

### graph_sync

Mandate running `venv_skillopt/bin/python -m graphify update .` post-changes during quality check or commit phase (never the bare `graphify` console-script — it fails `bad interpreter` under a relocated `.agents`; `rules/graphify.md`).

### jurisdictional_lock

A subagent task claims **exactly one file as its structural subject** — the file the task exists to change — declared in `task_scope.md`, and no concurrently in-progress task may claim that same subject (`no_interference`). **The subject is the unit of isolation, not a count of files in a commit**: a commit MAY stage further files that the subject's own rules require — notably the paired test a `fix(` commit must carry unless it takes the `Repro: manual` route (`rules/code_craft.md §6`, enforced by `hooks/on_commit.py audit_regression_test`) — because a mandatory companion is not an independently claimable subject and cannot collide with another task. It caps **concurrent** claim scope, never lifetime touches on a file: a later task may take the same subject once the earlier one has landed (Phase 014 `T21`/`T22` precedent). Stated as a bare file count until Sprint 048. That bare count left the invariant unstated and produced the opposite reading downstream — that the mandatory test of a `fix(` commit violated this rule. Sprint 046 escaped it by mislabelling a `fix(` commit `refactor(`, and Sprint 047 re-paired 7 units mid-execution.

## §3 Architecture and Topology of the Project

### federation

Check `git remote`; isolate `.agents` purely as a *Git Submodule*. The sanctioned bridge into the host's `.claude/` is exclusively `.agents/scripts/install.py` (`install.sh` is a deprecation shim that forwards to it; symlinks + non-destructive JSON merge) — no other mechanism may inject content into the host's Claude Code configuration.

### symlink_gate_exclusion

Host-root `AGENTS.md` that is a tracked symlink into `.agents/agents.md` is **out of host documentary-gate scope**. The host **excludes the symlink path** in its own gate configuration. Reason: `strict_rule` forbids the host from modifying that content, so a gate that demands fixing what the host must not touch is an unsalvageable red (`C5`).

### three_file_standard

Moved to `rules/skills_and_integrations.md` (D18).

### topological_order

Moved to `rules/skills_and_integrations.md` (D18).

### enforcement

Moved to `rules/skills_and_integrations.md` (D18).

### secret_sovereignty

See `RA-09: SECRET_SOVEREIGNTY` (canonical — adds the human-run `scripts/with_env.py` mechanism). BANNED from reading `.env` into memory or printing a value from it.

### local_testing

Moved to `rules/qa_and_testing.md` (D18).

## §5 Central Base (Project Master Index)

### mandatory_topology

Reject init if `/docs/` missing. **Canonical sprint path, declared here and referenced (never restated) elsewhere**: `docs/sprints/[Sprint_ID]-[Stack]-[Layer]/`. Four different forms of it were in circulation until Phase 019 — `docs/sprints/[ID]/`, this one, `docs/sprints/[ID]-[Stack]-[Layer]/`, and the nucleus's own `docs/sprints/core/pipeline/` — so `graph_stats.json` was being persisted to a path no other document recognised. **The nucleus uses this same path** (`docs/sprints/024-core-pipeline/` was the first). It previously did not, and could not: `.gitignore` excluded `docs/sprints/`, `task_scope.md`, `implementation_plan*` and the anchor itself, to keep a host's records out of the shared submodule. That intent is `RA-15` and is right; the instrument was inverted. `close_workflow.md` `submodule_purity` guards the submodule with `git -C .agents status --porcelain`, **which does not list ignored files** — verified: a file created under `docs/sprints/` left that command completely empty, so the exclusion hid host contamination from the only check built to catch it, while making `rules/documentation_standard.md:94` (a **git-tracked** `graph_stats.json` inside this directory) impossible to satisfy. Host protection is now stated where it can be enforced rather than assumed: a host session MUST NOT write inside `.agents` (`§3 strict_rule`), and `submodule_purity` refuses the close when it does.

### discovery_manifest

`.agents/claude/mcp.json` is the submodule's MCP server template; `install.py` (`install.sh` is a deprecation shim that forwards to it) merges it non-destructively into the host's `.mcp.json`, which is the actual discovery point Claude Code reads.

## §6 Agent Roles & Execution Pipeline

### devops_agent

Environment Agent. Manages venv, prepares `.env`-dependent commands for the human to run through `scripts/with_env.py` (`RA-09`; the agent never runs them), and Docker health. Retains `Bash` for those routines; does **not** hold `Write`/`Edit` for framework-root `scripts/`/`hooks/`/`tests/` — those trees are authored by `implementer_agent` (`ADR-0009`, Sprint 033; `F-086-A1` ownership preserved under the new profile). Not `skills/[name]/scripts/`, which `skill_architect` forges.

### Onboarding order 1

Protocol: `workflows/repository_hardening_workflow.md` (`/agents:harden`). Owns: **Platform controls**: secret scanning, private vulnerability reporting, Dependabot, code scanning, branch protection. Why here: Changes no code and reduces risk immediately, so it costs nothing to do first.

### Onboarding order 2

Protocol: `workflows/standardization_workflow.md` (`/agents:standardization`). Owns: **Artifacts and topology**: census of legacy material, secret scan, snapshot branch, migration under human approval. Why here: Ordering the house before documenting it; otherwise the documentation describes a layout about to change.

### Onboarding order 3

Protocol: `workflows/reverse_documentation_workflow.md` (`/agents:revdoc`). Owns: **Documentation of the code**: graph first, every declared path verified, contracts, C4, ADR. Why here: Fixing before documenting means fixing against a model of the system rather than the system.

## §7 Rule Amendments

### RA-01: ENVIRONMENT_VIOLATION

On an environment/tooling failure (missing venv, absent binary, broken lockfile) the agent MUST attempt one scoped autonomous fix through the isolated local environment (`§3 dependencies`) before escalating, UNLESS `rules/project_topology.md` or the Implementation Plan names that remediation human-only. Procedure: `workflows/remediation_workflow.md` for loop stalls (auto-invoked after >3 consecutive `REJECTED` on one logic block — `remediation_workflow.md` Phase 0); `RA-03: HOTFIX_FLAT` for CRITICAL/HIGH defects outside the sprint pipeline. Invoked by: `pipeline_workflow.md` Execution phase on any tool/interpreter failure, and `devops_agent` environment routines.

### RA-02: LAZY_SIGNAL_PARADIGM

See `rules/django_backend_standard.md §2 Signal Registration` (single authority since Sprint 047). Anchor kept resolvable for legacy `Clause J-02` via `rules/LEGACY_RULE_CONCORDANCE.md`.

### RA-03: HOTFIX_FLAT

For CRITICAL/HIGH defects outside the sprint pipeline (including protocol gaps found during or after `/agents:deployment`): (1) branch MUST be `hotfix/[H-ID]` — **never** `fix/`, `feat/`, or `chore/` as the branch name (Conventional Commits *type* `fix(...)` on that branch is fine), and **never an IDE-generated prefix**: `<user>/…` or `cursor/…` from an editor's "create branch and commit" affordance does not satisfy this row, and the rename is due before the first substantive commit (`RA-12`, Sprint 051 — precedent: a host's hotfix opened as `<user>/fix-…`); (2) record `docs/hotfixes/[H-ID]-[Layer].md` from `HOTFIX_TEMPLATE.md` **before** the first substantive commit; (3) commit suffix `#[H-ID]` with no hyphen (`#H003`, not `#H-003` — `hooks/on_commit.py` requires `#\w+`). Next free id is the successor of the highest existing `docs/hotfixes/H-*.md`. **Sanctioned exception to RA-06 naming** — emergency speed wins over Option B; the deviation is deliberate, not drift. Precedent: Hotfix H-003 was first opened as `fix/github-release-in-deploy` because this row named only the doc path, not the branch — corrected here.

### RA-04: FULL_DEPLOYMENT

**Retired Sprint 046** — superseded by `§6 orchestrator` (roadmap author, not deployer) + `RA-12 BRANCH_DISCIPLINE` + `deployment_workflow.md` Phase 1 (the sole merge authority). Historical text: "Orchestrator MUST deploy the COMPLETE task hierarchy in a single atomic action" — 0 external citations across 45 sprints, no implementing workflow, and it contradicted the `§6 orchestrator` charter. Row kept as a tombstone: `RA-05`..`RA-18` are **never renumbered** (100+ external by-number citations).

### RA-10: SUPPLY_CHAIN_SHIELD

See `§8 Supply Chain Security` (canonical). `§8` is the superset: the same `pnpm 11+` / `ignoreScripts: true` / `minimumReleaseAge: 1440` plus `onlyBuiltDependencies`, all in `pnpm-workspace.yaml` — never `.npmrc`, which pnpm 11+ does not read for them (`F-115-N1`). Row kept as a pointer so the external `RA-10` citations stay resolvable; `RA-05`..`RA-18` are never renumbered.

### RA-11: HOOK_BLOCKING_SEMANTICS

Claude Code `PreToolUse` hooks only block a tool call on exit code `2` (stderr fed back to the model); exit `1` is a non-blocking warning. Every hook in `hooks/` that must halt execution MUST `sys.exit(2)`, never `1`.

### RA-12: BRANCH_DISCIPLINE

Every sprint lives on `ai-sprint/[ID]`, created in `pipeline_workflow.md` Phase 3 before the first commit and pushed (never to `main`) in `close_workflow.md` Phase 5. Only `deployment_workflow.md` Phase 1 may merge a sprint branch into `main`/upstream. Direct commits or pushes to `main` during `Execution` are PROHIBITED. **An IDE-generated branch prefix does not satisfy this row** — `<user>/…`, `cursor/…` and anything else an editor's "create branch and commit" affordance invents is not `ai-sprint/[ID]`, however good the branch's contents are. Rename **before the first substantive commit**: after it, the commit-message gate has already accepted a `#[Sprint_ID]` suffix against a branch the rule does not recognise, and the sprint's history has to be rewritten rather than renamed. Same obligation, same timing, for `RA-03`'s `hotfix/[H-ID]`. Sprint 051.

### RA-13: SEQUENTIAL_GATES

A verification gate and the irreversible action it guards MUST be separate invocations: the gate's result is OBSERVED before the action is issued. Chaining them in one script/command (e.g. `sleep && merge`) voids the gate — that is how a red CI reached `main` in Sprint #081.

### RA-14: PATCH_PROPAGATION

A long-lived planning/design document revised across multiple sessions or review rounds MUST, at each patch, be grepped in full for other mentions of the same term/field before the patch is considered closed. A fix applied only where a reviewer looked, while the same reference drifts uncorrected elsewhere in the same artifact, is not a correction — it is a new inconsistency. **Headline-metrics clause** (`KI-045-2`): a deliverable's headline metrics — verdict counts, cross-reference targets — MUST be a `grep`-reproducible figure derived from the body register, never carried from the author's summary prose. Precedent: Sprint 045 Gate 1 cited a skill that exists nowhere, and Gate 2 found a headline `27/9` against a register of `22/14`. **Sprint-artifact-set clause** (Sprint 044 proposal): the mandatory patch-propagation grep extends from "the same artifact" to the sprint's **artifact set** (Implementation Plan, `task_scope.md`, ADRs, skill-assignment and every sprint-directory document), and binds to the **remediation step**, not only the reviewer's spot-check. Precedent: Sprint 044 reconciled "403/404" → "403" across the plan, `task_scope.md` and `ADR-0014` but left a 4th spelling in `skill_assignment.md:38` until Gate 1 round 2.

### RA-15: HOST_CONTENT_GENERICIZATION

Any `feedback_upstream` (`agents.md §4`) contribution to the nucleus — a framework-class fix, skill, or test fixture discovered while working inside a real host project — MUST have every host-identifying string (real project name, real absolute filesystem paths, real business logic/thresholds) genericized before it leaves the host — an outbox entry's `genericized: true` (`§4 feedback_upstream`), or the PR. Real project profiles (`profiles/[name]/`) are never committed to the public nucleus at all — they live at a host-controlled path (convention `<host-root>/.agents-profile/` or equivalent; installed with `scripts/install.py --profile-path`). Precedent: a real host's absolute path leaked into `skills/skillopt/data/scenarios.json`, and a real host project name was hardcoded into `skills/compliance-checker/scripts/kill_switch.sh`, both found only during a pre-publication audit rather than caught at contribution time.

### RA-16: INVOCATION_COVERAGE

No mechanism — workflow, script, executable skill, hook or gate — merges without a **declared, verifiable invoker**, or a typed exception stating why it has none. Workflows and scripts declare `invoked_by:` (frontmatter or module docstring); skills and vendored material are declared in `config/invocation_exceptions.json`, since `rules/skills_and_integrations.md §3` forbids editing vendored `SKILL.md` files. Enforced by `scripts/verify_references.py` check (d), which also rejects an exception pointing at a path that no longer exists. A mechanism nothing calls is a regression, not a pending feature. Precedent: `/agents:harden` shipped in PR #29 and was never run against this repository — five platform controls sat disabled for weeks — while `contract-writer` was built for `revdoc` Phase 6 and that phase never named it. The check must resolve Python **imports**, not just filename mentions: `merge_json.py` looked orphaned to a filename-only scan while `install.py` depends on it, and deleting it would have broken the bridge installer.

### RA-17: GATE_VERDICT_CLASSES

Phase 7 emits `APPROVED` \| `REJECTED` \| `RECORD` with class `charter` / `instructing` / `testifying`, and a severity `S0`-`S3` per finding (the row's `Severity` cell holds the highest, or `none`). `RECORD` does not count toward remediation. Procedure: `rules/qa_and_testing.md` §4.

### RA-18: CURSOR_PHASE1_NO_PLAN_MODE

Under `session_tool: cursor`, Phase 1 MUST NOT invoke `SwitchMode` to plan — that mode forbids writing the deliverable. Write `IMPLEMENTATION_PLAN.md` at the canonical sprint path in the current session. A file under `~/.cursor/plans/` is not the `triple_lock` plan. Procedure: `pipeline_workflow.md` Phase 1.

## §8 Supply Chain Security

### min_release_age

`minimumReleaseAge: 1440` (minutes, i.e. 24 hours) MUST be set in `pnpm-workspace.yaml` to avoid zero-day compromised packages. Verified by: `pnpm config get minimumReleaseAge` → `1440`.

### only_built_deps

All dependencies requiring build scripts MUST be explicitly whitelisted in `onlyBuiltDependencies` in `pnpm-workspace.yaml`. Verified by: `pnpm config get onlyBuiltDependencies` lists exactly the whitelisted packages.

### config_file

**`.npmrc` does NOT carry these settings.** Measured with pnpm 11.23.0: `minimum-release-age=1440` and `ignore-scripts=true` written in `.npmrc` both return `undefined` from `pnpm config get`, so a project that followed the earlier wording of this section had the 24-hour floor **off** with no error. The same keys in `pnpm-workspace.yaml` return `1440` and `true`. A host whose `.npmrc` still holds them MUST move them; leaving them there is harmless but enforces nothing (`F-115-N1`, Sprint 054).

## Text outside the rule rows

### Preamble of agents.md

This is the governance ruleset of the Token-Optimized Agent Pipeline (`.agents`). It dictates in an absolute and transversal manner the behavior of subagents, code quality, and topological design.

### feedback_upstream (routing part of the row)

**Canonical statement of the learning flow.** `§3 jurisdiction` and `workflows/extract_workflow.md` both point here *and* carry a compressed restatement of the framework-class path — grep both on every patch to this row (`RA-14`). `§3 strict_rule` is the prohibition this flow routes around, not a pointer to it. Learning is a LIVING three-tier flow, never a dead end. Each candidate carries a `routing_class` (`extract_workflow.md` Phase 2 — `host` \| `profile` \| `nucleus` \| `discard`): **host-class** findings stay in the host's `memory_index.json`; **project-family-class** findings route to `profiles/[name]/` (rules/skills/docs) — for a real project, the host-controlled profile path installed with `scripts/install.py --profile-path`, never `profiles/` inside the public nucleus (`RA-15`); **framework-class** findings (would improve every host) MUST become a nucleus contribution — a rule-amendment proposal or fix PR to the `.agents` repo.

### Core vs. Auxiliary

**Core vs. Auxiliary.** The 8 roles above are the *Core Pipeline Roles* (mandatory in every Planning → Sprint Closeout cycle). `governance_learner`, `doc_orchestrator`, `topology_mapper`, `git_sync_agent`, `token_economy_agent`, and `implementer_agent` (see `agents/*.md`) are **Auxiliary Agents** — invoked as needed (knowledge distillation, documentation, topology, upstream sync, **code/test authorship**) but not a mandatory stop on every pipeline pass. **Project-specific specialists** (e.g. `backend_identity_specialist`, `frontend_ux_hardener`) live in `profiles/[name]/agents/` and only join the pipeline when their profile is installed. Their absence from this table is intentional, not an omission.

### Onboarding order note

Steps 2 and 3 are frequently confused because they are adjacent: `standardization` migrates *artifacts*, `revdoc` documents *code*. Different objects, and until Phase 019 no document declared which ran first.

### Execution pipeline note

The normative 8-phase pipeline (Planning → Sprint Closeout) is defined **exclusively** in `workflows/pipeline_workflow.md`, loaded on demand via `/agents:pipeline`. It is not duplicated here to keep the always-loaded governance ruleset lean and drift-free. Non-negotiables enforced at this level: the Approval Gate (Phase 5) is a single attended human authorization — never wrapped in an unattended `/loop` — and all execution happens on `ai-sprint/[ID]` (RA-12).
