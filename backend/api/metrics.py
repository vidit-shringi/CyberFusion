from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
from backend.database.db import get_db
from backend.database.models import Event
from backend.services.security import get_current_user
router = APIRouter(prefix="/api/metrics", tags=["metrics"])
@router.get("/snapshot")
def metrics_snapshot(db: Session = Depends(get_db), user=Depends(get_current_user)):
    events=db.scalars(select(Event)).all()
    if not events: return {"precision":0,"recall":0,"f1":0,"false_positive_rate":0,"note":"No events available. Load demo data first."}
    y_true=[]; y_pred=[]
    for e in events:
        label=(e.metadata_json or {}).get("label")
        if label not in {"normal","attack"}: continue
        y_true.append(1 if label=="attack" else 0)
        y_pred.append(1 if (0.35*e.rule_score+0.25*e.anomaly_score+0.25*e.correlation_score+0.15*e.threat_score)>=55 else 0)
    if not y_true: return {"precision":0,"recall":0,"f1":0,"false_positive_rate":0,"note":"No labeled events available."}
    tn,fp,fn,tp=confusion_matrix(y_true,y_pred,labels=[0,1]).ravel(); fpr=fp/max(fp+tn,1)
    return {"precision":round(precision_score(y_true,y_pred,zero_division=0),4),"recall":round(recall_score(y_true,y_pred,zero_division=0),4),"f1":round(f1_score(y_true,y_pred,zero_division=0),4),"false_positive_rate":round(fpr,4),"samples":len(y_true)}
