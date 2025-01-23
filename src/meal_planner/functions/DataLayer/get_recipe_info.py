import requests #type: ignore
from typing import Dict, Union
from pydantic import BaseModel #type: ignore

API_KEY = "521555a76d7d411a83bbd678d50162bd"
API_URL = "https://api.spoonacular.com/recipes/informationBulk"

LOCAL_API_URL = "http://127.0.0.1:8000"

class SelectedRecipes(BaseModel):
    recipes: list[int]
    status_code: int

def get_info_from_id(selected_recipes: SelectedRecipes):
    # Process the list of ids (int) into a string
    recipes = list(map(str, selected_recipes.recipes))
    selected_recipes_str = ','.join(recipes)

    params = {
        "ids": selected_recipes_str,
        "apiKey": API_KEY,
        "includeNutrition": "false",
    }

    response = requests.get(API_URL, params).json()

    return {
        "list": response,
        "status_code": 200
    }