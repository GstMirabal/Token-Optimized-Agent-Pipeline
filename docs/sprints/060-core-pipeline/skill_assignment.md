# Skill Assignment — Sprint 060 (github-broker-and-059-residue)

Source: `docs/sprints/060-core-pipeline/IMPLEMENTATION_PLAN.md`.
Phase 4.2 of `workflows/pipeline_workflow.md`. Drafted from this template.

Mode: **claude-code**, `delegation_mode: native`.

After writing this file, run:
`python3 scripts/check_forge_ladder.py --sprint-dir docs/sprints/060-core-pipeline`
(exit `2` rejects an empty forge destination or submodule contamination).

---

## 1. Priority ladder (record every rung)

`rules/skills_and_integrations.md §1`:

The plan has 106 Work rows. Under D17 the ladder is opened per candidate, not per
unit: a unit can be served by the standard library or an edit (so P1 always
resolves it) and still belong to a recurring capability worth packaging. Section 2
resolves the 106 units; `## Candidates` decides the 8 candidates with
criteria (a) and (b) of D17, and records the ladder trail of each.

Result for the 106 units: P1 resolves every unit with a tool already present in
`skills/`, the Python standard library, `git`/`make`/`openssl`/`ssh-keygen`/
`venv_skillopt/bin/python`, or an edit of an existing file. The plan's Dependencies
table adds no package. Result for the 8 candidates: P1 resolves 6 (`none`, nearest skill named in Reason); 2 go
through P1, P2 and P3 with no match and wait for the O-09 A/B evidence (`forge-pending-O-09`).

| Rung | Source | Result | Evidence |
| :--- | :--- | :--- | :--- |
| P1 | `skills/manifest_skills.json` | hit for 106 of 106 units (section 2) and 6 of 8 candidates; partial or no match for C1 and C2 | `skills/manifest_skills.json` lists `python-quality-auditor`, `env-shielding-auditor`, `omni-context-minimizer`, `compliance-checker`, `token-saver-auditor`, `graphify`; the five script-bearing skills have their script on disk (`graphify` is a knowledge skill without `scripts/`); `grep -rli sandbox skills/*/SKILL.md` returns 0 files; the `graphify` skill queries by natural-language question, not by symbol with edge direction |
| P2 | `autoskills-3rd` | reached for C1 and C2 by reading only; no match | `skills/autoskills-3rd/SKILL.md` and `package.json`: a stack scanner that writes a discovery file; `node_modules/` is absent, so running it needs `pnpm install` (section 4); its description names no graph-query or sandbox-measurement capability |
| P3 | `https://skills.sh/` (WebSearch/WebFetch; simulated JSON allowed in tests) | reached for C1 and C2; WebSearch/WebFetch denied by `permissions.deny`, `curl` refused by the network allowlist, no result | `## Candidates`, "P3 search log" |
| P4 | Three-File Standard at Destination | not reached | no candidate has passed the O-09 A/B; nothing was built this task |

**When this sprint builds a new skill**, the third rung's outcome MUST be recorded
as a machine-readable trail — a JSON object carrying `source`, `query` and a
boolean `hit`, shaped `{"source": "skills.sh", "query": "<term>", "hit": <bool>}`
with `<bool>` replaced by the real value. No HTTP in `make verify`.
`scripts/check_forge_ladder.py` requires that trail beside a named skill and its
`SKILL.md` path, and exits `2` without it.

> **When this sprint builds nothing, change none of the wording above.** It is
> written the way it is on purpose. `scripts/check_forge_ladder.py` decides whether
> a build is being claimed by pattern-matching this file's prose, so a template
> that *describes* the claim in the claim's own words is read as *making* it —
> and the check then demands a skill name a blank template cannot carry.
>
> Until Sprint 041 this section's header column and its fourth row did exactly
> that, and **the template copied unedited failed the Phase 4.2 gate that consumes
> it** (`exit 2`). Two further attempts to document the repair re-broke it, by
> quoting the offending strings and by pasting a literal example trail. Hence the
> abstractions above: describe the shape, never spell out an instance.
>
> The detector is correct and is not relaxed. What changed is that the template
> stopped announcing work that had not happened.

---

## 2. Per-unit tool resolution

