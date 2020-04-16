from rest_framework import serializers

from .models import Recipe, Component, RecipeTag, RecipeFlag


class ComponentSerializer(serializers.ModelSerializer):
   """
   Detail/Push (etc) serialiser for Recipe - includes nested Components
   """
   name = serializers.ReadOnlyField()
   class Meta:
      model = Component
      exclude = ['in_recipe'] # Redundant - only accessible nested within its recipe

class RecipeNestedSerializer(serializers.HyperlinkedModelSerializer):
   """
   Detail/Put serialiser for Recipe - includes nested Components
   """
   nutrition_data = serializers.ReadOnlyField()       # Calculated values
   owner = serializers.ReadOnlyField()                # Current user or null, but immutable
   tags = serializers.StringRelatedField(many=True)   # FIXME not editable yet
   flag = serializers.StringRelatedField()            # FIXME not editable yet

   # FIXME mention this in README/api docs, note there are two
   # serializers for Recipe
   # Details of Components are not sent with recipes by default (as
   # they are not required for listing)
   components = ComponentSerializer(many=True)

   def create(self, validated_data):
      user = self.request.user # FIXME needs to be passed as extra context
      # Take component data off, save remainder as recipe, then save components
      component_data = validated_data.pop('components')
      recipe = Recipe.objects.create(owner=user, **validated_data)
      for comp in component_data:
         Component.object.create(**comp)
      return recipe

   # FIXME TODO def update(self, validated_data):

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


