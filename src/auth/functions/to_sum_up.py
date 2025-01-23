from functions_to_get_procedure import get_recipe, get_id_from_recipe, get_info_from_id, get_procedure_text_from_info

result = get_recipe.get_recipe_by_name("Butternut Squash Soup (In Half An Hour!)")
id_object = get_id_from_recipe.extract_recipe_id(list(result["results"]))
print(id)
if(id is None):
    print("Sorry, no recipes founded!")
else:
    info_object = get_info_from_id.get_info_from_id(id_object["id"])
    procedure = get_procedure_text_from_info.get_procedure_text_from_info(info_object)
    print(procedure)