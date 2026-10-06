from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.database.db import get_db
from backend.database.models import Asset, User
from backend.database.schemas import AssetIn
from backend.services.security import get_current_user

router = APIRouter(prefix="/api/assets", tags=["assets"])

@router.get("")
def list_assets(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return [{"asset_id":a.asset_id,"hostname":a.hostname,"ip":a.ip,"type":a.type,"criticality":a.criticality,"internet_exposed":a.internet_exposed,"owner":a.owner,"environment":a.environment} for a in db.scalars(select(Asset)).all()]

@router.post("")
def create_asset(payload: AssetIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if db.scalar(select(Asset).where(Asset.asset_id == payload.asset_id)):
        raise HTTPException(status_code=409, detail="Asset exists")
    asset = Asset(**payload.model_dump())
    db.add(asset); db.commit(); db.refresh(asset)
    return asset
