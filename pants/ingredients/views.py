# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Ingredient, IngredientTag
from .utils import get_nutrition_limits
from targets.models import Target


class IngredientListView(LoginRequiredMixin, ListView):
   # - Table view - generic macros and cost for each ingredient
   model = Ingredient
   queryset = Ingredient.objects.filter(tags__isnull=True)
   #queryset = Ingredient.objects.all()    # XXX NOTE: This now only shows untagged Ings

   def get_context_data(self, **kwargs):
      context = super(IngredientListView, self).get_context_data(**kwargs)
      context['alltags'] = IngredientTag.objects.values_list('name', flat=True)
      context['limits'] = get_nutrition_limits(self.queryset)
      context['listtype'] = 'untagged'
      return context


class IngredientListAllView(LoginRequiredMixin, ListView):
   # - Table view - generic macros and cost for each ingredient
   model = Ingredient
   queryset = Ingredient.objects.all()

   def get_context_data(self, **kwargs):
      context = super(IngredientListAllView, self).get_context_data(**kwargs)
      context['alltags'] = IngredientTag.objects.values_list('name', flat=True)
      context['limits'] = get_nutrition_limits(self.queryset) #TODO: Too intensive?
      context['listtype'] = 'all'
      return context


class IngredientListByTagView(LoginRequiredMixin, ListView):
   # - Table view filtered to a tag
   model = Ingredient

   def get_queryset(self):
        self.tag = get_object_or_404(IngredientTag, name=self.args[0])
        return Ingredient.objects.filter(tags=self.tag)

   def get_context_data(self, **kwargs):
      context = super(IngredientListByTagView, self).get_context_data(**kwargs)
      context['alltags'] = IngredientTag.objects.values_list('name', flat=True)
      context['limits'] = get_nutrition_limits(self.get_queryset())
      context['tag'] = self.tag
      context['listtype'] = 'tag'
      return context


class IngredientDetailView(LoginRequiredMixin, DetailView):
   model = Ingredient

   def get_context_data(self, **kwargs):
       context = super(IngredientDetailView, self).get_context_data(**kwargs)

       # User's current daily target for comparison
       # TODO: Should let user compare to different targets, and scale
       # to maximise something (etc)
       user = self.request.user
       daily_target = Target.get_primary_target(user)
       context.update({'daily_target': daily_target})

       return context

@login_required
def IngredientCSVExportView(request):
   # Create the HttpResponse object with the appropriate CSV header.
   response = HttpResponse(content_type='text/csv')
   response['Content-Disposition'] = 'attachment; filename="pants-ingredients.csv"'

   # FIXME BLOG post on this method!

   # Use dictionary writer to export nutrition data dicts.
   # Fields are all standard items plus 'name' and calories which should be 1st
   fields = [
      'name',
      'kilocalories',
      'protein_per_j',
      'fibre_per_j',
      'protein_per_cost',
      'fibre_per_cost',
      'rank',
      'pf_per_j',
   ] + list(settings.NUTRITION_DATA_ITEMS) + [
      'tags',
   ]
   writer = csv.DictWriter(
      response,
      fieldnames=fields,
      extrasaction='ignore',     # ignore extra data if present in dicts
   )

   writer.writeheader()
   for ing in Ingredient.objects.all().iterator():
      data = ing.nutrition_data
      data['name'] = ing.name
      data['tags'] = ing.tags.values_list('name', flat=True)
      writer.writerow(data)

   return response
