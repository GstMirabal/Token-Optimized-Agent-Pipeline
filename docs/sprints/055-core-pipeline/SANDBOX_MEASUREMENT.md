# Sprint 055 U01 - Sandbox Measurement

Measured effect of the template sandbox configuration (`claude/settings.hooks.json`) against the host-reported restrictions `S-1`..`S-7` (`docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` `F-115-N2`). Inputs for plan Design `D1`..`D9` (`IMPLEMENTATION_PLAN.md`). All paths are genericized (`RA-15`): `~` is the home directory, `<repo>` is the nucleus working tree.

## 1. Method

| Item | Fact |
| :--- | :--- |
| Runner | A Python matrix runner: one subprocess per case, 90 s timeout, records the exit code and the last stderr lines, redacts the fixture value. |
| Fixtures | `.env` containing `GEMINI_API_KEY=<fixture, not a secret>` and an untracked `.env.example`. Both were created for the run and removed afterwards. |
| Session type | Headless `claude -p --settings <overlay>`, launched by the principal agent. |
| Platform | Claude Code CLI 2.1.119, macOS (Seatbelt). |
| Overlay content | Template `claude/settings.hooks.json` plus `allowUnsandboxedCommands: false` (no unsandboxed retry) and `network.allowedDomains: [github.com, api.github.com, registry.npmjs.org]`. |
| Why the domain list | It replaces the interactive domain prompts and matches the host `S-5` condition "domain allowed". |
| Raw evidence | `.u01_raw_{unsandboxed,sandboxed,control,mlarray,machlookup_invalid}.txt` (tab-separated ID, exit, signature, command). Not committed. |

### 1.1 Deviation from plan D1

| Plan `D1` | Executed | Reason |
| :--- | :--- | :--- |
| Human-launched interactive session | Headless `claude -p` launched by the principal agent | An agent's Bash tool has no TTY, so an interactive `claude` cannot be launched from it. The human attempted it and received `Input must be provided either through stdin or as a prompt argument when using --print`. |

### 1.2 Run labels

| Label | Raw file | Configuration |
| :--- | :--- | :--- |
| Unsandboxed control | `.u01_raw_unsandboxed.txt` | No sandbox in effect. |
| Sandboxed (template) | `.u01_raw_sandboxed.txt`, `.u01_raw_control.txt`, `.u01_raw_mlarray.txt` | Template overlay with absolute deny paths. Three runs, same results for every case except where noted in section 3. |
| `allowMachLookup: true` | `.u01_raw_machlookup_invalid.txt` | Template overlay plus the boolean key. Sandbox did not start (section 4). |

### 1.3 Path-resolution finding (new, framework-class)

| Aspect | Fact |
| :--- | :--- |
| Observation | `./`-relative `denyRead` paths resolve against the directory of the settings file that declares them. With `--settings <file elsewhere>`, `./.env` did not protect the repository `.env`: the first sandboxed run opened `.env` with exit 0. |
| Documentation | States that `.` resolves to the project root only when the configuration lives in project settings. |
| Measurement choice | Absolute deny paths were used to emulate a host where the template is merged into `<host>/.claude/settings.json`. |
| Consequence | The template is correct only when merged into project settings. A `--settings` use of the template file protects nothing. |
| Routing | Framework-class (`agents.md §4 feedback_upstream`). |

### 1.4 Sandbox-active controls

| Control | Command intent | Unsandboxed | Sandboxed (every valid run) |
| :--- | :--- | :--- | :--- |
| `SBX0` | `HTTPS_PROXY` present in the environment | exit 1 | exit 0 |
| `SBX1` | `curl --noproxy '*'` to `registry.npmjs.org` | exit 0, HTTP 200 | exit 6, `Could not resolve host` |

A run is valid only when `SBX0` = 0 and `SBX1` = 6.

## 2. Results

Sandboxed column is identical across the three valid runs unless stated. "Reproduced" means the sandbox produces the failure the host reported.

