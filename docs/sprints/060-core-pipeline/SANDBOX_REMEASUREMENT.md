# Sprint 060 H-01 - Sandbox Re-measurement on CLI 2.1.311

Re-run of the matrices of `docs/sprints/055-core-pipeline/SANDBOX_MEASUREMENT.md` and `docs/sprints/056-core-pipeline/SANDBOX_ENUMERATION.md` on Claude Code 2.1.311. Paths are genericized (`RA-15`): `~` is the home directory, `<repo>` is the nucleus working tree, `<fx>` is the scratch fixture host, `<scratch>` is its parent directory. No `.env*` file of the nucleus was read, created, modified or deleted (`RA-09`); the fixture `.env` held a dummy value written for the run.

| Field | Value |
| :--- | :--- |
| Unit | `H-01` (`task_scope.md`, plan row `H-01`) |
| Finding | `KI-059-31`; `KI-060-09` (the sandboxed session could not finish the unit) |
| Date | 2026-11-22 |
| CLI | Claude Code 2.1.311 (`claude --version`); 055 and 056 measured 2.1.119 |
| Platform | macOS, Seatbelt |
| Sessions | Session 95 (sandboxed): 055 sandboxed column, `7dad78d`. A second, unsandboxed session chosen by the human: 055 unsandboxed column, the fixture host, its install, and the headless sessions A to E |
| Status | Complete for the scope in section 7; the items listed there are not measured |

## 1. Method

| Item | Fact |
| :--- | :--- |
| Runner (055 columns) | One `timeout 90` subprocess per case from the repository root, through a scratch wrapper that records the exit code and the last three output lines with `~` and `<repo>` redacted. The wrapper is not committed. The sandboxed column ran in the agent's own Bash tool inside session 95's Seatbelt sandbox; the unsandboxed column ran in the same way from a session with no sandbox (`SBX0` exit 1, `SBX1` exit 0 at both ends) |
| Settings in effect (055 columns) | The nucleus project settings `.claude/settings.json`, as merged for this working tree (not an overlay file). No user-scope file was read |
| Fixture `<fx>` (056 matrix, 055 sections 4 and 9) | Scratch host, `git init`; `.agents` added with `git submodule add` from the nucleus at `ced24b4` (gitdir `.git/modules/.agents`, `.agents/.git` = `gitdir:` file); `venv_skillopt` symlinked into the nucleus venv and excluded through the submodule `info/exclude`; `.env` = a 34-byte dummy line, `.env.example` = an empty key; local bare remote `origin`; deleted after the run |
| Install | `python3 .agents/scripts/install.py --target claude`, run outside the sandbox: merged `.claude/settings.json` and `.mcp.json`, linked `.claude/agents/*`, `.claude/skills/*`, installed host `.git/hooks/pre-commit`, `commit-msg`, `pre-push`, wrote `.agents/.bridge_claude.lock` |
| Fixture settings | Template as merged by install; `.claude/settings.local.json` absent in session A and set per session in B to E (section 5) |
| Session driver | Headless `claude -p --model sonnet --allowedTools Bash Read --output-format stream-json`, launched from `<fx>`; each numbered step its own Bash call |
| Probe rule | By operation (056 section 2 correction): every protected path is built at runtime inside `zz_probe.py`, so the command text never names it and only the sandbox layer answers |
| Controls | `SBX0` `printenv HTTPS_PROXY`, `SBX1` `curl --noproxy '*'` to `registry.npmjs.org`. Valid sandboxed run: `SBX0` exit 0 and `SBX1` non-zero (exit 6 where recorded) |
| Leak check | `grep -c` of the dummy value over each session transcript: 0 in sessions A to E |
| Cost | 7 `claude -p` calls: 1 login check, 1 refused attempt of session A (it declined commands given without context; re-issued with the fixture context and identical commands), sessions A to E |

### 1.1 Sandbox configuration in effect (nucleus)

