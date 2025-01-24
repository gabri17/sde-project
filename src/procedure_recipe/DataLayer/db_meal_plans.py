
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from environment import URI

#Get all meal planners created for a given user
def get_meal_plans_by_user(username: str):

    client = MongoClient(URI)
    db = client['ProgettoSDE']
    users_collection = db['Users']
    plans_collection = db['MealPlans']

    query = {"username": username}
    if(users_collection.find_one(query) is not None):
        res = plans_collection.find(query)
        if(res is None):
            return {"plans_response": []}
        else:
            #manipulation needed because returned object is intractable
            list_meal_plans = []
            for mp in list(res):
                obj = {
                    "date_meal_plan": mp["date"],
                    "recipes_number":  len(mp["ingredients"]),
                    "recipes_titles": list(mp["ingredients"])
                }
                list_meal_plans.append(obj)
            return {"plans_response": list_meal_plans}
    else:
        return {"plans_response": []}