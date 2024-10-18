from fastapi import APIRouter,FastAPI
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from jose import JWTError, jwt
from ..database import database
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware
from ..models import userModel
from ..schemas import userSchema 
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..oauth import oauth


router = APIRouter()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"  # Use a strong secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30




@router.post("/register", response_model=userSchema.UserResponse)
async def register(user: userSchema.UserCreate):
    db: Session = database.SessionLocal()
    existing_user = db.query(userModel.User).filter(userModel.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    password_hash = oauth.hash(user.password)
    new_user = userModel.User(username=user.username, hashed_password=password_hash,email= user.email)  # Use hashed password in production
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user(db: Session, username: str):
    return db.query(userModel.User).filter(userModel.User.username == username).first()


# User login and token retrieval
@router.post("/token",response_model=userSchema.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db : Session = Depends(database.get_db)):
    user = get_user(db, form_data.username)
    if not user or not oauth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = oauth.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Get current user
@router.get("/users/me", response_model=userSchema.UserResponse)
async def read_users_me(token: str = Depends(oauth.oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    db: Session = database.SessionLocal()
    user = db.query(userModel.User).filter(userModel.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

