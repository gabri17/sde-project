from typing import Dict, Union
from pydantic import BaseModel #type: ignore

API_URL = "http://127.0.0.1:8000"

class Recipes(BaseModel):
    offset: int
    number: int
    results: list[Dict[str, Union[str, int]]]
    totalResults: int

# Extracts only the name of a recipe and its corresponing id from the json response of the spoonacular API
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