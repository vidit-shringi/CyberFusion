# 🛡️ CyberFusion

### AI-Assisted Multi-Source Cybersecurity Correlation, Risk Prioritization & Digital Forensics

<p align="center">
  <strong>Security intelligence, correlated.</strong><br>
  From isolated telemetry to explainable, investigable incidents.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.12">
  <img src="https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/CI-GitHub%20Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white" alt="CI">
</p>

---

## ✦ What is CyberFusion?

**CyberFusion** is a full-stack cybersecurity intelligence and investigation platform designed to reduce the noise created by isolated security alerts.

Instead of treating every event as a separate alert, CyberFusion combines:

**Telemetry → Rules → Behavioral Anomaly → Correlation → Risk → Incident → Forensic Investigation**

The project is intentionally explainable. A high-risk result should be traceable to the events, rules, behavioral signals and contextual evidence that contributed to it.

> **Academic / engineering scope:** CyberFusion is a complete student-scale functional prototype for authorized laboratory data, synthetic datasets and controlled research evaluation. It is not positioned as an enterprise SIEM replacement, autonomous offensive-security system or guaranteed production-scale security platform.

---

## ⚡ Core capabilities

| Capability | Status |
|---|---|
| Multi-source event ingestion | ✅ Implemented |
| Event normalization | ✅ Implemented |
| Rule-based detection | ✅ Implemented |
| Behavioral anomaly scoring | ✅ Implemented |
| Isolation Forest support | ✅ Implemented |
| Event correlation | ✅ Implemented |
| 0–100 risk prioritization | ✅ Implemented |
| Incident generation | ✅ Implemented |
| Evidence and analyst recommendations | ✅ Implemented |
| Asset inventory | ✅ Implemented |
| NVD vulnerability enrichment | ✅ Implemented |
| CISA KEV enrichment | ✅ Implemented |
| Digital-forensic relationship graph | ✅ Implemented |
| Synthetic security-event simulator | ✅ Implemented |
| Research metrics | ✅ Implemented |
| JWT authentication | ✅ Implemented |
| Password hashing | ✅ Implemented |
| Docker + PostgreSQL | ✅ Configured |
| Render deployment | ✅ Configured |
| GitHub Actions CI | ✅ Configured |
| CodeQL | ✅ Configured |
| Optional PQC benchmarking | ✅ Implemented / runtime-dependent |

---

## 🧠 Architecture

~~~text
 ┌──────────────────────────────────────────────────────────┐
 │                    SECURITY TELEMETRY                    │
 │ Identity • Network • Endpoint • Asset • Vulnerability  │
 └─────────────────────────────┬────────────────────────────┘
                               │
                               ▼
                    ┌───────────────────┐
                    │ Event Ingestion   │
                    │ + Normalization   │
                    └─────────┬─────────┘
                              │
              ┌───────────────┼────────────────┐
              ▼               ▼                ▼
        ┌──────────┐   ┌─────────────┐  ┌─────────────┐
        │   Rules  │   │ Behavioral  │  │ Threat      │
        │  Engine  │   │  Anomaly AI │  │ Intelligence │
        └────┬─────┘   └──────┬──────┘  └──────┬──────┘
             │                │                │
             └────────────────┼────────────────┘
                              ▼
                    ┌───────────────────┐
                    │ Correlation Engine│
                    └─────────┬─────────┘
                              ▼
                    ┌───────────────────┐
                    │    Risk Engine    │
                    │      0 — 100      │
                    └─────────┬─────────┘
                              ▼
                    ┌───────────────────┐
                    │ Incident Generator│
                    └─────────┬─────────┘
                              │
                ┌─────────────┴─────────────┐
                ▼                           ▼
       ┌─────────────────┐        ┌──────────────────┐
       │ SOC Dashboard   │        │ Digital Forensics│
       │ Timeline / Risk │        │ Entity Graph     │
       └─────────────────┘        └──────────────────┘
