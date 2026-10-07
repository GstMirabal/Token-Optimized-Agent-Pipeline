# Rule Context: Project Topology

This document explicitly defines the strict structural routing inside the active project workspace. This context is loaded when operations involve modifying directory setups, deploying frameworks, or orchestrating database services.

## 1. Local Deterministic Execution
- **Strict Virtual Paths**: The use of global OS binaries (e.g., raw `python`, `npm`, `pip`) is absolutely **PROHIBITED**. Agents must imperatively employ deterministic local paths linked to the project context (e.g., `./venv/bin/python`, `./node_modules/.bin/npx`).
- **Nucleus interpreter**: The framework's own interpreter is `venv_skillopt/bin/python` (`Makefile`). The `./venv/` form above is the host-project convention; a nucleus session applying this section literally must substitute `venv_skillopt/bin/python`.
- **Binary Root Anchor**: Every valid workspace must expose its versioning file (e.g., `.nvmrc` or `.python-version`) to shield the local environment from system interference.

## 2. Infrastructure & Databases (Data-Leak Sieve) — host-only
*This section governs host projects. The nucleus ships no `docker-compose.yml` and no `./.docker-db-data`; its DB triggers never fire.*
- **Container Exclusivity**: Local databases or broker services (Postgres, Redis) must run purely via `docker-compose.yml`. Emulating or installing engines on the host OS is forbidden.
- **Physical Volume Sieve**: Agents must map persistent DB states forcefully into the hidden local directory `./.docker-db-data` to prevent accidental tracking.
- **Testing Purity**: Utilizing the local development database for Unit/Integration testing is **PROHIBITED**. Tests must dynamically instantiate purely ephemeral DB layers (default: `sqlite:///:memory:`). A host whose fidelity requirement SQLite cannot meet MAY substitute a real engine only through the declared-deviation path of `agents.md §3 local_testing` (`ADR-0016`): a host ADR naming the engine and an ephemeral per-run database or schema torn down after the run — never a shared or persistent one.

## 3. Data Persistence Policy
- **Mass Generation** (host-only): Scripts generating ETL outputs, PDFs, or raw heavy logs must dump directly to `./data/output/` or `./tmp/` and exclude themselves from the repository tracking index. The nucleus has no `./data/output/` referent.
- **Payload Reading Limiter**: Direct raw inspection (`cat`, full read) of unmasked documents > 1MB is banned. Agents must query using strictly AST chunking, `head`, `tail`, or metadata extraction limits to preserve the context window.

## 4. Claude Code sandbox: known failures and sanctioned forms

This is the single table of sandbox behaviour. Every other document references it and does not restate it (`RA-14`). Rows apply when `sandbox.enabled` is `true`, which `claude/settings.hooks.json` sets; `scripts/install.py` merges that template into the host's `.claude/settings.json`.

| Item | Fact |
| :--- | :--- |
| **Measuring CLI** | Claude Code 2.1.119, macOS (Seatbelt). |
| **Re-measure trigger** | Every row is a measurement of that version. When the CLI version changes, re-run the matrix in `docs/sprints/055-core-pipeline/SANDBOX_MEASUREMENT.md` and amend the affected rows before relying on them. |
| **Evidence column** | Row ids of `docs/sprints/055-core-pipeline/SANDBOX_MEASUREMENT.md` section 2 (`S-1`..`S-7`, `GKEY`, `DOCK`, `LOCAL`, `APPLE`) and section 4 (`allowMachLookup`). |
| **Excluded commands** | A command matched by `sandbox.excludedCommands` runs outside the sandbox and still passes through the permission flow. |

