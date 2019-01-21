
=================================================
PANTS TODOs (including known bugs/issues/kludges)
=================================================

Urgent
======

- ** Unit tests are severely incomplete! **
- Fix all the kludgy FIXMEs in the code (see "make fixme" output)

Target comparison (Currently WIP)
=================================

- Util funcs to get current user daily target, and current user diary today/last24 data (done, used on home page)
- Use to show target on diary breakdown page (done, just last calendar day so far)

NData and calculation DRYing
============================

- all the nutrition_data properties should be its own class that generates/caches individual values as required and enforces access/validation/etc, and does operations like summing and averaging (would remove LOTS of almost-identical code across ingredient/recipe/diary)
- Fix per-serve/per-weight dichotomy in recipe components
- Merge recipe and ingredient handling in diary save() and elsewhere
- Allow filtering on calculated ndata
- Remove NDATA_ settings cruft
- ndata should handle micronutrients in some generic way

API / filter (Currently WIP)
============================

- Use django-filter (replace custom tag view handling etc) (work in progress, mostly done)
- Limits and other context in FilterView
- Allow filtering on calculated ndata
- Fix/style form in ing-filter template
- filter recipe, diary as for ings
- API-based frontend? Use DRF API - Don't bother with substatial FE improvements until this is done!

Deploy tasks
============

- Deploy target assuming Heroku - include sub-parts below
- Proper non-admin login page
- Use login middleware instead of requiring mixins/decorators every view
- logout working
- 404 template

Miscellaneous
=============

- Replace recipe/ and ingredient/ with "landing" page with a list of tags and count of ings for each etc
- Add preparation_loss_factor to ingredient for e.g. peeling and trimming losses (can be half quantity for some vegetables, making them less cost-effective; also required for shopping list quantities etc)
- Add daily target comparison on recipe/ingredient detail pages
- Add daily target comparison as an option on recipe/ingredient list pages
- View-on-site in all admin
- "Favourite" (integer?) - use to sort, then updated-at
- Multilayer navigation, put little-used components in a misc section
- Flat (view all) view for Ing/Rec
- Diary nav for historic data - ArchiveView / TodayArchiveView/ DayArchiveView ?
- Diary edit/create/delete forms using generic views too
- admin command or buttons on DE list view to export ALL ing data and ALL recipe data as big tables
- Consider: Move to per-100g instead of per-kg?
- Consider: Deprecate Product by merging price functionality into ProductPrice and making Ingredients recurse to more generic/specific versions? Product concept is underused
- Ing list column with recipe count (recursive/nonrecursive), click for recipe list filtered to ing?
- Recipe is_vegan/is_vegetarian/gluten_free/has_gluten properties - check via ingredient tags
- Invalidate cache of ingredient/recipe/quantity on nutrients change
- Invalidate cache of product/ingredient/etc on price change
- Add missing data on Products list view
- Add Store/Price data to views (Ingredient/Product detail?)
- "tags:" text should be a button that toggles tag-bar visibility on/off
- Flatten and/or Crystallize ingredients option on recipe detail view?
- Collections app for free-form showcases of recipes, products and ingredients
- Bottom nav buttons
- Sanity Check page also listing out of date (e.g. nutrition over a year (?), price over a quarter) 
- User preferences (e.g. KJ or calories display, don't show some columns)
- User-custom data (consider split DB vs duped tables?)

