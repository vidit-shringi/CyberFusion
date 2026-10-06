# CyberFusion

**CyberFusion: An AI-Assisted Multi-Source Cybersecurity Correlation, Risk Prioritization and Digital Forensics Platform**

CyberFusion is a student-scale cybersecurity research and engineering prototype for turning isolated security telemetry into explainable, prioritized and investigable incidents. The implementation combines deterministic rules, behavioral anomaly scoring, event correlation, vulnerability intelligence, risk prioritization and a forensic relationship graph. The project also contains a separate experimental post-quantum benchmarking subsystem named **QuantForensics**.

> **Academic positioning:** CyberFusion is not a production enterprise SIEM replacement, is not presented as fully quantum-secure, and does not claim that AI can always determine whether an event is malicious. It is designed for authorized laboratory data, synthetic demonstrations and reproducible academic evaluation.

## 1. What is actually implemented

The repository contains a complete modular-monolith full-stack prototype rather than a static dashboard.

### Core pipeline

```text
Identity / Network / Endpoint / Vulnerability Events
                    |
              Event ingestion
                    |
              Normalized event model
                    |
        +-----------+-----------+
        |           |           |
      Rules        AI       Threat Intel
        |        anomaly        |
        |        score          |
        +-----------+-----------+
                    |
             Correlation Engine
                    |
                Risk Engine
                    |
             Incident Generator
                    |
           +--------+---------+
           |                  |
      Forensic Graph      Web Console
```

Implemented capabilities include:

- normalized security-event ingestion
- rule-based suspicious-pattern detection
- behavioral feature extraction
- Isolation Forest support with a safe heuristic bootstrap when no model is fitted yet
- event correlation by time, user, device, source IP, asset and session
- configurable 0–100 risk scoring
- incident generation and status management
- evidence and recommended analyst actions
- forensic relationship graph data for NetworkX-style relationship analysis and Cytoscape.js visualization
- NVD CVE enrichment
- CISA KEV synchronization
- asset inventory
- synthetic event generation
- evaluation metrics
- optional liboqs PQC benchmarking
- JWT authentication and password hashing
- audit logging
- Docker + PostgreSQL configuration
- CI + CodeQL workflows
- responsive dark SOC-style frontend

## 2. Technology stack

### Frontend
- HTML5
- CSS3
- Vanilla JavaScript
- Chart.js
- Cytoscape.js

### Backend
- Python 3.12-compatible code
- FastAPI
- Uvicorn
- Pydantic / pydantic-settings
- SQLAlchemy

### Data / AI
- PostgreSQL for deployment
- SQLite works for local development
- NumPy
- Pandas
- scikit-learn
- Isolation Forest

### Forensics
- Network relationship storage in SQL
- Cytoscape.js for browser visualization

### Threat intelligence
- NVD API 2.x
- CISA Known Exploited Vulnerabilities (KEV)

### PQC
- optional liboqs / liboqs-python benchmark integration

## 3. Repository structure

```text
CyberFusion/
├── .github/workflows/
│   ├── ci.yml
│   └── codeql.yml
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
├── frontend/
│   ├── css/
│   ├── js/
│   ├── index.html
│   ├── dashboard.html
│   ├── events.html
│   ├── incidents.html
│   ├── incident.html
│   ├── vulnerabilities.html
│   ├── identity-risk.html
│   ├── forensics.html
│   └── quantum.html
├── simulator/
├── datasets/
├── docs/
├── scripts/
├── tests/
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── render.yaml
├── requirements.txt
├── pytest.ini
├── CONTRIBUTORS.md
├── SECURITY.md
└── README.md
```

## 4. Local development — Windows

### Prerequisites

Install:

- Python 3.12 recommended
- Git
- Docker Desktop only when using the Docker path

Check:

```powershell
python --version
git --version
```

### Option A — easiest Windows launcher

From the repository root:

```powershell
scripts\start_windows.bat
```

The launcher:

1. creates `.venv` when needed
2. creates `.env` from `.env.example` when needed
3. installs dependencies with **Python module invocation**
4. starts Uvicorn
5. opens the CyberFusion web application

Using `python -m pip` instead of directly calling `pip.exe` is intentional because some Windows security policies block direct executable invocation.

