# Phase Register — Sprint 055 (`sandbox-restrictions-and-secret-path`)

No `PHASE_REGISTER_TEMPLATE.md` exists in `docs/standards/templates/` — still open as
`KI-052-8`, not invented for this file. Built from `config/artifact_registry.json`
(entry `PHASE_REGISTER.md`: Phase 8, writer `doc_orchestrator`, `required: false`) and
from `SPRINT_LOG.md`, `IMPLEMENTATION_PLAN.md`, `task_scope.md`, `SANDBOX_MEASUREMENT.md`
and `docs/audits/PIPELINE_AUDIT_REPORT-055.md`, following only the section shape of
`docs/sprints/054-core-pipeline/PHASE_REGISTER.md`.
Commit range of the sprint: `16c3cca..7cc668a` (141 commits, branch `ai-sprint/055`) when this
register was written; the close commits that follow it are in `git log 7cc668a..` on the branch.
The plan was first committed as `890c8e3` (`SPRINT_LOG.md`, Phase 3). Written while Phase 8
is in progress, so the Phase 8 row lists only what has been done.

| Phase | Deliverable | Evidence (path / SHA) | Verdict / Status | Deviations |
| :--- | :--- | :--- | :--- | :--- |
| 1 · Planning | `IMPLEMENTATION_PLAN.md` (19 units `U01`..`U19`, decisions `D1`..`D9`) | `docs/sprints/055-core-pipeline/IMPLEMENTATION_PLAN.md`, committed `890c8e3` before Phase 5; `audit_plan.py` exit `0`; base `16c3cca` with `make verify` exit `0`; scope: `F-115-N2` rows `S-1`..`S-8`, Chromium, graphify API key, `RA-09` secret path moved to `scripts/with_env.py` | Complete | `D1` named a human-launched interactive session; an agent Bash tool has no TTY and the human's attempt failed with `Input must be provided either through stdin or as a prompt argument when using --print`. U01 ran in headless `claude -p --settings <overlay>` sessions instead (`SANDBOX_MEASUREMENT.md` §1.1). Planning session reached session-cost ratio 5.0, so execution dispatched every unit to a subagent |
| 2 · Environment Readiness | none (precondition) | No dedicated `devops_agent` entry in `SPRINT_LOG.md`; evidenced by `make verify` exit `0` at `16c3cca` (Intelligence State) and by Phase 6 and 7 | Satisfied | No explicit Phase 2 line in `SPRINT_LOG.md` |
| 3 · Roadmap Drafting | `SPRINT_LOG.md` + branch `ai-sprint/055` | Branch `ai-sprint/055` cut from `main` (`RA-12`); anchor opened; plan committed `890c8e3` | Complete | None recorded |
| 4.1 · Agent Assignment | `agent_assignment.md` | `docs/sprints/055-core-pipeline/agent_assignment.md`; `check_forge_ladder.py` exit `0`; added in `abf2928` | Complete | None recorded |
| 4.2 · Skill Assignment | `skill_assignment.md` | `docs/sprints/055-core-pipeline/skill_assignment.md`; added in `abf2928` | Complete | `U12` (`skills/graphify/SKILL.md`) omitted: judged vendored (bulk import `cde6a71`, upstream sponsor line 747; `rules/skills_and_integrations.md §3`); the 7-key correction moved to `U11` |
| 4.3 · Rule Audit | `task_scope.md` | `docs/sprints/055-core-pipeline/task_scope.md`; `check_task_scope.py` exit `0`; amendment units `U22`..`U45` appended (24 rows) | Compliant | `U20` added: Phase 4.3 found `agents/devops_agent.md:16` still prescribing environment exports (`RA-14`). Escalation of `U02`, `U07`, `U13` to effort `high` declared as a Phase 4.3 proposal, not a `token_economy_agent` verdict |
| 5 · Approval Gate | none (human authorization) | Approved by GstMirabal on 2026-10-07 against plan commit `abf2928` (Approval table) | `APPROVED` — `triple_lock` lock 1 | Single attended invocation. Later human decisions on five amendments (see Human decisions) |
| 6 · Execution | Atomic commits on `ai-sprint/055` | Measurement `27210b1` (U01). Wrapper and template: `25dda50`, `6a090a4`, `ddd5bc7`, `f4986b5`, `6773f34`, `3ad277f`. Docs: `e589f19`, `056a5e3`, `c716b7f`, `d6b2649`, `f53b7fe`, `024ecd1`, `664c931`, `30d0a50`, `e5532cc`, `c8a4f8b` (`F-115-N2` closed), `739a750`. Gate 1 round 1 remediation `e68ac72`, `1fa9608`, `cfe7950`, `5ce803b`, `90e4a16` (U22), docs `e9848b6`..`fa9dc87`. Amendment 1: `660d278`, `b5b3088`, `17c67f8`, `88f5c90`, `e9dba4e`, `55911a1`, then `U29` `b68dbcc`..`032fcf6`. Amendment 2: `fb23f31`, `b1f246c`, `7580443`, `894108f`, `3fd788e`, then `U35` `952e47e`..`918e45a`. Amendment 3: `8fd097f`, `485dc39`, `e48c621`, `1efc190`, `dc72d78`, `e40c3e0`, `6796e92`, `52c6118`, `f09e148`, `584e003`. Amendment 3a: `caa546f`, `99001b7`, `a18bb53`, `a910f4c`, `e386ff7`, `3db5ecb`, `5af9fea`, `de35d1e`, `b508948`. Amendment 3b: `d077524`, `3dcf5eb`, `895c1a7`, `aff118a`, `e310f1c`, `c3feafa`, `8f029a4`, `0836a9c`, `fdeec95`, `bc3f9dd`, `22e9670`, `6a2b93c`. Outcome: `make verify` exit `0` (1081 passed) at the last gated head | Complete | See Deviations list below the table |
| 7 · Quality Gate | Eight rows in `SPRINT_LOG.md` (`Gate \| Round \| Verdict \| Class \| Notes`) | See Gate history below | QA Gate 1 `REJECTED` rounds 1-6 (classes: `charter` x5, `instructing` x1), then `RECORD` (`testifying`) at round 7; Tester Gate 2 `RECORD` (`testifying`) at round 1 | Fourth consecutive `REJECTED` triggered `remediation_workflow.md` (negative KI `RA-19`, `f8dc545`); round 5 was treated as the first gate on the Amendment 3 scope (remediation not re-run, human decision); round 6 carried the second `remediation-regression` label of the sprint, so the block was stopped and re-planned (`rules/qa_and_testing.md` §4, Amendment 3b) |
| 8 · Sprint Closeout | `PHASE_REGISTER.md` (this file), `CHANGELOG.md` `[Unreleased]` (`739a750`, extended through `U45` `6a2b93c`) | `close_workflow.md` so far: `docs_freshness_check` structural-delta BLOCK (053→055 `node_delta` 8883 > p90 5864) resolved via `docs/audits/PIPELINE_AUDIT_REPORT-055.md` (`cbff45f`); `graph_stats.json` 13240/18156/1059 (`d2a43f0`); model ledger regenerated (`e990410`); `readme_counts` exit `0`; `repo_docs_check` — `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md` present and not invalidated, `NOTICE.md` applies (vendored skills) and unchanged; `rules_optimization` skipped: skillopt stack absent; extract candidates human-confirmed at Phase 2.5 and routed `KI-055-1`..`KI-055-7` (`61a63ca`), `memory_index.json` `F-20261011-S551` (`7cc668a`); Phase 2.6 `check_task_scope` 0, `check_gate_log` 0; `current_sprint.last_audit_sprint` advanced `53` → `55` in the local anchor (gitignored); `memory_wipe`, platform recheck, release, push and deployment follow | In progress | None recorded yet |

