# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Ingredient, IngredientTag

class IngredientAdmin(admin.ModelAdmin):
   view_on_site = True

   save_as = True    # Allow cloning items by replacing "save and add another"

   list_display = ('name', 'updated_at', 'product_count')
   readonly_fields = ('created_at','updated_at','lowest_price','product_count')
   search_fields = ['name', 'description']

   fieldsets = (
      (None, {
         'fields': (('name', 'description'), ('serving',)),
      }),
      ('Tags', {
            'classes': ('collapse',),
            'fields': (
               ('tags',),
            )
      }),
      ('Nutrients (per KG)', {
         'fields': (
            'kilojoules',
            'protein',
            'fat',
            'saturatedfat',
            'carbohydrate',
            'sugar',
            'fibre',
            'sodium',
         )
      }),
      ('Internal Properties', {
            'classes': ('collapse',),
            'fields': (
               ('created_at','updated_at'),
               ('slug',),
               ('lowest_price',),
            )
      }),
   )

admin.site.register(Ingredient,IngredientAdmin)
admin.site.register(IngredientTag)
