from typing import List, Dict, Union
from pydantic import BaseModel #type: ignore

# This class constitutes the body of the POST requests make-pdf

# /make-pdf body
class RecipeRequest(BaseModel):
    ingredients: Dict[str, List[str]]  # Example: {"Recipe1": ["Item1", "Item2"]}
    image_links: List[str]             # Example: ["http://link1.com", "http://link2.com"]

# /recipes-adapter body
class Recipes(BaseModel):
    offset: int
    number: int
    results: list[Dict[str, Union[str, int]]]
    totalResults: int

# /recipes-selecter body
class RecipesTitles(BaseModel):
    recipes: list[Dict[str, Union[str, int]]]

# /recipes-info body
class SelectedRecipes(BaseModel):
    recipes: list[int]
    status_code: int

# /ingredients-adapter body
class RecipesInfo(BaseModel):
    list: list
    status_code: int