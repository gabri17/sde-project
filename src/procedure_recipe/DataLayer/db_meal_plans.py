
from pymongo.mongo_client import MongoClient
from environment import URI

from authentication.BusinessLayer import jwt_manipulation

#Get all meal planners created for a given user
def get_meal_plans_by_user(access_token: str):
    
    if not access_token:
        return {"status_code":401, "detail":"Unauthorized: token missing"}

    output = jwt_manipulation.verify_token(access_token)
    
    if(output == 0):
        return {"status_code":401, "detail":"Unauthorized: token not verified or internal server error"}

    client = MongoClient(URI)
    db = client['ProgettoSDE']
    users_collection = db['Users']
    plans_collection = db['MealPlans']

    query = {"username": output["username"]}
    if(users_collection.find_one(query) is not None):
        res = plans_collection.find(query)
        if(res is None):
            return {"plans_response": []}
        else:
            #just few manipulation to make _id iterable
            list_meal_plans = []
            for mp in list(res):
                mp["_id"] = str(mp["_id"])
                list_meal_plans.append(mp)
            return {"plans_response": list_meal_plans}
    else:
        return {"plans_response": []}