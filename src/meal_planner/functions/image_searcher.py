from duckduckgo_search import DDGS  # type: ignore
from random import randrange
import requests #type: ignore

def search(recipe_names):
    # Create a list which will hold all links
    image_links = []

    recipe_list = recipe_names["names"]
    print(recipe_list)

    # For each recipe name, look for an image and put it into the list
    for recipe in recipe_list:
        results = DDGS().images(
            keywords=recipe,
            region="wt-wt",
            safesearch="on",
            size=None,
            type_image=None,
            layout=None,
            license_image=None,
            max_results=100,
        )

        selected_image: int = randrange(100)
        while is_valid_image_url(results[selected_image]["image"]) == False:
            selected_image: int = randrange(100)

        url = results[selected_image]["image"]

        image_links.append(url)

    return {"links":image_links, "status_code": 200}


def is_valid_image_url(url: str) -> bool:
    """Check if the URL points to a valid image."""
    try:
        response = requests.head(url, timeout=10)
        response.raise_for_status()
        
        # Check Content-Type header
        content_type = response.headers.get("Content-Type", "")
        return "image" in content_type
    except (requests.RequestException, KeyError):
        return False