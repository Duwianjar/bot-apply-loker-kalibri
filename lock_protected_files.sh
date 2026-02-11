#!/usr/bin/env bash
set -euo pipefail

TARGET_FILES=("README.md")

chflags uchg "${TARGET_FILES[@]}"
echo "File berhasil di-lock: ${TARGET_FILES[*]}"
