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

from .models import Ingredient, IngredientTag
from .serializers import IngredientSerializer, IngredientTagSerializer
from .utils import get_nutrition_limits, owner_or_global
from targets.models import Target


class IngredientListView(LoginRequiredMixin, ListView):
    # - Default Table view - generic macros and cost for untagged ingredients
    model = Ingredient

    def get_queryset(self):
        user = self.request.user
        return owner_or_global(Ingredient, user).filter(Q(tags__isnull=True))

    def get_context_data(self, **kwargs):
        context = super(IngredientListView, self).get_context_data(**kwargs)
        context['alltags'] = IngredientTag.objects.values_list('name', flat=True)
        context['limits'] = get_nutrition_limits(self.get_queryset())
        context['listtype'] = 'untagged'
        return context


class IngredientListAllView(LoginRequiredMixin, ListView):
    # - List of all ingredients (all tags)
    # TODO Consider rate limiting due to server time cost
    model = Ingredient

    def get_queryset(self):
        user = self.request.user
        return owner_or_global(Ingredient, user)

    def get_context_data(self, **kwargs):
        context = super(IngredientListAllView, self).get_context_data(**kwargs)
        context['alltags'] = IngredientTag.objects.values_list('name', flat=True)
        context['limits'] = get_nutrition_limits(self.get_queryset())  # TODO: Too intensive?
        context['listtype'] = 'all'
        return context


class IngredientListByTagView(LoginRequiredMixin, ListView):
    # - Table view filtered to a tag
    model = Ingredient

    def get_queryset(self):
        user = self.request.user
        self.tag = get_object_or_404(IngredientTag, name=self.args[0])
        return owner_or_global(Ingredient, user).filter(tags=self.tag)

    def get_context_data(self, **kwargs):
        context = super(IngredientListByTagView, self).get_context_data(**kwargs)
        context['alltags'] = IngredientTag.objects.values_list('name', flat=True)
        context['limits'] = get_nutrition_limits(self.get_queryset())
        context['tag'] = self.tag
        context['listtype'] = 'tag'
        return context


class IngredientDetailView(LoginRequiredMixin, DetailView):
    model = Ingredient

    def get_queryset(self):
        user = self.request.user  # Required for detail to limit to user's own objects
        return owner_or_global(Ingredient, user)

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
        extrasaction='ignore',  # ignore extra data if present in dicts
    )

    writer.writeheader()
    user = request.user
    for ing in owner_or_global(Ingredient, user).iterator():
        data = ing.nutrition_data
        data['name'] = ing.name
        data['tags'] = ing.tags.values_list('name', flat=True)
        writer.writerow(data)

    return response


class IngredientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Ingredients to be viewed and user's ingredients to be altered.
    """
    serializer_class = IngredientSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    queryset = Ingredient.objects.none()  # Required for DjangoModelPermissions to get Model

    search_fields = ['name']

    def get_queryset(self):
        user = self.request.user
        return owner_or_global(Ingredient, user)  # FIXME filter to global (user null) and user objects


class IngredientTagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows IngredientTags to be viewed and what Ingredients the tags belong to to be altered
    """
    serializer_class = IngredientTagSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    queryset = IngredientTag.objects.all()