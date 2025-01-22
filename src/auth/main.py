from fastapi import FastAPI, HTTPException, Request #type: ignore
from pydantic import BaseModel #type: ignore
from typing import List, Dict
from .functions import jwt_manipulation, password_encryter, db_adapter
from datetime import datetime

#TODO: usare auth0? https://auth0.com/blog/how-to-handle-jwt-in-python

class LoginRequest(BaseModel):
    username: str
    password: str

def all_meal_plans(request: Request):
    auth_header = request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized: token missing")

    token = auth_header.split(" ")[1]
    output = jwt_manipulation.verify_token(token)
    if(output == 1):
       raise HTTPException(status_code=401, detail="Unauthorized: invalid signature")
    elif(output == 2):
        raise HTTPException(status_code=401, detail="Unauthorized: token expired")
    elif(output == 0):
        raise HTTPException(status_code=500, detail="Internal server error")
    else:
        res = db_adapter.get_meal_plans_by_user(output["username"]) #usare un adapter anche per questo
        
        if(res is None):
            return {"data": []}
        else:
            list_parsed = db_adapter.manipulate(res)
            return {"meal_plans_number": len(list_parsed), "data": sorted(list_parsed, key=lambda x: datetime.strptime(x['date_meal_plan'], '%Y-%m-%d %H:%M:%S'), reverse=True)}

def make_login(request: LoginRequest):

    #TODO adapter needed??

    username = request.username
    password = request.password

    if not username or not password:
        raise HTTPException(status_code=400, detail="Provide both username and password fields in body!")

    if(db_adapter.exists_username(username)):
        if(password_encryter.check_password(username, password)):
            token = jwt_manipulation.generate_jwt(username)
            return {"message": "You correctly logged in!", "access_token": token}
        else:
            raise HTTPException(status_code=401, detail="Authentication failed")
    else:
        raise HTTPException(status_code=401, detail="Authentication failed")

def make_register(request: LoginRequest):

    #TODO adapter needed??

    username = request.username
    password = request.password

    if not username or not password:
        raise HTTPException(status_code=400, detail="Provide both username and password fields in body!")

    if(len(password) < 8):
        raise HTTPException(status_code=400, detail="Password must have at least length 8!")
    elif(db_adapter.exists_username(username)):
        raise HTTPException(status_code=400, detail=f"Username '{username}' already existing!")
    else:
        hashed_password = password_encryter.hash_password(password)
        db_adapter.save_user(username, hashed_password)
        return {"message": "User saved!", "Username": username, "Password encrypted saved": db_adapter.get_user(username)["password"]}
