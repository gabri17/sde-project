import requests #type: ignore

from environment import API_KEY_SPOONACULAR as API_KEY

API_URL = "https://api.spoonacular.com/recipes/complexSearch"

# GET request to spoonacular (https://spoonacular.com/food-api/docs)
# Gets some info of the recipe with the NAME passed
def get_recipe_by_name(nameRecipe: str):
    params = {
        "titleMatch": nameRecipe,
        "apiKey": API_KEY
    }
    response = requests.get(API_URL, params)
    return response.json()

