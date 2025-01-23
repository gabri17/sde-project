import random
from typing import Dict, Union
from pydantic import BaseModel #type: ignore

API_URL = "http://127.0.0.1:8000"

class RecipesTitles(BaseModel):
    recipes: list[Dict[str, Union[str, int]]]

# Uses a Langauge Model to decide which recipes to put in the meal plan out of all those that have the desired filter(s)
def select_from_recipes(input_recipes: RecipesTitles):
    recipes = input_recipes.recipes

    # Shuffle the recipes
    random.shuffle(recipes)

    # Only take the ids of the first 2 recipes
    counter = 0
    selected_recipes = []
    for recipe in recipes:
        selected_recipes.append(recipe["id"])
        counter += 1
        if counter >= 2:
            break

    return {"recipes": selected_recipes, "status_code": 200}