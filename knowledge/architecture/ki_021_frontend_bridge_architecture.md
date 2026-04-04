# KI-021: Frontend Bridge Architecture (Phase 2.8)

## Summary
Architecture decisions and lessons learned from building the CryptoBot V3 Frontend Dashboard Bridge using Vite + React + TypeScript.

## Tags
`frontend`, `react`, `vite`, `tailwind`, `zustand`, `tanstack-query`, `jwt`, `dashboard`

---

## Key Learnings

### 1. Tailwind CSS v4 Configuration
- Tailwind v4 does NOT use `tailwind.config.js`. Configuration is done via the `@tailwindcss/vite` plugin.
- Import in `index.css` is simply `@import "tailwindcss"`.
- The `@apply` directive works but may show IDE lint warnings — these are false positives in Tailwind v4.

### 2. TypeScript verbatimModuleSyntax
- When `verbatimModuleSyntax` is enabled in `tsconfig.json`, type-only imports MUST use `import type { ... }`.
- Mixed imports like `import { authApi, LoginRequest }` will fail if `LoginRequest` is a type.
- Correct: separate into `import { authApi }` + `import type { LoginRequest }`.

### 3. Zustand Persistence with JWT
- `zustand/middleware` provides `persist` with `createJSONStorage(() => localStorage)`.
- Store key should be namespaced: `"cryptobot-auth-storage"`.
- Access token outside React components via `useAuthStore.getState().accessToken`.

### 4. Axios Interceptors for Auth
- Inject Bearer tokens via `apiClient.interceptors.request.use()`.
- Access Zustand state outside React: `useAuthStore.getState()`.

### 5. Django URL Prefix Duplication
- **CRITICAL BUG**: When `config/urls.py` uses `path("api/v1/datafeed/", include("apps.datafeed.urls"))`, the app-level `urls.py` must NOT add another `v1/` prefix.
- This caused a duplicated path: `/api/v1/datafeed/v1/monitor/` instead of `/api/v1/datafeed/monitor/`.

### 6. Redis as System Dependency
- Redis is a system-level service installed via `brew install redis`, NOT a Python package.
- `redis-py` (client) is in the venv; `redis-server` runs at OS level.
- Django's `django-redis` and `django-axes` will throw `ConnectionError` if Redis is not running.

### 7. Discovery Layer (npx autoskills)
- `npx -y autoskills --dry-run` detects project technologies and suggests AI coding skills.
- Skills are installed to `frontend/.agents/skills/` (10 skills for React/TS/Tailwind projects).
- Must run from the directory containing `package.json` for proper detection.

---
*Extracted from Session a6918854-038d-4ad8-9de7-efa47fc230fa*
*Certified: EXTRACTION_COMPLETE: INTELLIGENCE_DESTILLED*
