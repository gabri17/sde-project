import deepl

API_KEY = "2dc8af52-e7d2-4150-9610-866a482a29ae:fx"
translator = deepl.Translator(API_KEY)

#EN-GB, FR, IT, DE, ES, PT-PT

#https://developers.deepl.com/docs/api-reference/translate/openapi-spec-for-text-translation
result = translator.translate_text("Ciao a tutti sono gabriele e vengo da monaco di baviera! Saluto la mia famiglia!", target_lang="PT-PT")
print(result.text) 

import requests

API_URL = "https://api-free.deepl.com/v2/translate"

text = """
Dear all, these are the delivery instructions for the final project for registered (in Esse3) 
students for the examination session of January 27th.

Open the link below
https://drive.google.com/drive/folders/1wKod3Ttd_F6nzmV6jR0kbA2d4iGCvh3s?usp=sharing

and create in the shared google folder a folder named with the  list of surnames of the team.
We only need one person per group to submit the project
Please deliver here your final project at least TWO DAYS before the exam session you have registered in.

You can continue to work on your code until the exam session

We kindly ask you to deliver in the created google folder for each team:
 • the PDF report, which should contain a simple diagram of your project's architecture, a brief description of the project, and a listing all group members. The total length of the report shouldn't exceed  3 pages.
 • In a free text file, a link to the code's repository, and any instructions to access the "demo instance", if you made one.

Remember to clearly list all the participants in your group also in the PDF Report!
The day before the exam we will share a draft schedule for the projects presentations on January 27th
Good work!
Maurizio and Gino

P.S. you will find the same instructions also in the Moodle of the courses
"""
text = "ciao a tutti viva l'olanda!"
print(text)

params = {
    "auth_key": API_KEY,
    "text": text,
    "target_lang": "zh",  
}
response = requests.post(API_URL, params=params)
response = response.json()

print(response["translations"][0]["text"])