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

from procedure_recipe.AdapterLayer import meal_plans_adapter as m_p_adapt, get_id_from_recipes as g_i_f_rec
from procedure_recipe.DataLayer import db_meal_plans, get_recipe_by_name, get_recipe_info_from_id 
from procedure_recipe.BusinessLayer import elaborate_text as elaboration, translate_text as translation
from procedure_recipe.ProcessCentricLayer import get_procedure_translated as g_p_t

from procedure_recipe.interfaces import ListOfRecipes, RecipeInfo, TranslationRequest, ProcedureRequest

app = FastAPI(
    title="Documentation",
    description="This is the API documentation for all the services implemented in our project.<br>" + 
    "The various services are grouped in a label representing the specific process they are used in.<br><br>"+
    "They are listed following the order in which they are compose in each process centric service, to make workflow understanding easier.",
    version="1.0.0" 
)

# What follows is the list of all the endpoints used by our Web Service
# These are only the wrappers for the actual functions. The description of each function is described in the modules of the 2 Process Centric Services


#################################
#             AUTH              #
#################################

@app.post("/register", status_code=200, tags=["Auth"])
def make_register(request: auth_interfaces.LoginRequest):
    """
        Simple API for performing registration providing username and password.

        Returns:\n
        {"status_code": 200, "message": "User saved!", "Username": {username}, "Password encrypted saved": {hashed_password}}
        \nor\n
        {"status_code": 400, "detail": "Username '{username}' already existing!"}
        \nor\n
        {"status_code": 400, "detail": "Password must have at least length 8!"}
    """
    return m_register.make_register(request)

@app.post("/login", status_code=200, tags=["Auth"])
def make_login(request: auth_interfaces.LoginRequest):
    """
        Simple API for performing login with username and password.

        Returns:\n
        {"status_code": 200, "message": "You correctly logged in!", "access_token": {token}}
        \nor\n
        {"status_code": 401, "detail": "Authentication failed"}
    """
    return m_login.make_login(request)

#################################
#   PROCESS CENTRIC SERVICE 1   #
#################################

@app.get("/get-meal-plans-db", status_code=200, tags=["Procedure retrieval"])
def get_meal_plans_db(username: str):
    """It gives back a list of all meal planners created for a given user

    Args:\n
        username: str # The username of the user we want to get meal plans

    Returns:\n
        {"plans_response": list}   #list of meal plans objects generated
    """
    return db_meal_plans.get_meal_plans_by_user(username)

@app.get("/adapt-meal-plans", status_code=200, tags=["Procedure retrieval"])
def adapt_meal_plans(request: Request):
    """It is used to retrieve 

    Header:\n
        Authorization: 'Bearer {token}' # Requested the access_token to retrieve this information

    Returns:\n
        {
        "meal_plans_number": int, #number of meal planners
        "data": [{
            date_meal_plan: str,
            recipes_number: int,
            recipes_titles: list[str]
        }]}   #list of meal plans objects with information of the date, number of recipes and all recipes generated
    """
    return m_p_adapt.meal_plans_adapter(request)

@app.get("/get-recipe-by-name", status_code=200, tags=["Procedure retrieval"])
def get_recipe(nameRecipe: str):
    """
    GET request to spoonacular (https://spoonacular.com/food-api/docs) to get some info of the recipe with the NAME passed.
    
    Args:\n
        nameRecipe: the name of the recipe we want to find

    Returns:\n
        an object with the results got.\n
        In the 'results' field a list with all the recipes associated with that name (if it's the exact name just one recipe)
    """
    return get_recipe_by_name.get_recipe_by_name(nameRecipe)

@app.post("/id-from-recipes", status_code=200, tags=["Procedure retrieval"])
def get_id_from_recipes(listOfRecipes: ListOfRecipes):
    """
    Given a list of recipes returns the id of the first recipe.

    Returns:\n
        {"id": {id of first recipe}, "status_code": 200}
        \nor\n
        None
    """
    return g_i_f_rec.extract_recipe_id(listOfRecipes)

@app.get("/info-from-id", status_code=200, tags=["Procedure retrieval"])
def get_recipe_information(id):
    """
    GET request to spoonacular (https://spoonacular.com/food-api/docs) to get huge details of the recipe with the ID passed.\n
    Then we return only the relevant to us
    
    Args:\n
        id: id of the recipe we want to get details of

    Returns:\n
        {
        'title': str,
        'readyInMinutes': int,
        'procedure': str,
        }
    """
    return get_recipe_info_from_id.get_info_from_id(id)

