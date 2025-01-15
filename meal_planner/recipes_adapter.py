import get_recipes

# Extracts only the name of a recipe and its corresponing id from the json response of the spoonacular API
def extract_text_id(filters: str):
    response = get_recipes.get_recipes_with_filter("a")
    if (response["number"] == 0):
        exit(1) #//TODO use a better error

    recipes = []
    for recipe in response["results"]:
        recipes.append({
            "name": recipe["title"],
            "id": recipe["id"]
        })
    
    return recipes