`.claude/settings.json` top-level keys: `sandbox`, `permissions`, `env`. `.claude/settings.local.json` top-level keys: `permissions` only (seven `allow` entries for `Bash(...)` commands; no `sandbox` key, no `deny`).

| Key | Value in `.claude/settings.json` |
| :--- | :--- |
| `sandbox.enabled` | `true` |
| `sandbox.autoAllowBashIfSandboxed` | `true` |
| `sandbox.allowUnsandboxedCommands` | `false` |
| `sandbox.network.allowedDomains` | `api.github.com`, `github.com`, `pypi.org`, `files.pythonhosted.org` |
| `sandbox.filesystem.denyRead` | `./.env`, `./.env.*`, `~/.docker/config.json`, `~/.config/gh`, `~/.zsh_history`, `~/.claude/projects`, `~/Library/Keychains/login.keychain-db`, `~/.ssh`, `~/.aws`, `~/.npmrc`, `~/.bash_history`, `~/**/.env*` |
| `sandbox.filesystem.allowRead` | `./.env.example`, `./.env.sample`, `./.env.template` |
| `sandbox.filesystem.denyWrite` | `./.env`, `./agents`, `./venv_skillopt` |
| `sandbox.credentials.files` | `./.env` with `mode: deny` |
| `permissions.disableBypassPermissionsMode`, `disableAutoMode` | `disable`, `disable` |
| `permissions.deny` (path rules) | `Edit(/.agents/**)`, `Edit(/.git/modules/.agents/**)`, `Edit(/.env)`, `Read(/.env)`, `Read(/**/.env*)`, `Edit(/.claude/settings*.json)`, `Edit(~/.ssh/**)`, `Edit(~/.aws/**)`, `Edit(~/.gnupg/**)`, `Edit(~/.config/gh/**)`, `Edit(~/.docker/**)`, `Edit(~/Library/LaunchAgents/**)`, `Edit(~/Library/Keychains/**)` |
| `permissions.deny` (other) | `Bash(git push --force:*)`, `Bash(git push -f:*)`, `Bash(git reset --hard origin:*)`, `Bash(rm -rf /:*)`, `WebFetch`, `WebSearch`, `Artifact`, `ArtifactComments`, `ArtifactData`, `PushNotification`, `RemoteTrigger`, `SendMessage`, three `mcp__claude_ai_*` servers |
| `permissions.allow` | `Bash(cd:*)`, `jq`, `tee`, `xargs`, `touch`, `chmod`, `which`, `basename`, `dirname`, `tr`, `cut` |
| `sandbox.excludedCommands` | absent (no entry) |

The fixture's merged `.claude/settings.json` carries the template `sandbox` block of `claude/settings.hooks.json` at `ced24b4`: the same `denyRead` list plus `~/.config/agents-broker` and `~/.claude.json`, and `denyWrite` = `./.agents`, `./.git/modules/.agents`, `./.env`.

| Difference from the 055 overlay (055 section 1) | 055 | This measurement |
| :--- | :--- | :--- |
| Settings source | `--settings <overlay file>` over the template | Project `.claude/settings.json` (relative `./` paths resolve against the project root, 055 section 1.3) |
| `allowUnsandboxedCommands` | `false` | `false` (same) |
| `network.allowedDomains` | `github.com`, `api.github.com`, `registry.npmjs.org` | `github.com`, `api.github.com`, `pypi.org`, `files.pythonhosted.org`; `registry.npmjs.org` is absent from the project file, yet `S-5d` returned HTTP 200 (a user-scope or default list is not read here; not attributed) |
| `denyRead` | `./.env`, `./.env.*` (template) | Adds `~/.config/gh`, `~/.docker/config.json`, `~/.npmrc`, `~/.ssh`, `~/.aws`, keychain, histories, `~/**/.env*` (ADR-0019 D8 additions) |
| `allowRead` | absent | `./.env.example`, `./.env.sample`, `./.env.template` |
| `denyWrite` | template | Nucleus: `./.env`, `./agents`, `./venv_skillopt`. Fixture: `./.agents`, `./.git/modules/.agents`, `./.env` |

