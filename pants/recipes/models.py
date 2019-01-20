# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from django.db import models

from django.conf import settings
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
   # FIXME verify slug rules

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
         self.slug = slugify(self.name)      # FIXME handle clashes
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

   Includes the weight in g or ml. As ingredient/product measure in kg
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

   # FIXME only allow one of these to be active
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
   of_product = models.ForeignKey(
      Product,
      on_delete=models.PROTECT,
      null=True,
      blank=True,
      related_name='used_in',
   )

   # TODO: quantity in in g or ml but nutrients measured per kg or L!
   # TODO: unify g/number of serves
   weight = models.DecimalField(
      decimal_places=3,
      max_digits=7,
      validators=[not_negative],
      help_text="g or ml for ingredients or products; number of serves for recipes"
   )
   note = models.CharField(max_length=settings.DESCR_LENGTH,blank=True)

   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   @cached_property
   def name(self):
      if self.of_ingredient:
         return self.of_ingredient.name
      elif self.of_recipe:
         return self.of_recipe.name
      elif self.of_product:
         return self.of_product.name
      return "Invalid Component!"

   def __str__(self):
      return "%f g %s"%(self.weight, self.name)

   # FIXME MUST have custom clean and save() for validation!

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
         # Special cases
         data['grams']=self.weight  # FIXME or ml...
         if self.of_ingredient.best_price:      # 0 should not be valid
            data['cost'] = self.weight * settings.G_PER_KG * self.of_ingredient.best_price

         # get main macronutrient data directly from ingredient
         for k in settings.NUTRITION_DATA_ITEMS_BASIC:
            val = getattr(self.of_ingredient,k)
            if val is not None:  # Allow 0 to be valid
               data[k] = self.weight * settings.G_PER_KG * val
            else:
               data[k] = None

      # Get data from similar property in recipe
      elif self.of_recipe:
         r_data = self.of_recipe.nutrition_data
         for k in settings.NUTRITION_DATA_ITEMS:
            try:
               # TODO: Amount is per-serve for recipes; consider making per-g?
               # FIXME easier with grams in data
               data[k] = self.weight * r_data["%s_serve"%k]
            except KeyError:
               pass  # Already = None

      # Finally determine desired weights per other weights
      return add_nutrition_ratios(data)