### Deviations (Phase 6 and amendments)

| ID | Deviation | Human decision / record |
| :--- | :--- | :--- |
| D1 | Headless measurement instead of a human-run interactive session (see Phase 1). Control runs `SBX0`/`SBX1` record that the sandbox was active; a relative `denyRead` in a `--settings` file resolved against that file's directory and left `.env` readable until the run was repeated with absolute paths; `sandbox.network.allowMachLookup: true` on CLI 2.1.119 silently disabled the whole sandbox, so `D6` resolved to Branch B (human-run browser verification) | `SANDBOX_MEASUREMENT.md` §1.1-§1.4, §4 |
| U04 | Omitted: `D4` revised after a sandboxed measurement — `./.env.*` stays in `denyRead` and a narrower `allowRead` reopens `.env.example`/`.env.sample`/`.env.template`, so no template value retires and no merge-prune is needed | `SPRINT_LOG.md` Sprint Progression |
| U12 | Omitted (vendored file, see Phase 4.2) | `SPRINT_LOG.md` |
| U17 | No change needed: the `Rule 66` concordance row stays accurate after `U13` | `SPRINT_LOG.md` |
| U20, U21, U22 | Added after approval: `U20` by Phase 4.3, `U21` because the new script and registry drifted the README At a Glance counts (`make verify` exit `2`; `e5532cc`), `U22` (`RETIRED_VALUES` pruned inside `merge()`, `90e4a16`) by the human on 2026-10-07; `U22` deviates from the `prune_deprecated_hooks` idiom, which is called separately from `main()` | `SPRINT_LOG.md` resume pointer |
| Amendment 1 (`U23`..`U29`) | Plan *Enmienda* after Gate 1 round 2: absolute rendered exclusions (`D2-R`), `D2-N`, `D3-R`, `D10`, `D11`; Abort criterion 3 added | Approved by GstMirabal 2026-10-10, plan commit `80dac85`, approval `d1c0b49` |
| Amendment 1 execution deviations (recorded at `U23`) | `D2-N` is moot: `install_nucleus_bridge` merges no sandbox template (`nucleus_neutrality`), so `U23` renders in host mode only. `D2-R` denies `.agents/{scripts,config,venv_skillopt}` instead of all of `.agents`, because the boot writes `.agents/.bridge_*.lock` from inside the sandbox; `SANDBOX_MEASUREMENT.md` §8 `R5` shows the subdirectory denies still block renaming `.agents` | `SPRINT_LOG.md`; `SANDBOX_MEASUREMENT.md` §7, §8 |
| `R2-6` | `1fa9608` trailer names `9823a56` as the failing parent; the real parent is `e68ac72`; history not rewritten | `SPRINT_LOG.md` |
| Amendment 2 (`U30`..`U35`) | Plan *Enmienda 2* after round 3: no `sandbox.excludedCommands` at all (`D12`, the Abort criterion 3 fallback), write-denies for hook trees (`D13`); `D2-N`, `D2-R`, `D10` withdrawn | Approved by GstMirabal 2026-10-10, plan commit `409da6e`, approval `dfaa81a` |
| Amendment 3 (`U36`..`U41`) | Plan *Enmienda 3* after the remediation lock: scope cut, no secret boundary claimed for the sandboxed agent (`D14`), `Q1`-`Q5`, `Q7`, `Q11` routed as `F-055-N1` (`D15`), `Makefile` comment (`D16`) | Option 1 chosen by GstMirabal 2026-10-11, plan commit `c47f450` |
| Amendment 3a (`U42`, `U43`) | `D17` no prescribed git pre-check, `D18` G5-2/R5-1/R5-2/R5-4; Verification grep narrowed in `63b6c2b` and dry-run before the units ran | Chosen by GstMirabal 2026-10-11, plan commit `dc8185b` |
| Amendment 3b (`U44`, `U45`) | `D19` one canonical warning and zero procedures, `D20` `with_env.py` covers only its three graphify names, `D21` round 6 records | Chosen by GstMirabal 2026-10-11, plan commit `2f52524` |
| Residue routed | `Q8`, `Q9` (= `N6`), `Q10`, `R5-4`, `R7-4`, `R7-5`, `T2-1` routed to Sprint 056; `F-055-N1` open | `KI-055-1`..`KI-055-7` below |