### Option B — manual Windows setup

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
copy .env.example .env
python -m uvicorn backend.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/api/health
```

The FastAPI application serves the frontend and API from the same origin, so a separate frontend server is not required for the default local setup.

### Default local login

The development defaults are:

```text
Username: admin
Password: ChangeMe123!
```

These are only convenience defaults for a local academic environment. Change `ADMIN_PASSWORD`, `SECRET_KEY` and `JWT_SECRET` before any public deployment.

## 5. Local development — Linux / macOS

```bash
bash scripts/start_linux.sh
```

Or manually:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
python -m uvicorn backend.main:app --reload
```

## 6. Docker development

The repository includes a FastAPI application container and PostgreSQL.

```bash
docker compose up --build
```

Then open:

```text
http://127.0.0.1:8000/
```

Stop:

```bash
docker compose down
```

Remove the development database volume too:

```bash
docker compose down -v
```

> Do not use `docker compose down -v` unless you intentionally want to remove the local PostgreSQL data volume.

## 7. Environment configuration

Copy:

```text
.env.example -> .env
```

Important settings:

```text
DATABASE_URL=
SECRET_KEY=
JWT_SECRET=
ACCESS_TOKEN_EXPIRE_MINUTES=
FRONTEND_ORIGIN=
NVD_API_KEY=
CISA_KEV_URL=
ADMIN_USERNAME=
ADMIN_PASSWORD=
INCIDENT_THRESHOLD=
```

Optional external API keys are not required for the core product.

Never commit `.env`.

## 8. Synthetic demonstration — fully working path

The project includes a real synthetic event generator so the application does not depend on a third-party production SIEM.

### Generate controlled data

From the repository root:

```powershell
python simulator/run_demo.py --scenario mixed --events 1000 --seed 42
```

Supported scenarios include:

- `normal`
- `account_compromise`
- `mixed`

The output is written under `datasets/synthetic/` when the selected output path is used.

### Load the generated events into a running application

Start CyberFusion first, then:

```powershell
python simulator/load_demo.py datasets/synthetic/demo_events.jsonl
```

The loader authenticates against the API and submits events in batches.

### In-app demo

You can also use:

```text
Live Events -> Generate demo events
```

That endpoint generates an account-compromise-style scenario and pushes it through the actual ingestion, detection, correlation, risk and incident pipeline.

### Recommended viva scenario

Use the controlled identity:

```text
USR-001
```

and demonstrate a sequence similar to:

```text
LOGIN_FAILURE
LOGIN_FAILURE
LOGIN_FAILURE
NEW_DEVICE
NEW_IP
LOGIN_SUCCESS
PRIVILEGE_CHANGE
RESOURCE_ACCESS
```

The purpose is to show how separate security signals can be correlated into one investigable incident rather than presented as unrelated static alerts.

## 9. How the detection pipeline works

For each event, the backend can:

1. validate the payload
2. persist the normalized event
3. extract behavioral features
4. run deterministic rules
5. calculate an anomaly score
6. calculate correlation context
7. enrich vulnerability context where available
8. calculate a weighted 0–100 risk score
9. create or update an incident above the configured threshold
10. build/update forensic relationships
11. persist an audit record

### Initial risk weighting

The initial implementation uses:

```text
Rule score            35%
Behavior anomaly      25%
Correlation context   25%
Threat/vulnerability  15%
```

These weights are a research starting point, not a universal cybersecurity standard. They should be changed only through configuration or controlled experiments and documented in the research report.

## 10. Rule engine

The repository contains transparent rules such as:

- repeated failed logins
- new device + privileged access
- new IP after failed logins
- known exploited vulnerability + internet-exposed asset

Every rule match records evidence and contributes a score. The system should explain the rule that fired rather than producing an opaque alert.

## 11. Behavioral anomaly engine

The primary model is Isolation Forest.

The system extracts features including:

```text
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
```

When a fitted Isolation Forest is available, the model is used for anomaly scoring.

When the model has not yet been fitted on enough data, the implementation uses a clearly labeled heuristic bootstrap path instead of pretending that a trained model exists.

The UI and evidence should describe a behavior as **anomalous**, not as definitely malicious.

