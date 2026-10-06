# Deployment Guide

## Local
1. Create `.env` from `.env.example`.
2. Install dependencies with `python -m pip install -r requirements.txt`.
3. Start FastAPI with Uvicorn.
4. Open `http://127.0.0.1:8000/`; FastAPI serves the complete frontend and API from one origin.

## Docker
`docker compose up --build` starts PostgreSQL and the FastAPI service.

## Render
Deploy the repository as a Python web service:
`uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
Set `DATABASE_URL`, `SECRET_KEY`, `JWT_SECRET`, `FRONTEND_ORIGIN`, and `ADMIN_PASSWORD`.

## Supabase
Use a PostgreSQL connection string in `DATABASE_URL`. Enable SSL and use the connection mode recommended by your deployment environment.

## Cloudflare Pages
A separate static frontend is optional. If used, set `window.CYBERFUSION_API` to the public API URL in `frontend/config.js`. The default deployment is same-origin and requires no second frontend server.
