from typing import Dict, List
from fastapi import FastAPI, Response, Request, status #type: ignore
from auth import main as auth_main
from meal_planner import main as meal_main
from meal_planner.functions.ProcessCentricLayer.meal_plan import meal_plan
import uvicorn #type: ignore
from fastapi.responses import FileResponse #type: ignore
import os

app = FastAPI()

# What follows is the list of all the endpoints used by our Web Service
# These are only the wrappers for the actual functions. The description of each function is described in the modules of the 2 Process Centric Services

#################################
#   PROCESS CENTRIC SERVICE 1   #
#################################

@app.get("/meal_plans", status_code=200)
def meal_plans(request: Request):
    return auth_main.all_meal_plans(request)

@app.post("/login", status_code=200)
def make_login(request: auth_main.LoginRequest):
    return auth_main.make_login(request)

@app.post("/register", status_code=200)
def make_register(request: auth_main.LoginRequest):
    return auth_main.make_register(request)

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
def make_pdf(request: meal_main.RecipeRequest):
    return meal_main.make_pdf(request)

@app.get("/meal-plan", status_code=200)
def make_meal_plan(filters: str, response: Response, token: str = ""):
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
    return meal_main.get_recipes(filters)

@app.post("/recipes-adapter", status_code=200)
def recipes_adapter(recipe_list: meal_main.Recipes):
    return meal_main.recipes_adapter(recipe_list)

@app.post("/recipes-selecter", status_code=200)
def select_recipes(recipes: meal_main.RecipesTitles):
    return meal_main.select_recipes(recipes)

@app.post("/recipes-info", status_code=200)
def recipes_info(selected_recipes: meal_main.SelectedRecipes):
    return meal_main.recipes_info(selected_recipes)

@app.post("/ingredients-adapter", status_code=200)
def ingredients_adapter(recipes_info: meal_main.RecipesInfo):
    return meal_main.ingredients_adapter(recipes_info)

@app.post("/image-searcher", status_code=200)
def search_images(recipe_names: Dict[str, List[str]]):
    return meal_main.search_images(recipe_names)

##########################
#     USER INTERFACE     #
##########################

@app.get("/", status_code=200)
def serve_index():
    file_path = os.path.join(os.path.dirname(__file__), "frontend/index.html")
    return FileResponse(file_path)

@app.get("/page/meal-planner", status_code=200)
def serve_meal_planner():
    file_path = os.path.join(os.path.dirname(__file__), "frontend/meal-planner.html")
    return FileResponse(file_path)

@app.get("/page/login", status_code=200)
def serve_login():
    file_path = os.path.join(os.path.dirname(__file__), "frontend/login.html")
    return FileResponse(file_path)

@app.get("/page/profile", status_code=200)
def serve_profile():
    file_path = os.path.join(os.path.dirname(__file__), "frontend/profile.html")
    return FileResponse(file_path)

@app.get("/page/register", status_code=200)
def serve_profile():
    file_path = os.path.join(os.path.dirname(__file__), "frontend/register.html")
    return FileResponse(file_path)

##########################
#          MAIN          #
##########################

if __name__ == "__main__":
    #logging configuration for the terminal
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, log_config=log_config)