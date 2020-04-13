from rest_framework import serializers

from .models import Recipe

class RecipeSerializer(serializers.HyperlinkedModelSerializer):
   nutrition_data = serializers.ReadOnlyField()
   owner = serializers.ReadOnlyField()

   class Meta:
      model = Recipe
      exclude = ['tags','flag']   # FIXME TODO need nested serialization
