# 🧠 Domain Memory: CryptoBot Master Mapping (V3)

## Architectural Source: `ARCHITECTURE_FLOW.md`
**KI Code**: `ki_012_domain_mapping_v3`
**Security Level**: P-1 (Certified)

---

## 🏛️ Physical Domain Inventory (backend/apps/)

| Domain | Module | Status | Logic Density | Implementation Focus |
| :--- | :--- | :--- | :---: | :--- |
| **Identity** | `users` | ✅ 100% | High | JWT + AES-256 Fernet Vault + Step-Up Auth. |
| **Data Ops** | `datafeed` | ⚠️ 60% | Medium | CCXT REST Ingestion. WebSocket (Blocked). |
| **Analysis** | `tech_analysis`| 🕒 15% | Low | Correlation & Sector Momentum (Services). |
| **Strategies**| `strategies` | 🚫 0% | Void | Pre-deployment scaffolding. |
| **Trading** | `live_trading` | 🚫 0% | Void | Placeholder for order loops. |
| **Risk** | `risk_control` | 🚫 0% | Void | Redis Pre-Trade validation placeholder. |

---

## 🛡️ Critical Protocols Certified (V3)
1.  **Rule 34 (Federated Architecture)**: .agents submodule is the ONLY source of governance.
2.  **Rule 36 (Source of Truth)**: No duplication of governance in the project root.
3.  **Rule 71 (Localization)**: Project-specific design stays in root `/docs/`.

---

> [!IMPORTANT]
> **Audit Conclusion**: The scaffolding is 100% complete for all 11 domains. Any subagent MUST utilize the existing `backend/apps/` structure and MUST NOT create new top-level applications unless authorized by the Agente Principal.