~~~

---

# 🚀 Quick Start

## Windows — recommended

From the repository root:

~~~powershell
scripts\start_windows.bat
~~~

The launcher automatically:

1. verifies Python
2. creates .venv
3. creates .env
4. installs dependencies using Python module invocation
5. starts FastAPI
6. waits for the health endpoint
7. opens the browser

### Why Python module invocation?

Some Windows systems block direct execution of downloaded pip.exe through Device Guard / Smart App Control.

CyberFusion therefore uses:

~~~powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
~~~

instead of directly launching pip.exe.

If your organization blocks Python package installation completely, use the Docker deployment method or an approved development environment.

---

# 🔐 Local Administrator

The default **local development** administrator is:

| Field | Value |
|---|---|
| Username | **admin** |
| Password | **ChangeMe123!** |
| Role | **admin** |

### Local URLs

| Service | URL |
|---|---|
| CyberFusion Console | http://127.0.0.1:8000/ |
| Swagger API | http://127.0.0.1:8000/docs |
| Health Check | http://127.0.0.1:8000/api/health |

> ⚠️ **Security:** these credentials are for local development only. Change ADMIN_PASSWORD, SECRET_KEY and JWT_SECRET before any network/public deployment.

---

# 🐧 Linux / macOS

~~~bash
bash scripts/start_linux.sh
~~~

Or manually:

~~~bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
~~~

---

# 🐳 Docker

CyberFusion includes a complete Docker path with PostgreSQL.

~~~bash
docker compose up --build
~~~

Open:

~~~text
http://127.0.0.1:8000/
~~~

Stop:

~~~bash
docker compose down
~~~

Reset the local PostgreSQL volume:

~~~bash
docker compose down -v
docker compose up --build
~~~

> docker compose down -v intentionally deletes the local database volume.

### Container architecture

~~~text
┌──────────────────────┐
│   CyberFusion API    │
│      FastAPI         │
│      :8000           │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│    PostgreSQL 16     │
│      :5432           │
└──────────────────────┘
~~~

The Docker image runs as a non-root cyberfusion user and contains a health check for /api/health.

---

# ☁️ Cloud Deployment

## Recommended architecture

~~~text
                   HTTPS
                     │
                     ▼
            ┌─────────────────┐
            │ Render / FastAPI│
            └────────┬────────┘
                     │
             ┌───────┴────────┐
             ▼                ▼
      PostgreSQL          Threat Intel
      Supabase            NVD / CISA KEV
~~~

The default deployment is **same-origin**: FastAPI serves both the API and the complete frontend.

A separate Cloudflare Pages frontend is optional.

## Render

The repository contains render.yaml.

Build command:

~~~text
python -m pip install -r requirements.txt
~~~

Start command:

~~~text
python -m uvicorn backend.main:app --host 0.0.0.0 --port $PORT
~~~

Health check:

~~~text
/api/health
~~~

### Required production environment variables

~~~text
DATABASE_URL
SECRET_KEY
JWT_SECRET
FRONTEND_ORIGIN
ADMIN_USERNAME
ADMIN_PASSWORD
ENVIRONMENT=production
INCIDENT_THRESHOLD=50
~~~

## Database

CyberFusion supports:

- SQLite for local development
- PostgreSQL for deployment
- Supabase PostgreSQL as a managed option

Example local configuration:

~~~text
DATABASE_URL=sqlite:///./cyberfusion.db
~~~

Example PostgreSQL:

~~~text
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:5432/DATABASE
~~~

Never commit production database credentials.

## Optional Cloudflare Pages frontend

For a split deployment:

1. deploy the frontend directory
2. edit frontend/config.js
3. set window.CYBERFUSION_API to the HTTPS API origin
4. configure FRONTEND_ORIGIN on the backend
5. verify CORS

For the simplest deployment, do not split the frontend. Use FastAPI's same-origin frontend.

