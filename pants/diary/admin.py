from django.contrib import admin

from .models import DiaryFood

class DiaryFoodAdmin(admin.ModelAdmin):
   save_as = True    # Allow cloning items by replacing "save and add another"
                     # with "save as new" when editing existing objects. FIXME BLOG

   list_display = ('start_time', 'user', 'weight', 'servings', 'name')
   search_fields = ['name']
   readonly_fields = ('created_at','updated_at')
   fieldsets = (
      (None, {
         'fields': (
            ('start_time','user','name'),
         ),
      }),
      ('Source', {
         'fields': (
            ('weight','servings','cost'),
            ('of_ingredient', 'of_recipe', 'of_product'),
         ),
      }),
      ('Nutrients', {
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
   )


# Register your models here.
admin.site.register(DiaryFood,DiaryFoodAdmin)   # TODO custom admin?
