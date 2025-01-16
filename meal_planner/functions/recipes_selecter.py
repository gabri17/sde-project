import random
import g4f #type: ignore
from functions import recipes_adapter
import requests

API_URL = "http://127.0.0.1:8000"

# Uses a Langauge Model to decide which recipes to put in the meal plan out of all those that have the desired filter(s)
def select_from_recipes(filters: str):
    
    response = requests.get(API_URL+"/recipes-adapter", params={"filters":filters}).json()

    if response["status_code"] == 404:
        return {"status_code": 404}

    recipes = response["recipes"]
    random.shuffle(recipes)

    # Only take the names of the recipes
    counter = 0
    recipes_names = ""
    for recipe in recipes:
        recipes_names += recipe["name"] + "\n"
        counter += 1
        if counter >= 5:
            break

    # Pass the names to ChatGPT, which will choose the recipes to put in the meal plan
    g4f.check_version = False # Disable automatic version checking
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,                                                                               #//TODO The number 2 here is arbitrary
        messages=[{"role": "user", "content": "Given the following list of recipes:\n\n" + recipes_names + "\nChoose 2 random recipes and only output their name, one per line. In order to actually make the choice random, please choose the recipes based on randomly generated numbers using as seed time(NULL)"}],
    )
    ' '.join(response)
    
    # Get ids of selected recipes
    selected_recipes = []
    for recipe in recipes:
        if recipe["name"] in response:
            selected_recipes.append(recipe["id"])

    return {"recipes": selected_recipes, "status_code": 200}