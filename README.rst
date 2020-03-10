
===================================
Price And Nutrition Tracking System
===================================

Note for Current Users
======================

Significant DB changes have been made recently (2019-09-08) and you
will need to migrate your recipe data by running './manage.py migrate'
- see the "Schema Changes" subsection below for more details.

Introduction
============

PANTS is a self-hosted, open-source nutrition tracker and a tool for
nutritional data analysis of ingredients and recipes. It can be run on
your own computer or as a multiuser web service (e.g. for use by a
dietician/trainer/researcher and their clients).

As well as tracking daily calories etc, PANTS is designed to make
it easy to compare and optimize recipes which form a regular part of your
diet; a key feature is the ability for recipes to be components of
other recipes. For example a dough recipe and a filling recipe can
both be components in a pie recipe; you can clone the pie recipe
with alternate fillings to compare the nutritional values of the
alternatives. Any changes to the dough recipe will be reflected in
the data for all of the pies.

These "meta-recipes" can also be used to easily compare between
different similar meals and provide an "average" breakfast/snack/etc
for meal and diet planning.

Other features include support for multiple daily targets with a
minimum and maximum desired values and visualisation of data across
the last 24 hours (not just since mindnight like most other trackers)
to allow for a more realistic view of daily consumption.

PANTS is currently (as of 2019) under active, daily use by the author
so updates should be fairly frequent. On the other hand, the code
tends to be quick and dirty as new things get added because
the author wanted to use them ASAP while cooking his dinner.

It is currently not recommended for non-technical users; basic
familiarity with Django is useful.

.. contents:: Contents:
   :backlinks: none

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
   for particular meals (e.g. a pre/post workout meal), or special
   days.

Products
   DEPRECATED: This feature is underused, redundant and is being
   phased out, with Prices to directly apply to Ingredients soon, and
   the ability to mark an Ingredient as a brand-specific version of
   another, more generic ingredient.

   Specific versions of an ingredient like "Supermarket X's Own
   Brand Skim Milk". *Products* are available from *Suppliers* at
   specified *Prices*.

Some example screenshots can be seen at https://github.com/dylanleigh/PriceAndNutritionTrackingSystem/tree/master/screenshots

Other Feature Notes and Tips
----------------------------

Tagging
   Ingredients and recipes can be given multiple tags for easier searching and
   analysis; this makes it much easier to (for example) compare the fibre
   per calorie in different vegetables or the calories per serve of
   different dessert.

   Recipes can also be "flagged" to mark them as untested, tested and
   working, requiring further improvement, outdated, etc.

Repurposing Recursive Recipes
   As recipes can include other recipes, this can be used for other
   analysis and planning purposes.

   For example. an "average breakfast" meta-recipe which just contains one
   of all the other breakfast recipes; divided by the number of serves
   this provides an average breakfast which can be used for planning.
   This can be combined with other "typical meal" meta-recipes to make
   an "average day" overview which can be used as a meal plan.

   Changes to a recipe (or ingredient) will be reflected in any
   ingredient that uses them, so if you alter a recipe this will be
   reflected in the "typical meal/day" recipes.

   They can also be used as "variables" in other recipes, e.g. if you
   sometimes use normal flour or gluten free flour, a "flour" recipe
   can be created which can be used to toggle between them with one
   change which effectively toggles the ingredient in multiple recipes
   at once.

PANTS doesn't make assumptions or guesses
   It is preferable to show no data instead of wrong data. If an ingredient has
   something missing (e.g. no fibre listed, no product so no prices), any
   derived statistics will also be missing (e.g. no fibre-per-kj, or no
   protein-per-$ if there is no price). This also means that recipes
   which use that ingredient will not show a value for the sum of fibre
   in that recipe until all ingredients have that data entered in.

PANTS doesn't assume everyone sleeps at midnight
   Diary shows breakdown of nutrients by both calendar day and 24-hour
   periods, so it can be used by shift workers or those with irregular
   sleep cycles.

Recipes update; Diary doesn't change
   Diary entries are "crystallized" (future changes to a recipe do not
   affect past entries). On the other hand, changes to an
   ingredient/recipe immediately show up in any recipes which use them.

Once-off Diary entries
   Diary entries do not have to be linked to a specific
   ingredient/recipe, one off diary entries can be created with manual
   nutritional data e.g. when going out for the night and you can only
   guess how many calories are in dinner.

Micronutrients
   All Australian standard nutritional data is stored (e.g. sodium and
   saturated fat) but not everything is shown in all views by default.
   There was support for micronutrients such as individual amino acids
   which was removed as part of a DB schema change but this is planned to
   be readded in a more stable way (see roadmap for details).

