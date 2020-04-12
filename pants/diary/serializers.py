from rest_framework import serializers

from .models import DiaryFood

class DiaryFoodSerializer(serializers.HyperlinkedModelSerializer):
   nutrition_data = serializers.ReadOnlyField()

   class Meta:
      model = DiaryFood

      # Includes all fields except user (already filtered to the
      # logged in user).
      # Note DiaryFood entries of an Ingredient/Recipe are
      # crystallized to the DiaryFood, so returned nutrition data is
      # of this object, not it's relations. The fields on the object
      # itself are editable; nutrition_data is calculated and is
      # read-only.

      # FIXME re-include Ingredient/Recipe when they have API endpoints too

      exclude = ['user', 'of_recipe',]

