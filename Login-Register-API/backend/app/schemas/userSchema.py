from sqlalchemy import Column, String
from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str
    email:str
    name:str

class UserUpdate(BaseModel):
    username: str
    email:str
    name:str

class UserResponse(BaseModel):
    id:int
    name:str
    username: str
    email:str
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str