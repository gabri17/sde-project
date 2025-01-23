import requests #type: ignore

API_KEY = "ce26c380d30d4c7eb862dd149f07a2a7"
API_URL = "https://api.spoonacular.com/recipes/complexSearch"

# GET request to spoonacular (https://spoonacular.com/food-api/docs)
# Gets the some info of the recipe with the name passed (e.g vegan, gluten-free, ...)
def get_recipe_by_name(nameRecipe: str):
    params = {
        "titleMatch": nameRecipe,
        "apiKey": API_KEY
    }
    response = requests.get(API_URL, params)
    return response.json()

