from fastapi import FastAPI, Response, status #type: ignore
from fastapi.responses import FileResponse #type: ignore
import jwt #type: ignore
from jwt.exceptions import InvalidSignatureError, ExpiredSignatureError #type: ignore
from .functions.BusinessLayer import make_pdf as pdf
from .functions.DataLayer import get_recipes as getter
from .functions.AdapterLayer import recipes_adapter as r_adapter
from .functions.BusinessLayer import recipes_selecter as r_selecter
from .functions.DataLayer import get_recipe_info as i_getter
from .functions.AdapterLayer import ingredients_adapter as i_adapter
from .functions.AdapterLayer import image_searcher as image
from pydantic import BaseModel #type: ignore
from typing import List, Dict, Union
from auth.functions import jwt_manipulation

# This is the main module of the Meal Planner Process Centric Service
# The file contains the description of all the used functions and adapts them to return their responses as JSONs

# This class constitutes the body of the POST request make-pdf
class RecipeRequest(BaseModel):
    ingredients: Dict[str, List[str]]  # Example: {"Recipe1": ["Item1", "Item2"]}
    image_links: List[str]             # Example: ["http://link1.com", "http://link2.com"]

# Given an ingredient list and image links, create a PDF with the daily meal plan
def make_pdf(request: RecipeRequest):
    """
    Starting from a RecipeRequest (ingredients and images) creates a .pdf file
    """
    response = pdf.plan_to_pdf(request)

    if response["status_code"] == 404:
        return {"status_code": 404}
    
    return response

def get_recipes(filters: str):
    """
    Calls the spoonacular API and asks for 100 recipes with the given filter.
    Returns a JSON containing those recipes
    """
    response = getter.get_recipes_with_filter(filters)
    return response.json()

# This class constitutes the body of the POST request recipes_adapter
class Recipes(BaseModel):
    offset: int
    number: int
    results: list[Dict[str, Union[str, int]]]
    totalResults: int

def recipes_adapter(recipe_list: Recipes):
    """
    An adapter that extracts recipe title and id from the JSON returned by the spoonacular API
    """
    response = r_adapter.extract_text_id(recipe_list)

    if response["status_code"] == 404:
        return {"status_code": 404}
    
    return response
    
class RecipesTitles(BaseModel):
    recipes: list[Dict[str, Union[str, int]]]

def select_recipes(recipes: RecipesTitles):
    """
    Given a list of recipe names and ids, asks g4t to choose some recipes out of the and returns their ids
    """
    response = r_selecter.select_from_recipes(recipes)

    if response["status_code"] == 404:
        return {"status_code": 404}
    
    return response

class SelectedRecipes(BaseModel):
    recipes: list[int]
    status_code: int

def recipes_info(selected_recipes: SelectedRecipes):
    """
    Given a list of recipe ids, asks spoonacular for their additional information
    """
    response = i_getter.get_info_from_id(selected_recipes)

    if response["status_code"] == 404:
        return {"status_code": 404}
    
    return response

class RecipesInfo(BaseModel):
    list: list
    status_code: int

def ingredients_adapter(recipes_info: RecipesInfo):
    """
    Extracts the title and corresponding ingredients of each recipe from the JSON returned by the spoonacular API
    """
    response = i_adapter.extract_ingredients(recipes_info)

    if response["status_code"] == 404:
        return {"status_code": 404}
    
    return response

def search_images(recipe_names: Dict[str, List[str]]):
    """
    Given a JSON containing a list of recipe names, looks for the corresponding images on the internet
    """
    response = image.search(recipe_names)

    return response