from sqlalchemy import Column, String
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class Roles(str,Enum):
    user = 'user'
    admin = 'admin'


class UserCreate(BaseModel):
    username: str
    password: str
    email:str
    name:str
    role:str

class UserUpdate(BaseModel):
    username: str
    email:str
    name:str
    role:str

class UserResponse(BaseModel):
    id:int
    name:str
    username: str
    email:str
    role:str
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str