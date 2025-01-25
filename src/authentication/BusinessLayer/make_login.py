from authentication.interfaces import LoginRequest
from authentication.BusinessLayer import jwt_manipulation, password_encrypter

import requests

API_URL = "http://127.0.0.1:8000"

def make_login(request: LoginRequest):

    username = request.username
    password = request.password

    if not username or not password:
        return {"status_code": 400, "detail": "Provide both username and password fields in body!"}

    data = requests.get(API_URL + "/get-user?username=" + username).json()
    if(data is not None):
        if(password_encrypter.check_password(data["password"], password)):                  #businesslogic
            token = jwt_manipulation.generate_jwt(username)                                 #businesslogic
            return {"status_code": 200, "message": "You correctly logged in!", "access_token": token}
        else:
            return {"status_code": 401, "detail": "Authentication failed"}
    else:
        return {"status_code": 401, "detail": "Authentication failed"}
