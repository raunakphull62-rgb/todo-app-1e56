from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from supabase import create_client, Client
from supabase.py import User
from typing import List
from auth import verify_jwt
from schemas.User import UserCreate, UserResponse
from config import SUPABASE_URL, SUPABASE_KEY

supabase_url = os.getenv('SUPABASE_URL', SUPABASE_URL)
supabase_key = os.getenv('SUPABASE_KEY', SUPABASE_KEY)
supabase: Client = create_client(supabase_url, supabase_key)

router = APIRouter()
security = HTTPBearer()

class UserList(BaseModel):
    users: List[UserResponse]

@router.get("/users", response_model=UserList)
async def get_users(token: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = verify_jwt(token.credentials)
        users = supabase.from_('users').select('*')
        return {"users": users.execute()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, token: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = verify_jwt(token.credentials)
        user = supabase.from_('users').select('*').eq('id', user_id).execute()
        if not user.data:
            raise HTTPException(status_code=404, detail="User not found")
        return user.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate, token: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = verify_jwt(token.credentials)
        new_user = supabase.from_('users').insert([user.dict()]).execute()
        return new_user.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user: UserCreate, token: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = verify_jwt(token.credentials)
        updated_user = supabase.from_('users').update([user.dict()]).eq('id', user_id).execute()
        if not updated_user.data:
            raise HTTPException(status_code=404, detail="User not found")
        return updated_user.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/users/{user_id}")
async def delete_user(user_id: str, token: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = verify_jwt(token.credentials)
        supabase.from_('users').delete().eq('id', user_id).execute()
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))