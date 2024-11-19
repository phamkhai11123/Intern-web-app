# main.py
from fastapi import FastAPI, Depends, HTTPException, status,Request
from jose import JWTError, jwt
import os
from fastapi.middleware.cors import CORSMiddleware
from .oauth import oauth
from .router import userRoute
from .models import userModel
from .database import database
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

# Tải các biến môi trường từ .env (nếu có)
load_dotenv()

# Lấy DATABASE_URL từ biến môi trường
DATABASE_URL = os.getenv("DATABASE_URL")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"  # Use a strong secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

userModel.database.Base.metadata.create_all(bind= database.engine)
# FastAPI instance
app = FastAPI()


@app.get("/")
def read_root():
    return {"DB_URL": DATABASE_URL}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(userRoute.router)


@app.middleware("http")
async def check_user_permissions(request: Request, call_next):

    path = request.url.path
    method = request.method

    response = await call_next(request)

    # Sau khi xử lý yêu cầu
    print(f"API called: Path = {path}, Method = {method}")

    return response





