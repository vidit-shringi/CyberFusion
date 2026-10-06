from __future__ import annotations
from datetime import timedelta
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.database.models import Event, Incident, IncidentEvent
from backend.core.risk import risk_level
from backend.config import settings
def related_events(db: Session,event: Event,window_minutes: int=15)->list[Event]:
    start=event.timestamp-timedelta(minutes=window_minutes); end=event.timestamp+timedelta(minutes=window_minutes)
    candidates=list(db.scalars(select(Event).where(Event.timestamp>=start,Event.timestamp<=end)).all()); results=[]
    for e in candidates:
        if e.event_id==event.event_id: results.append(e); continue
        shared=sum(1 for a,b in ((event.user_id,e.user_id),(event.device_id,e.device_id),(event.source_ip,e.source_ip),(event.asset_id,e.asset_id),(event.session_id,e.session_id)) if a and b and a==b)
        if shared>=1: results.append(e)
    return results
def correlation_score(events:list[Event])->float:
    if not events: return 0.0
    types={e.event_type for e in events}; score=min(len(events)*6,30)+min(len(types)*5,25)
    if "LOGIN_FAILURE" in types and "LOGIN_SUCCESS" in types: score+=15
    if "NEW_DEVICE" in types: score+=10
    if "PRIVILEGE_CHANGE" in types: score+=10
    if "RESOURCE_ACCESS" in types: score+=5
    if "VULNERABILITY_EVENT" in types: score+=5
    return min(score,100.0)
def get_or_create_incident(db: Session,event: Event,related:list[Event],risk:float,evidence:list[dict],rec_action:str)->Incident|None:
    if risk<settings.incident_threshold: return None
    candidate=None
    for inc in db.scalars(select(Incident).where(Incident.status.in_(["NEW","INVESTIGATING"]))):
        if event.user_id and event.user_id in (inc.affected_users or []): candidate=inc; break
        if event.asset_id and event.asset_id in (inc.affected_assets or []): candidate=inc; break
    if candidate is None:
        incident_number=db.query(Incident).count()+1
        candidate=Incident(incident_id=f"INC-{incident_number:05d}",title="Correlated Security Incident",description="Multiple security signals were correlated into a single investigable incident.",risk_score=risk,severity=risk_level(risk),status="NEW",affected_users=list({e.user_id for e in related if e.user_id}),affected_devices=list({e.device_id for e in related if e.device_id}),affected_ips=list({e.source_ip for e in related if e.source_ip}),affected_assets=list({e.asset_id for e in related if e.asset_id}),related_vulnerabilities=list({e.cve_id for e in related if e.cve_id}),evidence=evidence,recommended_action=rec_action)
        db.add(candidate); db.flush()
    else:
        candidate.risk_score=max(candidate.risk_score,risk); candidate.severity=risk_level(candidate.risk_score)
        candidate.affected_users=list(set(candidate.affected_users or [])|{e.user_id for e in related if e.user_id})
        candidate.affected_devices=list(set(candidate.affected_devices or [])|{e.device_id for e in related if e.device_id})
        candidate.affected_ips=list(set(candidate.affected_ips or [])|{e.source_ip for e in related if e.source_ip})
        candidate.affected_assets=list(set(candidate.affected_assets or [])|{e.asset_id for e in related if e.asset_id})
        candidate.related_vulnerabilities=list(set(candidate.related_vulnerabilities or [])|{e.cve_id for e in related if e.cve_id})
        candidate.evidence=(candidate.evidence or [])+evidence; candidate.recommended_action=rec_action
    existing_event_ids={x.event_id for x in db.scalars(select(IncidentEvent).where(IncidentEvent.incident_id==candidate.incident_id)).all()}
    for e in related:
        if e.event_id not in existing_event_ids: db.add(IncidentEvent(incident_id=candidate.incident_id,event_id=e.event_id,relevance_score=1.0))
    return candidate
