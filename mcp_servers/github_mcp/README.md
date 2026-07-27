# Git Sync Agent MCP (Model Context Protocol)

This directory serves as the official node for the `@modelcontextprotocol/server-github` module.
It conforms to the pipeline policy of keeping MCP servers structurally distanced from standard atomic scripts into the `mcp_servers/` space. 

## Requirements
- **Node/NPX** installed on the host environment natively.
- **Environment Variable**: `GITHUB_PERSONAL_ACCESS_TOKEN` must be sourced prior to execution.

## Setup (Manual)
1. Create `.agents/.env` with a single line: `GITHUB_PERSONAL_ACCESS_TOKEN=<your-token>` (classic PAT with `repo` scope). This file is git-ignored — never commit it.
2. The server script will automatically validate the presence of this variable.

## Usage
The standard invocation handles JSON-RPC standard communication required by Model Context Protocols. It is designed to be attached strictly via the parent IDE MCP settings or via orchestrated proxy calls by the `git_sync_01` agent.
