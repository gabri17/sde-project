from duckduckgo_search import DDGS  # type: ignore
from random import randrange
import requests  # type: ignore
from PIL import Image  # type: ignore
from io import BytesIO


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

        # Keep trying different images until a valid one is found
        while True:
            selected_image: int = randrange(100)
            url = results[selected_image]["image"]

            if is_valid_image_url(url) and try_open_image(url):
                image_links.append(url)
                break

    return {"links": image_links, "status_code": 200}


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


def try_open_image(url: str) -> bool:
    """Download the image and try to open it."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        image.verify()  # Verify the image integrity
        return True
    except (requests.RequestException, IOError):
        return False