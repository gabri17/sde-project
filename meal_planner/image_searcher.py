from duckduckgo_search import DDGS # type: ignore

def search(recipe_names: list):

    # Create a list which will hold all links
    image_links = []

    # For each recipe name, look for an image and put it into the list
    for recipe in recipe_names:
        results = DDGS().images(
            keywords=recipe,
            region="wt-wt",
            safesearch="on",
            size=None,
            type_image=None,
            layout=None,
            license_image=None,
            max_results=1,
        )
        image_links.append(results[0]["image"])

    return image_links