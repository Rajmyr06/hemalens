#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if ! command -v brew >/dev/null 2>&1; then
  echo "Homebrew tidak ditemukan."
  exit 1
fi

if ! command -v python3.13 >/dev/null 2>&1; then
  echo "Python 3.13 tidak ditemukan."
  echo "Jalankan: brew install python@3.13"
  exit 1
fi

if ! brew list --versions libomp >/dev/null 2>&1; then
  echo "Menginstal libomp untuk XGBoost..."
  brew install libomp
fi

python3.13 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt

if [[ ! -f .env ]]; then
  cp .env.example .env
fi

python -c "import xgboost; print('XGBoost:', xgboost.__version__)"
python -m scripts.verify_bundle
pytest

echo
echo "Bootstrap HemaLens selesai."
echo "Jalankan: source .venv/bin/activate"
echo "Lalu: uvicorn app.main:app --reload"
