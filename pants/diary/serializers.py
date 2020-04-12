from rest_framework import serializers

from .models import DiaryFood

class DiaryFoodSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
      model = DiaryFood

      # Includes all fields, (inherits the nutrition fields from
      # AbstractBaseNutrients), but not nutrition_data.
      # FIXME Needs nutrition_data for display

      # Note DiaryFood entries of an Ingredient/Recipe are
      # crystallized to the DiaryFood, so no need to recurse to them
      # to get nutrition data (just the name or link to detail page, etc)

      # Always the logged in user
      # FIXME re-include Ingredient/Recipe when they have API endpoints too

      exclude = ['user', 'of_recipe', 'of_ingredient']


