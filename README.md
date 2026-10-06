# CyberFusion

**CyberFusion: An AI-Assisted Multi-Source Cybersecurity Correlation, Risk Prioritization and Digital Forensics Platform**

## Contributors

- **Kriti Purohit** — Project Lead / Backend, AI/ML, Correlation, PQC
  - https://github.com/kritipurohit
- **Vidit Shringi** — Frontend, Database, Forensics, Visualization
  - https://github.com/vidit-shringi

CyberFusion normalizes security telemetry, combines explainable rules with behavioral anomaly detection and threat intelligence, correlates related events, calculates risk scores, and provides forensic investigation views.

## Local setup

```powershell
py -3.12 -m venv .venv
.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt
.\\.venv\\Scripts\\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000/

## Demo events

```powershell
.\\.venv\\Scripts\\python.exe simulator/run_demo.py
```

## Deployment

Docker, Render, CI and CodeQL configuration are included. Use environment variables for secrets and HTTPS for public deployment.

## Security

Only test against systems you own or are explicitly authorized to test.

## Research integrity

Do not fabricate evaluation metrics. Generate them from controlled experiments.
