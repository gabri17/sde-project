
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

URI = "mongodb+srv://progettosde:ProgettoSde2024@clustersde.haahr.mongodb.net/?retryWrites=true&w=majority&appName=ClusterSDE"

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
