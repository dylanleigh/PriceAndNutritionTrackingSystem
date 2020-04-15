from rest_framework import serializers

from .models import Recipe

# FIXME componentserializer

class RecipeSerializer(serializers.HyperlinkedModelSerializer):
   nutrition_data = serializers.ReadOnlyField()       # Calculated values
   owner = serializers.ReadOnlyField()                # Current user or null, but immutable
   tags = serializers.StringRelatedField(many=True)
   flag = serializers.StringRelatedField()

   # FIXME mention this in README/api docs
   # Details of Components are not sent with recipes by default (as
   # they are not required for listing
   # FIXME should only be on detail call, not list
   # components = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

   class Meta:
      model = Recipe
      fields = '__all__'


