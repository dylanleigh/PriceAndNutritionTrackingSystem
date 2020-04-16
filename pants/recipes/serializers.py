from rest_framework import serializers

from .models import Recipe, Component, RecipeTag, RecipeFlag


class ComponentSerializer(serializers.ModelSerializer):
   """
   Detail/Push (etc) serialiser for Recipe - includes nested Components
   """
   # FIXME should show string of the linked recipe/ingredient as well as PK
   name = serializers.ReadOnlyField()
   class Meta:
      model = Component
      fields = '__all__'

class RecipeNestedSerializer(serializers.HyperlinkedModelSerializer):
   """
   Detail/Put serialiser for Recipe - includes nested Components
   """
   nutrition_data = serializers.ReadOnlyField()       # Calculated values
   owner = serializers.ReadOnlyField()                # Current user or null, but immutable
   tags = serializers.StringRelatedField(many=True)
   flag = serializers.StringRelatedField()

   # FIXME mention this in README/api docs, note there are two
   # serializers for Recipe
   # Details of Components are not sent with recipes by default (as
   # they are not required for listing)
   components = ComponentSerializer(many=True)

   class Meta:
      model = Recipe
      fields = '__all__'


class RecipeListSerializer(serializers.HyperlinkedModelSerializer):
   """
   List serialiser for Recipe - does not include nested Components
   (nutrition_data calculated from the components is included)
   """
   nutrition_data = serializers.ReadOnlyField()       # Calculated values
   owner = serializers.ReadOnlyField()                # Current user or null, but immutable
   tags = serializers.StringRelatedField(many=True)
   flag = serializers.StringRelatedField()

   class Meta:
      model = Recipe
      fields = '__all__'


