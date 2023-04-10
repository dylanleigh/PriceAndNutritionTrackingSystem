
===================================
Price And Nutrition Tracking System
===================================

Note for Current Users - DB Changes when Upgrading
==================================================

Changes to the database schema have been made recently (2020-04-13)
and when upgrading from older versions you will need to migrate your
database by running './manage.py migrate' - see the "Schema Changes"
subsection below for more details.

Introduction
============

PANTS is a self-hosted, open-source nutrition tracker and a tool for
nutritional data analysis of ingredients and recipes. It can be run on
your own computer or as a multiuser web service (e.g. for use by a
dietician/trainer/researcher and their clients).

As well as tracking daily calories etc, PANTS is designed to make it
easy to compare and optimize recipes which form a regular part of your
diet; a key feature is the ability for recipes to be components of
other recipes.

For example a dough recipe and a filling recipe can both be components
in a pie recipe; you can clone the pie recipe with alternate fillings
to compare the nutritional values of the alternatives. Any changes to
the dough recipe will be reflected in the data for all of the pies.
These "meta-recipes" can also be used to provide an "average"
breakfast/lunch/snack/etc for meal and diet planning.

PANTS is under active, daily use by the author so updates should be
fairly frequent. On the other hand, the code tends to be quick and
dirty as new things get added because the author wanted to use them
ASAP while cooking his dinner.

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
- Long term dietary planning - working out which ingredients or recipes you want to include regularly in your diet, based on cost and other factors.

PANTS is *not* ideal for:

- Tracking takeaway/restaraunt meals or prepackaged snack foods (rather than stuff you prepare yourself from basic ingredients)
- Determing the best place to buy a shopping list of items (cost is not designed to be updated regularly or automatically, it is there for long-term planning).
- Comparing the cost of ingredients across different regions.

Overview and Features
=====================

There are 4 basic sections of the system:

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
   for particular meals (e.g. a pre/post workout meal), or special days.

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

   This can also be used as a sort of "variables" in other recipes,
   e.g. if you sometimes use normal flour or gluten free flour, a "flour"
   recipe can be created which can be used to toggle between them with
   one change which effectively toggles the ingredient in multiple
   recipes at once.

PANTS doesn't make assumptions or guesses
   It is preferable to show no data instead of wrong data. If an ingredient has
   something missing (e.g. no fibre listed, no prices), any
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

Per-user and global data
   Ingredients and Recipes added by the admin are visible to all users
   (but not editable by them); Normal users can also enter in their
   own Recipes and Ingredients, which only they have access to
   (sharing may be added in a later version).

Progress/Percentage bars
   Once your default target is set, it will be used to compare against
   ingredients/recipes you view so you can see how much % of your
   daily intake that recipe/ingredient will satisfy. On most pages,
   Green/Yellow/Red bars indicate how much of the daily target's
   minimum/maximum are accounted for; Purple progress bars are used
   to show percentage out of the current total, or amount compared to the
   highest value in a list of recipes/ingredients.

Micronutrients
   All Australian standard nutritional data is stored (e.g. sodium and
   saturated fat) but not everything is shown in all views by default.
   There was support for micronutrients such as individual amino acids
   which was removed as part of a DB schema change but this is planned to
   be readded in a more stable way (see roadmap for details).


Installation
============

::

   git clone https://github.com/dylanleigh/PriceAndNutritionTrackingSystem.git
   cd PriceAndNutritionTrackingSystem

VirtualEnv
----------

It is highly recommended that PANTS is installed in a virtual environment, and
comes with a requirements.txt for pip::

   python3 -m venv env
   source env/bin/activate

Requirements
------------

::

   pip install -r requirements.txt

These will be installed automatically via pip:

- Django 2+
- Django-extensions 1.8+
- Django REST Framework
- Django-filter

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
   installations. **If someone knows the secret key it may be possible to
   login as admin users and mess with things, so keep it secret**.

