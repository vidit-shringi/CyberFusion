from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.db import get_db
from backend.database.schemas import EventIn
from backend.services.security import get_current_user
from backend.core.pipeline import process_event
from backend.simulation import build_demo_events

router = APIRouter(prefix="/api/demo", tags=["demo"])

@router.post("/generate")
def generate(
    scenario: str = "account_compromise",
    count: int = 30,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if count < 1 or count > 500:
        raise HTTPException(status_code=400, detail="count must be 1-500")
    events = build_demo_events(scenario=scenario, count=count)
    results = []
    for payload in events:
        event, incident = process_event(db, EventIn(**payload))
        results.append({
            "event_id": event.event_id,
            "incident_id": incident.incident_id if incident else None,
        })
    return {"scenario": scenario, "count": len(results), "results": results}
