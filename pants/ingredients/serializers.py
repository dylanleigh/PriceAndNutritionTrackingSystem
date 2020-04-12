from rest_framework import serializers

from .models import Ingredient

class IngredientSerializer(serializers.HyperlinkedModelSerializer):
   nutrition_data = serializers.ReadOnlyField()

   class Meta:
      model = Ingredient
      exclude = ['tags']   # FIXME TODO need nested serialization



