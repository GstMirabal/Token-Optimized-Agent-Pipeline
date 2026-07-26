# MCP Registry & Manager

## About The Project

The **MCP Registry & Manager** is the pipeline's external-data discovery system. It manages the configuration and routing of local and remote Model Context Protocol (MCP) servers, letting subagents expand their knowledge frontier in a safe, audited way. Project-specific servers (e.g. market-data feeds) live in `profiles/[name]/mcp/registry.json`.

**Key Features:**
*   **Centralized Registry:** A single source of truth in `registry.json` for all external connections.
*   **Zero-Trust Routing:** Ensures only registry-authorized MCPs can be invoked by the Orchestrator.
*   **Dynamic Provisioning:** Safely injects environment variables and API secrets.

### Built With

![JSON](https://img.shields.io/badge/json-5E5E5E?style=for-the-badge&logo=json&logoColor=white)
![MCP](https://img.shields.io/badge/MCP-Registry-brightgreen)

## Getting Started

### Prerequisites

*   **Claude / LLM Platform**: Model capability to interact with MCP servers.
*   **MCP Server Configuration**: Persistent location of server credentials in `.env` or the global configuration file.

### Installation & Configuration

1. **Integrated in Core**
   Located at `.agents/skills/mcp-registry/`.

2. **Register a Server**
   Add your new server to `registry.json` following the official metadata schema (local-process commands must use `pnpm dlx`, per agents.md §8).

## Usage

The **Orchestrator** consults the registry before any task requiring real-time external data. If a server is not in `registry.json` (or the active profile's registry), external access is blocked. Free-tier API credits are prioritized over paid calls.

```bash
# Example: viewing active servers in the registry
cat .agents/skills/mcp-registry/registry.json
```

## Contributing

1. Fork the Project
2. Create your Feature Branch
3. Pull Request
