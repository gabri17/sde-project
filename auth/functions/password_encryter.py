from functions import db_adapter
import bcrypt

def check_password(username: str, password: str) -> bool:
    stored_user = db_adapter.get_user(username)
    
    if(stored_user is None):
        return False
    
    stored_password = stored_user["password"]

    return bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8'))

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

#TODO: devo chiamare db_adapter.get_user(username) stile API?