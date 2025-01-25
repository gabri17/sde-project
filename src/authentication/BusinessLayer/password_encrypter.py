import bcrypt

def check_password(encrypted_password: str, password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), encrypted_password.encode('utf-8'))

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

#not services, just auxiliary functions used to generate jwt in login service and verify it when needed