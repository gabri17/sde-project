from procedure_recipe.DataLayer import db_meal_plans
from procedure_recipe.AdapterLayer import meal_plans_adapter
import requests

API_URL = "http://127.0.0.1:8000"

#This is managing the request of the user to recover old meal plans
def user_old_meal_plans(access_token: str):
    res1 = requests.get(API_URL + "/get-meal-plans-db?access_token=" + access_token).json()

    print("STEP 1")

    if("status_code" in res1 and res1["status_code"] == 401):
        return {"status_code":401, "detail":"Unauthorized: token not verified or missing or internal server error"}
    
    res2 = requests.post(API_URL + "/adapt-meal-plans", json=res1).json()
    print("STEP 2")
    
    return res2
