fake_db = {}

#TODO diventa un servizio?
def exists_username(username: str) -> bool:
    return username in fake_db

def save_user(username: str, password: str):
    fake_db[username] = password

def get_user(username: str):
    if(not exists_username(username)):
        return None
    return fake_db[username]