## 12. Vulnerability intelligence

### NVD

The application can retrieve CVE information from the NVD API 2.x.

### CISA KEV

The application can synchronize the Known Exploited Vulnerabilities catalog.

These sources are enrichment inputs. They are not treated as complete threat detection.

The vulnerability risk context can combine:

- CVSS
- exploit/KEV status
- internet exposure
- asset criticality
- observed suspicious activity

## 13. Forensic investigation

The incident investigation page can show:

- incident summary
- risk score
- severity
- status
- evidence
- recommended action
- timeline
- related events
- affected users/devices/IPs/assets
- forensic graph

Graph relationships represent investigation context such as:

```text
USER -> USED_DEVICE
USER -> OBSERVED_FROM -> IP
EVENT -> ACCESSED_RESOURCE
EVENT -> AFFECTED_ASSET
EVENT -> REFERENCES_VULNERABILITY
EVENT -> CONTRIBUTED_TO_INCIDENT
```

The browser graph is rendered with Cytoscape.js.

## 14. API

### Authentication

```http
POST /api/auth/login
GET  /api/auth/me
```

### Events

```http
POST /api/events
POST /api/events/bulk
GET  /api/events
GET  /api/events/{event_id}
```

### Incidents

```http
GET   /api/incidents
GET   /api/incidents/{incident_id}
GET   /api/incidents/{incident_id}/events
GET   /api/incidents/{incident_id}/graph
PATCH /api/incidents/{incident_id}
```

### Dashboard

```http
GET /api/dashboard/summary
GET /api/dashboard/recent
```

### Vulnerabilities

```http
GET  /api/vulnerabilities
POST /api/vulnerabilities
POST /api/vulnerabilities/sync/kev
POST /api/vulnerabilities/{cve_id}/sync
```

### Assets

```http
GET  /api/assets
POST /api/assets
```

### Forensics

```http
GET /api/forensics/graph
```

### Research metrics

```http
GET /api/metrics/snapshot
```

### PQC

```http
GET /api/pqc/benchmark
```

### Demo generator

```http
POST /api/demo/generate
```

### Health

```http
GET /api/health
```

Swagger/OpenAPI is available at:

```text
/docs
```

## 15. Testing

Run:

```bash
python -m pytest -q
```

The repository also runs automatically through GitHub Actions on pushes and pull requests.

Current CI coverage includes:

- dependency installation
- Python compilation
- automated tests

CodeQL is also configured for the Python codebase.

## 16. Research evaluation

The intended academic comparison is:

### Baseline

```text
Rule-only detection
```

### Proposed pipeline

```text
Rule engine
+
Behavior anomaly detection
+
Event correlation
+
Threat intelligence
```

Recommended metrics:

- precision
- recall
- F1-score
- false-positive rate
- detection latency
- incident count
- event-to-incident reduction
- analyst investigation effort/time

Do not enter invented values. Use real labeled experiment output.

## 17. QuantForensics / PQC module

The PQC module is intentionally separate from core authentication.

It attempts to use `liboqs-python` when the runtime supports it. When unavailable, the endpoint reports an explicit unavailable/error status rather than fabricating benchmark results.

The module is research-only and does not claim that CyberFusion is fully quantum-secure.

## 18. Deployment

Recommended academic deployment model:

```text
Cloudflare Pages
      |
      | HTTPS
      v
Render / FastAPI
      |
      v
Supabase PostgreSQL
      |
      +---- NVD
      |
      +---- CISA KEV
```

### Backend — Render

Use the included `render.yaml` or create a Python web service with:

