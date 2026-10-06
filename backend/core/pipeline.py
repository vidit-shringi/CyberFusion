from __future__ import annotations
import uuid
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.database.models import Event, EventFeature, RuleMatch, RiskScore, AuditLog, Vulnerability
from backend.database.schemas import EventIn
from backend.core.features import extract_features
from backend.core.rules import apply_rules
from backend.core.correlation import related_events, correlation_score, get_or_create_incident
from backend.core.risk import calculate_risk, recommended_action
from backend.ai.anomaly import anomaly_engine
from backend.services.forensics import update_forensic_graph

def ensure_event(db: Session,payload: EventIn)->Event:
    event_id=payload.event_id or f"EVT-{uuid.uuid4().hex[:12].upper()}"
    existing=db.scalar(select(Event).where(Event.event_id==event_id))
    if existing:return existing
    event=Event(event_id=event_id,timestamp=payload.timestamp,event_type=payload.event_type,user_id=payload.user_id,device_id=payload.device_id,source_ip=payload.source_ip,destination_ip=payload.destination_ip,resource=payload.resource,action=payload.action,status=payload.status,severity=payload.severity,asset_id=payload.asset_id,session_id=payload.session_id,cve_id=payload.cve_id,metadata_json=payload.metadata)
    db.add(event); db.flush(); return event

def threat_score(db: Session,event: Event)->float:
    if not event.cve_id:return 0.0
    vuln=db.scalar(select(Vulnerability).where(Vulnerability.cve_id==event.cve_id))
    if not vuln:return 0.0
    score=(vuln.cvss or 0)*10
    if vuln.kev: score=min(100.0,score+20)
    if (event.metadata_json or {}).get("internet_exposed"): score=min(100.0,score+10)
    return min(score,100.0)

def process_event(db: Session,payload: EventIn)->tuple[Event,object|None]:
    event=ensure_event(db,payload); features=extract_features(db,event); db.merge(EventFeature(event_id=event.event_id,features=features))
    anomaly,_meta=anomaly_engine.score(features); rule_score,matches=apply_rules(db,event)
    for m in matches: db.add(RuleMatch(event_id=event.event_id,rule_id=m["rule_id"],evidence=m["evidence"],score=m["score"]))
    related=related_events(db,event,int((event.metadata_json or {}).get("correlation_window_minutes",15))); corr=correlation_score(related); threat=threat_score(db,event)
    score,level,factors=calculate_risk(rule_score,anomaly,corr,threat)
    event.rule_score=rule_score; event.anomaly_score=anomaly; event.correlation_score=corr; event.threat_score=threat
    db.add(RiskScore(subject_type="event",subject_id=event.event_id,score=score,factors=factors))
    evidence=[{"kind":"rule","rule_id":m["rule_id"],"name":m["name"],"score":m["score"],"evidence":m["evidence"]} for m in matches]
    evidence.append({"kind":"model","anomaly_score":round(anomaly,2),"features":features})
    evidence.append({"kind":"correlation","related_event_ids":[e.event_id for e in related],"correlation_score":round(corr,2)})
    if event.cve_id:evidence.append({"kind":"threat_intelligence","cve_id":event.cve_id,"threat_score":round(threat,2)})
    incident=get_or_create_incident(db,event,related,score,evidence,recommended_action(score,factors))
    update_forensic_graph(db,event,related,incident)
    db.add(AuditLog(actor="system",action="event_processed",resource=event.event_id,details={"risk":score,"level":level}))
    db.commit(); db.refresh(event); return event,incident
