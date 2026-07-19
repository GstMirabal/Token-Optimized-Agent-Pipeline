<div align="center">

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

</div>

<a name="readme-top"></a>

<h3 align="center">MCP Registry & Manager</h3>

<p align="center">
  Registry and configuration manager for Model Context Protocol servers to maximize data utility.
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

The **MCP Registry & Manager** is the Matrix's external-data discovery system. It manages the configuration and routing of local and remote Model Context Protocol (MCP) servers, letting subagents expand their knowledge frontier in a safe, audited way. Project-specific servers (e.g. market-data feeds) live in `profiles/[name]/mcp/registry.json`.

**Key Features:**
*   **Centralized Registry:** A single source of truth in `registry.json` for all external connections.
*   **Zero-Trust Routing:** Ensures only registry-authorized MCPs can be invoked by the Orchestrator.
*   **Dynamic Provisioning:** Safely injects environment variables and API secrets.

### Built With

![JSON](https://img.shields.io/badge/json-5E5E5E?style=for-the-badge&logo=json&logoColor=white)
![MCP](https://img.shields.io/badge/MCP-Registry-brightgreen)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

### Prerequisites

*   **Claude / LLM Platform**: Model capability to interact with MCP servers.
*   **MCP Server Configuration**: Persistent location of server credentials in `.env` or the global configuration file.

### Installation & Configuration

1. **Integrated in Core**
   Located at `.agents/skills/mcp-registry/`.

2. **Register a Server**
   Add your new server to `registry.json` following the official metadata schema (local-process commands must use `pnpm dlx`, per agents.md §8).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage

The **Orchestrator** consults the registry before any task requiring real-time external data. If a server is not in `registry.json` (or the active profile's registry), external access is blocked. Free-tier API credits are prioritized over paid calls.

```bash
# Example: viewing active servers in the registry
cat .agents/skills/mcp-registry/registry.json
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contributing

1. Fork the Project
2. Create your Feature Branch
3. Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact

Gustavo Mirabal Suarez - gst.mirabal@gmail.com

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
