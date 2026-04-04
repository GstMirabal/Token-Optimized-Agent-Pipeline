# 🧠 KI-001: Survival Mode for Market Ingestion (Debug Strategy)

**Domain**: `devops/workflow`
**Version**: 1.0.0
**Status**: `CERTIFIED`
**Tag**: `django`, `debug`, `efficiency`, `market-data`

---

## 🏛️ Context & Rationale
During high-frequency backend development (Phase 2), full synchronization of thousands of assets and historical candles (OHLCV) saturates local databases and exhausts API quotas. To protect the developer experience (Rule 2.11), a "Survival Mode" is required to prioritize speed over exhaustiveness.

## 🛠️ Implementation Pattern
In the management commands or Celery tasks responsible for ingestion:

1.  **Environment Detection:** Check `settings.DEBUG`.
2.  **Tier Filtering:** If in Debug, filter `Asset.objects.filter(tier=1)` (Top 100 assets) to reduce the ingestion surface.
3.  **Count Override:** Lower the historical candle requirement (e.g., from 1000 to 100) to ensure immediate availability of data for testing indicators.

## 🛡️ Safeguards
- This policy MUST only trigger when `DEBUG` is `True`.
- It should be clearly logged in the terminal to avoid confusion with production-ready full audits.

---
*Certified under Roadmap 008 - Matrix Strategic Intelligence*
