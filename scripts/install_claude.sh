#!/usr/bin/env bash
echo "[.agents] DEPRECATED: use scripts/install.sh; scripts/install_claude.sh will be removed 2027-02-24" >&2
exec "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/install.sh" "$@"
