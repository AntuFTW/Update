import csv
import datetime
import pytz
import requests
import subprocess
import urllib
import uuid
import validators

from flask import redirect, render_template, session
from functools import wraps

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def get_nutrition(query):
    number_data = 11
    name, calories, fat_total_g, fat_saturated_g, protein_g, sodium_mg, cholesterol_mg, carbohydrates_total_g, fiber_g, sugar_g, serving_size_g = ([] for i in range(number_data))
    indexkey = ["name", "calories", "fat_total_g", "fat_saturated_g", "protein_g", "sodium_mg", "cholesterol_mg", "carbohydrates_total_g", "fiber_g", "sugar_g", "serving_size_g"]
    indexvalue = [name, calories, fat_total_g, fat_saturated_g, protein_g, sodium_mg, cholesterol_mg, carbohydrates_total_g, fiber_g, sugar_g, serving_size_g]

    api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
    response = requests.get(api_url + query, headers={'X-Api-Key': '6eH93am9zyDrQoTKLusadQ==Q872ZzJBtIrhaFjs'})
    reply = {}
    if response.status_code == requests.codes.ok:
        foods = (response.json())["items"]
        for food in foods:
            name.append(food["name"])
            calories.append(food["calories"])
            fat_total_g.append(food["fat_total_g"])
            fat_saturated_g.append(food["fat_saturated_g"])
            protein_g.append(food["protein_g"])
            sodium_mg.append(food["sodium_mg"])
            cholesterol_mg.append(food["cholesterol_mg"])
            carbohydrates_total_g.append(food["carbohydrates_total_g"])
            fiber_g.append(food["fiber_g"])
            sugar_g.append(food["sugar_g"])

            if food["serving_size_g"] == None:
                serving_size_g.append(100)

            serving_size_g.append(food["serving_size_g"])

        for i in range(number_data):
            reply[indexkey[i]] = indexvalue[i]

        return reply
    else:
        return None

def is_float(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

def table_helper(array, more_info):
    keys = list(array)
    everything = []
    ingredient_numb = len(array['name'])
    length = len(keys)
    for i in range(length):
        everything.append(array[keys[i]])

    result = []
    for i in range(ingredient_numb):
        temp = []
        for j in [0, 10, 1, 4, 2, 3, 5, 6, 7, 8, 9]: # so the answer is in the right order. HARDCODING SO SHOULD CHANGE
            if j == 0:
                names_capital = str(everything[j][i].capitalize()) #to make the first charcter a capital letter
                temp.append(names_capital)
            else:
                temp.append(everything[j][i])
        result.append(temp)

    if more_info == "on":

        return result
    elif more_info == None:
        result_alternate =[]
        for i in range(ingredient_numb): #range is 4 because it has name calories serving size and protein
            temp = []
            for j in range(4):
                temp.append(result[i][j])
            result_alternate.append(temp)

        return result_alternate


def image_check(image_url):
   image_formats = ("image/png", "image/jpeg", "image/jpg")
   r = requests.head(image_url)
   if r.headers["content-type"] in image_formats:
      return True
   return False


