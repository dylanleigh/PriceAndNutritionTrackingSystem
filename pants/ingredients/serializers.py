from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_str
from rest_framework import serializers

from .models import Ingredient, IngredientTag

class CreatableSlugRelatedField(serializers.SlugRelatedField):
    """
    From: https://stackoverflow.com/questions/28009829/creating-and-saving-foreign-key-objects-using-a-slugrelatedfield
    TODO extract this some where common, as it's used for both Recipe and Ingredient Tags
    """

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get_or_create(**{self.slug_field: data})[0]
        except ObjectDoesNotExist:
            self.fail('does_not_exist', slug_name=self.slug_field, value=smart_str(data))
        except (TypeError, ValueError):
            self.fail('invalid')

class IngredientSerializer(serializers.HyperlinkedModelSerializer):
    nutrition_data = serializers.ReadOnlyField()  # Calculated values
    owner = serializers.ReadOnlyField()  # Current user or null, but immutable

    tags = CreatableSlugRelatedField(slug_field="name", many=True, queryset=IngredientTag.objects.all())

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


class IngredientTagSerializer(serializers.HyperlinkedModelSerializer):



    class Meta:
        model = IngredientTag
        fields = "__all__"
