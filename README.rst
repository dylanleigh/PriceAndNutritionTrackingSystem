
===================================
Price And Nutrition Tracking System
===================================

PANTS is a self-hosted, open-source nutrition tracker and a tool for
nutritional data analysis of ingredients and recipes. It can be run on
your own computer or as a multiuser web service (e.g. for use by a
dietician/trainer/researcher and their clients).

PANTS is currently (as of 2019) under active, daily use by the author
so updates should be fairly frequent. On the other hand, the code
tends to be quick and dirty as new things get added because
the author wanted to use them ASAP while cooking his dinner.

It is currently not recommended for non-technical users; basic
familiarity with Django is useful.

Use Cases
=========

In particular PANTS is designed for:

- Tracking the calories and other nutrients in your food, especially things cooked frequently.
- Storing a list of recipes, and determining the cost and nutritional values of a recipe. This includes recipes which are used in other recipes (recursively) e.g. a dough recipe and a filling recipe can both be components in a pie recipe.
- Comparing the cost and nutritional values of different ingredients or recipes (e.g. "What food has the most protein-per-dollar?", "Which of these recipes has the least calories but is still high in fibre?").
- Long term dietary planning - working out which products or recipes you want to include regularly in your diet, based on cost and other factors.

PANTS is *not* ideal for:

- Tracking takeaway/restaraunt meals or prepackaged snack foods (rather than stuff you prepare yourself from basic ingredients)
- Determing the best place to buy a shopping list of items (cost is not designed to be updated regularly or automatically, it is there for long-term planning).
- Comparing the cost of products across different regions.

Overview and Features
=====================

There are 5 basic sections of the system:

Ingredients
   Generic ingredients, like "Rolled Oats", "Green Split Peas",
   "Skim Milk", not any particular brand or store.
   You can compare relative data such as Protein per Joule or Fibre per
   Dollar on the ingredients pages.

Products
   Specific versions of an ingredient like "Supermarket X's Own
   Brand Skim Milk". *Products* are available from *Suppliers* at
   specified *Prices*.

Recipes
   A collection of ingredients and/or other recipes, showing the combined
   nutritional value and cost of each serve of the recipe, as well as the relative
   per-calorie and per-dollar values.

Diary
   Record of food intake; compares the total to your target and also
   shows how much each food contributed to your total for the time
   period.

Targets
   Minimum and Maximum nutritional and cost values you are aiming to
   reach each day. As well as daily targets you can also set targets
   for particular meals (e.g. a pre/post workout meal).

Some example screenshots can be seen at https://github.com/dylanleigh/PriceAndNutritionTrackingSystem/tree/master/screenshots

Other Feature Notes and Tips
----------------------------

- Ingredients and recipes can be tagged for easier searching and analysis; this makes it much easier to (for example) compare the fibre per calorie in different vegetables or the calories per serve of different desserts
- PANTS prioritizes not showing bad data. If an ingredient has something missing (e.g. no fibre listed, no product so no prices), any derived statistics will also be missing (e.g. no fibre-per-kj, or no protein-per-$ if there is no price). This also means that recipes which use that ingredient will not show a value for the sum of fibre in that recipe until all ingredients have that data entered in.
- Recursive recipes can be used for other semantic purposes, e.g. to make an "average breakfast" recipe which is your other breakfast recipes combined (then divided by number of serves). These can be in turn combined to make an "average day" overview which can be used as a meal plan.
- Diary shows breakdown of nutrients by both calendar day and 24-hour periods, so it can be used by shift workers or those with irregular sleep cycles.
- Diary entries are crystallized so future changes to a recipe do not affect past entries (on the other hand, changes to an ingredient/recipe immediately show up in any recipes which use them).
- Diary entries do not have to be linked to a specific ingredient/recipe, one off diary entries can be created with manual nutritional data e.g. when going out for the night and you can only guess how many calories are in dinner.
- All Australian standard nutritional data is stored (e.g. sodium and saturated fat) but not everything is shown in all views by default. There was support for micronutrients such as individual amino acids which was removed as part of a DB schema change but this is planned to be readded in a more stable way (see roadmap for details).
- Diary is per-user, but ingredient/product/recipe are global. There are plans to add per-user recipes but this is very far down the roadmap as the focus is on adding features for personal use (it wouldn't be complex however).
- A default target must be set for progress bars to appear on the data on the home page.

Installation
============

It is highly recommended that PANTS is installed in a virtualenv, and
comes with a requirements.txt for pip::

   virtualenv pants
   cd pants
   . bin/activate
   git clone https://github.com/dylanleigh/PriceAndNutritionTrackingSystem.git
   pip install -r requirements.txt

Requirements
------------

- Django 1.11+
- Django-extensions 1.8+
- Future versions may require djangorestframework and django-filter.

Setup
-----

You will need to create an admin user first who can log in and create
ingredients, recipes etc::

   ./manage.py createsuperuser

Then run the server locally and access it via a browser::

   ./manage.py runserver

Initial data entry
------------------

You will need to log in as an admin user (at
http://127.0.0.1:8000/adminbackend/ ) to start creating initial
ingredients, and then recipes which use those ingredients (and recipes
which use those recipes...) To show cost data products need to be
added for each ingredient.

The about page will show some basic DB stats, including the count of
ingredients which are missing nutritional data and other potential
issues.

No ingredients/recipes need to be created to start using the diary
(although every entry will have to have all its data added manually if
there are no recipes or ingredients to use).

Developer Notes
===============

As mentioned earlier the code contains many crufty bits because many
features were added quickly when immediately required.

In particular, sets of "nutrition data" are often passed around as a
dict with a few specific sets of keys (specified in settings) and
there is an ongoing project to convert this to a class that manages it
in a sane way, handling all comparisons, additions and per-weight
calculations sensibly. A lot of future work is on hold pending this
tech debt cleanup to be completed.

Also, the django template frontend is quite basic. It is not really
intended for end-user use, only for personal or debugging purposes. It
does not have any forms so all data entry including diary is done via
the admin interface. Ideally "customer" users should access the
service through an app or a single page frontend. Future frontend work
will mostly therefore be via other projects using an API (I do plan to
add an Android app for my personal use).

See the todo list below for more details.


Roadmap, Todos and Issues
-------------------------

See https://github.com/dylanleigh/PriceAndNutritionTrackingSystem/blob/master/TODO.rst

History
=======

PANTS grew out of a spreadsheet I was using in early 2017 to do
nutritional analysis of different foods, looking for the best ratios
of protein and fibre to calories and cost.

I wanted to add recipes which combined different ingredients and this
became so cumbersome I realised it would be easier to do in a DB and
started the project in Django, importing the initial set of
ingredients from the spreadsheet. Soon I also realised since I was
entering in all my recipes here it would also be easier if I used it
as my daily calorie counter and added that as well.

Removed Features
----------------

Collections
   Never properly implemented; need for this is reduced by heavier
   use of tags, using recursive recipes (e.g. an "ideal day" as a
   recipe), better frontend comparison tools and CSV export to
   spreadsheet for doing analysis there.

Plots
   Recipes/Ingredients now have a CSV export button, use that to
   create charts externally via a spreadsheet.

Amino Acids
   The original design could intended to handle detailed micronutrient
   stats (including individual amino acids, minerals, EFAs, fibre types)
   but when the nutrients object was merged into ingredient this was
   dropped. It was rarely used, but may be readded when the
   nutrient_data class/cache system is reworked to be less kludgy - see TODOs

Authors
=======

Dylan Leigh 2017-2019