---

# 🧪 Synthetic Security Lab

CyberFusion contains a synthetic-event workflow so the platform can be evaluated without connecting to a real enterprise environment.

Generate controlled events:

~~~powershell
python simulator/run_demo.py --scenario mixed --events 1000 --seed 42
~~~

Supported scenarios include:

~~~text
normal
account_compromise
mixed
~~~

Load generated events into a running API:

~~~powershell
python simulator/load_demo.py datasets/synthetic/demo_events.jsonl
~~~

Recommended investigation sequence:

~~~text
LOGIN_FAILURE
LOGIN_FAILURE
LOGIN_FAILURE
NEW_DEVICE
NEW_IP
LOGIN_SUCCESS
PRIVILEGE_CHANGE
RESOURCE_ACCESS
       │
       ▼
Correlation
       │
       ▼
Risk
       │
       ▼
Incident
       │
       ▼
Forensic Graph
~~~

---

# 🤖 AI / Anomaly Detection

CyberFusion uses behavioral features such as:

~~~text
failed_logins_5m
successful_logins_1h
new_device
new_ip
login_hour_deviation
resource_rarity
privilege_change
number_of_destinations
network_volume
process_rarity
session_duration
authentication_frequency
~~~

The primary model is **Isolation Forest**.

When a trained model is unavailable, the implementation uses a clearly identified heuristic bootstrap path rather than pretending a trained ML model exists.

> Anomaly ≠ confirmed attack. CyberFusion presents anomaly evidence for investigation.

---

# 🔗 Correlation Engine

The correlation engine can associate events through:

- user
- device
- source IP
- asset
- session
- temporal proximity
- related security signals

The objective is to transform:

~~~text
Alert + Alert + Alert + Context
~~~

into:

~~~text
One correlated incident
with evidence and risk context
~~~

---

# 📊 Risk Engine

The initial research weighting is:

| Signal | Weight |
|---|---:|
| Rule score | 35% |
| Behavioral anomaly | 25% |
| Correlation context | 25% |
| Threat / vulnerability context | 15% |

~~~text
Risk = 0.35R + 0.25A + 0.25C + 0.15T
~~~

The score is normalized to 0–100.

These weights are research parameters, not a universal cybersecurity standard.

---

# 🕵️ Digital Forensics

The incident investigation workflow exposes:

- incident summary
- severity
- risk score
- status
- evidence
- timeline
- related events
- affected identities
- devices
- IP addresses
- assets
- vulnerability context
- relationship graph
- recommended analyst action

Example relationship model:

~~~text
USER
 │
 ├── USED_DEVICE ──> DEVICE
 │
 ├── OBSERVED_FROM ──> IP
 │
 └── GENERATED ──> EVENT
                     │
                     ├── ACCESSED ──> RESOURCE
                     ├── AFFECTED ──> ASSET
                     └── CONTRIBUTED_TO ──> INCIDENT
~~~

---

# 🛡️ Threat Intelligence

### NVD

National Vulnerability Database CVE enrichment.

### CISA KEV

Known Exploited Vulnerabilities catalog.

Threat intelligence is contextual enrichment, not a complete detection source.

External API failure should not prevent the core local event/risk pipeline from operating.

---

# ⚛️ QuantForensics / PQC

The optional PQC subsystem provides experimental post-quantum cryptography benchmarking when the required runtime/library support is available.

It does **not** claim that the entire platform is quantum-secure.

If the optional PQC runtime is unavailable, the application reports the capability as unavailable rather than fabricating benchmark results.

---

# 🔌 API Surface

### Authentication

~~~text
POST /api/auth/login
GET  /api/auth/me
~~~

### Events

~~~text
POST /api/events
POST /api/events/bulk
GET  /api/events
GET  /api/events/{event_id}
~~~

### Incidents

