import requests #type: ignore

API_KEY = "ce26c380d30d4c7eb862dd149f07a2a7"
API_URL = "https://api.spoonacular.com/recipes/informationBulk"

def get_info_from_id(id):
   
    params = {
        "apiKey" : API_KEY,
        "ids" : id 
    }

    response = requests.get(API_URL, params=params).json()
   
    list_response = list(response)
    if(len(list_response) == 0):
        return None
    else:
        recipe = list_response[0]
        recipe_info = {

        }
        recipe_info["title"] = recipe["title"]
        recipe_info["readyInMinutes"] = recipe["readyInMinutes"]
        recipe_info["procedure"] = recipe["instructions"]

    return recipe_info
