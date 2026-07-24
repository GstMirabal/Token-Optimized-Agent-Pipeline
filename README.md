<div align="center">

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

</div>

<a name="readme-top"></a>

<h3 align="center">Universal-Agents Framework (.agents)</h3>

<p align="center">
  A hierarchical, zero-trust subagent architecture for context-aware and token-efficient AI software engineering.
<br /><br />
<a href="https://github.com/GstMirabal/.agents"><strong>Explore the docs »</strong></a>
<br />
·
<a href="https://github.com/GstMirabal/.agents/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
·
<a href="https://github.com/GstMirabal/.agents/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
</p>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul><li><a href="#built-with">Built With</a></li></ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation & Configuration</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

## About The Project

Universal-Agents is a military-grade AI agent governance framework designed to prevent context bloat, secure RCE environments, and ensure long-term knowledge retention. It transforms standard AI agents into a disciplined swarm of specialized subagents.

**Key Features:**
*   **Zero-Trust Identity Hierarchy:** Segregated Principal, Orchestrator, QA Agent, Tester Agent, and Skill Architect roles to prevent autonomous logic failures.
*   **Matrix V2 Execution Pipeline:** A strict Double-Gate Review protocol ensuring structural and functional verification before user handoffs.
*   **100% Coverage Mandate:** Strategic requirement enforced by the **Tester Agent**, ensuring zero-defect integration before any code commitment.
*   **Token-Saver Auditor:** An economic kill-switch that prevents inefficient plans and reduces API costs by optimizing context windows.
*   **Omni-Context Minimizer:** Smart AST-based code skeleton extraction that allows AI to understand massive files (1000+ lines) while only consuming 10% of the normal token cost.
*   **Skill Forge & Arsenal Flat Mapping:** Universal, deterministic tooling governed by the Trinity Standard and external nomenclature (`-3rd`), bridged to real Claude Code slash commands via `scripts/install_claude.sh` + the `slash-commander` skill.
*   **Knowledge Extraction & Memory:** Automatic heuristic distillation via `extract_workflow.md`, indexing lessons into atomic Knowledge Items (KIs) inside `/memory/`.
*   **Persistent Compliance Roadmap:** Integrated topology via `docs/roadmaps/`, anchored by the unbreakable `docs/active_state.json`.
*   **Documentation Standard:** Deterministic freshness-gate (Diátaxis + C4 + ADR) that keeps architecture docs from silently going stale — enforced at sprint close, not by agent memory.

