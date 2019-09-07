# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Recipe, Component, RecipeTag

admin.site.register(RecipeTag)

#admin.site.register(Component) # rm in favour of inline only?
# TODO: might be worth having a custom non-inline one for internal + properties
# as component has a lot of functionality buried away behind recipe

class ComponentInlineAdmin(admin.TabularInline):
   model = Component
   fk_name = "in_recipe"
   fields = (
      ('weight', 'note',),
      ('of_ingredient', 'of_recipe',),
      # TODO: Deprecate product? ('of_ingredient', 'of_recipe', 'of_product'),
   )

class RecipeAdmin(admin.ModelAdmin):
   view_on_site = True
   save_as = True    # Allow cloning items by replacing "save and add another"

   search_fields = ['name', 'description']
   list_display = ('name', 'updated_at', 'description')
   readonly_fields = ('created_at','updated_at','nutrition_data')
   fieldsets = (
      (None, {
         'fields': (
            ('name', 'serves',),
            ('description',),
            ('method'),
         ),
      }),
      ('Last Tested', {
            'classes': ('collapse',),
            'fields': (
               ('last_tested',),
            )
      }),
      ('Tags', {
            'classes': ('collapse',),
            'fields': (
               ('tags',),
            )
      }),
      ('Internal Properties', {
            'classes': ('collapse',),
            'fields': (
               ('created_at','updated_at'),
               ('slug',),
               ('nutrition_data',),
            )
      }),
   )
   inlines = [ComponentInlineAdmin]

admin.site.register(Recipe, RecipeAdmin)
