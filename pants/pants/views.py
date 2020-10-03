from django.contrib.auth.models import User
from rest_framework import viewsets, permissions

from pants.models import UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows User entries to be viewed only
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    queryset = User.objects.none()  # Required for DjangoModelPermissions to get Model

    def get_queryset(self):
       user = self.request.user
       return User.objects.filter(username=user.username)