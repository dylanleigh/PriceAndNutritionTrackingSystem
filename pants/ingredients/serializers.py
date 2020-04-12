from rest_framework import serializers

from .models import Ingredient

class IngredientSerializer(serializers.HyperlinkedModelSerializer):
   nutrition_data = serializers.ReadOnlyField()


   class Meta:
      model = Ingredient

      # Note that the nutrition fields on Ingredient itself are
      # modifiable through the API, but those within nutrition_data
      # are calculated and read-only, so both have to be included
      exclude = ['tags']   # FIXME TODO need nested serialization