~~~text
GET   /api/incidents
GET   /api/incidents/{incident_id}
GET   /api/incidents/{incident_id}/events
GET   /api/incidents/{incident_id}/graph
PATCH /api/incidents/{incident_id}
~~~

### Dashboard

~~~text
GET /api/dashboard/summary
GET /api/dashboard/recent
~~~

### Vulnerabilities

~~~text
GET  /api/vulnerabilities
POST /api/vulnerabilities/sync/kev
POST /api/vulnerabilities/{cve_id}/sync
~~~

### Forensics

~~~text
GET /api/forensics/graph
~~~

### Research

~~~text
GET /api/metrics/snapshot
GET /api/pqc/benchmark
~~~

### Demo

~~~text
POST /api/demo/generate
~~~

### Health

~~~text
GET /api/health
~~~

Interactive OpenAPI documentation is available at /docs.

---

# 🧰 Troubleshooting

## ❌ pip.exe blocked by Windows Device Guard

Do not launch pip.exe directly.

Use:

~~~powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
~~~

The Windows launcher already uses this method.

If the machine blocks Python package execution itself, use Docker or an approved development environment.

## ❌ ModuleNotFoundError

Run from the repository root:

~~~powershell
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m pytest -q
~~~

## ❌ Port 8000 already in use

Windows:

~~~powershell
netstat -ano | findstr :8000
~~~

Then stop the conflicting process or use another port:

~~~powershell
python -m uvicorn backend.main:app --port 8001
~~~

## ❌ Blank page / 404

For the integrated deployment use:

~~~text
http://127.0.0.1:8000/
~~~

Do not open frontend/index.html directly from the filesystem.

## ❌ Login fails

Verify the local development credentials:

~~~text
Username: admin
Password: ChangeMe123!
~~~

If the administrator was created earlier with another password, changing ADMIN_PASSWORD does not automatically overwrite an existing database user.

For a fresh local SQLite installation, remove the local database and restart.

For Docker, intentionally reset the local volume only when appropriate:

~~~bash
docker compose down -v
docker compose up --build
~~~

## ❌ Database connection failure

Check DATABASE_URL and verify:

- host
- port
- database name
- username
- password
- SSL requirements
- provider network access

## ❌ CORS error

For a split deployment set:

~~~text
FRONTEND_ORIGIN=https://your-frontend.example
~~~

Do not use a wildcard origin with credentialed authentication.

## ❌ NVD / CISA synchronization fails

Check external connectivity, API rate limits and configuration.

The core CyberFusion detection pipeline can continue without external enrichment.

## ❌ PQC benchmark unavailable

The optional PQC runtime dependency is unavailable. This does not mean the core platform is broken.

## ❌ Docker says datasets does not exist

The repository contains a tracked datasets/.gitkeep file because the Docker image copies the datasets directory. Restore it if it was manually removed.

## ❌ Render service exits

Check the Render build/start log.

Reproduce locally:

~~~bash
python -m pip install -r requirements.txt
python -m compileall backend simulator
python -m pytest -q
~~~

Verify the production variables:

~~~text
DATABASE_URL
SECRET_KEY
JWT_SECRET
FRONTEND_ORIGIN
ADMIN_PASSWORD
~~~

The Render start command must use:

~~~text
python -m uvicorn backend.main:app --host 0.0.0.0 --port $PORT
~~~

---

# 🧪 Testing

Run:

~~~bash
python -m compileall backend simulator
python -m pytest -q
~~~

GitHub Actions runs the core verification on pushes and pull requests.

CodeQL is configured for the Python codebase.

A deployment should not be considered verified merely because the process starts. Check:

~~~text
Health
  ↓
Login
  ↓
Dashboard
  ↓
Event ingestion
  ↓
Correlation
  ↓
Incident creation
  ↓
Forensic investigation
~~~

---

# 📁 Project Structure

