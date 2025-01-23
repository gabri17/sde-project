from fastapi import FastAPI, HTTPException, Request #type: ignore
from pydantic import BaseModel #type: ignore
from typing import List, Dict
from .functions import jwt_manipulation, password_encryter, db_adapter
from datetime import datetime
from .functions.functions_to_get_procedure import get_recipe, get_id_from_recipe, get_info_from_id, get_procedure_text_from_info
import requests
#TODO: usare auth0? https://auth0.com/blog/how-to-handle-jwt-in-python

class LoginRequest(BaseModel):
    username: str
    password: str

def all_meal_plans(request: Request):
    auth_header = request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized: token missing")

    token = auth_header.split(" ")[1]
    output = jwt_manipulation.verify_token(token)
    if(output == 1):
       raise HTTPException(status_code=401, detail="Unauthorized: invalid signature")
    elif(output == 2):
        raise HTTPException(status_code=401, detail="Unauthorized: token expired")
    elif(output == 0):
        raise HTTPException(status_code=500, detail="Internal server error")
    else:
        res = db_adapter.get_meal_plans_by_user(output["username"]) #usare un adapter anche per questo
        
        if(res is None):
            return {"data": []}
        else:
            list_parsed = db_adapter.manipulate(res)
            return {"meal_plans_number": len(list_parsed), "data": sorted(list_parsed, key=lambda x: datetime.strptime(x['date_meal_plan'], '%Y-%m-%d %H:%M:%S'), reverse=True)}

def make_login(request: LoginRequest):

    #TODO adapter needed??

    username = request.username
    password = request.password

    if not username or not password:
        raise HTTPException(status_code=400, detail="Provide both username and password fields in body!")

    if(db_adapter.exists_username(username)):
        if(password_encryter.check_password(username, password)):
            token = jwt_manipulation.generate_jwt(username)
            return {"message": "You correctly logged in!", "access_token": token}
        else:
            raise HTTPException(status_code=401, detail="Authentication failed")
    else:
        raise HTTPException(status_code=401, detail="Authentication failed")

def make_register(request: LoginRequest):

    #TODO adapter needed??

    username = request.username
    password = request.password

    if not username or not password:
        raise HTTPException(status_code=400, detail="Provide both username and password fields in body!")

    if(len(password) < 8):
        raise HTTPException(status_code=400, detail="Password must have at least length 8!")
    elif(db_adapter.exists_username(username)):
        raise HTTPException(status_code=400, detail=f"Username '{username}' already existing!")
    else:
        hashed_password = password_encryter.hash_password(password)
        db_adapter.save_user(username, hashed_password)
        return {"message": "User saved!", "Username": username, "Password encrypted saved": db_adapter.get_user(username)["password"]}

class TranslationRequest(BaseModel):
    text: str
    target_lang: str

#https://developers.deepl.com/docs/api-reference/translate/openapi-spec-for-text-translation
def translate(request: TranslationRequest):

    text = request.text
    target_lang = request.target_lang

    if not text or not target_lang:
        raise HTTPException(status_code=400, detail="Provide both text and target_lang fields in body!")

    #EN-GB, FR, IT, DE, ES, PT-PT, NL, ZH (cinese mandarino) -> linguaggi accettati
    allowed_languages = ["IT", "EN-GB", "FR", "DE", "ES", "PT-PT", "NL", "ZH"]
    if target_lang not in allowed_languages:
        raise HTTPException(status_code=400, detail="Provide a target language in this list: " + str(allowed_languages) + "!")

    API_URL = "https://api-free.deepl.com/v2/translate"
    API_KEY = "2dc8af52-e7d2-4150-9610-866a482a29ae:fx"
    params = {
        "auth_key": API_KEY,
        "text": text,
        "target_lang": target_lang
    }
    response = requests.post(API_URL, params=params)
    response = response.json()

    return {"translated_text": response["translations"][0]["text"]}

def get_procedure_from_recipe(recipeName: str):

    result = get_recipe.get_recipe_by_name(recipeName)                                                  #1° servizio esterno
    id_object = get_id_from_recipe.extract_recipe_id(list(result["results"]))                           #adapter

    if(id_object is None):
        raise HTTPException(status_code=404, detail=f"No recipes founded with name '{recipeName}'!")
    else:
        info_object = get_info_from_id.get_info_from_id(id_object["id"])                                #2° servizio esterno
        procedure = get_procedure_text_from_info.get_procedure_text_from_info(info_object)              #adapter
        print(procedure)                                                                                #3° servizio esterno di traduzione
        return {"procedure": procedure}

class ProcedureRequest(BaseModel):
    recipeName: str
    target_lang: str

def get_translated_procedure_from_recipe(request: ProcedureRequest):
    result = get_recipe.get_recipe_by_name(request.recipeName)                                       #1° servizio esterno
    id_object = get_id_from_recipe.extract_recipe_id(list(result["results"]))                           #adapter

    if(id_object is None):
        raise HTTPException(status_code=404, detail=f"No recipes founded with name '{request.recipeName}'!")
    else:
        info_object = get_info_from_id.get_info_from_id(id_object["id"])                                #2° servizio esterno
        procedure = get_procedure_text_from_info.get_procedure_text_from_info(info_object)              #adapter

        text = procedure
        target_lang = request.target_lang

        #EN-GB, FR, IT, DE, ES, PT-PT, NL, ZH (cinese mandarino) -> linguaggi accettati
        allowed_languages = ["IT", "EN-GB", "FR", "DE", "ES", "PT-PT", "NL", "ZH"]
        if target_lang not in allowed_languages:
            raise HTTPException(status_code=400, detail="Provide a target language in this list: " + str(allowed_languages) + "!")

        API_URL = "https://api-free.deepl.com/v2/translate"
        API_KEY = "2dc8af52-e7d2-4150-9610-866a482a29ae:fx"
        params = {
            "auth_key": API_KEY,
            "text": text,
            "target_lang": target_lang
        }
        response = requests.post(API_URL, params=params)                     #3° servizio esterno di traduzione
        response = response.json()

        return {"translated_text": response["translations"][0]["text"]}
