from typing import Dict, Union
from pydantic import BaseModel #type: ignore
from meal_planner.interfaces import Recipes

API_URL = "http://127.0.0.1:8000"

# Extracts only the name of a recipe and its corresponing id from the json response of the spoonacular API
# An adapter that extracts recipe title and id from the JSON returned by the spoonacular API
def extract_text_id(recipe_list: Recipes):
    if (len(recipe_list.results) < 2):
        return {"status_code": 404}

    recipes = []
    for recipe in recipe_list.results:
        recipes.append({
            "name": recipe["title"],
            "id": recipe["id"]
        })
    
    return {"recipes": recipes, "status_code": 200}