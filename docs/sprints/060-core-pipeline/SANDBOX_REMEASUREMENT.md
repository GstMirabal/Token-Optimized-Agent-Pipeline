# Sprint 060 H-01 - Sandbox Re-measurement (sandboxed column)

Re-run of the sandboxed column of `docs/sprints/055-core-pipeline/SANDBOX_MEASUREMENT.md` section 2 on Claude Code 2.1.311. Paths are genericized (`RA-15`): `~` is the home directory, `<repo>` is the nucleus working tree. No `.env*` file was read, created, modified or deleted (`RA-09`).

| Field | Value |
| :--- | :--- |
| Unit | `H-01` (`task_scope.md`, plan row `H-01`) |
| Finding | `KI-059-31` |
| Date | 2026-11-22 |
| CLI | Claude Code 2.1.311 (`claude --version`); the 055 matrix measured 2.1.119 |
| Platform | macOS, Seatbelt |
| Status | Partial: sandboxed column of the 055 matrix only; the 055 unsandboxed control column and the 056 matrix are not measured in this session (outside-sandbox steps, human or unsandboxed session required) |

## 1. Method

| Item | Fact |
| :--- | :--- |
| Runner | One `timeout 90` subprocess per case from the repository root, through a scratch wrapper that records the exit code and the last three output lines with `~` and `<repo>` redacted. The wrapper is not committed. |
| Session type | The agent's own Bash tool, inside this session's Seatbelt sandbox. It is not a headless `claude -p --settings <overlay>` run as in 055 section 1. |
| Settings in effect | The nucleus project settings `.claude/settings.json`, as merged for this working tree (not an overlay file). No user-scope file was read. |
| Fixtures | None created. The nucleus holds a `.env` (never read) and no `.env.example`, `.env.sample` or `.env.template`. |
| Safety constraints applied | `S-1` open for append, close, no write. `S-5b` `git push --dry-run` only. `S-5c` one `gh api rate_limit`. `.env` probed only with `open().close()`, `os.stat()` and `sh -c 'set -a; . ./.env'` (exit and errno text recorded). Nothing installed; `install.py` not run; nothing committed. |
| Probe variations | `LOCAL` was run twice (bind attempt and connect-only) because the 055 listener setup is not recorded. `S-7a` was run with and without extra flags. `S-7b` used a probe written in this session (055 does not record its flags). Each is stated in section 3. |

### 1.1 Sandbox configuration in effect

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

| Difference from the 055 overlay (055 section 1) | 055 | This session |
| :--- | :--- | :--- |
| Settings source | `--settings <overlay file>` over the template | Project `.claude/settings.json` (relative `./` paths resolve against the project root, 055 section 1.3, so no absolute deny paths were needed) |
| `allowUnsandboxedCommands` | `false` | `false` (same) |
| `network.allowedDomains` | `github.com`, `api.github.com`, `registry.npmjs.org` | `github.com`, `api.github.com`, `pypi.org`, `files.pythonhosted.org`; `registry.npmjs.org` is absent from the project file, yet `S-5d` returned HTTP 200 (a user-scope or default list is not read here; not attributed) |
| `denyRead` | `./.env`, `./.env.*` (template) | Adds `~/.config/gh`, `~/.docker/config.json`, `~/.npmrc`, `~/.ssh`, `~/.aws`, keychain, histories, `~/**/.env*` (ADR-0019 D8 additions) |
| `denyWrite` | template | `./.env`, `./agents`, `./venv_skillopt` (the template names `./.agents` and the gitdir; this working tree is the nucleus) |
| `allowRead` | template names | `./.env.example`, `./.env.sample`, `./.env.template` (same intent; the 055 `S-2a` run predates it) |
| Extra | none | `credentials.files`, `env` keys; the session's own sandbox adds the denies listed by the harness |

Each configuration difference is a confound for the "changed" verdicts in section 3: a result that changed may come from the CLI version, from the configuration, or from the host state. This session cannot exclude any of the three: that needs the unsandboxed control column or a 2.1.119 run.

