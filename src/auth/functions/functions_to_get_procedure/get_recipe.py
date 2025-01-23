import requests #type: ignore

API_KEY = "521555a76d7d411a83bbd678d50162bd"
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

