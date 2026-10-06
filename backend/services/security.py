from datetime import datetime,timedelta,timezone
import jwt
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError,VerificationError
from sqlalchemy.orm import Session
from backend.config import settings
from backend.database.db import get_db
from backend.database.models import User
password_hash=PasswordHasher(); oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/api/auth/login"); ALGORITHM="HS256"
def hash_password(password:str)->str:return password_hash.hash(password)
def verify_password(password:str,hashed:str)->bool:
    try:return password_hash.verify(hashed,password)
    except Exception:return False
def create_access_token(user:User)->str:
    expire=datetime.now(timezone.utc)+timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode({"sub":str(user.id),"username":user.username,"role":user.role,"exp":expire},settings.jwt_secret,algorithm=ALGORITHM)
def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db))->User:
    exc=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid or expired token",headers={"WWW-Authenticate":"Bearer"})
    try:user_id=int(jwt.decode(token,settings.jwt_secret,algorithms=[ALGORITHM]).get("sub"))
    except Exception:raise exc
    user=db.get(User,user_id)
    if not user or not user.active:raise exc
    return user
def require_admin(user:User=Depends(get_current_user))->User:
    if user.role!="admin":raise HTTPException(status_code=403,detail="Admin role required")
    return user
