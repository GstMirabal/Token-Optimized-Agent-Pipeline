# Token Economy Study (Sprint 059, Unit A-00)

**Sprint**: 059
**Unit**: A-00
**Measurement date**: 2026-11-09
**Measured by**: `token_economy_agent`

## 1. Purpose and scope

| Item | Value |
| :--- | :--- |
| Decision served | D8 of `docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md`: study the token-saver instruments and the Claude Code mechanisms before touching the instruments |
| Data for | The A-06 debate and the H-01 estimate table (D14) |
| Measurement date | 2026-11-09 |
| Measured by | `token_economy_agent` |
| Source of every figure | The measurement report of `token_economy_agent`; its scripts and literal outputs are in section 8 |

Conventions that apply to every section:

| Term | Meaning |
| :--- | :--- |
| Four-field tokens (`total4`) | `input + output + cache_read + cache_creation`, the sum `KI-059-10` used |
| Fresh tokens (`fresh`) | `input + output + cache_creation`, which is the four-field sum without `cache_read` |
| Turn | A transcript record with `usage`, counted once per `message.id` |
| Piece output cost | Bytes of output. Token cost is not measured directly for the pieces in section 2, because no tokenizer was available |
| Snapshot drift | Transcript snapshots for sections 3 and 5 were taken while the live session `593ffb72` and the measuring subagent kept writing. Per-run turn counts differ by about 19 turns (5616 against 5635 in the cache script). Sprint 056-058 attribution is unaffected |

## 2. Token-saver pieces

Three of the four pieces were run inside the sandbox during the audit and all three exited 0. `scripts/session_probe.py` was not run, because it calls `gh` and stamps `docs/active_state.json`.

| Piece | Measures | Invoker | Deterministic | Sandbox | Output cost |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `skills/token-saver-auditor` (`SKILL.md`, `scripts/audit_plan.py`) | Structural filters 1-4 and 6, Mechanisms/Invoker, Cost section, Verification and Tests rows, and blast radius of a plan. The script's `collect_findings` and `audit` produce the verdict. `SKILL.md` keeps the semantic judgment for the agent. | `audit_plan.py:8` (`invoked_by:`) names `pipeline_workflow.md` Phases 1 and 5 and Makefile `verify`. `Makefile:76` runs `audit_plan.py --current-sprint` in `verify`. The `SKILL.md` loads on invocation. | The script is deterministic. The semantic half in `SKILL.md` is agent judgment. | Inside. `python3 -I skills/token-saver-auditor/scripts/audit_plan.py --current-sprint` exited 0. | 107 bytes on pass. `SKILL.md` is 2,459 bytes. |
| `skills/omni-context-minimizer` (`scripts/omni_minimizer.py`: `parse_python_ast`, `parse_heuristic`, `parse_file`) | Structural skeleton of a file (imports, classes, signatures). It measures nothing about tokens. | No hook and no Makefile target. It is a prose mandate in `workflows/pipeline_workflow.md:40` and `rules/token_economy.md:11`, so each use depends on agent judgment. `grep -c invoked_by` on the script returns 0. | Deterministic (AST for Python, regex for other languages). The decision to invoke it is judgment. | Inside. It is a read-only local file parse and exited 0. | On `scripts/session_probe.py` (757 lines, 31,238 bytes) it printed 45 lines and 2,297 bytes (7.4% of the bytes). `SKILL.md` is 2,465 bytes. |
| `scripts/session_probe.py` (`probe_cost` at line 683, `HARD_RATIO = 15` at line 51, `main`) | Six probes, one of them cost. `probe_cost` calls `session_cost.measure_previous` and reports only previous-session cycles above 15x, as advisory output. It reports no soft breach (`token_economy.md:37`). | `start_workflow.md:29` (0.6 `readiness_probe`) and `close_workflow.md:30` (3.5 `platform_recheck`, with `--force-platform`). Both are workflow steps that the agent runs. | Deterministic code. | Mixed. The `probe_cost` part only reads transcripts and runs inside. The platform probe launches `gh` (`rules/project_topology.md:42`, row `S-5c`, "derived, not re-measured"), so the human runs it under the sandbox. | Not measured, because running it would call `gh` and write `docs/active_state.json`. |
| `scripts/session_cost.py` (`read_turns`, `context_size`, `segment_cycles`, `cycle_summary`, `measure`, `measure_previous`) | Per context cycle: first-turn context, peak, ratio, and token totals per model. `read_turns` counts each `message.id` once. | `invoked_by:` in the module docstring names `session_probe.py` and `rules/token_economy.md#session_bound`. The `--from-anchor` form is for the plan Cost section (`token_economy.md:43`). Manual use is by the agent or a human. | Deterministic. | Inside. It reads `~/.claude/projects/...` and ran in this sandbox. | `--json` printed 741 bytes for a one-cycle session; the text form printed 456 bytes. |

## 3. Claude Code mechanisms

The "Sandbox" column follows the sandbox text in this session. It applies to Bash commands, so harness-internal mechanisms are marked as not applicable. Hooks run outside the sandbox (`docs/sprints/056-core-pipeline/SANDBOX_ENUMERATION.md` rows E1-E7).

