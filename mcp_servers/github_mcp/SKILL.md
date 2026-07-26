# MCP Synthesis Manifest

name: "github-mcp"
type: "mcp_server"
provider: "Model Context Protocol / NPX"
target_agent: "git_sync_01"
dependency: "node_modules"

## Governance Boundaries
- Jurisdiction explicitly limited to reading/pushing metadata and branch states to `.git` remote URLs.
- Operates under the topological exception established for **MCP Servers**, bypassing standard atomics.
