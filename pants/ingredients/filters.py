
import django_filters

from .models import Ingredient

class IngredientFilter(django_filters.FilterSet):
   class Meta:
      model = Ingredient
      fields = {
         'tags': ['exact',],
         'kilojoules':  ['lt', 'gt'],
      }
      # TODO: Updated at? Name?
      # TODO: Ndata stuff?
