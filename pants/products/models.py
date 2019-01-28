# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F
from django.template.defaultfilters import slugify
from django.utils.functional import cached_property

from ingredients.models import Ingredient

not_negative = MinValueValidator(0)

# Schema overview:
# Supplier - just a name, maybe tags like online/bulk/etc
# Product - one ingredient, brand string in descr
#         - NOT unique per supplier, per brand, per product etc
#         - optional link to its own macronutrientset, else property
#           to go through to generic
#         - If products changing data - new product? mark older as
#           old-pre-yyyy-mm
# Price   - Unique product,supplier,date - and tracks weight
#         - track historic prices or not?
# ProductNutrient - (Not yet implemented) - override ingredient nutrients

class Supplier(models.Model):
   """
   A place where products may be purchased
   Mainly just an anchor for price
   """

   name = models.CharField(
      max_length=settings.NAME_LENGTH,
      blank=False,
      unique=True,
   )
   slug = models.CharField(
      max_length=settings.SLUG_LENGTH,
      blank=False,
      unique=True,
   )
   description = models.CharField(max_length=settings.DESCR_LENGTH,blank=True)
   # TODO tags ("online", "bulk", "supermarket" etc) ?

   def __str__(self):
      return self.name

   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   @cached_property
   def product_count(self):
      """
      Number of products this supplier has prices listed for
      """
      return Product.objects.filter(price__supplier=self).distinct().count()


class Product(models.Model):
   """
   A branded product; a specific instance of a generic ingredient.

   May have its own nutrients or pass through to the nutrients of its
   parent.

   Different quantities are determined in price; changes in size or
   packaging only are NOT different products.
   """

   class Meta:
      ordering = ["-updated_at"]
      unique_together = ("name", "brand")

   name = models.CharField(
      max_length=settings.NAME_LENGTH,
      blank=False,
      unique=False,   # NOTE name and brand unique together, but name not unique
   )
   slug = models.CharField(
      max_length=settings.SLUG_LENGTH,
      blank=True,    # Set automatically; null=False still applies
      unique=True,
   )
   brand = models.CharField(max_length=settings.NAME_LENGTH,blank=False)

   description = models.CharField(max_length=settings.DESCR_LENGTH,blank=True)
   # TODO tags ("online", "bulk", "supermarket" etc)

   ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
   # TODO ProductNutrients for specific products later

   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   def __str__(self):
      return "%s (%s)"%(self.name,self.brand)

   def save(self, *args, **kwargs):
      if not self.slug:
         self.slug = slugify("%s_%s"%(self.brand, self.name)) # NOTE will Exception on clash
      super(Product, self).save(*args, **kwargs)

   # TODO use manager methods instead of properties with annotations?
   @cached_property
   def lowest_price(self):
      """
      Determines the lowest price per kg of all the most recent prices
      from all suppliers
      """
      prices = self.price_set.annotate(
         price_per_kg = F('price') - F('weight')
      )
      return prices.order_by('price_per_kg').first()


class Price(models.Model):
   """
   Price of a Product at a Supplier on a Date.

   Includes the weight of the product (we don't want to create a bunch
   of extra products when packaging or volume fluctuates!)
   """
   supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
   product = models.ForeignKey(Product, on_delete=models.CASCADE)

   price = models.DecimalField(
      decimal_places=2,
      max_digits=6,
      validators=[not_negative],
   )
   weight = models.DecimalField(
      decimal_places=3,
      max_digits=6,
      validators=[not_negative],
   )

   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   def __str__(self):
      return "%s@%s $%f/kg"%(self.product,self.supplier,self.per_kg)

   @cached_property
   def per_kg(self):
      """
      Returns price per kg - for display use
      """
      try:
         return self.price/self.weight
      except TypeError:
         return None
