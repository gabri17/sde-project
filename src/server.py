from typing import Dict, List
from fastapi import FastAPI, Response, Request, status #type: ignore
from procedure_recipe import main as auth_main
import uvicorn #type: ignore
from fastapi.responses import FileResponse #type: ignore
import os

from meal_planner import interfaces as mp_interfaces

from meal_planner.AdapterLayer import image_searcher, ingredients_adapter as i_a, recipes_adapter as r_adapter
from meal_planner.DataLayer import get_recipe_info as i_getter, get_recipes as r_getter
from meal_planner.BusinessLayer import recipes_selecter as r_selecter, make_pdf as pdf_maker
from meal_planner.ProcessCentricLayer.meal_plan import meal_plan
from meal_planner.DataLayer.db_upload import insert_plan_db

from authentication.BusinessLayer import make_login as m_login, make_register as m_register
from authentication import interfaces as auth_interfaces

app = FastAPI()

# What follows is the list of all the endpoints used by our Web Service
# These are only the wrappers for the actual functions. The description of each function is described in the modules of the 2 Process Centric Services


#################################
#             AUTH              #
#################################

@app.post("/login", status_code=200)
def make_login(request: auth_interfaces.LoginRequest):
    return m_login.make_login(request)

@app.post("/register", status_code=200)
def make_register(request: auth_interfaces.LoginRequest):
    return m_register.make_register(request)

#################################
#   PROCESS CENTRIC SERVICE 1   #
#################################

@app.get("/meal_plans", status_code=200)
def meal_plans(request: Request):
    return auth_main.all_meal_plans(request)

@app.get("/procedure", status_code=200)
def get_procedure(recipe: str):
    return auth_main.get_procedure_from_recipe(recipe)

@app.post("/translate", status_code=200)
def get_translation(request: auth_main.TranslationRequest):
    return auth_main.translate(request)

@app.post("/procedure_translated", status_code=200)
def get_procedure_translated(request: auth_main.ProcedureRequest):
    return auth_main.get_translated_procedure_from_recipe(request)

#################################
#   PROCESS CENTRIC SERVICE 2   #
#################################

@app.post("/make-pdf", status_code=200)
def make_pdf(request: mp_interfaces.RecipeRequest):
    """Creates a PDF file starting from a RecipeRequest

    Args:\n
        class RecipeRequest(BaseModel):
            ingredients: Dict[str, List[str]]  # Example: {"Recipe1": ["Item1", "Item2"]}
            image_links: List[str]             # Example: ["http://link1.com", "http://link2.com"]

    Returns:\n
        {"status_code": val}   # val = 200 if successfully created, otherwise 404
    """
    return pdf_maker.plan_to_pdf(request)

@app.get("/meal-plan", status_code=200)
def make_meal_plan(filters: str, response: Response, token: str = ""):
    """Creates and returns a .pdf file containing a meal plan sttarting from a series of filters

    Args:\n
        filters: str # Example: "vegan, gluten-free"
        token: str   # The authentication token of the logged in user

    Returns:\n
        FileResponse containing the .pdf file
    """
    result = meal_plan(filters, token)
    if result["status_code"] == 201:
        response.status_code = status.HTTP_201_CREATED
        return FileResponse(
            path="./DailyMealPlan.pdf",
            media_type="application/pdf",
            filename="DailyMealPlan.pdf",
            headers={"Content-Disposition": "attachment; filename=DailyMealPlan.pdf"}
        )
    else:
        response.status_code = status.HTTP_404_NOT_FOUND

@app.get("/get-recipes", status_code=200)
def get_recipes(filters: str):
    """Asks the spoonacular API for recipes that satisfy a series of filters

    Args:\n
        filters: str # Example: "vegan, gluten-free"

    Returns:\n
        The JSON returned by the spoonacular API
    """
    return r_getter.get_recipes_with_filter(filters)

