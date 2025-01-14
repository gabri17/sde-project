import g4f #type: ignore
import recipes_adapter

def select_from_recipes(filters: str):
    recipes = recipes_adapter.extract_text_id(filters)

    # Only take the names of the recipes
    recipes_names = ""
    for recipe in recipes:
        recipes_names += recipe["name"] + "\n"

    # Pass the names to ChatGPT, which will choose the recipes to put in the meal plan
    g4f.check_version = False # Disable automatic version checking
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,                                                                               #//TODO The number 2 here is arbitrary
        messages=[{"role": "user", "content": "Given the following list of recipes:\n\n" + recipes_names + "\nChoose 2 recipes and only output their name, one per line"}],
    )
    ' '.join(response)
    
    # Get ids of selected recipes
    selected_recipes = []
    for recipe in recipes:
        if recipe["name"] in response:
            selected_recipes.append(recipe["id"])

    print(selected_recipes)

select_from_recipes("a")