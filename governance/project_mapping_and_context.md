# Project Mapping and Context
Exclusive Rules for Filesystem and Local OS Topology.

## 1. Location and Base Space
- **Single Root:** All repositories must forcibly reside under a single root or organizational directory defined by the human (e.g., `$HOME/Developer/`).
- **Propagation of the `.agents` Repository (Copying Blocked):** The master AI directory (this repository) must be treated as the source of truth. Every new project requires integrating this matrix mandatory as a **Git Submodule** (`git submodule add <url_or_path_to_master_repo>`). **ABSOLUTE LAW:** It is strictly prohibited to use flat copying (`cp -R`); if copying is used, projects become disconnected from global improvements.
- **Self-Improvement and Centralization (Git):** Any refactoring of these rules and manuals by the Auditor agent **IS STRICTLY PROHIBITED** on the local copies of each project. Any self-improvement to the constitution or skills must be executed and versioned mandatory on the original master repository to ensure global inheritance.

## 2. Virtual Environments (venv)
- **Isolation:** Each project hosts its own `./venv/` directory at the root. All global installations (`pip install`) are prohibited.
- **Path Anchor:** Agents must forcibly position themselves with `cd` at the project root before executing any tools.
- **Binary Execution:** Prohibited to use global commands (`python`, `pip`). Imperatively call local binaries (e.g., `./venv/bin/python`, or `./node_modules/.bin/`).

## 3. Code Layout (Src Layout)
- **Central Logic:** `/src/`
- **Testing Framework:** `/tests/`
- **Web Components:** In web architectures: `/static/` (public resources) and `/media/` (customer-uploaded files, prohibited in version control).
- **Jupyter Notebooks:** Computational tests in Jupyter must be isolated in `/notebooks/`.

## 4. Persistence and Databases
- **Exclusive Engine:** Infrastructure deployment (e.g., PostgreSQL, Redis) mandatory shielded through `docker-compose.yml`. Installation of physical database engines on the macOS OS layer is strictly prohibited.
- **Bind Mounts:** Mandatory mapping of database volumes to hidden local directories (e.g., `./.docker-db-data`) to ensure data persistence.
- **Temporary Files/Reports:** Mass file generation (ETLs, PDFs) must be isolated in `./data/output/` or `./tmp/`.
- **Git LFS:** Heavy files (>50MB, e.g., models, large CSV datasets) must forcibly be tracked using `git lfs track`.

## 5. Repository Governance
- `.python-version` anchored to the project root, specifying the base Pyenv version.
- Strict `.gitignore`, inherently excluding: `/venv/`, `.env`, `.agent_state/`, temporals, logs, and datasets (`/data/`).
- `Makefile` (or similar orchestrator like `Taskfile`) is mandatory to centralize repetitive workflows (`make test`, `make db-up`).
- Exclusive `/logs/` directory for dumping production execution traces.
