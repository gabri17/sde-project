from procedure_recipe.interfaces import TranslationRequest
import requests

API_URL = "https://api-free.deepl.com/v2/translate"
API_KEY = "2dc8af52-e7d2-4150-9610-866a482a29ae:fx"

def translate(request: TranslationRequest):

    text = request.text
    target_lang = request.target_lang

    if not text or not target_lang:
        return {"status_code": 400, "detail":"Provide both text and target_lang fields in body!"}

    #EN-GB, FR, IT, DE, ES, PT-PT, NL, ZH (cinese mandarino) -> linguaggi accettati
    allowed_languages = ["IT", "EN-GB", "FR", "DE", "ES", "PT-PT", "NL", "ZH"]
    if target_lang not in allowed_languages:
        return {"status_code":400, "detail":"Provide a target language in this list: " + str(allowed_languages) + "!"}

    params = {
        "auth_key": API_KEY,
        "text": text,
        "target_lang": target_lang
    }
    response = requests.post(API_URL, params=params)
    response = response.json()

    list_translations = []
    for element in response["translations"]:
        list_translations.append(element["text"])

    return {"translated_text": list_translations}