| Mechanism | Cost | Sandbox | Deterministic | Source |
| :--- | :--- | :--- | :--- | :--- |
| Auto-compact | Two events in all transcripts. `compact_boundary` records show `trigger: auto`, `preTokens` 325,169 to `postTokens` 18,582 (`aeda1d83`) and 237,131 to 14,433 (`351ebf72`). The cost of the summarisation call is `unverified`. | Not applicable (harness). | Summary content is model-generated. The trigger threshold is `unverified`: 5 other sessions passed 325K without a `compact_boundary` record (550,187, 418,579, 391,087, 355,707, 324,258 last-turn context). | `$TMPDIR/mech.py` output; `rules/token_economy.md §3.1` says compaction is not a cost control. |
| `/compact` (manual) | `unverified` | Not applicable | Not applicable | 0 occurrences in `<command-name>` records. Only `/agents:start` (28) and `/clear` (5) appear. |
| `/context` | `unverified` | Not applicable | Not applicable | 0 occurrences, same scan. |
| `statusLine` | `unverified` | `unverified` | `unverified` | Not present in `claude/settings.hooks.json`, `.claude/settings.json` or `.claude/settings.local.json`. User-level settings were not read. |
| `PostToolUse` hook | `unverified` | Would run outside (the same class as E1-E7) | Not applicable | Not configured in the repo (grep over `*.json`, `*.py`, `*.md` returned none). |
| `PreCompact` hook | The command is `persist_session_context.py`, which refreshes the mirror and prints the `task_scope.md` path. Output size not measured, because running it writes the mirror. | Outside (E4: `scripts/` is `denied (rule)`) | Deterministic | `claude/settings.hooks.json:104`; `scripts/persist_session_context.py` docstring. The nucleus `.claude/settings.json` has no `hooks` key, so it is host-only. No PreCompact event appears in the nucleus transcripts. |
| `Stop` hook | In the nucleus transcripts: 432 `stop_hook_summary` records, all from user-level `~/.config/iterm2/cc-status`. Median 12 ms, max 177 ms, `hasOutput` false. The repo's `state_mirror.py` is not seen running. | Outside (E3) | Deterministic | `$TMPDIR` inline scan; `claude/settings.hooks.json` (Stop entry runs `state_mirror.py`). |
| Subagents as context isolation | 270 subagent transcripts. First-turn context median 26,252 (min 15,501, max 30,327) against the main median of 60,612. Peak context median 42,133, max 175,947. Median 7.5 turns. They account for 23.1% of four-field tokens and 2,909 turns. 229 of those 2,909 (7.9%) are cold-cache turns, against 1 of 2,726 in main. | `unverified` for subagent Bash. E11 shows frontmatter `hooks:` run outside. | The decision to delegate is judgment. | `$TMPDIR/mech.py` and `cache.py` outputs. |
| Progressive loading of skills and `rules/` | Always loaded: `instructions` attachment (`CLAUDE.md` + `agents.md` + memory), median 52,505 chars. `skill_listing` is 20,311 chars (42 skills, names and descriptions only). `agent_listing_delta` is 8,610 chars. A skill body (`invoked_skills` attachment) was 1,584 chars. Median first-turn context across the 27 closed sessions is 60,612 tokens. `rules/` load is by the `agents.md §0` index, which is a convention. | Not applicable | Skill listing is deterministic. Loading `rules/` depends on agent judgment. `config/rule_triggers.json` is checked by `verify_references.py` check (e), which checks the mirror, not the loading. | Attachment-size scan (inline, section 8); `agents.md §0`. |
| Prompt caching | `cache_read` is 94.14% of all four-field tokens. Main-session cache writes carry a 1h TTL (16,611,110 tokens) and subagent writes carry a 5m TTL (19,696,172 tokens). Price ratio is `unverified`: `config/model_tiers.json:10` states prices are deliberately absent. | Not applicable | Deterministic | `$TMPDIR/cache.py` and `mech.py` outputs. |

### 3.1 What `scripts/install.py` does today with `agents:*` commands

Input for the question of whether `install.py` should install the `agents:*` commands only by opt-in (D8). The script installs all of them unconditionally.

| Fact | Value |
| :--- | :--- |
| `install_host_claude_bridge` (`scripts/install.py` lines 686-688) | Loops `sorted((AGENTS_DIR / "commands").glob("*.md"))` and calls `link_one` for each |
| Command files | 13: `audit`, `close`, `deployment`, `extract`, `graphify`, `harden`, `pipeline`, `reconcile`, `remediation`, `revdoc`, `skill-forge`, `standardization`, `start`; 3,835 bytes in total |
| `install_nucleus_bridge` (lines 445-447) | Does the same |
| Other links | Every `skills/*` directory (lines 691-693) and every `agents/*.md` |
| Flags | Only `--profile`, `--profile-path` and `--target`, so no opt-in exists |
| Effect of reinstalling | Reverts any deletion of commands |

## 4. Context growth, boot to close

**Selection rule.** Take every top-level `*.jsonl` in `~/.claude/projects/-Users-gstmirabal-Developer--agents/`. Subagent transcripts sit in subdirectories and are excluded. Exclude the live session id from `docs/active_state.json`, which is `593ffb72-167e-4a9d-b835-f884487d749d`. The result is **27 sessions**, all measurable. The 20 sessions in `KI-059-10` were counted on 2026-11-07, and 7 more have closed since.

**Command.** For each session the script runs `python3 -I scripts/session_cost.py --json --session <UID>`. It takes `first` from `cycles[0].first_turn` and `last` from the final turn via `read_turns` and `context_size`. `ratio_last` is `last` divided by `first`.

### 4.1 Per-session table

| Session | Msgs | Cycles | First | Last | last/first | Peak/first | Four-field total |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| ab327e08 | 266 | 1 | 57,964 | 550,187 | 9.49 | 9.49 | 89,017,430 |
| ea40fe66 | 128 | 1 | 58,838 | 293,225 | 4.98 | 4.98 | 22,963,329 |
| c6ce92da | 133 | 1 | 60,508 | 299,973 | 4.96 | 4.96 | 27,729,503 |
| b598c55f | 3 | 1 | 59,073 | 62,283 | 1.05 | 1.05 | 184,375 |
| 50beb1b8 | 214 | 1 | 60,612 | 418,579 | 6.91 | 6.91 | 56,127,020 |
| f6838ecd | 99 | 1 | 61,097 | 284,311 | 4.65 | 4.65 | 18,121,107 |
| d2b5fc4e | 149 | 1 | 61,095 | 263,587 | 4.31 | 4.31 | 25,127,462 |
| aeda1d83 | 366 | 2 | 61,391 | 355,707 | 5.79 | 5.79 | 82,381,913 |
| ed8e9182 | 92 | 1 | 61,768 | 233,296 | 3.78 | 3.78 | 15,308,333 |
| 3d849daa | 112 | 1 | 61,842 | 260,764 | 4.22 | 4.22 | 19,486,986 |
| 1e6c06e5 | 30 | 1 | 62,842 | 122,615 | 1.95 | 1.95 | 3,068,783 |
| 6169af22 | 59 | 1 | 63,357 | 165,127 | 2.61 | 2.61 | 7,740,723 |
| 351ebf72 | 163 | 2 | 63,629 | 184,118 | 2.89 | 3.71 | 23,835,039 |
| 7204cadc | 104 | 1 | 63,883 | 227,062 | 3.55 | 3.55 | 17,179,998 |
| 2dec9213 | 75 | 1 | 63,820 | 193,308 | 3.03 | 3.03 | 10,393,815 |
| b1572a48 | 43 | 1 | 64,022 | 171,295 | 2.68 | 2.68 | 5,545,936 |
| fab5c6d1 | 48 | 1 | 64,031 | 150,502 | 2.35 | 2.35 | 5,961,091 |
| 9679503b | 93 | 1 | 64,026 | 391,087 | 6.11 | 6.11 | 23,776,091 |
| 7a037351 | 91 | 1 | 51,720 | 324,258 | 6.27 | 6.27 | 18,521,315 |
| 93b61aea | 54 | 1 | 51,942 | 270,967 | 5.22 | 5.22 | 9,165,766 |
| e9a7a9bf | 117 | 1 | 51,966 | 283,936 | 5.46 | 5.46 | 22,217,983 |
| d6ff3736 | 61 | 1 | 51,889 | 157,808 | 3.04 | 3.04 | 6,751,041 |
| 5c094c0f | 39 | 1 | 51,838 | 146,423 | 2.82 | 2.82 | 4,089,727 |
| ea0f7781 | 40 | 1 | 52,040 | 117,486 | 2.26 | 2.26 | 3,579,958 |
| a84488fd | 57 | 1 | 55,002 | 140,110 | 2.55 | 2.55 | 5,630,475 |
| d241cdc7 | 49 | 1 | 55,027 | 159,686 | 2.90 | 2.90 | 5,262,675 |
| 5d48524f | 35 | 1 | 55,015 | 144,954 | 2.63 | 2.63 | 3,749,029 |