```text
Build:
pip install -r requirements.txt

Start:
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

Set:

```text
DATABASE_URL
SECRET_KEY
JWT_SECRET
FRONTEND_ORIGIN
ADMIN_USERNAME
ADMIN_PASSWORD
```

### Database — Supabase

Create a PostgreSQL database and supply its PostgreSQL connection string through `DATABASE_URL`.

The application creates its tables during startup through SQLAlchemy for this student-scale implementation. For a more formal production/research deployment, add Alembic migrations before schema evolution.

### Frontend — Cloudflare Pages

For the default same-origin Render deployment, the frontend is already served by FastAPI.

For a split Cloudflare Pages + Render architecture:

1. deploy the contents of `frontend/` to Cloudflare Pages
2. set `window.CYBERFUSION_API` in `frontend/config.js` to the public API URL
3. set `FRONTEND_ORIGIN` on Render to the Pages origin
4. verify HTTPS and browser CORS behavior

Do not put database credentials or privileged API keys into frontend JavaScript.

## 19. Troubleshooting and error resolution

### Error: 'pip' is not recognized

Use:

```powershell
python -m pip install -r requirements.txt
```

or run:

```powershell
scripts\start_windows.bat
```

The included launcher deliberately invokes pip through Python.

### Error: 'pip.exe' blocked by Windows Device Guard / security policy

Do not execute `pip.exe` directly.

Use:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

This is the intended workaround for the project.

### Error: Port 8000 already in use

Find the process:

```powershell
netstat -ano | findstr :8000
```

Then either stop the conflicting process or run on another port:

```powershell
python -m uvicorn backend.main:app --reload --port 8001
```

When using another port, update your browser URL accordingly.

### Error: ModuleNotFoundError

Make sure the virtual environment is active and dependencies were installed:

```powershell
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m pytest -q
```

Run commands from the **repository root**, not from inside `backend/`.

### Error: database connection failed

For local SQLite development, use the default:

```text
DATABASE_URL=sqlite:///./cyberfusion.db
```

For Supabase/PostgreSQL, verify:

- hostname
- port
- username
- password
- database name
- SSL requirements
- network accessibility

Also confirm that the Render `DATABASE_URL` is actually configured.

### Error: invalid or expired token

Log out, clear the browser storage and log in again.

The frontend token is stored in local browser storage for this student prototype. In a production-grade application, use a more hardened session architecture.

### Error: CORS policy blocked

For split frontend/backend deployment, set:

```text
FRONTEND_ORIGIN=https://your-pages-domain.example
```

Do not use a wildcard origin for credentialed authentication.

Then restart/redeploy the API.

### Error: NVD synchronization fails

The core application can run without the NVD API.

Check:

- outbound internet connectivity
- NVD rate limits
- `NVD_API_KEY` when available
- the CVE identifier format

Treat an external NVD outage as an enrichment failure, not as a reason for the entire application to stop.

### Error: CISA KEV sync fails

Check:

- outbound HTTPS access
- `CISA_KEV_URL`
- response availability

The application should still run without KEV synchronization.

### Error: PQC benchmark reports unavailable

This is expected when `liboqs-python` and the required native library are not installed.

Do not replace the result with fake numbers.

The rest of CyberFusion remains usable without the PQC module.

### Error: Docker cannot connect to PostgreSQL

Run:

```bash
docker compose ps
docker compose logs db
docker compose logs cyberfusion
```

Then restart:

```bash
docker compose down
docker compose up --build
```

For a clean local database reset:

```bash
docker compose down -v
docker compose up --build
```

### Error: Render service starts but immediately exits

Check the Render logs first.

Common causes:

- missing environment variables
- invalid `DATABASE_URL`
- package installation error
- application import error

Use the configured start command:

```text
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

### Error: GitHub Actions fails

Open the failed workflow run and inspect the failed step.

For the standard CI pipeline, reproduce locally:

```bash
python -m pip install -r requirements.txt
python -m compileall backend simulator
python -m pytest -q
```

If local tests pass but CI fails, inspect environment/version differences in the Actions log before changing application logic.

### Error: blank frontend / 404 page

For the default integrated deployment, open the FastAPI root:

```text
http://127.0.0.1:8000/
```

Do not open `frontend/index.html` through an unrelated local path and expect API-relative routing to behave the same way.

For Cloudflare Pages split deployment, verify `frontend/config.js` points to the public backend URL.

### Error: events are accepted but no incidents appear

Check:

1. `/api/events` response
2. event type is supported
3. enough related activity exists for the selected scenario
4. rule matches are being generated
5. the combined score crosses `INCIDENT_THRESHOLD`
6. the event chain shares relevant user/device/IP/asset/session context

Use the built-in account-compromise simulator rather than manually inventing unrelated single events.

### Error: dashboard numbers are zero

