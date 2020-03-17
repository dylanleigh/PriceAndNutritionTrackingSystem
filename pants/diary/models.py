from datetime import timedelta, datetime, time
from collections import defaultdict
from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.utils.functional import cached_property
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

from ingredients.models import AbstractBaseNutrients,Ingredient
from recipes.models import Recipe
from products.models import Product
from ingredients.utils import add_nutrition_ratios


# TODO utils?
not_negative = MinValueValidator(0)


# Per-User diary of food eaten

# MODELS OVERVIEW

# DiaryFood  - a food at a given datetime
#            - inherits nutritionABC
#            - source of data can be LOADED from ing/rec or just entered in by user
#              - effectively nutrition data crystallized when saving from ing/rec
#            - viewing by 

# TODO: Base off other apps? "Exercise" "Biometrics"?
# DiaryExercise - record exercise session TODO
# DiaryStat - record weight or other biomentric data - resting heart rate, blood pressure etc TODO

# VIEWS OVERVIEW

# NOTE XXX must always filter all Diary views to just the logged in user's stuff!

# More TODO:
# Main List View - Combined Meal and Food and Exercise - just Food for now
#                - Meal should be explodable to individual foods
#                - Time scale should fan out to show values over 24hr etc - in progress
#                - Separate view for per-hour calculations?
# Detail Views for each model
#                - DiaryFood detail view includes forms to edit or update etc...
#                - "Clone to now"
#                - etc...

