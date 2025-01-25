from environment import URI
from pymongo.mongo_client import MongoClient

def get_user(username: str):

    client = MongoClient(URI)
    db = client['ProgettoSDE']
    users_collection = db['Users']

    query = {"username": username}
    obj = users_collection.find_one(query)
    if(obj is None):
        return obj
    obj["_id"] = str(obj["_id"])    #necessary otherwise the object returned by MongoDB is returnable
    return obj

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
        inserted_user["_id"] = str(inserted_user["_id"]) #necessary otherwise the object returned by MongoDB is returnable
        return inserted_user
    else:
        return None