## Gate history (Phase 7)

| Gate | Round | Verdict | Class | Range | Evidence | What the round changed |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| QA Agent (Gate 1) | 1 | `REJECTED` | `charter` | `16c3cca..30c2e05` (last commit before the round 1 transcription `9823a56`) | `check_fix_reproduces` 0 (3 `fix(` OK), ruff 0, quality-audit 0, `make verify` 0. Blockers F1-F8, record F9 | `e68ac72`, `1fa9608`, `cfe7950`, `5ce803b`; docs `e9848b6`..`fa9dc87`; plan `D4`/`T1`/`T5`/row 3 amended (F7); `U22` `90e4a16` |
| QA Agent (Gate 1) | 2 | `REJECTED` | `charter` | `16c3cca..43e4c5d` | 5 `fix(` OK, `make verify` 0 (1047 passed). Blockers R2-1..R2-3 (`R2-3` carries `remediation-regression`), record R2-4..R2-9 | Amendment 1 (`U23`..`U29`) |
| QA Agent (Gate 1) | 3 | `REJECTED` | `charter` | `16c3cca..edc7564` | 8 `fix(` OK, `make verify` 0 (1073 passed), CHANGELOG 50/50 SHAs. Blockers N1-N5 measured on CLI 2.1.119; record N6, N7 | Amendment 2 (`U30`..`U35`) |
| QA Agent (Gate 1) | 4 | `REJECTED` | `charter` | `16c3cca..0c6fe03` | 10 `fix(` OK, `make verify` 0 (1081 passed), CHANGELOG 62/62. Blockers Q1-Q6, `N3` open, `N5` reopened. Fourth consecutive `REJECTED`: `RA-01` / `remediation_workflow.md` Phase 0 | Remediation run 2026-10-10 (Phases 1-3; negative KI `RA-19` `f8dc545`; session locked); human option 1 on 2026-10-11 produced Amendment 3 |
| QA Agent (Gate 1) | 5 | `REJECTED` | `charter` | `16c3cca..8a96215` | `make verify` 0 (1081 passed), CHANGELOG 73/73. Blockers G5-1 (`instructing`), G5-2 (`charter`); record R5-1..R5-5 | Amendment 3a (`U42`, `U43`); remediation not re-run (human decision) |
| QA Agent (Gate 1) | 6 | `REJECTED` | `instructing` | `16c3cca..ff3a5da` | `make verify` 0 (1081 passed), CHANGELOG 81/81. Blockers H1 (second `remediation-regression`), H2; record R6-1..R6-8 | Block stopped and re-planned: Amendment 3b (`U44`, `U45`) |
| QA Agent (Gate 1) | 7 | `RECORD` | `testifying` | `16c3cca..da585c1` | 10 `fix(` OK (3 JSON-only with manual `Repro`), `make verify` 0 (1081 passed), CHANGELOG 92/92. Record R7-1..R7-5 | `R7-1`..`R7-3` fixed in sprint artifacts after the verdict; `R7-4`, `R7-5` routed to Sprint 056 |
| Tester Agent (Gate 2) | 1 | `RECORD` | `testifying` | `16c3cca..26de887` | pytest 1081 passed / 0 failed / 0 skipped, `make verify` 0, seven sprint test files 99 passed; hands-on fixture checks of `with_env.py`, `merge()` and `prune_rendered_exclusions`. Record `T2-1` | `T2-1` routed to Sprint 056 (`KI-055-3`) |

