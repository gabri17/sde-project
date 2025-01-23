import requests #type: ignore

API_URL = "http://127.0.0.1:8000"

def plan_to_pdf(filters: str, token: str):
    ingredients_response = requests.get(API_URL+"/ingredients-adapter", params={"filters":filters}).json()

    if ingredients_response["status_code"] == 404:
        return {"status_code": 404}

    ingredients = ingredients_response["list"]

    # Make a list only containing the names
    recipe_names = []
    for item in ingredients.keys():
        recipe_names.append(item)

    image_response = requests.post(API_URL+"/image-searcher", json={"names":recipe_names}).json()
    print(image_response)
    image_links = image_response["links"]

    json_params = {
        "ingredients": ingredients,
        "image_links": image_links
    }

    params = {
        "token": token
    }

    response = requests.post(API_URL+"/make-pdf", json=json_params, params=params).json()

    # Check response
    if response["status_code"] == 200:
        # Save the file if returned as a response
        return response
    else:
        return {"status_code": 404}