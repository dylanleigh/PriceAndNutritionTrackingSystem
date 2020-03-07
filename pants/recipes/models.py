# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from django.db import models

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.functional import cached_property

from ingredients.models import Ingredient
from ingredients.utils import add_nutrition_ratios
from products.models import Product

# TODO utils?
not_negative = MinValueValidator(0)

# Schema overview:
# Recipe - A recipe made from some number of Ingredients
# Quantity - Through-model between Ingredient and Recipe (with weight in g / ml)
# RecipeGroup - A set of one or more recipes added together to e.g.
#               show a daily diet or allow easy comparison between them
# RecipeNutrient - (Not yet implemented) - override ingredient nutrients

class RecipeTag(models.Model):
   """
   Tags for recipes - just a name.
   Name follows slug rules (only lowercase, hyphens and underscores)
   e.g. stew, baked, gluten-free, no_cook etc
   """
   verbose_name_plural = "Recipe Tags"

   name = models.SlugField(
      max_length=settings.TAG_LENGTH,
      blank=False,
      unique=True,
   )

   description = models.CharField(max_length=settings.DESCR_LENGTH,blank=True)

   def __str__(self):
      return self.name


class Recipe(models.Model):
   """
   A recipe made from some number of Ingredients, with a method stored for
   display (not relevant to PANTS itself).
   """

   class Meta:
        ordering = ["-updated_at"]

   name = models.CharField(
      max_length=settings.NAME_LENGTH,
      blank=False,
      unique=True,
   )
   slug = models.CharField(
      max_length=settings.SLUG_LENGTH,
      blank=True,    # Set automatically; null=False still applies
      unique=True,
   )
   description = models.CharField(max_length=settings.DESCR_LENGTH,blank=True)

   tags = models.ManyToManyField(RecipeTag, blank=True)

   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   last_tested = models.DateTimeField(
      blank=True,
      null=True,
      help_text="When this recipe was last made to check it works, and it did",
   )
   # FIXME Add arbitrary "flags" like tags for this?
   # TODO Options to handle flagging for testing
   #  Statuses: 
   #     NULL (not specified),
   #     testing not required,      # "needless"
   #     required but not yet done, # "required"
   #     tried but not working ,    # "alpha"
   #     works but has issues,      # "beta"
   #     tested working 100%        # "verified"
   #     not working and abandoned for now # "deprecated"
   # TODO Auto when added to diary? "Last used"?
   # TODO How to handle testing when a recipe is working well then
   #      alterations are made to it? Can't flag if (last_tested <
   #      updated_at) as updated_at will be updated when test date is

   serves = models.DecimalField(
      decimal_places=2,
      max_digits=4,
      validators=[not_negative],
   )

   method = models.TextField(blank=True)

   def __str__(self):
      return self.name

   def save(self, *args, **kwargs):
      if not self.slug:
         self.slug = slugify(self.name)      # NOTE will Exception on clash
      super(Recipe, self).save(*args, **kwargs)

   # TODO: How much of this logic should be in the template or client side?
   @cached_property
   def nutrition_data(self):
      """
      Returns cost/protein/fibre/kj of total and one serve of the recipe,
      plus protein and fibre per J and dollar etc.

      Returns None for a value (and any dependent values) if ANY
      ingredients are missing that value (e.g. missing Fibre or Price data)
      """

      # init
      data = dict()
      for k in settings.NUTRITION_DATA_ITEMS:
         data[k] = 0
      # Sum cost and basic macros - if any missing, make the sum None
      for c in self.components.iterator(): 
         comp_data = c.nutrition_data
         for key in settings.NUTRITION_DATA_ITEMS:
            if data[key] is not None:
               if comp_data[key] is None:
                  data[key] = None
               else:
                  data[key] += comp_data[key]

      # For all valid values currently there, include per-serve data
      serves = self.serves if self.serves else 1
      keys = dict.fromkeys(data)
      for k in keys:
         if data[k] is not None:
            data["%s_serve"%k]=data[k]/serves

      # Convert KJ to Kcal/serve
      if 'kilojoules_serve' in data and data['kilojoules_serve'] > 0:
         data['kilocalories_serve']=data['kilojoules_serve'] / settings.KJ_PER_KCAL

      # Finally determine desired weights per other weights
      return add_nutrition_ratios(data)

   # NOTE: This is deprecated, only required for dictsort being flaky
   @cached_property
   def sort_rank(self):
      '''
      Returns the rank from nutrition data, as an integer.
      Returns 0 if there is no rank.
      Used for sorting things that can't sort floating point numbers
      '''
      try:
         return self.nutrition_data['rank']
      except:
         return 0

   @cached_property
   def used_in_recipes(self):
      """
      Returns a dict (slug->name) of Recipes that this ingredient
      is a part of (including child recipes)

      Iterations/queries are proportional to the number of generations
      (not the raw number of recipes).
      """
      values = {}
      rqset = Recipe.objects.filter(components__of_recipe__pk=self.pk)

      while rqset.count():    # until no more child recipes
         values.update(rqset.values_list('slug','name'))   # Add to return dict
         rqset = Recipe.objects.filter(components__of_recipe__in=rqset) # Recurse

      return values


