
===================================
Price And Nutrition Tracking System
===================================

PANTS is a self-hosted, open-source nutrition tracker and a tool for
nutritional data analysis of ingredients and recipes. It can be run on
your own computer or as a multiuser web service (e.g. for use by a
dietician/trainer/researcher and their clients).

In particular it is designed for:

   - Tracking the calories and other nutrients in your food, especially things cooked frequently.
   - Storing a list of recipes, and determining the cost and
     nutritional values of a recipe.
      - Storing recipes which are used in other recipes (recursively)
        e.g. a dough recipe and a filling recipe can both be
        components in a pie recipe.
   - Comparing the cost and nutritional values of different
     ingredients or recipes.
      - "What food has the most protein-per-dollar?"
      - "Which of these recipes has the least calories but is still high in fibre?"
   - Long term dietary planning - working out which products or
     recipes you want to include regularly in your diet, based on cost
     and other factors.

PANTS is *not* ideal for:

   - Tracking takeaway/restaraunt meals or prepackaged snack foods (rather than stuff you prepare yourself from basic ingredients)
   - Determing the best place to buy a shopping list of items (cost is
     not designed to be updated regularly or automatically, it is
     there for long-term planning).
   - Comparing the cost of products across different regions.

Features and Glossary
=====================

   - *Ingredients* are the fundamental foodstuffs


Roadmap/TODO/Bugs
=================

   - See seperate file TODO

Removed Features
================

   Collections
      Never properly implemented; need for this is reduced by heavier
      use of tags, using recursive recipes (e.g. an "ideal day" as a
      recipe), better frontend comparison tools and CSV export to
      spreadsheet for doing analysis there.

   Plots
      Recipes/Ingredients now have a CSV export button, use that to
      create charts externally via a spreadsheet.

   Amino Acids
      The original design was intended to handle detailed micronutrient
      stats (including individual amino acids, minerals, EFAs, fibre types)
      but when the nutrients object was merged into ingredient this was
      dropped. It was very underused but may be readded when the
      nutrient_data class/cache system is reworked to be less kludgy - see TODOs

Authors
=======

Dylan Leigh 2017-2019


