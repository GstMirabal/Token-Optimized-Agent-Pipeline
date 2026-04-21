# 🧠 Knowledge Item: Antigravity Monorepo Module Resolution

**ID**: KI-040  
**Domain**: Architecture / Tooling  
**Status**: DRAFT (Pending Approval)  
**Ref**: Sprint 039 / Audit V2

## 📝 Problem Statement
In monorepo structures (e.g., `backend/` as a sub-directory), static analysis engines in the **Antigravity** environment may fail to resolve sub-packages (like `apps.*`) if the import root is strictly bound to the git root.

## 🛡️ Resolution Strategies

### 1. Linguistic Parent Navigation (Relative Imports)
When importing between sibling packages within the monorepo root (e.g., from `config/` to `apps/`), use relative parent imports to help the linter trace the physical path:
- **Correct**: `from ..apps.core.views import HealthCheckView`
- **Avoid**: `from apps.core.views import HealthCheckView` (if not explicitly added to path).

### 2. Physical Bridge (Symbolic Links)
To maintain the "clean" `apps.xxx` syntax preferred by Django while satisfying a root-bound linter, create symbolic links in the project root:
```bash
ln -s backend/apps apps
ln -s backend/config config
```
This tricks the linter into seeing the packages at the level it expects without duplicating code.

### 3. Structural Signal (`pyproject.toml`)
Explicitly define the execution environment root for Pyright:
```toml
[tool.pyright]
executionEnvironments = [
  { root = "backend" }
]
analysis.extraPaths = ["backend", "backend/apps"]
```

## ⚠️ Warning
Always verify that relative parent imports (`..`) do not break Django unit tests when run from the `backend/` directory. If they do, the symbolic link approach is the most stable "Antigravity-compatible" solution.
