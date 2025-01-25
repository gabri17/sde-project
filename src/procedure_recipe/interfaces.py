from pydantic import BaseModel 
from typing import Any, List

class ListOfRecipes(BaseModel):
    """
    Input of /id-from-recipes service
    """
    recipes: List[Any]            

class RecipeInfo(BaseModel):
    """
    Input of /get-procedure-text-from-info service
    """
    title: str
    readyInMinutes: int
    procedure: str

class TranslationRequest(BaseModel):
    """
    Input of /translate-text service
    """
    text: List[str]
    target_lang: str

class ProcedureRequest(BaseModel):
    """
    Input of /procedure_translated service
    """
    recipeName: str
    target_lang: str

class ObjectFromDb(BaseModel):  #a list of object retrieved from collections "MealPlans"
    """
    Input of /adapt-meal-plans service
    """
    plans_response: List[Any]