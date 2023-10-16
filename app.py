import os
import ast
import validators

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from decimal import Decimal, ROUND_UP

from helpers import apology, login_required, get_nutrition, is_float, table_helper, image_check

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///nutrition.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/favorite_display", methods = ["GET","POST"])
@login_required
def favorite_display():
    if request.method == "POST":
        title_name = request.form.get("delete")
        print( title_name)
        value = db.execute("SELECT * FROM favorites WHERE faveuser_id=? AND name=?", session["user_id"], title_name)
        if value == None:
            return apology("This recipe does not exist", 400)

        recipe_id = db.execute("SELECT recipe_id FROM favorites WHERE faveuser_id=? AND name=?", session["user_id"], title_name)
        db.execute("DELETE FROM image WHERE recipe_id=?", recipe_id[0]["recipe_id"])
        db.execute("DELETE FROM favorites WHERE faveuser_id=? AND name=?", session["user_id"], title_name)
        return redirect("/")

    return redirect("/")



@app.route("/favorites", methods = ["GET","POST"])
@login_required
def favorites():
    if request.method == "POST":
        id_val = request.form.get("id")
        data = db.execute("SELECT * FROM favorites WHERE recipe_id=?", id_val)
        title_name = data[0]["name"]
        headers = ast.literal_eval(data[0]["headers"])
        sum_totals = ast.literal_eval(data[0]["sum_totals"])
        nutrition = ast.literal_eval(data[0]["nutrition"])
        formated_table_rows = ast.literal_eval(data[0]["formated_table_rows"])
        row_length = data[0]["row_length"]
        return render_template("favorite_display.html", title_name = title_name, headers = headers, sum_totals = sum_totals, nutrition = nutrition, formated_table_rows = formated_table_rows, row_length = row_length)

    data_favorites = db.execute("SELECT name, recipe_id FROM favorites WHERE faveuser_id=?", session["user_id"])
    # To get picture URL
    img_url_list=[]
    for i in range(len(data_favorites)):
        recipeid_temp = (data_favorites[i]["recipe_id"])
        img_urldata = db.execute("SELECT img_url FROM image WHERE recipe_id=?", recipeid_temp)
        img_url_list.append(img_urldata[0]["img_url"])

    # To get the names and recipe_id
    length_fave = len(data_favorites)
    names = []
    ids = []
    for i in range(length_fave):
        names.append(data_favorites[i]["name"])
        ids.append(data_favorites[i]["recipe_id"])

    return render_template("favorites.html", img_url_list = img_url_list, names = names, ids = ids, length_fave = length_fave)