### 4.2 Summary statistics across the 27 sessions

Script output:

| Statistic | First | Last | last/first |
| :--- | ---: | ---: | ---: |
| Min | 51,720 | 62,283 | 1.05 |
| Median | 60,612 | 227,062 | 3.55 |
| Max | 64,031 | 550,187 | 9.49 |

Peak context has min 62,283, median 233,296 and max 550,187. Peak/first has median 3.71 and max 9.49.

### 4.3 Multi-cycle sessions

Multi-cycle sessions behave differently. The per-cycle ratios come from `scripts/session_cost.py`; `ratio_last` is last over the first turn of the session.

| Session | Per-cycle ratios | `ratio_last` | `peak/first` |
| :--- | :--- | ---: | ---: |
| `aeda1d83` | 5.3 and 4.4 | 5.79 | 5.79 |
| `351ebf72` | 3.7 and 2.5 | 2.89 | 3.71 |

## 5. The 15x hard bound (KI-059-9)

Data only. This section makes no recommendation and takes no decision.

| Measure | Value |
| :--- | :--- |
| Median baseline | 60,612 tokens |
| 5x of the median baseline | 303,060 |
| 15x of the median baseline | **909,180**, which is 1.65 times the largest context ever observed (550,187, which is 9.08x the median baseline) |
| Sessions above 5x against their own first turn | **7 of 27** (`ab327e08`, `50beb1b8`, `aeda1d83`, `9679503b`, `7a037351`, `93b61aea`, `e9a7a9bf`). `ea40fe66` (4.98) and `c6ce92da` (4.96) sit just under |
| Sessions above 15x against their own first turn | **0 of 27** |
| Sessions above the absolute median-baseline values | **5** exceed 303,060 and **0** exceed 909,180 |
| Origin of the 958K figure in `KI-059-9` | 15 x 63,883, the first turn of `7204cadc` |
| Closed sessions that reached the hard bound | None |

## 6. Real cost per unit, Sprints 056-058

**Attribution is possible for all three sprints, so abort criterion 7 does not apply.** The reason: rule C attributes 180 of 181 units, and rule P attributes units in every sprint. One unit could not be attributed, and the results are a subset in other respects, stated in the limits below.

### 6.1 Evidence on rewritten history