| Unit | Skill / tool | Destination | P1–P4 trail |
| :--- | :--- | :--- | :--- |
| A-01 | none | N/A | P1: no skill authors ADRs; written from the ADR template |
| A-02 | none | N/A | P1: written from `BLUEPRINT_TEMPLATE.md` |
| A-03 | `python-quality-auditor`, `env-shielding-auditor` | N/A | P1 hit: `python_quality_auditor.py` on the new script; `env_shielding_auditor.py` confirms no key material lands in the repo |
| A-04 | `python-quality-auditor`, `env-shielding-auditor` | N/A | P1 hit: same pair as A-03 |
| A-05 | `env-shielding-auditor` | N/A | P1 hit: `env_shielding_auditor.py` after the `denyRead` and `permissions.deny` edit; candidate C6 |
| A-06 | none | N/A | P1: public key supplied by the human; no tool needed |
| A-07 | `omni-context-minimizer`, `python-quality-auditor` | N/A | P1 hit: skeleton before any partial read of the existing script (>200 lines rule); quality audit after |
| A-08 | none | N/A | P1: unit closed without change (`d700a2e`, human decision 2026-11-22); `scripts/install.py` has no tag-resolving path, so there is no edit and no skill runs (RV-70) |
| A-09 | none | N/A | P1: guide prose; no skill authors guides |
| A-10 | none | N/A | P1: Bash measurements M1-M5 written into the report; `devops_agent` is not the assignee (agent_assignment.md) |
| A-11 | none | N/A | P1: workflow prose edit |
| A-12 | none | N/A | P1: agent profile prose edit |
| A-13 | none | N/A | P1: rule prose edit |
| A-14 | none | N/A | P1: workflow prose edit |
| A-15 | none | N/A | P1: measurement M5 is recorded by hand from the GitHub IDs of each deploy operation; no skill applies |
| B-01 | `omni-context-minimizer`, `python-quality-auditor` | N/A | P1 hit: skeleton before partial read; quality audit on the fix |
| B-02 | none | N/A | P1: JSON edit with values from `token_economy_agent` |
| K-01 | `graphify` | N/A | P1 hit: `rules/graphify.md` method to confirm the `graph_update.py` workaround still holds on 0.9.x; the pin itself is `pip` under `--require-hashes`, no skill |
| N-01 | none | N/A | P1: ADR prose from `ADR_TEMPLATE.md`; candidate C8 |
| N-02 | `env-shielding-auditor` | N/A | P1 hit: `env_shielding_auditor.py` after the `allowRead` edit; the `{{PROJECT_TRANSCRIPT_DIR}}` marker carries no host path (`RA-15`); candidate C6 |
| N-03 | `python-quality-auditor`, `omni-context-minimizer`, `env-shielding-auditor` | N/A | P1 hit: skeleton before partial read of `install.py` (>200 lines); quality audit on the change and `tests/test_install.py`; `env_shielding_auditor.py` confirms the rendered path lands only in the host's settings; candidate C5 |
| N-04 | none | N/A | P1: exit-code-only probes by Bash from the sandbox after the human applies `install.py` (the agent runs `session_cost.py` and `prompt_count.py` itself, D16); candidate C2 is `forge-pending-O-09`, so no skill exists to call yet |
| M-01 | `python-quality-auditor`, `graphify` | N/A | P1 hit: quality audit on the battery and its test; `rules/graphify.md` for the `graph.json` edge schema the battery compares with the stdlib `ast` ground truth |
| M-02 | `graphify` | N/A | P1 hit: `rules/graphify.md` rebuild method for the 0.8.30 and post-K-01 baselines; counts by `wc -c`, timing by `time`, battery from M-01 |
| M-03 | `python-quality-auditor`, `graphify` | N/A | P1 hit: quality audit on the query script and its test; `rules/graphify.md` for the node and edge schema |
| M-04 | `python-quality-auditor`, `env-shielding-auditor`, `graphify` | N/A | P1 hit: quality audit on the stdio server; `env_shielding_auditor.py` confirms no credential or host term lands in the repo and the user-scope install stays outside writable trees (D2); `rules/graphify.md` for the tool surface |
| M-05 | `env-shielding-auditor` | N/A | P1 hit: `env_shielding_auditor.py` after the project-scope MCP entry is removed; JSON edit otherwise |
| M-06 | `graphify`, `compliance-checker` | N/A | P1 hit: `rules/graphify.md` is the file edited, so its own method is the content source; `compliance-checker` scans the normative text |
| M-07 | none | N/A | P1: agent profile prose edit; protocol text comes from M-06 |
| M-08 | none | N/A | P1: agent profile prose edit |
| M-09 | none | N/A | P1: agent profile prose edit |
| M-10 | none | N/A | P1: agent profile prose edit |
| M-11 | none | N/A | P1: agent profile prose edit |
| M-12 | `compliance-checker` | N/A | P1 hit: scan of the edited normative workflow |
| M-13 | `python-quality-auditor`, `env-shielding-auditor` | N/A | P1 hit: quality audit on the hook and its test; `env_shielding_auditor.py` confirms the usage log stores no tool input that can carry secrets; `RA-11` exit semantics checked by hand |
| M-14 | `env-shielding-auditor` | N/A | P1 hit: same check as A-05 after the hook registration edit; candidate C6 |
| M-15 | `python-quality-auditor` | N/A | P1 hit: quality audit on the checker and its test |
| M-16 | none | N/A | P1: the A/B is run by the agent with `scripts/session_cost.py` under the sandbox after N-04 (D16, RV-24); `token-saver-auditor` classifies prompts, it does not measure sessions |
| M-17 | `compliance-checker` | N/A | P1 hit: scan of the edited normative workflow (`workflows/close_workflow.md`); `scripts/map_workflows.py` regenerates the step map in the same commit; candidate C7 |
| M-18 | `python-quality-auditor`, `omni-context-minimizer`, `env-shielding-auditor` | N/A | P1 hit: skeleton before partial read of `install_broker.py` (>200 lines); quality audit on the change and `tests/test_install_broker.py`; `env_shielding_auditor.py` confirms no credential or host term lands in the repo; candidate C5 |
| O-01 | none | N/A | P1: ADR prose from `ADR_TEMPLATE.md`; candidate C8 |
| O-02 | `compliance-checker` | N/A | P1 hit: scan of the edited rule text (`rules/skills_and_integrations.md` §1); candidate C7 |
| O-03 | none | N/A | P1: agent profile prose edit; candidate C7 |
| O-04 | none | N/A | P1: agent profile prose edit; P3 moves to `curl` through Bash and `WebSearch`, `WebFetch` leave `tools:` (RV-16); candidate C7 |
| O-05 | none | N/A | P1: template edit; the table shape is in D17 |
| O-06 | none | N/A | P1: template edit; the table shape is in D17 and `## Candidates` of this file is its first instance |
| O-07 | `python-quality-auditor`, `omni-context-minimizer` | N/A | P1 hit: skeleton before partial read of `check_forge_ladder.py` (>200 lines); quality audit on the change and its test; candidate C5 |
| O-08 | `python-quality-auditor`, `env-shielding-auditor` | N/A | P1 hit: new stdlib script that reads transcripts; quality audit; `env_shielding_auditor.py` confirms it prints counts and names, no message content; candidate C5 |
| O-09 | none | N/A | P1: the A/B per candidate is run by the agent with `scripts/session_cost.py` under the sandbox after N-04 (D16); `token-saver-auditor` classifies prompts and does not measure sessions; the report records evidence only, the `forge`/`reuse`/`none` decision for C1 and C2 stays in this file and `agent_assignment.md` |
| O-10 | `compliance-checker` | N/A | P1 hit: scan of the edited normative workflow; candidate C7 |
| O-11 | `env-shielding-auditor` | N/A | P1 hit: `env_shielding_auditor.py` after the JSON settings edit (`claude/settings.hooks.json`, add `skills.sh` to `sandbox.network.allowedDomains`); opens the egress for the `curl` P3 of O-04; candidate C6 |
| O-12 | none | N/A | P1: agent profile prose edit (`agents/implementer_agent.md` `write_scope`) plus the `ADR-0009` amendment in the same commit; candidate C7 |
| Q-01 | `compliance-checker` | N/A | P1 hit: scan of the edited normative workflow (`workflows/pipeline_workflow.md`, Phase 6 parallel batches without worktrees); candidate C7 |
| Q-02 | none | N/A | P1: workflow prose edit (`workflows/pipeline_workflow.md`, Phase 6 step (3): `python3 scripts/check_readme_counts.py --write` and `README.md` added to the commit of a unit that adds or removes a `scripts/*.py` or `config/*.json`). `compliance-checker` is not assigned: it has no single-file invocation (KI-060-06, routed to S-04 by human decision 2026-11-22), so it cannot scan this edit. The unit is checked by `python3 scripts/map_workflows.py --check` (regenerated step map equals the committed guide) and `make verify`; candidate C7 |
| S-01 | `compliance-checker` | N/A | P1 hit: scan of the edited sprint document; the edit narrows the `python-quality-auditor` justification row to what is measured (`ruff check`, `scripts/quality_audit.py`); a scan of a prose claim, no Python; KI-060-05 |
| S-02 | none | N/A | P1: pinned requirements file regenerated with `pip install --dry-run --ignore-installed --report` (Python 3.13 and, with `--python-version 3.12 --only-binary=:all:`, 3.12) and sha256 hashes from the venv interpreter; checked by `pip install --dry-run --require-hashes` on `requirements-quality.txt` and `requirements-core.txt` (exit `0`); no skill applies and no Python source changes |
| S-03 | `python-quality-auditor` | N/A | P1 hit, limited: `python-quality-auditor` is the unit's subject, so its output cannot witness its own repair. It proves only `ruff check` on the fix and its test (`tests/test_python_quality_auditor.py`, which gains `::test_missing_tool_exits_nonzero` in the same commit). Mypy, Bandit and Radon are proven by running `venv_skillopt/bin/python -m mypy`, `-m bandit` and `-m radon` directly, and only after S-02 installs them; until S-03 lands the skill exits 0 regardless (KI-060-05). The script is 61 lines, so no `omni-context-minimizer`; candidate C5 |
| S-04 | none | N/A | P1: measurement report written from reading every `skills/*/scripts/` import and from running each script with its dependency absent; no skill applies. Widened scope (RV-50, RV-53, RV-54; KI-060-06 routed here by human decision 2026-11-22): input is this file at the S-03 commit; for every skill assigned to a unit, with or without `scripts/`, the assigned capability is compared with its real invocations (`SKILL.md`, scripts, accepted arguments); a skill with a script is run on a fixture file of that unit and its exit is recorded, a `SKILL.md`-only skill is marked `read-only` and gets no `can execute` verdict; each finding becomes an `S-NN` re-plan row; the report carries the import to distribution alias table that S-05 reads |
| S-05 | `python-quality-auditor` | N/A | P1 hit: new stdlib script with a paired test, audited after S-03 lands; its `README.md` counted block is regenerated by the Phase 6 step that Q-02 adds (no skill); the skill proves `ruff check` only until S-02 installs Mypy, Bandit and Radon in `venv_skillopt` and S-03 makes the skill run them (KI-060-05); candidate C5 |
| T-01 | none | N/A | P1: Bash measurements written into `DB_ROUTE_MEASUREMENT.md` (exit code of a query to the disposable database, exit code of an attempt on the development database, enumeration of the out-of-sandbox entry points per route, `RA-19`); the Docker and `.env` steps are prepared as commands for the human and the pasted output is recorded (`RA-09`). `env-shielding-auditor` is not assigned: its `SKILL.md` and `scripts/env_shielding_auditor.py` do not mention the sandbox and `SCANNED_SUFFIXES` omits `.md`, so it can neither measure a route nor scan the report. `make sandbox-probe` (`scripts/sandbox_probe.py`, no `SKILL.md`) re-measures only M7, M9-1..M9-4, A1 and B2-1 against closed cases; it executes none of T-01's routes (A1-b, A2-1, A2-d unlink and re-bind, F-18, the no-network container by socket), so it may run before and after as a control, not as the measurement. Candidate C2 (`forge-pending-O-09`, with the agent form named in O-09): no skill exists to call yet; after H-01 |
| T-02 | none | N/A | P1: ADR prose from `ADR_TEMPLATE.md` (`docs/decisions/ADR-0029-local-database-route.md`) plus the one-line `ADR-0019` edit (`Superseded by ADR-0029` in D4 on branch 1, `Amended by ADR-0029` on branch 2); the `KI-057-1` roadmap row is updated by Z-06 (RV-62), so T-02 has no roadmap companion; no skill authors ADRs. `compliance-checker` is not assigned: it has no single-file invocation (KI-060-06, routed to S-04 by human decision 2026-11-22), so it cannot scan this ADR; candidate C8 |
| T-03 | none | N/A | P1: rule prose edit (`rules/qa_and_testing.md` §7 `local_testing`); text comes from T-02. `compliance-checker` is not assigned: it has no single-file invocation (KI-060-06, routed to S-04 by human decision 2026-11-22), so it cannot scan this edit. Checked by `make verify`; candidate C7 |
| T-04 | none | N/A | P1: agent profile prose edit (`agents/tester_agent.md` line 18, which repeats `local_testing`, reflects what T-03 writes in `rules/qa_and_testing.md` §7; RV-60). `compliance-checker` is not assigned: it has no single-file invocation (KI-060-06, routed to S-04 by human decision 2026-11-22), so it cannot scan this edit. Checked by `make verify`; candidate C7 |
| U-01 | none | N/A | P1: deletion of `scripts/publish_github_release.py` and `tests/test_publish_github_release.py`, no new code, so `python-quality-auditor` has nothing to audit and `omni-context-minimizer` nothing to read. Checked by `git grep -n 'publish_github_release' -- workflows scripts tests config rules Makefile` (no output) and `make verify` exit `0`; after A-11 |
| U-02 | none | N/A | P1: deletion of `scripts/ci_gate.py` and `tests/test_ci_gate.py`, no new code, so `python-quality-auditor` has nothing to audit and `omni-context-minimizer` nothing to read. Checked by `git grep -n 'ci_gate' -- workflows scripts tests config rules Makefile` (no output) and `make verify` exit `0`; after A-11 |
| U-03 | none | N/A | P1: rule prose edit (`rules/project_topology.md` §4, delete the `scripts/ci_gate.py` row; before H-02). `compliance-checker` is not assigned: it has no single-file invocation (KI-060-06, routed to S-04 by human decision 2026-11-22), so it cannot scan this edit. Checked by `grep -c 'ci_gate' rules/project_topology.md` = `0` and `make verify`; candidate C7 |
| U-04 | none | N/A | P1: ADR status-line edit (`docs/decisions/ADR-0014-ci-gate-record-on-uninspectable-protection.md`, `**Status**` becomes `Superseded by ADR-0025`; body unchanged); no skill edits ADRs. Checked by `grep -n 'Superseded by ADR-0025'` on that file returning the `**Status**` line and `make verify` |
| O-13 | none | N/A | P1: prose edit of `agent_assignment.md` (final forge/none decision per agent candidate from O-09 evidence, reconciled with `skill_assignment.md` on `claude/settings.hooks.json`); no skill applies |
| O-14 | none | N/A | P1: prose edit of `skill_assignment.md` (final forge/none decision per candidate from O-09 evidence; C6 reconciled with the agent candidate for the same file, RV-37, RV-39); no skill applies |
| L-01 | `python-quality-auditor`, `env-shielding-auditor` | N/A | P1 hit: new stdlib script with network I/O and a paired test |
| L-02 | none | N/A | YAML job edit; no skill applies |
| L-03 | `python-quality-auditor`, `omni-context-minimizer` | N/A | P1 hit: modify a large script (`session_start.py`) with a paired test |
| L-04 | `env-shielding-auditor` | N/A | P1 hit: sandbox egress change; candidate C6 |
| L-05 | none | N/A | ADR prose from `ADR_TEMPLATE.md` |
| L-06 | none | N/A | conditional config file or transcription of the alert message |
| P-01 | `python-quality-auditor` | N/A | P1 hit: quality audit on the fix to `scripts/check_task_scope.py` and `tests/test_check_task_scope.py`; candidate C5 |
| C-01 | none | N/A | P1: workflow prose edit |
| D-01 | `python-quality-auditor`, `env-shielding-auditor` | N/A | P1 hit: quality audit; the scanner handles only hashes, `env_shielding_auditor.py` confirms no plaintext term enters the repo |
| D-02 | none | N/A | P1: JSON supplied by the human (hashes) |
| D-03 | `python-quality-auditor` | N/A | P1 hit: quality audit on the modified test |
| D-04 | none | N/A | P1: runs `scripts/check_host_terms.py` (D-01) over `origin/main`; no skill |
| D-05 | none | N/A | P1: Makefile edit; `make verify` is the check, no skill applies |
| E-01 | `omni-context-minimizer`, `python-quality-auditor` | N/A | P1 hit: skeleton before partial read; quality audit on the change |
| F-01 | `compliance-checker` | N/A | P1 hit: `compliance-checker` scans the trimmed `agents.md` for rule violations; byte count by `wc -c` |
| F-02 | `compliance-checker` | N/A | P1 hit: same scan on `rules/skills_and_integrations.md` |
| G-01 | `python-quality-auditor` | N/A | P1 hit: quality audit on the fix |
| G-02 | `python-quality-auditor` | N/A | P1 hit: quality audit on the fix |
| H-01 | none | N/A | P1: Bash matrices of 055 and 056 written into the report |
| H-02 | none | N/A | P1: rule prose edit |
| I-01 | none | N/A | P1: `git mv` to `GLOBAL_TOPOLOGY_MAP.md` plus a grep of the old path (RA-14); no skill renames files |
| I-02 | none | N/A | P1: `git mv` to `TOPOLOGY_MAP.md` plus a grep of the old path (RA-14); no skill renames files |
| I-03 | none | N/A | P1: `git mv` to `DOC_ORCHESTRATOR_CONTRACT.md` plus a grep of the old path (RA-14); no skill renames files |
| I-04 | none | N/A | P1: `git mv` to `TOPOLOGY_MAPPER_CONTRACT.md` plus a grep of the old path (RA-14); no skill renames files |
| I-05 | none | N/A | P1: `git mv` to `TOPOLOGY_SCAFFOLDER_CONTRACT.md` plus a grep of the old path (RA-14); no skill renames files |
| I-06 | none | N/A | P1: `git mv` to `TOKEN_ECONOMY_DOCUMENTATION_STANDARD_AUDIT.md` plus a grep of the old path (RA-14); no skill renames files |
| I-07 | none | N/A | P1: `git mv` to `SKILLOPT_TRANSITIVE_CLOSURE_AUDIT.md` plus a grep of the old path (RA-14); no skill renames files |
| I-08 | none | N/A | P1: `git mv` to `THIRD_PARTY_PROVENANCE_REGISTER.md` plus a grep of the old path (RA-14); no skill renames files |
| I-09 | none | N/A | P1: `git mv` to `AUTONOMY_POSTURE_PLAN.md` plus a grep of the old path (RA-14); no skill renames files |
| J-01 | `token-saver-auditor` | N/A | P1 hit: its rejection filters classify the measured findings; byte and token counts by `wc -c` and `scripts/` measurement tools |
| J-02 | `compliance-checker` | N/A | P1 hit: `compliance-checker` as the scan base for prose motives in normative documents |
| Z-01 | none | N/A | P1: written from `SPRINT_LOG` template |
| Z-02 | `graphify` | N/A | P1 hit: dependency graph query for the jurisdictional scope (`graph_sovereignty`) |
| Z-03 | none | N/A | P1: already written (commit `024598e`) |
| Z-07 | none | N/A | P1: already created in Phase 4.2 before Phase 5, not re-run in Phase 6; O-14 is its only later modification |
| Z-05 | none | N/A | P1: ledger edit |
| Z-06 | none | N/A | P1: roadmap edit |

