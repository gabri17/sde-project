from pydantic import BaseModel 
from typing import Any, List

class ListOfRecipes(BaseModel):
    recipes: List[Any]            

class RecipeInfo(BaseModel):
    title: str
    readyInMinutes: int
    procedure: str

class TranslationRequest(BaseModel):
    text: List[str]
    target_lang: str

class ProcedureRequest(BaseModel):
    recipeName: str
    target_lang: str
