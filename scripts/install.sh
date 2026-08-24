#!/usr/bin/env bash
# Thin wrapper — the actual installer logic lives in install_claude.py
# (portable: works on macOS/Linux, and on Windows via `python3 install_claude.py`,
# where it degrades symlinks to copies if Developer Mode is off).
set -euo pipefail
exec python3 "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/install.py" "$@"
