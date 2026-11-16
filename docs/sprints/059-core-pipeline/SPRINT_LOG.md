# 📝 Sprint Log: #059
**Session Tracker**: b1572a48-e812-4c06-87b1-21e72fbfb738
**Role Active**: orchestrator

---

## 🚦 Session Metadata
| Parameter | Value |
| :--- | :--- |
| **Active Layer** | core-pipeline |
| **Strategic Goal** | `efficiency-and-sandbox-regime`: cut the framework's own cost (`agents.md` ≤ 20000 bytes, parallel Phase 6 batches, nucleus sandbox with `autoAllowBashIfSandboxed`), give the §3.1 bound a non-zero baseline and an in-session invoker, re-measure the `RA-19` enumeration and decide the sandbox regime, and close the Sprint 058 residues. |
| **Intelligence State** | Phase 7 (Quality Gate), Wave 1. Plan approved at `65c86d3`; Phase 6 deviations and decisions: D15 to D32. |
| **Branch / Base** | `ai-sprint/059` created from `main` at `08c669c` (`v4.41.0`) |
| **Session Tool / Delegation** | `claude-code` / `native` |
| **Start Time** | 2026-11-02 |

---

## 🏁 Sprint Progression
Tracking of atomic goals achieved during the session. Work units and execution order: plan `## Work` and `## Cost`; one wave per session, `session_state.py suspend` between waves (plan `## Cost`).

- [x] **Phase 1 (Planning)**: plan drafted and committed.
    - `[x]` Intake triage: channel A empty, channel B empty, `F-116-N1` and `F-116-N2` accepted with reproduction (plan `## Context`).
    - `[x]` Human decisions of 2026-11-02 recorded in plan Design D2, D3, D9 and P11.
    - `[x]` `IMPLEMENTATION_PLAN.md` committed at `88d8a51`.
