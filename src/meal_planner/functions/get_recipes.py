import requests #type: ignore

API_KEY = "ce26c380d30d4c7eb862dd149f07a2a7"
API_URL = "https://api.spoonacular.com/recipes/complexSearch"

# GET request to spoonacular (https://spoonacular.com/food-api/docs)
# Gets all recipes given a filter (e.g vegan, gluten-free, ...)
def get_recipes_with_filter(filters: str):
    params = {
        "query": "",
        "diet": filters,
        "apiKey": API_KEY,
        "number": 100,    #//TODO change this with the desired number in the final application
    }
    response = requests.get(API_URL, params)
    return response