An empty dashboard is valid before events are ingested.

Generate controlled events:

```powershell
python simulator/run_demo.py --scenario mixed --events 100
python simulator/load_demo.py datasets/synthetic/demo_events.jsonl
```

Then refresh the dashboard.

## 20. Security notes

Do not commit:

- database passwords
- NVD API keys
- JWT secrets
- application secrets
- production credentials

For any public deployment:

- use HTTPS
- use strong secrets
- restrict CORS
- change default admin credentials
- keep dependencies updated
- use managed PostgreSQL instead of local SQLite
- monitor application logs
- keep testing limited to systems you are authorized to assess

Response actions in CyberFusion are recommendations/simulations. The academic prototype does not autonomously attack, block arbitrary third-party systems or execute destructive actions.

## 21. Known limitations

- student-scale processing assumptions
- simplified entity resolution
- no enterprise SIEM connector
- no guaranteed enterprise throughput
- synthetic data is not a substitute for production telemetry
- external threat-intelligence services can fail or rate-limit
- the anomaly model is not always fitted and can use a bootstrap heuristic
- PQC support depends on optional native/runtime dependencies
- formal Alembic migrations should be added before long-term schema evolution
- public hosting depends on the selected provider's availability and plan limits

## 22. Future work

Keep these as future work unless required:

- full SIEM integration
- SOAR integration
- Kafka/distributed event processing
- Neo4j
- enterprise identity providers
- endpoint agents
- advanced UEBA
- graph neural networks
- LLM-assisted forensic explanation
- stronger PQC integration
- automated containment
- real-time SIEM connectors

## 23. Two-member project division

### Member 1
Focus:

- Python backend
- APIs
- AI/ML
- anomaly detection
- correlation
- risk engine
- PQC module
- backend security
- testing

### Member 2
Focus:

- frontend
- dashboard
- database design
- forensic visualization
- vulnerability views
- integration
- documentation
- UI testing

Both members should understand the complete architecture for viva.

## 24. Viva demonstration flow

The intended demonstration is:

```text
1. Open CyberFusion
2. Log in
3. Open Live Events
4. Generate the controlled synthetic scenario
5. Watch event telemetry enter the system
6. Show rule matches
7. Show behavioral/anomaly context
8. Show correlation
9. Show risk score
10. Open the generated incident
11. Inspect evidence and timeline
12. Open the forensic graph
13. Inspect affected identity/device/IP
14. Inspect vulnerability context
15. Update the incident status
16. Show research metrics
17. Run the optional PQC benchmark
```

## 25. Research integrity

CyberFusion must not fabricate:

- detection metrics
- AI output
- threat-intelligence results
- benchmark results
- production-scale performance claims

Use actual experiment data and document:

- dataset
- seed
- scenario
- sample size
- model configuration
- thresholds
- scoring weights
- run date
- environment

## 26. Scope

The project follows the priority order from the build specification:

```text
1. Functional core
2. Correct event correlation
3. Explainable risk scoring
4. Useful forensic investigation
5. Good UI
6. Research evaluation
7. PQC extension
8. Advanced integrations
```

The target is a technically strong system that two students can understand, demonstrate, defend and maintain.

## 27. Project identity

**Project:** CyberFusion

**Full name:** CyberFusion: An AI-Assisted Multi-Source Cybersecurity Correlation, Risk Prioritization and Digital Forensics Platform

**Forensic/PQC subsystem:** QuantForensics

**Primary objective:**

> Transform isolated security telemetry into explainable, prioritized and investigable cybersecurity incidents through rule-based detection, behavioral anomaly analysis, contextual threat intelligence and event correlation.

**Primary users:**

- SOC analyst
- security investigator
- system administrator
- cybersecurity student/researcher

**Primary output:**

> A correlated, explainable incident with a risk score, evidence trail, timeline, entity relationships, vulnerability context and recommended analyst action.

## 28. Current repository verification

The repository's GitHub Actions were executed for the current completed build.

- **CyberFusion CI:** successful
- **Python compilation:** successful
- **Automated tests:** successful
- **CodeQL:** successful

The CI workflow is therefore the first verification layer; local testing should still be performed before every academic demo and before any public deployment.
