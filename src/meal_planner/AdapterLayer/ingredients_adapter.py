from typing import Dict, Union
from pydantic import BaseModel #type: ignore
from meal_planner.interfaces import RecipesInfo

API_URL = "http://127.0.0.1:8000"

#
#class RecipesInfo(BaseModel):
    #list: list
    #status_code: int

#Extracts the title and corresponding ingredients of each recipe from the JSON returned by the spoonacular API
def extract_ingredients(recipes_info: RecipesInfo):
    
    info = recipes_info.list

    # We make a dictionary where the key is the recipe title and the value is the list of ingredients
    ingredients = {}

    # Iterate through all recipes info
    for item in info:
        # We take the recipe title to use it as key
        name = item["title"]

        # Then we iterate through all the ingredients and add it to the ingredient list. This will be the value
        ingredient_list = []
        for ingredient in item["extendedIngredients"]:
            # We extract amount + metric + name of each ingredient
            tmp = ""
            tmp += str(ingredient["measures"]["us"]["amount"]) + " "
            tmp += ingredient["measures"]["us"]["unitLong"] + " "
            tmp += ingredient["name"]
            ingredient_list.append(tmp)

        # Finally, we add the (key, value) tuple to the dictionary
        ingredients.update({name: ingredient_list})

    return {
        "list": ingredients,
        "status_code": 200
    }