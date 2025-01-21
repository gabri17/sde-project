import requests #type: ignore

API_URL = "http://127.0.0.1:8000"

def extract_ingredients(filters: str):

    response = requests.get(API_URL+"/recipes-info", params={"filters":filters}).json()

    if response["status_code"] == 404:
        return {"status_code": 404}
    
    recipes_info = response["list"]

    # We make a dictionary where the key is the recipe title and the value is the list of ingredients
    ingredients = {}

    # Iterate through all recipes info
    for item in recipes_info:
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