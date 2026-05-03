# Knowledge Item: Market Intelligence Ingestion & Resiliency (KI-047)

## 🎯 Context
This intelligence was distilled from **Sprints 045-047**, focused on the high-fidelity integration of macro, derivatives, and liquidity data into the CryptoBot terminal.

## 🛠️ Systemic Resilience (The Circuit Breaker)
*   **CCXT Rate-Limit Defense**: Implemented `resilience_circuit_breaker` specifically for Binance Futures endpoints.
*   **Logic**: Monitoring the `x-mbx-used-weight` headers to preemptively throttle requests during high-volatility spikes, preventing IP bans.

## 🏗️ Architectural Patterns
*   **Widget Scope Sovereignty**: To prevent false-positive IDE errors and path resolution regressions in high-density frontend widgets (e.g., `Dashboard.tsx`), the use of **Absolute Imports** (mapped in `tsconfig.json`) is mandatory for all UI icons and sub-components.
*   **Environment Parity Protocol**: Management commands involving data ingestion MUST verify the presence of `MASTER_KEY` and `DJANGO_SECRET_KEY`. 
    *   *Correction*: Explicitly export these variables in the terminal session to satisfy `ImproperlyConfigured` checks before initiating sync tasks.

## 📈 Functional Integration
*   **Macro-Correlation Engine**: Automated FRED ingestion now correlates frequency-adjusted data (e.g., Weekly vs. Monthly) using a standardized `MacroIndicator` metadata schema.
*   **Liquidity Mapping**: "Gravity Zones" implemented via cluster analysis of Binance Futures liquidation data.

## 🐛 Forensic Memory
*   **Import Regression**: Missing `Magnet` icon in `Dashboard.tsx` resolved by verifying component scope within the atomic UI folder.
*   **Model Relaxation**: `MacroIndicator` refactored to support dynamic frequency mapping, allowing for non-destructive schema updates.

---
*Generated via Extract Workflow (v4.0.0).*
