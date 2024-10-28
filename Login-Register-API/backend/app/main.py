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
from .models import userModel
from .database import database


userModel.database.Base.metadata.create_all(bind= database.engine)
# FastAPI instance
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(userRoute.router)


