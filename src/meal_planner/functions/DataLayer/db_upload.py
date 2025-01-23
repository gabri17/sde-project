import datetime
from typing import Dict, List
from pydantic import BaseModel
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from meal_planner.functions.DataLayer.environment import URI

# Struct to encapsulate all meal_plan data
class RecipeRequest(BaseModel):
    ingredients: Dict[str, List[str]]  # Example: {"Recipe1": ["Item1", "Item2"]}
    image_links: List[str]             # Example: ["http://link1.com", "http://link2.com"]

def insert_plan_db(username: str, recipes: RecipeRequest):

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
    
    print("Found user:")
    print(result)

    # Access the meal_plans collection
    plans_collection = db['MealPlans']

    # Extract data from RecipeRequest
    ingredients = recipes["ingredients"]
    image_links = recipes["image_links"]

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

#! TESTING
#ingredients = {"pizza": ["farina", "mozzarella", "pomodoro"]}
#images = ["https://cdn.shopify.com/s/files/1/0274/9503/9079/files/20220211142754-margherita-9920_5a73220e-4a1a-4d33-b38f-26e98e3cd986.jpg?v=1723650067"]

#recipe = RecipeRequest(ingredients=ingredients, image_links=images)

#insert_plan_db("admin", recipe)