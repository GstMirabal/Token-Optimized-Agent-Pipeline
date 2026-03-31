# 🧠 Knowledge Item: Custom User Model Root Identity Provisioning

## 🚦 Context: Specialized Identity logic
Standard Django `createsuperuser` command does not always respect custom business logic (e.g., `is_verified` flags, UUID generation, signals).

## ⚠️ The Blockage: Broken Identity States
Creating a superuser without satisfying the custom `User` model's constraints (like email verification or profile creation) leads to inconsistent application states.

## ✅ The Solution: Root Bootstrapping (Sprint 004)
1.  **Identity Script**: Created `provision_root.py` to handle the administrator creation via the local app's `CustomUserManager`.
2.  **Auth Consistency**: Root identity uses Email as the primary identifier, satisfying the `USERNAME_FIELD = "email"` configuration.
3.  **Governance Trace**: The first action logged in the `UserSecretAudit` is now the root identity creation, establishing a clear audit trail.

---
`Governance Standard: Phase 3 Operational Infrastructure`
