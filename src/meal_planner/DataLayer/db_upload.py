import datetime
from typing import Dict, List
from authentication.BusinessLayer import jwt_manipulation
from pydantic import BaseModel #type: ignore
from pymongo.mongo_client import MongoClient #type: ignore
from pymongo.server_api import ServerApi #type: ignore
from environment import URI

from meal_planner.interfaces import RecipeRequest

def insert_plan_db(token: str, recipes: RecipeRequest):

    # A token has been inserted, validate it
    result = jwt_manipulation.verify_token(token)
    username = ""

    if result != 1 and result != 2 and result != 0:
        # Token is valid, extract username
        username = result["username"]
    else:
        return {"status_code": 404}

    client = MongoClient(URI, server_api=ServerApi('1'))

    try:
        client.admin.command('ping')
        print("connected to DB!")
    except Exception as e:
        print(e)

    db = client['ProgettoSDE']
    
    # Start by verifying that the username exists
    users_collection = db['Users']
    query = {"username": username}
    result = users_collection.find_one(query) 
    if result is None:
        print("No user found")
        return {"status_code": 404}
    
    # Access the meal_plans collection
    plans_collection = db['MealPlans']

    # Extract data from RecipeRequest
    ingredients = recipes.ingredients
    image_links = recipes.image_links

    # Get current datetime and use it to differentiate meal_plans for the same user
    current_datetime = datetime.datetime.now()
    # Convert to string and format
    datetime_string = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

    # Create the new DB entry
    plan_document = {
        "username": username,
        "date": datetime_string,
        "ingredients": ingredients,
        "images": image_links,
    }

    plans_collection.insert_one(plan_document)
    print("Meal PLan added to DB!")

    return {"status_code": 200}