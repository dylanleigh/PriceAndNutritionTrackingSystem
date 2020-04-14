from rest_framework import serializers

from .models import Recipe

class RecipeSerializer(serializers.HyperlinkedModelSerializer):
   nutrition_data = serializers.ReadOnlyField()       # Calculated values
   owner = serializers.ReadOnlyField()                # Current user or null, but immutable
   tags = serializers.StringRelatedField(many=True)
   flag = serializers.StringRelatedField()

   class Meta:
      model = Recipe
      fields = '__all__'
