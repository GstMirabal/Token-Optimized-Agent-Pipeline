# 🧭 How to use the Token-Optimized Agent Pipeline slash commands
**File**: `docs/guides/AGENTS_SLASH_COMMANDS_GUIDE.md` (RA-06 Option B naming)
**Module**: AGENTS

---

## 1. Goal
Discover and invoke the `/agents:*` slash commands that map every `workflows/*.md` protocol to a real Claude Code command, in both a fresh host and an already-established (retrofit) repository.

## 2. Prerequisites
- `.agents` added as a Git submodule at the host project root (`git submodule add https://github.com/GstMirabal/Token-Optimized-Agent-Pipeline .agents`).
- The Claude Code bridge installed at least once via `.agents/scripts/install.sh` (symlinks `.agents/commands/*.md` into `.claude/commands/agents/`, exposing the `/agents:*` namespace so host-defined commands never collide with framework ones).
- A restarted Claude Code session after installation — commands are discovered at session start, not live.

## 3. Steps

### 3.1 Retrofitting an already-established repository
If you are adding the framework to an **already established repository**, follow this sequence to align your architectural roadmap:

1. **Submodule Insertion:** In your root folder: `git submodule add https://github.com/GstMirabal/Token-Optimized-Agent-Pipeline .agents`
2. **Bridge Installation:** `.agents/scripts/install.sh` (creates `.claude/agents`, `.claude/commands/agents`, `.claude/skills`, and merges hooks/MCP config).
3. **AI Session Trigger:** Tell the AI: *"Initialize session using governance protocols in `.agents/` and execute `/agents:start`."*
4. **Roadmap Discovery:** The topology mapper will map `docs/active_state.json` (scaffolding it on first run — see `start_workflow.md`).
5. **Then follow the canonical onboarding order**, defined once in `agents.md §6` and referenced rather than repeated (`RA-14`): **`/agents:harden`** → **`/agents:standardization`** → **`/agents:revdoc`** → **`/agents:pipeline`**. Each owns a different object — platform controls, artifacts and topology, documentation of the code, and change itself — and running them out of order produces documentation of a layout that is about to move.

The Orchestrator will automatically scan your source code, identify your project's current Phase, initialize your local context, and generate persistent architectural tracking in `docs/roadmaps/`.

### 3.2 Core commands reference
Every `workflows/*.md` protocol maps to a real Claude Code slash command in `commands/*.md`, installed under the `/agents:*` namespace:

| Command | Purpose |
| :--- | :--- |
| **`/agents:start`** | **Entry Gate**: Initializes Zero-Memory, installs the Claude bridge on first run, syncs the DevOps/Git Sync agents, and prepares execution limits. |
| **`/agents:pipeline`** | **Orchestration**: The Double-Gate execution pipeline. Distributes tasks across subagents. |
| **`/agents:close`** | **Exit Gate**: Extracts heuristics, updates roadmaps, mirrors state, and seals the repo securely. |
| **`/agents:audit`** | **Standards Sweep**: Proactive structural maintenance to purge logic drifts and missing `.md` rules. |
| **`/agents:skill-forge`** | **Tool Registration**: Creates, tests, and natively registers new pipeline tools without mutating production logic. |
| **`/agents:remediation`** | **Rollback & Recovery**: Halts infinite hallucination loops, nukes git to pristine state, and logs negative knowledge. |
| **`/agents:reconcile`** | **Protocol-Failure Recovery**: Restores traceability for commits made without `start` or `close` — rebuilds the Master Ledger entry and phase record from commit bodies and diffs. **Reverts nothing**: the work is good, its record is missing. Not to be confused with `remediation`, which revokes bad work. |
| **`/agents:standardization`** | **Structural**: Enforces the `[layer]/[app]/` dictionary and Technical English purity. |
| **`/agents:extract`** | **Distillation**: Memory indexer handling the "Rule Amendment Loop" (see `agents.md §4`). |
| **`/agents:deployment`** | **Deployment**: Merges the sprint branch to upstream branches and operates CI/CD boundaries. |
| **`/agents:graphify`** | **Knowledge Graph**: Runs the graphify pipeline over the current project into `graphify-out/`. |

Two more sit outside the sprint pipeline and apply to a repository the framework has not handled before:

| Command | Purpose |
| :--- | :--- |
| **`/agents:harden`** | **Platform Controls**: Turns on secret scanning, private vulnerability reporting, Dependabot, code scanning, and branch protection, in an order that does not lock you out of your own repository. |
| **`/agents:revdoc`** | **Reverse Documentation**: Produces documentation for an existing codebase that is true, and provably so — graph first, every declared path verified, contracts written for every exposed interface. Runs before any remediation on an undocumented repository. |

> [!TIP]
> **Documentation Sovereignty:** All technical docs, implementation plans (`docs/sprints/`), and local roadmaps (`docs/roadmaps/`) are tightly bound directly to Pipeline tracking under `/docs/`.

### 3.3 Reading the Skills Manifest
The Orchestrator statically routes external tools using **`.agents/skills/manifest_skills.json`**, drastically reducing token consumption and discovery time during sessions:

```json
// Example: The Orchestrator statically routes external tools using the Skills Manifest
{
  "name": "omni-context-minimizer",
  "category": "Efficiency",
  "tags": ["token-saver", "ast", "scan"]
}
```

Check the `/workflows/` directory for automated protocols like project scaffolding. Explore `/mcp_servers/` for bridging external LLM data nodes.

If there's more than one valid path:
- **If working inside the `.agents` repo itself (Nucleus Mode)**: the full host bridge is refused (`agents.md §5 nucleus_neutrality`); run the installer's minimal self-bridge instead — `python3 scripts/install.py` — which links only `.claude/commands/agents/*` and `.claude/agents/*` (no hooks, skills, MCP, or scaffolding), then restart the session.

## 4. Verify it worked
```bash
ls .claude/commands/agents/
```
Expected output: one `.md` file per command listed in §3.2 (`start.md`, `pipeline.md`, `close.md`, `audit.md`, `skill-forge.md`, `remediation.md`, `reconcile.md`, `standardization.md`, `extract.md`, `deployment.md`, `graphify.md`, `harden.md`, `revdoc.md`), and in Claude Code the `/agents:` prefix autocompletes to the same 13 commands.

## 5. If something goes wrong
| Symptom | Likely cause | Fix |
| :--- | :--- | :--- |
| `/agents:*` commands don't autocomplete in Claude Code | Session started before the bridge was installed | Re-run `.agents/scripts/install.sh` (or `scripts/install.py` in Nucleus Mode), then restart the Claude Code session — commands are discovered at session start, not live. |
| `/agents:pipeline` fails to find project context | `docs/active_state.json` not yet scaffolded | Run `/agents:start` first; it scaffolds `docs/active_state.json` on first run per `start_workflow.md`. |
| Commands collide with host-defined commands of the same name | Bridge installed outside the `/agents:*` namespace, or a non-symlink mechanism was used to inject config | Reinstall exclusively via `.agents/scripts/install.sh` — it is the only sanctioned bridge (`agents.md §3 federation`) and never overwrites non-symlinked host content. |
| Orchestrator ignores a new skill | `manifest_skills.json` not updated | Register the skill's `name`/`category`/`tags` entry in `.agents/skills/manifest_skills.json` (see §3.3). |

---
*See also: `.agents/README.md` (Tutorial) · related guides in `docs/guides/`.*
