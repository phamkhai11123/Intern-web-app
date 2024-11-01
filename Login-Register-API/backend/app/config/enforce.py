import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import casbin

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
    
# check_permission('admin@gmail.com','/user','get')

