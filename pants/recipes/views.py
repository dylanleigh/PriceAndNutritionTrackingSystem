# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from rest_framework import viewsets, permissions

from .models import Recipe, RecipeTag
from .serializers import RecipeListSerializer, RecipeNestedSerializer, RecipeTagSerializer
from targets.models import Target
from ingredients.utils import get_nutrition_limits, owner_or_global


class RecipeListView(LoginRequiredMixin, ListView):
   # - Table view - default is to show untagged recipes
   model = Recipe

   def get_queryset(self):
      user=self.request.user
      return owner_or_global(Recipe, user).filter(Q(tags__isnull=True))

   def get_context_data(self, **kwargs):
      context = super(RecipeListView, self).get_context_data(**kwargs)
      context['limits'] = get_nutrition_limits(self.get_queryset())
      context['alltags'] = RecipeTag.objects.values_list('name', flat=True)
      return context


class RecipeListAllView(LoginRequiredMixin, ListView):
   # - Table view - generic macros and cost for each ingredient
   # TODO Consider rate limiting due to server time cost
   model = Recipe

   def get_queryset(self):
      user=self.request.user
      return owner_or_global(Recipe, user)

   def get_context_data(self, **kwargs):
      context = super(RecipeListAllView, self).get_context_data(**kwargs)
      context['alltags'] = RecipeTag.objects.values_list('name', flat=True)
      context['limits'] = get_nutrition_limits(self.get_queryset()) #FIXME: Too CPU intensive?
      context['listtype'] = 'all'
      return context

class RecipeListByTagView(LoginRequiredMixin, ListView):
   # - Table view filtered by tag
   model = Recipe

   def get_queryset(self):
        self.tag = get_object_or_404(RecipeTag, name=self.args[0])
        user=self.request.user
        return owner_or_global(Recipe, user).filter(tags=self.tag)

   def get_context_data(self, **kwargs):
      context = super(RecipeListByTagView, self).get_context_data(**kwargs)
      context['alltags'] = RecipeTag.objects.values_list('name', flat=True)
      context['limits'] = get_nutrition_limits(self.get_queryset())
      context['tag'] = self.tag
      return context


class RecipeDetailView(LoginRequiredMixin, DetailView):
   model = Recipe

   def get_queryset(self):
      # required for access control (can't view other users objects)
      user=self.request.user
      return owner_or_global(Recipe, user)

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
      'cost_serve',
      'cost_per_kg',
      'pf_per_j',
      'rank',
   ] + list(settings.NUTRITION_DATA_ITEMS) + [
      'tags',        # TODO: Add a column with ingredient/component names to export?
   ]

   writer = csv.DictWriter(
      response,
      fieldnames=fields,
      extrasaction='ignore',     # ignore extra data if present in dicts
   )

   writer.writeheader()
   user=request.user
   for rec in owner_or_global(Recipe, user).iterator():
      data = rec.nutrition_data
      data['name'] = rec.name
      data['tags'] = rec.tags.values_list('name', flat=True)
      writer.writerow(data)

   return response

class RecipeViewSet(viewsets.ModelViewSet):
   """
   API endpoint that allows Recipes to be viewed and user's ones to be altered.
   """
   permission_classes = [permissions.DjangoModelPermissions]
   queryset = Recipe.objects.none()  # Required for DjangoModelPermissions to get Model

   # To enable searching
   search_fields = ['name']

   # Don't show components in list, but use serializer with nested
   # components for other actions (get/put/etc)
   def get_serializer_class(self):
      if self.action:
         if self.action == 'list':
            return RecipeListSerializer
      return RecipeNestedSerializer

   def get_queryset(self):
      return owner_or_global(Recipe, self.request.user)

class RecipeNestedViewSet(viewsets.ModelViewSet):
   """
   API endpoint for getting a FULL view of the recipe, including components
   @todo I added this so that I could get components, but perhaps if we aren't allowing listing recipes and components
      together on purpose I should have added a Components api directly? But again that would only get used for getting
      recipe components, since you can update components with the regular view set. Maybe just add a "?include_components=true"
      query string option to other viewset?
   """
   permission_classes = [permissions.DjangoModelPermissions]
   queryset = Recipe.objects.none()  # Required for DjangoModelPermissions to get Model

   def get_serializer_class(self):
      return RecipeNestedSerializer

   def get_queryset(self):
      return owner_or_global(Recipe, self.request.user)

class RecipeTagViewSet(viewsets.ModelViewSet):
   """
   API Endpoint for viewing and editing Recipe Tags
   """
   queryset = RecipeTag.objects.all()

   def get_serializer_class(self):
      return RecipeTagSerializer


