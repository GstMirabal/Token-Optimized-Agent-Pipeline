# 🛡️ KI 003: Shared Submodule Isolation (Shielding Protocol)

## Context
When using **Universal-Agents (`.agents`)** as a Git Submodule across multiple repositories, a conflict arises: where to store project-specific tasks (`task.md`) and sprints without polluting the global framework repository?

## The Problem
If `task.md` and `sprints/` are tracked inside the submodule directory, any change would force a commit to the framework itself, mixing logic from different projects and causing architectural pollution.

## The Shielding Solution (V1.7 Implementation)
We implemented a **Local-Only State Isolation** within the submodule folder:

1.  **Git Shielding:** The `.agents/.gitignore` now explicitly ignores `task.md`, `sprints/`, `roadmaps/`, and `task/` folders.
2.  **Governance Modification:** `global_user_rules.md` (Rule 38) mandates that task-tracking files are **Project-Local**.
3.  **Physical-Local Strategy:** These files are kept inside the `.agents/` folder for operational convenience but are **Invisible to Git**. 
4.  **Mirroring Deliverables:** High-value documents (Roadmaps) are mirrored to the project's root `docs/` folder for permanent versioning in the main repository.

## Tags
`git`, `submodule`, `governance`, `shielding`, `local-context`
