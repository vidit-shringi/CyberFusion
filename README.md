# CyberFusion

**CyberFusion: An AI-Assisted Multi-Source Cybersecurity Correlation, Risk Prioritization and Digital Forensics Platform**

CyberFusion is a student-scale cybersecurity research prototype that converts isolated security telemetry into explainable, prioritized incidents. It combines deterministic security rules, behavioral anomaly scoring, event correlation, vulnerability intelligence and forensic relationship graphs. The project includes a separate experimental post-quantum cryptography benchmark module named **QuantForensics**.

## What it does

- Normalizes multi-source security events into one schema
- Detects suspicious patterns with explainable rules
- Scores unusual behavior with Isolation Forest (with a safe heuristic bootstrap before a model is fitted)
- Correlates events by time, user, device, IP, session and asset
- Calculates a 0–100 risk score
- Generates incidents with evidence and recommended actions
- Builds a digital-forensic graph using NetworkX
- Enriches vulnerability events with NVD/CISA KEV data
- Provides a synthetic event simulator for repeatable demonstrations
- Includes a research metrics endpoint
- Includes an optional liboqs-based PQC benchmark
- Ships with tests and Docker configuration

## Architecture

```text
Identity / Network / Endpoint / Vulnerability Events
                    |
              Normalization
                    |
              Entity Resolution
                    |
        +-----------+-----------+
        |           |           |
      Rules        AI       Threat Intel
        |           |           |
        +-----------+-----------+
                    |
             Correlation Engine
                    |
                Risk Engine
                    |
             Incident Generator
                    |
           +--------+--------+
           |                 |
      Forensic Graph     Dashboard
```

## Quick start (Windows)

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn backend.main:app --reload
```

Open the complete CyberFusion console at `http://127.0.0.1:8000/`. The FastAPI application serves the frontend, API and static assets from one origin. API documentation is available at `http://127.0.0.1:8000/docs`.

Default local credentials come from `.env` (defaults are `admin` / `ChangeMe123!`). Change them before any public deployment.

## Generate demo events

From the repository root:

```powershell
python simulator/run_demo.py --scenario mixed --events 1000
```

To load the generated file into a running API:

```powershell
python simulator/load_demo.py datasets/synthetic/demo_events.jsonl
```

You can also use **Live Events → Generate demo events** in the UI for an in-app account-compromise scenario.

## API highlights

- `POST /api/auth/login`
- `GET /api/auth/me`
- `POST /api/events`
- `POST /api/events/bulk`
- `GET /api/events`
- `GET /api/incidents`
- `GET /api/incidents/{incident_id}`
- `GET /api/incidents/{incident_id}/events`
- `GET /api/incidents/{incident_id}/graph`
- `PATCH /api/incidents/{incident_id}`
- `GET /api/dashboard/summary`
- `GET /api/dashboard/recent`
- `GET /api/vulnerabilities`
- `POST /api/vulnerabilities/sync/kev`
- `POST /api/vulnerabilities/{cve_id}/sync`
- `GET /api/forensics/graph`
- `GET /api/metrics/snapshot`
- `GET /api/pqc/benchmark`
- `POST /api/demo/generate`

## Research methodology

The repository is designed to compare:

1. Rule-only detection
2. Rule + anomaly detection
3. Rule + anomaly + correlation + threat intelligence

Do not hard-code research results. Load labeled data and calculate precision, recall, F1 and false-positive rate from the actual experiment.

## External data

Optional integrations:

- NVD API 2.x for CVE enrichment
- CISA Known Exploited Vulnerabilities (KEV) catalog

The core application must still run without external API keys.

## PQC / QuantForensics

The PQC module is an experimental research benchmark. It attempts to use `liboqs-python` if available and otherwise reports a clear "unavailable" status. The project does not claim to be fully quantum-secure.

## Docker

```bash
docker compose up --build
```

The Compose stack includes the FastAPI application and PostgreSQL; the FastAPI container serves the complete web console from the same origin.

## Deployment

Recommended academic deployment model:

- Frontend: Cloudflare Pages
- API: Render
- Database: Supabase PostgreSQL

For Render, set:

- `DATABASE_URL`
- `SECRET_KEY`
- `JWT_SECRET`
- `FRONTEND_ORIGIN`
- `ADMIN_PASSWORD`

Do not store secrets in the repository. The Render free service is suitable for demos, not guaranteed always-on production operation.

## Tests

```bash
pytest -q
```

## Safety and research scope

The project is designed for authorized lab data and synthetic demonstrations. Response actions are intentionally recommendations/simulations instead of destructive autonomous actions against third-party systems.

## Project structure

```text
CyberFusion/
├── backend/
│   ├── api/
│   ├── ai/
│   ├── core/
│   ├── database/
│   ├── forensic/
│   ├── pqc/
│   ├── services/
│   ├── config.py
│   ├── simulation.py
│   └── main.py
├── frontend/
├── simulator/
├── datasets/
├── tests/
├── docs/
├── Dockerfile
├── docker-compose.yml
├── render.yaml
├── requirements.txt
└── README.md
```
