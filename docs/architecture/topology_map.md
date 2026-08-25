# 📍 Topology Map & Inventory
Version: 1.4.0 | **VERIFIED_TOPOLOGY_SIG:** b7e2f914-pipeline-v3.7-documentation-standard

> [!IMPORTANT]
> This file is the **Absolute Truth** of the internal framework geography. Recursive structural discovery is strictly FORBIDDEN in this session while the signature is valid.

## 1. Framework Inventory (.agents/)

| Component | Origin Type | Function | Status |
| :--- | :--- | :--- | :--- |
| **`docs/`** | Framework-Anchor | Documentation Entry Point and standardized documentation tree. | ✅ SOVEREIGN |
| **`rules/`** | Framework-Core | System rules and standards. | ✅ PROTECTED |
| **`workflows/`** | Custom-Hardened | Refactored execution manuals and protocols. | ✅ ALIGNED |
| **`memory/`** | Framework-Persist | Long-term memory (Knowledge Items). | ✅ INDEXED |
| **`skills/`** | Framework-Library | Validated binary and quality tools. | ✅ AUDITED |
| **`agents/`** | Core-Intelligence | Subagent profiles (real Claude Code frontmatter: `name`/`description`/`tools`). | ✅ PROTECTED |
| **`commands/`** | System-Bridge | Real Claude Code slash commands (`.md`, `@`-referencing `workflows/`). Installed as `/agents:*` via `scripts/install.sh`, never generated. | ✅ ALIGNED |
| **`hooks/`** | DevOps-Gates | Execution gates for telemetry and structural mirrors; wired into the host's `.claude/settings.json` via `claude/settings.hooks.json`. | ✅ PROTECTED |
| **`mcp_servers/`** | Bridge-Nodes | Native Model Context Protocol registries. Config template lives at `claude/mcp.json`, merged into host `.mcp.json`. | ✅ ALIGNED |
| **`claude/`** | System-Bridge | Templates merged into the host by the installer: `mcp.json`, `settings.hooks.json`. | ✅ ALIGNED |
| **`scripts/install.sh`** | System-Bridge | The only sanctioned mechanism for wiring `.agents/` into a host's `.claude/` (symlinks + non-destructive JSON merge + `CLAUDE.md` governance-rules import). | ✅ ALIGNED |
| **`profiles/`** | Project-Packs | Opt-in project-specific packs (rules/agents/skills/mcp) installed only via `--profile [name]`. Preserves project self-learning without contaminating other hosts. | ✅ ALIGNED |
| **`styles/`** | Framework-Core | Vale prose-lint style packages (`styles/Diataxis/`), scoped via `.vale.ini`. New in v1.4.0 (`rules/documentation_standard.md`). | ✅ ALIGNED |
| **`Makefile`** | DevOps-Gates | Deterministic entrypoints: `graphify-update`, `graphify-rebuild`, `verify`. | ✅ ALIGNED |

## 2. Standardized Documentation hierarchy (/docs/)
- **`active_state.json`**: Authoritative session anchor (Rule 83).
- **`architecture/`**: High-level topological maps and Mermaid views.
- **`roadmaps/`**: Strategic multi-phase blueprints.
- **`sprints/`**: Session logs and implementation tracking.
- **`contracts/`**: Formal technical agreements and I/O specifications.

## 3. Workflow Function Mapping
- **`start_workflow.md`**: Initial session protocol and crash detection (Rule 0.1).
- **`pipeline_workflow.md`**: Universal orchestration and Double-Gate review pipeline.
- **`close_workflow.md`**: Intelligence distillation, roadmap sync, and atomic lockdown.
- **`extract_workflow.md`**: Heuristic distillation and `memory_index.json` update (flat schema, no domain subfolders — see `agents.md §4`).
- **`audit_workflow.md`**: The Standards Sweep protocol for sweeping preventative maintenance and standards enforcement.
- **`skill_forge_workflow.md`**: The Tool Registration protocol for natively assembling and registering pipeline tools in isolation.
- **`remediation_workflow.md`**: The Rollback & Recovery protocol. Executes Git nuke and extracts negative-heuristics on Double-Gate stalemates.
- **`deployment_workflow.md`**: The Deployment protocol for git-push, merge, and CI/CD operations without mutating code.
- **`standardization_workflow.md`**: Structural alignment protocol for /docs and nomenclature purges.

## 4. Discovery Lock (Sync-Lock)
Upon detecting this signature, the Agent MUST avoid redundant `list_dir` and rely exclusively on this index for internal pipeline navigation.
