# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product


class ProductListView(LoginRequiredMixin, ListView):
   model = Product
   queryset = Product.objects.order_by('-updated_at')


   def get_context_data(self, **kwargs):
      context = super(ProductListView, self).get_context_data(**kwargs)
      # TODO cost data?
      return context