@app.route("/nutrition", methods = ["GET","POST"])
@login_required
def nutrition():
    if request.method == "POST":
        #name, tcalories, tfat_total_g, tfat_saturated_g, tprotein_g, tsodium_mg, tcholesterol_mg, tcarbohydrates_total_g, tfiber_g, tsugar_g, tserving_size_g = ([] for i in range(number_data))
        totals = ["serving_size_g", "calories", "protein_g", "fat_total_g", "fat_saturated_g", "sodium_mg", "cholesterol_mg", "carbohydrates_total_g", "fiber_g", "sugar_g"]
        query = request.form.get("query")
        nutrition = get_nutrition(query)
        print(nutrition)
        sum_totals=[]
        if nutrition == None:
            return apology("invalid query", 400)

        # If name is present check if there is allready the same name for the same user in favorites
        name_check = request.form.get("recipename")
        favorites_user = db.execute("SELECT name FROM favorites WHERE faveuser_id=? AND name=?", session["user_id"], name_check)
        if len(favorites_user) > 0:
            return apology("already a recipe with that name")
        # This checks the if image url is present, if so its adds to database, if not it will add stock pic instead
        if request.form.get("recipeimg", 400) != "":
            print(request.form.get("recipeimg"))

            if validators.url(request.form.get("recipeimg")) != True:
                return apology("Invalid URL", 400)

            if image_check(request.form.get("recipeimg")) == False:
                return apology("The image URL is not valid", 400)

            image_url = request.form.get("recipeimg")
        elif request.form.get("recipeimg", 400) == "":
            image_url = "https://images.unsplash.com/photo-1504674900247-0877df9cc836?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80"


        for index in totals: #get totals
            sum_temp = round(sum(nutrition[index]), 6)
            sum_totals.append(sum_temp)

        # Table headers depending if extra nutrients option was selected if checkbox is not ticked the header list will only contain the decault values, if ticked
        # then the opposite
        headers_total = ["Name","Serving Size (g)", "Calories (kcal)", "Protein (g)", "Total Fats (g)", "Saturated Fats (g)", "Sodium (mg)", "Cholesterol (mg)", "Total Carbohydrates (g)", "Fiber (g)", "Sugar (g)"]

        if request.form.get("more_options") == "on":
            headers = headers_total
        elif request.form.get("more_options") == None:
            headers = headers_total[:4] #3 because 0 is serving size, 1 is protein, 2 is calories and it stops at 3
            sum_totals = sum_totals[:3] # has to change so another template isnt needed for a different case
        formated_table_rows = table_helper(nutrition, request.form.get("more_options"))
        row_length = len(formated_table_rows[0])

        # now check for favorites check and to save the data to sql
        if request.form.get("recipename") != "": #sql can not store list so converting to text then will convert back to list
            fave_name_sql = request.form.get("recipename")
            headers_sql = str(headers)
            sum_totals_sql = str(sum_totals)
            nutrition_sql = str(nutrition)
            formated_table_rows_sql = str(formated_table_rows)
            row_length_sql = row_length #int so it stays the same, just for completness
            db.execute("INSERT INTO favorites (faveuser_id, name, headers, sum_totals, nutrition, formated_table_rows, row_length) VALUES(?, ?, ?, ?, ?, ?, ?)", session['user_id'], fave_name_sql, headers_sql, sum_totals_sql, nutrition_sql, formated_table_rows_sql, row_length_sql)

        #  This saves the img url to the database which is connected to recipes
        if request.form.get("recipename") != "":
            recipe_id_db = db.execute("SELECT recipe_id FROM favorites WHERE faveuser_id=? AND name=?", session["user_id"], request.form.get("recipename"))
            recipe_id = recipe_id_db[0]["recipe_id"]
            db.execute("INSERT INTO image (recipe_id, img_url) VALUES(?, ?)", recipe_id, image_url)


        return render_template("tablenutrition.html", headers = headers, sum_totals = sum_totals, nutrition = nutrition, formated_table_rows = formated_table_rows, row_length = row_length)
        #return render_template("tablenutrition.html", sum_totals = sum_totals, nutrition = nutrition)
        #return render_template("tablenutrition.html") I was planning of sending the sums and keys and the values of the results to a new html to then
        #put it in a table so the user can confirm that this is what they wanted and choose to save it if they want to look at it later. As well as this i will do
        #caluclations on how much of their daily goal they have achieved with their diet with mabye plus or minus 10 percent (database). so they can see if they need mroe
        # or less

    return render_template("nutrition.html")

