#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

command -v python3 >/dev/null 2>&1 || {
  echo "ERROR: Python 3 is required."
  exit 1
}

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi

[ -f .env ] || cp .env.example .env

.venv/bin/python -m pip install -r requirements.txt
exec .venv/bin/python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
