#!/bin/bash
# 🛡️ MCP Health Check: GitHub Sentinel
# Version: 1.0.0

# Protocol: Safe Export (No-Parser)
# This script is called by the DevOps Sentinel to verify API connectivity.

# Set Working Directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"

# 1. Load Environment (Export Only)
if [ -f "$PARENT_DIR/.env" ]; then
    export $(grep -v '^#' "$PARENT_DIR/.env" | xargs)
else
    echo "❌ [HEALTH_CHECK] Error: .env file missing in root."
    exit 1
fi

# 2. Validate Token Existence
if [ -z "$GITHUB_PERSONAL_ACCESS_TOKEN" ]; then
    echo "❌ [HEALTH_CHECK] Error: GITHUB_PERSONAL_ACCESS_TOKEN not defined in environment."
    exit 1
fi

# 3. API Handshake (Curl)
echo "🔍 [HEALTH_CHECK] Verifying GitHub API connectivity..."
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: token $GITHUB_PERSONAL_ACCESS_TOKEN" https://api.github.com/user)

# 4. Certification
if [ "$RESPONSE" == "200" ]; then
    echo "✅ [HEALTH_CHECK] GitHub Sentinel: Connection established successfully."
    exit 0
else
    echo "❌ [HEALTH_CHECK] Error: API returned HTTP $RESPONSE. Check token validity and network."
    exit 1
fi
