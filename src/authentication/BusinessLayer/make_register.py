from authentication.interfaces import LoginRequest
from authentication.DataLayer import db_users
from authentication.BusinessLayer import password_encrypter


def make_register(request: LoginRequest):

    username = request.username
    password = request.password

    if not username or not password:
        return {"status_code": 400, "detail": "Provide both username and password fields in body!"}

    if(len(password) < 8):
        return {"status_code": 400, "detail": "Password must have at least length 8!"}
    elif(db_users.get_user(username) is not None):                                                         #data
        return {"status_code": 400, "detail": f"Username '{username}' already existing!"}
    else:
        hashed_password = password_encrypter.hash_password(password) #businesslogic
        db_users.save_user(username, hashed_password)                                                       #data
        return {"status_code": 200, "message": "User saved!", "Username": username, "Password encrypted saved": hashed_password}