`Destination` for a forged skill: `host:.claude/skills/<name>/` (default),
`profile:<path>`, or `nucleus:PR`. Writing under `.agents/skills/` from a
host session is PROHIBITED (`strict_rule`). Every Destination here is `N/A`: no skill is created in Phase 4.2; D17 allows writing one only after the O-09 A/B.

---

## Candidates

Applies D17 from the plan text (the template gains this table in O-06).

- Criterion (a): the same operation on the same class of subject appears in 3 or
  more plan units, or in 2 or more of the previous 5 sprints (`055`..`059`).
- Criterion (b): the unit's subject is governed by a `rules/` file that no assigned
  skill or profile covers.
- Decision: `reuse:<skill>` or `forge-pending-O-09`. A skill is written only if its
  O-09 A/B measures at least 30 % fewer `fresh` tokens (D14 threshold) on its units.

The final decision per candidate is written by unit O-14 from the O-09 evidence; there C6 (`claude/settings.hooks.json`) is reconciled with the agent candidate for the same file in `agent_assignment.md` (O-13), so both files carry one decision (RV-37, RV-39). Decisions below are provisional until O-14.

Notation: `P` = `docs/sprints/060-core-pipeline/IMPLEMENTATION_PLAN.md`; `E` =
`grep -E '^\| [A-Z]-[0-9]{2} \|' P` (106 lines, `grep -c` reproduces it); `Q<n>` =
the same plan file of sprint `05<n>-core-pipeline`.

