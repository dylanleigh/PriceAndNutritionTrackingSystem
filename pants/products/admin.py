# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Supplier,Product,Price

# admin.site.register(Price)    # rm in favour of inline only

class ProductAdmin(admin.ModelAdmin):
   save_as = True    # Allow cloning items by replacing "save and add another"

   list_display = ('name', 'brand', 'ingredient', 'updated_at',)
   search_fields = ['name', 'description', 'brand']
   readonly_fields = ('created_at','updated_at')
   fieldsets = (
      (None, {
         'fields': (
            ('brand', 'name',),
            ('ingredient', 'description'),
         ),
      }),
      ('Internal Properties', {
            'classes': ('collapse',),
            'fields': (
               ('slug',),
               ('created_at','updated_at'),
            )
      }),
   )
admin.site.register(Product,ProductAdmin)

class SupplierAdmin(admin.ModelAdmin):
   list_display = ('name', 'description', 'product_count', 'updated_at',)
admin.site.register(Supplier, SupplierAdmin)