class Component(models.Model):
   """
   Component of a recipe; could be a (generic) ingredient, a
   (specific) product or another recipe.

   Includes the weight in grams. As ingredient/product measure in kg
   or L, Component is responsible for the converstion of units.
   TODO: Unify units - should all be g or kg.

   Caches nutrition data so it can be queried generically regardless
   of the type of component.
   """

   in_recipe = models.ForeignKey(
      Recipe,
      on_delete=models.CASCADE,
      related_name='components',
   )

   # NOTE one and only one of these must be active (validated)
   of_ingredient = models.ForeignKey(
      Ingredient,
      on_delete=models.PROTECT,
      null=True,
      blank=True,
      related_name='used_in',
   )
   of_recipe = models.ForeignKey(
      Recipe,
      on_delete=models.PROTECT,
      null=True,
      blank=True,
      related_name='used_in',
   )

   # NOTE one and only one of these must be active (validated)
   servings = models.DecimalField(
      decimal_places=2,
      max_digits=5,
      validators=[not_negative],
      help_text="WARNING: Overrides weight if used!",
      null=True,
      blank=True,
   )
   weight = models.DecimalField(
      decimal_places=3,
      max_digits=7,
      validators=[not_negative],
      help_text="In grams; WARNING will be overridden by servings if that is used",
      null=True,
      blank=True,
   )
   # TODO: weight in in g but nutrients measured per kg!

   note = models.CharField(max_length=settings.DESCR_LENGTH,blank=True)

   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   def clean(self):
      """
      Validate component - we must have either a recipe or an
      ingredient (but not both), specified in servings or in grams
      (but not both), and if servings are used on an ingredient it
      must have that setting.
      """

      if self.of_ingredient:
         if self.of_recipe:
            raise ValidationError('Must specify either recipe or ingredient, but not both')
         elif self.servings and (not self.of_ingredient.serving):
            raise ValidationError('That ingredient does not have servings listed - use raw weight instead')
      else:
         if not self.of_recipe:
            raise ValidationError('Must specify either a recipe or ingredient for this component')

      if (self.servings and self.weight):
         raise ValidationError('Must specify either servings or weight, not both')
      elif not (self.servings or self.weight):
         raise ValidationError('Must specify the amount of either weight or servings')

      super(Component, self).clean()

   @cached_property
   def quantity(self):
      """
      Returns the weight or number of servings of this component, whichever is applicable.
      """
      return self.weight if self.weight else self.servings

   @cached_property
   def name(self):
      if self.of_ingredient:
         return self.of_ingredient.name
      elif self.of_recipe:
         return self.of_recipe.name
      return "Invalid Component!"

   def __str__(self):
      return "%f g %s"%(self.quantity, self.name)

   @cached_property
   def nutrition_data(self):
      """
      Returns cost/protein/fibre/kj of this component
      (multiplying by weight and doing any kg->g conversion required),
      plus protein and fibre per J and dollar etc.

      Returns None for a value if that value is missing from the source object.
      """
      # init TODO consider dependent values here too?
      data = dict()
      for k in settings.NUTRITION_DATA_ITEMS:
         data[k] = None

      # Get ingredient->nutrients data if ingredient
      # NOTE: Requires conversion kg to grams
      if self.of_ingredient:
         weight = self.weight or self.of_ingredient.serving * self.servings
         # Special cases
         data['grams']=weight
         if self.of_ingredient.best_price:      # 0 should not be valid
            data['cost'] = weight * settings.G_PER_KG * self.of_ingredient.best_price

         # get main macronutrient data directly from ingredient
         for k in settings.NUTRITION_DATA_ITEMS_BASIC:
            val = getattr(self.of_ingredient,k)
            if val is not None:  # Allow 0 to be valid
               data[k] = weight * settings.G_PER_KG * val
            else:
               data[k] = None

      # Get data from similar property in recipe
      elif self.of_recipe:
         r_data = self.of_recipe.nutrition_data
         if self.servings:
            for k in settings.NUTRITION_DATA_ITEMS:
               try:
                  data[k] = self.servings* r_data["%s_serve"%k]
               except KeyError:
                  pass  # Already = None
         else: # using self.weight     # TODO simplify weight calc and merge if possible
            grams_serve = r_data["grams_serve"]
            for k in settings.NUTRITION_DATA_ITEMS:
               try:
                  data[k] = self.weight * r_data["%s_serve"%k]/grams_serve
               except KeyError:
                  pass  # Already = None

      # Finally determine desired weights per other weights
      return add_nutrition_ratios(data)
