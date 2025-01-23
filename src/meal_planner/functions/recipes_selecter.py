import random
import requests #type: ignore

API_URL = "http://127.0.0.1:8000"

# Uses a Langauge Model to decide which recipes to put in the meal plan out of all those that have the desired filter(s)
def select_from_recipes(filters: str):
    
    response = requests.get(API_URL+"/recipes-adapter", params={"filters":filters}).json()

    if response["status_code"] == 404:
        return {"status_code": 404}

    recipes = response["recipes"]

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