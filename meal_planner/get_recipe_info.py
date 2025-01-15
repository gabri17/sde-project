import json
import requests #type: ignore
import recipes_selecter

API_KEY = "ce26c380d30d4c7eb862dd149f07a2a7"
API_URL = "https://api.spoonacular.com/recipes/informationBulk"

def get_info_from_id(filters: str):
    selected_recipes = recipes_selecter.select_from_recipes(filters)

    # Process the list of ids (int) into a string
    selected_recipes = list(map(str, selected_recipes))
    selected_recipes_str = ','.join(selected_recipes)

    params = {
        "ids": selected_recipes_str,
        "apiKey": API_KEY,
        "includeNutrition": "false",
    }

    response = requests.get(API_URL, params).json()

    return response