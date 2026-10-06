from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from backend.database.db import get_db
from backend.database.models import Incident, IncidentEvent, Event, User, AuditLog
from backend.database.schemas import IncidentOut, IncidentUpdate, EventOut
from backend.services.security import get_current_user
from backend.services.forensics import get_graph
router = APIRouter(prefix="/api/incidents", tags=["incidents"])
@router.get("", response_model=list[IncidentOut])
def list_incidents(limit: int = 100, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return list(db.scalars(select(Incident).order_by(desc(Incident.created_at)).limit(max(1, min(limit, 500)))).all())
@router.get("/{incident_id}", response_model=IncidentOut)
def get_incident(incident_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    incident = db.scalar(select(Incident).where(Incident.incident_id == incident_id))
    if not incident: raise HTTPException(status_code=404, detail="Incident not found")
    return incident
@router.get("/{incident_id}/events", response_model=list[EventOut])
def incident_events(incident_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    event_ids = [x.event_id for x in db.scalars(select(IncidentEvent).where(IncidentEvent.incident_id == incident_id)).all()]
    if not event_ids: return []
    return list(db.scalars(select(Event).where(Event.event_id.in_(event_ids)).order_by(Event.timestamp)).all())
@router.get("/{incident_id}/graph")
def incident_graph(incident_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    nodes, edges = get_graph(db, incident_id)
    return {"nodes":[{"data":{"id":n.node_id,"label":n.label,"type":n.node_type, **(n.properties or {})}} for n in nodes],"edges":[{"data":{"id":str(e.id),"source":e.source_node_id,"target":e.target_node_id,"relationship":e.relationship}} for e in edges]}
@router.patch("/{incident_id}", response_model=IncidentOut)
def update_incident(incident_id: str, payload: IncidentUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    allowed={"NEW","INVESTIGATING","CONTAINED","RESOLVED","FALSE_POSITIVE"}
    if payload.status not in allowed: raise HTTPException(status_code=400, detail="Invalid incident status")
    incident=db.scalar(select(Incident).where(Incident.incident_id==incident_id))
    if not incident: raise HTTPException(status_code=404, detail="Incident not found")
    incident.status=payload.status
    db.add(AuditLog(actor=user.username,action="incident_status_change",resource=incident_id,details={"status":payload.status}))
    db.commit(); db.refresh(incident); return incident