Setup 2: Migrations and Admin User
----------------------------------

Finally you will need to run initial migrations and create an admin
user who can log in and create the initial ingredients, recipes etc::

   cd pants
   ./manage.py migrate
   ./manage.py createsuperuser

Starting the Server
-------------------

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
which use those recipes...)

The about page will show some basic DB stats, including the count of
ingredients which are missing nutritional data and other potential
issues.

No ingredients/recipes need to be created to start using the diary
(although every entry will have to have all its data added manually if
there are no recipes or ingredients to use).

Adding Non-Super Users
----------------------

TODO this needs to be documented for API consumers.

API
===

This is a work in progress as of 2020-04-13. Documentation will go
here when it's implemented for all major models. It is located at
/api/1/ (i.e. http://127.0.0.1:8000/api/1/ on a local server).

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

No further user input or manual conversion should be required. The
details below are mostly for background.

2020-04-13
   Recipe and Ingredient can now be linked to an "owner" (user) - user
   created recipes and ingredients through the API will be owned by
   that user. Only the logged in user can see/edit things they own.

   "Global" recipes/ingredients with no owner are visible to everyone,
   and only editable by admin (i.e. no change from previous versions)

2020-04-02
   Each Recipe and Ingredient may now have an "Introduction" and
   "Notes" - these are freeform text fields that are simply displayed
   at the start/end of the detail page for the recipe or ingredient.

2020-03-20 (v0.93)
   Following on from yesterday's changes, Price has now been fully
   detached from Product. This update also changes Prices to require an
   Ingredient set (during the migration, this was optional to allow
   data to be migrated automatically).

   If there are errors applying this migration it is probably because
   there are Price objects which don't have an Ingredient. The last
   version should have converted all the old ones automatically, and
   converted any new ones created in the admin when they were saved.
   However, if by some chance you have any corrupt prices not linked to
   an ingredient, these will have to be deleted for the migration to
   work.

   The product model still exists, but is now deprecated; it has no
   current purpose except to associate brand names with ingredients.
   If you don't care about that, products can be all safely deleted
   via the admin interface (use the checkbox to "select all" and then
   drop-down action box to "delete selected"). They should not be
   any performance effects from leaving them there, as no calculations
   use products anymore.

2020-03-19 (v0.92)
   Prices are changing from being attached to a Product to directly
   being attached to Ingredient, to simplify both the user interface
   and the code.

   As of this version, Price is attached to both Product and
   Ingredient. Ingredient will be set automatically from the Product.

   Future versions will make Price settable via the Ingredient section
   of the admin interface rather than Product.

2020-03-11
   Recipe Flags added. These differ from Tags in two ways - each
   recipe can have only one flag, but flags are much more visible
   (being shown in lists etc).

   The intended use case is to mark recipes which are OK for general
   use to differentiate them from recipes which aren't working and
   need further changes and testing, or outdated recipes no longer
   recommended. However, they can be used for whatever the admin
   wants.

   Also, tags for Recipe and Ingredient can now have a brief text
   description which is shown in list view when that tag is selected.

2019-09-07 (v0.91)
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

Products (partially)
   After the nutrient model was merged into Ingredient, Product lost
   it's ability to have separate nutrient data, and it was just a
   redundant way of linking prices to ingredients, which is now done
   directly.

   The product model still exists in the admin, but currently has no
   purpose except to associate brand names with an ingredient.
   It may be used again in the future for storing further data about a
   specific branded product.

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

See the todo list below for more details.

Bits Useful for Other Projects
------------------------------

- Recipe/Ingredient have a very simple but effective CSV export view.
- There are convenient templatetags to do division, combined min/max percentage display and generate a little CSS bar chart (most tabular data uses them, see the screenshots for examples).


Roadmap, Todos and Issues
-------------------------

See https://github.com/dylanleigh/PriceAndNutritionTrackingSystem/blob/master/TODO.rst


Authors
=======

Dylan Leigh 2017-2019


