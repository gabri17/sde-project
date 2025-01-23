from fastapi import FastAPI, HTTPException, Request #type: ignore
from pydantic import BaseModel #type: ignore
from typing import List, Dict
from authentication import jwt_manipulation, password_encryter, db_adapter
from datetime import datetime
from procedure_recipe import get_recipe, get_id_from_recipe, get_info_from_id, get_procedure_text_from_info
import requests
#TODO: usare auth0? https://auth0.com/blog/how-to-handle-jwt-in-python

from authentication.interfaces import LoginRequest
from authentication.DataLayer import db_users
from authentication.BusinessLayer import jwt_manipulation, password_encryter

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
    if("status" in result and result["status"] == "failure"):
        raise HTTPException(status_code=402, detail=f"Endpoint limit exceeded!")
    
    id_object = get_id_from_recipe.extract_recipe_id(list(result["results"]))                        #adapter

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
            "text": [text, request.recipeName],
            "target_lang": target_lang
        }
        response = requests.post(API_URL, params=params)                     #3° servizio esterno di traduzione
        response = response.json()

        return {"translated_procedure": response["translations"][0]["text"], "translated_title": response["translations"][1]["text"]}
