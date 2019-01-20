# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Target

# Basic class views. Targets are used more from other models to
# compare to.
# TODO templates

class TargetListView(LoginRequiredMixin, ListView):
   model = Target

   def get_context_data(self, **kwargs):
      context = super(TargetListView, self).get_context_data(**kwargs)
      return context

class TargetDetailView(LoginRequiredMixin, DetailView):
   model = Target

   def get_context_data(self, **kwargs):
       context = super(IngredientDetailView, self).get_context_data(**kwargs)
       return context

