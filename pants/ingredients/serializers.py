from rest_framework import serializers

from .models import Ingredient

class IngredientSerializer(serializers.HyperlinkedModelSerializer):
   nutrition_data = serializers.ReadOnlyField()
   owner = serializers.ReadOnlyField()


   class Meta:
      model = Ingredient

      # FIXME these comments should go in readme/api docs
      # Note that the nutrition fields on Ingredient itself are
      # modifiable through the API, but those within nutrition_data
      # are calculated and read-only, so both have to be included.

      # The best price per kg data is included as part of
      # nutrition_data, so detailed prices are not included in
      # ingredient by default - they must be fetched separately to
      # show exact price/supplier breakdown.

      exclude = ['tags']   # FIXME TODO need nested serialization
