# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Ingredient, IngredientTag
from products.models import Price

class PriceInlineAdmin(admin.TabularInline):
   model = Price
   readonly_fields = ('per_kg', 'created_at','updated_at')

class IngredientAdmin(admin.ModelAdmin):
   view_on_site = True

   save_as = True    # Allow cloning items by replacing "save and add another"

   list_display = ('name', 'updated_at', 'price_count')
   readonly_fields = ('created_at','updated_at','lowest_price','price_count')
   search_fields = ['name', 'description']

   inlines = [PriceInlineAdmin]

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
         'classes': ('collapse',),
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