class DiaryFood(AbstractBaseNutrients):
   """
   Basic entry for something consumed in diary.
   Contains it's own nutrient values - although these may be loaded
   from a Recipe/Ingredient and we maintain the link they are actually
   independent.
   """

   class Meta:
      ordering = ["-start_time"]

   name = models.CharField(
      max_length=settings.NAME_LENGTH,
      blank=True,
      null=False,    # Can be left blank if copying name from recipe/ing
      help_text="Name of the entry i.e. description of the food",
   )
   # Time starting to eat
   start_time = models.DateTimeField(
      blank=False,
      null=False,
      help_text="Time meal started",
   )
   # User this diary entry is for - this is required
   user = models.ForeignKey(
      User,
      blank=False,
      null=False,
      on_delete=models.CASCADE,
      related_name='+',       # Prevents User-> related name being created
   )

   cost = models.DecimalField(
      decimal_places=2,
      max_digits=4,
      null=True,     # Can be empty if self-entered nutritional info
      blank=True,
      validators=[not_negative],
      help_text="WARNING: Only for once-off items! Cost and nutrients will be overwritten by ingredients or recipes"
   )

   # Possibly linked to a Recipe or Ingredient, or primary data if
   # self-entered diary entry
   weight = models.DecimalField(
      decimal_places=3,
      max_digits=7,     # xxxx.xxx g
      null=True,     # Can be empty if self-entered nutritional info
      blank=True,
      validators=[not_negative],
      help_text="g or ml for ingredients or products; WARNING: using servings will OVERWRITE this value!"
   )

   servings = models.DecimalField(
      decimal_places=2,
      max_digits=4,     # xx.xx servings
      null=True,
      blank=True,
      validators=[not_negative],
      help_text="number of servings for recipes or ingredients - WARNING: entering this will overwrite weight & cost automatically"
   )

   # FIXME only allow one of these to be active
   of_ingredient = models.ForeignKey(
      Ingredient,
      on_delete=models.CASCADE,
      null=True,
      blank=True,
      related_name='consumed',
   )
   of_recipe = models.ForeignKey(
      Recipe,
      on_delete=models.CASCADE,
      null=True,
      blank=True,
      related_name='consumed',
   )
   of_product = models.ForeignKey(
      Product,
      on_delete=models.CASCADE,
      null=True,
      blank=True,
      related_name='consumed',
   )

   def __str__(self):
      return "%s: %s"%(self.start_time,self.name)

   def clean(self):
      # If recipe is specified, we must have "servings" or "weight"
      # (and servings will be reversed from the weight if required!)

      # If ingredient is specified, we must have "weight" or both
      # "servings" and the ingredient must have a grams-per-serve.

      # If this is a manual entry, there is no special validation
      # required (some fields will just be unused in internal
      # calculaion but are kept for user record keeping)

      if self.of_recipe:
         if not (self.servings or self.weight):
            raise ValidationError('When using a recipe, must specify weight or servings')
      elif self.of_ingredient:
         if not (self.servings or self.weight):
            raise ValidationError('Must specify weight of Ingredient (or servings if set on Ingredient)')
         elif self.servings and (not self.of_ingredient.serving):
            raise ValidationError('Ingredient does not have servings listed - use raw weight instead')

      super(DiaryFood, self).clean()

   def save(self, *args, **kwargs):
      # copy (scaled) nutrient data from source and name if name is empty

      # TODO: This does not copy all possible data (e.g. saturated
      # fat, sodium) from ingredients

      # FIXME: recipe/ingredient can be treated the same soon!
      # source = self.of_recipe or self.of_ingredient or self.of_product:
      #  if source:
      #     source.nutrition_data ...
      # TODO: merge component logic the same way as recipe/ingredient here

      if self.of_recipe:
         ndata = self.of_recipe.nutrition_data

         # Must get correct weight & servings first, to scale the rest
         if self.servings:
            self.weight = ndata['grams_serve'] * self.servings   # servings overrides weight
         else:
            # clean() ensures weight exists if servings doesn't
            self.servings = self.weight / ndata['grams_serve']

         # Get basic items plus cost - use per-serve data
         for k in settings.NUTRITION_DATA_ITEMS_BASIC:
            try:
               setattr(self, k, self.servings * ndata["%s_serve"%k])
            except (KeyError,TypeError):
               setattr(self, k, None)
         try:
            if ndata['cost_serve']:
               self.cost = self.servings * ndata['cost_serve'] # cost not included in _BASIC
         except:
            # TODO: Warn user that this recipe has no cost data - not critical
            pass

         if not self.name:  # use name from source unless overridden
            self.name = self.of_recipe.name

      elif self.of_ingredient:
         ndata = self.of_ingredient.nutrition_data

         # FIXME: can merge all of this above when recipe per-kg and ing per-serving ndata unified!

         if self.servings and self.of_ingredient.serving:   # don't trust ndata['grams_serve']
            self.weight = self.of_ingredient.serving * self.servings   # servings overrides weight
         elif self.weight is None: # no serving - we must have weight!
            # validation error should be raised earlier (unless this was created in code)
            raise ValueError('Ingredient has no serving - must explicitly specify weight')

         for k in settings.NUTRITION_DATA_ITEMS_BASIC:
            val = getattr(self.of_ingredient, k)
            if val is not None:  # Allow 0 to be valid
               setattr(self, k, self.weight * settings.G_PER_KG * val)
            else:
               setattr(self, k, None)
            if ndata['cost']:
               self.cost = self.weight * settings.G_PER_KG * ndata['cost'] # cost not included in _BASIC
         if not self.name:  # use name from source unless overridden
            self.name = self.of_ingredient.name

      super(DiaryFood, self).save(*args, **kwargs)

   @cached_property
   def nutrition_data(self):
      """
      Returns cost/protein/fibre/kj of this component
      (multiplying by weight and doing any kg->g conversion required),
      plus protein and fibre per J and dollar and other ratios
      """

      data = dict()
      data['cost']=self.cost # required for some ratios/ranks

      data['grams']=self.weight

      for k in settings.NUTRITION_DATA_ITEMS_BASIC:
         data[k] = getattr(self,k)

      return add_nutrition_ratios(data)

   @staticmethod
   def get_diary_aggs(user, times):
      """
      Given an ordered iterative of start-end time pairs, return an
      ordered dict of tuples; each contains (filtered to the user):
         [0] The start time (as passed)
         [1] The end time (as passed)
         [2] The list of diary items within those times
         [3] The totals of those diary items, as a dict of nutition
             data (protein, kilojoules, etc)

      NOTE: This function is to be the authoritative/definitive way of
      getting totals and aggregate diary data, and should be responsible for
      doing any analysis we generally want done like BLG/GLY/etc.
      """
      return None  # TODO this should maybe replace below; profile
                   # both as this may be less efficient at handling
                   # the overlapping periods.

                   # TODO Consider a way to allow overlapping periods to be
                   # returned separately as lists but together as
                   # aggregates, just like below. This would be *fantastic*
                   # for having a detailed breakdown of last hour/2
                   # hours/4 hours etc for exercise nutrition.

                   # TODO A flag to not bother with the objects in
                   # cases where we only care about the totals (home
                   # page, widgets etc)

   @staticmethod
   def get_recent_diary_aggs(user):
      """
      Return a dict containing (for the given user):
         'today_objects': List of all the diary entries from the current calendar day
         'last24_objects' All the diary entries from the last 24 hours
                          (except those in the above)
         'lastday_objects' All the diary entries from the previous calendar day
                           (except those in the above)

         'today_total' The summed or otherwise aggregated (e.g. ratios)
                       nutrition data for the current calendar day, as a dict.
         'last24_total' The aggregated nutrition data for the last 24
            hours (not today)
         'lastday_total' The aggregated nutrition data for the previous calendar day,
                         INCLUDING the last-24-hour items that are OLDER than today.
      """

      # NOTE XXX: BELOW CODE IS DEPRECATED in favour of
      # get_diary_aggs(), but when that is finished we still
      # want to profile this approach as it may be faster.

      # TODO: A lot of this maybe should be done in the frontend, we
      # should just pass it a list of relevant items. Consider what we
      # want to be authoritative about any analysis of the data.

      # We want to split the view into overlapping parts, with subtotals:
      # - 1- Items in the current calendar day (with total)
      # - 2- Items in the last 24 hours but previous day
      #   -  (the displayed total includes #1)
      # - 3- Items in the previous calendar day
      #   -  (displayed total includes #2, but not #1)

      context = {}

      # Boundaries of the 3 lists
      now = timezone.now()
      naivenow = datetime.now() # For "today" calc only
      today = now-timedelta(
         hours=naivenow.hour,
         minutes=naivenow.minute,         # XXX: Just doing .replace() causes TZ issues
         seconds=naivenow.second,
      )
      last24 = now-timedelta(days=1)
      lastday = today-timedelta(days=1)

      # our 3 lists and subtotals
      # note as they are nutritiondata our subtotals are a dict of NUTRITION_ITEMS keys
      today_df = list()
      last24_df = list()
      lastday_df = list()
      today_total = defaultdict(Decimal)
      last24_total = defaultdict(Decimal)
      lastday_total = defaultdict(Decimal)

      qset_all = DiaryFood.objects.filter(
         user=user,
         start_time__gte=lastday,
         start_time__lte=now,       # Ignore anything in the future...
      )


      # There is likely a more efficient way to do this but for
      # now we are going to:
      #     - Iterate through each item since the last calendar day
      #     - Add it to a list corresponding to period 1/2/3
      #     - Add it's nutrition data to a subtotal dict for 1/2/3
      #        - also get combined totals for #3 into #4, #2 into #3 and #1 into #2.
      # This shouldn't be too bad as the total number of things a person
      # will enter in the diary shouldn't be very high, if using recipes etc.

      for df in qset_all.iterator():
         ndata = df.nutrition_data
         if df.start_time >= today:
            today_df.append(df)
            for k in settings.NUTRITION_DATA_ITEMS:
               if ndata[k]:
                  today_total[k] += ndata[k]
         elif df.start_time >= last24:
            last24_df.append(df)
            for k in settings.NUTRITION_DATA_ITEMS:
               if ndata[k]:
                  last24_total[k] += ndata[k]
         else:
            lastday_df.append(df)
            for k in settings.NUTRITION_DATA_ITEMS:
               if ndata[k]:
                  lastday_total[k] += ndata[k]

      # Finally add everything to context dict and return it
      context['today_objects']=today_df
      context['last24_objects']=last24_df
      context['lastday_objects']=lastday_df

      # XXX: MUST create the xx_sum dicts first before doing ratios,
      # as we want the ratio of the sum and NOT to sum the ratios
      context['last24_sum']=add_nutrition_ratios(
         { k: today_total.get(k, 0) + last24_total.get(k, 0) for k in set(today_total) | set(last24_total) }
      )
      context['lastday_sum']=add_nutrition_ratios(
         { k: lastday_total.get(k, 0) + last24_total.get(k, 0) for k in set(lastday_total) | set(last24_total) }
      )

      # Now can add ratios for the totals of each list
      context['today_total']=add_nutrition_ratios(today_total)
      context['last24_total']=add_nutrition_ratios(last24_total)
      context['lastday_total']=add_nutrition_ratios(lastday_total)

      # Exact timestamps we used to generate all this
      context['ref_now']=now
      context['ref_today']=today
      context['ref_last24']=last24
      context['ref_lastday']=lastday

      return context
