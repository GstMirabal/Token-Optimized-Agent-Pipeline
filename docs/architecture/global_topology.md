# 🌐 Global Framework Architecture (.agents)

This document provides a high-level visual representation of the Universal-Agents framework architecture and its internal interconnections.

## 1. Macro-Component Connectivity

The following diagram illustrates the flow of governance, intelligence, and execution within the Matrix.

```mermaid
flowchart TD
    subgraph Governance_Nucleus [Governance Nucleus]
        agents_md[agents.md] --> roles[Agent Roles]
        agents_md --> rules[Global Rules]
    end

    subgraph State_Control [State & Scaffolding]
        active_state[active_state.json] -- Anchor --> docs[docs/ tree]
        mapper[Matrix Mapper] -- Injects --> docs
    end

    subgraph Execution_Engine [Execution & Logic]
        workflows[workflows/] -- Orchestrates --> skills[skills/]
        skills -- Operates --> project[Host Project]
    end

    subgraph Memory_Buffer [Sovereign Memory]
        project -- Distills --> extractor[Knowledge Extractor]
        extractor -- Persists --> memory[memory/]
    end

    %% Interconnections
    Governance_Nucleus -- Constrains --> Execution_Engine
    State_Control -- Guides --> Execution_Engine
    Execution_Engine -- Reports --> State_Control
    Memory_Buffer -- Informs --> Execution_Engine
```

## 2. Core Functional Layers

### 🏛️ Layer 1: Governance (The Constitution)
The Foundation of the Matrix. It defines the "Legal" boundaries of any operation. No subagent or workflow can bypass the rules defined in `agents.md`.

### ⚓ Layer 2: Scaffolding & State (The Anchor)
The Operational Truth. Controlled by the **Matrix Mapper**, this layer ensures that every session has a clear point of origin and a standardized geography through the `/docs/` tree.

### ⚡ Layer 3: Orchestration (The Brains)
The Tactical Logic. Controlled by the **Orchestrator** and **Doc Orchestrator**, this layer translates strategic roadmaps into actionable tasks and hardened documentation.

### 🛠️ Layer 4: Execution (The Arsenal)
The Physical Impact. Highly specialized **Skills** (local and 3rd party) perform the actual code manipulation and quality audits under the command of Layer 3.

## 3. Communication Bridge
Inter-agent communication is managed through **Contracts** located in `docs/contracts/`. These files define the technical interfaces and I/O expectations for every functional handoff.
