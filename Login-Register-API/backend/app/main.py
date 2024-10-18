# main.py
from fastapi import FastAPI, Depends, HTTPException, status

from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from jose import JWTError, jwt
import os
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware
from .router import userRoute

# FastAPI instance
app = FastAPI()

origins = [
    "http://localhost:5173",  # your Vue.js app
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


app.include_router(userRoute.router)


