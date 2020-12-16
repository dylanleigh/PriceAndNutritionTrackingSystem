from django.db import transaction
from rest_framework import serializers

from targets.models import Target, Minimums, Maximums


class MaximumsSerializer(serializers.ModelSerializer):
   class Meta:
      model = Maximums
      exclude = ['of_target', 'id']


class MinimumsSerializer(serializers.ModelSerializer):
   class Meta:
      model = Minimums
      exclude = ['of_target', 'id']


class TargetSerializer(serializers.HyperlinkedModelSerializer):
   """
   Serialize a target
   """
   minimum = MinimumsSerializer()
   maximum = MaximumsSerializer()

   class Meta:
      model = Target
      fields = '__all__'
      read_only_fields = ['user']

   @transaction.atomic
   def create(self, validated_data):
      user = self.context['request'].user  # FIXME needs to be passed as extra context
      # Take min and max data off, save remainder as target, then save min and max
      min_data = validated_data.pop('minimum')
      max_data = validated_data.pop('maximum')
      target = Target.objects.create(
         user=user,
         **validated_data)
      min_data["of_target_id"] = target.id
      max_data["of_target_id"] = target.id
      min = Minimums.objects.create(**min_data)
      target.minimum = min
      max = Maximums.objects.create(**max_data)
      target.maximum = max
      return target