Each configuration difference is a confound for a "changed" verdict between 2.1.119 and 2.1.311. The unsandboxed column (section 3) separates sandbox effects from host effects on 2.1.311; it does not separate the CLI version from the configuration, which needs a 2.1.119 run. No change is attributed to the CLI version alone.

## 2. Controls

| Control | Command | Sandboxed start / end | Unsandboxed start / end |
| :--- | :--- | :--- | :--- |
| `SBX0` | `printenv HTTPS_PROXY` (value never recorded) | exit 0 / exit 0 | exit 1 / exit 1 |
| `SBX1` | `curl -s --noproxy '*' -o /dev/null -m 10 https://registry.npmjs.org` | exit 6 / exit 6 | exit 0, HTTP 200 / exit 0, HTTP 200 |

Both columns are valid.

## 3. 055 matrix (section 2 cases)

"2.1.119" columns are copied from 055 section 2. A verdict compares 2.1.311 with 2.1.119; "sandbox effect" means the 2.1.311 sandboxed and unsandboxed outcomes differ.

| ID | Case | 2.1.119 unsandboxed / sandboxed (055) | 2.1.311 unsandboxed | 2.1.311 sandboxed | Signature (2.1.311 sandboxed) | Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `S-1` | Open `.claude/settings.local.json` for append, close | exit 0 / exit 1 | exit 0 | exit 1 | `PermissionError: [Errno 1] Operation not permitted` | unchanged; sandbox effect |
| `S-2a` | Open `.env.example` for read | exit 0 / exit 1 | nucleus: no fixture (exit 1, `FileNotFoundError`); `<fx>`: exit 0 | nucleus: no fixture; `<fx>` session A: opened | none | **changed**: `allowRead` now opens the template (`<fx>`); 055 predates the `allowRead` key, so the change is the configuration, not attributed to the CLI |
| `S-2b` | `git status --porcelain`, count of `Operation not permitted` lines | 0 / 0 | 0 | 0 | none | unchanged (still inconclusive: no tracked `.env*` file) |
| `S-3a` | Open `.env` | exit 0 / exit 1 | exit 0 | exit 1 | `PermissionError: [Errno 1] Operation not permitted: '.env'` | unchanged; sandbox effect |
| `S-3b` | `sh -c 'set -a; . ./.env'` | exit 0 / exit 1 | nucleus: not run (sourcing the real `.env` is a human step, `RA-09`); `<fx>`: exit 0 | exit 1 | `sh: ./.env: Operation not permitted` | unchanged; sandbox effect |
| `S-4a` | `os.stat('.env')` | exit 0 / exit 1 | exit 0 | exit 1 | `PermissionError: [Errno 1] Operation not permitted: '.env'` | unchanged; sandbox effect |
| `S-4b` | `venv_skillopt/bin/python -m graphify update .` | exit 0 / exit 0 | exit 0 | exit 0 | `graph.json and GRAPH_REPORT.md updated`; tip to set `GEMINI_API_KEY` | unchanged |
| `S-4c` | `pytest tests/test_merge_json.py` | exit 0, 9 passed / exit 4, `found no collectors` | exit 0, 34 passed | exit 0, 34 passed | none | **changed**: no sandbox effect on 2.1.311 (both columns collect); the test file grew from 9 to 34 tests and 055 used an overlay, so the cause is not isolated |
| `GKEY` | Count of 7 provider key variables set | 0 / 0 | 0 | 0 | `count=0` | unchanged |
| `S-5a` | `git ls-remote origin HEAD` | exit 0 / exit 0 | exit 0 | exit 0 | HEAD SHA returned | unchanged |
| `S-5b` | `git push --dry-run origin ai-sprint/060` (055: `ai-sprint/055`) | exit 0 / exit 0 | exit 0, `[new branch]` | exit 128 | `fatal: could not read Username for 'https://github.com': Device not configured` | **changed**: sandbox effect on 2.1.311 (the credential is reachable outside, not inside); `~/Library/Keychains/login.keychain-db` and `~/.config/gh` entered `denyRead` after 055 (ADR-0019 D8), so the configuration is the likely cause; not isolated |
| `S-5c` | `gh api rate_limit` | exit 0, 5000 / exit 1, `x509: OSStatus -26276` | exit 0, limit 5000 | exit 1 | `failed to read configuration: open ~/.config/gh/config.yml: operation not permitted` | **changed signature**: `gh` stops on the `~/.config/gh` read deny (ADR-0019 D8) before TLS; the `x509` signature is not reached, so neither confirmed nor refuted |
| `S-5d` | `curl` to `registry.npmjs.org` through the proxy | exit 0 / exit 0 | exit 0, HTTP 200 | exit 0, HTTP 200 | none | unchanged |
| `S-6a` | `pnpm store path` | `~/Library/pnpm/store/v11` / `<repo>/.pnpm-store/v11` | `~/Library/pnpm/store/v11` | `<repo>/.pnpm-store/v11` | none | unchanged (store relocates into the working tree under the sandbox) |
| `S-6b` | Write probe in the store directory | exit 0 / exit 1 | exit 0 | exit 1 | `No such file or directory`; `.pnpm-store` does not exist | unchanged (still inconclusive for `ERR_PNPM_STORE_DIR_OPEN_OPERATION_LOCK`) |
| `S-7a` | Playwright `chrome-headless-shell --dump-dom about:blank` | exit 0 / exit -5 | exit 0 | exit 133 (128 + SIGTRAP) | `FATAL mach_port_rendezvous_mac.cc:159 ... bootstrap_check_in ... Permission denied (1100)` | unchanged; sandbox effect |
| `S-7b` | Chrome for Testing headless, alive-after-6 s probe | `alive-after-6s` / exit 1 | exit 0, `alive-after-6s` | exit 1 (died) | `process_singleton_posix.cc:1043 Failed to create socket directory` | outcome unchanged; sandbox effect; signature changed (055 `CVDisplayLink` lines also appear unsandboxed on 2.1.311, so they are not causal) |
| `DOCK` | `docker info` | exit 0, server 29.7.2 / exit 1 | exit 0, server 29.7.2 | exit 1 | `permission denied ... unix:///var/run/docker.sock` | outcome unchanged; sandbox effect; socket path in the message differs from 055 (`~/.docker/run/docker.sock`); not isolated |
| `LOCAL` | Listen and connect on `127.0.0.1:8765` | HTTP 200 / exit 7 | exit 0, HTTP 200 | bind: exit 1, `PermissionError` at `socket.bind`; connect: exit 7 | as stated | unchanged; sandbox effect |
| `APPLE` | `osascript -e 'return 1'` | exit 0 / exit 0 | exit 0, `1` | exit 0, `1` | `1` | unchanged (cross-app `-600` case not exercised) |

