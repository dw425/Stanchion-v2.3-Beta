#!/usr/bin/env bash
# Stanchion universal installer (macOS / Linux). Fetches install.py and runs it.
#   curl -fsSL https://raw.githubusercontent.com/dw425/Beta_V1.8_UAT/main/install.sh | bash
set -euo pipefail
TMP="$(mktemp -t stanchion-install-XXXX.py)"
URL="https://raw.githubusercontent.com/dw425/Beta_V1.8_UAT/main/install.py"
if command -v curl >/dev/null 2>&1; then curl -fsSL "$URL" -o "$TMP"; else wget -qO "$TMP" "$URL"; fi
PY="$(command -v python3 || command -v python)"
exec "$PY" "$TMP" "$@"
