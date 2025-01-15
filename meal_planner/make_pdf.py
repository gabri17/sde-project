import ingredients_adapter
import image_searcher

def plan_to_pdf(filters: str):
    ingredients = ingredients_adapter.extract_ingredients(filters)

    # Make a list only containing the names
    recipe_names = []
    for item in ingredients.keys():
        recipe_names.append(item)

    image_links = image_searcher.search(recipe_names)

    #//TODO -------------------------------------------------------------------
    # At the moment I'm making the PDF here, but this should be an internal API. I'll make this change in another moment

    from reportlab.pdfgen import canvas # type: ignore
    from datetime import datetime
    from reportlab.lib.pagesizes import letter # type: ignore
    from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer, PageBreak # type: ignore
    from reportlab.lib.styles import getSampleStyleSheet # type: ignore
    import requests #type: ignore
    import os

    # Get current date and time
    now = datetime.now()

    # Format it as: dd-mm-YY_H-M-S
    dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")

    doc = SimpleDocTemplate("meal_plan_"+dt_string+".pdf",pagesize=letter,
                        rightMargin=72,leftMargin=72,
                        topMargin=72,bottomMargin=18)
    
    # Get styles for paragraphs
    styles = getSampleStyleSheet()

    # Maximum width and height for the images. Needed to avoid overflow
    MAX_IMAGE_WIDTH = 400 
    MAX_IMAGE_HEIGHT = 300

    # Iterate through all recipes
    file_content = []
    iterator = 0
    for item in ingredients.keys():
        # Add the recipe name as a title
        file_content.append(Paragraph(item, styles['Title']))

        # Add the recipe image. We need to download it
        img_data = requests.get(image_links[iterator]).content
        with open(item + '.jpg', 'wb') as handler:
            handler.write(img_data)
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

        # Add all the ingredients as a list
        file_content.append(Paragraph("Ingredients:", styles['Heading2']))
        for ingredient in ingredients[item]:
            file_content.append(Paragraph(ingredient, styles['BodyText']))

        # Add space between recipes
        file_content.append(Spacer(1, 24))

        # Add a page break after each recipe
        file_content.append(PageBreak())

        iterator += 1

    # Build the pdf
    doc.build(file_content)

    # Delete all images that have been downloaded
    dir_content = os.listdir("./")
    for item in dir_content:
        if item.endswith(".jpg"):
            os.remove(os.path.join("./", item))

    #//TODO -------------------------------------------------------------------

plan_to_pdf("a")