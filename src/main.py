from typing import Dict, List
from fastapi import FastAPI, HTTPException, Request #type: ignore
from auth import main as auth_main
from meal_planner import main as meal_main
import uvicorn #type: ignore
from fastapi.responses import FileResponse
import os

app = FastAPI()

@app.get("/protected", status_code=200)
def protected_res(request: Request):
    return auth_main.protected_res(request)

@app.post("/login", status_code=200)
def make_login(request: auth_main.LoginRequest):
    return auth_main.make_login(request)

@app.post("/register", status_code=200)
def make_register(request: auth_main.LoginRequest):
    return auth_main.make_register(request)

@app.post("/make-pdf", status_code=200)
def make_pdf(request: meal_main.RecipeRequest, token: str):
    return meal_main.make_pdf(request, token)

@app.get("/meal-plan", status_code=200)
def make_meal_plan(filters: str, token: str = ""):
    return meal_main.make_meal_plan(filters, token)

@app.get("/get-recipes", status_code=200)
def get_recipes(filters: str):
    return meal_main.get_recipes(filters)

@app.get("/recipes-adapter", status_code=200)
def recipes_adapter(filters: str):
    return meal_main.recipes_adapter(filters)

@app.get("/recipes-selecter", status_code=200)
def select_recipes(filters: str):
    return meal_main.select_recipes(filters)

@app.get("/recipes-info", status_code=200)
def recipes_info(filters: str):
    return meal_main.recipes_info(filters)

@app.get("/ingredients-adapter", status_code=200)
def ingredients_adapter(filters: str):
    return meal_main.ingredients_adapter(filters)

@app.post("/image-searcher", status_code=200)
def search_images(recipe_names: Dict[str, List[str]]):
    return meal_main.search_images(recipe_names)

##########################
######USER INTERFACE######
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
##########################
##########################

if __name__ == "__main__":
    #logging configuration for the terminal
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, log_config=log_config)