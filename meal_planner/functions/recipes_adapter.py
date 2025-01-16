from functions import get_recipes
import requests

API_URL = "http://127.0.0.1:8000"

# Extracts only the name of a recipe and its corresponing id from the json response of the spoonacular API
def extract_text_id(filters: str):
    response = requests.get(API_URL+"/get-recipes", params={"filters":filters}).json()
    
    if (response["number"] == 0):
        return {"status_code": 404}

    recipes = []
    for recipe in response["results"]:
        recipes.append({
            "name": recipe["title"],
            "id": recipe["id"]
        })
    
    return {"recipes": recipes, "status_code": 200}