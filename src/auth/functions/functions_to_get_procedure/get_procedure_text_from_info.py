import requests #type: ignore

API_KEY = "ce26c380d30d4c7eb862dd149f07a2a7"
API_URL = "https://api.spoonacular.com/recipes/informationBulk"

def get_procedure_text_from_info(recipe_info):

    if(recipe_info is None):
        return ""

    text = recipe_info["procedure"] + "\n\n" + "It will be ready in " + str(recipe_info["readyInMinutes"]) + " minutes."
    return text
