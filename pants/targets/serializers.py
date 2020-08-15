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

