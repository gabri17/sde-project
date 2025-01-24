import requests #type: ignore
from authentication.BusinessLayer import jwt_manipulation
from meal_planner.DataLayer.db_upload import insert_plan_db

API_URL = "http://127.0.0.1:8000"

def meal_plan(filters: str, token: str = "", upload: bool = True):
    # Get recipes that satisfy the given filter
    get_recipes_response = requests.get(API_URL+"/get-recipes", params={"filters": filters}).json()

    # Extract title and id of each recipe
    recipes_adapter_response = requests.post(API_URL+"/recipes-adapter", json=get_recipes_response).json()
    if recipes_adapter_response["status_code"] == 404:
        return {"status_code": 404}

    # Select 2 random recipes
    recipes_selecter_response = requests.post(API_URL+"/recipes-selecter", json=recipes_adapter_response).json()
    if recipes_selecter_response["status_code"] == 404:
        return {"status_code": 404}

    # Get information of the selected recipes
    recipes_info_response = requests.post(API_URL+"/recipes-info", json=recipes_selecter_response).json()
    if recipes_info_response["status_code"] == 404:
        return {"status_code": 404}

    # Extract ingrediants from recipes information
    ingredients_adapter_response = requests.post(API_URL+"/ingredients-adapter", json=recipes_info_response).json()
    if ingredients_adapter_response["status_code"] == 404:
        return {"status_code": 404}
    
    # Search images for the selected recipes
    # Make a list only containing the names
    recipe_names = []
    for item in ingredients_adapter_response["list"].keys():
        recipe_names.append(item)
    image_search_response = requests.post(API_URL+"/image-searcher", json={"names":recipe_names}).json()

    # Build a RecipeRequest
    input_request = {
        "ingredients": ingredients_adapter_response["list"],
        "image_links": image_search_response["links"]
    }
    # Use the RecipeRequest to make a pdf
    make_pdf_response = requests.post(API_URL+"/make-pdf", json=input_request).json()
    print(make_pdf_response)
    if make_pdf_response["status_code"] == 404:
        return {"status_code": 404}

    # If the user is authenticated and upload is True, we upload the meal plan to the DB
    if upload == True:
        # If user is authenticated, add meal_plan to his history
        # Check if authenticated
        if token != "":
            # A token has been inserted, validate it
            result = jwt_manipulation.verify_token(token)

            if result != 1 and result != 2 and result != 0:
                # Token is valid, extract username
                username = result["username"]

                # Insert the meal plan in the DB for that user
                #//TODO Make this an API
                result = insert_plan_db(username, input_request)
                
                if (result["status_code"] == 404):
                    return {"status_code": 404}
                
    return {"status_code": 201}