@app.post("/recipes-adapter", status_code=200)
def recipes_adapter(recipe_list: mp_interfaces.Recipes):
    """An adapter to extract recipe title and id

    Args:\n
        The JSON returned by the spoonacular API, which is seen as:

        class Recipes(BaseModel):
            offset: int
            number: int
            results: list[Dict[str, Union[str, int]]]
            totalResults: int

    Returns:\n
        {
            "recipes": [{
                "name": recipe_name,
                "id": recipe_id,
            },
            ...],
            "status_code": val
        }
    """
    return r_adapter.extract_text_id(recipe_list)

@app.post("/recipes-selecter", status_code=200)
def select_recipes(recipes: mp_interfaces.RecipesTitles):
    """Given a series of recipe names and ids, selects 2 of them

    Args:\n
        The JSON returned by the /recipes-adapter endpoint, which is seen as:

        class RecipesTitles(BaseModel):
            recipes: list[Dict[str, Union[str, int]]]

    Returns:\n
        {
            "recipes": [id1, id2, ...],
            "status_code": val
        }
    """
    return r_selecter.select_from_recipes(recipes)

@app.post("/recipes-info", status_code=200)
def recipes_info(selected_recipes: mp_interfaces.SelectedRecipes):
    """Asks the spoonacular API for additional info about some recipes

    Args:\n
        The JSON returned by the /recipes-selecter endpoint, which is seen as:

        class SelectedRecipes(BaseModel):
            recipes: list[int]
            status_code: int

    Returns:\n
        The JSON returned by the spoonacular API
    """
    return i_getter.get_info_from_id(selected_recipes)

@app.post("/ingredients-adapter", status_code=200)
def ingredients_adapter(recipes_info: mp_interfaces.RecipesInfo):
    """Extract the ingredients of a recipe from the additional info JSON returned by the spoonacular API

    Args:\n
        The JSON returned by the spoonacular API, which is seen as:

        class RecipesInfo(BaseModel):
            list: list
            status_code: int

    Returns:\n
        {
            "list": [
                {"recipe_name": [ingredient1, ingredient2, ...]}.
                {"recipe2": ...},
                ...
            ],
            "status_code": int
        }
    """
    return i_a.extract_ingredients(recipes_info)

@app.post("/image-searcher", status_code=200)
def search_images(recipe_names: Dict[str, List[str]]):
    """Looks for images given some recipes

    Args:\n
        The JSON returned by the /ingredients-adapter endpoint, which is seen as:

        recipe_names: Dict[str, List[str]]

    Returns:\n
        {
            "links": [link1, link2, ...], 
            "status_code": int
        }
    """
    return image_searcher.search(recipe_names)

@app.post("/upload_recipe", status_code=200)
def upload_recipe(recipe: mp_interfaces.RecipeRequest, token: str):
    """Uploads the meal plan of an authenticated user to the DB

    Args:\n
        class RecipeRequest(BaseModel):
            ingredients: Dict[str, List[str]]  # Example: {"Recipe1": ["Item1", "Item2"]}
            image_links: List[str]             # Example: ["http://link1.com", "http://link2.com"]

    Returns:\n
        {"status_code": int}    # 200 if ok, otherwise 404
    """
    return insert_plan_db(token, recipe)

##########################
#     USER INTERFACE     #
##########################

@app.get("/", status_code=200)
def serve_index():
    file_path = os.path.join(os.path.dirname(__file__), "../frontend/index.html")
    return FileResponse(file_path)

@app.get("/page/meal-planner", status_code=200)
def serve_meal_planner():
    file_path = os.path.join(os.path.dirname(__file__), "../frontend/meal-planner.html")
    return FileResponse(file_path)

@app.get("/page/login", status_code=200)
def serve_login():
    file_path = os.path.join(os.path.dirname(__file__), "../frontend/login.html")
    return FileResponse(file_path)

@app.get("/page/profile", status_code=200)
def serve_profile():
    file_path = os.path.join(os.path.dirname(__file__), "../frontend/profile.html")
    return FileResponse(file_path)

@app.get("/page/register", status_code=200)
def serve_profile():
    file_path = os.path.join(os.path.dirname(__file__), "../frontend/register.html")
    return FileResponse(file_path)

##########################
#          MAIN          #
##########################

if __name__ == "__main__":
    #logging configuration for the terminal
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True, log_config=log_config)