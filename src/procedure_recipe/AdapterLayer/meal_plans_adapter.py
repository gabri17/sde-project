from authentication.BusinessLayer import jwt_manipulation
from fastapi import Request #type: ignore
import requests

#from procedure_recipe.AdapterLayer import meal_plans_adapter
from procedure_recipe.DataLayer import db_meal_plans
from datetime import datetime

API_URL = "http://127.0.0.1:8000"

#take an HTTP request and gives back the list of meal plans for a user
def meal_plans_adapter(request: Request):
    auth_header = request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        return {"status_code":401, "detail":"Unauthorized: token missing"}

    token = auth_header.split(" ")[1]
    output = jwt_manipulation.verify_token(token)
    if(output == 0):
        return {"status_code":401, "detail":"Unauthorized: token not verified or internal server error"}
    else:
        res = requests.get(API_URL + "/get-meal-plans-db?username="+output["username"]).json()
        
        list_parsed = res["plans_response"]
        return {"meal_plans_number": len(list_parsed), "data": sorted(list_parsed, key=lambda x: datetime.strptime(x['date_meal_plan'], '%Y-%m-%d %H:%M:%S'), reverse=True)}