| ID | Case | Unsandboxed control | Sandboxed (template) | Signature | Verdict vs host report |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `S-1` | Open `.claude/settings.local.json` for append | exit 0 | exit 1 | `PermissionError: [Errno 1] Operation not permitted` | Reproduced (protected path). |
| `S-2a` | Open `.env.example` for read | exit 0 | exit 1 | `[Errno 1] Operation not permitted` under the `./.env.*` deny | Reproduced. |
| `S-2b` | `git status --porcelain` noise (count of `Operation not permitted` lines) | 0 lines | 0 lines | none | Not reproduced in this form. The fixture is untracked and the host case is a tracked file: inconclusive, not refuted. |
| `S-3a` | Open `.env` | exit 0 | exit 1 | `[Errno 1] Operation not permitted` | Reproduced. |
| `S-3b` | `sh -c 'set -a; . ./.env'` (the `RA-09` prescribed mechanism) | exit 0 | exit 1 | `sh: ./.env: Operation not permitted` | Reproduced: the prescribed mechanism is blocked. |
| `S-4a` | `os.stat('.env')` | exit 0 | exit 1 | `[Errno 1] Operation not permitted` | Reproduced. |
| `S-4b` | `python -m graphify update .` | exit 0 | exit 0 | version warning only | Not reproduced in the nucleus: graphify `detect.py` skips names `.env`. Inconclusive for hosts with other `.env*` names. |
| `S-4c` | `pytest tests/test_merge_json.py` | exit 0, 9 passed | exit 4 | `ERROR: found no collectors for <repo>/tests/test_merge_json.py` | Reproduced with a different signature from the host `PermissionError`. |
| `GKEY` | Count of LLM key variables visible in the environment (7 names) | 0 | 0 | none | Confirms the graphify cause (section 3.1). |
| `S-5a` | `git ls-remote origin HEAD` | exit 0 | exit 0 | HEAD sha returned | Host report refuted for git read. |
| `S-5b` | `git push --dry-run origin ai-sprint/055` | exit 0 | exit 0 | `[new branch] ai-sprint/055 -> ai-sprint/055` | Host report refuted for git push. |
| `S-5c` | `gh api rate_limit` | exit 0, limit 5000 | exit 1 | `tls: failed to verify certificate: x509: OSStatus -26276` | Reproduced for Go-based `gh` (matches the documented Go-TLS-under-Seatbelt issue). |
| `S-5d` | `curl` to `registry.npmjs.org` through the proxy | exit 0, HTTP 200 | exit 0, HTTP 200 | none | Refuted for curl. |
| `S-6a` | `pnpm store path` | `~/Library/pnpm/store/v11` | `<repo>/.pnpm-store/v11` | store relocates into the working tree | New observation. |
| `S-6b` | Write probe in the store directory | exit 0 | exit 1 | `touch: <repo>/.pnpm-store/v11/.sbx055_probe: No such file or directory` | The relocated directory does not exist. Host `ERR_PNPM_STORE_DIR_OPEN_OPERATION_LOCK` not reproduced (no pnpm project in the nucleus): inconclusive. |
| `S-7a` | Playwright chromium headless shell `--dump-dom about:blank` | exit 0, DOM printed | exit -5 (SIGTRAP) | `FATAL mach_port_rendezvous_mac.cc:159 ... bootstrap_check_in org.chromium.Chromium.MachPortRendezvousServer.<pid>: Permission denied (1100)` | Reproduced. |
| `S-7b` | Chrome for Testing headless, alive-after-6 s probe | exit 0, `alive-after-6s` | exit 1 (process died) | `CVDisplayLinkCreateWithCGDisplay failed` lines in stderr (also present in the unsandboxed control, so not causal) | Reproduced: exit 1 in all three sandboxed runs instead of staying alive. |
| `DOCK` | `docker info` | exit 0, server 29.7.2 | exit 1 | `permission denied while trying to connect to the docker API at unix://~/.docker/run/docker.sock` | Incompatible (documented). |
| `LOCAL` | Listen and connect on `127.0.0.1:8765` | exit 0, HTTP 200 | exit 7 | `curl: (7) Failed to connect to 127.0.0.1 port 8765` | Binding blocked (documented `allowLocalBinding`). |
| `APPLE` | `osascript -e 'return 1'` | exit 0 | exit 0 | `1` | No cross-app Apple Event exercised; the `-600` case was not exercised. |

