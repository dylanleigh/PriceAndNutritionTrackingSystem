# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Target, Minimums, Maximums

class MinimumInlineAdmin(admin.TabularInline):
   model = Minimums
   fk_name = "of_target"
   fields = (
      ('kilojoules','protein','fibre','carbohydrate','fat','sugar','saturatedfat','sodium','cost'),
   )

class MaximumInlineAdmin(admin.TabularInline):
   model = Maximums
   fk_name = "of_target"
   fields = (
      ('kilojoules','protein','fibre','carbohydrate','fat','sugar','saturatedfat','sodium','cost'),
   )

class TargetAdmin(admin.ModelAdmin):
   save_as = True    # Allow cloning items by replacing "save and add another"
   search_fields = ['name', 'description']
   list_display = ('name', 'updated_at', 'description')
   readonly_fields = ('created_at','updated_at')

   inlines = [MaximumInlineAdmin,MinimumInlineAdmin]

   fieldsets = (
      (None, {
       'fields': (
             ('name', 'user',),
             ('description',),
             ('daily_target',),
             ),
       }),
      ('Internal Properties', {
       'classes': ('collapse',),
       'fields': (
             ('created_at','updated_at'),
             ('slug',),
             )
       }),
      )


admin.site.register(Target, TargetAdmin)

