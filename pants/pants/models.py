from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Only here to allow hyperlinking to owners in recipes/tags
    This is NOT to allow any edits
    """
    class Meta:
        model = User
        fields = ("username", "first_name")
        read_only_fields = fields  # This is to prevent any editing
