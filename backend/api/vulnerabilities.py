from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.database.db import get_db
from backend.database.models import Vulnerability, User
from backend.database.schemas import VulnerabilityIn
from backend.services.security import get_current_user
from backend.services.threat_intel import fetch_nvd_cve, fetch_cisa_kev
router = APIRouter(prefix="/api/vulnerabilities", tags=["vulnerabilities"])
@router.get("")
def list_vulns(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return [{"cve_id":v.cve_id,"description":v.description,"cvss":v.cvss,"severity":v.severity,"kev":v.kev,"affected_products":v.affected_products,"source":v.source} for v in db.scalars(select(Vulnerability)).all()]
@router.post("")
def create_vuln(payload: VulnerabilityIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    existing=db.scalar(select(Vulnerability).where(Vulnerability.cve_id==payload.cve_id))
    if existing:
        for k,v in payload.model_dump().items(): setattr(existing,k,v)
        db.commit(); db.refresh(existing); return existing
    v=Vulnerability(**payload.model_dump()); db.add(v); db.commit(); db.refresh(v); return v
@router.post("/sync/kev")
async def sync_kev(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    entries=await fetch_cisa_kev(); count=0
    for item in entries:
        cve=item.get("cveID")
        if not cve: continue
        v=db.scalar(select(Vulnerability).where(Vulnerability.cve_id==cve))
        if not v:
            v=Vulnerability(cve_id=cve,description=item.get("shortDescription",""),kev=True,source="cisa_kev",published_at=item.get("dateAdded")); db.add(v); count+=1
        else: v.kev=True
    db.commit(); return {"downloaded":len(entries),"new_or_updated":count}
@router.post("/{cve_id}/sync")
async def sync_one(cve_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    data=await fetch_nvd_cve(cve_id)
    if not data: raise HTTPException(status_code=404, detail="CVE not found in NVD")
    desc=next((d.get("value","") for d in data.get("descriptions",[]) if d.get("lang")=="en"),"")
    metrics=data.get("metrics",{}); cvss=None; severity="UNKNOWN"
    for key in ("cvssMetricV40","cvssMetricV31","cvssMetricV30","cvssMetricV2"):
        if metrics.get(key):
            m=metrics[key][0].get("cvssData",{}); cvss=m.get("baseScore"); severity=m.get("baseSeverity",severity); break
    v=db.scalar(select(Vulnerability).where(Vulnerability.cve_id==cve_id))
    if not v: v=Vulnerability(cve_id=cve_id); db.add(v)
    v.description=desc; v.cvss=cvss; v.severity=severity; v.source="nvd"; v.published_at=data.get("published"); v.last_modified=data.get("lastModified")
    db.commit(); db.refresh(v); return v
