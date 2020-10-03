from django.db import transaction
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
   flag = CreatableSlugRelatedField(slug_field="name", allow_null=True, queryset=RecipeFlag.objects.all())

   # FIXME mention this in README/api docs, note there are two
   # serializers for Recipe
   # Details of Components are not sent with recipes by default (as
   # they are not required for listing)
   components = ComponentSerializer(many=True)

   @transaction.atomic
   def create(self, validated_data):
      user = self.context['request'].user  # FIXME needs to be passed as extra context
      # Take component and tag data off, save remainder as recipe, then save components and tags
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

   @transaction.atomic
   def update(self, recipe, validated_data):
      # Get all the requested update fields except for the many to many tags and components
      update_fields = [key for key in validated_data.keys() if key not in ['tags', 'components']]
      for key in update_fields:
         setattr(recipe, key, validated_data[key])
      recipe.save(update_fields=update_fields)

      if('tags' in validated_data):
         # Update the tags for this recipe, delete all previous tags first
         recipe.tags.clear()
         for tag_name in validated_data['tags']:
            new_tag = RecipeTag.objects.get_or_create(name=tag_name)[0]  # Returns a tuple, but we only want the object
            recipe.tags.add(new_tag)

      if('components' in validated_data):
         # Update the components for this recipe
         # @todo there is probably a more efficient way to do this, but for now clear and add is 'good enough'
         recipe.components.all().delete()
         for comp in validated_data['components']:
            comp['in_recipe_id'] = recipe.id
            new_component = Component.objects.create(**comp)
            recipe.components.add(new_component)


      return recipe

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

class RecipeFlagSerializer(serializers.ModelSerializer):
   """
   Serialize RecipeFlags
   """
   class Meta:
      model = RecipeFlag
      fields = '__all__'