Per-user and global data
   Diary is per-user, but ingredient/product/recipe are global. There
   are plans to add per-user recipes but this is very far down the
   roadmap as the focus is on adding features for personal use (it
   wouldn't be complex however).

Progress/Percentage bars
   Once your default target is set, it will be used to compare against
   ingredients/recipes you view so you can see how much % of your
   daily intake that recipe/ingredient will satisfy. On most pages,
   Green/Yellow/Red bars indicate how much of the daily target's
   minimum/maximum are accounted for; Purple progress bars are used
   to show percentage out of the current total, or amount compared to the
   highest value in a list of recipes/ingredients.


Installation
============

It is highly recommended that PANTS is installed in a virtualenv, and
comes with a requirements.txt for pip::

   virtualenv -p python3 pants
   cd pants
   . bin/activate
   git clone https://github.com/dylanleigh/PriceAndNutritionTrackingSystem.git
   cd PriceAndNutritionTrackingSystem
   pip install -r requirements.txt

Requirements
------------

These will be installed automatically via pip:

- Django 2+
- Django-extensions 1.8+
- Future versions may require djangorestframework and django-filter
  for the API.

Setup 1: Secret Key
-------------------

The environment variable "PANTS_DJANGO_SECRET_KEY" needs to be set for
PANTS/Django to start.

The exact place to set this will depend on the OS and environment you
are using. For hosted infrastructure such as AWS or Heroku this can be
set in the instance settings; for local installs you can set it as
part of the virtualenv activation script or as a variable on the
account of the user who will be running it::

   echo export PANTS_DJANGO_SECRET_KEY='968af690a7bcca77c9261e395885af77bc661d1c' >> ~/.profile

You can generate an appropriate secret key from the SHA1 of any
randomly chosen phrase or file::

   $ echo blahblahblah | sha1sum
   968af690a7bcca77c9261e395885af77bc661d1c  -
   $ export PANTS_DJANGO_SECRET_KEY='968af690a7bcca77c9261e395885af77bc661d1c'

Warning
   The Django Secret Key is used to generate session tokens and other
   cryptographically important things. Keeping it in an environment
   variable makes it easier to have seperate, secure secrets on different
   installations. If someone knows the secret key it may be possible to
   login as admin users and mess with things, so keep it secret.

Setup 2: Migrations and Admin User
----------------------------------

Finally you will need to run initial migrations and create an admin
user who can log in and create the initial ingredients, recipes etc::

   cd pants
   ./manage.py migrate
   ./manage.py createsuperuser

Starting
--------

To run the server locally and access it via a browser::

   ./manage.py runserver

Sample Ingredient Data
----------------------

The author's ingredient data (about 200 ingredients as of 2019) can be
imported from a fixture with this command::

   ./manage.py loaddata fixtures/pants-ingredient-fixture.json

This command should only be run on an empty/new database, to avoid
overwriting any entries you have already created 

Starting data entry
-------------------

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


Bits Useful for Other Projects
------------------------------

- Recipe/Ingredient have a very simple but effective CSV export view.
- There are convenient templatetags to do division, combined min/max percentage display and generate a little CSS bar chart (most tabular data uses them, see the screenshots for examples).


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

Schema Changes
--------------

For all changes mentioned here, your database must be migrated by
running the following commands::

   git pull
   ./manage.py migrate

(No user input or manual conversion should be required)


2019-09-07
   Recipe Components now have separate "servings" and weight" to bring
   them in line with the way all other models work (previously,
   "weight" was interpreted as number of serves if connected to a
   recipe).

   This fixes various issues, including data entry errors from
   overloading one field to have two meanings and allows a lot of the
   code between ingredient/recipe/diary to be simplified.

   Existing recipes will be converted to this new system by
   recipes/migrations/0018_auto_20190908_0152.py when the migrate
   command is run.

Removed Features
----------------

Collections
   Never properly implemented; need for this is reduced by heavier
   use of tags, creative use of recursive recipes (e.g. a "daily meal
   plan" as a "recipe"), better frontend comparison tools and CSV
   export to spreadsheet for doing analysis there.

Plots
   Recipes/Ingredients now have a CSV export button, use that to
   create charts externally via a spreadsheet.

Amino Acids
   The original design could handle detailed micronutrient
   stats (including individual amino acids, minerals, EFAs, fibre types)
   but when the nutrients object was merged into ingredient this was
   dropped. It was rarely used, but may be readded when the
   nutrient_data class/cache system is reworked to be less kludgy - see TODOs

Authors
=======

Dylan Leigh 2017-2019


