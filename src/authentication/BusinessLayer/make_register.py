from authentication.interfaces import LoginRequest
from authentication.BusinessLayer import password_encrypter

import requests

API_URL = "http://127.0.0.1:8000"


def make_register(request: LoginRequest):

    username_request = request.username
    password_request = request.password

    if not username_request or not password_request:
        return {"status_code": 400, "detail": "Provide both username and password fields in body!"}

    if(len(password_request) < 8):
        return {"status_code": 400, "detail": "Password must have at least length 8!"}
    
    user = requests.get(API_URL + "/get-user?username=" + username_request).json()                              #data
    if(user is not None):                                                         
        return {"status_code": 400, "detail": f"Username '{username_request}' already existing!"}
    else:
        hashed_password = password_encrypter.hash_password(password_request) #businesslogic
        params = {
            "username": username_request,
            "password": hashed_password
        }                                                       
        saved_user = requests.post(API_URL + "/save-user", json=params).json()                                 #data
        print(saved_user)
        return {"status_code": 200, "message": "User saved!", "Username": username_request, "Password encrypted saved": hashed_password}