@app.route("/")
@login_required
def index():
    goals = db.execute("SELECT * FROM goals WHERE stat_id=?", session["user_id"])
    print(goals)
    if len(goals) == 0:
        return apology("please update your goals in the goals tab", 400)
    weight_goal = goals[0]["weight"]
    protein_total_goal = goals[0]["protein_per_kg"] * weight_goal
    calories_goal = goals[0]["calories"]

    data = db.execute("SELECT * FROM favorites WHERE faveuser_id=?", session["user_id"])
    names = []
    serving_size = []
    calorie_goal_percent = []
    protein_goal_percent = []
    calorie_int = []
    protein_int = []
    for i in range(len(data)):
        names.append(data[i]["name"])
        totals_temp = ast.literal_eval(data[i]["sum_totals"])
        serving_size.append(str(totals_temp[0]) + "g")
        calorie_rounded = round((totals_temp[1] / calories_goal), 3)
        protein_rounded = round((totals_temp[2] / protein_total_goal), 3)
        calorie_goal_percent.append(str(calorie_rounded * 100) + "%")
        protein_goal_percent.append(str(protein_rounded * 100) + "%")
        protein_int.append(protein_rounded * 100)
        calorie_int.append(calorie_rounded * 100)

    protein_total_goal = round(protein_total_goal, 2)

    length = len(serving_size)
    return render_template("home.html", weight_goal = weight_goal, protein_total_goal = protein_total_goal, calories_goal = calories_goal, calorie_goal_percent = calorie_goal_percent, protein_goal_percent = protein_goal_percent, names = names, serving_size = serving_size, length = length, calorie_int = calorie_int, protein_int = protein_int)

@app.route("/goals", methods = ["GET", "POST"])
@login_required
def goals():
    if request.method == "POST":
        weight = request.form.get("weight")
        protein = request.form.get("protein")
        calories = request.form.get("calories")

        if not is_float(weight):
            return apology("Please Enter Valid Inputs1", 400)

        if round(float(weight), 2) < 0 or round(float(calories), 2) < 0 or round(float(protein), 2) < 0:
            return apology("Please Enter Valid Inputs2", 400)

        if weight == None or protein == None or calories == None:
            return apology("Please Enter all Inputs", 400)

        if len(db.execute("SELECT * FROM goals WHERE stat_id=?", session['user_id'])) == 0:
            db.execute("INSERT INTO goals (stat_id, weight, protein_per_kg, calories) VALUES(?, ?, ?, ?)", session['user_id'], weight, protein, calories)
            # inserts data into the goals table
        else:
            db.execute("UPDATE goals SET weight=?, protein_per_kg=?, calories=? WHERE stat_id=?", weight, protein, calories, session['user_id'])
            #db.execute("UPDATE users SET cash=? WHERE id=?", new_balance, session['user_id'])
            # updates the table if the user decides he want to change the information

        return redirect("/")

    return render_template("goals.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            return apology("please enter username", 400)
        # Check for duplicate username
        usernames_list = db.execute("SELECT username FROM users")
        usernames = []
        for i in range(len(usernames_list)):
            usernames.append(usernames_list[i]['username'])

        if username in usernames:
            return apology("username allready in use", 400)

        passw = request.form.get("password")
        if not passw:
            return apology("please enter password", 400)

        passwcon = request.form.get("confirmation")
        if not passwcon:
            return apology("please enter password confirmation", 400)

        if passw != passwcon:
            return apology("the passwords do not match, please try again.", 400)

        hashedpass = generate_password_hash(passw, method='pbkdf2', salt_length=16)
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hashedpass)
        return redirect("/login")

    """Register user"""
    return render_template("register.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        # Redirect user to home page
        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/changepass", methods=["GET", "POST"])
@login_required
def change_pass():
    if request.method == "POST":
        # Get password hashes and new password for comparison
        current_password = request.form.get("current_password") # Requested
        print(f"{current_password}")
        new_password = request.form.get("new_password")
        user_pass = db.execute("SELECT * FROM users WHERE id=?", session['user_id'])
        if not check_password_hash(user_pass[0]['hash'], current_password):
            return apology("your current password does not match, please try again", 400)

        if len(new_password) < 1:
            return apology("please enter a new password", 400)
        # Update users table with new hash and then logout the user so he can log in again
        new_passwordhash = generate_password_hash(new_password, method='pbkdf2', salt_length=16)
        db.execute("UPDATE users SET hash=? WHERE id=?", new_passwordhash, session['user_id'])
        # Forget any user_id
        session.clear()
        # Redirect user to login form
        return redirect("/")

    return render_template("changepass.html")

