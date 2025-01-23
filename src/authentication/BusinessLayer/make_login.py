from authentication.interfaces import LoginRequest
from authentication.DataLayer import db_users
from authentication.BusinessLayer import jwt_manipulation, password_encrypter

def make_login(request: LoginRequest):

    username = request.username
    password = request.password

    if not username or not password:
        return {"status_code": 400, "detail": "Provide both username and password fields in body!"}

    if(db_users.exists_username(username)): #data
        data = db_users.get_user(username) #data
        if(password_encrypter.check_password(data["password"], password)):   #businesslogic
            token = jwt_manipulation.generate_jwt(username)         #businesslogic
            return {"status_code": 200, "message": "You correctly logged in!", "access_token": token}
        else:
            return {"status_code": 401, "detail": "Authentication failed"}
    else:
        return {"status_code": 401, "detail": "Authentication failed"}
