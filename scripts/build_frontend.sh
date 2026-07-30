#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if ! command -v node >/dev/null 2>&1; then
  echo "Node.js tidak ditemukan. Instal Node.js 22 atau versi LTS yang kompatibel."
  exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
  echo "npm tidak ditemukan."
  exit 1
fi

npm install
npm run build

echo "Frontend HemaLens selesai dibangun."
