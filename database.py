from supabase import create_client, Client
from fastapi import HTTPException
from pydantic import BaseModel
from typing import Optional
import os

class DatabaseConfig(BaseModel):
    url: str
    key: str

class Database:
    def __init__(self, config: DatabaseConfig):
        self.supabase_url = config.url
        self.supabase_key = config.key
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)

    async def fetch(self, table: str, query: Optional[dict] = None):
        try:
            data = self.supabase.from_(table).select('*')
            if query:
                data = data.filter(query)
            return await data.execute()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def insert(self, table: str, data: dict):
        try:
            return await self.supabase.from_(table).insert([data]).execute()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def update(self, table: str, id: str, data: dict):
        try:
            return await self.supabase.from_(table).update(data).eq('id', id).execute()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def delete(self, table: str, id: str):
        try:
            return await self.supabase.from_(table).delete().eq('id', id).execute()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

def get_database_config() -> DatabaseConfig:
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    if not supabase_url or not supabase_key:
        raise HTTPException(status_code=500, detail='Supabase URL and key are required')
    return DatabaseConfig(url=supabase_url, key=supabase_key)

database_config = get_database_config()
db = Database(database_config)