## 3. Interpretation

### 3.1 graphify and the key variable

| Fact | Evidence |
| :--- | :--- |
| LLM key variables visible: 0 in both modes | `GKEY` |
| graphify reads only `os.environ` (7 names) | Source read during the sprint. |
| A key that lives only in `.env` is invisible to graphify, and the sandbox denies `.env` | `GKEY` plus `S-3a`, `S-3b` |
| Conclusion | The cause of the human-reported graphify symptom is confirmed. |

### 3.2 Reproduction scorecard

| Verdict | Cases |
| :--- | :--- |
| Reproduced | `S-1`, `S-2a`, `S-3a`, `S-3b`, `S-4a`, `S-4c`, `S-5c`, `S-7a`, `S-7b`, `DOCK`, `LOCAL` |
| Refuted | `S-5a`, `S-5b`, `S-5d` |
| Inconclusive | `S-2b`, `S-4b`, `S-6b` (host symptom) |
| New observation | `S-6a` store relocation; template path resolution (section 1.3) |
| Not exercised | `APPLE` `-600` case |

## 4. allowMachLookup (plan D6)

| Variant | Sandbox state | `S-7a` Chromium | Other effects | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| Boolean `allowMachLookup: true` (documented form) on CLI 2.1.119 | Did not start: `SBX0` exit 1, `SBX1` HTTP 200 | Launched, DOM printed | `.env` readable, `docker info` exit 0, `LOCAL` HTTP 200. Commands ran unsandboxed despite `allowUnsandboxedCommands: false`, with no warning. | Fails open. |
| Isolation probe: unknown key `sbx055BogusKey: true` | Sandbox stayed active | not applicable | none | The failure is caused by this key and value specifically. |
| List form `["org.chromium.*"]` (`.u01_raw_mlarray.txt`) | Sandbox stayed active | Same `bootstrap_check_in` error, exit -5 | none | `bootstrap_check_in` registers a service; lookup permission does not cover it. |
| Result | | | | `D6` Branch B: no sandbox-side form makes Chromium launch. |

## 5. Sanctioned-form input for U07/U09/U10

Status of every row: **proposal**, not a decision. Form numbers refer to plan `D7`: (1) `allowWrite` / `allowedDomains`; (2) narrow `excludedCommands`; (3) human opt-in in user settings; (4) human-run.

| Case | Proposed `D7` form | Proposed action | Basis |
| :--- | :--- | :--- | :--- |
| `S-1` (`.claude/settings.local.json`) | (4) human-run | The human runs `bash .agents/scripts/install.sh --target claude`. The agent never writes the protected path. | Protected path denied by design. |
| `S-2` (`.env.example`) | (1) path scoping | Narrow `denyRead` so it excludes templates, and add `allowRead` for `.env.example` and `.env.sample`. | `S-2a` blocked by `./.env.*`. |
| `S-3` and graphify key | (2) narrow `excludedCommands` | Add `scripts/with_env.py` to `excludedCommands` (plan `D2`) so the key is loaded outside the sandbox and exported to the child. | `S-3b`, `GKEY`. |
| `S-4` (pytest needing a tree walk) | Document | Document the `found no collectors` signature and the cause. No config change proposed. | `S-4c`. |
| `S-5c` (`gh`) | (2) narrow `excludedCommands` | One entry per invocation pattern (`gh api *`, `gh pr *`, and so on); never bare `gh *` unless a pattern list cannot cover the use. | `S-5c`; git and curl need nothing (`S-5a`, `S-5b`, `S-5d`). |
| `S-6` (pnpm store) | (1) `allowWrite` plus document | Document the relocation into the working tree; add `allowWrite` for the host store path. | `S-6a`, `S-6b`. |
| `S-7` (browsers) | (4) human-run | Browser verification is run by the human (`D6` Branch B). `allowMachLookup: true` is NEVER set on CLI 2.1.119 because it disables the sandbox without warning. | Section 4. |
| `DOCK` | (2) narrow `excludedCommands` | Add only the `docker` subcommands the host needs. | `DOCK`. |
| `LOCAL` | (3) human opt-in | `allowLocalBinding` set by the human in user settings. | `LOCAL`. |
| Template path resolution | Template guidance | State that the template is consumed only when merged into project settings (`<host>/.claude/settings.json`); `--settings <template file>` protects nothing. | Section 1.3. |

