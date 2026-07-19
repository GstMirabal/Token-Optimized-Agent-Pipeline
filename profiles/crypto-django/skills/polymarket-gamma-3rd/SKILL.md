---
name: polymarket-gamma
description: Ingests real-world event probabilities from the Polymarket Gamma API for asset sentiment analysis.
---

# ♟️ Skill: Polymarket Gamma API Bridge

## 1. Tactical Purpose
This skill empowers the Backend Specialist to fetch, filter, and normalize prediction market data from Polymarket. It is the primary data source for the "Crowd Intelligence" layer.

## 2. Usage Protocol
- **Endpoint**: `https://gamma-api.polymarket.com/events`
- **Filter Rule**: Only ingest events with `volume > 10000`.
- **Normalization**: Convert `price` (0.0 - 1.0) to a `probability_index` (0 - 100).

## 3. Implementation Steps
1.  **Discovery**: Search for events matching asset names (e.g., "Bitcoin", "Ethereum").
2.  **Validation**: Verify the market is active (`closed: false`).
3.  **Extraction**: Pull the `last_trade_price` for the 'Yes' outcome.

## 4. Dependencies
- Python `requests` library.
