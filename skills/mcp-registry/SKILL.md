---
name: mcp-registry
description: Mandatory skill for the Orchestrator. Defines the standard registry and routing protocol for local and remote Model Context Protocol (MCP) servers. Use this to bind subagents to specific external contexts.
---

# 🌐 Skill: MCP Registry & Router

## ⚠️ When to Trigger this Skill?
This skill is **exclusively reserved for The Orchestrator**. 
During the Technical Design phase (Plan) and Step Zero (DevOps), the Orchestrator MUST consult the `registry.json` file located in this directory whenever a task requires external data sources (e.g., PostgreSQL, GitHub API, external file systems) that go beyond standard local code reading.

## 🛠️ How it Works (Instructions)

**Step 1: Context Discovery (Plan Phase)**
Before finalizing the `implementation_plan.md`, read `.agents/skills/mcp-registry/registry.json` (and the active profile's `profiles/[name]/mcp/registry.json`, if one is installed). Identify if there is an active/available MCP server that matches the task requirements. If the MCP does not exist, you must propose adding it to the human.

**Step 2: Subagent Routing**
If an MCP is required, explicitly state in your `implementation_plan.md` which subagent gets authorization for which MCP. 
*Example:* "Agent [Database Auditor] is statically routed to use the `postgres-mcp` defined in the registry."
Remember: Subagents cannot auto-discover MCPs. If it is not in the plan, they cannot use it.

**Step 3: Provisioning (Step Zero - DevOps)**
During execution Step Zero, prior to the subagents acting, the Orchestrator must verify that the designated MCP servers are provisioned. If an MCP server requires initialization, the Orchestrator must execute its startup command dynamically — local-process servers MUST launch via `pnpm dlx` (never `npx -y`, per agents.md §8).

## 🔴 Security and Zero-Trust Authorization
No external API or Model Context Protocol may be added to `registry.json` without the explicit approval of the Human User. The Orchestrator can propose the JSON structure, but it must wait for explicit human authorization (chat confirmation or Claude Code permission prompt) to commit the new tool to the registry.
