# 🧠 Knowledge Item: Pytest LocMemCache Isolation Protocol

## 🚦 Context: Infrastructure Friction (Sprint 011)
During architectural audits in environments without active Redis instances (e.g., CI/CD, agent local environment), security tests using `django-redis` for 2FA/Step-Up sessions fail with `ConnectionError`.

## ⚠️ The Blockage: Port 6379 Dependency
Hard-coded Redis dependencies in `settings.py` break the **Quality Isolation (Rule 76)** and prevent 100% Audit Passed certification.

## ✅ The Solution: Shadow Settings (Hardenization)
1.  **`settings_test.py` Layer**: Create a test-specific settings file that inherits from `settings.py`.
2.  **LocMemCache Injection**: Force `django.core.cache.backends.locmem.LocMemCache` for the `default` cache.
3.  **Environment Command**: Execute pytest using `DJANGO_SETTINGS_MODULE=config.settings_test` and ensure `PYTHONPATH=.` is set to resolve the config module correctly.

---
`Governance Standard: Quality Hardening Phase 0`
<!-- slide -->
# 🧠 Knowledge Item: Multi-Tiered Systemic Vault Architecture

## 🚦 Context: Global Secrets Migration (Sprint 011)
Systemic providers (CMC, FRED, CoinGecko) initially relied on `settings.CONFIG` (plaintext), violating **Zero-Trust (Rule 42)** despite having the Identity Vault available.

## ⚠️ The Blockage: User-Centric Vaulting
The existing `UserSecret` model was tied to specific users via `OneToOneField`, preventing a "Global Matrix Secret" from being securely stored and retrieved by the Datafeed services.

## ✅ The Solution: SystemSecret Global Hub
1.  **Global Model**: Implementation of `SystemSecret` model in `Users` with `provider_id` as unique index.
2.  **Cryptographic Hub**: `SecretVaultService` in the Identity Hub to centralize retrieval.
3.  **Hybrid Migration**: services fetching keys prioritized from the vault: `Vault.get_key() or settings.CONFIG['KEY']`.

---
`Governance Standard: Military-Grade Security Phase 3`
<!-- slide -->
# 🧠 Knowledge Item: Rule 10 Modularization Heuristic

## 🚦 Context: Architecture Divergence (Sprint 011)
Django default `tests.py` files allow for quick development but cause a "Structural Breach" in Rule 10 (Decoupling) as complexity grows.

## ⚠️ The Blockage: Monolithic Smothering
As services, models, and API layers grow, a single `tests.py` file becomes unmanageable and violates the modularity of the **Universal-Agents Methodology**.

## ✅ The Solution: Early Fragmenting (Clustering)
1.  **Test Clusters**: Every app MUST transition from `tests.py` to a `tests/` directory with `__init__.py` before reaching 25% implementation.
2.  **Categorization**: Split into `test_services.py`, `test_api.py`, and `test_models.py` to ensure atomic audit success.

---
`Governance Standard: Modular Architecture Rule 10`
