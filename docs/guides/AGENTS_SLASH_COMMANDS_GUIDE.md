# 🧭 How to use the Universal-Agents slash commands
**File**: `docs/guides/AGENTS_SLASH_COMMANDS_GUIDE.md` (J-06 Option B naming)
**Module**: AGENTS

---

## 1. Goal
Discover and invoke the `/agents:*` slash commands that map every `workflows/*.md` protocol to a real Claude Code command, in both a fresh host and an already-established (retrofit) repository.

## 2. Prerequisites
- `.agents` added as a Git submodule at the host project root (`git submodule add https://github.com/GstMirabal/.agents .agents`).
- The Claude Code bridge installed at least once via `.agents/scripts/install_claude.sh` (symlinks `.agents/commands/*.md` into `.claude/commands/agents/`, exposing the `/agents:*` namespace so host-defined commands never collide with framework ones).
- A restarted Claude Code session after installation — commands are discovered at session start, not live.

## 3. Steps

### 3.1 Retrofitting an already-established repository
If you are adding the framework to an **already established repository**, follow this sequence to align your architectural roadmap:

1. **Submodule Insertion:** In your root folder: `git submodule add https://github.com/GstMirabal/.agents .agents`
2. **Bridge Installation:** `.agents/scripts/install_claude.sh` (creates `.claude/agents`, `.claude/commands/agents`, `.claude/skills`, and merges hooks/MCP config).
3. **AI Session Trigger:** Tell the AI: *"Initialize session using governance protocols in `.agents/` and execute `/agents:start`."*
4. **Roadmap Discovery:** The matrix will map `docs/active_state.json` (scaffolding it on first run — see `start_workflow.md`). Run the command: **`/agents:matrix`**.

The Orchestrator will automatically scan your source code, identify your project's current Phase, initialize your local context, and generate persistent architectural tracking in `docs/roadmaps/`.

### 3.2 Core commands reference
Every `workflows/*.md` protocol maps to a real Claude Code slash command in `commands/*.md`, installed under the `/agents:*` namespace:

| Command | Purpose |
| :--- | :--- |
| **`/agents:start`** | **Entry Gate**: Initializes Zero-Memory, installs the Claude bridge on first run, syncs DevOps/Git Sentinels, and prepares execution limits. |
| **`/agents:matrix`** | **Orchestration**: The V3 Double-Gate execution pipeline. Distributes tasks across subagents. |
| **`/agents:close`** | **Exit Gate**: Extracts heuristics, updates roadmaps, mirrors state, and seals the repo securely. |
| **`/agents:audit`** | **Inquisitor**: Proactive structural maintenance to purge logic drifts and missing `.md` rules. |
| **`/agents:skill-forge`** | **Quartermaster**: Creates, tests, and natively registers new Matrix tools without mutating production logic. |
| **`/agents:remediation`** | **Panic Button**: Halts infinite hallucination loops, nukes git to pristine state, and logs negative knowledge. |
| **`/agents:standardization`** | **Structural**: Enforces the `[layer]/[app]/` dictionary and Technical English purity. |
| **`/agents:extract`** | **Distillation**: Memory indexer handling the "Jurisprudence Loop" (see `agents.md §4`). |
| **`/agents:deployment`** | **Vanguard**: Merges the sprint branch to upstream branches and operates CI/CD boundaries. |
| **`/agents:skeleton`** | **Context Compression**: Forces the Omni-Minimizer to carve AST summaries of massive codefiles to protect token limits. |
| **`/agents:graphify`** | **Knowledge Graph**: Runs the graphify pipeline over the current project into `graphify-out/`. |

> [!TIP]
> **Documentation Sovereignty:** All technical docs, implementation plans (`docs/sprints/`), and local roadmaps (`docs/roadmaps/`) are tightly bound directly to Matrix V2 tracking under `/docs/`.

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
- **If working inside the `.agents` repo itself (Nucleus Mode)**: the full host bridge is refused (`agents.md §5 nucleus_neutrality`); run the installer's minimal self-bridge instead — `python3 scripts/install_claude.py` — which links only `.claude/commands/agents/*` and `.claude/agents/*` (no hooks, skills, MCP, or scaffolding), then restart the session.

## 4. Verify it worked
```bash
ls .claude/commands/agents/
```
Expected output: one `.md` file per command listed in §3.2 (`start.md`, `matrix.md`, `close.md`, `audit.md`, `skill-forge.md`, `remediation.md`, `standardization.md`, `extract.md`, `deployment.md`, `skeleton.md`, `graphify.md`), and in Claude Code the `/agents:` prefix autocompletes to the same 11 commands.

## 5. If something goes wrong
| Symptom | Likely cause | Fix |
| :--- | :--- | :--- |
| `/agents:*` commands don't autocomplete in Claude Code | Session started before the bridge was installed | Re-run `.agents/scripts/install_claude.sh` (or `scripts/install_claude.py` in Nucleus Mode), then restart the Claude Code session — commands are discovered at session start, not live. |
| `/agents:matrix` fails to find project context | `docs/active_state.json` not yet scaffolded | Run `/agents:start` first; it scaffolds `docs/active_state.json` on first run per `start_workflow.md`. |
| Commands collide with host-defined commands of the same name | Bridge installed outside the `/agents:*` namespace, or a non-symlink mechanism was used to inject config | Reinstall exclusively via `.agents/scripts/install_claude.sh` — it is the only sanctioned bridge (`agents.md §3 federation`) and never overwrites non-symlinked host content. |
| Orchestrator ignores a new skill | `manifest_skills.json` not updated | Register the skill's `name`/`category`/`tags` entry in `.agents/skills/manifest_skills.json` (see §3.3). |

---
*See also: `.agents/README.md` (Tutorial) · related guides in `docs/guides/`.*
