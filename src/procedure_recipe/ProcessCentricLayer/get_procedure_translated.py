from procedure_recipe.interfaces import ProcedureRequest, ListOfRecipes

from procedure_recipe.AdapterLayer import meal_plans_adapter as m_p_adapt, get_id_from_recipes as g_i_f_rec
from procedure_recipe.DataLayer import db_meal_plans, get_recipe_by_name, get_recipe_info_from_id 
from procedure_recipe.BusinessLayer import elaborate_text as elaboration, translate_text as translation

import requests

API_URL = "http://127.0.0.1:8000"

def get_translated_procedure_from_recipe(request: ProcedureRequest):

    result = requests.get(API_URL + "/get-recipe-by-name?nameRecipe="+request.recipeName).json()    #1° servizio esterno

    if("status" in result and result["status"] == "failure"):
        return {"status_code":402, "detail":"Endpoint limit exceeded!"}
    
    print("STEP 1")

    body: ListOfRecipes = {"recipes": list(result["results"])}

    id_object = requests.post(API_URL + "/id-from-recipes", json=body).json()          #adapter

    print("STEP 2")

    if(id_object is None):
        return {"status_code":404, "detail":f"No recipes founded with name '{request.recipeName}'!"}
    else:

        info_object = requests.get(API_URL + "/info-from-id?id="+str(id_object["id"])).json()                        #2° servizio esterno
        print("STEP 3")
        procedure = requests.post(API_URL + "/get-procedure-text-from-info",json=info_object).json()                 #adapter
        print("STEP 4")
        
        translationBody = {
            "text": [procedure, request.recipeName],
            "target_lang": request.target_lang
        }


        translations_parts = requests.post(API_URL + "/translate-text", json=translationBody).json()           #3° servizio esterno 
        print("STEP 5")
        print(translations_parts)
        if("status_code" in translations_parts and translations_parts["status_code"] == 400):
            return translations_parts

        return {"status_code": 200, "translated_procedure": translations_parts["translated_text"][0], "translated_title": translations_parts["translated_text"][1]}
