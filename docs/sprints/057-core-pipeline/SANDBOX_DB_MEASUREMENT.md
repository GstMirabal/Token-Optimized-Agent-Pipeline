# Sprint 057 - Sandbox measurement for a local test database (M1-M3)

| Field | Value |
| :--- | :--- |
| Sprint | 057 (`docs/sprints/057-core-pipeline/`) |
| Unit | `W01` (`IMPLEMENTATION_PLAN.md` `D1`, `## Abort criterion` item 1) |
| Method precedent | `docs/sprints/056-core-pipeline/SANDBOX_ENUMERATION.md` (headless `claude -p`, one case per Bash call, controls per session) |
| CLI version | `2.1.119 (Claude Code)` (`claude --version`). Every result below is per this version; another version needs a re-run |
| Sandbox | macOS Seatbelt; settings are the `permissions` and `sandbox` blocks of `claude/settings.hooks.json`, extracted with `jq '{permissions, sandbox}'`, no hooks |
| Driver | Headless `claude -p "$PROMPT" --allowedTools Bash --output-format stream-json --verbose`, working directory = fixture |
| Sessions used | 2 of budget 6 (`claude -p` calls) |
| Raw results | Kept in the session scratchpad, transcribed below |

## 1. Fixture

| Item | Value |
| :--- | :--- |
| Repository | Scratch git repository in the session scratchpad, one commit `d8ea2e9` (`probe base`); no hooks, no `.agents` directory, no `./.git/modules/.agents` |
| `./.env` | One line, `DUMMY_SECRET=not-a-real-secret-057` (disposable value) |
| `./.env.agent` | One line, `DATABASE_URL=postgres://test:test@127.0.0.1:55432/test` (disposable value) |
| Listener (M1) | `python3 -m http.server 55432 --bind 127.0.0.1`, started from the fixture outside the session; `curl http://127.0.0.1:55432/` from the unsandboxed shell returned `200` before session 1 |

## 2. Sessions

| Session | Settings | Purpose |
| :--- | :--- | :--- |
| 1 | Template `sandbox` block unchanged: `denyRead` = `["./.env", "./.env.*"]`; `allowRead` = `["./.env.example", "./.env.sample", "./.env.template"]`; `denyWrite` = `["./.agents", "./.git/modules/.agents", "./.env"]` | `M1`, `M2` without `allowRead`, `M3`, controls |
| 2 | Same as session 1 except `allowRead` = `["./.env.example", "./.env.sample", "./.env.template", "./.env.agent"]`; `denyRead` unchanged | `M2` with `allowRead`, controls |

## 3. Cases

| Case | Session | Command sent | Literal result | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| `M1` | 1 | `python3 -c 'import socket; socket.create_connection(("127.0.0.1", 55432), timeout=2); print("CONNECTED")'` | `Exit code 1`; `Traceback (most recent call last):` ... `File ".../socket.py", line 849, in create_connection`; `sock.connect(sa)`; `PermissionError: [Errno 1] Operation not permitted` (`is_error: true`; interpreter path abbreviated to `...`) | Denied. The failure is a `PermissionError` raised by `socket.connect`, with the listener up: not a timeout and not a refused connection |
| `M2` without `allowRead` | 1 | `cat .env.agent` | `Exit code 1`; `cat: .env.agent: Operation not permitted` (`is_error: true`) | Denied |
| `M2` with `allowRead`, target | 2 | `cat .env.agent` | `DATABASE_URL=postgres://test:test@127.0.0.1:55432/test` (`is_error: false`) | Readable |
| `M2` with `allowRead`, control | 2 | `cat .env` | `Exit code 1`; `cat: .env: Operation not permitted` (`is_error: true`) | Denied |
| `M2` control without `allowRead` | 1 | `cat .env` | `Exit code 1`; `cat: .env: Operation not permitted` (`is_error: true`) | Denied |
| `M3` | 1 | `git worktree add ../wt-probe HEAD` | `Preparing worktree (detached HEAD d8ea2e9)`; `HEAD is now at d8ea2e9 probe base` (`is_error: false`) | Allowed |

## 4. Controls

| Session | Control | Command sent | Literal result | Reading |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `SBX0` | `printenv HTTPS_PROXY` | `http://localhost:50175` (exit 0) | Proxy present |
| 1 | `SBX1` | `curl --noproxy "*" -sS -o /dev/null https://example.com; echo "exit=$?"` | `curl: (6) Could not resolve host: example.com`; `exit=6` | Direct egress fails |
| 2 | `SBX0` | `printenv HTTPS_PROXY` | `http://localhost:50216` (exit 0) | Proxy present |
| 2 | `SBX1` | `curl --noproxy "*" -sS -o /dev/null https://example.com; echo "exit=$?"` | `curl: (6) Could not resolve host: example.com`; `exit=6` | Direct egress fails |

Together `SBX0` and `SBX1` show the sandbox was active in both sessions. Both sessions ended with final assistant text `DONE`, result subtype `success`, process exit 0.

## 5. Results

| Case | Result in this fixture with CLI 2.1.119 |
| :--- | :--- |
| `M1` | TCP connect to `127.0.0.1:55432` measured denied: `PermissionError: [Errno 1] Operation not permitted` |
| `M2` | `./.env.agent` measured readable with the `allowRead` entry and unreadable without it; `./.env` measured denied in both sessions |
| `M3` | `git worktree add` measured allowed |

## 6. Consequence

| Item | Consequence |
| :--- | :--- |
| Abort criterion 1 | Fires because `M1` is denied. `W02`-`W06` are not executed in Sprint 057. The rest of the sprint continues (`IMPLEMENTATION_PLAN.md` `## Abort criterion` item 1) |
| `KI-057-1` (routes to Sprint 059, sandbox regime) | "pytest against a local database cannot run inside the sandbox: TCP to 127.0.0.1 is denied (M1); `.env.agent` readability (M2) is feasible but has no use until a DB route exists; options to measure in 059: whether a sandbox network setting permits loopback connections, or a unix-socket DB connection" |
| `M3` and `B-5` | `B-5` (`check_fix_reproduces.py` running `git worktree add` under the sandbox) does not reproduce in this fixture |
| Scope of `M3` | The fixture carried no host `./.git/modules/.agents` and no `.agents` directory, so the `denyWrite` entry for that path had no target. The `M3` result covers a nucleus-shaped fixture only; a host-shaped fixture is unmeasured |

## 7. Cleanup and post-state

| Item | Value |
| :--- | :--- |
| Worktree created by `M3` | Removed with `git worktree remove --force`; `git worktree list` shows only the fixture; directory absent |
| Listener on `127.0.0.1:55432` | Stopped; `curl` exits 7 (connection refused); `pgrep` finds no `http.server 55432` |
| Nucleus `git status --porcelain` after the sessions | Empty at the time of measurement (no repository file written by the sessions) |
| `claude -p` calls used | 2 of 6 |
