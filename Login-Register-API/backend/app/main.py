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
from pprint import pprint

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"  # Use a strong secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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


@app.middleware("http")
async def check_user_permissions(request: Request, call_next):
    # Trước khi xử lý yêu cầu
    # token = request.headers.get("Authorization")
    # print(token)
    user_email = None

    # if token:
    #     try:
    #         token = token.split(" ")[1]  # Get the actual token
    #         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    #         user_email = payload.get("sub")
    #         if user_email is None:
    #             raise HTTPException(status_code=401, detail="Invalid token")
    #     except JWTError:
    #         raise HTTPException(status_code=401, detail="Invalid token")
    # else:
    #     raise HTTPException(status_code=401, detail="Token is missing")

    path = request.url.path
    method = request.method

    # print(user_email)
    # Xử lý yêu cầu và lấy phản hồi
    response = await call_next(request)

    # Sau khi xử lý yêu cầu
    print(f"API called: Path = {path}, Method = {method}")

    return response

def get_email_from_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["email"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_token_from_request(request: Request) -> str:
    authorization: str = request.headers.get("Authorization")
    if not authorization:
        raise HTTPException(status_code=403, detail="Authorization header missing")
    token = authorization.split(" ")[1]
    return token

def check_permission(request: Request, token: str = Depends(get_token_from_request)) -> bool:
    email = get_email_from_token(token)
    method = request.method
    path = request.url.path
    
    # Casbin check: email (sub), method (act), path (obj)
    allowed = e.enforce(email, path, method)
    
    if not allowed:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    return True




