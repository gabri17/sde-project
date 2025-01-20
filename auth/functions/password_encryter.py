from functions import db_adapter
import bcrypt

def check_password(username: str, password: str) -> bool:
    stored_password = db_adapter.get_user(username)
    return bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8'))

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')