## 2. Controls

| Control | Command | Start | End | Valid when |
| :--- | :--- | :--- | :--- | :--- |
| `SBX0` | `printenv HTTPS_PROXY` (value never recorded) | exit 0 | exit 0 | 0 |
| `SBX1` | `curl -s --noproxy '*' -o /dev/null -m 10 https://registry.npmjs.org` | exit 6 | exit 6 | 6 |

The run is valid (`SBX0` = 0 and `SBX1` = 6 at both ends).

## 3. Results

"Result 2.1.119" is copied from 055 section 2. Verdict `changed` compares the sandboxed outcome (exit and signature class); `unchanged` means the same exit and the same signature class. No attribution to the CLI version is claimed.

| ID | Case | 2.1.119 sandboxed (055) | 2.1.311 sandboxed | Signature (2.1.311) | Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `S-1` | Open `.claude/settings.local.json` for append, close | exit 1 | exit 1 | `PermissionError: [Errno 1] Operation not permitted` | unchanged |
| `S-2a` | Open `.env.example` for read | exit 1, `Operation not permitted` | exit 1 | `FileNotFoundError: [Errno 2] No such file or directory: '.env.example'` | **not measurable: no fixture** (`.env.example` does not exist and creating a `.env*` name is barred by `RA-09`; the template `allowRead` effect is untested) |
| `S-2b` | `git status --porcelain`, count of `Operation not permitted` lines | 0 lines | 0 lines (2 tracked modifications listed, unrelated) | none | unchanged (still inconclusive: no tracked `.env*` file) |
| `S-3a` | Open `.env` | exit 1 | exit 1 | `PermissionError: [Errno 1] Operation not permitted: '.env'` | unchanged |
| `S-3b` | `sh -c 'set -a; . ./.env'` | exit 1 | exit 1 | `sh: ./.env: Operation not permitted` | unchanged |
| `S-4a` | `os.stat('.env')` | exit 1 | exit 1 | `PermissionError: [Errno 1] Operation not permitted: '.env'` | unchanged |
| `S-4b` | `venv_skillopt/bin/python -m graphify update .` | exit 0, version warning | exit 0 | `graph.json and GRAPH_REPORT.md updated`; tip to set `GEMINI_API_KEY` | unchanged (`graphify-out` is git-ignored; no tracked change) |
| `S-4c` | `pytest tests/test_merge_json.py` | exit 4, `found no collectors for <repo>/tests/test_merge_json.py` (9 tests unsandboxed) | exit 0 | `34 passed in 0.02s` | **changed** (explicit path now collects under the sandbox; the file now holds 34 tests, not 9, so the case is not identical to 055; run with `venv_skillopt/bin/python -m pytest -q`) |
| `GKEY` | Count of 7 provider key variables set (`rules/graphify.md` list) | 0 | 0 | `count=0` | unchanged |
| `S-5a` | `git ls-remote origin HEAD` | exit 0, SHA | exit 0 | HEAD SHA returned | unchanged |
| `S-5b` | `git push --dry-run origin ai-sprint/060` (dry-run only; 055 used `ai-sprint/055`) | exit 0, `[new branch]` line | exit 128 | `fatal: could not read Username for 'https://github.com': Device not configured` | **changed** (no credential is available to git in this session; `~/Library/Keychains/login.keychain-db` and `~/.config/gh` are in `denyRead`; cause not isolated) |
| `S-5c` | `gh api rate_limit` (one call) | exit 1, `tls: failed to verify certificate: x509: OSStatus -26276` | exit 1 | `failed to read configuration: open ~/.config/gh/config.yml: operation not permitted` (also `warning: failed to load config`) | **changed** (signature: `gh` stops on the `~/.config/gh` read deny before reaching TLS, as `project_topology.md` already predicts via ADR-0019 D8; the 055 `x509` signature was not reached, so it is neither confirmed nor refuted) |
| `S-5d` | `curl` to `registry.npmjs.org` through the proxy | exit 0, HTTP 200 | exit 0 | `HTTP 200` | unchanged |
| `S-6a` | `pnpm store path` | `<repo>/.pnpm-store/v11` | exit 0 | `<repo>/.pnpm-store/v11` | unchanged |
| `S-6b` | `touch .pnpm-store/v11/.sbx060_probe` | exit 1, `No such file or directory` | exit 1 | `touch: .pnpm-store/v11/.sbx060_probe: No such file or directory`; `.pnpm-store` does not exist | unchanged (still inconclusive for `ERR_PNPM_STORE_DIR_OPEN_OPERATION_LOCK`) |
| `S-7a` | Playwright `chrome-headless-shell --dump-dom about:blank` (run plain, and with `--no-sandbox --disable-gpu`) | exit -5 (SIGTRAP), `bootstrap_check_in ... Permission denied (1100)` | exit 133 (128 + SIGTRAP 5), both runs | `FATAL mach_port_rendezvous_mac.cc:159 ... bootstrap_check_in org.chromium.Chromium.MachPortRendezvousServer.<pid>: Permission denied (1100)` | unchanged |
| `S-7b` | Chrome for Testing headless, alive-after-6 s probe (`--headless=new --disable-gpu`, own profile dir, two runs) | exit 1 (process died), `CVDisplayLinkCreateWithCGDisplay failed` | exit 1 (process died, `rc=21`) | `ERROR:chrome/browser/process_singleton_posix.cc:1043 Failed to create socket directory` and `Failed to create a ProcessSingleton for your profile directory` | outcome unchanged (died); **signature changed** and the cause is not attributed (the profile directory I chose may confound; no unsandboxed control exists here; the 055 `CVDisplayLink` line did not appear in the tail) |
| `DOCK` | `docker info` | exit 1, `permission denied ... unix://~/.docker/run/docker.sock` | exit 1 | `permission denied while trying to connect to the docker API at unix:///var/run/docker.sock` | outcome unchanged; socket path in the message changed (`/var/run/docker.sock`, not `~/.docker/run/docker.sock`; a docker context or Docker Desktop setting, not the CLI, may explain it; not isolated) |
| `LOCAL` | Listen and connect on `127.0.0.1:8765` | exit 7, `curl: (7) Failed to connect` | bind attempt: exit 1, `PermissionError: [Errno 1] Operation not permitted` at `socket.bind`; connect-only `curl`: exit 7, `HTTP 000` | as stated | unchanged outcome (binding blocked; the bind failure itself is now directly observed) |
| `APPLE` | `osascript -e 'return 1'` | exit 0, `1` | exit 0 | `1` | unchanged (cross-app Apple Event `-600` case still not exercised) |

