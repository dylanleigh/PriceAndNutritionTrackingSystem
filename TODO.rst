
=================================================
PANTS TODOs (including known bugs/issues/kludges)
=================================================

Urgent
======

- ** Unit tests are severely incomplete! **
- Fix all the kludgy FIXMEs in the code (see "make fixme" output)
- Fix per-serve/per-weight dichotomy in recipe components (waiting on Ndata work)
- Provide a fixture with some initial basic ingredients and a few recipes so new users can get started ASAP.
- Replace recipe/ and ingredient/ with "landing" page with a list of tags and count of ings for each etc, links to /all/ etc
- Add preparation_loss_factor to ingredient for e.g. peeling and trimming losses (can be half quantity for some vegetables, making them less cost-effective; also required for shopping list quantities etc). Add on product to allow e.g. pre-chopped vs whole veg price comparison

Target comparison (Currently WIP)
=================================

- Util funcs to get current user daily target, and current user diary today/last24 data (done)
- Use on home page summary (done)
- Use to show target on diary breakdown page (done)
- Add daily target comparison on recipe detail page (done)
- Add % to home and clean up ui (done)
- Add % to diary (done)
- Fix new bar charts on recipe detail (ui?)
- Add daily target comparison on ingredient detail page (as for recipe)

NData and calculation DRYing (urgent, blocking)
===============================================

All the nutrition_data properties should be its own class that
generates/caches individual values as required and enforces
access/validation/etc, and does operations like summing and averaging.
This will remove LOTS of almost-identical code across
ingredient/recipe/diary.

- ndata class
- ndata class for ing
- ndata class for rec
- ndata class for diary
- Fix per-serve/per-weight dichotomy in recipe components
- Merge recipe and ingredient handling in diary save() and elsewhere
- Use F()/aggregate/annotate expressions in recipe calcs
- Allow filtering on calculated ndata
- Remove NDATA_ settings cruft
- ndata should handle micronutrients in some generic and graceful way

API / filter
============

- Use django-filter (replace custom tag view handling etc) (work in progress, mostly done)
- Limits and other context in FilterView
- Allow filtering on calculated ndata
- Fix/style form in ing-filter template
- filter recipe, diary as for ings
- API-based frontend? Use DRF API - Don't bother with substatial FE improvements until this is done!

Deploy and Login
================

- Deploy target assuming Heroku - include sub-parts below
- Proper non-admin login/logout pages
- Use login middleware instead of requiring mixins/decorators every view
- 404 template

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

- User-prof-object to hold age, height etc (age required for some physio calcs)
- User preferences for FE (e.g. KJ or calories display, don't show some columns)
- User-custom ing/rec data (Nullable user field; exclude if user!= request.user)
- Fix setting of daily target on target list page

Django Frontend
===============

Note that the Django template frontend is only for personal/debugging
use; "real" clients should be accessing PANTS via an API. Major
frontend improvements should thus be done via other applications that use
that API.

As such most of these range from nice-to-have to wont-fix in priority.

- Clean up templates by using more templatetags
- Handle particular target values set as None gracefully where they are displayed in lists
- 3-part bar chart templatetag for max-min-current target comparison
- Sanity Check page also listing out of date (e.g. nutrition over 2 year (?), price over 6 months) 
- Add chosen target comparison on recipe/ingredient detail pages (for pre/post workout targets etc)
- Consider Daily target comparison as an option on recipe/ingredient list pages
- "tags:" text should be a button that toggles tag-bar visibility on/off
- Diary edit/create/delete forms using generic views too
- Ing list column with recipe count (recursive/nonrecursive), click for recipe list filtered to ing?
- Add Store/Price data to views (Ingredient/Product detail?)
- Bottom nav buttons for convenience
- View-on-site in all admin
- Product has no detail view

Miscellaneous
=============

- Improved bulk import/export facilities in general
- Consider: Deprecate Product by merging price functionality into ProductPrice and making Ingredients recurse to more generic/specific versions? Product concept is underused
- Consider: Move to per-100g instead of per-kg?
- Import from standard sources (i.e. open source nutrition data)
- "Favourite" ings/recs - show first in add-diary-item etc
- Diary nav for historic data - ArchiveView / TodayArchiveView/ DayArchiveView ?
- Recipe is_vegan/is_vegetarian/gluten_free/has_gluten properties - check via ingredient tags
- Invalidate cache of ingredient/recipe/quantity on nutrients change
- Invalidate cache of product/ingredient/etc on price change
- Flatten and/or Crystallize ingredients option on recipe detail view?
- Collections app for free-form showcases of recipes, products and ingredients