### Built With

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Shell Script](https://img.shields.io/badge/shell_script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white)
![Markdown](https://img.shields.io/badge/markdown-%23000000.svg?style=for-the-badge&logo=markdown&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

### Prerequisites

*   **Git**: Required for submodule management and architectural inheritance.
*   **Python 3.x**: Required for running the Omni-Minimizer and optimization scripts.
*   **Node.js**: Recommended for managing advanced AI skills via `npx skills`.

### Installation & Configuration

1. **Clone the repository**
   ```bash
   git clone https://github.com/GstMirabal/.agents.git
   cd .agents
   ```

2. **Initialize Git Submodule**
   To use this framework in a new project, add it as a submodule to your root directory:
   ```bash
   git submodule add https://github.com/GstMirabal/.agents .agents
   ```

3. **Install the Claude Code bridge**
   Claude Code only auto-discovers agents/commands/skills/hooks from `.claude/` and `.mcp.json` at your **project root** — it never reads inside a submodule. Run the installer once (idempotent, safe to re-run):
   ```bash
   .agents/scripts/install_claude.sh
   ```
   This symlinks `.agents/agents/*.md` → `.claude/agents/`, `.agents/commands/*.md` → `.claude/commands/agents/` (exposed as `/agents:*`), `.agents/skills/*/` → `.claude/skills/`, merges hooks + MCP servers into your `.claude/settings.json` / `.mcp.json`, and adds the `@.agents/agents.md` import to your `CLAUDE.md` so the constitution auto-loads every session. It never overwrites non-symlinked host content.

   **Project profiles (opt-in)**: project-family packs (extra rules, specialist agents, domain skills) live under `profiles/` and are only linked when explicitly requested:
   ```bash
   .agents/scripts/install_claude.sh --profile crypto-django
   ```

4. **Pin a release (recommended) or track main**
   Pin the submodule to a tagged release for reproducible governance — updates then happen deliberately, not by drift (same supply-chain reasoning as J-10):
   ```bash
   cd .agents && git fetch --tags && git checkout v3.0.0 && cd ..
   git add .agents && git commit -m "chore(deps): pin .agents to v3.0.0 #[Sprint_ID]"
   ```
   To upgrade later: check the [CHANGELOG](CHANGELOG.md), check out the new tag, and re-run the installer to pick up new agents/commands/skills:
   ```bash
   git submodule update --remote --merge   # only if you deliberately track main
   .agents/scripts/install_claude.sh
   ```

5. **Audit & Configure**
   Review `agents.md` (the constitution) to ensure your local environment variables and paths are correctly mapped within the framework.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage

Once integrated, the framework automatically triggers its auditors during your AI coding sessions. For example, if you ask the AI to analyze a large module, the **Token-Saver** will mandate the use of the minimizer:

```bash
# Example: Extracting the skeleton of a large class to save tokens
python .agents/skills/omni-context-minimizer/scripts/omni_minimizer.py path/to/large_file.py
```

### 🛡️ Scenario: Retrofitting Existing Projects
If you are adding the framework to an **already established repository**, follow this sequence to align your architectural roadmap:

1.  **Submodule Insertion:** In your root folder: `git submodule add https://github.com/GstMirabal/.agents .agents`
2.  **Bridge Installation:** `.agents/scripts/install_claude.sh` (creates `.claude/agents`, `.claude/commands/agents`, `.claude/skills`, and merges hooks/MCP config).
3.  **AI Session Trigger:** Tell the AI: *"Initialize session using governance protocols in `.agents/` and execute `/agents:start`."*
4.  **Roadmap Discovery:** The matrix will map `docs/active_state.json` (scaffolding it on first run — see `start_workflow.md`). Run the command: **`/agents:matrix`**.

The Orchestrator will automatically scan your source code, identify your project's current Phase, initialize your local context, and generate persistent architectural tracking in `docs/roadmaps/`.

---

### 🤖 AI-Ops: Core Commands (Slash Commands)
The framework maps every `workflows/*.md` protocol to a real Claude Code slash command in `commands/*.md`, installed under the `/agents:*` namespace so they never collide with commands your host project defines:

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

> [!IMPORTANT]
> **Orchestration Manifest:** The Orchestrator now uses **`.agents/skills/manifest_skills.json`** to statically route tools, drastically reducing token consumption and discovery time during sessions.

```json
// Example: The Orchestrator statically routes external tools using the Skills Manifest
{
  "name": "omni-context-minimizer",
  "category": "Efficiency",
  "tags": ["token-saver", "ast", "scan"]
}
```

Check the `/workflows/` directory for automated protocols like project scaffolding. Explore `/mcp_servers/` for bridging external LLM data nodes.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make to the core framework are **greatly appreciated**.

### 🧬 Developing the Framework Itself (Nucleus Mode)

Working *inside* this repo (not a host project) is a different case: the full host bridge is refused (`agents.md §5 nucleus_neutrality` — this repo is the law, not a project it governs), so `/agents:*` commands don't exist here until you run the installer's **minimal self-bridge**:

```bash
git clone https://github.com/GstMirabal/.agents.git
cd .agents
python3 scripts/install_claude.py
```

This links `.claude/commands/agents/*` and `.claude/agents/*` (so `/agents:start`, `/agents:close`, etc. work while you develop) and adds `@agents.md` to a nucleus-local `CLAUDE.md` — no hooks, skills, MCP, or scaffolding (those assume a host root; `.claude/` here is git-ignored, regenerate anytime by re-running the script). **Restart your Claude Code session** afterward — commands are discovered at session start, not live.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact

Gustavo Mirabal Suarez - gst.mirabal@gmail.com

- LinkedIn: [@Gustavo-Mirabal](https://www.linkedin.com/in/gstmirabal/)
- GitHub: [@GstMirabal](https://github.com/GstMirabal)
- Twitter: [@GstMirabal](https://x.com/gst_mirabal)

Project Link: [https://github.com/GstMirabal/.agents](https://github.com/GstMirabal/.agents)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/GstMirabal/.agents.svg?style=for-the-badge
[contributors-url]: https://github.com/GstMirabal/.agents/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/GstMirabal/.agents.svg?style=for-the-badge
[forks-url]: https://github.com/GstMirabal/.agents/network/members
[stars-shield]: https://img.shields.io/github/stars/GstMirabal/.agents.svg?style=for-the-badge
[stars-url]: https://github.com/GstMirabal/.agents/stargazers
[issues-shield]: https://img.shields.io/github/issues/GstMirabal/.agents.svg?style=for-the-badge
[issues-url]: https://github.com/GstMirabal/.agents/issues
[license-shield]: https://img.shields.io/github/license/GstMirabal/.agents.svg?style=for-the-badge
[license-url]: https://github.com/GstMirabal/.agents/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/gstmirabal/
