# 🛡️ Rule 041: Frontend Modular Standard (Matrix V2)

## 1. Directory Anatomy (Rule 41.1)
Every module inside `frontend/src/modules/` must adhere to the following minimum structure to guarantee interoperability and isolation:
- `pages/`: Contains route-level views exclusively (suffix: `View.tsx`).
- `components/`: Atomic or molecular components specific to the module's domain.
- `api/`: Interface definitions and backend communication services.
- `hooks/`: Encapsulated state and effect logic.
- `store/`: (Optional) Module-specific global state definitions (Zustand/Redux).
- `index.ts`: The module's **Public API**. Only what is exported here is accessible from outside the module.

## 2. Cross-Module Communication (Rule 41.2)
- **Zero-Leaking**: Importing files directly from another module's subfolders is strictly **PROHIBITED** (e.g. `import { UserCard } from "@/modules/users/components/UserCard"` is ILLEGAL).
- **Public Access**: Cross-module imports must go through the module's root entry point (e.g. `import { UserCard } from "@/modules/users"`).

## 3. UI Consistency (Rule 41.3)
- **Sovereign Aesthetic**: All module components must inherit the design tokens defined in `SovereignLayout` and use `framer-motion` for view-state transitions.
- **Loading States**: Every `View.tsx` must implement a loading state (Skeleton or premium Loader) while API promises resolve.

---
*Effective since: 2026-05-07*
*Status: ACTIVE*