## 6. Abort criterion 2 (Gate 1 remediation, 2026-10-10)

Plan Abort criterion 2: stop if `with_env.py` cannot make an allowlisted command read the key under `excludedCommands` in a sandboxed session, or if the secret value appears unmasked in the agent output. Measured after `e68ac72`, `cfe7950` (named commands, `-I`, narrowed template).

| Item | Fact |
| :--- | :--- |
| Fixture | Host-shaped scratch directory (removed afterwards): `git init`; `.agents/scripts/with_env.py` copied from the nucleus; `.agents/venv_skillopt` symlinked to the nucleus venv; `.agents/config/with_env_allowlist.json` = nucleus allowlist plus one entry `probe-key` (prints the key length, whether `HTTPS_PROXY` is set, and the raw key value); `.env` = `GEMINI_API_KEY=<18-character fixture, not a secret>`. |
| Settings | Template `claude/settings.hooks.json` as **project settings** (`<fixture>/.claude/settings.json`), with `hooks` removed (they name files the copy lacks), `sandbox.allowUnsandboxedCommands: false` (as section 1), and `python3 -I .agents/scripts/with_env.py probe-key` appended to `excludedCommands`. No absolute deny paths: `./` resolves against the project root here (section 1.3). |
| Session | Headless `claude -p --allowedTools Bash --output-format stream-json`, Claude Code CLI 2.1.119, launched by the principal agent from the fixture root; each case issued as its own Bash tool call. |
| Why a probe entry | It tests key visibility and output masking without sending fixture content to an LLM provider, which the real `graphify-*` entries would do. |

| ID | Command | Exit | Output | Reading |
| :--- | :--- | :--- | :--- | :--- |
| `SBX0` | `printenv HTTPS_PROXY` | 0 | `http://localhost:<port>` | Sandbox active. |
| `SBX1` | `curl -s --noproxy '*' -o /dev/null -m 10 https://registry.npmjs.org` | 6 | none | Sandbox active (run valid). |
| `A2-0` | `python3 -c "open('.env').close()"` | 1 | `PermissionError: [Errno 1] Operation not permitted: '.env'` | `./.env` deny resolves against the project root in project settings. |
| `A2-1` | `python3 -I .agents/scripts/with_env.py probe-key` | 0 | `len 18` / `proxy 0` / `raw ***` | Ran outside the sandbox (`proxy 0`), read the key from `.env` (length 18), value masked. |
| `A2-2` | `python3 .agents/scripts/with_env.py probe-key` (no `-I`) | 2 | `with_env: run as 'python3 -I …' (isolated mode)` | Not excluded, refused. |
| `A2-3` | `python3 -I .agents/scripts/with_env.py not-a-name` | 2 | `with_env: 'not-a-name' is not in config/with_env_allowlist.json` | Off-allowlist name refused. |
| `A2-4` | `python3 -I .agents/scripts/with_env.py graphify-label --help` | 2 | `usage: python3 -I with_env.py <name>` | An appended argv is refused. |
| `A2-5` | `grep -c '<fixture value>'` over the full session transcripts (stream-json) | — | `0` | The raw value never reached the agent's context. |

Verdict: **Abort criterion 2 not triggered.** `D2` stands. The masking result covers the exact-copy case only; per `agents.md RA-09`, masking is not the security boundary. `SBX1` cancelled the parallel batch of later cases on the first attempt; they were re-issued one at a time with identical commands. `A2-0` replaced a `head -c 0 .env` case that macOS `head` rejects as an illegal byte count.

