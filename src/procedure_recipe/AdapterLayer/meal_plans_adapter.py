from datetime import datetime
from procedure_recipe.interfaces import ObjectFromDb

def meal_plans_adapter(objectToManipulate: ObjectFromDb):        
    list_to_parse = objectToManipulate.plans_response
    list_parsed = []
    for mp in list_to_parse:
        obj = {
            "date_meal_plan": mp["date"],
            "recipes_number":  len(mp["ingredients"]),
            "recipes_titles": list(mp["ingredients"])
        }
        list_parsed.append(obj)
    return {"status_code": 200, "meal_plans_number": len(list_parsed), "data": sorted(list_parsed, key=lambda x: datetime.strptime(x['date_meal_plan'], '%Y-%m-%d %H:%M:%S'), reverse=True)}
