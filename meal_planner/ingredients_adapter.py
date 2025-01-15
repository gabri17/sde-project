import get_recipe_info

def extract_ingredients(filters: str):
    recipes_info = get_recipe_info.get_info_from_id(filter)

    # We make a dictionary where the key is the recipe title and the value is the list of ingredients
    ingredients = {}

    # Iterate through all recipes info
    for item in recipes_info:
        # We take the recipe title to use it as key
        name = item["title"]

        # Then we iterate through all the ingredients and add it to the ingredient list. This will be the value
        ingredient_list = []
        for ingredient in item["extendedIngredients"]:
            ingredient_list.append(ingredient["name"])

        # Finally, we add the (key, value) tuple to the dictionary
        ingredients.update({name: ingredient_list})

    return ingredients