| Fact | Value |
| :--- | :--- |
| Squash-merge commits on main | `246cd20` (#90, Sprint 056), `15ac17f` (#93, Sprint 057), `000fd0d` (#94, Sprint 058) |
| `✅` shas that resolve with `git show -s --format=%ct` | All 182; `unresolved 0` |
| Shas that are ancestors of `HEAD` | None. `git merge-base --is-ancestor` returned 1 for all 109 + 44 + 29 shas |
| Commits of `git rev-list <tip> --not main` | 36 (056), 164 (057), 53 (058) |
| Status of the original commits | They survive as unreachable objects. They are exposed to garbage collection, so the study records the timestamps |

Units: 181 across 056 (29), 057 (109) and 058 (43). One unit has two shas. `d40f3da` is shared by units 056 `A8` and `A16`.

### 6.2 Attribution rule P (primary)

| Step | Definition |
| :--- | :--- |
| Commit list | `git rev-list --reverse --topo-order <tip> --not main`, covering every commit of the sprint branch, unit or not |
| Tip | The latest-timestamped unit sha of the sprint |
| Turn | A transcript record with `usage`, deduplicated by `message.id` per transcript file. Its time is the timestamp of the first record for that id |
| Sources | Every main transcript and every `subagents/*.jsonl` of the project |
| Charging | A turn at time `t` goes to the interval `(ct[k-1], ct[k]]` and is charged to commit `k`, the first commit with `ct >= t` |
| Unit or overhead | If commit `k` is a unit commit, the turn is charged to that unit. Otherwise it counts as `overhead` |
| Excluded | Turns at or before the first sprint commit, or after the last unit commit |
| Consequence | A turn between two commits belongs to the commit that closes the interval |

Results of rule P:

| Sprint | Sprint commits | Unit commits | Overhead turns | Overhead four-field tokens | Unit four-field tokens | Unit turns | Subagent turns in units |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 056 | 36 | 27 | 61 | 6,658,574 | 16,293,652 | 165 | 119 |
| 057 | 164 | 109 | 504 | 61,698,560 | 60,906,848 | 512 | 237 |
| 058 | 53 | 44 | 80 | 10,680,870 | 40,384,018 | 401 | 169 |

All attributed turns carry the sprint's own `gitBranch` (`ai-sprint/056`, `/057`, `/058`): 165, 512 and 401 turns respectively.

### 6.3 Units that rule P could not attribute: 40

| Cause | Detail |
| :--- | :--- |
| Empty interval | 38 unit commits were committed at most 3 seconds after the previous sprint commit (`zero.py`: max gap 3 s). In 37 of them the previous commit is also a unit commit, which indicates batch commits from one command. They are 31 in 057 and 7 commits in 056 |
| Shared sha | Units `A8` and `A16` of 056 share `d40f3da`, so rule P charges only `A16` |
| Sha outside the tip chain | Unit `B7` of 056 has sha `5083e70`, which is outside the tip's chain, so it has no interval at all |

### 6.4 Attribution rule C (used for the group table)

Rule C is rule P, except that unit commits with an empty interval pool their cost with the next commit that has turns, split evenly across the batch's units. It attributes **180 of 181 units** (056: 28 of 29, 057: 109 of 109, 058: 43 of 43). The one unattributed unit is `B7`. The even split is an assumption that blurs per-unit differences within a batch.

Rule A uses unit commits only as boundaries. It attributes 42 fewer units than rule P.

### 6.5 Group table under rule C

Medians and ranges by group under rule C. Tokens are four-field totals (`total4`) and fresh tokens (`fresh`). Operation is create or modify. `refactor` (one unit) is grouped with modify. File type comes from the path of the first backticked file: `rules/`, `workflows/`, `agents/`, `commands/`, `agents.md` and `CLAUDE.md` are rule; `.py`, `.sh`, `.json`, `.yml`, `Makefile`, `scripts/`, `hooks/` and `tests/` are script; everything else is doc.

| Group | n | total4 median | total4 min-max | fresh median | fresh min-max |
| :--- | ---: | ---: | :--- | ---: | :--- |
| create/doc | 4 | 2,400,341 | 378,541-3,960,991 | 115,354 | 34,705-152,885 |
| create/script | 15 | 801,408 | 161,594-3,407,649 | 17,087 | 1,025-150,126 |
| modify/doc | 33 | 325,166 | 87,273-4,482,977 | 3,753 | 1,005-283,578 |
| modify/rule | 41 | 406,971 | 87,273-3,066,658 | 4,883 | 676-179,498 |
| modify/script | 87 | 472,164 | 71,143-3,563,167 | 10,101 | 1,005-637,749 |
| risk high | 22 | 850,709 | 79,005-3,960,991 | 54,797 | 1,025-210,567 |
| risk medium | 53 | 696,561 | 87,273-4,482,977 | 10,101 | 676-637,749 |
| risk low | 105 | 325,166 | 71,143-3,407,649 | 4,613 | 676-365,769 |
| modify/script/high | 13 | 749,659 | 79,005-2,958,876 | 66,204 | 3,894-210,567 |
| modify/script/medium | 31 | 641,824 | 87,273-3,563,167 | 10,101 | 1,005-637,749 |
| modify/script/low | 43 | 257,612 | 71,143-1,266,592 | 4,717 | 1,005-365,769 |
| modify/rule/high | 3 | 842,022 | 794,455-1,453,529 | 49,477 | 11,953-129,877 |
| modify/rule/medium | 14 | 522,971 | 103,478-1,358,068 | 7,867 | 676-142,863 |
| modify/rule/low | 24 | 312,919 | 87,273-3,066,658 | 4,037 | 676-179,498 |
| modify/doc/low | 31 | 304,066 | 87,273-1,811,820 | 2,798 | 1,005-283,578 |
| create/script/low | 6 | 724,229 | 402,548-3,407,649 | 26,377 | 6,050-123,151 |
| create/script/medium | 6 | 814,243 | 377,555-1,270,444 | 33,574 | 3,612-150,126 |
| create/script/high | 3 | 1,248,923 | 161,594-1,565,941 | 15,109 | 1,025-20,113 |

The small cells `create/doc/{high,low,medium}`, `modify/doc/{high,medium}` and `modify/doc/high` have n of 1 or 2, so their medians are single observations. The full output prints turn counts too. Per sprint, `total4` medians are 205,622 (056, n=28), 403,580 (057, n=109) and 715,884 (058, n=43).

### 6.6 Sensitivity to the rule

Rule P and rule A numbers differ materially. Rule A (unit commits only as boundaries) attributes 42 fewer units than rule P. It gives larger medians, for example modify/rule max 14,294,365 and modify/script max 11,048,181, because it also absorbs non-unit work between units. The full outputs of all three rules are produced by `attribute.py` (section 8). Medians shift by up to about 2x between the rules, so any D14 estimate table must name its rule.

### 6.7 Limits of this attribution

| Limit | Detail |
| :--- | :--- |
| `total4` measures context size | `total4` is dominated by `cache_read`, which scales with the context size at the time of the unit, not with the unit's difficulty. `fresh` is the better difficulty signal |
| Parallel subagent work | Work in the same time window is charged by time, not by task, so overlapping units can mix |
| Commit time versus work time | Commits are original timestamps from preserved objects; whether the committer time equals work time is unverified |
| Unreachable originals | The original commits are unreachable objects exposed to garbage collection (6.1) |
| Scratchpad projects not read | The scratchpad project directories under `~/.claude/projects/` (5 directories named `-private-tmp-...-scratchpad-...`) were not read |
| Rule C absorbs non-unit commit cost | In `rule_c` (section 8, `attribute.py`), a pending batch of units is assigned to the next commit that has turns (`if a and a[2]: if pending: ...`). The branch does not test whether that commit is a unit commit. When it is a non-unit commit, the batch is charged that commit's whole cost, split evenly across the batch's units, so that cost is not counted as `overhead` |
| Even split | The even split inside a batch blurs per-unit differences (6.4) |
| One unit unattributed | Unit `B7` of 056 has no interval under any rule (6.3) |

Abort criterion 7 does not apply: attribution is possible for all three sprints (6.4: 180 of 181 units, with `B7` as the single exception and every sprint represented).

## 7. Candidate methods

Four methods for in-session cost control. None is chosen here.

| # | Method | Figure | Main objection |
| :--- | :--- | :--- | :--- |
| 1 | Planned per-unit budget with suspend points (D14) | Rule C medians vary by type and risk, for example `fresh` 4,613 (low) against 54,797 (high), and `total4` 325,166 against 850,709 | The spread inside each group is wide (low-risk `fresh` runs 676 to 365,769), and `total4` depends on context size at execution time, so estimates carry no tight error bound |
| 2 | Lower the hard bound, or add an absolute-token trigger | 0 of 27 sessions ever reached 15x, 7 reached 5x, the maximum was 9.49x, and the absolute 15x value of 909,180 is 1.65 times the largest observed context | Any new threshold is chosen from n=27 sessions of one repository and cannot be validated. Also, a bound that fires earlier makes the `agents.md` trim (which lowers `first`) tighten it further, as `KI-059-9` notes |
| 3 | Delegate read-heavy work to subagents for context isolation | Subagents start at a median 26,252 tokens against 60,612 for main sessions, peak at a median 42,133, and take 23.1% of tokens | They run on a 5m cache TTL (against 1h for main), 7.9% of their turns are cold-cache against 1 of 2,726 in main, and in rule P 169 of 401 sprint-058 unit turns were already subagent turns, so the total is not obviously lower |
| 4 | Cut the boot baseline | Every turn re-reads a median 60,612-token first-turn context, and `cache_read` is 94.14% of all tokens. The `instructions` attachment is a median 52,505 chars, the skill listing 20,311 chars (42 skills) and the agent listing 8,610 chars | A smaller baseline raises the ratio for the same growth, so the 5x and 15x triggers fire sooner (`KI-059-9`), and the progressive-loading convention for `rules/` is enforced only by agent judgment |

## 8. Reproduction

The scripts were run from the repository root with `python3 -I`. `$TMPDIR` is ephemeral, which is why the script text is kept in this file. Run each script as `python3 -I $TMPDIR/<name>.py`, in this order: `units.py`, then `attribute.py` (needs `units.json`), then `zero.py` (needs `perunit.json` from `attribute.py`). The others are independent. Shell commands for inline checks are quoted where used.

**`growth.py`** (section 4):

```python
"""A-00 measurement 3: context growth boot->close per closed main-session transcript."""
import glob, json, os, statistics as st, subprocess, sys
sys.path.insert(0, "scripts")
import session_cost as sc
live = json.load(open("docs/active_state.json"))["session_id"]
d = os.path.expanduser("~/.claude/projects/-Users-gstmirabal-Developer--agents/")
rows = []
for p in sorted(glob.glob(d + "*.jsonl"), key=os.path.getmtime):
    uid = os.path.basename(p)[:-6]
    if uid == live:
        continue
    out = subprocess.run([sys.executable, "-I", "scripts/session_cost.py", "--json", "--session", uid],
                         capture_output=True, text=True)
    j = json.loads(out.stdout)
    if not j.get("measurable"):
        rows.append((uid, None)); continue
    turns, _ = sc.read_turns(__import__("pathlib").Path(p))
    ctx = [sc.context_size(t) for t in turns]
    first, last, peak = j["cycles"][0]["first_turn"], ctx[-1], max(ctx)
    tot = sum(j["totals"].values())
    rows.append((uid, dict(msgs=j["messages"], cycles=len(j["cycles"]), first=first, last=last, peak=peak,
        ratio_last=round(last/first,2), ratio_peak=round(peak/first,2), total=tot,
        model=",".join(j["by_model"]), mtime=int(os.path.getmtime(p)))))
for uid, r in rows: print(uid[:8], r)
m = [r for _, r in rows if r]
print("n_listed", len(rows), "n_measurable", len(m))
for k in ("first", "last", "peak", "ratio_last", "ratio_peak"):
    v = sorted(r[k] for r in m); print(k, "min", v[0], "median", st.median(v), "max", v[-1])
med = st.median(r["first"] for r in m)
print("median first", med, "5x", 5*med, "15x", 15*med)
for k in ("ratio_last", "ratio_peak"):
    print(k, ">5x", sum(r[k] > 5 for r in m), ">15x", sum(r[k] > 15 for r in m))
print("peak > 15x median baseline", sum(r["peak"] > 15*med for r in m), "; > 5x", sum(r["peak"] > 5*med for r in m))
print("last > 15x median baseline", sum(r["last"] > 15*med for r in m), "; > 5x", sum(r["last"] > 5*med for r in m))
```

Literal tail of its output:

```
n_listed 27 n_measurable 27
first min 51720 median 60612 max 64031
last min 62283 median 227062 max 550187
peak min 62283 median 233296 max 550187
ratio_last min 1.05 median 3.55 max 9.49
ratio_peak min 1.05 median 3.71 max 9.49
median first 60612 5x 303060 15x 909180
ratio_last >5x 7 >15x 0
ratio_peak >5x 7 >15x 0
peak > 15x median baseline 0 ; > 5x 5
last > 15x median baseline 0 ; > 5x 5
```

The per-cycle ratios for the two multi-cycle sessions come from `python3 -I scripts/session_cost.py --json --session aeda1d83-cbd8-463b-8f56-25f5958d428e` and the same for `351ebf72-6bc5-40c4-8cc6-c50ae436d806`, read through `json.load`. Outputs: `aeda1d83 [(180, 61391, 322677, 5.3), (186, 80226, 355707, 4.4)]` and `351ebf72 [(106, 63629, 236223, 3.7), (57, 73842, 184118, 2.5)]`.

**`units.py`** (section 6, step 1):

```python
"""A-00 measurement 4, step 1: units (rows with a checkmark and sha) of 056-058, and whether each sha resolves."""
import glob, re, subprocess, json
units = []
for sp in ("056", "057", "058"):
    f = glob.glob(f"docs/sprints/{sp}*/task_scope.md")[0]
    for ln in open(f, encoding="utf-8"):
        if not ln.startswith("|") or "✅" not in ln: continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        shas = re.findall(r"`([0-9a-f]{7,40})`", cells[-1])
        if not shas: continue
        units.append(dict(sprint=sp, id=cells[0].strip("`"), file=cells[1], op=cells[2] if sp!="056" else cells[2], risk=None, cells=cells, shas=shas))
bad = 0
for u in units:
    ts = []
    for s in u["shas"]:
        r = subprocess.run(["git","show","-s","--format=%ct",s],capture_output=True,text=True)
        ts.append(int(r.stdout) if r.returncode==0 else None)
    u["ts"]=ts
    if None in ts: bad += 1
json.dump(units, open(__import__("os").environ["TMPDIR"]+"/units.json","w"))
from collections import Counter
print(Counter(u["sprint"] for u in units), "units", len(units), "unresolved", bad)
print("multi-sha", sum(len(u["shas"])>1 for u in units))
```

Output: `Counter({'057': 109, '058': 43, '056': 29}) units 181 unresolved 0`. The `units.json` file holds 182 shas across 181 units; `multi-sha 1`. One 058 row has an escaped pipe in its file cell, so `attribute.py` reads risk from `cells[-5]`.

**`attribute.py`** (section 6, rules P, A and C), as run:

```python
"""A-00 measurement 4: cost per unit (056-058) by crossing commit times with transcript turns.

Rule P (primary): sprint commits = `git rev-list --reverse --topo-order <tip> --not main` (all commits of the
sprint branch, unit or not). A turn at time t (timestamp of the first record of its message.id, deduplicated
per transcript file) belongs to the interval (ct[k-1], ct[k]] and is charged to commit k. If commit k is a unit
commit the turn is charged to that unit; otherwise it is `overhead`. Turns <= ct of the first sprint commit or
> ct of the last unit commit are `outside`. Rule A (sensitivity): boundaries are unit commits only.
Transcripts: every main transcript and every subagents/*.jsonl of the project dir.
"""
import glob, json, os, re, subprocess, statistics as st, collections, datetime as dt, sys
TMP = os.environ["TMPDIR"]
D = os.path.expanduser("~/.claude/projects/-Users-gstmirabal-Developer--agents/")
FIELDS = ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")
def epoch(s): return dt.datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()
def git(*a): return subprocess.run(["git", *a], capture_output=True, text=True).stdout

# turns: (t, total4, fresh, is_sub, file)
turns = []
for p in glob.glob(D + "*.jsonl") + glob.glob(D + "*/subagents/*.jsonl"):
    seen = set(); sub = "/subagents/" in p
    for l in open(p, encoding="utf-8", errors="replace"):
        try: r = json.loads(l)
        except Exception: continue
        m = r.get("message")
        if not isinstance(m, dict) or not m.get("usage") or m.get("model") == "<synthetic>": continue
        i = m.get("id")
        if i in seen: continue
        if i: seen.add(i)
        u = m["usage"]; v = [u.get(f) or 0 for f in FIELDS]
        turns.append((epoch(r["timestamp"]), sum(v), v[0] + v[1] + v[3], sub, os.path.basename(p), r.get("gitBranch")))
turns.sort()
print("turns loaded", len(turns), "subagent turns", sum(t[3] for t in turns))

units = json.load(open(TMP + "/units.json"))
def ftype(path):
    if path.startswith(("rules/", "workflows/", "agents/", "commands/")) or path in ("agents.md", "CLAUDE.md"): return "rule"
    if path.endswith((".py", ".sh", ".json", "Makefile")) or path.startswith(("scripts/", "hooks/", "tests/")) or path.endswith(".yml"): return "script"
    return "doc"
for x in units:
    x["risk"] = x["cells"][-5]
    x["subject"] = re.findall(r"`([^`]+)`", x["cells"][1])[0]
    x["opk"] = re.split(r"[ :(,]", x["cells"][2].strip("`"))[0]
    x["ftype"] = ftype(x["subject"])

def rule_c(sp, commits, units_of, res):
    """Rule C: rule P, but a unit commit with an empty interval (batch commit) shares the cost of the next
    commit that has turns, split evenly among the batch's units."""
    import bisect
    cts = [ct for _, ct in commits]; per_commit = collections.defaultdict(lambda: [0, 0, 0, 0])
    last_unit_ct = max(ct for h, ct in commits if h in units_of)
    for (t, tot, fresh, sub, f, br) in turns:
        if t <= cts[0] or t > last_unit_ct: continue
        a = per_commit[commits[bisect.bisect_left(cts, t)][0]]; a[0] += tot; a[1] += fresh; a[2] += 1; a[3] += sub
    acc = {}; pending = []
    for h, _ in commits:
        if h in units_of: pending += units_of[h]
        a = per_commit.get(h)
        if a and a[2]:
            if pending:
                n = len(pending)
                for uid in pending: acc[uid] = [a[0] / n, a[1] / n, a[2] / n, a[3] / n, collections.Counter()]
            pending = []
        elif h not in units_of: pending = pending  # empty non-unit commit changes nothing
    return acc

def run(rule):
    res = {}; extra = {}
    for sp in ("056", "057", "058"):
        us = [x for x in units if x["sprint"] == sp]
        tip = max((t, s) for x in us for s, t in zip(x["shas"], x["ts"]))[1]
        out = git("rev-list", "--reverse", "--topo-order", "--format=%H %ct", tip, "--not", "main").split("\n")
        commits = [(l.split()[0], int(l.split()[1])) for l in out if re.match(r"^[0-9a-f]{40} \d+$", l)]
        unit_of = {}; units_of = collections.defaultdict(list)
        for x in us:
            for s in x["shas"]:
                full = git("rev-parse", s).strip(); unit_of[full] = x["id"]; units_of[full].append(x["id"])
        if rule == "A": commits = [c for c in commits if c[0] in unit_of]
        if rule == "C":
            return rule_c(sp, commits, units_of, res)
        last_unit_ct = max(ct for h, ct in commits if h in unit_of)
        cts = [ct for _, ct in commits]
        acc = collections.defaultdict(lambda: [0, 0, 0, 0, collections.Counter()])
        import bisect
        for (t, tot, fresh, sub, f, br) in turns:
            if t <= cts[0] or t > last_unit_ct: continue
            k = bisect.bisect_left(cts, t)          # first commit with ct >= t
            h = commits[k][0]
            key = unit_of.get(h, "overhead")
            a = acc[key]; a[0] += tot; a[1] += fresh; a[2] += 1; a[3] += sub; a[4][br] += 1
        res[sp] = (acc, len(commits), sum(h in unit_of for h, _ in commits))
    return res

def summarize(res):
    rows = []
    for x in units:
        acc = res[x["sprint"]][0]
        a = acc.get(x["id"])
        rows.append((x, a))
    return rows

P = run("P"); A = run("A")
C = {}
for sp in ("056", "057", "058"):
    us = [x for x in units if x["sprint"] == sp]
    tip = max((t, s) for x in us for s, t in zip(x["shas"], x["ts"]))[1]
    out = git("rev-list", "--reverse", "--topo-order", "--format=%H %ct", tip, "--not", "main").split("\n")
    commits = [(l.split()[0], int(l.split()[1])) for l in out if re.match(r"^[0-9a-f]{40} \d+$", l)]
    uo = collections.defaultdict(list)
    for x in us:
        for s_ in x["shas"]: uo[git("rev-parse", s_).strip()].append(x["id"])
    C[sp] = (rule_c(sp, commits, uo, None), len(commits), len(uo))
json.dump({sp: {k: v[:4] for k, v in P[sp][0].items()} for sp in P}, open(TMP + "/perunit.json", "w"))
for rule, R in (("P", P), ("A", A), ("C", C)):
    print("=== rule", rule)
    for sp in R:
        acc, nc, nu = R[sp]
        ov = acc.get("overhead", [0, 0, 0, 0])
        if rule == "C": print(sp, "units with an estimate", len(acc)); continue
        print(sp, "sprint commits", nc, "unit commits", nu, "overhead turns", ov[2], "overhead tokens", ov[0],
              "unit tokens", sum(v[0] for k, v in acc.items() if k != "overhead"),
              "unit turns", sum(v[2] for k, v in acc.items() if k != "overhead"),
              "subagent turns in units", sum(v[3] for k, v in acc.items() if k != "overhead"))
    rows = summarize(R)
    zero = [x for x, a in rows if not a or a[2] == 0]
    print("units with zero turns attributed:", len(zero), [(x["sprint"], x["id"]) for x in zero])
    def grp(keyf, name):
        g = collections.defaultdict(list)
        for x, a in rows:
            if a and a[2]: g[keyf(x)].append((a[0], a[1], a[2]))
        print("-- by", name)
        for k in sorted(g):
            v = g[k]; tot = sorted(i[0] for i in v); fr = sorted(i[1] for i in v); tn = sorted(i[2] for i in v)
            print(f"{str(k):28s} n={len(v):3d} total4 med={int(st.median(tot)):>10,} min={tot[0]:>10,} max={tot[-1]:>11,} | fresh med={int(st.median(fr)):>8,} min={fr[0]:>8,} max={fr[-1]:>9,} | turns med={st.median(tn)} min={tn[0]} max={tn[-1]}")
    grp(lambda x: (x["opk"] if x["opk"] in ("create", "modify") else "modify") + "/" + x["ftype"], "operation/filetype")
    grp(lambda x: x["risk"], "risk")
    grp(lambda x: (x["opk"] if x["opk"] in ("create", "modify") else "modify") + "/" + x["ftype"] + "/" + x["risk"], "operation/filetype/risk")
    grp(lambda x: x["sprint"], "sprint")
    if rule == "P":
        br = collections.Counter()
        for sp in R:
            for k, v in R[sp][0].items():
                if k != "overhead":
                    for b, n in v[4].items(): br[(sp, b)] += n
        print("branch of attributed unit turns", dict(br))
```

The `grp` function in rule C prints fractional values with raw floats because batch splitting produces non-integer turn counts. This changes presentation only, not any median. The full per-rule output is what the script prints; the rule C table in 6.5 is quoted from it.

**`zero.py`** (why units had no turns), output `38 zero-turn unit commits`, `max gap 3`, `previous commit is also a unit commit: 37`, counts `057: 31, 056: 7`:

```python
"""For units with zero attributed turns under rule P: seconds since the previous sprint commit."""
import json, os, re, subprocess, collections
TMP=os.environ["TMPDIR"]
units=json.load(open(TMP+"/units.json")); per=json.load(open(TMP+"/perunit.json"))
def git(*a): return subprocess.run(["git",*a],capture_output=True,text=True).stdout
gaps=[]
for sp in ("056","057","058"):
    us=[x for x in units if x["sprint"]==sp]
    tip=max((t,s) for x in us for s,t in zip(x["shas"],x["ts"]))[1]
    out=git("rev-list","--reverse","--topo-order","--format=%H %ct",tip,"--not","main").split("\n")
    cm=[(l.split()[0],int(l.split()[1])) for l in out if re.match(r"^[0-9a-f]{40} \d+$",l)]
    full={git("rev-parse",s).strip():x["id"] for x in us for s in x["shas"]}
    for i,(h,ct) in enumerate(cm):
        uid=full.get(h)
        if uid and uid not in per[sp]:
            gaps.append((sp,uid,ct-cm[i-1][1],cm[i-1][0] in full))
print(len(gaps),"zero-turn unit commits")
print("gap seconds to previous sprint commit: max",max(g[2] for g in gaps),"; <=5s:",sum(g[2]<=5 for g in gaps),"; >5s:",[g for g in gaps if g[2]>5])
print("previous commit is also a unit commit:",sum(g[3] for g in gaps))
print(collections.Counter(g[0] for g in gaps))
```

Three inline checks, run as `python3 -I -` heredocs, gave these results:

| Check | Result |
| :--- | :--- |
| Shared shas | `1 shared shas covering 2 units`, namely `d40f3da` for 056 `A8` and `A16` |
| Unit shas outside the tip chain (`git rev-list <tip> --not main` against `git rev-parse <sha>`) | `056 36 unit shas outside tip chain: [('B7', ['5083e70'])]`; 057 and 058 have none |
| Ancestry (`git merge-base --is-ancestor <sha> HEAD`) | `Counter({('057', 1): 109, ('058', 1): 44, ('056', 1): 29})`, so the return code is 1 for every sha |

**`sessions.py`** (span and branch of every transcript): lists each main transcript with the first and last timestamp, `gitBranch` counts, turn count and subagent count. It is the 25-line script that globs `*.jsonl` and `*/subagents/*.jsonl`, and its output is the basis for the session-to-sprint mapping and the "5616 turns" snapshot. Reproduce with:

```python
"""List every transcript (main + subagent) with time span, branches, turn counts."""
import glob, json, os, collections
d = os.path.expanduser("~/.claude/projects/-Users-gstmirabal-Developer--agents/")
for p in sorted(glob.glob(d+"*.jsonl"), key=os.path.getmtime):
    ts=[];br=collections.Counter();ids=set()
    for l in open(p):
        try:r=json.loads(l)
        except: continue
        if r.get("timestamp"): ts.append(r["timestamp"])
        if r.get("gitBranch"): br[r["gitBranch"]]+=1
        m=r.get("message")
        if isinstance(m,dict) and m.get("usage") and m.get("id"): ids.add(m["id"])
    sub=glob.glob(p[:-6]+"/subagents/*.jsonl")
    print(os.path.basename(p)[:8], min(ts), max(ts), dict(br), "turns",len(ids),"subagents",len(sub))
```

**`mech.py`** (section 3 transcript evidence): scans `system` records (`compact_boundary` count, subtypes), `<command-name>` slash commands in user records, and per-role token sums. Output lines: `system subtypes {'stop_hook_summary': 432, 'compact_boundary': 2, 'informational': 2, 'local_command': 5, 'api_error': 13}` and `slash commands seen in user records {'/agents:start': 28, '/clear': 5}`. It also printed `cache_read share of all four-field tokens 0.9414` and `subagent share of four-field tokens 0.2309`. Its text:

```python
"""A-00 measurement 2 (transcript evidence): compact events, slash commands, cache split, subagent share."""
import glob, json, os, re, collections, statistics as st
D = os.path.expanduser("~/.claude/projects/-Users-gstmirabal-Developer--agents/")
F = ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")
sub_types = collections.Counter(); cmds = collections.Counter(); comp = []
tot = {"main": [0]*4, "sub": [0]*4}; c1h = c5m = 0; firsts = []; nsub = 0; subfirst = []
hookev = collections.Counter(); attr = collections.Counter()
for p in glob.glob(D + "*.jsonl") + glob.glob(D + "*/subagents/*.jsonl"):
    sub = "/subagents/" in p; seen = set(); first = None
    for l in open(p, encoding="utf-8", errors="replace"):
        try: r = json.loads(l)
        except Exception: continue
        if r.get("type") == "system": sub_types[r.get("subtype")] += 1
        if r.get("subtype") == "compact_boundary": comp.append((os.path.basename(p)[:8], r.get("compactMetadata")))
        if r.get("subtype") in ("hook_started","hook_response","stop_hook_summary") or r.get("hookInfos"): hookev[(r.get("subtype"), r.get("hookEvent") or r.get("hook_event"))] += 1
        m = r.get("message")
        if r.get("type") == "user" and isinstance(m, dict):
            c = m.get("content"); c = c if isinstance(c, str) else json.dumps(c)
            for name in re.findall(r"<command-name>(/?[\w:-]+)</command-name>", c): cmds[name] += 1
        if not isinstance(m, dict) or not m.get("usage") or m.get("model") == "<synthetic>": continue
        i = m.get("id")
        if i in seen: continue
        seen.add(i); u = m["usage"]
        v = [u.get(f) or 0 for f in F]
        for k in range(4): tot["sub" if sub else "main"][k] += v[k]
        cc = u.get("cache_creation") or {}
        c1h += cc.get("ephemeral_1h_input_tokens", 0); c5m += cc.get("ephemeral_5m_input_tokens", 0)
        if first is None: first = v[0] + v[2] + v[3]
        if r.get("attributionSkill"): attr[r["attributionSkill"]] += 1
    if first is not None and sub: subfirst.append(first)
print("system subtypes", dict(sub_types))
print("compact_boundary records", len(comp)); [print(" ", c) for c in comp[:20]]
print("slash commands seen in user records", dict(cmds))
print("hook events", dict(hookev))
for k, v in tot.items(): print(k, dict(zip(F, v)), "sum", sum(v))
print("cache_creation 1h", c1h, "5m", c5m)
cr = tot["main"][2] + tot["sub"][2]; allsum = sum(tot["main"]) + sum(tot["sub"])
print("cache_read share of all four-field tokens", round(cr / allsum, 4))
print("subagent first-turn context: n", len(subfirst), "median", st.median(subfirst), "min", min(subfirst), "max", max(subfirst))
print("subagent share of four-field tokens", round(sum(tot["sub"]) / allsum, 4))
print("attributionSkill turns", dict(attr.most_common(12)))
```

**`cache.py`** (cache TTL split and subagent context size): output was `main n=2726 cold=1 c1h=16611110 c5m=0 cr=514195451 cc=16611110`, `sub n=2909 cold=229 c1h=0 c5m=19696172 cr=139051459 cc=19696172`, and `subagent transcripts 270 turns median 7.5 max 56`, `first-turn ctx median 26252.5`, `peak ctx median 42133.0 max 175947`. Text:

```python
"""A-00 measurement 2: prompt-cache evidence and subagent context size, from transcripts (deduplicated by message.id)."""
import glob, json, os, statistics as st
D = os.path.expanduser("~/.claude/projects/-Users-gstmirabal-Developer--agents/")
res = {"main": dict(n=0, cold=0, c1h=0, c5m=0, cr=0, cc=0), "sub": dict(n=0, cold=0, c1h=0, c5m=0, cr=0, cc=0)}
subpeak = []; subfirst = []; subturns = []
for p in glob.glob(D + "*.jsonl") + glob.glob(D + "*/subagents/*.jsonl"):
    k = "sub" if "/subagents/" in p else "main"; seen = set(); ctx = []
    for l in open(p, encoding="utf-8", errors="replace"):
        try: r = json.loads(l)
        except Exception: continue
        m = r.get("message")
        if not isinstance(m, dict) or not m.get("usage") or m.get("model") == "<synthetic>": continue
        i = m.get("id")
        if i in seen: continue
        seen.add(i); u = m["usage"]; cc = u.get("cache_creation") or {}
        a = res[k]; a["n"] += 1; a["cold"] += (u.get("cache_read_input_tokens") or 0) == 0
        a["c1h"] += cc.get("ephemeral_1h_input_tokens", 0); a["c5m"] += cc.get("ephemeral_5m_input_tokens", 0)
        a["cr"] += u.get("cache_read_input_tokens") or 0; a["cc"] += u.get("cache_creation_input_tokens") or 0
        ctx.append((u.get("cache_read_input_tokens") or 0) + (u.get("cache_creation_input_tokens") or 0) + (u.get("input_tokens") or 0))
    if k == "sub" and ctx: subpeak.append(max(ctx)); subfirst.append(ctx[0]); subturns.append(len(ctx))
print(res)
print("subagent transcripts", len(subpeak), "turns median", st.median(subturns), "max", max(subturns))
print("subagent first-turn ctx median", st.median(subfirst), "peak ctx median", st.median(subpeak), "max", max(subpeak))
```

**Inline attachment scans** (section 3 sizes), run as `python3 -I -` heredocs over `message`-less `attachment` records:

| Scan | Result |
| :--- | :--- |
| Attachment sizes (chars of the JSON-encoded attachment) | `skill_listing` n=34, median 20,311; `instructions` n=31, median 52,505; `agent_listing_delta` n=30, median 8,610; `deferred_tools_delta` n=31, median 6,731; `mcp_instructions_delta` n=30, median 2,157; `sandbox_instructions` n=7, median 7,233; `invoked_skills` n=2, median 1,584 |
| Stop hook | `Counter({'~/.config/iterm2/cc-status': 432}) median ms 12.0 max 177` (the scan printed the user-level home path of this file) |
| Skill count | The 42 in the `skill_listing` is the `skillCount` field of that attachment |

**Other commands run, with literal results:**

| Command | Result |
| :--- | :--- |
| `python3 -I skills/token-saver-auditor/scripts/audit_plan.py --current-sprint` | Exit 0 and `[OK] audit_plan: docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md` (the scan printed the absolute path of this file; 107 bytes) |
| `python3 -I skills/omni-context-minimizer/scripts/omni_minimizer.py scripts/session_probe.py` | Exit 0, ending with `--- [OPTIMIZATION]: The file was reduced to 40 lines of pure AST structure. ---` (45 lines, 2,297 bytes) |
| `python3 -I scripts/session_cost.py --json --session 7204cadc-d44b-4226-a000-597c17b52b33` | A one-cycle record: `messages 104`, `first_turn 63883`, `peak 227062`, `ratio 3.6`, totals `input 230`, `output 68,200`, `cache_read 16,819,796`, `cache_creation 291,772` |