## 4. 056 matrix on the current template (fixture session A)

056 sessions 1 to 3 measured the pre-`B2` base template, which the framework no longer ships; this section measures the template at `ced24b4` (`B2` and `R1` included), the state that `rules/project_topology.md` section 4 describes. "056 at current template" is the 2.1.119 result of the same case after `B2`/`R1` (056 sections 3.3, 5.2, 6.5, 6.8).

| Case | Target (built at runtime) | 056 at current template (2.1.119) | 2.1.311 | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| `R01` | `.agents/_mode.py` append | refused | `PermissionError` | unchanged |
| `R02` | `.agents/mcp_servers/` | refused | `FileNotFoundError`: the directory was retired (`f4a62e8`, H-007) | not measurable (target gone; entry point `E9` no longer exists) |
| `R03`..`R09` | `.agents/agents/`, `Makefile`, `agents.md`, `rules/`, `workflows/`, `config/`, `hooks/` | refused | `PermissionError` each | unchanged |
| `D02` | `.agents/.bridge_claude.lock` append | exit 1 | `PermissionError` | unchanged |
| `D09` | rename `.agents` | exit 1 | `PermissionError` | unchanged |
| `R10` | host-root `graphify/__init__.py` | creatable | created | unchanged; parent check: `-I` imports the venv copy, without `-I` the shadow; `.mcp.json` `graphify` args start `-I -m graphify.serve` (`E10` stays closed by `B3`) |
| `R11` | project `venv/bin/zz_probe` | writable | created | unchanged (`E15` open) |
| `N01` | `git -C .agents config core.fsmonitor ...` | exit 255, marker absent | exit 255 `could not lock config file ... Operation not permitted`; marker absent; value absent when read unsandboxed | unchanged |
| `N02`..`N04` | gitdir `config`, `hooks/`, `info/attributes` | `PermissionError` | `PermissionError` each | unchanged |
| `N04b` | gitdir `commondir` (new case) | not probed | `PermissionError` | new: `R1` covers the `commondir` vector of 056 section 6.4 |
| `M04`, `M05`, `M06` | host `.git/hooks/`, host `.git/config`, `~/.gitconfig` | `PermissionError` | `PermissionError` each | unchanged |
| `P01`..`P07` | `.mcp.json`, `.claude/settings.json`, `.claude/settings.local.json`, new and existing `.claude/agents/*.md`, `~/.claude/` new file and `settings.json` | `PermissionError` | `PermissionError` each | unchanged |
| `P08` | new file directly under `.claude/` | created | created | unchanged |
| `Q01`, `Q02` | `.claude/commands/`, `.claude/skills/zz/` | `PermissionError` | `PermissionError` | unchanged |
| `Q03` | `.claude/hooks/zz.py` | created | `PermissionError` | **changed**: the template `denyWrite` names neither path, so the refusal is not a template write rule; attribution to the CLI version is not isolated |
| `Q04` | `.claude/rules/zz.md` | created | created | unchanged (`E16` open) |
| `Q05` | `.claude/settings.zz.json` | created | `PermissionError` | **changed**, as `Q03` |
| `Q06` | append-open host `CLAUDE.md` | opened | opened | unchanged (`E16` open) |
| `N05` / `D07` | `session_start.py --boot --tool claude-code` | exit 0 | exit 0; advisory `[sync_agents_pin] ping failed (... FETCH_HEAD: Operation not permitted)` | unchanged outcome; the advisory comes from `sync_agents_pin.py`, which postdates 056 |
| `N06`..`N08` | `git status --porcelain`, `git -C .agents status --porcelain`, `git submodule status` | exit 0 | exit 0; submodule status empty | unchanged |
| `N09` / `R13` | agent `git commit --allow-empty -m "chore(probe): measure sandbox #060"` | exit 0, hooks passed | exit 0 | unchanged |
| `N10` | `git push origin HEAD:refs/heads/probe` (local bare) | exit 0 | exit 0 | unchanged |
| `N11` | `git -C .agents fetch origin` | exit 255 | exit 255, `cannot open ... FETCH_HEAD: Operation not permitted` | unchanged |
| `L01`, `L02` | lock set to `HEAD~1` before the session; read after it | lock refreshed to HEAD by the unsandboxed `SessionStart` hook | lock = `ced24b4` = `.agents` HEAD after the session | unchanged |
| `S-3a`, `S-4a` | open and `stat` `.env` (control) | `PermissionError` | `PermissionError` | unchanged |
| `gh` | `gh api rate_limit` | not in 056 | exit 1, `~/.config/gh` read deny | as `S-5c` |