~~~text
CyberFusion/
│
├── .github/workflows/
│   ├── ci.yml
│   └── codeql.yml
│
├── backend/
│   ├── ai/
│   ├── api/
│   ├── core/
│   ├── database/
│   ├── forensic/
│   ├── pqc/
│   ├── services/
│   ├── config.py
│   ├── main.py
│   └── simulation.py
│
├── frontend/
│   ├── css/
│   ├── js/
│   ├── config.js
│   ├── index.html
│   ├── dashboard.html
│   ├── events.html
│   ├── incidents.html
│   ├── incident.html
│   ├── forensics.html
│   ├── vulnerabilities.html
│   ├── identity-risk.html
│   └── quantum.html
│
├── datasets/
├── simulator/
├── tests/
├── docs/
│
├── Dockerfile
├── docker-compose.yml
├── render.yaml
├── requirements.txt
├── pytest.ini
├── .env.example
├── SECURITY.md
├── CONTRIBUTORS.md
└── README.md
~~~

---

# 👥 Contributors

## 👩‍💻 Kriti Purohit

**Contribution ID:** KRITI_PUROHIT

**Role:**
- Project Lead
- Backend Engineering
- AI / ML
- Correlation Engine
- Risk Engine
- PQC subsystem
- System Architecture

GitHub: https://github.com/kritipurohit

---

## 👨‍💻 Vidit Shringi

**Contribution ID:** VIDIT_SHRINGI

**Role:**
- Frontend Engineering
- Database
- Digital Forensics
- Visualization
- Documentation
- Testing

GitHub: https://github.com/vidit-shringi

Kriti Purohit is explicitly documented as a project contributor in CONTRIBUTORS.md.

---

# 📜 Security & Responsible Use

CyberFusion is intended for:

- authorized environments
- synthetic security data
- defensive research
- cybersecurity education
- controlled laboratory testing
- forensic investigation research

Do not use it to access, monitor or interfere with systems without authorization.

CyberFusion does not autonomously execute destructive containment or offensive operations.

See SECURITY.md.

---

# 🎓 Research Evaluation

For academic evaluation, compare:

### Baseline

~~~text
Rule-only detection
~~~

### Proposed

~~~text
Rules
+
Behavioral anomaly
+
Correlation
+
Threat intelligence
~~~

Measure:

- Precision
- Recall
- F1-score
- False-positive rate
- Detection latency
- Events-to-incidents reduction
- Analyst investigation effort

Do not publish invented metrics. Record the dataset, random seed, thresholds, model configuration and experiment environment for every reported result.

---

# 🎓 Recommended Viva Demonstration

~~~text
01  Open CyberFusion
02  Login as administrator
03  Open Dashboard
04  Generate controlled security events
05  Inspect Live Events
06  Show rule detections
07  Show anomaly context
08  Show event correlation
09  Show risk score
10  Open generated incident
11  Inspect evidence and timeline
12  Open forensic relationship graph
13  Inspect vulnerability context
14  Update incident status
15  Review research metrics
16  Run optional PQC benchmark
~~~

---

# 📌 Project Identity

**Project:** CyberFusion

**Full title:**

> CyberFusion: An AI-Assisted Multi-Source Cybersecurity Correlation, Risk Prioritization and Digital Forensics Platform

**Primary objective:**

> Transform isolated security telemetry into explainable, prioritized and investigable cybersecurity incidents through rule-based detection, behavioral anomaly analysis, contextual threat intelligence and event correlation.

**Primary output:**

> A correlated incident containing a risk score, evidence trail, timeline, entity relationships, vulnerability context and recommended analyst action.

---

## ⭐ Repository

**CyberFusion:**  
https://github.com/vidit-shringi/CyberFusion

**Contributors:**

- Vidit Shringi — VIDIT-SHRINGI
- Kriti Purohit — KRITI-PUROHIT

---

<p align="center">
  <strong>CYBERFUSION</strong><br>
  <sub>Security intelligence, correlated.</sub>
</p>
