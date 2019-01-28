# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.functional import cached_property
from django.template.defaultfilters import slugify

from ingredients.models import AbstractBaseNutrients
from ingredients.utils import add_nutrition_ratios

not_negative = MinValueValidator(0)


class Target(models.Model):
   """
   Set of nutritional (and cost) targets. This is a user-specific model.
   A minimum and maximum can be entered; each is stored in a related model.

   This is not necessarily a daily target, e.g. it can be used to have
   a target for a week or a single pre-workout or post-workout meal.
   Targets can be marked as a daily target for the user and then
   should be used automatically on diary/home page (TODO)
   """

#          TODO XXX where do targets get compared?
#        - Has to be in the model being examined (e.g. could be
#          recipe, ing, collection...) as it is specific to that
#        - may need multiplier ratio for comparing e.g. single ingr or
#          a meal to # a daily target
#           - if automatic, multiplier ratio should consider what to
#             scale to fit - to calories? protein? cost?

   # Usual stuff  # TODO DRY this out
   name = models.CharField(
      max_length=settings.NAME_LENGTH,
      blank=True,
      null=False,    # Can be left blank if copying name from recipe/ing
   )
   slug = models.CharField(
      max_length=settings.SLUG_LENGTH,
      blank=True,    # Set automatically; null=False still applies
      unique=True,
   )
   description = models.CharField(max_length=settings.DESCR_LENGTH,blank=True)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   # User this target is for - this is required
   user = models.ForeignKey(
      User,
      blank=False,
      null=False,
      on_delete=models.CASCADE,
      related_name='+',       # Prevents User-> related name being created
   )

   # TODO Ideally we would have a subclass of user that links to this
   # TODO We could validate/enforce this in save() but the above is
   # the better long-term solution and fixes other issues e.g. prefs
   daily_target = models.BooleanField(
      help_text="If set, will be used for daily target on diary/home page",
      default=False
   )

   def __str__(self):
      return self.name

   def save(self, *args, **kwargs):
      if not self.slug:
         self.slug = slugify(self.name)      # NOTE will Exception on clash
      super(Target, self).save(*args, **kwargs)

   @staticmethod
   def get_primary_target(user):
      """
      Returns the daily nutrition target for a given user, or none if
      there are none.
      """
      # TODO: 
      try:
         return Target.objects.get(user=user,daily_target=True)
      except ObjectDoesNotExist:
         return None
      except MultipleObjectsReturned:
         # TODO warning message
         return Target.objects.filter(user=user,daily_target=True).first()


class Minimums(AbstractBaseNutrients):
   """
   Contain a set of nutrients + cost that are the minimum for a target.
   Can be None to indicate no lower limit for that item.
   """

   of_target = models.OneToOneField(
      Target,
      on_delete=models.CASCADE,
      related_name='minimum',
   )

   cost = models.DecimalField(
      decimal_places=2,
      max_digits=4,
      null=True,
      blank=True,
      validators=[not_negative],
   )

   # FIXME custom manager and/or class for the generic nutrients data,
   # try to use db rather than going  through properties! Would also
   # reduce repetition of these properties
   @cached_property
   def nutrition_data(self):
      """
      Returns all known nutrition data as a dict including ratios (protein/$, fibre/J etc)
      Return should be the same as in recipe and at least contain NUTRITION_DATA_ITEMS_BASIC
      (Although some may be None)
      """
      data = dict()
      data['cost'] = self.cost      # Basic doesn't include cost; we don't want grams here either
      for k in settings.NUTRITION_DATA_ITEMS_BASIC:
            data[k] = getattr(self,k)
      return add_nutrition_ratios(data) # TODO most of these ratios not useful to target...


class Maximums(AbstractBaseNutrients):
   """
   Contain a set of nutrients + cost that are the maximum for a target.
   Can be None to indicate no lower limit for that item.
   """

   of_target = models.OneToOneField(
      Target,
      on_delete=models.CASCADE,
      related_name='maximum',
   )

   cost = models.DecimalField(
      decimal_places=2,
      max_digits=4,
      null=True,
      blank=True,
      validators=[not_negative],
   )

   # FIXME custom manager and/or class for the generic nutrients data,
   # try to use db rather than going  through properties! Would also
   # reduce repetition of these properties
   @cached_property
   def nutrition_data(self):
      """
      Returns all known nutrition data as a dict including ratios (protein/$, fibre/J etc)
      Return should be the same as in recipe and at least contain NUTRITION_DATA_ITEMS_BASIC
      (Although some may be None)
      """
      data = dict()
      data['cost'] = self.cost      # Basic doesn't include cost; we don't want grams here either
      for k in settings.NUTRITION_DATA_ITEMS_BASIC:
            data[k] = getattr(self,k)
      return add_nutrition_ratios(data) # TODO most of these ratios not useful to target...
