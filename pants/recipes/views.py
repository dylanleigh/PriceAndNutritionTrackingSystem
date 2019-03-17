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

from .models import Recipe, RecipeTag
from targets.models import Target
from ingredients.utils import get_nutrition_limits


class RecipeListView(LoginRequiredMixin, ListView):
   # - Table view - generic macros and cost for each ingredient
   model = Recipe
   queryset = Recipe.objects.filter(tags__isnull=True)
   #queryset = Recipe.objects.all()     # TODO consider limits/paging

   def get_context_data(self, **kwargs):
      context = super(RecipeListView, self).get_context_data(**kwargs)
      context['limits'] = get_nutrition_limits(self.queryset)
      context['alltags'] = RecipeTag.objects.values_list('name', flat=True)
      return context


class RecipeListAllView(LoginRequiredMixin, ListView):
   # - Table view - generic macros and cost for each ingredient
   model = Recipe
   queryset = Recipe.objects.all()

   def get_context_data(self, **kwargs):
      context = super(RecipeListAllView, self).get_context_data(**kwargs)
      context['alltags'] = RecipeTag.objects.values_list('name', flat=True)
      context['limits'] = get_nutrition_limits(self.queryset) #TODO: Too intensive?
      context['listtype'] = 'all'
      return context

class RecipeListByTagView(LoginRequiredMixin, ListView):
   # - Table view filtered by tag
   model = Recipe

   def get_queryset(self):
        self.tag = get_object_or_404(RecipeTag, name=self.args[0])
        return Recipe.objects.filter(tags=self.tag)

   def get_context_data(self, **kwargs):
      context = super(RecipeListByTagView, self).get_context_data(**kwargs)
      context['alltags'] = RecipeTag.objects.values_list('name', flat=True)
      context['limits'] = get_nutrition_limits(self.get_queryset())
      context['tag'] = self.tag
      return context


class RecipeDetailView(LoginRequiredMixin, DetailView):
   model = Recipe

   def get_context_data(self, **kwargs):
      context = super(RecipeDetailView, self).get_context_data(**kwargs)

      # User's current daily target for comparison
      # TODO: Should let user compare to different targets, and scale
      # to maximise something (etc)
      user = self.request.user
      daily_target = Target.get_primary_target(user)
      context.update({'daily_target': daily_target})

      return context

@login_required
def RecipeCSVExportView(request):
   # Create the HttpResponse object with the appropriate CSV header.
   response = HttpResponse(content_type='text/csv')
   response['Content-Disposition'] = 'attachment; filename="pants-recipes.csv"'

   # Use dictionary writer to export nutrition data dicts.
   # Fields are all standard items plus 'name' and calories which should be 1st
   fields = [
      'name',
      'kilocalories_serve',
      'kilocalories',         # Total of recipe
      'protein_per_j',
      'fibre_per_j',
      'protein_per_cost',
      'fibre_per_cost',
      'protein_serve',
      'fibre_serve',
      'carbohydrate_serve',
      'fat_serve',
      'grams_serve',
      'pf_per_j',
      'rank',
   ] + list(settings.NUTRITION_DATA_ITEMS) + [
      'tags',        # TODO: Add ingredient/component names somehow here!
   ]

   writer = csv.DictWriter(
      response,
      fieldnames=fields,
      extrasaction='ignore',     # ignore extra data if present in dicts
   )

   writer.writeheader()
   for rec in Recipe.objects.all().iterator():
      data = rec.nutrition_data
      data['name'] = rec.name
      data['tags'] = rec.tags.values_list('name', flat=True)
      writer.writerow(data)

   return response
