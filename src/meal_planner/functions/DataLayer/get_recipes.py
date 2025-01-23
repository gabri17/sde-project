import requests #type: ignore

API_KEY = "521555a76d7d411a83bbd678d50162bd"
API_URL = "https://api.spoonacular.com/recipes/complexSearch"

# GET request to spoonacular (https://spoonacular.com/food-api/docs)
# Gets all recipes given a filter (e.g vegan, gluten-free, ...)
def get_recipes_with_filter(filters: str):
    params = {
        "query": "",
        "diet": filters,
        "apiKey": API_KEY,
        "number": 2,    #//TODO change this with the desired number in the final application
    }
    response = requests.get(API_URL, params)
    return response