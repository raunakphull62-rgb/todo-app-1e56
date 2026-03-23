from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from supabase import create_client, Client
from supabase.py import Database
from typing import List, Optional
from datetime import datetime
from jose import jwt
from config import settings
from database import supabase_url, supabase_key
from auth import authenticate_user, get_current_user

router = APIRouter()

supabase: Client = create_client(supabase_url, supabase_key)

class Todo(BaseModel):
    id: Optional[int]
    title: str
    description: Optional[str]
    completed: Optional[bool]
    due_date: Optional[datetime]
    user_id: int

@router.get("/todos", response_model=List[Todo])
async def get_todos(current_user: dict = Depends(get_current_user)):
    data = supabase.from_("Todo").select("*").eq("user_id", current_user["id"])
    todos = data.execute()
    if todos.error:
        raise HTTPException(status_code=500, detail="Failed to retrieve todos")
    return todos.data

@router.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int, current_user: dict = Depends(get_current_user)):
    data = supabase.from_("Todo").select("*").eq("id", todo_id).eq("user_id", current_user["id"])
    todo = data.execute()
    if todo.error:
        raise HTTPException(status_code=500, detail="Failed to retrieve todo")
    if not todo.data:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo.data[0]

@router.post("/todos", response_model=Todo)
async def create_todo(todo: Todo, current_user: dict = Depends(get_current_user)):
    data = supabase.from_("Todo").insert([{
        "title": todo.title,
        "description": todo.description,
        "completed": todo.completed,
        "due_date": todo.due_date,
        "user_id": current_user["id"]
    }])
    todo = data.execute()
    if todo.error:
        raise HTTPException(status_code=500, detail="Failed to create todo")
    return todo.data[0]

@router.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo: Todo, current_user: dict = Depends(get_current_user)):
    data = supabase.from_("Todo").update({
        "title": todo.title,
        "description": todo.description,
        "completed": todo.completed,
        "due_date": todo.due_date
    }).eq("id", todo_id).eq("user_id", current_user["id"])
    updated_todo = data.execute()
    if updated_todo.error:
        raise HTTPException(status_code=500, detail="Failed to update todo")
    if not updated_todo.data:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated_todo.data[0]

@router.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, current_user: dict = Depends(get_current_user)):
    data = supabase.from_("Todo").delete().eq("id", todo_id).eq("user_id", current_user["id"])
    deleted_todo = data.execute()
    if deleted_todo.error:
        raise HTTPException(status_code=500, detail="Failed to delete todo")
    if not deleted_todo.data:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}