## Human decisions

| Date | Decision | Where recorded |
| :--- | :--- | :--- |
| 2026-10-07 | Approval of the plan at commit `abf2928`; wrapper `scripts/with_env.py` as the sanctioned secret path (`D2`); `U22` added | Approval table; `SPRINT_LOG.md` |
| 2026-10-10 | Gate 1 round 2: absolute rendered paths (`D2-R`, `D2-N`), remove `gh pr create *` and `gh release create *` (`D10`), allowlist nucleus-only (`D3-R`) | Amendment 1; `80dac85`, `d1c0b49` |
| 2026-10-10 | Gate 1 round 3: no `excludedCommands` at all (`D12`); fix hook trees in this sprint (`D13`) | Amendment 2; `409da6e`, `dfaa81a` |
| 2026-10-11 | After the remediation lock: option 1, scope cut and close (`D14`..`D16`) | Amendment 3; `c47f450` |
| 2026-10-11 | Gate 1 round 5 treated as first gate on the Amendment 3 scope; no git pre-check prescribed (`D17`) | Amendment 3a; `dc8185b` |
| 2026-10-11 | Gate 1 round 6: one canonical warning, zero procedures (`D19`..`D21`) | Amendment 3b; `2f52524` |
| 2026-10-11 | Phase 2.5 extract candidates confirmed and routed | `61a63ca`, `7cc668a` |

## Known items opened (extract candidates)

All seven are transcribed in `docs/roadmaps/core/pipeline/021-030-program-queue.md`
(commit `61a63ca`), each routed to Sprint 056.

| KI | Finding | `routing_class` | Opened by |
| :--- | :--- | :--- | :--- |
| `KI-055-1` | `F-055-N1`: unsandboxed execution entry points stay agent-writable (`Q1`-`Q5`, `Q7`, `Q11`); deliverable is the `RA-19` enumeration | `nucleus` | QA Gate 1 round 4 |
| `KI-055-2` | `Q8`: `install.py` keeps host-added `sandbox.excludedCommands` silently | `nucleus` | QA Gate 1 round 4 |
| `KI-055-3` | `prune_rendered_exclusions` residue: `Q9`, `Q10`, `T2-1` | `nucleus` | QA Gate 1 rounds 3-4 (`N6`, `Q10`), Tester Gate 2 round 1 (`T2-1`) |
| `KI-055-4` | `R5-4`: `branch_sovereignty.py`, `ci_gate.py`, `session_probe.py` call `gh` from agent-driven steps | `nucleus` | QA Gate 1 round 5 |
| `KI-055-5` | Documentation residue `R7-4`, `R7-5`, `PIPELINE_AUDIT_REPORT-055.md` F1-F4 | `nucleus` | QA Gate 1 round 7, close audit |
| `KI-055-6` | `RA-19` amendment proposal: extend the ban to prescribed safety procedures without the enumeration | `nucleus` | QA Gate 1 round 5 |
| `KI-055-7` | `current_sprint.last_audit_sprint` is written by no script | `nucleus` | `PIPELINE_AUDIT_REPORT-055.md` F5 |

Heuristic harvest without a KI (`SPRINT_LOG.md` table): two pre-existing mechanisms load
`.env` directly, bypassing `scripts/with_env.py` (`mcp_servers/github_mcp/scripts/check_health.sh:14`,
`skills/skillopt/scripts/train_runner.py:23`), left human-run and out of scope; an
`excludedCommands` pattern covering a working-tree script lets the agent rewrite the script and
run it unsandboxed.
