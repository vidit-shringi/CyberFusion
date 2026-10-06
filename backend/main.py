from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from sqlalchemy import select
from backend.config import settings
from backend.database.db import Base,engine,SessionLocal
from backend.database.models import User,Asset
from backend.services.security import hash_password
from backend.core.rules import ensure_default_rules
from backend.api import auth,events,incidents,dashboard,assets,vulnerabilities,forensics,metrics,pqc,demo
BASE_DIR=Path(__file__).resolve().parents[1]; FRONTEND_DIR=BASE_DIR/"frontend"
def seed():
    Base.metadata.create_all(bind=engine); db=SessionLocal()
    try:
        ensure_default_rules(db); admin=db.scalar(select(User).where(User.username==settings.admin_username.lower()))
        if not admin: db.add(User(user_id="USR-ADMIN",username=settings.admin_username.lower(),password_hash=hash_password(settings.admin_password),role="admin"))
        for asset_id,crit,exposed in [("ASSET-WEB-01","HIGH",True),("ASSET-DB-01","CRITICAL",False),("ASSET-DEV-01","LOW",False)]:
            if not db.scalar(select(Asset).where(Asset.asset_id==asset_id)): db.add(Asset(asset_id=asset_id,hostname=asset_id.lower(),type="server" if "DB" not in asset_id else "database",criticality=crit,internet_exposed=exposed,environment="lab"))
        db.commit()
    finally: db.close()
@asynccontextmanager
async def lifespan(app:FastAPI):
    seed(); yield
app=FastAPI(title=settings.app_name,version="1.0.0",lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=settings.frontend_origin,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
for router in [auth.router,events.router,incidents.router,dashboard.router,assets.router,vulnerabilities.router,forensics.router,metrics.router,pqc.router,demo.router]: app.include_router(router)
@app.get("/api/health")
def health(): return {"status":"ok","service":settings.app_name,"environment":settings.environment}
app.mount("/",StaticFiles(directory=FRONTEND_DIR,html=True),name="frontend")
