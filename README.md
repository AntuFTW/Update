# FINALPROJECT
#### Video Demo:  https://www.youtube.com/watch?v=GPCLdpjW4Z4
#### Description:
My project is called update and is all about planning your meals for your day when you are on a diet, and you need a certain number of calories and
protein per day. After the user registers at the resister page in the navigation bar the user can then log in with their credentials and they will be
at the home page where there is an apology that asks them to update their goals.

In the navigation bar there is a section called Goals where you can enter your weight, protein (per kg of your weight) and your daily calorie intake
goals. These are then saved into a SQL table which has a foreign key connected to the id of the user in the users table (which stores username and
passwords). If you wish to update these values, you can go to this webpage again via the navigation bar and your data will be deleted and
re-inserted in the table after you submit. After this you are sent to the home page but all this contains right now is your current goals so you
will have to add your recipes.

You can do this by going to the Nutrition Information tab in the navigation bar and you will be redirected to a page where you can enter the weight
and the names of the ingredients you used for your recipe, the textbox that takes this input is special as when it runs out of space in the textbox
the words will wrap round to a new line which does not normally happen, this is so the user can see everything they have written down so far
especially if it’s a long recipe . If you want extra nutrition information other than just protein, serving size and calories, such as saturated
fats and carbohydrates, your can check the checkbox on the page. This was added as an option as the API I am using gives this information
alongside the protein and calories and since some people may want to know about these nutrients as well the option is included. Moreover, you can
also enter a name of the recipe if you wish to save the recipe, the reason it is not saved automatically or doesn’t give an error when a name
isn’t inputted in the textbox is so that users can check their recipes or just certain ingredients without having to save the recipe or
ingredients just to go to the favourites tab later and delete them after if they don’t want to save the recipe. Finally, you can enter a URL
in a textbox that contains an image and the code checks if the URL is valid and if the URL contains a file of an image format. The function
that checks for the image format can sometimes be wrong as the URL “content-type” could be text even if the URL is for an image, in this case you will
have to use a different picture or change the content type yourself. This is because the function works by requesting the head of the URL which gives
you a dictionary, and in this dictionary the code indexs into the “content-type” where the output could consist of image/png, image/jpg etc for
images and test/html for text then checks if the content type is in an array that is previously defined. After this you can press submit and your
recipe, along with the image will be saved in the favourites tab.

The favourites tab contains images under which is the name of the recipe for that image. Images are used so its easier for the user to identify what
recipe they want to look at. After pressing on the image, you will be redirected to a page that contains the nutritional information like before but
here you can also delete the recipe if you wish to do so.

Finally, you can go back to the homepage where all your recipes will be contained along with their names in the second table. This table contains the
percentage of your daily calorie and protein goal that the recipe fulfils. This was done as its useful to see this as a percentage over the normal
numbers as numbers are not as user friendly. As well as this the last column lets you select checkboxes that help you plan what to have that day by
summing up the percentages for the checked recipes and showing it bellow. This was done using by Javascript and adding event listeners to each
checkbox for a “change”.

There are not many files in the python side of the directory. The main one is app.py which mainly just contains the logic to pass the values need to
the webpages via jinja and the render_template() function. The other main python file is helpers.py which just contains the functions need for app.
py. Functions such as image_check(), which checks if URL is in a image format and get_nutrition(), which sends a request to the API then formats the
following json response and returns a more easily usable dictionary. This python file even contains more functions essential to app.py. The test.py
is just a workspace where I could test my functions without running the whole website and making it easier to debug some mistakes, it does not need
to be in the directory however I have left it in regardless.

Nutrition.db is the SQLite database which contains three tables. These tables are for ‘users’ that store the usernames and passwords, ‘favourites’
which store the recipes for each user, ‘image’ which contains the recipe image URL and ‘goals’ which contains the goals for the user. The schema or
commands used to create these tables in the database are shown in the sqlcmd.txt file in the directory.


The templates folder contains all the HTML files that are used for the website routes. If Javascript is used it is contained in the HTML file. And
finally, the static folder just contains my header icon for the website, the background image I use for my HTML layout as well as the CSS file for my
HTML. The CSS has many aesthetic features one of which is the class for the body which sets the background to the selected picture and makes it
cover the whole screen because if this isn’t done the image repeats itself in the fashion of tiles instead.
