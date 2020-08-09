from rest_framework import serializers

from ingredients.serializers import CreatableSlugRelatedField
from pants.models import UserSerializer
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
   tags = CreatableSlugRelatedField(slug_field="name", many=True, queryset=RecipeTag.objects.all())
   flag = serializers.StringRelatedField()            # FIXME not editable yet

   # FIXME mention this in README/api docs, note there are two
   # serializers for Recipe
   # Details of Components are not sent with recipes by default (as
   # they are not required for listing)
   components = ComponentSerializer(many=True)

   def create(self, validated_data):
      user = self.context['request'].user  # FIXME needs to be passed as extra context
      # Take component data off, save remainder as recipe, then save components
      component_data = validated_data.pop('components')
      tag_data = validated_data.pop('tags')
      recipe = Recipe.objects.create(
         #owner=user,
         **validated_data)
      for comp in component_data:
         comp['in_recipe_id'] = recipe.id
         new_component = Component.objects.create(**comp)
         recipe.components.add(new_component)
      for tag_name in tag_data:
         new_tag = RecipeTag.objects.get_or_create(name=tag_name)[0]  # Returns a tuple, but we only want the object
         recipe.tags.add(new_tag)


      return recipe

   # FIXME TODO def update(self, validated_data):

   class Meta:
      model = Recipe
      fields = '__all__'
      read_only_fields = ['owner']


class RecipeListSerializer(serializers.HyperlinkedModelSerializer):
   """
   List serialiser for Recipe - does not include nested Components
   (nutrition_data calculated from the components is included)
   """
   nutrition_data = serializers.ReadOnlyField()       # Calculated values
   tags = serializers.StringRelatedField(many=True)
   flag = serializers.StringRelatedField()

   class Meta:
      model = Recipe
      fields = '__all__'
      read_only_fields = ['owner']

class RecipeTagSerializer(serializers.HyperlinkedModelSerializer):
   """
   Serialize RecipeTags
   """
   class Meta:
      model = RecipeTag
      fields = '__all__'