| Candidate | Units | Criterion (a/b) | Evidence | Decision | Reason |
| :--- | :--- | :--- | :--- | :--- | :--- |
| C1 structural graph query (symbol or file to callers, callees, dependents, impact) | M-03, M-04 (build); M-07, M-08, M-09, M-10, M-11 (consume) | a: yes; b: no | `E \| grep -cE 'graph_query\|graph_mcp\|dependents\|callers\|impact'` = 9 units (M-01, M-03, M-04, M-07..M-11, M-18); `grep -ciE '^\| .*graph'` on Q5..Q9 = 28, 4, 0, 7, 9 (4 of 5 sprints); `rules/graphify.md` is covered by `graphify`, so (b) fails | forge-pending-O-09 | The same operation on the same subject class recurs in 5 consumer units and in 4 of 5 earlier sprints. `graphify` answers natural-language questions and M-06 prohibits that mode; no skill wraps the M-03/M-04 interface. Value is unproven until M-03 exists: O-09 runs the A/B on M-07..M-11 |
| C2 sandbox boundary measurement (exit-code-only probes, no content printed) | A-10, A-15, H-01, N-04, T-01 | a: yes; b: yes | `E \| grep -c 'MEASUREMENT'` = 6 (A-10, A-15, N-04, M-16, H-01, T-01; M-16 is an A/B, not a probe, so 5 units); `ls docs/sprints/05[5-9]-core-pipeline \| grep -c SANDBOX` = 4 (055, 056, 057, 059); `grep -rli sandbox skills/*/SKILL.md` = 0 files; `rules/project_topology.md §5` and `RA-19` govern the subject | forge-pending-O-09 | Both criteria hold: 5 units here and 4 of 5 earlier sprints, and no assigned skill covers the sandbox rule. `scripts/sandbox_probe.py` is a script with no `SKILL.md`, so agents do not find it through the manifest. The plan also names an agent form of this candidate; that decision belongs to `agent_assignment.md` |
| C3 rename plus old-path grep sweep (`RA-06`, `RA-14`) | I-01..I-09 | a: yes; b: no | `E \| grep -c 'git mv'` = 9 (I-01..I-09); `grep -E '^\| ' Q5..Q9 \| grep -ciE 'git mv\|rename'` = 0 in all five; `grep -ciE 'rename\|git mv' skills/manifest_skills.json` = 0; no `rules/` file governs it (`RA-06` and `RA-14` are in `agents.md`) | none | No skill packages this work; gap evaluated by O-09 under D17. Unit count meets (a) but the batch is one pair of commands (`git mv`, then a grep of the old path with 0 hits) and appeared in 0 of the 5 earlier sprints: not recurring. `compliance-checker` scans the `RA-06` names after the batch. If renames recur, `check_sprint_refs.py` is the nearest script to extend |
| C4 OSV advisory check of pins | L-01 (script); L-04, L-05 (settings, ADR) | a: no; b: no | `E \| grep -ciE 'osv\|advisor'` = 3 units, with 3 different operations (create script, edit settings, write ADR); the check itself is 1 unit; `grep -rliE 'osv\|advisor' skills/*/SKILL.md` = 0 files; L-01 subject is a Python script under `rules/code_craft.md`, covered by `python-quality-auditor` | none | No skill packages this work; gap evaluated by O-09 under D17. One script in one unit does not meet (a); the settings and ADR rows belong to C6 and C8. Nothing recurs, so nothing to package. `python-quality-auditor` is the nearest skill and audits the L-01 script; no OSV capability is missing from it that a skill could supply |
| C5 stdlib script plus paired test | A-03, A-04, A-07, B-01, N-03, M-01, M-03, M-04, M-13, M-15, M-18, O-07, O-08, L-01, L-03, D-01, E-01, P-01, G-01, G-02, S-03, S-05 | a: yes; b: no | `E \| grep -E '\| `(scripts\|hooks)/[a-z_]+\.py`' \| grep -cvE '\| (close\|delete) '` = 21 units (the pattern also matches A-08, closed without change, and U-01, U-02, deletions, which are excluded; S-03 edits `skills/python-quality-auditor/scripts/python_quality_auditor.py`, outside that pattern, so the candidate lists 22); `grep -cE '^\| [^\|]+\| `(scripts\|hooks)/[a-z_]+\.py`'` on Q5..Q9 = 9, 11, 22, 18, 57 (5 of 5 sprints); `rules/code_craft.md` is covered by `python-quality-auditor` | none | No skill packages this work; gap evaluated by O-09 under D17. Highest recurrence in the plan, and `python-quality-auditor` (nearest skill) is already assigned to all 22 units (section 2; for S-03 limited to `ruff check`, see its row) and `omni-context-minimizer` to the 7 that edit an existing script above 200 lines. A new skill would add no capability |
| C6 sandbox settings edit (`claude/settings.hooks.json`) | A-05, N-02, L-04, O-11, M-14 | a: yes; b: no | `E \| grep -c 'settings.hooks.json'` = 6 lines (the 5 units plus O-04, which names the file but edits `agents/skill_architect.md`); `grep -cE '^\| [^\|]+\| `claude/settings'` on Q5..Q9 = 3, 1, 1, 1, 4 (5 of 5 sprints); `env-shielding-auditor` covers the secret and deny-list part of `rules/project_topology.md §5` | none | No skill packages this work; gap evaluated by O-09 under D17. Recurs in every sprint and in 5 units here, but the edit text is fixed by each plan row. `env-shielding-auditor` is the nearest skill and already scans the result; the boundary measurement after the edit is C2, not this candidate |
| C7 normative prose edit (`agents/`, `workflows/`, `rules/`) | A-11, A-12, A-13, A-14, C-01, F-02, H-02, M-06..M-12, M-17, O-02, O-03, O-04, O-10, O-12, Q-01, Q-02, T-03, T-04, U-03 | a: yes; b: no | `E \| grep -cE '\| `(agents\|workflows\|rules)/'` = 25 (10 agents + 8 workflows + 7 rules); on Q5..Q9: agents rows 1, 1, 0, 1, 4 (T-04 adds the tenth `agents/` row here) and workflows rows 3, 4, 6, 7, 11 | none | No skill packages this work; gap evaluated by O-09 under D17. The text of each edit is fixed by its plan row; the only deterministic part is the rule-violation scan, which `compliance-checker` already performs. A skill would add no capability |
| C8 ADR and document authoring from a template | A-01, A-02, N-01, O-01, L-05, T-02 | a: yes; b: no | `E \| grep -c 'docs/decisions/ADR'` = 6 (A-01, N-01, O-01, L-05, T-02 and U-04, a status-line edit that authors no ADR) plus A-02 from `BLUEPRINT_TEMPLATE.md`; ADR rows on Q9 = 8, on Q6 = 0; `rules/documentation_standard.md` is covered by the `doc_orchestrator` profile, so (b) fails | none | No skill packages this work; gap evaluated by O-09 under D17. The templates under `docs/standards/templates/` and the `doc_orchestrator` profile are the capability; `compliance-checker` scans the result. A skill would duplicate the templates |

