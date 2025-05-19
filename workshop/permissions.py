from rest_framework.permissions import BasePermission
from django.contrib.auth import authenticate
from rest_framework.exceptions import PermissionDenied

class RequireSuperuserConfirmation(BasePermission):
    """
    Permission that requires confirmation of superuser credentials
    for sensitive actions performed by staff users.
    """

    def has_permission(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True

        if request.user.is_superuser:
            return True

        superuser_username = request.data.get('superuser_username')
        superuser_password = request.data.get('superuser_password')

        if not superuser_username or not superuser_password:
            raise PermissionDenied('Superuser credentials are required for this action.')

        superuser = authenticate(username=superuser_username, password=superuser_password)

        if superuser and superuser.is_superuser:
            return True

        raise PermissionDenied('Invalid superuser credentials or user is not a superuser.')
