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
*   **Zero-Trust Hierarchy:** Segregated Mentor (Debate), Orchestrator (Planning), and Auditor (Validation) roles to prevent autonomous logic failures.
*   **Token-Saver Auditor:** An economic kill-switch that prevents inefficient plans and reduces API costs by optimizing context windows.
*   **Omni-Context Minimizer:** Smart AST-based code skeleton extraction that allows AI to understand massive files (1000+ lines) while only consuming 10% of the normal token cost.
*   **MCP Registry & Routing:** Strict Zero-Trust assignment of external Model Context Protocols (MCPs). The Orchestrator queries `.agents/skills/mcp-registry/registry.json` and provisions specific local/remote data sources before unlocking subagent execution.
*   **Amnesia & Atomic KIs:** Automatic knowledge extraction distilling long-term "lessons learned" into atomic `.md` files indexed by `ki_index.json` under `/knowledge/`, avoiding token bloating in future sessions.
*   **Modular Scaffolding:** Standardized project initialization ensuring every new repository inherits the same constitutional security and quality rules.

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

3. **Sync AI Intelligence**
   Update the framework to the latest global version to inherit new patterns and skills:
   ```bash
   git submodule update --remote --merge
   ```

4. **Audit & Configure**
   Review `governance/global_user_rules.md` to ensure your local environment variables and paths are correctly mapped within the framework.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage

Once integrated, the framework automatically triggers its auditors during your AI coding sessions. For example, if you ask the AI to analyze a large module, the **Token-Saver** will mandate the use of the minimizer:

```bash
# Example: Extracting the skeleton of a large class to save tokens
python .agents/skills/omni-context-minimizer/scripts/omni_minimizer.py path/to/large_file.py
```

### 🛠️ AI-Ops: Session Initialization
To ensure the AI follows the constitutional rules and architectural standards from the very first message:
> **Protocol**: Start any new conversation or context window by referencing the `.agents` path and the `governance/global_user_rules.md`.
> **Trigger Phrase**: *"Initialize session using framework protocols in `.agents/`. Audit my requests against `governance/global_user_rules.md` and keep the `task.md` indexed."*

### 🤖 AI-Ops: Core Commands (Slash Commands)
The framework supports automated workflows via standardized Markdown protocols. Use these to trigger complex engineering tasks:

| Command | Purpose | Location |
| :--- | :--- | :--- |
| **`/amnesia_extractor`** | **Post-Sprint Purgatory**: Extracts LTM Lessons into Knowledge Items. | `workflows/amnesia_extractor.md` |
| **`/scaffolding_modular`** | **Project Scaffolding**: Initializes a new repo with Modular Architecture. | `workflows/scaffolding_modular.md` |

> [!TIP]
> Any `.md` file added to the `workflows/` directory becomes an executable "slash command" that you can request from the AI.

```json
// Example: The Orchestrator statically routes external tools using the MCP Registry
"example-postgres-mcp": {
  "command": "npx -y @modelcontextprotocol/server-postgres postgres://.../db",
  "authorized_roles": ["Database Auditor", "Backend Architect"]
}
```

Check the `/workflows/` directory for automated protocols like project scaffolding. Explore `/skills/mcp-registry/` for adding external LLM data connections.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make to the core framework are **greatly appreciated**.

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
