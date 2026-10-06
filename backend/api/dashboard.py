from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from backend.database.db import get_db
from backend.database.models import Event, Incident, Vulnerability, RiskScore, Asset
from backend.database.schemas import DashboardSummary
from backend.services.security import get_current_user

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

@router.get("/summary", response_model=DashboardSummary)
def summary(db: Session = Depends(get_db), user=Depends(get_current_user)):
    now = datetime.now(timezone.utc)
    hour_ago = now - timedelta(hours=1)
    total = db.scalar(select(func.count()).select_from(Event)) or 0
    last_hour = db.scalar(select(func.count()).select_from(Event).where(Event.timestamp >= hour_ago)) or 0
    critical = db.scalar(select(func.count()).select_from(Incident).where(Incident.severity == "CRITICAL", Incident.status.not_in(["RESOLVED","FALSE_POSITIVE"]))) or 0
    open_inc = db.scalar(select(func.count()).select_from(Incident).where(Incident.status.not_in(["RESOLVED","FALSE_POSITIVE"]))) or 0
    anomalies = db.scalar(select(func.count()).select_from(Event).where(Event.timestamp >= hour_ago, Event.anomaly_score >= 50)) or 0
    vulnerabilities = db.scalar(select(func.count()).select_from(Vulnerability)) or 0
    kev = db.scalar(select(func.count()).select_from(Vulnerability).where(Vulnerability.kev == True)) or 0
    user_scores = db.scalars(select(RiskScore).where(RiskScore.subject_type == "event").order_by(RiskScore.created_at.desc()).limit(1000)).all()
    high_users = set(); high_assets = set()
    for rs in user_scores:
        if rs.score >= 70: high_users.add(rs.subject_id)
    for a in db.scalars(select(Asset)).all():
        if a.criticality in {"HIGH","CRITICAL"}: high_assets.add(a.asset_id)
    return DashboardSummary(total_events=total, events_last_hour=last_hour, critical_incidents=critical, high_risk_users=len(high_users), high_risk_assets=len(high_assets), open_incidents=open_inc, anomalies_last_hour=anomalies, vulnerabilities=vulnerabilities, kev_vulnerabilities=kev)

@router.get("/recent")
def recent(db: Session = Depends(get_db), user=Depends(get_current_user)):
    rows = db.scalars(select(Event).order_by(Event.timestamp.desc()).limit(25)).all()
    return [{"event_id":e.event_id,"timestamp":e.timestamp,"type":e.event_type,"severity":e.severity,"risk":round((0.35*e.rule_score+0.25*e.anomaly_score+0.25*e.correlation_score+0.15*e.threat_score),2)} for e in rows]
