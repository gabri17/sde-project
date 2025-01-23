
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from .environment import URI

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

#torna tutti i meal plans di un utente
def get_meal_plans_by_user(username: str):

    client = MongoClient(URI)
    db = client['ProgettoSDE']
    users_collection = db['Users']
    plans_collection = db['MealPlans']

    query = {"username": username}
    if(users_collection.find_one(query) is not None):
        res = plans_collection.find(query)
        return res       
    else:
        return None

def manipulate(cursor):

    if(cursor is None):
        return []

    list_meal_plans = []
    for mp in list(cursor):
        obj = {
            "date_meal_plan": mp["date"],
            "recipes_number":  len(mp["ingredients"]),
            "recipes_titles": list(mp["ingredients"])
        }
        list_meal_plans.append(obj)

    return list_meal_plans
