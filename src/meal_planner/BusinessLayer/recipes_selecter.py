import random
from typing import Dict, Union
from pydantic import BaseModel #type: ignore
from meal_planner.interfaces import RecipesTitles

API_URL = "http://127.0.0.1:8000"

# Given a list of recipe names and ids, take randomly some recipes out of the and returns their ids
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