from rest_framework import serializers

from .models import Ingredient

class IngredientSerializer(serializers.HyperlinkedModelSerializer):
   nutrition_data = serializers.ReadOnlyField()       # Calculated values
   owner = serializers.ReadOnlyField()                # Current user or null, but immutable
   tags = serializers.StringRelatedField(many=True)

   class Meta:
      model = Ingredient
      fields = '__all__'

      # FIXME these comments should go in readme/api docs
      # Note that the nutrition fields on Ingredient itself are
      # modifiable through the API, but those within nutrition_data
      # are calculated and read-only, so both have to be included.

      # The best price per kg data is included as part of
      # nutrition_data, so detailed prices are not included in
      # ingredient by default - they must be fetched separately to
      # show exact price/supplier breakdown.

