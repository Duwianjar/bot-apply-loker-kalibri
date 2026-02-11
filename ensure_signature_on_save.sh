#!/usr/bin/env bash
set -euo pipefail

FILE_PATH="$1"

if command -v python3 >/dev/null 2>&1; then
  python3 "${PWD}/ensure_signature.py" "$FILE_PATH"
elif command -v python >/dev/null 2>&1; then
  python "${PWD}/ensure_signature.py" "$FILE_PATH"
else
  echo "Python tidak ditemukan untuk menjalankan ensure_signature.py"
  exit 1
fi
