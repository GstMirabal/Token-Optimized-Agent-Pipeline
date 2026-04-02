# Project Mapping & Context Manual
Strategic Topology, Environmental Isolation, and Architectural Hierarchy.

## 1. Submodule Integrity & Global Inheritance
- **Rule 34: Federated Architecture:** The `.agents` directory MUST be treated exclusively as a **Git Submodule**. Repositories can reside anywhere in the filesystem (no single-root restriction); the project root is the submodule's parent.
- **Rule 35: Inheritance Lock & Matrix Sovereignty:** (1) Strict veto on flat-copying (`cp -R`). (2) Prohibited local architecture/rule edits; all governance improvements MUST be versioned in the master submodule repository for global propagation via `git submodule update`. (3) **Sovereignty:** Any local copy of `.agents/` that diverges from the constitutional master is invalid.
- **Rule 36: Source of Truth:** Any divergence between local rules and the master governance is a terminal failure. Compliance with the latest global hash is mandatory.

## 2. Environmental Purity & Deterministic Execution
- **Rule 37: Absolute Isolation:** Each project hosts its own `./venv/` or `./node_modules/` directory at the root. Use of global OS binaries (`python`, `pip`, `npm`) is strictly PROHIBITED.
- **Rule 38: Proactive Setup:** If the local environment is missing, the Agent MUST propose immediate initialization (e.g., `make setup`) before any tactical execution.
- **Rule 39: Deterministic Binary Path:** Mandatory use of relative paths for all tool executions (e.g., `./venv/bin/python`, `./node_modules/.bin/`). Naked calls are prohibited even if the shell context appears active.
- **Rule 40: Runtime Anchoring:** Every project MUST include its ecosystem-specific version anchor (e.g., `.python-version`, `.nvmrc`, `go.mod`) in the root for environment reproducibility.

## 3. Project Topography & Hierarchy (Master Navigational Map)
To prevent navigational drift and ensure multi-agent synchronization, all repositories MUST follow this hierarchical topology:

### 3.1: Application Layer (Logic & Tests)
- **Rule 41: Code Hierarchy:** Central logic MUST reside in `/src/`, and testing frameworks in `/tests/`. Computational experiments isolated in `/notebooks/`. Public resources in `/static/`. Customer/media uploads in `/media/` (ignored by Git).

### 3.2: Infrastructure & Persistence (Docker & Data)
- **Rule 42: Infrastructure Lock:** All services (Postgres, Redis) MUST be shielded via `docker-compose.yml`. Physical engine installation on host OS layer is prohibited.
- **Rule 43: Bind Mounts:** Mandatory mapping of DB volumes to hidden directories (e.g., `./.docker-db-data`).
- **Rule 44: Test Isolation:** Agents are PROHIBITED from using development databases for testing. Unit tests MUST use in-memory databases (e.g., `:memory:`) or ephemeral containers.
- **Rule 45: Persistence Policy:** Mass file generation (ETLs, PDFs) must be isolated in `./data/output/` or `./tmp/`.
- **Rule 46: Data-Leak Sieve:** (1) PROHIBITED reading full content of files > 1MB; mandatory metadata scan (`df.info()`, `cat | head`). (2) Heavy files (> 50MB) MUST use `git lfs track`.

### 3.3: Automation & Governance (Makefiles & Logs)
- **Rule 47: Orchestration:** `Makefile` is mandatory. Standard targets: `make setup` (init), `make test` (QA), `make lint` (style), `make clean` (reset).
- **Rule 48: Tracability:** Mandatory `/logs/` directory for production execution traces (ignored by Git ecosystem).

### 3.4: Internal Agent Geography (Matrix Tracking)
All tactical and architectural metadata MUST reside in these ignored locations:
- **Rule 49: Master Local Index:** Located in `.agents/task.md`.
- **Rule 50: Planning Repository:** Sprints and Roadmaps stored in `.agents/task/`.
- **Rule 51: Infrastructure Registry:** Mandatory JSON manifest (`.agents/topology/infra_registry.json`) for automated subagent infra-discovery.
- **Rule 52: Ephemeral Cache:** Mandatory `.agent_state/` for session AST and context traces.

### 3.5: Onboarding & Living Blueprint Bridge
- **Rule 53: Mandatory Retrofitting:** Upon entry, if roadmaps are legacy/incompatible, the Agent MUST propose a **Sprint 000: Retrofitting**. Execution is locked until human-authorization.
- **Rule 54: Bidirectional Sync:** ALL tactical architectural shifts during a Phase MUST be propagated back to the Global Roadmap (Blueprint).
- **Rule 55: High-Value Mirroring:** Finalized architectural designs and roadmaps MUST be mirrored to the project's root `/docs/` for permanent repository history.
- **Rule 56: Topology Audit:** The Agent MUST verify compliance with Rules 34-55 at the start of every session.

## 3.6: Excepciones de Soberanía (Core Matrix)
- **Rule 82: Governance Matrix Exemption:** El repositorio `.agents/`, en su función de núcleo global de gobernanza (Master Submodule), queda estrictamente **EXENTO** del mandato de `Makefile` (Regla 47) y Entorno Local (Regla 37). Esta exclusión previene la contaminación recursiva del núcleo constitucional con artefactos de orquestación de proyectos.
