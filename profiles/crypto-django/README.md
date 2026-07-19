# 📦 Profile: crypto-django

Project-specific pack for **crypto/trading platforms built on Django + React**. It preserves the self-learning accumulated by that project family (crowd-intelligence standards, KYC/vault rules, identity specialists, market-data MCP servers) without contaminating hosts that don't need it.

## Contents
| Path | What it adds |
| :--- | :--- |
| `rules/crowd_intelligence_standards.md` | Polymarket/prediction-market data normalization rules. |
| `rules/data_visibility_and_vault.md` | Secret/PII storage, KYC document handling, dashboard density. |
| `agents/backend_identity_specialist.md` | Django identity/auth developer (jurisdiction `backend/apps/users/`). |
| `agents/frontend_ux_hardener.md` | React/TS UX developer (jurisdiction `frontend/src/`). |
| `skills/polymarket-gamma-3rd/` | Polymarket Gamma API bridge for crowd-intelligence ingestion. |
| `mcp/registry.json` | Market-data MCP servers (CoinMarketCap, CoinGecko, FRED, yfinance, CCXT). |

## Installation (opt-in only)
The base installer never links profiles. From the host project root:

```bash
.agents/scripts/install_claude.sh --profile crypto-django
```

This additionally symlinks the profile's `agents/` and `skills/` into the host `.claude/` tree and appends `@`-imports for the profile's `rules/` to the host `CLAUDE.md`.

## Governance
- Profile contents follow the same constitution (`agents.md`) as the core framework.
- New project-specific learning goes **here** (or into a new `profiles/[name]/`), never into the framework's core `rules/`, `agents/`, or `skills/` (agents.md §3 `topological_order`).
