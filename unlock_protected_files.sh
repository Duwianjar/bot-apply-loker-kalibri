#!/usr/bin/env bash
set -euo pipefail

PIN_REQUIRED="1234"
TARGET_FILES=("README.md")

read -r -s -p "Masukkan PIN untuk unlock file: " pin
printf "\n"

if [[ "$pin" != "$PIN_REQUIRED" ]]; then
  echo "PIN salah."
  exit 1
fi

chflags nouchg "${TARGET_FILES[@]}"
echo "File berhasil di-unlock: ${TARGET_FILES[*]}"
