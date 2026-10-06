from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.db import get_db
from backend.services.forensics import get_graph
from backend.services.security import get_current_user

router = APIRouter(prefix="/api/forensics", tags=["forensics"])

@router.get("/graph")
def graph(incident_id: str | None = None, db: Session = Depends(get_db), user=Depends(get_current_user)):
    nodes, edges = get_graph(db, incident_id)
    return {"nodes":[{"data":{"id":n.node_id,"label":n.label,"type":n.node_type, **(n.properties or {})}} for n in nodes], "edges":[{"data":{"id":str(e.id),"source":e.source_node_id,"target":e.target_node_id,"relationship":e.relationship}} for e in edges]}