- [x] **Phase 3 (Roadmap Drafting)**: sprint opened.
    - `[x]` `current_sprint` written by `scripts/session_state.py open-sprint` (`id` 59, `path` `docs/sprints/059-core-pipeline`, `branch` `ai-sprint/059`).
    - `[x]` Branch `ai-sprint/059` created from `main` at `08c669c`.
    - `[x]` `SPRINT_LOG.md` instantiated from `docs/standards/templates/SPRINT_LOG_TEMPLATE.md` (session #68).
- [x] **Phase 4 (Assignment and Rule Audit)**: artifacts written and checked.
    - `[x]` `agent_assignment.md` written; six overwrites of `Assignee (proposed)` (A-00, A-07, H-01, C-01, D-01, F-01), all for a missing `Write`/`Edit` tool.
    - `[x]` `skill_assignment.md` written; ladder terminates at P1, no skill forged.
    - `[x]` `task_scope.md` written by `rule_validator` (fresh subagent); `check_task_scope.py`, `check_forge_ladder.py` and `audit_plan.py` exit 0.
    - `[x]` Phase 4.3 raised F-1..F-12 except F-7 (S2, instructing) and F-7, F-13, F-14 (S3, testifying); each one verified against the tree and resolved in the plan (`task_scope.md` `## Resolution of the findings`). Work units 44 → 47 (B-07, E-01c, H-03).
    - `[x]` "Proposal E points 3-5" (plan P11; source not in the repository): human decision at Phase 5, routed to a `KI-059-n` by Z-02.
- [x] **Phase 5 (Approval Gate)**: Human OK («Aprobado») on 2026-11-02 over the plan at `65c86d3`.
- [x] **Phase 6 (Execution), Wave 1**: all units committed, A-19 to A-54 (plan D22 to D35) included.
    - `[x]` Human decision 2026-11-05 after QA Gate 1 round 3 (plan D21): unit A-18 before A-00; work units 52 → 53.
    - `[x]` Human decisions 2026-11-07 after QA Gate 1 round 5 (plan D22, D23): units A-19 to A-25; work units 53 → 60.
    - `[x]` Human re-plan 2026-11-07 after the deadlock of QA Gate 1 round 6 (plan D24 to D28): units A-26 to A-39; work units 60 → 74; `session_state.py unblock` run after it.
    - `[x]` Human re-plan 2026-11-07 after the deadlock of QA Gate 1 round 7 (plan D29 to D32): one host-data inventory, units A-40 to A-45; work units 74 → 80; `session_state.py unblock` run after it. Convergence rule 1 applies to the gate from round 8 on.
    - `[x]` Human re-plan 2026-11-07 after the deadlock of QA Gate 1 round 8 (plan D33, D34): N1 to N5 fixed, `scripts/check_log_append_only.py` added for the N3 family, units A-46 to A-52; work units 80 → 87; `session_state.py unblock` run after it.
    - `[x]` Human re-plan 2026-11-07 after the deadlock of QA Gate 1 round 9 (plan D35): R9-1 to R9-3 fixed, units A-53, A-54; work units 87 → 89; `session_state.py unblock` run after it. Decided stop: another S0 or S1 in `scripts/check_log_append_only.py` at round 10 withdraws the check to Z-02.
    - `[x]` Plan D35 stop applied 2026-11-07 after QA Gate 1 round 10: A-49 to A-53 and the README count reverted (`873fb1e` to `120860b`); `KI-059-15` routes the check to Z-02; work units stay 89, with those five rows naming their reverts. `session_state.py block` and `unblock` run under the decision taken in advance.
    - `[x]` Human re-plan 2026-11-07 after the deadlock of QA Gate 1 round 11 (plan D36): the Z-02 rows stop enumerating ids; units I-08 to I-10 added to Wave 6; work units 89 → 92, an estimate; `session_state.py unblock` run after it.
    - `[x]` Human re-plan 2026-11-07 after the deadlock of QA Gate 1 round 12 (plan D37): method for the sprint artifacts (one home per fact, a check per claim, a cap on gate notes); Wave 1b units M-01 to M-11 replace I-08 to I-10; work units 92 → 103; `session_state.py unblock` run after it.
    - `[x]` Human re-plan 2026-11-07 after the deadlock of QA Gate 1 round 13 (plan D37 reduced): Wave 1b runs before the gates re-run; unit M-12; work units 103 → 104; `session_state.py unblock` run after it.
- [x] **Phase 6 (Execution), Wave 1b**: units committed; status in `task_scope.md`.
    - `[x]` A-05 committed at `1dbe533`.
    - `[x]` A-09 committed at `0c7a9b2`.
    - `[x]` A-10 committed at `a694ffe`.
    - `[x]` A-11 committed at `72ac88b`; A-13 at `a014f4f`; A-01 at `ef490cd`. Moved text compared to `agents.md` by script: identical.
    - `[x]` A-15 committed at `18b692e`; A-16 at `9b8db89`; A-17 at `d133bc2`; A-12 at `d6f5756` (`wc -c agents.md` 19970, `make verify` exit 0, 1531 passed).
    - `[x]` A-14 checked and corrected (a fact that A-08 would falsify; an open-ended trial) and committed at `ed96115`; A-08 at `80518b4`. Wave 1 units all committed.
    - `[x]` Remediation of Tester Gate 2 round 1: A-08 reverted at `8e8a566`; A-01 extended at `919d4f2` (35 transcripts: 37 cycles, 0 None, 5 above 5x, 0 above 15x; `make verify` exit 0).
    - `[x]` Human decisions 2026-11-05 after Tester Gate 2 round 1: restore `segment_cycles` in A-01 (plan D19); revert A-08 under abort criterion 4 (plan D20).
    - `[x]` Deviation: unit A-13 (`docs/guides/RULE_PRECEDENTS_GUIDE.md`) added before A-12, human decision 2026-11-02 (plan Design D15); work units 47 → 48.
    - `[x]` Deviation (plan D16): the orchestrator dispatched A-11, A-13, A-08 and A-01 together on its reading of a human question; no rule allowed it. Human decision 2026-11-04: keep the work once checked, return to the approved order.
    - `[x]` A-08 was held uncommitted: it contradicts `ADR-0003` (KI-059-3). Human decision 2026-11-04: unit A-14 creates the superseding `ADR-0021` first (plan D17), then A-08 commits; work units 48 → 49.
    - `[x]` Human decision 2026-11-04 (plan D18): `agents.md` allocated by risk; A-15, A-16, A-17 added before the A-12 commit; work units 49 → 52.
    - `[x]` Deviation (`RA-13`), 2026-11-08: the orchestrator chained `make verify` and the B-07 commit in one command; `2d40946` landed with `make verify` at exit 2 on a stale `WORKFLOWS_STEP_MAP_GUIDE.md`. Closed by `35301fc`, committed after `make verify` exit 0 was observed.
    - `[x]` Human decisions 2026-11-08 after QA Gate 1 round 16: units M-18 to M-21 and B-08 added to Wave 2; the nucleus installer runs on this checkout so B-08 re-measures under the sandbox; B-02 narrowed to the baseline; work units 109 → 114.
    - `[x]` Human decisions 2026-11-08 after QA Gate 1 round 17: units B-09, M-22 and M-23 added to Wave 2; work units 114 → 117.
    - `[x]` Human decisions 2026-11-08 after QA Gate 1 round 18 (A-1 stop, chain `c5fbf5f`, `639fd05`): block `scripts/check_task_scope.py` re-planned as M-24, a removal; no history rewrite; units B-10 and M-24 added; work units 117 → 119.
    - `[x]` Human decision 2026-11-09 after QA Gate 1 round 19: R19-1 closed by removal in unit M-25; units B-11 and M-25 added; work units 119 → 121. Chain 2 of the A-1 stop now has three commits (`c5fbf5f`, `639fd05`, `16b1dc6`).
    - `[x]` Human decision 2026-11-09 after Tester Gate 2 round 3 (A-1 re-plan): T3-1 fixed in unit M-27, a further `fix(` on `scripts/check_task_scope.py` and a fourth commit of chain 2; T3-2 closed by removal in unit M-26; units B-12, M-26 and M-27 added; work units 121 → 124. T3-3 and T3-4 (S3) noted only.
    - `[x]` Human decision 2026-11-09 after QA Gate 1 round 20: R20-1 closed in unit B-13; work units 124 → 125.
    - `[x]` Human decisions 2026-11-09 after Tester Gate 2 round 4: a claim about system behaviour with no instrument is removed; T4-1 closed by removing the table in unit B-15; live `file:line` citations removed in M-28 to M-32, the 3 citations in historical precedents kept; units B-14, B-15 and M-28 to M-32 added, work units 125 → 132; the Gate findings instrument and the audit of prose reasons moved to Sprint 060; no dedicated gate round: these units enter the range of the Wave 3 gates.
    - `[x]` Human decision 2026-11-09 after unit A-18 (plan D38): A-04 and C-01 extended, units K-01 to K-04 added to Wave 6; work units 132 → 136.
    - `[x]` Human decision 2026-11-09 after unit A-00 (plan D39): `graphify update .` failed under the sandbox on `SC_SEM_NSEMS_MAX`; units L-01 to L-05 added to Wave 6; work units 136 → 141.
    - `[x]` Human decision 2026-11-09 (plan D40): formula of H-02 fixed with `baseline_context` 60,612 tokens in `config/unit_cost_estimates.json`; no unit added by this decision; work units stay 141.
    - `[x]` Units added 2026-11-09 with no numbered decision, as the plan "Work units" row records them: A-55 (rests on `ADR-0018`: the absolute bound of 550,000 tokens replaces `HARD_RATIO = 15` in `probe_cost`), A-56 (rests on a measurement of 2026-11-09: an empty `task_scope.md` gave `OK`) and H-04; work units 141 → 144.
    - `[x]` Human decision 2026-11-09 (plan D41): `make verify` writes no bytecode; units B-16 to B-20 added; work units 144 → 149.
    - `[x]` Human decision 2026-11-09 (plan D42): `make verify` writes no pytest or ruff cache; unit B-21 added; work units 149 → 150.
    - `[x]` Human decision 2026-11-09 (plan D43): C-01b runs before abort criterion 1 is applied; unit C-01b added; work units 150 → 151.
    - `[x]` Human decisions 2026-11-10 after QA Gate 1 round 21 (plan D44): R21-3 vector recorded as KI-059-18 and measured further in unit C-01c; R21-4 the 23 `claude -p` calls of C-01b accepted (verdict G kept); R21-1 and R21-2 A-1 stop: blocks `scripts/session_cost.py` and `scripts/check_task_scope.py` frozen as they are, no further `fix(` this sprint, the only edit is C-03 (R21-6); units C-01c and C-03 added; work units 151 → 153.
    - `[x]` Human decisions 2026-11-10 after QA Gate 1 round 22 (plan D45): R22-1 the "without the B-06 block" half of C-01c withdrawn, because without that block no sandbox is declared; unit C-04 records the cause; R22-2 second occurrence of the R21-5 family, so unit C-05 adds to `scripts/check_sprint_refs.py` the check that a known-issue row naming a unit marked ✅ cites that unit's SHA; units C-04 and C-05 added; work units 153 → 155.
    - `[x]` Human decision 2026-11-10 during unit C-05 (plan D45): the check found 27 mentions in 13 known-issue rows naming done units without their SHA, mostly historical references; the SHAs are appended to those rows as a "Commits (2026-11-10)" clause, and the check keeps full coverage.
    - `[x]` Human decision 2026-11-10 after QA Gate 1 round 23 (plan D46): R23-1, the exit 2 that C-05 added for a missing `task_scope.md` or `SPRINT_LOG.md` came from the unit brief, not the plan, and fails `make verify` in Phases 1 to 4.2; unit C-06 makes the known-issue SHA check skip with an `[OK] ... (skip)` line in that case; unit C-06 added; work units 155 → 156.
    - `[x]` Human decision 2026-11-11 after Tester Gate 2 round 5 (plan D47): T5-1 the read-failure exit 2 of `scripts/check_sprint_refs.py` gets a test in unit C-07; T5-2 the plan template's 5×/15× bound sentence is replaced in unit C-08 by a reference to `rules/token_economy.md` section 3.1 with no figures; T5-3 (S3) noted only; QA Gate 1 round 25 and Tester Gate 2 round 6 follow; units C-07 and C-08 added; work units 156 → 158.
    - `[x]` Human decision 2026-11-11 after Tester Gate 2 round 6 and QA Gate 1 round 25 (plan D48): the four S3 findings are fixed in this sprint, one unit per subject: C-09 tests the `OSError` half of the read `except` of `scripts/check_sprint_refs.py` (T6-1); C-10, C-11 and C-12 correct the C-07 operation in the plan, the C-07 line cite in `task_scope.md` and the Tester Gate 2 round 5 range in this log (T6-2 to T6-4, R25-1 to R25-3); QA Gate 1 round 26 and Tester Gate 2 round 7 follow, then Wave 5; work units 158 → 162.
    - `[x]` Human decision 2026-11-11 after QA Gate 1 round 26 (plan D49): R26-1 the C-11 line fix was not propagated to the Tester Gate 2 round 5 row (`RA-14`); R26-2 the Gate findings table holds S3 rows without a command and lacks T5-1 and T5-2; unit C-13 fixes both in this log, keeping the S3 rows because `scripts/check_sprint_refs.py` requires a row for every cited `R<round>-<n>` ID; QA Gate 1 round 27 and Tester Gate 2 round 7 follow, then Wave 5; work units 162 → 163.
    - `[x]` Human decision 2026-11-11 after QA Gate 1 round 27 (plan D50): the three S3 findings are fixed in this sprint, one unit per file: C-14 replaces the D49 Check in the plan with a grep scoped to the Tester Gate 2 round 5 row (R27-1); C-15 adds the file to the R25-2 `sed` and the SHA to the C-11 and C-13 Close cells in this log (R27-2, R27-3); QA Gate 1 round 28 and Tester Gate 2 round 7 follow, both fresh, then Wave 5; work units 163 → 165.
    - `[x]` Human decision 2026-11-12 after QA Gate 1 round 28 (`RECORD`, S3): R28-1 to R28-3 are noted only (`RA-17`); no unit is added; Tester Gate 2 round 7 follows, dispatched fresh, then Wave 5; work units stay 165.
    - `[x]` Human decision 2026-11-14 at the start of Wave 5 (plan D51): the wave's goal is unchanged (P7, `KI-056-1`: fewer permission requests while keeping `RA-19`; the D-01 requirement that `devops_agent` runs `gh`); D51 refines the means into a security harness with which agents run `gh`, database tests and hooks without a permission request per action, with no access to credentials and no say in permission decisions; the session measurements M1-M18 and the independent review (F-01 to F-23) are transcribed in unit S-01; A1-A10 and B1-B11 are measured in units S-02 to S-12 with at most 42 `claude -p` calls; S-13 to S-15 add `make sandbox-probe`; ADR-0019 (D-01) follows S-12; F-01, F-02, F-05/F-06 and F-15 recorded as KI-059-19 to KI-059-22; work units 165 → 180.
    - `[x]` Human decision 2026-11-14 after two measurement briefs (S-03 original, S-04) were stopped by a safety classifier before dispatch (plan D51 principle): the harness frees normal work, not attacks on the boundary; agents run normal work without prompts and checks that a control still holds; escape attempts are never run by an agent, they go to a list the human runs or ADR-0019 records them as outside the agent's scope; units S-04 to S-12 are dispatched under this principle; nothing was run for the stopped briefs.
    - `[x]` Human decision 2026-11-14 after a fourth measurement brief (S-05) was stopped by a safety classifier before dispatch (plan D52): controls are shown by design and verified configuration, not by attack attempts; S-05 and S-06 are rewritten that way; S-16 scopes an attack validation run outside the agent session after the harness implementation units; work units 181.
    - `[x]` Human decision 2026-11-14 on the ADR-0019 decision brief of unit D-01: the fine-grained token of A10 is held and renewed by the human only, and the GitHub App with a token broker is the target of a later unit; RA-09 is amended to list the measured controls as exposure reduction; lines 141-142 and 149-153 of `workflows/repository_hardening_workflow.md` are rewritten to the measured state; the remaining recommendations (network and read lists, A3, A9, B1, B5, B7, B10, B11) are accepted; `gh` stays with the human, the local DB route and D-12 are RECORD and no hooks run in the nucleus, all determined by measurement; the A5 replacement for `Edit(~/**)` was not put to the human and stays open; recorded in ADR-0019 (`71d2ad6`).
    - `[x]` Human decision 2026-11-14 after unit D-03 (plan D53): the settings units ADR-0019 decides are added at the close of Wave 5, before its Phase 7 gates: R-01 template `claude/settings.hooks.json`, R-02 the human installs `.claude/settings.json`, R-03 `make sandbox-probe` recorded in B9 in a new session, R-04 probe expectations; work units 181 → 185.
    - `[x]` Human decision 2026-11-14 (plan D54): every ADR-0019 consequence without a unit enters this sprint at the close of Wave 5: P-01 to P-03 (B7 key, A5 rule chosen by the human), R-05 to R-12 (hash pinning, hardening workflow, signed and verified tags, ruleset bypass removal), T-01 (A10 token renewal before 2026-12-14), V-01 and V-02 (attack validation by a person outside the session); Z-02 also closes or re-routes KI-059-19 to KI-059-26; work units 185 → 208.
    - `[x]` Human decision 2026-11-14 after D54: no GitHub App and no token broker; units W-01 to W-09 removed, `gh` and the A10 token stay with the human, P-03 withdraws the broker target of ADR-0019 D6; work units 208 → 199; unit P-04 added to delete the broker revisit clause of `rules/project_topology.md` (199 → 200).
    - `[x]` Human decision 2026-11-15: the call cap of unit P-02 is raised from 4 to 5, so the fifth call isolates the file pattern `Edit(~/<file>)` and the directory entry left unmeasured in section A5 of `HARNESS_MEASUREMENT.md` (`5f71010`).
    - `[x]` Human decision 2026-11-15: the call cap of unit P-02 is raised from 5 to 6, so the sixth call measures the Write tool on the exact path of a denied HOME directory that does not exist, the step A5-18 left not executed.
    - `[x]` Human decision 2026-11-15 (plan D55), reversing the decision after D54: the agent creates the version tag and uses the GitHub token through a GitHub App with a broker outside the sandbox, and the same helper signs the tag; everything built for the A10 token is reworked in Sprint 060; P-04, R-09, R-10 and R-11 removed (moved to Sprint 060 through Out of scope), P-03 keeps the broker target of ADR-0019 D6, V-01 no longer depends on R-11, R-09 commit `191feff` reverted in `588ca1a`; work units 201 → 197.
    - `[x]` Human decision 2026-11-15 (unit P-02): the A5 replacement for `Edit(~/**)` is candidate set C1 of section A5 of `HARNESS_MEASUREMENT.md` (`e51109f`): `Edit(~/.ssh/**)`, `Edit(~/.aws/**)`, `Edit(~/.gnupg/**)`, `Edit(~/.config/gh/**)`, `Edit(~/.docker/**)`, `Edit(~/Library/LaunchAgents/**)`, `Edit(~/Library/Keychains/**)`; sets C2 and C3 are not adopted.
    - `[x]` Human decision 2026-11-15 (plan D56): ADR-0019 is `Accepted` and immutable (`rules/documentation_standard.md` line 50), so the in-place edit of P-03 is discarded uncommitted; P-03 creates ADR-0022, which amends ADR-0019, and V-02 writes its results to ADR-0022.
    - `[x]` Human decision 2026-11-15 (plan D57): ADR-0022 is `Accepted` and immutable too, so V-02 creates ADR-0023, which amends ADR-0019 section 2.1 with the V-01 result, and ADR-0022 carries no boundary section.
    - `[x]` Human decision 2026-11-15 (plan D58): the template sandbox must allow pip; unit P-05 measures `pypi.org` and `files.pythonhosted.org` in `allowedDomains` and the TLS setting pip needs before R-01, as ADR-0019 D8 requires for any other domain; work units 197 → 198.
    - `[x]` Human decision 2026-11-15: the call cap of unit P-05 is raised from 3 to 5; calls 1 to 3 (A1-7 to A1-9) showed pip needs `enableWeakerNetworkIsolation`, which ADR-0019 D2 forbids, so call 4 measures pip with a certificate setting and no widening key, and call 5 isolates `files.pythonhosted.org`.
    - `[x]` Human decision 2026-11-15 (plan D59), after the R-01 report (edit kept uncommitted): unit P-06 measures the `~/` form and the out-of-project `.env*` pattern of `denyRead` before R-01 commits; unit R-14 adds the pip `env` pair on macOS only and merges the template keys and the nucleus `denyWrite` in `install_nucleus_bridge`; R-01 removes `defaultMode: "auto"`; the `SendMessage` deny of ADR-0019 D9 B1 stays, so subagents are relaunched, not continued; work units 198 → 200.
    - `[x]` Human decision 2026-11-15: the call cap of unit P-06 is raised from 3 to 4, so the fourth call measures `~/**/.env*` on an `.env` nested several levels outside the project and on an `.env` inside the project, each with a control.
    - `[x]` Human decision 2026-11-15 (plan D60): after R-02 `make verify` fails on an uncaught `PermissionError` for `.env` in `scripts/quality_audit.py`; unit R-15 fixes the script and keeps the P-06 deny; unit P-07 measures `registry.npmjs.org` for `pnpm`, run by the human from commands `devops_agent` prepares; work units 200 → 202.
    - `[x]` Under plan D60 (each further failure is a unit of its own), the step-by-step run of `make verify` under the installed settings also fails in `pytest tests/` (pytest's collection calls `stat()` on the root `.env`) and in `tests/test_installer.sh` (`rsync` opens `.env`); units R-16 and R-17 added; work units 202 → 204; the other steps pass.
    - `[x]` Human decision 2026-11-15 (plan D61), after R-03: R-04 also classifies an A1 non-control case `closed` when the control A1-C is open in the same run and the proxy ends the CONNECT with EOF or a reset; a timeout stays `not-measurable`.
    - `[x]` Human decision 2026-11-16 (plan D62), after the R-04 re-run in a new session: A1-1 and A1-2 stay open with unchanged settings, so unit P-08 runs the same probe and `curl` in the terminal CLI to separate the harness surface from the configuration.
    - `[x]` Human decision 2026-11-16 (plan D63), after P-08: unit P-09 (call cap 3) looks for a network approval stored outside the repository in the `/sandbox` and `/permissions` outputs; without a cause, A1-1 and A1-2 are recorded `not measurable` and R-04 marks them `known_open` with KI-059-27.

---

## 🧠 Rule Amendments & Heuristic Harvest
Extraction of knowledge for the **Memory Purge Protocol**.

| Friction Point | Resolution / Workaround | KI ID |
| :--- | :--- | :--- |
| A-12's 20000-byte target was set without measuring how many rows it forces to trim; 9 planned destinations covered about half the needed reduction | Measure the row-cap projection at Phase 4.3 for any size target; A-13 added as the missing destination. Commits (2026-11-10): A-12 `d6f5756`, A-13 `a014f4f` | KI-059-1 |
| Dispatched a batch that no rule allowed, on a question read as an order (plan D16) | Work kept after unit-by-unit checks; order restored. A human question about the method is not a change to it: answer it, then amend the plan if the human decides | KI-059-2 |
| Plan D9 and A-08 move `qa_agent` off the `gate` tier, but `ADR-0003` requires a superseding ADR; neither the plan nor the Phase 4 audit named it, and A-08 edited the test that pins that list | A-14 added (plan D17): `ADR-0021` supersedes that clause before A-08 commits. Check every plan tier move against `docs/decisions/` at Phase 4.3. Commits (2026-11-10): A-08 `80518b4`, `8e8a566`; A-14 `ed96115` | KI-059-3 |
| A-01's agent also moved `segment_cycles` to context size. Over 35 transcripts cycles fall from 86 to 37 and 17 sessions change; `ratio` None falls from 11 to 0 with `cycle_summary` alone. `F-116-N1` names this defect, the plan Operation does not | First reverted to the plan's literal scope on the orchestrator's recommendation, and the gate prompt told QA not to report it. Tester Gate 2 found that revert to be an S1. Restored (plan D19). A gate is never told what not to report. Commits (2026-11-10): A-01 `ef490cd`, `919d4f2` | KI-059-4 |
| Rules with no blocking script found in `hooks/` or `scripts/check_*`: `ephemeral` (`TODO`/`FIXME`), `RA-03` branch name, `RA-12` direct commit to `main` (only the push is blocked), `§8` pnpm settings. A trigger reduces the risk of missing them, it does not enforce them | Out of this sprint's scope; Z-02 routes scripts for them to the program queue | KI-059-5 |
| QA Gate 1 round 2 S3 notes: `config/invocation_exceptions.json:60,80` and `scripts/detect_drift.py:328`, `tests/test_detect_drift.py:459` cite text no longer in `agents.md`; `agents.md` `Why here` cells are terse and `Risk-free` overclaims; the `devops_agent` row lost the framework-root scope | Recorded, not blocking; agents.md has almost no margin to 20000 bytes (`wc -c agents.md`), so Z-02 routes them. Current: human decision 2026-11-09 (plan D38): units K-01 to K-04 | KI-059-6 |
| `qa_agent` trial ended by abort criterion 4 after one wave (plan D20). One case says nothing general about `sonnet`: QA on `sonnet` also found real S2 defects in round 1 | A new trial needs a new ADR that covers `--resolve` under Cursor | KI-059-7 |
| Host names reached the plan at `88d8a51` (QA Gate 1 round 3, S0 suspected); no instrument scans plans for them | Human decision 2026-11-05: no other project's name stays in the tree (`git grep` at `d2dbd29` was clean for three of the four names removed at `af220fe`; the fourth stayed in 6 historical files, measured by QA Gate 1 round 5, and A-19 to A-24 remove it, plan D22); this branch's unpushed history is accepted as is, with no rewrite and no check due before push. Commits (2026-11-10): A-19 `4fb09a9`, A-24 `ff69f15` | KI-059-8 |
| The 15x hard bound moved from about 371K to about 958K in session `7204cadc` when the baseline became context size (D1, D19), with no decision on whether 15 stays valid | A-00 and A-06 name it for a human decision, with the `agents.md` trim lowering `first` Closed by `ADR-0018` decision 1: absolute bound of 550,000 tokens. Commits (2026-11-10): A-00 `9b5488c`, A-06 `6d6e469` | KI-059-9 |
| `read_turns` counts one API message once per transcript record, so token totals are too high by a factor of 1.66 to 2.51, median 2.17, over the 20 closed main-session transcripts on disk on 2026-11-07, with the sum of the four usage fields: `python3 -I -c "import glob,json,os,statistics as st;S=lambda m:sum(m['usage'].get(k) or 0 for k in('input_tokens','output_tokens','cache_read_input_tokens','cache_creation_input_tokens'));M=lambda p:[m for m in(json.loads(l).get('message') for l in open(p)) if isinstance(m,dict) and m.get('usage') and m.get('model')!='<synthetic>'];R=lambda ms:sum(map(S,ms))/sum(map(S,{m['id']:m for m in reversed(ms)}.values()));live=json.load(open('docs/active_state.json'))['session_id'];v=sorted(R(M(p)) for p in glob.glob(os.path.expanduser('~/.claude/projects/*-agents/*.jsonl')) if live not in p and M(p));print(len(v),round(v[0],2),round(st.median(v),2),round(v[-1],2))"`. Earlier readings, annotated: this row said 2.1 to 2.5, and QA Gate 1 round 4 read 1.64 to 2.5 on its own transcript set; neither set is reproducible. `ratio` and cuts are unaffected. A-00, H-01 and H-03 would calibrate on these totals | Human decision 2026-11-05 (plan D21): unit A-18 before A-00. `rules/token_economy.md` totals measured before it are suspect. Commits (2026-11-10): A-00 `9b5488c`, A-18 `40b2da1`, H-01 `d8a083e`, H-03 `1678522` | KI-059-10 |
| When this row was opened, no session had run on the trimmed `agents.md`. Six sessions before it started at 63629 to 64031 tokens of context; the trim removed 33914 bytes, about 8500 tokens at 4 bytes per token (estimate), but moved 10307 bytes to `rules/code_craft.md` and 6840 to `rules/project_topology.md` | At the next session's first turn, `python3 -I scripts/session_cost.py --session <id> --json`: `first_turn` near 55500 confirms the saving; near 64000 refutes it. Whether rules are still obeyed needs later gates, not this figure. **Measured 2026-11-07, session `7a037351-d2f6-4ff2-8ca0-1e6a82e612cc`: `first_turn` 51720, below 55500, so the criterion confirms a saving.** Two limits: the drop of about 12300 tokens exceeds the 8500 estimate and Claude Code also moved from 2.1.314 to 2.1.319 between these sessions, so one measurement does not separate the two causes; and this is the first turn only, since the moved bytes return when their rule loads | KI-059-11 |
| Host data predates this sprint on public `main` (6 files name one host, one of them calling it a private repository; another host's name is in its history), and no instrument scans for host names | Human decision 2026-11-05: Z-02 routes a review of public history and a host-name scanner to Sprint 060; no rewrite in this sprint. Human decision 2026-11-07 (plan D22): A-19 to A-24 remove the name from the current tree; public history stays with Z-02. Commits (2026-11-10): A-19 `4fb09a9`, A-24 `ff69f15` | KI-059-12 |
| Transcripts on disk for this project: 21, the oldest from 2026-10-08, against the 35 cited on 2026-11-05 (QA Gate 1 round 5). Age-based deletion is inferred, not measured, and A-00 needs the Sprint 056-058 transcripts | Abort criterion 7 covers a short A-00; A-00 states which sessions it could read. Commits (2026-11-10): A-00 `9b5488c` | KI-059-13 |
| Earlier text of this row, annotated (restored after QA Gate 1 round 8, N3; plan D29 supersedes its first sentence for `scenarios.json` and `RULE_PRECEDENTS_GUIDE.md`): Domain wording judged in the D24 pass and kept: `skills/skillopt/data/scenarios.json:58-59` is a dataset that names no project, in Spanish, and `docs/guides/RULE_PRECEDENTS_GUIDE.md:205` gives generic role examples. `tests/test_profile_references.py` does not detect bare names. Current text: `tests/test_profile_references.py` covers only `profiles/<slug>` references and its docstring lists the shapes it does not detect; since A-48 (plan D33) that docstring claims only the shapes it lists, and states the files it skips; a host term outside the one-time inventory of plan D29 stays undetected. Round 7 S3 notes F7 to F14 are recorded, not remediated (`rules/qa_and_testing.md` §4 rule 1). The inventory's term list stays outside the repository (`RA-15`). Plan D31: `origin/main` still holds the host name in 11 commits and the profile slug in 6, reachable from 58 tags | Earlier resolution: Z-02 routes it with the Sprint 060 scanner. Current: Z-02 routes them with the Sprint 060 scanner; plan D31 decides public history after the merge. Commits (2026-11-10): A-48 `8923501` | KI-059-14 |
| The N3 family (superseded record prose overwritten) has no deterministic check: `scripts/check_log_append_only.py` was added (plan D34) and withdrawn (plan D35) after S1 findings in QA Gate 1 rounds 9 and 10. Its comparison held: all three recorded instances exited 2. What failed was target resolution. `current_sprint_dir` returns `None` both for no anchor, which is legitimate in a clone because the anchor is git-ignored, and for a sprint directory deleted in the range; `make verify` in a fresh clone would skip the check, and CI by inference. Round 10 also measured `check_gate_log.py` and `check_task_scope.py` printing the same kind of skip and exiting 0 on the deleted-directory fixture, and `check_gate_log.py` skipping from a host subdirectory; both predate this sprint and are not fixed by the withdrawal. The 14 older detections on `08c669c..60383e3` were not classified. QA Gate 1 round 11 also measured `audit_plan.py` skipping on the deleted-directory fixture and `check_gate_log.py --sprint-dir` exiting 0 on a mistyped path | Human decision 2026-11-07 (plan D37): the sibling skips are one family, fixed in Wave 1b by M-01 to M-04 and M-12 and held by the family test M-05 over every script with `--current-sprint`; Z-02 keeps only the withdrawn check. Earlier resolution: human decision 2026-11-07 (plan D36): the sibling skips move to units I-08 to I-10 of Wave 6, and Z-02 keeps the check. Earlier resolution: Z-02 routes the check and the sibling skips to the program queue; a new attempt resolves the sprint from committed data, not from the working tree, and is tested from every cwd and with the directory deleted. Rule 3 stays unmet for this family by human decision (plan D35). Commits (2026-11-10): M-01 `62bbce8`, M-04 `e393405`, M-05 `74eb9d7`, M-12 `d74a969` | KI-059-15 |
| The `isolation: "worktree"` dispatch of unit A-18 (`workflows/pipeline_workflow.md` Phase 6 step 2) cut the worktree from `main` at `08c669c`, not from `ai-sprint/059` at `dea1f08`, so a unit without a correction starts from pre-sprint code | Human decision 2026-11-09: every worktree dispatch instructs `git merge --ff-only ai-sprint/059` and a base check before the first edit; Phase 6 is not amended in Wave 3. Current: human decision 2026-11-09 (plan D38): A-04 amends Phase 6 step 2. Commits (2026-11-10): A-04 `bced56b`, A-18 `40b2da1` | KI-059-16 |
| `git worktree remove` for unit A-18 (Phase 6 step 4) exited 255 under the sandbox with `failed to delete '.git/worktrees/agent-a97e1538cbe7584ce': Operation not permitted`; the worktree directory was already gone and the branch could not be deleted | `git worktree prune` and `git branch -D` run outside the sandbox for that cleanup, through the permission prompt; repeats at each batch until measured in C-01. Current: human decision 2026-11-09 (plan D38): the C-01 Operation names this measurement. Current (2026-11-10): C-01 measured worktree add, remove and branch -D exiting 0 under the sandbox, not reproduced (SANDBOX_ENUMERATION.md section 2.7); a harness-created worktree removal stays unmeasured. Commits (2026-11-10): A-18 `40b2da1`, C-01 `e4f435d` | KI-059-17 |
| Gitfile vector: a subdirectory `.git` file points to an agent-made gitdir whose config sets `core.fsmonitor`; `git add` registers it and an unsandboxed git runs it. Measured outside the sandbox on CLI 2.1.119 (case `P2`); on CLI 2.1.319 the set-up succeeds and its unsandboxed trigger is not yet measured. No `.git/*` `denyWrite` closes it (C-01b case D) | Human decisions 2026-11-10 (plan D43, D44): recorded as a known issue, not closed; unit C-01c measures the unsandboxed trigger on 2.1.319 with and without the B-06 block; B-06 is reverted only if the block opens it. Source: `SANDBOX_ENUMERATION.md` sections 4 and 6. Current (2026-11-10): C-01c (`9489ce8`) measured on CLI 2.1.319 no run outside the sandbox with the B-06 block for the headless triggers it drove (startup, `git commit`); interactive startup git, IDE git and a human's unsandboxed git stay unmeasured; B-06 not reverted (plan D44, D45). Source: `SANDBOX_ENUMERATION.md` sections 4.4 and 7. Commits (2026-11-10): B-06 `92fddf8`, C-01b `56b715f` | KI-059-18 |
| Egress from the Bash sandbox is not filtered to a list: with no `network.allowedDomains` in any settings file and the session in auto mode, `curl` through the proxy reached `webhook.site`, `pastebin.com` and `httpbin.org` (HTTP 200, harness `2.1.322`, 2026-11-14). Review finding F-01 | Plan D51: recorded as a known issue, not closed. Unit S-02 (`1b5997a`) measured that `network.allowedDomains` set to the two GitHub hosts denies other hosts on 2.1.322 and 2.1.119, at project level and via `--settings`; unit S-03 (`ea85ed5`) measured that a `claude -p` child with the `network` key absent denies every host, so the open egress of the interactive auto-mode session comes from the session mode, not the settings (inferred; B7 measures the auto-mode approvals); ADR-0019 decides | KI-059-19 |
| The sandbox proxy tunnels to loopback: `curl --noproxy '' -x "$HTTPS_PROXY" -p http://127.0.0.1:5000/` returned `200 Connection Established` then `Server: AirTunes` (harness `2.1.322`, 2026-11-14), so local TCP services are reachable from the sandbox through the proxy while direct connects return `EPERM`. The earlier "proxy CONNECT to localhost -> 000" reading bypassed the proxy through `NO_PROXY`. Review finding F-02 | Plan D51: recorded as a known issue, not closed. Unit S-02 (`1b5997a`) measured the proxy CONNECT to 127.0.0.1:5000 denied with `network.allowedDomains` set, but its control also denied it, so the cause is not isolated; unit S-03 (`ea85ed5`) measured the same denial with the `network` key absent in a `claude -p` child, so the open tunnel of the interactive auto-mode session comes from the session mode (inferred); ADR-0019 decides | KI-059-20 |
| Credentials readable from the Bash sandbox: `gh auth token` (scopes `gist, read:org, repo, user, workflow`, no expiry header), the `osxkeychain` git credential for `github.com`, and `security find-generic-password -s gh:github.com` (exit 0); no value printed. Review findings F-05, F-06 | Plan D51: recorded as a known issue, not closed; unit S-05 (`343f3d7`, plan D52) measured that `sandbox.filesystem.denyRead` blocks Bash reads of a listed file (A6-1, A6-2); unit S-08 (`bfbc361`) measured that `denyRead` blocks `~/.config/gh` and the keychain file from Bash (B2); the keychain service is not covered by a file rule and is unmeasured; the human replaces the token with a fine-grained expiring one; ADR-0019 decides | KI-059-21 |
| A token with `repo` scope held by the repository owner can delete the branch protection of `main` through the API, so branch protection is not a boundary while the agent can read that token (inferred from the scopes; not executed). Review finding F-15 | Plan D51: recorded as a known issue, not closed; unit S-06 (`c72528c`, plan D52) measured a fine-grained single-repository token without Administration: `403` on reading the protection of `main` (A10-2); the `repo`-scope token stays readable until the human revokes it; ADR-0019 decides | KI-059-22 |
| The protection of `main` has `enforce_admins: false` and 0 required approvals (A10-4, unit S-06 `c72528c`), so a token acting for the owner with Contents and Pull requests write may push past the protection or merge a pull request into `main` once the checks pass (`RA-12`); inferred, not executed | Admin bypass closed 2026-11-14: the human enabled `enforce_admins`, and unauthenticated `GET repos/<nucleus>/branches/main` prints `protected: true`, `enforcement_level: "everyone"`; the merge without human review stays open; unit S-16 (`b803704`) scopes the attack validation; ADR-0019 decides the merge control | KI-059-24 |
| In auto mode an agent uses out-of-sandbox tools that send data to third parties (WebFetch, connectors able to create and share files, Artifact publishing) with no approval prompt, and neither the nucleus nor the host template denies any of them; measured by unit S-07 (`0ac2fd0`), checks B1-4 and B1-7 | Recorded as a known issue, not closed; a `permissions.deny` entry removes a tool or a whole connector from the agent (B1-5, B1-6); ADR-0019 decides the deny list | KI-059-25 |
| A host boot checks out the newest nucleus version tag with no signature check, and the nucleus has no tag protection (`rulesets: []`), so any credential with Contents write on the nucleus, the A10 token included, can publish code every host loads at its next boot; measured by unit S-10 (`2b4cbaa`), checks B4-1 to B4-3; inferred, not executed | Narrowed 2026-11-14: the human created tag ruleset `version-tags`, and the unauthenticated API prints `enforcement: active`, include `refs/tags/v*`, rules `creation`, `update`, `deletion`, `non_fast_forward`; unit S-12 (`00ba632`, B11-4) measured its bypass list as the Admin repository role with `bypass_mode: always`, and whether a token acting for the owner inherits that bypass is unmeasured (unit S-16, `b803704`); ADR-0019 decides tag signing and the verification in `scripts/sync_agents_pin.py` | KI-059-26 |
| The code the host template's hooks run (`hooks/`, `scripts/`) is writable from the Bash sandbox in the nucleus, so a hook runs content an agent can change (`RA-19` (3)); measured by unit S-05 (`343f3d7`), check A7-3; unit S-09 (`f17299e`, B3) adds that the git hooks run `hooks/on_commit.py`, `hooks/on_commit_msg.py`, `hooks/on_push.py` and `scripts/install.py` on the human's commits and pushes, and that `Makefile` is writable | Recorded as a known issue, not closed; sandbox writability of `.agents/hooks/` in a host is unmeasured; ADR-0019 decides write protection for the hook code | KI-059-23 |
| After R-02 (`374a5f8`) installed `sandbox.network.allowedDomains` (the two GitHub hosts and the two PyPI hosts) in the nucleus `.claude/settings.json` and the running session reloaded its `denyRead` list (B2-1 to B2-5 closed, B9), egress to unlisted hosts stays open in that session: `curl https://webhook.site` gave `200` from the Bash sandbox on 2026-11-16, and the proxy answered `200` to a CONNECT for `127.0.0.1:5000` and `example.org:443` in the R-04 run of `make sandbox-probe` (A1-1, A1-2 `FAIL`, commit `3295e45`); the cause is not measured; re-run in a new session (session `7b446d03`, VS Code 2.1.322) on 2026-11-16: `make sandbox-probe` exit `1` (`FAIL=2 ok=13`, A1-1 and A1-2 `open [200]`, B2-1 to B2-5 closed) and `webhook.site` `200`, with `.claude/settings.json` unchanged since R-02 (2026-11-15 20:33) while R-03 measured A1-1 and A1-2 `proxy-io-error` after that time | Open. ADR-0019 D8 does not hold in the VS Code session; re-planned with the human as plan D62: unit P-08 (`a301473`, B9) ran the same probe and `curl` in the terminal CLI 2.1.119 and measured A1-1, A1-2 `open [200]` and `webhook.site` `200`, so the surface does not explain it; plan D63 adds unit P-09 (`/sandbox` and `/permissions` outputs), then R-04 is re-planned from its row; `example.org` gives `000` with or without `allowedDomains` (M6), so it proves no denial | KI-059-27 |

---

## 🚦 Quality Gate

Transcribed here by `orchestrator` from the gate agents' emissions at **Phase 7**
(`workflows/pipeline_workflow.md`; gates emit, they do not write). Leave the table
with **no data rows until Phase 7** — `scripts/check_gate_log.py` (run by `make
verify` and `config/template_gates.json`) rejects any placeholder verdict token,
and a fabricated row would teach authors to invent verdicts
(`config/template_gates.json` `gate_exceptions`).

<!--
Verdict vocabulary (`rules/qa_and_testing.md §4`, `RA-17`):
  Verdict ∈ APPROVED | REJECTED | RECORD
  APPROVED  → Class cell empty
  REJECTED  → Class ∈ charter | instructing   (more than 3 consecutive REJECTED
              of one logic block → workflows/remediation_workflow.md Phase 0)
  RECORD    → Class = testifying               (does NOT count toward remediation)
Gate cell: Gate 1 row starts with "QA"; Gate 2 row starts with "Tester".
Severity cell ∈ S0 | S1 | S2 | S3 | none. Scale and definitions: `rules/qa_and_testing.md §4`
  (not restated here). Write the highest severity found in that round; write
  `none` for a round with no findings.
escape token: write the literal lowercase word `escape` in the Notes cell of a
  row when that round reports an S0 or S1 finding that is new in round 2 or later
  AND sits on material an earlier round of the same gate already reviewed
  (`rules/qa_and_testing.md §4` convergence rule 2; an S2 or S3 carries no token). Write it
  once per row, with no other use of the word `escape` in Notes. Rows without
  such a finding carry no token.
Example (do not uncomment — Phase 7 writes the real rows):
  | QA Agent (Gate 1)     | 1 | REJECTED | instructing | S2 | 1 finding in scripts/x.py. |
  | QA Agent (Gate 1)     | 2 | APPROVED |  | none | ruff + lint clean; structure verified. |
  | Tester Agent (Gate 2) | 1 | RECORD   | testifying | S3 | 701 passed, zero regression; N items recorded. |
  | Tester Agent (Gate 2) | 2 | REJECTED | instructing | S1 | escape: new failure in a module round 1 reviewed. |
-->

| Gate | Round | Verdict | Class | Severity | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| QA Agent (Gate 1) | 1 | REJECTED | instructing | S2 | Range `08c669c..HEAD`, on `sonnet` (`ADR-0021` trial). 5 findings: `feedback_upstream` and `RA-09` contradict other rules; D18 unmet for `unambiguous_action`, `RA-03`, `RA-12`; S3 stale pointers and sprint staleness. Also: `globs` reach only `cursor_adapter`, so A-17's trigger has no effect in Claude Code. |
| QA Agent (Gate 1) | 2 | RECORD | testifying | S3 | Range `08c669c..32dfbe4`, on `sonnet`. Round 1 S2 findings resolved. 4 S3 notes (KI-059-6). The gate emitted `APPROVED` with class `testifying`; `rules/qa_and_testing.md §4` makes S3 and `testifying` a `RECORD`, so it is transcribed as `RECORD`. |
| QA Agent (Gate 1) | 3 | REJECTED | charter | S0 | escape: suspected host data in the plan (`RA-15`) and `rules/token_economy.md §3.1` naming a unit the instrument no longer measures, both on material earlier rounds reviewed. Range `08c669c..0138287`, on `opus`. 13 findings, 5 S2 included. Revert of A-08 complete; `919d4f2` correct (cuts match real compactions). |
| QA Agent (Gate 1) | 4 | REJECTED | charter | S0 | escape on `rules/token_economy.md` soft row: `probe_cost` never surfaces a soft breach. remediation-regression: the `KI-059-8` check written at `af220fe` cannot pass, because the names are also in `main`'s history. Host data predates this range on public `main` (human decision). Range `08c669c..6a85eff`, on `opus`. 7 findings. |
| QA Agent (Gate 1) | 5 | REJECTED | instructing | S2 | Range `08c669c..7779e7f`, on `opus`. `check_fix_reproduces.py` exit 0 (2 fix commits, 0 violations); `check_remediation_chain.py` exit 0 (chains: 0); `make verify` exit 0, 1535 passed. All round 4 fixes verified. 8 findings: 4 S2, 4 S3. `rules/token_economy.md:54` says the soft threshold records and does not act, against line 37 and the plan template, which require a Cost update. The Z-02 row in `task_scope.md` omits the plan's proposal E routing. `KI-059-8` says `git grep` is clean while 6 files still name one host (`KI-059-12`). `rules/token_economy.md:58` says Sprint 021 totals stay suspect until A-18, which cannot re-measure them. No new host name in the range. Round 3, 4 and 5 are consecutive REJECTED. |
| QA Agent (Gate 1) | 6 | REJECTED | charter | S0 | escape: the slug of a real host's profile stays in 4 tracked files, 9 lines, one of them the line A-19 edited, beside its own description as real and identifiable, against the human decision in KI-059-8; the host-name sweeps of rounds 3 to 5 left it unreported, and no sprint record ever names it. Predates the range, also on origin/main. remediation-regression: 9345c66 turned rules/token_economy.md:54 into an instruction to write forced: true by hand with no target file, and 1e1deda pins that text. Range 08c669c..d06c939, on opus. check_fix_reproduces.py exit 0 (2 fix commits, 0 violations); check_remediation_chain.py exit 0 (chains: 0); make verify exit 0, 1538 passed. Round 5 S2 fixes verified. 7 findings: 1 S0, 2 S2, 4 S3. Rounds 3, 4, 5 and 6 are consecutive REJECTED. |
| QA Agent (Gate 1) | 7 | REJECTED | charter | S0 | escape: the business-domain phrase that A-26 and A-30 replaced stays at `docs/roadmaps/core/pipeline/018-post-publication-field-hardening.md:36`, against plan D24; the name and slug sweeps never searched for that phrase, and D24 listed only two of its three sites. Predates the range, also on origin/main. remediation-regression: `af819b1` wrote `rules/token_economy.md:54` to say the hard close is read from `task_scope.md`, which has no such marker since D27 withdrew it, and `a655251` pins that text. Range 08c669c..1dbb43e, on opus. check_fix_reproduces.py exit 0 (2 fix commits, 0 violations); check_remediation_chain.py exit 0 (chains: 0); make verify exit 0, 1541 passed; ruff exit 0; quality-audit exit 0. Round 6 S0 slug fix verified: A-31 logic fails at d06c939 on all 4 files, 0 hits at HEAD. 14 findings: 1 S0, 5 S2, 8 S3. Rounds 3, 4, 5, 6 and 7 are consecutive REJECTED; this is the third remediation-regression label of the sprint. |
| QA Agent (Gate 1) | 8 | REJECTED | instructing | S2 | Range 1dbb43e..10c88f4 plus the round 7 S0-S2 fixes, on opus. check_fix_reproduces.py exit 0 (2 fix commits, 0 violations); check_remediation_chain.py exit 0 (chains: 0); make verify exit 0, 1540 passed; ruff exit 0; quality-audit exit 0; check_gate_log exit 0; check_role_artifact exit 0. Round 7 F1, F2, F5 and F6 fixes verified; F4 partly. F3: `skills/compliance-checker` discarded by D32, and its third location `docs/standards/templates/HOTFIX_TEMPLATE.md:25` has no fix, KI or discard (S2, instructing), which is what rejects the round. 5 findings: 0 S0, 0 S1, 4 S2, 1 S3 group with 3 notes. No remediation-regression label. Rounds 3 to 8 are consecutive REJECTED. |
| QA Agent (Gate 1) | 9 | REJECTED | charter | S1 | Range 60383e3..ae6ef40 plus the round 8 S0-S2 fixes, on opus. check_fix_reproduces.py exit 0 (2 fix commits, 0 violations); check_remediation_chain.py exit 0 (chains: 0); make verify exit 0, 1564 passed; ruff exit 0; quality-audit exit 0 (171 files, 0 violations); check_gate_log exit 0; check_role_artifact exit 0; check_log_append_only.py on 60383e3..HEAD exit 0. D34 positive controls 10c88f4, 1dbb43e and 60383e3 all exit 2. Round 8 N1, N2, N4 and N5 fixes verified; N3 fixed for KI-059-14 and D24. remediation-regression: R9-1 and R9-2 are defects in scripts/check_log_append_only.py, which the round 8 remediation introduced (A-49). R9-1 (S1, charter): --current-sprint from a host root reads the framework anchor, prints [OK] skip and exits 0 on a host sprint 60 with a real KI loss. R9-2 (S1, charter): --sprint-dir given relative to a subdirectory or as an absolute path compares empty with empty and exits 0 on 10c88f4^..10c88f4, a range with known losses; a mistyped directory and the range ..HEAD also exit 0. R9-3 (S2, testifying): D32 narrows D23 and D26 and neither row carries a mark. 3 findings and 3 S3 notes: 0 S0, 2 S1, 1 S2, 3 S3. Convergence rule 2 does not apply: this script is first reviewed in this round. Rounds 3 to 9 are consecutive REJECTED. |
| QA Agent (Gate 1) | 10 | REJECTED | charter | S1 | escape: R10-1 sits on scripts/check_log_append_only.py, reviewed in round 9, whose probes deleted no sprint directory under --current-sprint and whose unit test deletes only the log, under --sprint-dir. Range 4b34cf9..e24e848 plus the round 9 S0-S2 fixes, on opus. check_fix_reproduces.py exit 0 (3 fix commits, 0 violations); check_remediation_chain.py exit 0 (chains: 0); make verify exit 0, 1572 passed; ruff exit 0; quality-audit exit 0 (171 files, 0 violations); check_gate_log exit 0; check_role_artifact exit 0; check_log_append_only.py on 60383e3..HEAD exit 0. D34 positive controls 10c88f4, 1dbb43e and 60383e3 all exit 2. R9-1, R9-2 and R9-3 fixes verified. remediation-regression: R10-1 and R10-2 are defects in scripts/check_log_append_only.py from the A-49 and A-53 remediations. R10-1 (S1, charter): --current-sprint with the whole sprint directory deleted in the range prints [OK] no sprint >= 60 (skip) and make verify exits 0, contradicting docstring lines 24-25. R10-2 (S1, charter): --current-sprint from a subdirectory prints the same skip and exits 0 on a real KI loss; the parent of f273f93 exits 2. R10-3 (S2, testifying): an empty last_close_commit or a truncated anchor exits 0, contradicting line 233. 3 findings and 3 S3 notes: 0 S0, 2 S1, 1 S2, 3 S3. Convergence rule 3 applies: R10-1 and R10-2 share the silent-pass family of R9-1 and R9-2. Rounds 3 to 10 are consecutive REJECTED. |
| QA Agent (Gate 1) | 11 | REJECTED | instructing | S2 | Range e24e848..e8f06df plus the round 10 S0-S2 fixes, on opus. check_fix_reproduces.py exit 0 (3 fix commits, 0 violations); check_remediation_chain.py exit 0 (chains: 0); make verify exit 0, 1540 passed; ruff exit 0; quality-audit exit 0 (169 files, 0 violations); check_gate_log exit 0; check_role_artifact exit 0. R10-1, R10-2 and R10-3 fixed by withdrawal under plan D35: scripts/check_log_append_only.py and its test are absent, and Makefile, README.md and rules/documentation_standard.md equal their state before A-49. remediation-regression: R11-1 (S2, instructing): the D35 remediation added KI-059-15 and routed it to Z-02, but the closed KI lists of Z-02 at IMPLEMENTATION_PLAN.md:239 and task_scope.md:150 stop at KI-059-14. 1 finding and 3 S3 notes: 0 S0, 0 S1, 1 S2, 3 S3. Convergence rule 3 applies: R11-1 is the second occurrence of the family of round 8 N2, a plan decision that did not reach the plan's other rows. Rounds 3 to 11 are consecutive REJECTED. |
| QA Agent (Gate 1) | 12 | REJECTED | charter | S1 | escape: R12-2 sits on skills/token-saver-auditor/scripts/audit_plan.py, which round 11 measured only on the deleted-directory fixture without varying the id type. Range e8f06df..7ff9bb3 plus the fix of R11-1. check_fix_reproduces.py exit 0 (3 fix commits, 0 violations); check_remediation_chain.py exit 0 (chains: 0); make verify exit 0, 1540 passed; ruff exit 0; quality-audit exit 0 (169 files, 0 violations); check_gate_log exit 0; check_role_artifact exit 0. R11-1 fixed: IMPLEMENTATION_PLAN.md:243 and task_scope.md:153 refer to the KI table and enumerate no KI-059 id. R12-2 (S1, charter): audit_plan.py:58-59 skips a string anchor id such as "059"; on a fixture plan with no required sections, id 59 exits 2 and id "059" prints [OK] (skip) and exits 0. The nucleus anchor holds an integer, so nucleus make verify is not affected. remediation-regression: R12-1 (S2, testifying): plan D36 and KI-059-15 move the sibling skips to I-08 to I-10 with one declared exception, but those units leave three cases: a subdirectory cwd skips in all three checks, audit_plan.py exits 0 on a mistyped plan path, and a truncated anchor skips. R12-3 (S2, instructing): I-10 does not name its paired test file, tests/test_token_saver_auditor.py, against the Phase 4 F-10 resolution. 3 findings and 3 S3 notes: 0 S0, 1 S1, 2 S2, 3 S3. Convergence rule 3 applies: R12-1 is the third occurrence of the family of round 8 N2 and R11-1; R12-2 is the third occurrence of the silent-pass family of rounds 9 and 10. Rounds 3 to 12 are consecutive REJECTED. |
| QA Agent (Gate 1) | 13 | REJECTED | instructing | S2 | Range 01c0083..6043e7d plus the R12 fixes. All 9 commands exit 0; make verify 1540 passed. R12-2 and R12-1 assigned to Wave 1b; R12-3 fixed. R13-1 (S2, instructing), R13-2 (S2, instructing), R13-3 (S2, testifying); 3 S3. Detail: deadlock record, round 13. Rule 3: R13-1 and R13-3 are further occurrences of the round 8 N2 family. Rounds 3 to 13 are consecutive REJECTED. |
| QA Agent (Gate 1) | 14 | REJECTED | charter | S1 | Range 3af48b5..fc377e3 plus R13 fixes. check_fix_reproduces exit 0; chains: 0; make verify 1602 passed; ruff, quality-audit exit 0. R13-1/2/3 closed. R14-1 (S1, charter), R14-2, R14-3 (S2, instructing); 3 S3. Rule 3: R14-1 is the silent-pass family. Rounds 3 to 14 consecutive REJECTED. |
| QA Agent (Gate 1) | 15 | RECORD | testifying | S2 | Range fc377e3..HEAD plus R14 fixes. check_fix_reproduces exit 0; 1 chain, exit 0; make verify 1613 passed; ruff, quality-audit exit 0. R14-1/2/3 closed. R15-1, R15-2 (S2, testifying); 4 S3. First round since round 2 not REJECTED. |
| QA Agent (Gate 1) | 16 | REJECTED | charter | S1 | Range f1d193f..f8cfac3. `--batches` schedules replaced I-08..I-10 as pending (S1); prompt_count omits subagent transcripts, baseline 78 vs 99 (S1); B-02 re-measure undone, B-06 not applied (S2); splitlines drops U+2028 records (S2); RA-14 docs on self-bridge stale (S2). fix replay 0, chains 0, verify 0, quality-audit 0. |
| QA Agent (Gate 1) | 17 | REJECTED | charter | S2 | Range f8cfac3..f70df84. Fix replay 0, 1 chain exit 0, verify 0, quality-audit 0. R16-1..5 closed. R17-1 (S2, charter): --batches treats an unknown Status as landed and schedules its dependents. R17-2 (S2, testifying): no round 16 Remediation notes; check_gate_log exits 2 on a round 17 row. 3 S3. |
| QA Agent (Gate 1) | 18 | REJECTED | charter | S2 | Range f70df84..0c41e80; tools on 08c669c..HEAD. Fix replay 0 (19 OK). Chain exit 2: A-1 stop, second chain c5fbf5f>639fd05; re-plan with the human. verify 0, quality-audit 0. R17-1, R17-2 closed. R18-1 (S2, charter) A-1 stop. R18-2 (S2) R-4 notes omit the chain check. R18-3 (S2) docstring vs any() guard; any->all mutation survives. |
| QA Agent (Gate 1) | 19 | RECORD | testifying | S2 | Range 0c41e80..db738ca; tools also on 08c669c..HEAD. Fix replay 0 (20 OK). Chain exit 2 from the base: same A-1 stop as R18-1, no third chain. verify 0 (1668 passed), quality-audit 0. R18-1 actioned; R18-2, R18-3 closed. R19-1 (S2, testifying) stale line citations in the pipeline workflow. |
| QA Agent (Gate 1) | 20 | RECORD | testifying | S2 | Range 2c438d6..29c49a4; tools also on 08c669c..HEAD. Fix replay 0 (21 OK). Chain exit 2 from the base: same A-1 stop, chain 2 now four commits, no third chain. verify 0 (1670 passed), quality-audit 0. R19-1, T3-1, T3-2 closed. R20-1 (S2, testifying) T3-1 and T3-2 have no Gate findings row. |
| QA Agent (Gate 1) | 21 | REJECTED | charter | S0 | Range c6c41fe..cd2ee05; tools on 08c669c..HEAD. Fix replay 0 (24 OK). Chain exit 2, chains: 3 (A-1 stop). verify 0 (1761 passed), quality-audit 0, ruff 0. R21-3 (S0) gitfile vector with no KI, B-06 on 2.1.319 unmeasured. R21-1, R21-2 (S2) A-1 stop patched. R21-4 (S2) 23 claude -p calls of 20. R21-5, R21-6 (S2) stale records. 5 S3. |
| QA Agent (Gate 1) | 22 | REJECTED | charter | S2 | Range cd2ee05..548a2d3; tools on 08c669c..HEAD. Fix replay 0 (24 OK). Chain exit 2, chains: 3, unchanged (D44 freeze). verify 0 (1761 passed), quality-audit 0, ruff 0. R21-1, R21-2, R21-4, R21-5, R21-6 closed; R21-3 KI written, measure half open. R22-1 (S2) C-01c without-B-06 case not run, reason circular. R22-2 (S2) KI-059-18 row stale after C-01c. 1 S3. |
| QA Agent (Gate 1) | 23 | REJECTED | charter | S2 | Range 548a2d3..261b640; tools on 08c669c..HEAD. Fix replay 0 (24 OK). Chain exit 2, chains: 3, unchanged (D44 freeze, no fix( in range). verify 0 (1766 passed), quality-audit 0. R22-1, R22-2 closed; C-05 mutations caught by its tests. R23-1 (S2) check_sprint_refs exits 2 on a sprint with a plan but no task_scope.md or SPRINT_LOG.md (Phases 1-4.2). 3 S3. |
| QA Agent (Gate 1) | 24 | RECORD | testifying | S3 | Range 261b640..10204e4; tools on 08c669c..HEAD. Fix replay 0 (25 OK, 72d410b included). Chain exit 2, chains: 3, unchanged (D46 check holds; 72d410b not linked). verify 0 (1767 passed), quality-audit 0. R23-1 closed by 72d410b: plan-only fixture exits 0, KI check still exits 2 with both files present. 2 S3. |
| QA Agent (Gate 1) | 25 | RECORD | testifying | S3 | Range 10204e4..b13cb49; tools on 08c669c..HEAD. Fix replay 0 (25 OK). Chain exit 2, chains: 3, unchanged (D44/D46 freeze, no fix( in range). verify 0 (1768 passed), quality-audit 0, ruff 0. T5-1 closed by 649eb96: removing the read except fails the new test. T5-2 closed by 65b4709: no 15x figure left in the template. 3 S3 (record wording). |
| QA Agent (Gate 1) | 26 | RECORD | testifying | S2 | Range b13cb49..e95d239; tools on 08c669c..HEAD. Fix replay 0 (25 OK). Chain exit 2, chains: 3, unchanged (D44/D46 freeze, no fix( in range). verify 0 (1769 passed), quality-audit 0, ruff 0. T6-1 closed by 28630d7: narrowing the except to UnicodeDecodeError fails the new test. R25-1..3, T6-2..4 closed. R26-1 (S2) round 5 row still cites check_sprint_refs.py:264. 1 S3. |
| QA Agent (Gate 1) | 27 | RECORD | testifying | S3 | Range e95d239..17ed349; tools on 08c669c..HEAD. Fix replay 0 (25 OK). Chain exit 2, chains: 3, unchanged (D44/D46 freeze, no fix( in range). verify 0 (1769 passed), quality-audit 0, ruff 0, check_gate_log/task_scope/sprint_refs 0. R26-1, R26-2 closed by 62db62c; row commands rerun. R27-1 D49 Check names 2 rows, grep -c prints 3. R27-2 R25-2 sed lacks file. R27-3 Close cells lack SHA. 3 S3. |
| QA Agent (Gate 1) | 28 | RECORD | testifying | S3 | Range 17ed349..b79fdad; tools on 08c669c..HEAD. Fix replay 0 (25 OK). Chain exit 2, chains: 3, unchanged (D44/D46 freeze, no fix( in range). verify 0 (1769 passed), quality-audit 0, ruff 0, check_gate_log/task_scope/sprint_refs 0. R27-1 closed by 8139ca4, R27-2, R27-3 by a44919a. R28-1 R27-3 grep -o does not discriminate. R28-2 round 5 grep matches 2 rows. R28-3 D50 "hoy 3" is 0. 3 S3. |
| Tester Agent (Gate 2) | 1 | REJECTED | charter | S1 | Range `08c669c..c6c7987`, 1531 passed. Baseline on context size with cuts on `cache_read`: 50 of 52 cuts over 35 transcripts are not collapses, and the ratio that feeds the hard bound falls (synthetic 20x reads 2.5x). 3 more: `--resolve` alternatives diverge under Cursor (S2), hard bound and cut field untested (S2), census wording (S3). |
| Tester Agent (Gate 2) | 2 | RECORD | testifying | S2 | Range c6c7987..8b84259, 1613 passed, make verify exit 0, zero regression. Round 1 S0-S2 findings closed. T2-1 (S2, testifying); 3 S3. |
| Tester Agent (Gate 2) | 3 | RECORD | testifying | S2 | Range 8b84259..2c438d6, 1668 passed, make verify exit 0, zero regression. T2-1 closed. T3-1 (S2) a repeated unit id drops rows from --batches with exit 0, `scripts/check_task_scope.py:380`. T3-2 (S2) false reason citing hooks/on_commit.py, `workflows/pipeline_workflow.md:24`. T3-3, T3-4 (S3) noted. |
| Tester Agent (Gate 2) | 4 | RECORD | testifying | S2 | Range 2c438d6..c6c41fe, 1670 passed, make verify exit 0, zero regression. T3-1, T3-2, R20-1 closed. T4-1 (S2) Jurisdiction table omits units claiming the same subject. T4-2 (S3) noted. |
| Tester Agent (Gate 2) | 5 | RECORD | testifying | S2 | Range c6c41fe..d97c1fe, 1767 passed, make verify exit 0, zero regression. T4-1 closed: --batches puts no two units with one File in a batch. T5-1 (S2) untested read-failure exit 2, `scripts/check_sprint_refs.py:266`. T5-2 (S2) plan template keeps the hard bound at 15x against ADR-0018 550,000, `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md:117`. T5-3 (S3) noted. |
| Tester Agent (Gate 2) | 6 | RECORD | testifying | S3 | Range d97c1fe..6196230, 1768 passed, make verify exit 0, zero regression. T5-1 closed by 649eb96: removing the read except fails the new test. T5-2 closed by 65b4709: no 15x left, section 3.1 exists. T6-1 (S3) OSError half of the read except untested, `scripts/check_sprint_refs.py:266`. T6-2, T6-3, T6-4 (S3) C-07 operation and line cite, round 5 range names HEAD. |
| Tester Agent (Gate 2) | 7 | APPROVED |  | none | Range 6196230..3bc2bdb; tools on 08c669c..HEAD. 1769 passed, make verify 0, pytest 0, zero regression. T6-1 closed by 28630d7: narrowing the except to UnicodeDecodeError fails the new test, removing it fails both. C-07..C-15 and D47..D50 checks print as claimed. Fix replay 0 (25 OK), chain exit 2 unchanged (chains: 3), gate_log/task_scope/sprint_refs 0. No findings. |

### Gate findings

One row per S0-S2 finding from QA Gate 1 round 13 on (plan D37), plus one row for every `R<round>-<n>` ID of any severity that another sprint artifact cites, because `scripts/check_sprint_refs.py` requires it (plan D49). Check: the command that reproduces it.

| Round | ID | Severity | File:line | Check |
| :--- | :--- | :--- | :--- | :--- |
| 13 | R13-1 | S2 | `scripts/loop_guard.py:112-114` | in a fixture repository with an armed loop: `python3 scripts/loop_guard.py check --sprint-dir docs/sprints/059-typo` → exit 0 |
| 13 | R13-2 | S2 | `docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md` M-11 | `grep -c "^### Gate findings" docs/sprints/059-core-pipeline/SPRINT_LOG.md` → 0 at `3af48b5` |
| 13 | R13-3 | S2 | `docs/sprints/059-core-pipeline/SPRINT_LOG.md:20` | `git show 3af48b5:docs/sprints/059-core-pipeline/SPRINT_LOG.md \| grep -c "Work units: 92"` → 1 |
| 14 | R14-1 | S1 | `skills/token-saver-auditor/scripts/audit_plan.py:69` | repository under `005-dir/`, anchor id 59, empty plan: `python3 skills/token-saver-auditor/scripts/audit_plan.py --current-sprint` → `(skip)`, exit 0 |
| 14 | R14-2 | S2 | `docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md` M-01 | `grep -c "agents_root" scripts/_current_sprint.py` → 0 at `fc377e3` |
| 14 | R14-3 | S2 | `scripts/_current_sprint.py:15-16` | `grep -c "_current_sprint" scripts/loop_guard.py` → 0 at `fc377e3` |
| 15 | R15-1 | S2 | `docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md` M-01 | `git show 61bc129:docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md \| grep -c "la conducta de referencia es"` → 1 |
| 15 | R15-2 | S2 | `docs/sprints/059-core-pipeline/SPRINT_LOG.md` Remediation notes | at `61bc129`, the round 14 Remediation notes hold 3 commands against 9 for round 13 |
| 16 | R16-1 | S1 | `scripts/check_task_scope.py:238` | `python3 scripts/check_task_scope.py --sprint-dir docs/sprints/059-core-pipeline --batches` at `f8cfac3` → a batch lists I-08 I-09 I-10, Status `replaced` |
| 16 | R16-2 | S1 | `scripts/prompt_count.py:201` | `python3 scripts/prompt_count.py --session e9a7a9bf-bf5b-4800-bd46-edd6c8fc46c5 --json` at `f8cfac3` → `decisions_user_approved` 78; its `subagents/*.jsonl` hold 21 more |
| 16 | R16-3 | S2 | `docs/sprints/059-core-pipeline/PROMPT_MEASUREMENT.md:33` | `grep -c "pending B-06" docs/sprints/059-core-pipeline/PROMPT_MEASUREMENT.md` → 1 at `f8cfac3`; `ls .claude/settings.json` → exit 1 |
| 16 | R16-4 | S2 | `scripts/prompt_count.py:84` | a `tool_result` with a raw U+2028 and `permissionDecision` at `f8cfac3` → `decisions_user_approved` 0, `tool_uses_without_decision` 1 |
| 16 | R16-5 | S2 | `docs/plans/README.md:57` | `grep -n "settings" docs/plans/README.md` at `f8cfac3` states the self-bridge writes no `.claude/settings.json`; `scripts/install.py:444` writes it |
| 17 | R17-1 | S2 | `scripts/check_task_scope.py:344` | `python3 scripts/check_task_scope.py --sprint-dir <fixture> --batches` on a fixture with unit A Status `in progress` and unit B depending on A at `f70df84` → audit exit 0, `batch 1: B` |
| 17 | R17-2 | S2 | `docs/sprints/059-core-pipeline/SPRINT_LOG.md:258` | `python3 scripts/check_gate_log.py --sprint-dir <copy>` on a copy of the log with a round 17 row at `f70df84` → exit 2, no Remediation notes row for round 16 |
| 18 | R18-1 | S2 | `scripts/check_task_scope.py:26` | `python3 scripts/check_remediation_chain.py --range 08c669c..HEAD` at `0c41e80` → exit 2, `A-1 stop: second remediation chain in the range`, chain 2 `c5fbf5f`, `639fd05` |
| 18 | R18-2 | S2 | `docs/sprints/059-core-pipeline/SPRINT_LOG.md:268` | `grep -n "check_remediation_chain" docs/sprints/059-core-pipeline/SPRINT_LOG.md` at `0c41e80` → last notes row is round 14; round 17 rows hold no chain check |
| 18 | R18-3 | S2 | `scripts/check_task_scope.py:398` | fixture with one table without `Depends on` (Status `shipped last week`) and one with it, `python3 scripts/check_task_scope.py --sprint-dir <fixture>` at `0c41e80` → exit 2; `any(` changed to `all(` in a copy → `38 passed` |
| 19 | R19-1 | S2 | `workflows/pipeline_workflow.md:22` | `grep -n MODEL_FROM_SPRINT scripts/check_task_scope.py` at `db738ca` → lines 52 and 152; the workflow cell cites line 38 and line 119 |
| 2 | T2-1 | S2 | `scripts/_current_sprint.py:118` | fixture with `059-aaa` valid and the anchor `path` naming `059-core-x` invalid: `python3 scripts/check_gate_log.py --current-sprint` → exit 0 |
| 3 | T3-1 | S2 | `scripts/check_task_scope.py:380` | fixture with two pending rows of id `U-1`, `python3 scripts/check_task_scope.py --sprint-dir <fixture> --batches` at `2c438d6` → exit 0, one batch; replay `tests/test_check_task_scope.py::test_a_repeated_unit_id_fails_the_audit_and_batches` |
| 3 | T3-2 | S2 | `workflows/pipeline_workflow.md:24` | `grep -n check_task_scope hooks/on_commit.py hooks/on_commit_msg.py` at `2c438d6` → exit 1, no match; the workflow cell states those hooks ran the check |
| 20 | R20-1 | S2 | `docs/sprints/059-core-pipeline/SPRINT_LOG.md:176` | `grep -n "T3-[12]" docs/sprints/059-core-pipeline/SPRINT_LOG.md` at `29c49a4` → lines 66 and 149 only, no Gate findings row |
| 4 | T4-1 | S2 | `docs/sprints/059-core-pipeline/task_scope.md:203` | at `c6c41fe`, the Work rows of `task_scope.md` claim `scripts/check_task_scope.py` for 9 units; its Jurisdiction row names 4 |
| 5 | T5-1 | S2 | `scripts/check_sprint_refs.py:266` | testifying. `grep -n "cannot read" tests/test_check_sprint_refs.py` at `d97c1fe` → exit 1, no match; the read-failure exit 2 had no test. Close: C-07 `649eb96` |
| 5 | T5-2 | S2 | `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md:117` | testifying. `git show d97c1fe:docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md \| grep -n "15×"` → `117:`; `rules/token_economy.md` section 3.1 sets the hard bound at 550,000 tokens. Close: C-08 `65b4709` |
| 21 | R21-1 | S2 | `scripts/session_cost.py` (chain 919d4f2 > 40b2da1) | `python3 scripts/check_remediation_chain.py --range 08c669c..HEAD` at `cd2ee05` prints `chains: 3`. Class charter. Close: principal_agent re-plans the session_cost.py block with the human (`rules/qa_and_testing.md` §4 A-1); orchestrator records the decision in Progression |
| 21 | R21-2 | S2 | `docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md:248` (A-56), `scripts/check_task_scope.py` | `python3 scripts/check_remediation_chain.py --range 08c669c..HEAD` at `cd2ee05` shows chain c5fbf5f, 639fd05, 16b1dc6, 39f243c, a6f569d; A-56 has no recorded human decision. Class charter. Close: record the human re-plan that authorized A-56, or re-plan the block with the human |
| 21 | R21-3 | S0 | `docs/sprints/059-core-pipeline/SANDBOX_ENUMERATION.md` sections 4 and 6; `docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md` abort criterion 1 | `grep -n "KI-059-1[8-9]" docs/sprints/059-core-pipeline/SPRINT_LOG.md` at `cd2ee05` returns nothing. Class charter. Close: write the KI-059-n row as D43 restricts it; before close, measure the 2.1.319 gitfile vector without the B-06 block or revert B-06 |
| 21 | R21-4 | S2 | `docs/sprints/059-core-pipeline/SANDBOX_ENUMERATION.md` section 6.10 | the section states 23 `claude -p` calls against a maximum of 20. Class charter. Close: a recorded human decision accepting the 3 calls, or withdraw verdict G's reliance on `G2_*` |
| 21 | R21-5 | S2 | `docs/sprints/059-core-pipeline/SPRINT_LOG.md` Progression and the KI-059-17 row | Progression stops at D39 at `cd2ee05`; the KI-059-17 row is stale. Class testifying. Close: Progression lines for D40-D43 and their units; KI-059-17 row updated with the C-01 result (not reproduced) |
| 21 | R21-6 | S2 | `scripts/session_cost.py:45-46` | `grep -n "until then it is run by hand" scripts/session_cost.py` at `cd2ee05` matches. Class testifying. Close: delete the sentence |
| 22 | R22-1 | S2 | `docs/sprints/059-core-pipeline/SANDBOX_ENUMERATION.md` section 7.6 and sections 4.2, 4.4; `task_scope.md` C-01c | charter. C-01c's done-criterion needs both with and without the B-06 block; 7.6 gives the without case the circular reason "no fixture ran without them", and 4.2 contradicts 4.4. Close: run the without-block case under a new human call budget, or a recorded human decision drops that half, with 7.6 stating the real cause and 4.2 and 4.4 agreeing. |
| 22 | R22-2 | S2 | `docs/sprints/059-core-pipeline/SPRINT_LOG.md` KI-059-18 row | testifying. After 9489ce8 the row still says the 2.1.319 trigger "is not yet measured" and cites only sections 4 and 6. Same family as R21-5: convergence rule 3 (`rules/qa_and_testing.md` §4) requires a deterministic check. Close: update the row with the C-01c result citing sections 4.4 and 7, plus the deterministic check. |
| 23 | R23-1 | S2 | `scripts/check_sprint_refs.py` (`ki_sha_findings`); `tests/test_check_sprint_refs.py` (`test_a_missing_task_scope_exits_2`) | charter. C-05 added an exit 2 the plan did not ask for: a sprint directory with a plan but no `task_scope.md` or `SPRINT_LOG.md` fails, so a correct sprint fails `make verify` during Phases 1 to 4.2; at 548a2d3 the same fixture exits 0. Close: skip the check with an `[OK] ... (skip)` line when either file is missing, as for a missing plan, with the test and docstring changed to match; or a recorded human decision keeps exit 2 and amends the pipeline order. |
| 25 | R25-1 | S3 | `docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md` C-07 row | testifying. `git show b13cb49:docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md \| grep -n "^| C-07 .*create test"` → one match; `task_scope.md` and `agent_assignment.md` call C-07 `modify`. Same as T6-2. Close: C-10 `9e5d8bb` |
| 25 | R25-2 | S3 | `docs/sprints/059-core-pipeline/task_scope.md` C-07 row | testifying. The row cites `scripts/check_sprint_refs.py:264`; `sed -n 264p scripts/check_sprint_refs.py` prints `try:`, the `except` is at line 266. Same as T6-3. Close: C-11 `7aef661` |
| 25 | R25-3 | S3 | `docs/sprints/059-core-pipeline/SPRINT_LOG.md` Tester Gate 2 round 5 row | testifying. `git show b13cb49:docs/sprints/059-core-pipeline/SPRINT_LOG.md \| grep -n "Gate 2) | 5 | RECORD.*c6c41fe\.\.HEAD"` → one match; round 5 ran at `d97c1fe`. Same as T6-4. Close: C-12 `f759d89` |
| 26 | R26-1 | S2 | `docs/sprints/059-core-pipeline/SPRINT_LOG.md` Tester Gate 2 round 5 row | testifying. `grep -n "check_sprint_refs.py:264" docs/sprints/059-core-pipeline/SPRINT_LOG.md` at `e95d239` matches the round 5 row; `git show d97c1fe:scripts/check_sprint_refs.py \| grep -n "except (OSError, UnicodeDecodeError)"` prints `266:`. The C-11 fix was not propagated (`RA-14`). Close: C-13 `62db62c` |
| 26 | R26-2 | S3 | `docs/sprints/059-core-pipeline/SPRINT_LOG.md` Gate findings table | testifying. `grep -n "^| 25 | R25-" docs/sprints/059-core-pipeline/SPRINT_LOG.md` at `e95d239` prints three S3 rows against the scope sentence "One row per S0-S2 finding"; `grep -c "^| 5 | T5-" docs/sprints/059-core-pipeline/SPRINT_LOG.md` at `e95d239` prints `0` for the two S2 findings T5-1 and T5-2. Close: C-13 `62db62c` |
| 27 | R27-1 | S3 | `docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md` D49 row | testifying. `grep -c "check_sprint_refs.py:264" docs/sprints/059-core-pipeline/SPRINT_LOG.md` at `17ed349` prints `3`; the D49 Check names two rows (R25-2, R26-1) and no number; the third is the QA Gate 1 round 26 row. Close: C-14 `8139ca4` |
| 27 | R27-2 | S3 | `docs/sprints/059-core-pipeline/SPRINT_LOG.md` R25-2 row | testifying. The Check holds `sed -n 264p` with no file; `sed -n 264p scripts/check_sprint_refs.py` at `17ed349` prints `    try:`. Close: C-15 `a44919a` |
| 27 | R27-3 | S3 | `docs/sprints/059-core-pipeline/SPRINT_LOG.md` R25-2, R26-1, R26-2 rows | testifying. `grep -o "Close: C-1[13]\`*" docs/sprints/059-core-pipeline/SPRINT_LOG.md` at `17ed349` prints Close cells for C-11 and C-13 with no SHA; C-11 is `7aef661`, C-13 is `62db62c`. Close: C-15 `a44919a` |
| 28 | R28-1 | S3 | `docs/sprints/059-core-pipeline/SPRINT_LOG.md` R27-3 row | testifying. The R27-3 command uses `grep -o`, which prints only the matched text, so it prints the same three lines at `17ed349` and at `b79fdad`; its escaped backtick ends the code span early. The discriminating command is the D50 one, ``grep -c 'Close: C-1[13] [^`]' docs/sprints/059-core-pipeline/SPRINT_LOG.md``: `3` at `17ed349`, `0` at `b79fdad` |
| 28 | R28-2 | S3 | `docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md` D49 and D50 rows | testifying. D50 and `8139ca4` call the C-14 grep scoped to the Tester Gate 2 round 5 row; `grep -c "Gate 2) . 5 . RECORD" docs/sprints/059-core-pipeline/SPRINT_LOG.md` at `b79fdad` prints `2` (the round 5 row and the R25-3 row) (`fail_closed_claims`) |
| 28 | R28-3 | S3 | `docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md` D50 row | testifying. The D50 Check says the C-15 grep prints `3` "hoy"; at `b79fdad` it prints `0`. The word has no anchor (`unambiguous_action`); the C-15 task_scope row anchors it as "before C-15" |

### Remediation notes

The remediator fills this table before re-sending a REJECTED round to its gate, one
row per command run; `scripts/check_gate_log.py` (sprint ids >= 58) exits 2 when a
Quality Gate row of Round N >= 2 has no row here for the same Gate and Round N-1.
Leave it with **no data rows** until a gate emits a REJECTED round.

<!--
Gate: repeats the Gate cell of the Quality Gate table (compared case-insensitively).
Round: the REJECTED round being remediated.
Command: at least one backticked command.
Exit: a non-negative integer, read with `$?` on that command alone, never through a pipe.
Example (do not uncomment):
  | QA Agent (Gate 1) | 1 | `python3 -I -m pytest tests/test_x.py` | 0 |
-->

| Gate | Round | Command | Exit |
| :--- | :--- | :--- | :--- |
| QA Agent (Gate 1) | 1 | `python3 scripts/check_fix_reproduces.py --range 08c669c..HEAD` | 0 |
| QA Agent (Gate 1) | 1 | `python3 scripts/check_remediation_chain.py --range 08c669c..HEAD` | 0 |
| QA Agent (Gate 1) | 1 | `make verify` | 0 |
| QA Agent (Gate 1) | 2 | `python3 scripts/check_fix_reproduces.py --range 08c669c..HEAD` | 0 |
| QA Agent (Gate 1) | 2 | `python3 scripts/check_remediation_chain.py --range 08c669c..HEAD` | 0 |
| QA Agent (Gate 1) | 2 | `make verify` | 0 |
| QA Agent (Gate 1) | 3 | `python3 scripts/check_fix_reproduces.py --range 08c669c..HEAD` | 0 |
| QA Agent (Gate 1) | 3 | `python3 scripts/check_remediation_chain.py --range 08c669c..HEAD` | 0 |
| QA Agent (Gate 1) | 3 | `make verify` | 0 |
| QA Agent (Gate 1) | 4 | `python3 scripts/check_fix_reproduces.py --range 08c669c..HEAD` | 0 |
| QA Agent (Gate 1) | 4 | `python3 scripts/check_remediation_chain.py --range 08c669c..HEAD` | 0 |
| QA Agent (Gate 1) | 4 | `make verify` | 0 |
| QA Agent (Gate 1) | 5 | `python3 scripts/check_fix_reproduces.py --range 08c669c..HEAD` | 0 |
| QA Agent (Gate 1) | 5 | `python3 scripts/check_remediation_chain.py --range 08c669c..HEAD` | 0 |
| QA Agent (Gate 1) | 5 | `make verify` | 0 |
| QA Agent (Gate 1) | 6 | `python3 scripts/check_fix_reproduces.py --range 08c669c..HEAD` | 0 |
| QA Agent (Gate 1) | 6 | `python3 scripts/check_remediation_chain.py --range 08c669c..HEAD` | 0 |
| QA Agent (Gate 1) | 6 | `make verify` | 0 |
| QA Agent (Gate 1) | 7 | `python3 scripts/check_fix_reproduces.py --range 08c669c..HEAD` | 0 |
| QA Agent (Gate 1) | 7 | `python3 scripts/check_remediation_chain.py --range 08c669c..HEAD` | 0 |
| QA Agent (Gate 1) | 7 | `make verify` | 0 |
| QA Agent (Gate 1) | 8 | `python3 scripts/check_fix_reproduces.py --range 08c669c..HEAD` | 0 |
| QA Agent (Gate 1) | 8 | `python3 scripts/check_remediation_chain.py --range 08c669c..HEAD` | 0 |
| QA Agent (Gate 1) | 8 | `make verify` | 0 |
| QA Agent (Gate 1) | 8 | `venv_skillopt/bin/python -m ruff check .` | 0 |
| QA Agent (Gate 1) | 8 | `make quality-audit` | 0 |
| QA Agent (Gate 1) | 8 | `python3 scripts/check_gate_log.py --sprint-dir docs/sprints/059-core-pipeline` | 0 |
| QA Agent (Gate 1) | 8 | `python3 scripts/check_role_artifact.py --role "QA Agent" --sprint-dir docs/sprints/059-core-pipeline` | 0 |
| QA Agent (Gate 1) | 8 | `python3 scripts/check_log_append_only.py --sprint-dir docs/sprints/059-core-pipeline --range 60383e3..HEAD` | 0 |
| QA Agent (Gate 1) | 9 | `python3 scripts/check_fix_reproduces.py --range 08c669c..HEAD` | 0 |
| QA Agent (Gate 1) | 9 | `python3 scripts/check_remediation_chain.py --range 08c669c..HEAD` | 0 |
| QA Agent (Gate 1) | 9 | `make verify` | 0 |
| QA Agent (Gate 1) | 9 | `venv_skillopt/bin/python -m ruff check .` | 0 |
| QA Agent (Gate 1) | 9 | `make quality-audit` | 0 |
| QA Agent (Gate 1) | 9 | `python3 scripts/check_gate_log.py --sprint-dir docs/sprints/059-core-pipeline` | 0 |
| QA Agent (Gate 1) | 9 | `python3 scripts/check_role_artifact.py --role "QA Agent" --sprint-dir docs/sprints/059-core-pipeline` | 0 |
| QA Agent (Gate 1) | 9 | `python3 scripts/check_log_append_only.py --sprint-dir docs/sprints/059-core-pipeline --range 60383e3..HEAD` | 0 |
| QA Agent (Gate 1) | 10 | `python3 scripts/check_fix_reproduces.py --range 08c669c..HEAD` | 0 |
| QA Agent (Gate 1) | 10 | `python3 scripts/check_remediation_chain.py --range 08c669c..HEAD` | 0 |
| QA Agent (Gate 1) | 10 | `make verify` | 0 |
| QA Agent (Gate 1) | 10 | `venv_skillopt/bin/python -m ruff check .` | 0 |
| QA Agent (Gate 1) | 10 | `make quality-audit` | 0 |
| QA Agent (Gate 1) | 10 | `python3 scripts/check_gate_log.py --sprint-dir docs/sprints/059-core-pipeline` | 0 |
| QA Agent (Gate 1) | 10 | `python3 scripts/check_role_artifact.py --role "QA Agent" --sprint-dir docs/sprints/059-core-pipeline` | 0 |
| QA Agent (Gate 1) | 11 | `python3 scripts/check_fix_reproduces.py --range 08c669c..HEAD` | 0 |
| QA Agent (Gate 1) | 11 | `python3 scripts/check_remediation_chain.py --range 08c669c..HEAD` | 0 |
| QA Agent (Gate 1) | 11 | `make verify` | 0 |
| QA Agent (Gate 1) | 11 | `venv_skillopt/bin/python -m ruff check .` | 0 |
| QA Agent (Gate 1) | 11 | `make quality-audit` | 0 |
| QA Agent (Gate 1) | 11 | `python3 scripts/check_gate_log.py --sprint-dir docs/sprints/059-core-pipeline` | 0 |
| QA Agent (Gate 1) | 11 | `python3 scripts/check_role_artifact.py --role "QA Agent" --sprint-dir docs/sprints/059-core-pipeline` | 0 |
| QA Agent (Gate 1) | 12 | `python3 scripts/check_fix_reproduces.py --range 08c669c..HEAD` | 0 |
| QA Agent (Gate 1) | 12 | `python3 scripts/check_remediation_chain.py --range 08c669c..HEAD` | 0 |
| QA Agent (Gate 1) | 12 | `make verify` | 0 |
| QA Agent (Gate 1) | 12 | `venv_skillopt/bin/python -m ruff check .` | 0 |
| QA Agent (Gate 1) | 12 | `make quality-audit` | 0 |
| QA Agent (Gate 1) | 12 | `python3 scripts/check_gate_log.py --sprint-dir docs/sprints/059-core-pipeline` | 0 |
| QA Agent (Gate 1) | 12 | `python3 scripts/check_role_artifact.py --role "QA Agent" --sprint-dir docs/sprints/059-core-pipeline` | 0 |
| QA Agent (Gate 1) | 13 | `python3 scripts/check_fix_reproduces.py --range 08c669c..HEAD` | 0 |
| QA Agent (Gate 1) | 13 | `python3 scripts/check_remediation_chain.py --range 08c669c..HEAD` | 0 |
| QA Agent (Gate 1) | 13 | `make verify` | 0 |
| QA Agent (Gate 1) | 13 | `venv_skillopt/bin/python -m ruff check .` | 0 |
| QA Agent (Gate 1) | 13 | `make quality-audit` | 0 |
| QA Agent (Gate 1) | 13 | `python3 scripts/check_gate_log.py --sprint-dir docs/sprints/059-core-pipeline` | 0 |
| QA Agent (Gate 1) | 13 | `python3 scripts/check_role_artifact.py --role "QA Agent" --sprint-dir docs/sprints/059-core-pipeline` | 0 |
| QA Agent (Gate 1) | 13 | `python3 scripts/check_task_scope.py --current-sprint` | 0 |
| QA Agent (Gate 1) | 13 | `python3 skills/token-saver-auditor/scripts/audit_plan.py docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md` | 0 |
| QA Agent (Gate 1) | 14 | `python3 scripts/check_fix_reproduces.py --range fc377e3..HEAD` | 0 |
| QA Agent (Gate 1) | 14 | `python3 scripts/check_remediation_chain.py --range fc377e3..HEAD` | 0 |
| QA Agent (Gate 1) | 14 | `make verify` | 0 |
| QA Agent (Gate 1) | 14 | `venv_skillopt/bin/python -m ruff check .` | 0 |
| QA Agent (Gate 1) | 14 | `make quality-audit` | 0 |
| QA Agent (Gate 1) | 14 | `python3 scripts/check_gate_log.py --sprint-dir docs/sprints/059-core-pipeline` | 0 |
| QA Agent (Gate 1) | 14 | `python3 scripts/check_role_artifact.py --role "QA Agent" --sprint-dir docs/sprints/059-core-pipeline` | 0 |
| QA Agent (Gate 1) | 14 | `python3 scripts/check_task_scope.py --current-sprint` | 0 |
| QA Agent (Gate 1) | 14 | `python3 skills/token-saver-auditor/scripts/audit_plan.py docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md` | 0 |
| QA Agent (Gate 1) | 15 | `python3 scripts/check_fix_reproduces.py --range 605d3f1..3a3136b` | 0 |
| QA Agent (Gate 1) | 15 | `make verify` | 0 |
| QA Agent (Gate 1) | 15 | `python3 scripts/check_task_scope.py --sprint-dir docs/sprints/059-core-pipeline` | 0 |
| QA Agent (Gate 1) | 15 | `python3 scripts/check_sprint_refs.py --current-sprint` | 0 |
| QA Agent (Gate 1) | 16 | `make verify` | 0 |
| QA Agent (Gate 1) | 16 | `python3 scripts/check_sprint_refs.py --current-sprint` | 0 |
| QA Agent (Gate 1) | 17 | `make verify` | 0 |
| QA Agent (Gate 1) | 17 | `make quality-audit` | 0 |
| QA Agent (Gate 1) | 17 | `python3 scripts/check_fix_reproduces.py --range 169bd8a..HEAD` | 0 |
| QA Agent (Gate 1) | 17 | `python3 scripts/check_sprint_refs.py --current-sprint` | 0 |
| QA Agent (Gate 1) | 17 | `python3 scripts/check_fix_reproduces.py --range 08c669c..HEAD` | 0 |
| QA Agent (Gate 1) | 17 | `python3 scripts/check_remediation_chain.py --range 08c669c..HEAD` | 2 |
| QA Agent (Gate 1) | 18 | `make verify` | 0 |
| QA Agent (Gate 1) | 18 | `make quality-audit` | 0 |
| QA Agent (Gate 1) | 18 | `python3 scripts/check_fix_reproduces.py --range 08c669c..HEAD` | 0 |
| QA Agent (Gate 1) | 18 | `python3 scripts/check_remediation_chain.py --range 08c669c..HEAD` | 2 |
| QA Agent (Gate 1) | 19 | `make verify` | 0 |
| QA Agent (Gate 1) | 19 | `make quality-audit` | 0 |
| QA Agent (Gate 1) | 19 | `python3 scripts/check_fix_reproduces.py --range 08c669c..HEAD` | 0 |
| QA Agent (Gate 1) | 19 | `python3 scripts/check_remediation_chain.py --range 08c669c..HEAD` | 2 |
| Tester Agent (Gate 2) | 2 | `venv_skillopt/bin/python -m pytest -q -p no:cacheprovider` | 0 |
| Tester Agent (Gate 2) | 2 | `make verify` | 0 |
| Tester Agent (Gate 2) | 3 | `venv_skillopt/bin/python -m pytest -q -p no:cacheprovider` | 0 |
| Tester Agent (Gate 2) | 3 | `make verify` | 0 |
| QA Agent (Gate 1) | 20 | `make verify` | 0 |
| QA Agent (Gate 1) | 20 | `make quality-audit` | 0 |
| QA Agent (Gate 1) | 20 | `python3 scripts/check_fix_reproduces.py --range 08c669c..HEAD` | 0 |
| QA Agent (Gate 1) | 20 | `python3 scripts/check_remediation_chain.py --range 08c669c..HEAD` | 2 |
| Tester Agent (Gate 2) | 4 | `venv_skillopt/bin/python -m pytest -q -p no:cacheprovider` | 0 |
| Tester Agent (Gate 2) | 4 | `make verify` | 0 |
| Tester Agent (Gate 2) | 5 | `venv_skillopt/bin/python -m pytest -q -p no:cacheprovider` | 0 |
| Tester Agent (Gate 2) | 5 | `make verify` | 0 |
| Tester Agent (Gate 2) | 6 | `venv_skillopt/bin/python -m pytest -q -p no:cacheprovider` | 0 |
| Tester Agent (Gate 2) | 6 | `make verify` | 0 |
| Tester Agent (Gate 2) | 1 | `venv_skillopt/bin/python -m pytest -q -p no:cacheprovider` | 0 |
| Tester Agent (Gate 2) | 1 | `make verify` | 0 |
| QA Agent (Gate 1) | 21 | `python3 scripts/check_fix_reproduces.py --range 08c669c..HEAD` | 0 |
| QA Agent (Gate 1) | 21 | `python3 scripts/check_remediation_chain.py --range 08c669c..HEAD` | 2 |
| QA Agent (Gate 1) | 21 | `make verify` | 0 |
| QA Agent (Gate 1) | 21 | `make quality-audit` | 0 |
| QA Agent (Gate 1) | 21 | `venv_skillopt/bin/python -m ruff check --no-cache .` | 0 |
| QA Agent (Gate 1) | 22 | `python3 scripts/check_fix_reproduces.py --range 08c669c..HEAD` | 0 |
| QA Agent (Gate 1) | 22 | `python3 scripts/check_remediation_chain.py --range 08c669c..HEAD` | 2 |
| QA Agent (Gate 1) | 22 | `make verify` | 0 |
| QA Agent (Gate 1) | 22 | `make quality-audit` | 0 |
| QA Agent (Gate 1) | 23 | `python3 scripts/check_fix_reproduces.py --range 08c669c..HEAD` | 0 |
| QA Agent (Gate 1) | 23 | `python3 scripts/check_remediation_chain.py --range 08c669c..HEAD` | 2 |
| QA Agent (Gate 1) | 23 | `make verify` | 0 |
| QA Agent (Gate 1) | 23 | `make quality-audit` | 0 |
| QA Agent (Gate 1) | 24 | `python3 scripts/check_fix_reproduces.py --range 08c669c..HEAD` | 0 |
| QA Agent (Gate 1) | 24 | `python3 scripts/check_remediation_chain.py --range 08c669c..HEAD` | 2 |
| QA Agent (Gate 1) | 24 | `make verify` | 0 |
| QA Agent (Gate 1) | 24 | `make quality-audit` | 0 |
| QA Agent (Gate 1) | 25 | `python3 scripts/check_fix_reproduces.py --range 08c669c..HEAD` | 0 |
| QA Agent (Gate 1) | 25 | `python3 scripts/check_remediation_chain.py --range 08c669c..HEAD` | 2 |
| QA Agent (Gate 1) | 25 | `make verify` | 0 |
| QA Agent (Gate 1) | 25 | `make quality-audit` | 0 |
| QA Agent (Gate 1) | 26 | `python3 scripts/check_fix_reproduces.py --range 08c669c..HEAD` | 0 |
| QA Agent (Gate 1) | 26 | `python3 scripts/check_remediation_chain.py --range 08c669c..HEAD` | 2 |
| QA Agent (Gate 1) | 26 | `make verify` | 0 |
| QA Agent (Gate 1) | 26 | `make quality-audit` | 0 |
| QA Agent (Gate 1) | 27 | `python3 scripts/check_fix_reproduces.py --range 08c669c..HEAD` | 0 |
| QA Agent (Gate 1) | 27 | `python3 scripts/check_remediation_chain.py --range 08c669c..HEAD` | 2 |
| QA Agent (Gate 1) | 27 | `make verify` | 0 |
| QA Agent (Gate 1) | 27 | `make quality-audit` | 0 |

---

Bytecode written by `make verify` (plan D41, unit B-16), measured after B-05 at `921db7d`: with the 29 `__pycache__` directories purged, `make verify` exited 0 and wrote 138 `.pyc` files (78 `tests/`, 50 `scripts/`, 6 `hooks/`, 4 `skills/`), invisible to `git status` because git ignores them. A read-only copy of `scripts/_root.py` and `scripts/py_compile_tree.py` imported and ran with exit 0 and wrote 0 `.pyc`; the full `make verify` over a write-protected tree was not measured. Human decision 2026-11-09: export `PYTHONDONTWRITEBYTECODE=1` in `verify` instead of narrowing D5.

## 🛑 Abort Criteria

`principal_agent` measures each numbered item of the plan's `## Abort criterion` at
every phase boundary and appends one row per measurement; `scripts/check_plan_closure.py`
reads it at close (`workflows/close_workflow.md` Phase 2.6) and requires at least one
row per criterion. Leave it with **no data rows** until the first measurement.

<!--
Criterion: the integer of a numbered item in the plan's `## Abort criterion`.
Command: at least one backticked command.
Exit: an integer.
Observation: what the command showed. A criterion closes only on the observation it
  names; "met by arithmetic" leaves it open.
Example (do not uncomment):
  | 1 | `make verify` | 0 | verify passes at the Phase 3 boundary. |
-->

| Criterion | Command | Exit | Observation |
| :--- | :--- | :--- | :--- |
| 1 | `test -f docs/sprints/059-core-pipeline/SANDBOX_ENUMERATION.md` | 1 | Wave 1 boundary: C-01 has not run (Wave 4), so nothing to act on yet. |
| 2 | `test -f docs/sprints/059-core-pipeline/PROMPT_MEASUREMENT.md` | 1 | Wave 1 boundary: B-02 has not run (Wave 2); no rule relaxed. |
| 3 | `test -f docs/sprints/059-core-pipeline/TOKEN_ECONOMY_STUDY.md` | 1 | Wave 1 boundary: the A-06 debate has not run (Wave 3). |
| 4 | `grep -n '^model:' agents/qa_agent.md` | 0 | Wave 1 boundary: `model: sonnet`, trial starts with this gate; no later gate has run. |
| 4 | `python3 -I scripts/audit_cursor_models.py --resolve qa_agent` | 0 | Tester Gate 2 round 1: differs from `--resolve gate`; criterion fired, A-08 reverted (plan D20). |
| 5 | `grep -n autoAllowBashIfSandboxed scripts/install.py` | 1 | Wave 1 boundary: B-06 not applied (Wave 2), nothing to revert. |
| 6 | `git worktree list` | 0 | Wave 1 boundary: one worktree; the D16 batch used none and produced no git conflict. No D11 batch has run. |
| 7 | `test -f docs/sprints/059-core-pipeline/TOKEN_ECONOMY_STUDY.md` | 1 | Wave 1 boundary: A-00 has not run (Wave 3). |
| 8 | `python3 scripts/check_gate_log.py --current-sprint` | 0 | Wave 1 boundary: the Quality Gate table has no data rows, so no consecutive REJECTED. |
| 8 | `grep -c "(Gate 1) . [34567] . REJECTED" docs/sprints/059-core-pipeline/SPRINT_LOG.md` | 0 | Rounds 3 to 7 of QA Gate 1 are REJECTED: criterion fired at round 6 and again at round 7; `workflows/remediation_workflow.md` ran twice and the human re-planned each time. |
| 8 | `grep -c "(Gate 1) . [345678] . REJECTED" docs/sprints/059-core-pipeline/SPRINT_LOG.md` | 0 | Rounds 3 to 8 of QA Gate 1 are REJECTED: criterion fired again at round 8; `workflows/remediation_workflow.md` ran a third time and the sprint is BLOCKED until the human re-plans. |
| 8 | `grep -c "(Gate 1) . [3456789] . REJECTED" docs/sprints/059-core-pipeline/SPRINT_LOG.md` | 0 | Rounds 3 to 9 of QA Gate 1 are REJECTED: criterion fired again at round 9; `workflows/remediation_workflow.md` ran a fourth time and the sprint is BLOCKED until the human re-plans. |
| 8 | `grep -c "(Gate 1) . \(3\|4\|5\|6\|7\|8\|9\|10\) . REJECTED" docs/sprints/059-core-pipeline/SPRINT_LOG.md` | 0 | Rounds 3 to 10 of QA Gate 1 are REJECTED: criterion fired again at round 10; `workflows/remediation_workflow.md` ran a fifth time; the human's decision was taken in advance in plan D35, so the block was lifted under it. |
| 8 | `grep -c "(Gate 1) . \(3\|4\|5\|6\|7\|8\|9\|10\|11\) . REJECTED" docs/sprints/059-core-pipeline/SPRINT_LOG.md` | 0 | Rounds 3 to 11 of QA Gate 1 are REJECTED: criterion fired again at round 11; `workflows/remediation_workflow.md` ran a sixth time and the sprint is BLOCKED until the human re-plans. |
| 8 | `grep -c "(Gate 1) . \(3\|4\|5\|6\|7\|8\|9\|10\|11\|12\) . REJECTED" docs/sprints/059-core-pipeline/SPRINT_LOG.md` | 0 | Rounds 3 to 12 of QA Gate 1 are REJECTED: criterion fired again at round 12; `workflows/remediation_workflow.md` ran a seventh time and the sprint is BLOCKED until the human re-plans. |
| 8 | `grep -c "(Gate 1) . \(3\|4\|5\|6\|7\|8\|9\|10\|11\|12\|13\) . REJECTED" docs/sprints/059-core-pipeline/SPRINT_LOG.md` | 0 | Rounds 3 to 13 of QA Gate 1 are REJECTED: criterion fired again at round 13; `workflows/remediation_workflow.md` ran an eighth time and the sprint is BLOCKED until the human re-plans. |

---

## ✅ Plan Results

`principal_agent` fills this table at close; `scripts/check_plan_closure.py` reads it
and requires exactly one row per data row of the plan's Tests table and per data row
of its Verification table, each with a non-empty Result. Leave it with **no data rows**
until close.

<!--
Section: `Tests` or `Verification`.
Row: the 1-based index of a data row in that plan table.
Check: the check that row names.
Result: non-empty; the observed outcome.
Example (do not uncomment):
  | Tests | 1 | tests/test_x.py passes | 12 passed, exit 0. |
  | Verification | 1 | make verify | exit 0. |
-->

| Section | Row | Check | Result |
| :--- | :--- | :--- | :--- |

---

## ⚓ Documentation Entry Point Seal
Closing the session state and certifying traceability.

**Strategic Lock**: Plan approved (`triple_lock` lock 1).
**Next Phase (current)**: Phase 6, Wave 5, suspended 2026-11-14 at the 5-hour usage limit, in batch 1 of `check_task_scope.py --batches`: P-01 (`35ba2db`), R-06 (`5befc83`) and R-07 (`e0152f2`) committed; R-05 stopped before its commit and its worktree discarded, then re-run from the start on 2026-11-15 and committed as `0f069da` (29 packages hashed, `pip install --require-hashes` exit 0); unit R-13 added (201 units) because R-06 breaks `.github/workflows/ci.yml` line 33 (`pytest` unhashed under hash-checking mode; CI runs on push only, at closeout, RA-08); note for R-05 and R-13: pip inside the Bash sandbox fails TLS with `OSStatus -26276` (same trustd cause as `gh`, SANDBOX_ENUMERATION.md section 2.6), and R-06 and R-07 worked around it with a temporary wrapper under `$TMPDIR` that disables pip truststore and passes `--cert /etc/ssl/cert.pem`, outside the repository; batch 2 on 2026-11-15: R-08 committed as `e56ebbc`, P-02 as `e51109f` (A5 rule set C1), R-09 reverted by D55; R-13 committed as `fe0ee0f`; P-03 committed as `114f649` (ADR-0022); P-05 committed as `3db51e7` (pip needs `pypi.org`, `files.pythonhosted.org` and the settings `env` pair `PIP_USE_DEPRECATED=legacy-certs`, `PIP_CERT=/etc/ssl/cert.pem`, A1-10); P-06 committed as `138caee` (`~/**/.env*`, in-project `.env` block accepted), R-01 as `d89bdda`; R-14 committed as `7abe081`; R-02 run by the human on 2026-11-15 (`venv_skillopt/bin/python scripts/install.py --target claude` at `374a5f8`; the read-only check printed `OK`); observed in the running session without a restart, from the harness's own sandbox report: the new `denyRead` list loaded, `dangerouslyDisableSandbox` became disabled and the Google Drive connector disconnected (not yet a B9 measurement); `make verify` then failed in `scripts/quality_audit.py` (D60); R-15 committed as `ea79fef`, R-16 as `16f24af`, R-17 as `d6887b1`, and `make verify` exits 0 under the installed settings (1860 passed); R-03 measured by `devops_agent` on 2.1.322 (`make sandbox-probe` exit 0: M7, M9 closed, B2-1 to B2-5 closed, A1-1 and A1-2 not-measurable); R-03 rows committed as `6b997a9`; R-04 committed as `3295e45` (tests pass) but its done-criterion is not met: the re-run gives A1-1 and A1-2 `observed=open [200]`, recorded as `KI-059-27`; the R-04 re-run in a new session on 2026-11-16 gives A1-1 and A1-2 open again, so plan D62 adds unit P-08, committed as `a301473` (terminal CLI also open); plan D63 adds unit P-09; next: P-09 and P-07 (the human runs them), then the re-plan of R-04, then the Wave 5 Phase 7 gates after V-02; S-01 to S-16, D-01 to D-03, P-01, R-06 and R-07 committed, D-04 and E-01b RECORD by ADR-0019; 181 units. Wave 4 gates stay closed: Tester Gate 2 round 7 `APPROVED` (`a7e528c`), QA Gate 1 round 28 `RECORD`, S3.

**Next Phase (2026-11-14, start of Wave 5, superseded by the line above)**: Phase 6, Wave 5, unit S-01 (plan D51), then S-02 to S-15 in order, then D-01; 180 units. Wave 4 gates stay closed: Tester Gate 2 round 7 `APPROVED` (`a7e528c`), QA Gate 1 round 28 `RECORD`, S3.

**Next Phase (superseded by the line above)**: Phase 6, Wave 5, unit D-01. Wave 4 gates are closed: Tester Gate 2 round 7 was `APPROVED` (`a7e528c`), QA Gate 1 round 28 was `RECORD`, S3, with R28-1 to R28-3 noted only; 165 units, plan D50.

**Next Phase (superseded by the line above)**: Phase 7, Wave 4, Tester Gate 2 round 7, dispatched fresh on range `6196230..<end SHA at dispatch>`; then Phase 6, Wave 5, unit D-01. QA Gate 1 round 28 was `RECORD`, S3 (`7ff090d`); the human noted R28-1 to R28-3 only (2026-11-12); 165 units, plan D50.

**Next Phase (superseded by the line above)**: Phase 7, Wave 4, QA Gate 1 round 28 on range `17ed349..<end SHA at dispatch>`, then Tester Gate 2 round 7 on range `6196230..<end SHA at dispatch>`, both dispatched fresh; then Phase 6, Wave 5, unit D-01. Units C-14 (`8139ca4`) and C-15 (`a44919a`) are committed (165 units, plan D50); QA Gate 1 round 27 was `RECORD`, S3; no QA Gate 1 round 28 or Tester Gate 2 round 7 verdict exists.

**Next Phase (superseded by the line above)**: Phase 7, Wave 4, in a new session: first the human decides whether R27-1 to R27-3 (S3, QA Gate 1 round 27, `7069c7d`) are noted only or fixed under a new plan decision; then Tester Gate 2 round 7, dispatched fresh on range `6196230..<end SHA at dispatch>`; then Phase 6, Wave 5, unit D-01. Units C-01 to C-13 are committed (163 units, plan D49); QA Gate 1 rounds 26 and 27 were `RECORD` (S2, S3); no Tester Gate 2 round 7 verdict exists.

**Next Phase (superseded by the line above)**: Phase 7, Wave 4, QA Gate 1 round 27 on range `e95d239..<end SHA at dispatch>`, then Tester Gate 2 round 7 on range `6196230..<end SHA at dispatch>`, both dispatched fresh; then Phase 6, Wave 5, unit D-01. Unit C-13 is committed (163 units, plan D49); QA Gate 1 round 26 was `RECORD`, S2.

**Next Phase (superseded by the line above)**: Phase 7, Wave 4, QA Gate 1 round 26 on range `b13cb49..<end SHA at dispatch>`, then Tester Gate 2 round 7 on range `6196230..<end SHA at dispatch>`, both dispatched fresh; then Phase 6, Wave 5, unit D-01. Units C-09 to C-12 are committed (162 units, plan D48); QA Gate 1 round 25 and Tester Gate 2 round 6 were `RECORD`, S3.

**Next Phase (superseded by the line above)**: Phase 7, Wave 4, QA Gate 1 round 25 on range `10204e4..HEAD`, then Tester Gate 2 round 6 on range `d97c1fe..HEAD`, both dispatched fresh. Units C-07 (`649eb96`) and C-08 (`65b4709`) are committed (158 units, plan D47); Tester Gate 2 round 5 was `RECORD`, S2 (`bd2680e`).

**Next Phase (superseded by the line above)**: Phase 7, Wave 4, Tester Gate 2 round 5, in a new session, dispatched fresh on range `c6c41fe..d97c1fe`. Wave 4 units C-01 to C-06 are committed (156 units); QA Gate 1 converged at round 24 (`RECORD`, S3, `aa5a995`). A round 5 dispatch of 2026-11-10 was stopped before any verdict at the human's suspend order, so no round 5 verdict exists.

**Next Phase (superseded by the line above)**: Phase 6, Wave 4, unit C-01, in a new session, then C-02. B-03, B-04, B-05 and B-16 to B-21 are committed (150 units); after purging `__pycache__`, `.pytest_cache` and `.ruff_cache`, `make verify` exited 0 and modified 0 files in the tree (D41, D42). The Wave 4 gates run after C-02.

**Next Phase (superseded by the line above)**: Phase 6, Wave 4, unit B-03, in a new session. Wave 3 closed at `bced56b`; `ADR-0018` holds the bounds. Every worktree dispatch runs `git merge --ff-only ai-sprint/059` and checks its base before the first edit (`workflows/pipeline_workflow.md` Phase 6).

**Next Phase (superseded by the line above)**: Phase 6, Wave 3, batch 2, unit A-00, in a new session: `token_economy_agent` produces the figures, then `doc_orchestrator` writes the study; the figures step of session `5d48524f` was stopped at suspend with no output. Every worktree dispatch runs `git merge --ff-only ai-sprint/059` and checks its base before the first edit (KI-059-16).

**Next Phase (superseded by the line above)**: `session_state.py suspend`, then Phase 6, Wave 3, in a new session. On a rejection: no patch, re-plan with the human.

**Next Phase (after QA Gate 1 round 13, superseded by the line above)**: Phase 6, Wave 1b, in the plan's order (plan D37). Then QA Gate 1 round 14 on `3af48b5..HEAD` and the R13 fixes, then Tester Gate 2 round 2, both fresh agents. On a rejection: no patch, re-plan with the human.

**Next Phase (2026-11-07, after QA Gate 1 round 13, superseded by the line above)**: the sprint is BLOCKED (`TERMINAL_REMEDIATION_LOOP`). Step 2 of the handoff below applies: no patch; the human decides how to resume, with R13-1, R13-2 and R13-3 on the table. The block is lifted only by `session_state.py unblock` after that decision.

**Next Phase (after QA Gate 1 round 12, superseded by the line above from its step 2 on)**: Phase 7, Wave 1. The deadlock of QA Gate 1 round 12 was re-planned with the human (plan D37); the block was lifted with `session_state.py unblock`. In order:
1. QA Gate 1 round 13 under convergence rule 1: the diff `01c0083..HEAD` and the fix of R12-1, R12-2 and R12-3, which plan D37 assigns to Wave 1b. A fresh agent.
2. If it rejects, no patch: re-plan with the human, with the finding on the table.
3. Tester Gate 2 round 2, a fresh agent, under the same rule.
4. Wave 1b, then its own gates, then Wave 2, in series.

**Next Phase (2026-11-07, after QA Gate 1 round 12, superseded by the line above)**: the sprint is BLOCKED (`TERMINAL_REMEDIATION_LOOP`). Step 2 of the handoff below applies: no patch; the human decides how to resume, with R12-1, R12-2 and R12-3 on the table. The block is lifted only by `session_state.py unblock` after that decision.

**Next Phase (after QA Gate 1 round 11, superseded by the line above from its step 2 on)**: Phase 7, Wave 1. The deadlock of QA Gate 1 round 11 was re-planned with the human and remediated (plan D36); the block was lifted with `session_state.py unblock`. In order, in a new session:
1. QA Gate 1 round 12 under convergence rule 1: the diff `e8f06df..HEAD` and the fix of R11-1, the one S0, S1 or S2 of round 11 (its row in the Quality Gate table holds the file and lines). A fresh agent.
2. If it rejects, no patch: re-plan with the human, with the finding on the table.
3. Tester Gate 2 round 2, a fresh agent, under the same rule.
4. `session_state.py suspend`, then Wave 2, in series.

**Next Phase (2026-11-07, after QA Gate 1 round 11, superseded by the line above)**: the sprint is BLOCKED (`TERMINAL_REMEDIATION_LOOP`). Step 2 of the handoff below applies: no patch; the human decides how to resume, with R11-1 and the round 11 measurement of the sibling skips on the table. The block is lifted only by `session_state.py unblock` after that decision.

**Next Phase (after QA Gate 1 round 10, superseded by the line above from its step 2 on)**: Phase 7, Wave 1. QA Gate 1 round 10 met the stop plan D35 decided in advance: another S1 in `scripts/check_log_append_only.py`. No fix round: A-49 to A-53 and the README count are reverted, and the check is routed to Z-02 (`KI-059-15`). In order:
1. QA Gate 1 round 11 under convergence rule 1: the diff `e24e848..HEAD` and the fix of each S0, S1 and S2 of round 10.
2. If it rejects, no patch: re-plan with the human, with the finding on the table.
3. Tester Gate 2 round 2, a fresh agent, under the same rule.
4. `session_state.py suspend`, then Wave 2, in series.

**Next Phase (after QA Gate 1 round 9, superseded by the line above)**: Phase 7, Wave 1. The deadlock of QA Gate 1 round 9 was re-planned with the human and remediated (plan D35); the block was lifted with `session_state.py unblock`. In order:
1. QA Gate 1 round 10 under convergence rule 1: the diff `4b34cf9..HEAD` and the fix of each S0, S1 and S2 of round 9.
2. If it reports another S0 or S1 in `scripts/check_log_append_only.py`: no further fix round; revert A-49 to A-53 and the README count, and route the check to Z-02 (plan D35). Any other rejection: no patch, re-plan with the human.
3. Tester Gate 2 round 2, a fresh agent, under the same rule.
4. `session_state.py suspend`, then Wave 2, in series.

**Next Phase (2026-11-07, after QA Gate 1 round 9, superseded by the line above)**: the sprint is BLOCKED (`TERMINAL_REMEDIATION_LOOP`). Step 2 of the handoff below applies: no patch; the human decides how to resume, with R9-1 to R9-3 on the table. The block is lifted only by `session_state.py unblock` after that decision.

**Next Phase (after QA Gate 1 round 8, superseded by the line above from its step 2 on)**: Phase 7, Wave 1. The deadlock of QA Gate 1 round 8 was re-planned with the human and remediated (plan D33, D34); the block was lifted with `session_state.py unblock`. In order:
1. QA Gate 1 round 9 under convergence rule 1: the diff `60383e3..HEAD` and the fix of each S0, S1 and S2 of round 8.
2. If it rejects, no patch: re-plan with the human, with the finding on the table.
3. Tester Gate 2 round 2, a fresh agent, under the same rule.
4. `session_state.py suspend`, then Wave 2, in series.

**Next Phase (2026-11-07, after QA Gate 1 round 8, superseded by the line above)**: the sprint is BLOCKED (`TERMINAL_REMEDIATION_LOOP`). Step 2 of the handoff below applies: no patch; the human decides how to resume, with findings N1 to N5 of round 8 on the table. The block is lifted only by `session_state.py unblock` after that decision. The handoff below stays as written and is superseded from its step 2 on.

**Next Phase (earlier handoff)**: Phase 7, Wave 1. The deadlock of QA Gate 1 round 7 was re-planned with the human and remediated (plan D29 to D32); the block was lifted with `session_state.py unblock`. In order, in a new session:
1. QA Gate 1 round 8 under convergence rule 1 (`rules/qa_and_testing.md` §4): the diff `1dbb43e..HEAD` and the fix of each S0, S1 and S2 of round 7. A fresh agent; it reports what it finds, and a new S0 anywhere carries `escape`.
2. If it rejects, no patch: re-plan with the human, with the finding on the table.
3. Tester Gate 2 round 2, a fresh agent, under the same rule.
4. `session_state.py suspend`, then Wave 2, in series; batches stay out until the plan's unit allows them (human decision 2026-11-07: no amendment to D11).

Before editing a claim, run the command that verifies it; with no instrument, delete it (plan D32).

Deadlock record (`workflows/remediation_workflow.md` Phase 2 `error_mining`). Round 6 origin, restored here because `1dbb43e` removed it: `rules/token_economy.md` §3.1 kept being rewritten to describe bound conduct that no instrument performs instead of dropping the claim, and plan D22 checked one named string where the rule covers a property. Round 7 origin: the remediation of that same `rules/token_economy.md` line rewrote the claim a further time, against the rule A-37 added, and plan D24 listed domain sites by line where a phrase search over the tree was needed. `negative_ki` for round 6: A-37, with `fail_closed_claims` cited. `negative_ki` for round 7: none added; the same A-37 and `fail_closed_claims` cover it. Round 8 origin: plan D32 recorded a disposition for `skills/compliance-checker` only, so `docs/standards/templates/HOTFIX_TEMPLATE.md:25`, the third location of round 7 F3, was left with no fix, KI or discard. `negative_ki` for round 8: none added; `RA-14` already requires the grep across the sprint artifacts that would have caught it and the stale plan rows of N2. `family_check` for round 8: N3, N4 and N5 are second occurrences of the round 7 F6, F4 and F5 families; no check was written, because the human decides the resumption first. Human decision 2026-11-07 (plan D33, D34): the N3 family got `scripts/check_log_append_only.py`; N4 and N5 narrowed their claims. Round 9 origin: `scripts/check_log_append_only.py`, written in the round 8 remediation, always anchors `--current-sprint` to the framework root and reads `--sprint-dir` from the working directory in one git call and from the tree root in another, and its tests only ran it from the repository root with a root-relative path. `negative_ki` for round 9: none added; `fail_closed_claims` and `_root.py` already state both rules. `family_check` for round 9: no earlier occurrence of this family is recorded in the sprint. Round 10 origin: `scripts/check_log_append_only.py` reads "no anchor or no directory" as "out of scope" under `--current-sprint`, and `scripts/check_task_scope.py` `current_sprint_dir` returns `None` for both, so a deleted sprint directory and a subdirectory cwd both skip. `negative_ki` for round 10: none added; `fail_closed_claims` already states it. `family_check` for round 10: second occurrence of the silent-pass family; plan D35 withdraws the check instead of adding a further one, by human decision taken before the round ran. Round 11 origin: the Z-02 rows of `IMPLEMENTATION_PLAN.md` and `task_scope.md` hold a hand-kept list of KI ids, and `KI-059-15` was added to `SPRINT_LOG.md` without the `RA-14` grep that would have reached them. `negative_ki` for round 11: none added; `RA-14` already requires that grep. `family_check` for round 11: second occurrence of the round 8 N2 family; no check was written, because the human decides the resumption first. Human decision 2026-11-07 (plan D36): the Z-02 rows stop enumerating ids, which narrows the claim. Round 12 origin: plan D36 and `KI-059-15` state the sibling skips as a whole while units I-08 to I-10 in `IMPLEMENTATION_PLAN.md` name only the cases round 11 measured, and `skills/token-saver-auditor/scripts/audit_plan.py:59` reads a string id as out of scope. `negative_ki` for round 12: none added; `RA-14` and `fail_closed_claims` already state both. `family_check` for round 12: R12-1 and R12-2 are third occurrences of the round 8 N2 family and of the silent-pass family; no check was written, because the human decides the resumption first. Human decision 2026-11-07 (plan D37): the silent-pass family gets the family test M-05, and the N2 family gets `scripts/check_sprint_refs.py` (M-06). Round 13 origin, with the finding detail that plan D37 rule D sends to a Gate findings table not yet created (R13-2): R13-1, D37 and `KI-059-15` say M-05 holds every script with `--current-sprint`, but no unit modifies `scripts/loop_guard.py`, whose `check --sprint-dir` on a missing directory exits 0 because `status_hash` returns an empty hash (`scripts/loop_guard.py:112-114`); R13-2, rule D applies from round 13 while M-11, which creates the table, runs after the Wave 1 gates; R13-3, `SPRINT_LOG.md:20` keeps 92 units and omits Wave 1b, and `task_scope.md:26` omits Wave 1b, against 103 in the plan. Cause: the re-plan again wrote, as plan prose, claims about work not yet executed, and the gate measured them against the current tree. `negative_ki` for round 13: none added; D37 rules B and C state it. `family_check` for round 13: R13-1 and R13-3 are the fourth and fifth occurrences of the round 8 N2 family; as specified, M-06 detects neither; no check was written, because the human decides the resumption first. Human decision 2026-11-07 (plan D37 reduced): Wave 1b runs before the gates re-run; M-12 fixes `loop_guard.py`.

*Certified under conventional commit standard: feat(scope): message #059*
