from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.database.db import get_db
from backend.database.models import User, AuditLog
from backend.database.schemas import LoginRequest, TokenResponse, UserOut
from backend.services.security import verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])
_login_failures: dict[str, int] = {}

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, request: Request, db: Session = Depends(get_db)):
    key = payload.username.lower().strip()
    if _login_failures.get(key, 0) >= 8:
        raise HTTPException(status_code=429, detail="Too many failed login attempts; try again later.")
    user = db.scalar(select(User).where(User.username == key))
    if not user or not verify_password(payload.password, user.password_hash):
        _login_failures[key] = _login_failures.get(key, 0) + 1
        raise HTTPException(status_code=401, detail="Invalid credentials")
    _login_failures[key] = 0
    db.add(AuditLog(actor=user.username, action="login", resource="/api/auth/login", details={"ip": request.client.host if request.client else None}))
    db.commit()
    return TokenResponse(access_token=create_access_token(user))

@router.get("/me", response_model=UserOut)
def me(user=Depends(get_current_user)):
    return user
