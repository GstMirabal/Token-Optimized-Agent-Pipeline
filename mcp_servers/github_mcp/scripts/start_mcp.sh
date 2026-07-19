#!/usr/bin/env bash
# Execution Wrapper for GitHub MCP Server
# Ensure GITHUB_PERSONAL_ACCESS_TOKEN is exported

set -e

if [ -z "$GITHUB_PERSONAL_ACCESS_TOKEN" ]; then
    echo "ERROR: GITHUB_PERSONAL_ACCESS_TOKEN is missing or not exported." >&2
    exit 1
fi

echo "Starting @modelcontextprotocol/server-github proxy..."
# pnpm dlx per agents.md §8 (npm/npx prohibited; supply-chain shield).
pnpm dlx @modelcontextprotocol/server-github
