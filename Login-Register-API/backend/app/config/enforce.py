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

def check_per(request: Request, token: str = Depends(get_token_from_request)) -> bool:
    email = get_email_from_token(token)
    method = request.method
    path = request.url.path
    
    # Casbin check: email (sub), method (act), path (obj)
    allowed = enf.enforce(email, path, method)
    
    if not allowed:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    return True



