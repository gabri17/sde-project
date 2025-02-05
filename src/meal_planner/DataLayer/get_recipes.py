import requests #type: ignore

from environment import API_KEY_SPOONACULAR as API_KEY

API_URL = "https://api.spoonacular.com/recipes/complexSearch"

# GET request to spoonacular (https://spoonacular.com/food-api/docs)
# Gets all recipes given a filter (e.g vegan, gluten-free, ...)

def get_recipes_with_filter(filters: str):
    """
        Calls the spoonacular API and asks for 100 recipes with the given filter.
        Returns a JSON containing those recipes
    """
    params = {
        "query": "",
        "diet": filters,
        "apiKey": API_KEY,
        "number": 100,
    }
    response = requests.get(API_URL, params)
    return response.json()