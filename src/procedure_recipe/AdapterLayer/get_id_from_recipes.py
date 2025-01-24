from procedure_recipe.interfaces import ListOfRecipes

# Extracts only the id of a recipe, passing in input the array given back by get_recipe
def extract_recipe_id(list: ListOfRecipes):
    
    if(len(list.recipes) == 0):
        return None
    else:
        return {"id": list.recipes[0]["id"], "status_code": 200}  