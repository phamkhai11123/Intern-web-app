import os
from fastapi import FastAPI, Depends, HTTPException,Request
from fastapi.security import OAuth2PasswordBearer
import casbin
from jose import JWTError, jwt

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"  # Use a strong secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# Initialize FastAPI
app = FastAPI()

current_directory = os.path.dirname(os.path.abspath(__file__))

# Initialize Casbin Enforcer
model_path = os.path.join(current_directory, "model.conf")
policy_path = os.path.join(current_directory, "policy.csv")
enf = casbin.Enforcer(model_path, policy_path)

def check_permission(user: str, obj: str, act: str):
    if enf.enforce(user, obj, act):
        print(f"{user} được phép thực hiện hành động {act} trên {obj}.")
    else:
        print(f"{user} khong được phép thực hiện hành động {act} trên {obj}.")
        raise HTTPException(status_code=403, detail="Access denied")
    







