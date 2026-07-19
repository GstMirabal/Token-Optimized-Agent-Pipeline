# 🛡️ Operational Rule: Crowd Intelligence & Prediction Standards

**Context**: High-integrity data normalization and source governance for Prediction Markets and Sentiment indicators.
**Scope**: `backend/apps/datafeed/`, `PolymarketService`, `SentimentIndicator`.

---

## 1. Data Normalization Rule
- **Standard**: ALL external crowd/prediction data MUST be scaled to a **0-100 range** before DB persistence.
- **Formula**: `probability_index = round(external_odds * 100)`.
- **Constraint**: Reject any implementation that stores raw 0.0-1.0 floats in fields intended for the UI Pulse gauge.

## 2. Source Governance
- **Primary Source**: Polymarket (Gamma API) is the single source of truth for "Market Probabilities".
- **Legacy Purge**: Prohibit the use of LunarCrush categories (`social_dominance`, `social_volume`) in new service logic.
- **Filtering**: Reject any prediction event with a 24h trading volume lower than **,000 USD**.

## 3. Asset Mapping Integrity
- **Strict Matching**: Every prediction event MUST be linked to an `Asset` instance via `cmc_id`. 
- **Fallback**: If an asset name from Gamma API cannot be matched with 100% certainty to a CMC ID, the record MUST be discarded to prevent data pollution.

## 4. UI Parity
- **Density Rule**: Any field added to the `SentimentIndicator` or `Prediction` models MUST be exposed in the frontend `MarketPulse` or `AssetExplorer` components. Placeholders are strictly prohibited.

---

**[ENFORCEMENT_LEVEL: CRITICAL]**
**[AUDIT_HOOK: PRE_COMMIT]**