### Ladder trail per candidate

| Candidate | P1 manifest | P2 `autoskills-3rd` | P3 `skills.sh` | P4 |
| :--- | :--- | :--- | :--- | :--- |
| C1 | `graphify` found, partial: natural-language query only, no symbol or edge-direction query | read `SKILL.md` and `package.json`: stack scanner, no graph-query capability; not run | network refused (log below) | pending O-09 |
| C2 | no skill: 0 files mention `sandbox` | same read: no sandbox-measurement capability; not run | network refused (log below) | pending O-09 |
| C3 | `compliance-checker` found (naming scan only) | not needed | not needed | not reached |
| C4 | `python-quality-auditor` found (nearest; decision `none`) | not needed | not needed | not reached |
| C5 | `python-quality-auditor`, `omni-context-minimizer` found (nearest; decision `none`) | not needed | not needed | not reached |
| C6 | `env-shielding-auditor` found (nearest; decision `none`) | not needed | not needed | not reached |
| C7 | `compliance-checker` found | not needed | not needed | not reached |
| C8 | `compliance-checker` found; templates on disk | not needed | not needed | not reached |

### P3 search log

WebSearch and WebFetch are denied by `permissions.deny` in `claude/settings.hooks.json`, not merely unexposed (RV-16). Unit O-04 moves P3 to `curl` through Bash; unit O-11 opens the egress by adding `skills.sh` to `sandbox.network.allowedDomains`. The fallback used here was `curl` through
Bash against `https://skills.sh/` with generic terms only (no project or host term):
`graph query`, `sandbox measurement`, `rename references`, `dependency advisory osv`.
Every request returned the same refusal, verbatim:

