import csv
import datetime
import pytz
import requests
import subprocess
import urllib
import uuid
import json
import validators

from flask import redirect, render_template, session
from functools import wraps

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
            protein_g.append(food["protein_g"])
            fat_total_g.append(food["fat_total_g"])
            fat_saturated_g.append(food["fat_saturated_g"])
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

#answer = get_nutrition("100g carrot and 200g banana")

#print(answer)

#def table_helper(array, more_info):
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
    #for i in range(len(keys)):

##print(table_helper(answer, "on"))
##https://geekrobocook.com/wp-content/uploads/2021/03/1.-Cream-of-Tomato-Soup.jpg
a = "https://veenaazmanov.com/wp-content/uploads/2012/12/Easy-Chicken-Curry-Recipe-with-6-ingredients1.jpg"

def is_url_image(image_url):
   image_formats = ("image/png", "image/jpeg", "image/jpg")
   r = requests.head(image_url)
   print(r.headers["content-type"])
   if r.headers["content-type"] in image_formats:
      return True
   return False

#answer_img = is_url_image("https://images.unsplash.com/photo-1504674900247-0877df9cc836?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80")

validation = validators.url(a)
if validation:
    print("URL is valid First")
else:
    print("URL is invalid First")

print(is_url_image(a))