from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from supabase import create_client, Client
from supabase.py import Auth
from jose import jwt
from datetime import datetime, timedelta
import os
import logging

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
JWT_SECRET = os.getenv("JWT_SECRET")

# Initialize Supabase client
supabase_url: str = SUPABASE_URL
supabase_key: str = SUPABASE_KEY
supabase: Client = create_client(supabase_url, supabase_key)

# Initialize FastAPI app
app = FastAPI()

# Initialize CORS
origins = [
    "http://localhost:8000",
    "https://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize JWT authentication
security = HTTPBearer()

# Define a function to verify JWT token
def verify_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Define a function to authenticate user
async def authenticate_user(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")
    token = token.split(" ")[1]
    payload = verify_token(token)
    return payload

# Define a route for root
@app.get("/")
async def root():
    return {"message": "Welcome to Todo App"}

# Include routes
from routes.User import user_router
from routes.Todo import todo_router

app.include_router(user_router)
app.include_router(todo_router)