### 4.1 Parent checks, unsandboxed

| 056 id | Setup | 2.1.119 | 2.1.311 | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| 6.4 `commondir` | `commondir` in `.git/modules/.agents/` pointing at a copy of the gitdir whose `config` sets `core.fsmonitor` | fsmonitor executed | `git -C .agents status` exit 0; marker created | unchanged (the class is the whole gitdir; a first attempt with a `commondir` lacking objects and refs exited 128 and is void) |
| `B5` | `.claude/settings.local.json` with `excludedCommands: ["gh run list *"]`, then `install.py --target claude` | exit 2, names the entry | exit 2, `Install refused: the host's Claude Code settings carry sandbox.excludedCommands entries.`, names the entry | unchanged |
| `B9` | fixture `Measuring CLI` row at 2.1.119, CLI 2.1.311 | advisory names both matrices | `_cli_version_notes` returns `Claude Code 2.1.311 is not the measuring CLI 2.1.119 ... re-measure` both matrices (called directly; the nucleus boot of this session stopped at the session lock before the advisory step) | unchanged |

### 4.2 Rows of 056 not probed individually

| 056 case | Why |
| :--- | :--- |
| `W03` `.agents/scripts/`, `W05` `.agents/venv_skillopt/`, `W23`/`W24` `.agents/claude/` | Same `./.agents` `denyWrite` as `R01`..`R09` and `D09`; not probed per path |
| `D01`..`D08` with the session-2 local `allowWrite` | `allowWrite` of the lock is not in the template; `D02` covers the lock under the shipped template |
| `W26` / `M08` import shadowing and fsmonitor execution through a commit | Preconditions (`W01`, `M01`) are refused on the current template (`R01`, `N01`), so the chain cannot start |

