# Rule Context: Project Topology

This document explicitly defines the strict structural routing inside the active project workspace. This context is loaded when operations involve modifying directory setups, deploying frameworks, or orchestrating database services.

## 1. Local Deterministic Execution
- **Strict Virtual Paths**: The use of global OS binaries (e.g., raw `python`, `npm`, `pip`) is absolutely **PROHIBITED**. Agents must imperatively employ deterministic local paths linked to the project context (e.g., `./venv/bin/python`, `./node_modules/.bin/npx`).
- **Binary Root Anchor**: Every valid workspace must expose its versioning file (e.g., `.nvmrc` or `.python-version`) to shield the local environment from system interference.

## 2. Infrastructure & Databases (Data-Leak Sieve)
- **Container Exclusivity**: Local databases or broker services (Postgres, Redis) must run purely via `docker-compose.yml`. Emulating or installing engines on the host OS is forbidden.
- **Physical Volume Sieve**: Agents must map persistent DB states forcefully into the hidden local directory `./.docker-db-data` to prevent accidental tracking.
- **Testing Purity**: Utilizing the local development database for Unit/Integration testing is **PROHIBITED**. Tests must dynamically instantiate purely ephemeral DB layers (e.g., `sqlite:///:memory:`).

## 3. Data Persistence Policy
- **Mass Generation**: Scripts generating ETL outputs, PDFs, or raw heavy logs must dump directly to `./data/output/` or `./tmp/` and exclude themselves from the repository tracking index.
- **Payload Reading Limiter**: Direct raw inspection (`cat`, full read) of unmasked documents > 1MB is banned. Agents must query using strictly AST chunking, `head`, `tail`, or metadata extraction limits to preserve the context window.
