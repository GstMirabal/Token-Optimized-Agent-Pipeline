# 🛡️ Rule 040: Data Visibility & Vault Sovereignty

## 1. Vault Security (Rule 40.1)
- **Zero-Storage**: User secrets (API Keys, DNI) must NEVER be persisted in `localStorage`, `sessionStorage`, or Redux state in plain text.
- **Masking**: All sensitive secrets retrieved from the backend MUST be boolean indicators (`has_api_key`) or masked strings (`********`).
- **Handshake**: Updating secrets ALWAYS requires a Step-Up Auth handshake (Re-authentication).

## 2. KYC Document Integrity (Rule 40.2)
- **Isolation**: Uploaded documents MUST be stored in private storage (e.g., `kyc_documents/` outside the web root).
- **Naming**: Filenames MUST be randomized using UUID-v4 to prevent ID enumeration.
- **Verification**: Document metadata MUST include `IP Address` and `User-Agent` of the operator at the time of upload.

## 3. Intelligence Hub Aesthetics (Rule 40.3)
- **Data Density**: Dashboards for Market Intelligence MUST prioritize high-density data over whitespace.
- **Normalization**: All price action data (Candles) MUST use institutional color coding (Cian-500 for bullish / Rose-500 for bearish).
- **Transparency**: Every calculated indicator (RSI/ATR) MUST display its "Source Logic" tag in a tooltip.