## 5. 055 sections 4 and 9 (fixture sessions B to E)

| Session | `.claude/settings.local.json` `sandbox` | Case | 2.1.119 (055) | 2.1.311 | Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- |
| B | `allowUnsandboxedCommands: false`, `allowMachLookup: true` | `SBX0`, `SBX1`, `S-7a`, `S-3a` | sandbox did not start (`SBX0` exit 1, `SBX1` HTTP 200); Chromium launched; `.env` readable | `SBX0` exit 0, `SBX1` exit 6; `S-7a` exit -5, `bootstrap_check_in` fatal; `.env` `PermissionError` | **changed**: the boolean no longer fails open; it still does not make Chromium launch |
| C | as B, `allowMachLookup: ["org.chromium.*"]` | same | sandbox active; `S-7a` exit -5, same error | sandbox active; `S-7a` exit -5, same error | unchanged |
| D | `allowUnsandboxedCommands: false`, `excludedCommands: ["gh run list *"]` | `gh run list x; python3 -c "<multi-line probe>"` | 055 `A3`: chained command ran unsandboxed and read `.env` (single-line) | `gh` and the chained probe sandboxed: `P 1`, `.env` `PermissionError` | not comparable: the command text spanned several lines; the entry did not match it |
| E | `allowUnsandboxedCommands: false`, `excludedCommands: ["python3 zz_env.py", "gh run list *"]` | `E1` `python3 zz_env.py` | not in 055 | `P 0`, `ENV 34` (outside the sandbox, `.env` read) | an exact entry runs its command unsandboxed |
| E | same | `E2` `python3 zz_env.py; python3 -c "<one line>"` | not in 055 | `P 1`, `ENV PermissionError`, `CHAIN P 1` | an exact entry does not match a compound command: all of it ran sandboxed |
| E | same | `E3` `gh run list x; python3 zz_env.py` | 055 `A3`: escape | `gh` usage error, then `P 0`, `ENV 34` | **unchanged**: a wildcard entry matches the single-line compound and the chained command runs outside the sandbox and reads `.env` |

