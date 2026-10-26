#!/usr/bin/env bash
echo "[.agents] DEPRECATED: use scripts/install.py; scripts/install_claude.sh will be removed 2027-02-24" >&2
exec "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/install.sh" "$@"
