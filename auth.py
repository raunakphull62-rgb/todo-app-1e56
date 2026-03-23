from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional

from config import settings
from database import supabase

security = HTTPBearer()

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return plain_password == hashed_password

def get_password_hash(password: str) -> str:
    return password

def authenticate_user(username: str, password: str) -> bool:
    user = supabase.from_('User').select('password').eq('username', username).execute()
    if user.data:
        return verify_password(password, user.data[0]['password'])
    return False

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(token: HTTPAuthorizationCredentials) -> str:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = supabase.from_('User').select('username').eq('username', token_data.username).execute()
    if not user.data:
        raise credentials_exception
    return token_data.username

async def get_current_active_user(current_user: str) -> str:
    user = supabase.from_('User').select('username').eq('username', current_user).execute()
    if not user.data:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user