### 3.1 Other sandboxed ids in 055

| ID (055 section) | Why not re-run here |
| :--- | :--- |
| Section 4 `allowMachLookup` variants | Each needs a settings overlay passed with `--settings` to a fresh `claude -p` session; this session cannot start one (`Not logged in`; `api.anthropic.com` blocked). The prohibition on the key stays on the 2.1.119 measurement. |
| Section 6 `A2-0`..`A2-5` (`with_env.py` probe) | Needs a host fixture, a copied wrapper, an `excludedCommands` entry and a headless session. Not run. |
| Section 7 `H-*`, `N-*` (U25) | Host fixtures plus headless sessions. Not run. |
| Section 8 `R1`..`R9` | Needs `install.py` run outside the sandbox. Not run. |
| Section 9 `A1`..`D1` | Needs `install.py` run outside the sandbox and a headless session. Not run. |

## 4. Rows of `rules/project_topology.md` section 4 affected (input for H-02)

List only; the file is not edited here. Rows are named by their first cell. "Candidate" means a measured result in section 3 differs from what the row states; the row still needs the matching unmeasured column before it can be amended.

| Row | Section 3 id | Reason it is a candidate | Gap before amending |
| :--- | :--- | :--- | :--- |
| `Measuring CLI` | all | States 2.1.119; this session ran 2.1.311 on a partial matrix | Do not change to 2.1.311 until the unsandboxed column and the 056 matrix are measured |
| Walkers of the full tree: `pytest`, `stat()` of `.env` (`S-4`) | `S-4c` | Row states `pytest tests/test_merge_json.py` exits 4 `found no collectors`; now exit 0 with explicit paths | Unsandboxed control not run; the test file changed (9 to 34 tests) |
| `gh` (Go TLS) (`S-5`) | `S-5c` | Row states `x509: OSStatus -26276`; this session saw the `~/.config/gh` read denial first | `x509` is untested on this configuration; the unsandboxed column and a `gh` run without the `~/.config/gh` deny are needed |
| `git ls-remote`, `git push`, `curl` over HTTPS (`S-5`) | `S-5b` | Row says `None` when the domain is allowed; `git push --dry-run` exited 128 for lack of a credential | The 055 `S-5b` ran with credentials present; whether it needs a credential outside the sandbox is not measured here |
| Chromium, Playwright, Chrome for Testing (`S-7`) | `S-7b` | The row cites the `S-7a` signature, which is unchanged; the `S-7b` signature differed | Attribution of the `ProcessSingleton` error |
| `docker`, `docker compose` | `DOCK` | Socket path in the message is `/var/run/docker.sock`, not `<home>/.docker/run/docker.sock` | Docker context or install state |
| Read `.env.example`, `.env.sample`, `.env.template` (`S-2`) | `S-2a` | Not measurable here (no fixture); the row asserts `allowRead` works | A fixture file created by the human or a host session |
| Unchanged in this session (no amendment input) | `S-1`, `S-2b`, `S-3a`, `S-3b`, `S-4a`, `S-4b`, `GKEY`, `S-5a`, `S-5d`, `S-6a`, `S-6b`, `S-7a`, `LOCAL`, `APPLE` | Same exit and signature class on the sandboxed column | The row's unsandboxed or 056 evidence remains unre-measured |

