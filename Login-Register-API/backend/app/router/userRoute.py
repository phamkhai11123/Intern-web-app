from typing import List
from fastapi import APIRouter,FastAPI,Query,Request
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
from ..config import enforce

router = APIRouter()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"  # Use a strong secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post("/register", response_model=userSchema.UserResponse, )
async def register(user: userSchema.UserCreate):
    db: Session = database.SessionLocal()
    existing_user = db.query(userModel.User).filter(userModel.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    password_hash = oauth.hash(user.password)
    new_user = userModel.User(username=user.username,
                               hashed_password=password_hash,
                               email= user.email,
                               name = user.name,
                                role = user.role)  
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user(db: Session, username: str):
    return db.query(userModel.User).filter(userModel.User.username == username).first()

@router.get("/user", response_model=List[userSchema.UserResponse],)
async def get_list_user(db:Session = Depends(database.get_db),user: dict = Depends(oauth.get_current_user)):
    with database.SessionLocal() as db:
        list_user = db.query(userModel.User).all()
        return list_user
    
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not admin",
            headers={"WWW-Authenticate": "Bearer"},
            )
# User login and token retrieval
@router.post("/token",response_model=userSchema.Token,name="login")
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
@router.get("/users/me",response_model = userSchema.UserResponse, )
async def read_users_me(current_user: userSchema.UserResponse = Depends(oauth.get_current_user)):
    return current_user

@router.put("/users/{user_id}",response_model=None)
def update_user(user_id: int, user_update: userSchema.UserUpdate,
                db: Session = Depends(database.get_db),
                current_user: dict = Depends(oauth.get_current_user)):
    
    user = db.query(userModel.User).filter(userModel.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.name = user_update.name
    user.username = user_update.username
    user.email = user_update.email
    user.role = user_update.role
    db.commit()
    db.refresh(user)
    return user
   

@router.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(database.get_db),current_user: dict = Depends(oauth.get_current_user)):
    user = db.query(userModel.User).filter(userModel.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}

@router.get("/queryUsers/", response_model=List[userSchema.UserResponse])
def get_users(name: str = Query(None), db: Session = Depends(database.get_db)):
    query = db.query(userModel.User)
    if name:
        query = query.filter(userModel.User.name.ilike(f"%{name}%"))
    return query.all()






