from os import write
import ingredients_adapter
import image_searcher
import requests #type: ignore

API_URL = "http://127.0.0.1:8000/make-pdf"

def plan_to_pdf(filters: str):
    ingredients = ingredients_adapter.extract_ingredients(filters)

    # Make a list only containing the names
    recipe_names = []
    for item in ingredients.keys():
        recipe_names.append(item)

    image_links = image_searcher.search(recipe_names)

    params = {
        "ingredients": ingredients,
        "image_links": image_links
    }

    response = requests.post(API_URL, json=params)

    # Check response
    if response.status_code == 200:
        # Save the file if returned as a response
        with open("DailyMealPlanDownloaded.pdf", "wb") as file:
            file.write(response.content)
        print("PDF downloaded successfully!")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

plan_to_pdf("gluten-free")