Rows with no section 3 case (`After a sandboxed agent session`, `Excluded commands`, `allowMachLookup`, template paths, hooks `N3`, `git pull`/`checkout` rewriting settings, `graphify update` with 20 or more uncached files, `jest`, `scripts/*.py` derived `gh` rows) were not exercised.

## 5. Not measured in this session

| Item | What it covers | Step needed outside the sandbox |
| :--- | :--- | :--- |
| 055 unsandboxed control column | `S-1` ... `APPLE` without a sandbox, to separate version effects from sandbox effects | The human runs the same commands in their own shell (no `HTTPS_PROXY`; `SBX0` exit 1, `SBX1` exit 0 and HTTP 200) |
| 056 sessions 1-3 (`W01`..`W27`, `D01`..`D09`, `L01`..`L02`, section 3 enumeration `E1`..`E17`) | Write probes and the `denyWrite ./.agents` design probe | A scratch host fixture, `python3 .agents/scripts/install.py --target claude` run unsandboxed, then headless `claude -p` sessions with the same settings |
| 056 section 5 (session 4, `B5`, `B9`) | Re-measurement after B2, B3, B5, B9; `B5` and `B9` were measured unsandboxed | Fixture plus install outside the sandbox; the `B5`, `B9` cases run unsandboxed |
| 056 section 6 (sessions 5-7, `E13`, gitdir `commondir` check, `M04`, `M05`) | Git-mediated writes to `.git/modules/.agents` | Fixture, install outside the sandbox, headless sessions; the `commondir` check ran unsandboxed |
| 056 section 6.8 (sessions 8-9) | By-operation re-measurement of the approval-gated rows (`.mcp.json`, `.claude/*`, `~/.claude`) | Fixture, install outside the sandbox, headless sessions |
| 056 section 2.6 / 6.9 case `G` | `gh` with `enableWeakerNetworkIsolation` | Headless session with that key set; a human-chosen configuration (ADR-0019 D2) |
| 055 sections 4, 6-9 | `allowMachLookup`, `with_env.py` probe, U25 and install renders | As listed in 3.1 |

No claim is made for any item in this section.
