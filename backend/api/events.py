from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from backend.database.db import get_db
from backend.database.models import Event, User
from backend.database.schemas import EventIn, EventOut
from backend.services.security import get_current_user
from backend.core.pipeline import process_event

router = APIRouter(prefix="/api/events", tags=["events"])

@router.post("", response_model=EventOut)
def ingest_event(payload: EventIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if payload.event_type not in {"LOGIN_SUCCESS","LOGIN_FAILURE","LOGOUT","NEW_DEVICE","NEW_IP","PRIVILEGE_CHANGE","RESOURCE_ACCESS","NETWORK_EVENT","PROCESS_EVENT","VULNERABILITY_EVENT","SECURITY_ALERT"}:
        raise HTTPException(status_code=400, detail="Unsupported event_type")
    event, _ = process_event(db, payload)
    return event

@router.post("/bulk")
def ingest_bulk(payloads: list[EventIn], db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if len(payloads) > 5000: raise HTTPException(status_code=413, detail="Bulk limit is 5000 events")
    created = []
    for p in payloads:
        event, incident = process_event(db, p)
        created.append({"event_id": event.event_id, "incident_id": incident.incident_id if incident else None})
    return {"count": len(created), "results": created}

@router.get("", response_model=list[EventOut])
def list_events(limit: int = 100, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    limit = max(1, min(limit, 500))
    return list(db.scalars(select(Event).order_by(desc(Event.timestamp)).limit(limit)).all())

@router.get("/{event_id}", response_model=EventOut)
def get_event(event_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    event = db.scalar(select(Event).where(Event.event_id == event_id))
    if not event: raise HTTPException(status_code=404, detail="Event not found")
    return event