- `curl: (56) CONNECT tunnel failed, response 403`
- `deny network-outbound skills.sh:443 (host is not on the allow list)`

No result came back for any term, so P3 is recorded as unresolved, not as a
confirmed absence. For C1 and C2, the human or O-09 may repeat the search from a
session whose allowlist covers `skills.sh`; plan unit O-11 adds `skills.sh` to `sandbox.network.allowedDomains` as the remediation of the refused connection; `forge-pending-O-09` holds either way
because the A/B evidence, not the search, decides whether a skill is written.

---

## 3. Skills used

| Skill | Why |
| :--- | :--- |
| `python-quality-auditor` | A-03, A-04, A-07, B-01, L-01, L-03, D-01, D-03, E-01, G-01, G-02, M-01, M-03, M-04, M-13, M-15, M-18, N-03, O-07, O-08, P-01, S-03, S-05: what the skill proves today is `ruff check` only (`agents.md §1 linter_command`; the pinned `ruff==0.16.3` in `requirements-quality.txt`); `scripts/quality_audit.py`, run by `make verify`, proves `max_indentation` and `max_lines_per_func`. Mypy, Bandit and Radon are absent from `venv_skillopt` (`venv_skillopt/bin/python -c "import mypy"` raises `ModuleNotFoundError`, likewise `bandit` and `radon`) and the skill exits `0` regardless (KI-060-05), so A-03 (`172c145`) is inconclusive on Mypy, Bandit and Radon. S-03 is limited to `ruff check` because it repairs the skill. S-05 is the first unit where the skill is a real gate, after S-02 installs the tools and S-03 lands. |
| `env-shielding-auditor` | A-03, A-04, A-05, L-01, L-04, D-01, M-04, M-05, M-13, M-14, M-18, N-02, N-03, O-08, O-11: the broker, its installer, the deny settings, the hash scanner, the graph MCP server, the usage hook, the transcript-read setting and the capability-usage script handle credentials, host names or tool input; the scan proves nothing sensitive is committed (`RA-09`, `RA-15`). |
| `omni-context-minimizer` | A-07, B-01, L-03, E-01, M-18, N-03, O-07: existing scripts above 200 lines get a skeleton before any partial read (`agents.md §2 ast_skeleton`). |
| `compliance-checker` | F-01, F-02, J-02, M-06, M-12, M-17, O-02, O-10, Q-01, S-01: normative text edits and the prose-motive audit need a rule-violation scan. |
| `token-saver-auditor` | J-01: its rejection filters are the classification basis for prompt-audit findings. The plan itself was already audited at Phase 3. |
| `graphify` | K-01, Z-02, M-01, M-02, M-03, M-04, M-06: graph workaround check on the new `graphifyy`, the dependency graph behind `task_scope.md`, and the `rules/graphify.md` schema and method that Wave M (D14) turns into the battery, the query interface, the MCP server and the structural-first protocol. |

