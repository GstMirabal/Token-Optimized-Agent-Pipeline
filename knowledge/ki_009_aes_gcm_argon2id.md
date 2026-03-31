# 🧠 Knowledge Item: AES-256-GCM & Argon2id Hardening

## 🚦 Context: Security Upgrade
The initial implementation used **Fernet** (symmetric encryption), which lacks modern authenticated encryption (AEAD) and key derivation (KDF) standards suitable for high-value API keys.

## ⚠️ The Blockage: Brute Force & Integrity
Plain symmetric encryption without a robust KDF makes the Master Key vulnerable to brute-force attacks and bit-flipping during transit.

## ✅ The Solution: Military-Grade Vault (Sprint 004)
1.  **AES-256-GCM**: Adopted Authenticated Encryption to ensure both privacy and data integrity.
2.  **Argon2id (KDF)**: Using `argon2-cffi` to derive working keys from the `MASTER_KEY`.
    *   **Params**: `time_cost=3`, `memory_cost=65536`, `parallelism=4`.
3.  **RAM-Safe Buffer**: The derived key is cached in memory but initialized only on demand, preventing clear-text Master Key exposure after derivation.

---
`Governance Standard: Phase 3 Operational Infrastructure`