## 7. U25 — absolute rendered exclusions (plan *Enmienda*, before U23)

Measured 2026-10-10 on Claude Code CLI 2.1.119, headless `claude -p --allowedTools Bash Edit`, launched by the principal agent, each step its own tool call. Two scratch fixtures, removed afterwards, each with `.env` = 18-character fixture value and `sandbox.allowUnsandboxedCommands: false`:

| Fixture | Project settings (`.claude/settings.json`) | Local settings (`.claude/settings.local.json`) |
| :--- | :--- | :--- |
| Host (`<fx>/.agents/` = copied wrapper, allowlist with probes, symlinked venv) | Template minus `hooks`, minus the three relative `with_env.py` lines and the two `gh … create` (as `U24`), plus `<python3 abs> -I <fx>/.agents/scripts/with_env.py probe-key2` | `excludedCommands`: `<python3 abs> -I <fx>/.agents/scripts/with_env.py probe-key`; `denyWrite`: `["<fx>/.agents"]`; `permissions.deny`: `Edit(//<fx>/.agents/**)` |
| Nucleus (`<fx>/scripts/`, `<fx>/config/`, `<fx>/venv_skillopt`) | Same, with `<fx>/scripts/with_env.py probe-key2` | `excludedCommands` with `probe-key`; `denyWrite`: the absolute wrapper, allowlist and venv paths; matching `Edit(//…/**)` |

Controls: `SBX0` exit 0 (proxy set) and `SBX1` exit 6 in every session.

| Plan item | ID | Command | Exit | Output | Reading |
| :--- | :--- | :--- | :--- | :--- | :--- |
| (b), (c) | `H-B1` | absolute line, `probe-key` (local list) | 0 | `len 18` / `proxy 0` / `raw ***` | Local `excludedCommands` honored; key read outside the sandbox; masked. |
| (b) | `H-B2` | absolute line, `probe-key2` (project list) | 0 | same | Project and local lists are **combined**, not overridden. |
| (a) | `H-A1` | `touch .agents/scripts/new_file` | 1 | `Operation not permitted` | Absolute `denyWrite` (`/…` form) honored. |
| (e) | `H-A2` | `mv .agents .agents_x` | 1 | `rename … Operation not permitted` | Renaming the protected directory is denied. |
| (e) | `H-A3` | `mv .agents/scripts .agents/scripts_x` | 1 | `rename … Operation not permitted` | Renaming inside it is denied. |
| (a) | `H-A4` | Edit tool on the absolute wrapper path | tool error | `File is in a directory that is denied by your permission settings.` | `Edit(//<abs>/**)` honored; file unchanged. |
| (d) | `H-D1` | relative `python3 -I .agents/scripts/with_env.py probe-key` at the root | 2 | `cannot read .env in the current directory` | The relative form is no longer excluded: runs sandboxed, `.env` denied. |
| (d) | `H-D3` | after `cd sub`, the same relative line runs the impostor `sub/.agents/scripts/with_env.py` | 0 | `IMPOSTOR_RAN proxy=1` / `IMPOSTOR_BLOCKED PermissionError: … '../.env'` | R2-1 closed: the impostor runs **inside** the sandbox and cannot read `.env`. |
| (d) | `H-D4` | after `cd sub`, the absolute line | 2 | `cannot read .env in the current directory` | The absolute line runs the real wrapper regardless of the working directory. |
| (b), (c) | `N-B1`, `N-B2` | absolute lines, local and project lists | 0, 0 | `len 18` / `proxy 0` / `raw ***` | As host. |
| (a) | `N-A1` | `touch scripts/with_env.py` | 1 | `Operation not permitted` | File-level absolute `denyWrite` honored. |
| (e) | `N-E1` | `mv scripts scripts_x` | 1 | `rename scripts to scripts_x: Operation not permitted` | A file-level `denyWrite` also blocks renaming its parent directory. |
| (e) | `N-E3` | `cp sub/scripts/with_env.py scripts/with_env.py` | 1 | `Operation not permitted` | Overwrite denied. |
| (e) | `N-E4` | absolute line after E1-E3 | 0 | `len 18` / `proxy 0` / `raw ***` | Still the real wrapper. |
| (e) | `N-F1` | `mv config config_x` | 1 | `Operation not permitted` | Allowlist parent rename denied. |
| — | — | `grep -c '<fixture value>'` over the three session transcripts | — | `0`, `0`, `0` | The raw value never reached the agent's context. |

