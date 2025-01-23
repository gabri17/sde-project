import requests #type: ignore

API_URL = "http://127.0.0.1:8000"

# Extracts only the id of a recipe, passing in input the array given back by get_recipe
def extract_recipe_id(recipes: str):
    
    if(len(recipes) == 0):
        return None
    else:
        return {"id": recipes[0]["id"], "status_code": 200}  