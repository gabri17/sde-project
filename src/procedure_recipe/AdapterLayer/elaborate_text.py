from procedure_recipe.interfaces import RecipeInfo

def get_procedure_text_from_info(recipe_info: RecipeInfo):

    if(recipe_info is None):
        return ""

    text = recipe_info.procedure + "\n\n" + "It will be ready in " + str(recipe_info.readyInMinutes) + " minutes."
    return text