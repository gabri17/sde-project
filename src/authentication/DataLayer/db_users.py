from environment import URI
from pymongo.mongo_client import MongoClient

def exists_username(username: str) -> bool:
    
    client = MongoClient(URI)
    db = client['ProgettoSDE']
    users_collection = db['Users']

    query = {"username": username}
    return users_collection.find_one(query) is not None 

def get_user(username: str):

    client = MongoClient(URI)
    db = client['ProgettoSDE']
    users_collection = db['Users']

    query = {"username": username}
    return users_collection.find_one(query)

def save_user(username: str, password: str):

    client = MongoClient(URI)
    db = client['ProgettoSDE']
    users_collection = db['Users']

    query = {"username": username}
    if(users_collection.find_one(query) is None):
        
        user_document = {
        "username": username,
        "password": password
        }
        
        result = users_collection.insert_one(user_document)
        inserted_user = users_collection.find_one({"_id": result.inserted_id})

    
        print(f"User '{inserted_user["username"]}' has been successfully inserted.")
        return inserted_user
    else:
        return None
