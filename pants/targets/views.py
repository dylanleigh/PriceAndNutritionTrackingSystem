# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from rest_framework import viewsets, permissions

from .models import Target

# Basic class views. Targets are used more from other models to
# compare to.
# TODO templates
from .serializers import TargetSerializer


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

class TargetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows targets to be viewed and altered.
    """
    serializer_class = TargetSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    queryset = Target.objects.none()  # Required for DjangoModelPermissions to get Model

    def get_queryset(self):
       user = self.request.user
       return Target.objects.filter(user=user)
