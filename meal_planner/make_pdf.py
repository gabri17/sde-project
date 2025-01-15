import ingredients_adapter
import image_searcher

def plan_to_pdf(filters: str):
    ingredients = ingredients_adapter.extract_ingredients(filters)

    # Make a list only containing the names
    recipe_names = []
    for item in ingredients.keys():
        recipe_names.append(item)

    image_links = image_searcher.search(recipe_names)

    print(image_links)

    #//TODO -------------------------------------------------------------------
    # At the moment I'm making the PDF here, but this should be an internal API. I'll make this change in another moment

    

    #//TODO -------------------------------------------------------------------

plan_to_pdf("a")