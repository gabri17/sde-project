# SDE Project: Meal Planner

This Meal Planner web service is capable of creating daily meal plans given any dietary constraints. In particular, it can:
- Create a daily meal plan made up of 2 recipes
- If the user is authenticated, the created meal plan is saved
- An authenticated user can access its older meal plans and ask for the procedure to prepare one of those recipes

## Prerequisites

- [Python](https://www.python.org/downloads/)

## Use

1. Create virtual environment:
`python -m venv venv`

2. Launch virtual environment
   - Linux:
    `source venv/bin/activate`
   - Windows Command Prompt:
    `venv\Scripts\activate.bat`

3. Install all dependencies:
    `pip install -r requirements.txt`

4. Run the main script:
   - Linux:
    `python3 src/server.py`
   - Windows Command Prompt:
    `python src\server.py`

5. Go at http://127.0.0.1:8000/

APIs documentation available at: http://127.0.0.1:8000/docs

## Developer Notes

In order to generate/update the *requirements.txt* file when new dependencies are added use:

    pip freeze > requirements.txt