## 6. Rows of `rules/project_topology.md` section 4 affected (input for H-02)

List only; the file is not edited by H-01. Rows are named by their first cell.

| Row | Evidence | Amendment input |
| :--- | :--- | :--- |
| `Measuring CLI` | sections 3 to 5 | The 055 and 056 matrices are measured on 2.1.311; rows measured only in Sprint 059 cite 2.1.319 and 2.1.322 (`KI-059-31`), higher than the installed 2.1.311, and are outside H-01 (section 7) |
| Walkers of the full tree: `pytest`, `stat()` of `.env` (`S-4`) | `S-4c`, `S-4a` | `pytest tests/test_merge_json.py` no longer exits 4 under the sandbox (exit 0 in both columns); the `stat()` deny is unchanged |
| `gh` (Go TLS) (`S-5`) | `S-5c` | Under the shipped template `gh` stops on the `~/.config/gh` read deny before TLS; `x509` is not reached on 2.1.311 |
| `git ls-remote`, `git push`, `curl` over HTTPS (`S-5`) | `S-5b` | `git push` fails under the sandbox for lack of a credential (exit 128) and succeeds outside it; `ls-remote` and `curl` unchanged |
| Chromium, Playwright, Chrome for Testing (`S-7`) | `S-7a`, `S-7b` | Sandbox effect confirmed by the unsandboxed column; the `S-7b` signature is `ProcessSingleton`, not `CVDisplayLink` |
| `docker`, `docker compose` | `DOCK` | Socket path in the message is `/var/run/docker.sock` |
| Read `.env.example`, `.env.sample`, `.env.template` (`S-2`) | `S-2a` (`<fx>`) | `allowRead` opens `.env.example` under the sandbox |
| `allowMachLookup` | section 5, B and C | On 2.1.311 the boolean keeps the sandbox active and Chromium still fails; neither form makes Chromium launch |
| Excluded commands | section 5, E | Unchanged: a wildcard entry lets a single-line chained command escape and read `.env`; `B5` still refuses entries at install |
| Hooks and what they execute (`N3`) | section 4 `R01`..`R09`, `N01`..`N04b`, `L02`, 4.1 | Unchanged; `commondir` is now probed and refused under `R1` |
| `.claude/` paths | `Q03`, `Q05` | `.claude/hooks/` and `.claude/settings.zz.json` are refused on 2.1.311 (created on 2.1.119); `.claude/rules/`, a file directly under `.claude/` and host `CLAUDE.md` stay writable |
| Unchanged (no amendment input) | `S-1`, `S-2b`, `S-3a`, `S-3b`, `S-4b`, `GKEY`, `S-5a`, `S-5d`, `S-6a`, `S-6b`, `LOCAL`, `APPLE`; 056 cases marked unchanged in section 4 | Same exit and signature class |

## 7. Not measured

| Item | Reason |
| :--- | :--- |
| A 2.1.119 run on the current configuration | Needed to attribute any "changed" verdict to the CLI version alone; that CLI is not installed |
| 056 sessions 1 to 3 at the pre-`B2` base template | That template is not shipped; section 4 measures the shipped one |
| 055 sections 6 to 8 (`with_env.py` exclusions, rendered absolute exclusions) | `install.py` no longer renders exclusions and prunes rendered ones (`scripts/install.py:31`, `RENDER_OWNED_RE` line 64); the exclusion class itself is measured in section 5 |
| Rows measured in Sprint 059 (`docs/sprints/059-core-pipeline/SANDBOX_ENUMERATION.md`, including case `G` `enableWeakerNetworkIsolation`) | Outside the H-01 row (055 and 056 matrices) |
| `S-3b` in the nucleus, unsandboxed | Sourcing the real `.env` is a human step (`RA-09`); measured on the fixture instead |
| Cross-app Apple Event (`-600`) | Not exercised in 055 either |

No claim is made for any item in this section.
