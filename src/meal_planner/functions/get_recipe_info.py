import requests #type: ignore

API_KEY = "ce26c380d30d4c7eb862dd149f07a2a7"
API_URL = "https://api.spoonacular.com/recipes/informationBulk"

LOCAL_API_URL = "http://127.0.0.1:8000"

def get_info_from_id(filters: str):
    response = requests.get(LOCAL_API_URL+"/recipes-selecter", params={"filters":filters}).json()

    if response["status_code"] == 404:
        return {"status_code": 404}

    selected_recipes = response["recipes"]

    # Process the list of ids (int) into a string
    selected_recipes = list(map(str, selected_recipes))
    selected_recipes_str = ','.join(selected_recipes)

    params = {
        "ids": selected_recipes_str,
        "apiKey": API_KEY,
        "includeNutrition": "false",
    }

    response = requests.get(API_URL, params).json()

    return {
        "list": response,
        "status_code": 200
    }