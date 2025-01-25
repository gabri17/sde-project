from typing import List, Dict, Union
from pydantic import BaseModel #type: ignore

# This class constitutes the body of the POST requests make-pdf

# /make-pdf body
class RecipeRequest(BaseModel):
    """
    Input of /make-pdf and /upload_recipe services.
    """
    ingredients: Dict[str, List[str]]  # Example: {"Recipe1": ["Item1", "Item2"]}
    image_links: List[str]             # Example: ["http://link1.com", "http://link2.com"]

# /recipes-adapter body
class Recipes(BaseModel):
    """
    Input of /recipes-adapter service
    """
    offset: int
    number: int
    results: list[Dict[str, Union[str, int]]]
    totalResults: int

# /recipes-selecter body
class RecipesTitles(BaseModel):
    """
    Input of /recipes-selecter service
    """
    recipes: list[Dict[str, Union[str, int]]]

# /recipes-info body
class SelectedRecipes(BaseModel):
    """
    Input of /recipes-info service
    """
    recipes: list[int]
    status_code: int

# /ingredients-adapter body
class RecipesInfo(BaseModel):
    """
    Input of /ingredients-adapter service
    """
    list: list
    status_code: int