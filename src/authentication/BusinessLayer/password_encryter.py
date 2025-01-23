import bcrypt

def check_password(encrypted_password: str, password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), encrypted_password.encode('utf-8'))

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

#TODO: devo chiamare db_adapter.get_user(username) stile API?