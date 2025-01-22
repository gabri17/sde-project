from fastapi import FastAPI, Response, status #type: ignore
from fastapi.responses import FileResponse
import jwt #type: ignore
from jwt.exceptions import InvalidSignatureError, ExpiredSignatureError
from .functions import make_pdf as pdf
from .functions import get_recipes as getter
from .functions import recipes_adapter as r_adapter
from .functions import recipes_selecter as r_selecter
from .functions import get_recipe_info as i_getter
from .functions import ingredients_adapter as i_adapter
from .functions import image_searcher as image
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer, PageBreak, Table, TableStyle #type: ignore
from reportlab.lib.pagesizes import letter #type: ignore
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle #type: ignore
from reportlab.lib import colors #type: ignore
from reportlab.pdfbase.ttfonts import TTFont #type: ignore
from reportlab.pdfbase import pdfmetrics #type: ignore
from reportlab.lib.units import mm #type: ignore
import requests #type: ignore
import os
from pydantic import BaseModel #type: ignore
from typing import List, Dict

from auth.functions import jwt_manipulation

# This class constitutes the body of the POST request make-pdf
class RecipeRequest(BaseModel):
    ingredients: Dict[str, List[str]]  # Example: {"Recipe1": ["Item1", "Item2"]}
    image_links: List[str]             # Example: ["http://link1.com", "http://link2.com"]

# Given an ingredient list and image links, create a PDF with the daily meal plan
def make_pdf(request: RecipeRequest, token: str = "", upload: bool = True):
    """
    Starting from a RecipeRequest (ingredients and images) creates a .pdf file.
    If upload = true and the user is authenticated, the meal_plan is also uploaded online
    """
    
    if upload == True:
        # If user is authenticated, add meal_plan to his history
        # Check if authenticated
        if token != "":
            # A token has been inserted, validate it
            result = jwt_manipulation.verify_token(token)

            if result != 1 and result != 2 and result != 0:
                # Token is valid, extract username
                username = result["username"]

                # Insert the meal plan in the DB for that user
                from .functions.db_adapter import insert_plan_db
                result = insert_plan_db(username, request)
                
                if (result["status_code"] == 404):
                    return {"status_code": 404}

    ingredients = request.ingredients
    image_links = request.image_links

    # Styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="CustomTitle", fontSize=18, fontName="Helvetica-Bold", spaceAfter=12))
    styles.add(ParagraphStyle(name="CustomHeading", fontSize=14, fontName="Helvetica-Bold", textColor=colors.darkblue))
    styles.add(ParagraphStyle(name="CustomBody", fontSize=12, fontName="Helvetica", leading=14))

    # File Content. It will be filled with the data to put inside the PDF and then made a PDF
    file_content = []

    # Maximum dimensions for images
    MAX_IMAGE_WIDTH = 200
    MAX_IMAGE_HEIGHT = 200

    iterator = 0
    for item in ingredients.keys():
        # Recipe Title
        file_content.append(Paragraph(item, styles["CustomHeading"]))
        file_content.append(Spacer(1, 12))

        # Add the recipe image. We need to download it
        img_data = requests.get(image_links[iterator]).content
        with open(item + '.jpg', 'wb') as handler:
            handler.write(img_data)
        
        # Create the Image flowable
        im = Image(item + '.jpg')
        
        # Scale the image proportionally if it exceeds the max dimensions
        if im.drawWidth > MAX_IMAGE_WIDTH or im.drawHeight > MAX_IMAGE_HEIGHT:
            aspect_ratio = im.drawWidth / im.drawHeight
            if im.drawWidth > MAX_IMAGE_WIDTH:
                im.drawWidth = MAX_IMAGE_WIDTH
                im.drawHeight = MAX_IMAGE_WIDTH / aspect_ratio
            if im.drawHeight > MAX_IMAGE_HEIGHT:
                im.drawHeight = MAX_IMAGE_HEIGHT
                im.drawWidth = MAX_IMAGE_HEIGHT * aspect_ratio

        # Add the image to the content
        file_content.append(im)

        # Add space after the image
        file_content.append(Spacer(1, 12))

        # Ingredients Table
        data = [["Ingredients:"]]
        for ingredient in ingredients[item]:
            data.append([ingredient])
        table = Table(data, colWidths=[400])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
            ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ]))
        file_content.append(table)

        # Add a PageBreak after each recipe
        file_content.append(PageBreak())
        iterator += 1

    # Add page numbers
    def add_page_numbers(canvas, doc):
        page_num = canvas.getPageNumber()
        text = f"Page {page_num}"
        canvas.drawRightString(200 * mm, 10 * mm, text)

    # Build PDF
    doc = SimpleDocTemplate(
        "DailyMealPlan.pdf",
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
    )
    doc.build(file_content, onLaterPages=add_page_numbers)

    # Delete all images that have been downloaded
    dir_content = os.listdir("./")
    for item in dir_content:
        if item.endswith(".jpg"):
            os.remove(os.path.join("./", item))

    if os.path.isfile("./DailyMealPlan.pdf"):
        return {"status_code": 200}
    else:
        return {"status_code": 404}

def make_meal_plan(filters: str, token: str):
    """
    Given a set of filters and a token (if authenticated), if succesfull returns a .pdf file containing a meal plan
    """
    response = pdf.plan_to_pdf(filters, token)

    if response["status_code"] == 200:
        return FileResponse(
            path="./DailyMealPlan.pdf",
            media_type="application/pdf",
            filename="DailyMealPlan.pdf",
            headers={"Content-Disposition": "attachment; filename=DailyMealPlan.pdf"}
        )
    else:
        return {"status_code": 400}

def get_recipes(filters: str):
    """
    Calls the spoonacular API and asks for 100 recipes with the given filter.
    Returns a JSON containing those recipes
    """
    response = getter.get_recipes_with_filter(filters)
    return response.json()

def recipes_adapter(filters: str):
    """
    An adapter that extracts recipe title and id from the JSON returned by the spoonacular API
    """
    response = r_adapter.extract_text_id(filters)

    if response["status_code"] == 404:
        return {"status_code": 404}
    
    return response

def select_recipes(filters: str):
    """
    Given a list of recipe names and ids, asks g4t to choose some recipes out of the and returns their ids
    """
    response = r_selecter.select_from_recipes(filters)

    if response["status_code"] == 404:
        return {"status_code": 404}
    
    return response

def recipes_info(filters: str):
    """
    Given a list of recipe ids, asks spoonacular for their additional information
    """
    response = i_getter.get_info_from_id(filters)

    if response["status_code"] == 404:
        return {"status_code": 404}
    
    return response

def ingredients_adapter(filters: str):
    """
    Extracts the title and corresponding ingredients of each recipe from the JSON returned by the spoonacular API
    """
    response = i_adapter.extract_ingredients(filters)

    if response["status_code"] == 404:
        return {"status_code": 404}
    
    return response

def search_images(recipe_names: Dict[str, List[str]]):
    """
    Given a JSON containing a list of recipe names, looks for the corresponding images on the internet
    """
    response = image.search(recipe_names)

    return response