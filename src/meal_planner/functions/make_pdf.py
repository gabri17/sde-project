import requests #type: ignore

API_URL = "http://127.0.0.1:8000"

def plan_to_pdf(filters: str):
    ingredients_response = requests.get(API_URL+"/ingredients-adapter", params={"filters":filters}).json()
    ingredients = ingredients_response["list"]

    # Make a list only containing the names
    recipe_names = []
    for item in ingredients.keys():
        recipe_names.append(item)

    image_response = requests.post(API_URL+"/image-searcher", json={"names":recipe_names}).json()
    print(image_response)
    image_links = image_response["links"]

    params = {
        "ingredients": ingredients,
        "image_links": image_links
    }

    response = requests.post(API_URL+"/make-pdf", json=params).json()

    # Check response
    if response["status_code"] == 200:
        # Save the file if returned as a response
        return response
    else:
        return {"status_code": 400}