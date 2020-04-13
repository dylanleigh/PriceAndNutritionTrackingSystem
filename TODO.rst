
=======================
PANTS TODOs and Roadmap
=======================

(including known bugs/issues/kludges)

Urgent / Important
==================

- ** Unit tests are severely incomplete! **
- In particular need coverage to catch keyerrors on new installs, and other things that are going to affect new users.
- Fix all the FIXMEs in the code (see "make fixme" output) (most of these now relate to the NData work)
- Proper non-admin login/logout pages - can't login without admin interface

API (In Progress)
=================
- GET/POST/PUT/DELETE for DiaryFood [done]
- Model-level permissions for API views [done]
- Per-user ing/rec data (Nullable user field; exclude if user!= request.user) [done]
- GET/POST/PUT/DELETE for Ingredient [done except access checks]
- GET/POST/PUT/DELETE for Recipe [done]
- Add nested tags/flag/etc to Ingredient/Recipe serialisations
- Add price GET/POST/PUT/DELETE - access to user objects only, supplier read only
- Object-level permission to ensure users can only change their own
  objects [done for Rec/Diary]

NData and calculation DRYing (should be done before further recipe/diary work)
==============================================================================

All the nutrition_data properties should be its own class that manages
access/validation/caching/etc, and does operations like summing and averaging.
This will remove LOTS of almost-identical code across
ingredient/recipe/diary.

- ndata class/mixin
- ndata mixin for ing
- ndata mixin for rec
- ndata mixin for diary
- Fix per-serve/per-weight dichotomy in recipe components [done]
- Merge recipe and ingredient handling in diary save() and elsewhere
- Use F()/aggregate/annotate expressions in recipe calcs
- Allow filtering on calculated ndata
- Remove NDATA_ settings cruft
- ndata should handle micronutrients in some generic and graceful way

Deploy and Login, Production-Readiness
======================================

- Provide a fixture with some initial basic ingredients [done]
- Provide a fixture with few initial basic recipes, including at least one meta
- All urgent/important stuff at top done
- Deploy target assuming Heroku - include sub-parts below
- Proper non-admin login/logout pages [done by AustinGrey]
- Use login middleware instead of requiring mixins/decorators every view
- 404 template

Filtering Options
=================

- Use django-filter (replace custom tag view handling etc) (work in progress, mostly done)
- Limits and other context in FilterView
- Allow filtering on calculated ndata
- Fix/style form in ing-filter template
- filter recipe, diary as for ings

Exercise and Physiological Diary
================================

- Exercise diary item (start/stop time, calories, distance, etc)
- Physiological data diary item (weight, resting pulse, peak breath flow, body tape measurements, body fat caliper measurements, blood sugar etc)
- Show above in same table (3 rows of headers for item types)
- Derived physio data (BMR, body fat % from multiple sources, lean mass...)
- Deltas of physio data (weight loss, body fat % loss, lean mass gain etc)
- Totals and other aggregates for exercise/physio data

User Profiles
=============

- User-prof-object to hold age, height etc (age required for some physiological calcs)
- User preferences for FE (e.g. KJ or calories display, don't show some columns)
- Custom user "rank" formula replacing the built in hardcoded sorting rank
- Fix setting of daily target on target list page

Django Frontend
===============

- Automatic conversion of kilocalories to kilojoules when entering ingredients
- Ratio bar charts on ingredient detail aren't very useful without the ability to scale by grams or servings
- Ratio bar charts on recipe detail use only max limit; should use midpoint of min/max
- Replace recipe/ and ingredient/ with "landing" page with a list of tags and count of ings for each etc, links to /all/ etc
- Diary entry admin page should default to logged in user, etc
- Clean up templates by using more templatetags
- Handle particular target values set as None gracefully where they are displayed in lists
- 3-part bar chart templatetag for max-min-current target comparison
- Sanity Check page also listing out of date (e.g. nutrition over 2 year (?), price over 6 months) 
- Add chosen target comparison on recipe/ingredient detail pages (for pre/post workout targets etc)
- Consider Daily target comparison as an option on recipe/ingredient list pages
- "tags:" text should be a button that toggles tag-bar visibility on/off
- Diary edit/create/delete forms using generic views too
- Ing list column with recipe count (recursive/nonrecursive), click for recipe list filtered to ing?
- Bottom nav buttons for convenience
- View-on-site in all admin

Miscellaneous
=============

- Add Wall/Prep/Cooking times to recipes
- Add the capacity for recipes to lose water/oil during the process (changing the nutritional output to not be just the sum of ingredients)
- Add preparation_loss_factor to Product for e.g. peeling and trimming losses (can be half quantity for some vegetables, making them less cost-effective; also required for shopping list quantities etc). Add on product to allow e.g. pre-chopped vs whole veg price comparison
- Bug: Does not detect recursion loops in recipes
- Bug: User must handle out of date slugs on a name change
- Copy some of the cleaner explanations of the ratios and meta-recipes from various blog posts to README (also, clean up README in general)
- Diary doesn't rewrite cost if there is no cost on ingredient/recipe - should be allowed as a manual override but at least give a warning.
- Improved bulk import facilities in general, especially open data
- Consider: Move to per-100g instead of per-kg?
- "Favourite" ings/recs - show first in add-diary-item etc
- Diary nav for historic data - ArchiveView / TodayArchiveView/ DayArchiveView ?
- Recipe is_vegan/is_vegetarian/gluten_free/has_gluten properties - check via ingredient tags
- Invalidate cache of ingredient/recipe/quantity on nutrients change
- Invalidate cache of product/ingredient/etc on price change
- Option to Flatten and/or Crystallize ingredients on recipe detail view? Alternatively a "Print" version