| Command / tool | In-sandbox signature (measured) | Sanctioned form | Evidence |
| :--- | :--- | :--- | :--- |
| Write to `.claude/settings.json` or `.claude/settings.local.json` (`S-1`) | `PermissionError: [Errno 1] Operation not permitted`. The path is a sandbox protected path. | The agent never writes it. `scripts/install.py` prints a `PermissionError` advisory with the exact command and exits `3`; the human runs `bash .agents/scripts/install.sh --target claude` in their own shell. | `S-1` |
| Read `.env.example`, `.env.sample`, `.env.template` (`S-2`) | Blocked by the `./.env.*` deny before the template carried `allowRead`. | The template keeps `./.env` and `./.env.*` in `sandbox.filesystem.denyRead` and adds the three template names to `sandbox.filesystem.allowRead`. `.env` and every other `.env.*` stay denied. | `S-2a` |
| Any command that needs a `.env` value, for example `set -a; . ./.env` (`S-3`) | `sh: ./.env: Operation not permitted`. | `python3 .agents/scripts/with_env.py <allowlisted command>` (nucleus: `python3 scripts/with_env.py ...`), invoked directly. A `make` target or script that calls it is not matched by `sandbox.excludedCommands`. The allowlist is `config/with_env_allowlist.json` (graphify only by default); a host adds an entry only by human decision, and every entry runs outside the sandbox. Values are never printed and output is redacted. The wrapper and the allowlist are write-denied by the template (`sandbox.filesystem.denyWrite`, `permissions.deny` `Edit`), because an excluded command that covers a working-tree script would let the agent rewrite the script and run it unsandboxed. | `S-3a`, `S-3b` |
| `python -m graphify . --mode deep` (graphify key) | No provider key in the environment (0 of 7 variables visible); a key held only in `.env` is invisible and the sandbox denies `.env`. | Agent, inside the sandbox: `python3 .agents/scripts/with_env.py .agents/venv_skillopt/bin/python -m graphify . --mode deep`. Human, unsandboxed shell: `make -f .agents/Makefile graphify-deep`. Variable list and source claim: `rules/graphify.md`. | `GKEY`, `S-3b` |
| Walkers of the full tree: `pytest` without explicit paths, any `stat()` of `.env` (`S-4`) | The `.env` deny also refuses `stat()`. `pytest tests/test_merge_json.py` exits `4`, `ERROR: found no collectors for <path>`; the same run passes unsandboxed. `python -m graphify update .` succeeded in the nucleus because graphify skips names equal to `.env`. | The human runs the walker unsandboxed, or the agent scopes it with explicit paths or a rootdir that excludes the denied file. | `S-4a`, `S-4b`, `S-4c` |
| `gh` (Go TLS) (`S-5`) | `tls: failed to verify certificate: x509: OSStatus -26276`. | The template excludes only the `gh` patterns the framework uses: `gh api repos/*`, `gh api -X * repos/*`, `gh api graphql *`, `gh pr create *`, `gh pr checks *`, `gh pr merge *`, `gh pr list *`, `gh repo view *`, `gh auth status*`, `gh release create *`, `gh release view *`. Any other `gh` subcommand: the human runs it, or the host adds a narrow pattern by human decision. | `S-5c` |
| `git ls-remote`, `git push`, `curl` over HTTPS (`S-5`) | None, when the domain is in `sandbox.network.allowedDomains`. | No exclusion needed. Add the domain to `network.allowedDomains`. | `S-5a`, `S-5b`, `S-5d` |
| `pnpm` store (`S-6`) | `pnpm store path` relocates to `<repo>/.pnpm-store/v11`; writes there fail with `No such file or directory`. The host's `ERR_PNPM_STORE_DIR_OPEN_OPERATION_LOCK` was not reproduced. | Run `pnpm store path` outside the sandbox and add the printed path to `sandbox.filesystem.allowWrite` in user settings; or the human runs the reinstall unsandboxed. | `S-6a`, `S-6b` |
| Chromium, Playwright, Chrome for Testing (`S-7`) | `FATAL mach_port_rendezvous_mac.cc ... bootstrap_check_in org.chromium.Chromium.MachPortRendezvousServer.<pid>: Permission denied (1100)`; exit `-5` (SIGTRAP). | Human-run browser verification: `rules/qa_and_testing.md` section 6. | `S-7a`, `S-7b` |
| `sandbox.network.allowMachLookup: true` | The whole sandbox is silently disabled (fail-open), even with `allowUnsandboxedCommands: false`: `.env` readable, `docker info` exit `0`, no warning. | **PROHIBITED** in every settings file. The list form (`["org.chromium.*"]`) keeps the sandbox but does not fix Chromium, because the browser must register a Mach service and lookup permission does not cover registration. | `allowMachLookup` (section 4) |
| `docker`, `docker compose` | `permission denied while trying to connect to the docker API at unix://<home>/.docker/run/docker.sock`. | Narrow `excludedCommands` such as `docker compose *`, in the host's own settings, by human decision. The template carries none. | `DOCK` |
| Local dev server on `127.0.0.1` | `curl: (7) Failed to connect to 127.0.0.1 port <port>`; binding is blocked. | `sandbox.network.allowLocalBinding: true`, opt-in by the human in user settings. | `LOCAL` |
| `open`, `osascript` against another application | Plain `osascript -e 'return 1'` exits `0`; the cross-app Apple Event `-600` case was not exercised. | `allowAppleEvents` only in user settings, set by the human (it removes code-execution isolation); or a narrow `open *` exclusion by human decision. | `APPLE` |
| `jest` | Not measured in Sprint 055. | Run `jest --no-watchman`. | none (sprint 055 decision, not a measured row) |
| Template paths `./...` in `sandbox.filesystem` | With `claude --settings <template file>`, `./.env` did not protect the repository `.env`: a sandboxed open exited `0`. | `./` resolves against the directory of the settings file that declares it. The template is correct only when merged into the host's project `.claude/settings.json` by `scripts/install.py`; passing the template file with `--settings` protects nothing. | section 1.3 |
