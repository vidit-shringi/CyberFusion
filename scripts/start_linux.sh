#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
[ -f .env ] || cp .env.example .env
exec .venv/bin/python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