## 4. Skills considered and rejected

| Candidate | Why rejected |
| :--- | :--- |
| `mcp-registry` | A-03 and M-04 are MCP servers, but D2 forbids registering it in `claude/mcp.json` or `.mcp.json`; the registry protocol would route it into agent-writable files. Registration is the human's `claude mcp add --scope user` step; M-05 removes the project-scope `graphify` entry rather than adding one. |
| `autoskills-3rd` (run) | Read for C1 and C2 only: it is a stack scanner, with no graph-query or sandbox-measurement capability. Running it needs `pnpm install` (`node_modules/` is absent) and writes a discovery file for no gain. |
| `compliance-checker` for Q-02, T-02, T-03, T-04 | Its `SKILL.md` gives no single-file invocation and its scripts act on memory telemetry and `agents.md` (KI-060-06, routed to S-04 by human decision 2026-11-22); Q-02 is checked by `python3 scripts/map_workflows.py --check` and `make verify`, T-02, T-03 and T-04 by `make verify`. |
| `env-shielding-auditor` for T-01 | Neither its `SKILL.md` nor its script mentions the sandbox, and `SCANNED_SUFFIXES` omits `.md`, so it can neither run a route measurement nor scan `DB_ROUTE_MEASUREMENT.md`. `make sandbox-probe` re-measures only the closed cases M7, M9, A1 and B2 and is a control for T-01, not its measurement. |
| `skillopt` | F-01, F-02, M-06, M-12: it rewrites rule files and needs explicit human authorization per run; no authorization exists and the edits are specified by the plan. |
| `contract-writer` | A-03 has no HTTP API of its own; the operation list is in D4 and ADR-0025. M-04 is a stdio tool surface specified by D14, not an HTTP contract. |
| `token-saver-auditor` for M-16 | It classifies prompt findings; the A/B needs per-session `fresh` token counts, which only `scripts/session_cost.py` run by the agent under the sandbox after N-04 produces (D16, RV-24). |
| A graph-query skill for Wave M, decided now | Not rejected and not built: C1 in `## Candidates` is `forge-pending-O-09`. M-01, M-03 and M-04 stay scripts in `scripts/`; D14 asks for a query interface, and only the O-09 A/B can justify a skill over it. |
| A sandbox-measurement skill, decided now | Not rejected and not built: C2 is `forge-pending-O-09`, for the same reason. |
| `topology-scaffolder`, `topology-monitor` | Nucleus mode forbids scaffolding (`nucleus_neutrality`); I-01..I-09 are renames of existing files, not new topology. |
| `mass-standardizer`, `readme-standardizer`, `skill-creator` | No skill is added or changed this sprint, so the manifest is not regenerated and no README is written. |
| `sprint-architect` | The plan exists and was approved for drafting at Phase 3; Z-01 and Z-03 are already templated. |
| `django-*`, `nodejs-*`, `typescript-advanced-types`, `vercel-*`, `vite`, `tailwind-css-patterns`, `frontend-design`, `accessibility`, `seo`, `js-standardizer`, `slash-commander`, `skills-samples-3rd` | No Django, Node, frontend or slash-command surface in any Work row. |

## 5. Gaps

Two open decisions, both owned by O-09: C1 (structural graph query) and C2 (sandbox boundary measurement) are `forge-pending-O-09`. No skill was forged and nothing was written under `skills/`. The P3 search was denied (WebSearch/WebFetch by `permissions.deny`, `curl` by the network allowlist; log in `## Candidates`; O-04 and O-11 remediate), so P3 is unresolved for C1 and C2, not confirmed absent. The plan's Dependencies table adds no package.