Verdict: **Abort criterion 3 not triggered.** `D2-R` holds in both modes. `D2-N` resolves to **nucleus receives the rendered exclusion**, because a file-level `denyWrite` blocks renaming the parent directory (`N-E1`, `N-F1`). Syntax for `U23`: `sandbox.filesystem.denyWrite` takes the plain absolute path (`/…`); `permissions.deny` takes `Edit(//<absolute path>/**)`. Run notes: the first `H-A4` attempt was void (the session stripped the trailing spaces of the replacement, so no edit was attempted) and was re-run with `import jsonx`; the first `H-D3` impostor used `os.path.lexists`, which the `.env` deny also refuses (section 3, `S-4`), so it printed nothing about `.env` and was re-run with a direct `open()`; two sessions issued two independent steps in one turn, recorded in the transcripts and without effect on any result.

## 8. U25 re-measure (d), (e) with the real `install.py` render (after `55911a1`)

| Item | Fact |
| :--- | :--- |
| Fixture | Scratch host (removed afterwards): `git init`; `.agents` = clone of the nucleus at `55911a1` converted to submodule shape (`.agents/.git` is a `gitdir:` file, so `scripts/_mode.py` reports host mode); `venv_skillopt` symlinked; one `probe-key` entry added to the clone's allowlist **before** install; `.env` = 18-character fixture. |
| Install | `python3 .agents/scripts/install.py --target claude`, run outside the sandbox (the human step): exit 0; `Merged … settings.json`, `Merged … .mcp.json`, `Rendered 4 absolute with_env exclusion(s) -> …/.claude/settings.local.json`. |
| Rendered | `excludedCommands`: `<python3 abs> -I <fx>/.agents/scripts/with_env.py <name>` for the four names; `denyWrite`: `<fx>/.agents/{scripts,config,venv_skillopt}`; `permissions.deny`: `Edit(//<fx>/.agents/{scripts,config,venv_skillopt}/**)`. Project `excludedCommands`: the five `gh` inspection patterns only. |
| Only manual change | `sandbox.allowUnsandboxedCommands: false` added to `settings.local.json` (as sections 1, 6, 7). Hooks were left active. |

| ID | Command | Exit | Output | Reading |
| :--- | :--- | :--- | :--- | :--- |
| `SBX0`, `SBX1` | controls | 0, 6 | proxy set; no resolve | Valid run. |
| `R1` | rendered absolute line, `probe-key` | 0 | `len 18` / `proxy 0` / `raw ***` | Rendered exclusion honored; key read outside the sandbox; masked. |
| `R3` | after `cd sub`, `python3 -I .agents/scripts/with_env.py probe-key` (impostor) | 0 | `IMPOSTOR_RAN proxy=1` / `IMPOSTOR_BLOCKED PermissionError … '../.env'` | R2-1 closed on the real render. |
| `R5` | `mv .agents .agents_x` | 1 | `Operation not permitted` | Denying three subdirectories blocks renaming `.agents` itself. |
| `R6` | `mv .agents/scripts .agents/scripts_x` | 1 | `Operation not permitted` | — |
| `R7` | `touch .agents/config/x` | 1 | `Operation not permitted` | — |
| `R8` | `touch .agents/.bridge_probe.lock` | 0 | none | Boot lock writes inside `.agents` still work (reason for not denying all of `.agents`). |
| `R9` | Edit tool on the wrapper | tool error | `File is in a directory that is denied by your permission settings.` | File unchanged. |
| — | `grep -c '<fixture value>'` over the transcript | — | `0` | — |

Verdict: plan Verification (enmienda) row 3 met — the impostor cannot read `.env`.
