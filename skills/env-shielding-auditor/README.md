<h3 align="center">Env-Shielding Auditor</h3>

<p align="center">
  Scans for hardcoded secrets (API keys, tokens) and validates .env security via Gitignore.
</p>

## About The Project

The **Env-Shielding Auditor** is the Matrix's security guard against sensitive-information leaks. It scans source code for hardcoded secrets (API keys, access tokens, PII) and validates that the `.env` file is correctly git-ignored at the root and in submodules.

**Key Features:**
*   **Leak Detection:** Recursive regex-pattern search for provider keys (OpenAI, AWS, GCP, CCXT).
*   **Gitignore Compliance:** Verifies that `.env` and sensitive files are on Git's blacklist.
*   **PII Masking:** Suggests masking personal-data traces in subagent logs.

### Built With

![Bash](https://img.shields.io/badge/bash-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white)
![Security](https://img.shields.io/badge/Security-Shield-red)

## Getting Started

### Prerequisites

*   **Ripgrep (rg)**: Recommended for high-speed scans on large repositories.

### Installation & Configuration

1. **Submodule Access**
   Located at `.agents/skills/env-shielding-auditor/`.

2. **Setup**
   No additional heavy external dependencies required.

## Usage

Invoked manually or by the **DevOps Sentinel** before every atomic commit:

```bash
# Example: preventive secret scan of the current directory
bash .agents/skills/env-shielding-auditor/scripts/shield_audit.sh
```