@app.post("/get-procedure-text-from-info", status_code=200, tags=["Procedure retrieval"])
def elaborate_text(recipe_info: RecipeInfo):
    """
    Elaborate the object returned by /info-from-id and get a receipt string

    Returns:\n
        string with the procedure to follow for the specific receipt
    """
    return elaboration.get_procedure_text_from_info(recipe_info)

@app.post("/translate-text", status_code=200, tags=["Procedure retrieval"])
def get_translation_text(translationBody: TranslationRequest):
    """
    Given an array of string and a target language, it translates the strings in the target language.
    
    Returns:\n
        {"translated_text": List[str]} 
    """
    return translation.translate(translationBody)


@app.post("/procedure_translated", status_code=200, tags=["Procedure retrieval"])
def get_procedure_translated(request: ProcedureRequest):
    """
    It implements the whole composition: from a recipe name, we get the translated procedure!

    Returns:\n
        {"status_code": 200, "translated_procedure": {procedure translated in the desired language}, "translated_title": {title translated in the desired language}}

        \nor\n
        {"status_code": 400,"detail": "Provide a target language in this list: ['IT', 'EN-GB', 'FR', 'DE', 'ES', 'PT-PT', 'NL', 'ZH']!"}
        \nor\n
        {"status_code":404, "detail":"No recipes founded with name '{request.recipeName}'!"}
    """
    return g_p_t.get_translated_procedure_from_recipe(request)

#################################
#   PROCESS CENTRIC SERVICE 2   #
#################################

@app.get("/meal-plan", status_code=200, tags=["Meal plan creation"])
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

@app.get("/get-recipes", status_code=200, tags=["Meal plan creation"])
def get_recipes(filters: str):
    """Asks the spoonacular API for recipes that satisfy a series of filters

    Args:\n
        filters: str # Example: "vegan, gluten-free"

    Returns:\n
        The JSON returned by the spoonacular API
    """
    return r_getter.get_recipes_with_filter(filters)

@app.post("/recipes-adapter", status_code=200, tags=["Meal plan creation"])
def recipes_adapter(recipe_list: mp_interfaces.Recipes, response: Response):
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
            "status_code": int
        }
    """
    result = r_adapter.extract_text_id(recipe_list)
    if result["status_code"] == 404:
        response.status_code = status.HTTP_404_NOT_FOUND
    return result

@app.post("/recipes-selecter", status_code=200, tags=["Meal plan creation"])
def select_recipes(recipes: mp_interfaces.RecipesTitles):
    """Given a series of recipe names and ids, selects 2 of them

    Args:\n
        The JSON returned by the /recipes-adapter endpoint, which is seen as:

        class RecipesTitles(BaseModel):
            recipes: list[Dict[str, Union[str, int]]]

    Returns:\n
        {
            "recipes": [id1, id2, ...],
            "status_code": int
        }
    """
    return r_selecter.select_from_recipes(recipes)

@app.post("/recipes-info", status_code=200, tags=["Meal plan creation"])
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

@app.post("/ingredients-adapter", status_code=200, tags=["Meal plan creation"])
def ingredients_adapter(recipes_info: mp_interfaces.RecipesInfo, response: Response):
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

@app.post("/image-searcher", status_code=200, tags=["Meal plan creation"])
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

@app.post("/make-pdf", status_code=200, tags=["Meal plan creation"])
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

@app.post("/upload_recipe", status_code=200, tags=["Meal plan creation"])
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

@app.get("/", status_code=200, include_in_schema=False)
def serve_index():
    file_path = os.path.join(os.path.dirname(__file__), "../frontend/index.html")
    return FileResponse(file_path)

@app.get("/page/meal-planner", status_code=200, include_in_schema=False)
def serve_meal_planner():
    file_path = os.path.join(os.path.dirname(__file__), "../frontend/meal-planner.html")
    return FileResponse(file_path)

@app.get("/page/register", status_code=200, include_in_schema=False)
def serve_profile():
    file_path = os.path.join(os.path.dirname(__file__), "../frontend/register.html")
    return FileResponse(file_path)

@app.get("/page/login", status_code=200, include_in_schema=False)
def serve_login():
    file_path = os.path.join(os.path.dirname(__file__), "../frontend/login.html")
    return FileResponse(file_path)

@app.get("/page/profile", status_code=200, include_in_schema=False)
def serve_profile():
    file_path = os.path.join(os.path.dirname(__file__), "../frontend/profile.html")
    return FileResponse(file_path)

##########################
#          MAIN          #
##########################

if __name__ == "__main__":
    #logging configuration for the terminal
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True, log_config=log_config)