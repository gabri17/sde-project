import requests #type: ignore

API_KEY = "521555a76d7d411a83bbd678d50162bd"
API_URL = "https://api.spoonacular.com/recipes/informationBulk"

def get_procedure_text_from_info(recipe_info):

    if(recipe_info is None):
        return ""

    text = recipe_info["procedure"] + "\n\n" + "It will be ready in " + str(recipe_info["readyInMinutes"]) + " minutes."
    return text
